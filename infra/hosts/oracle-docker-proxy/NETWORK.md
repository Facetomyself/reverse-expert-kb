# oracle-docker-proxy / NETWORK

## 1. Public Network Identity
- Public IP: `129.150.61.78`
- Provider: Oracle Cloud
- Domain group label from historical export comments: `docker_proxy`

## 2. Domains currently mapped here
No primary live public domains should now be treated as served by this host after the 2026-03-25 migration.

The following names historically lived here but were migrated to `oracle-new1` (`140.245.33.114`) and should now be treated as served there instead:
- `hub.zhangxuemin.work`
- `ghcr.zhangxuemin.work`
- `k8s.zhangxuemin.work`
- `mcr.zhangxuemin.work`

Additional DNS name currently pointed at this host's public IP, but not yet confirmed as an active application route:

- `backup.zhangxuemin.work`
  - DNS resolves to `129.150.61.78`
  - plain HTTP reaches host Caddy and returns `308 Permanent Redirect` to HTTPS
  - HTTPS currently fails with `tlsv1 alert internal error`
  - no explicit `backup.zhangxuemin.work` site block is currently present in `/etc/caddy/Caddyfile`

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

## 4. To Be Confirmed
- what exact intended purpose `backup.zhangxuemin.work` now serves on this host (it is intentionally pointed at this public IP and reaches Caddy over HTTP, but is not yet documented as an active HTTPS application route)
- whether `backup.zhangxuemin.work` should later get its own explicit Caddy site block / certificate path / backend mapping
- exact data volumes for each registry proxy
- any nginx/traefik/cloudflared involvement behind or alongside Caddy
