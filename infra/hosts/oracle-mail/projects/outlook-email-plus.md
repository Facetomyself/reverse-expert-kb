# Outlook Email Plus on `oracle-mail`

## Runtime shape
- Host: `oracle-mail` (`140.83.52.216`)
- Public front door: `https://mail.zhangxuemin.work`
- Compose root: `/opt/outlook-email-plus`
- Containers:
  - `outlook-email-plus-app`
  - `outlook-email-plus-caddy`

## 2026-04-18 inbound failure / DNS drift incident

### User-visible symptom
- The site itself stayed up, but opening inboxes started failing.
- App logs showed:
  - `GRAPH_TOKEN_EXCEPTION`
  - `EMAIL_PROXY_CONNECTION_FAILED`
  - `Failed to resolve 'login.microsoftonline.com'`
- Caddy logs in the same window also showed ACME renewal lookups timing out against `acme-v02.api.letsencrypt.org`.

### What was ruled out
- `mail.zhangxuemin.work` public DNS was still correct and reachable.
- HTTPS front door, redirect behavior, and the current Let's Encrypt certificate were all healthy.
- This was **not** explained by the earlier Cloudflare cleanup of historical `autoconfig` / `autodiscover` / Mailu / moemail leftovers.

### Root cause
The running Docker containers had stale DNS upstreams in their generated `resolv.conf`:
- Docker internal resolver: `127.0.0.11`
- stale upstreams: `100.100.100.100`
- stale search domain evidence: old tailnet search suffix present in container resolver comments

At the same time, the host itself had already moved back to the OCI resolver:
- host `/etc/resolv.conf` nameserver: `169.254.169.254`

So the actual breakage was:
- host DNS OK
- public site OK
- container outbound DNS broken
- Graph token fetch and Caddy ACME lookups failed as a consequence

### Remediation applied
Patched `/opt/outlook-email-plus/docker-compose.yml` to pin explicit DNS for both services:

```yaml
services:
  app:
    dns:
      - 169.254.169.254
      - 1.1.1.1

  caddy:
    dns:
      - 169.254.169.254
      - 1.1.1.1
```

Then force-recreated the containers:

```bash
cd /opt/outlook-email-plus
docker compose up -d --force-recreate --no-build app caddy
```

## Validation after repair
- Container `resolv.conf` now shows Docker internal resolver backed by:
  - `169.254.169.254`
  - `1.1.1.1`
- `outlook-email-plus-app` can again resolve:
  - `login.microsoftonline.com`
  - `acme-v02.api.letsencrypt.org`
- `outlook-email-plus-caddy` immediately resumed successful ACME renewal-info fetches after recreation.

## Practical lesson
If `mail.zhangxuemin.work` stays reachable but inbox/API calls suddenly throw Graph token / connection failures, check container DNS before blaming Cloudflare DNS cleanup.
