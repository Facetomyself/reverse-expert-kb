# oracle-gateway / NETWORK

## 1. Public Network Identity
- Public IP: `129.150.61.78`
- Provider: Oracle Cloud
- Domain group label from historical export comments: `docker_proxy`

## 2. Domains currently mapped here
No primary live public domains should now be treated as served by this host after the 2026-03-25 migration.

The following names historically lived here but were migrated to `oracle-registry` (`140.245.33.114`) and should now be treated as served there instead:
- `hub.zhangxuemin.work`
- `ghcr.zhangxuemin.work`
- `k8s.zhangxuemin.work`
- `mcr.zhangxuemin.work`

Additional active DNS names currently pointed at this host's public IP:

- `derp.zhangxuemin.work`
  - DNS resolves directly to `129.150.61.78` (Cloudflare proxy removed before DERP cutover)
  - TCP `80/443` serves `derper`
  - UDP `3478` serves DERP STUN
  - deployed on 2026-04-03 as the host's primary public TCP front door

- `backup.zhangxuemin.work`
  - DNS resolves to `129.150.61.78`
  - UDP `443` continues to serve Hysteria 2 traffic
  - historical TCP `443` Caddy service was displaced on 2026-04-03 by the DERP cutover
  - host-local Caddy content path was retained on alternate ports `8080/8443` instead of public `80/443`

Historical DNS/Caddy names formerly associated with this host but no longer served after the 2026-03-21 cleanup:

- `elastic.zhangxuemin.work`
- `gcr.zhangxuemin.work`
- `hubcmd.zhangxuemin.work`
- `k8sgcr.zhangxuemin.work`
- `nvcr.zhangxuemin.work`
- `quay.zhangxuemin.work`
- `ui.zhangxuemin.work`

## 3. Interpretation
This host is now best understood as a small shared Caddy front door for a reduced registry-proxy set, not the earlier broader historical domain surface.

Observed external probes after cleanup/state convergence on 2026-03-21:
- `https://hub.zhangxuemin.work` -> `HTTP/2 200`, `via: 1.1 Caddy`
- `https://ghcr.zhangxuemin.work` -> `HTTP/2 200`, `via: 1.1 Caddy`
- `https://k8s.zhangxuemin.work` -> `HTTP/2 200`, `via: 1.1 Caddy` (after DNS was added)
- `https://mcr.zhangxuemin.work` -> `HTTP/2 200`, `via: 1.1 Caddy`

Observed on-host listeners / mapping:
- Caddy listens on `*:80` and `*:443`
- Caddy admin API listens on `127.0.0.1:2019`
- As of 2026-03-21, only these backend listener ports actually exist on-host:
  - `51000` (`hub`)
  - `52000` (`ghcr`)
  - `55000` (`k8s`)
  - `57000` (`mcr`)
- `/etc/caddy/Caddyfile` now retains only these hostname -> localhost mappings:
  - `hub.zhangxuemin.work` -> `localhost:51000`
  - `ghcr.zhangxuemin.work` -> `localhost:52000`
  - `k8s.zhangxuemin.work` -> `localhost:55000`
  - `mcr.zhangxuemin.work` -> `localhost:57000`
- Local backend probe on 2026-03-21 confirmed these mapped ports answer locally:
  - `51000` (`hub`)
  - `52000` (`ghcr`)
  - `55000` (`k8s`)
  - `57000` (`mcr`)
- Removed stale Caddy route targets on 2026-03-21:
  - `50000`, `30080`, `53000`, `54000`, `56000`, `58000`, `59000`
- After cleanup, the previously stale public names (`ui`, `hubcmd`, `gcr`, `k8sgcr`, `quay`, `elastic`, `nvcr`) are no longer routed by Caddy on this host.
- `k8s.zhangxuemin.work` was briefly in an internal-only / no-public-DNS intermediate state during the cleanup, but DNS was added later on 2026-03-21 and the public route now resolves correctly to this host.

## 4. Current confirmed gateway exposure
Deployment validation on 2026-04-03 confirmed the live public surface is now split across DERP and Hysteria:
- `derp.zhangxuemin.work` is the primary public TCP entrypoint on this host
- host `derper` is active and listening on TCP `80/443`
- `derper` STUN is active on UDP `3478`
- Hysteria remains active on UDP `443`
- Tailscale remains joined with IPv4 `100.116.171.76`
- local validation confirmed:
  - `http://127.0.0.1` -> `302` redirect into DERP debug path
  - `https://derp.zhangxuemin.work` -> `HTTP/2 200`
  - `https://derp.zhangxuemin.work/debug/` renders the DERP debug page
- host `caddy` was intentionally moved off public `80/443` to alternate local ports `8080/8443` during the cutover so DERP could bind directly as required
- the old temporary upload helper backend on `127.0.0.1:18081` still exists as local residue behind Caddy config, but is no longer part of the primary public front door

## 5. Reusable temporary upload pattern
A validated ad-hoc upload pattern now exists for this host when the user needs browser-based file transfer without SSH on the sender side:
- front door: `backup.zhangxuemin.work`
- auth UX: browser-native HTTP Basic Auth popup
- Caddy path route: `/tmp-upload/`
- backend shape: local Python upload app bound to `127.0.0.1:18081`
- retained host-side notes/scripts: `~/.tmp-upload-gateway/`
- retained upload directory from the 2026-03-27 run: `~/tmp-upload-drop`

This pattern should be treated as reusable but normally disabled; only re-enable it for explicit short-lived transfer windows, then remove the public route afterward.

## 6. To Be Confirmed
- whether `backup.zhangxuemin.work` should later gain additional routed content beyond the current Clash Verge config distribution path
- exact long-term retention expectations for any future gateway-side config artifacts
- any future nginx/traefik/cloudflared involvement if the host role expands again
