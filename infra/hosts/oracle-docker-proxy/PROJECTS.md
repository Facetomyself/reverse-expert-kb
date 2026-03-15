# oracle-docker-proxy / PROJECTS

## Summary
This host has not yet been SSH-audited. The current page is a DNS-driven placeholder created from the 2026-03-15 Cloudflare export.

## Suspected project groups
### 1. Registry / mirror / proxy endpoints
Likely represented by:
- `gcr.zhangxuemin.work`
- `ghcr.zhangxuemin.work`
- `k8sgcr.zhangxuemin.work`
- `mcr.zhangxuemin.work`
- `nvcr.zhangxuemin.work`
- `quay.zhangxuemin.work`
- `hub.zhangxuemin.work`
- `hubcmd.zhangxuemin.work`

### 2. UI / panel
Likely represented by:
- `ui.zhangxuemin.work`

### 3. Backup / misc
Likely represented by:
- `backup.zhangxuemin.work`
- `elastic.zhangxuemin.work`

## Current status
- Host identity: confirmed by SSH
- Runtime topology: confirmed at front-door and container-port level
- Front-door reverse proxy: Caddy (`/etc/caddy/Caddyfile`)
- Project docs: not yet created

## Confirmed external behavior
- `hub.zhangxuemin.work` returns `HTTP 200` behind Caddy
- `ghcr.zhangxuemin.work` returns `HTTP 200` behind Caddy
- `gcr.zhangxuemin.work` returns `HTTP 200` behind Caddy
- `quay.zhangxuemin.work` returns `HTTP 200` behind Caddy
- `ui.zhangxuemin.work` currently returns `HTTP 502` behind Caddy

## Confirmed runtime components
- `registry-ui` -> host `50000` -> container `8080`
- `hubcmd-ui` -> host `30080` -> container `3000`
- `reg-docker-hub` -> host `51000` -> container `5000`
- `reg-ghcr` -> host `52000` -> container `5000`
- `reg-gcr` -> host `53000` -> container `5000`
- `reg-k8s-gcr` -> host `54000` -> container `5000`
- `reg-k8s` -> host `55000` -> container `5000`
- `reg-quay` -> host `56000` -> container `5000`
- `reg-mcr` -> host `57000` -> container `5000`
- `reg-elastic` -> host `58000` -> container `5000`
- `reg-nvcr` -> host `59000` -> container `5000`

## Known issue
- `ui.zhangxuemin.work` -> `localhost:50000` currently fails locally with `Recv failure: Connection reset by peer`, which aligns with the external `HTTP 502` from Caddy.

## Harbor stack / adjacent deployment clue
On-host, a full Harbor deployment tree exists under `/root/harbor`, including:
- `/root/harbor/docker-compose.yml`
- `/root/harbor/harbor.yml`
- `/root/harbor/common/...`

Important current conclusion:
- Harbor deployment files and data paths exist
- but no Harbor containers are currently running
- the currently exposed registry services are the custom Caddy-fronted `dqzboy/*` stack, not active Harbor runtime containers

This suggests the machine has both:
- a custom Caddy-fronted registry-proxy stack (`dqzboy/registry`, `registry-ui`, `hubcmd-ui`)
- and a dormant or at least currently inactive Harbor deployment footprint using `/data/...`

## Current project docs
- `projects/caddy.md`
- `projects/registry-proxies.md`
- `projects/registry-ui.md`
- `projects/hubcmd-ui.md`

## Next operational step
Deepen the relationship between the custom registry proxy stack and `/root/harbor` by checking:
- whether Harbor containers are currently running or dormant
- how `/data/registry-proxy/*` relates to `/data/registry`
- whether the registry UI issue is app-version/media-type related rather than infrastructure-level
