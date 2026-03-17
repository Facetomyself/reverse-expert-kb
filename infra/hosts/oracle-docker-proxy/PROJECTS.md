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
Observed on 2026-03-16:
- `hub.zhangxuemin.work` returns `HTTP 200` behind Caddy
- `ghcr.zhangxuemin.work` returns `HTTP 200` behind Caddy
- `mcr.zhangxuemin.work` returns `HTTP 200` behind Caddy
- `gcr.zhangxuemin.work` currently returns `HTTP 502` behind Caddy
- `quay.zhangxuemin.work` currently returns `HTTP 502` behind Caddy
- `ui.zhangxuemin.work` currently returns `HTTP 502` behind Caddy
- `hubcmd.zhangxuemin.work` currently returns `HTTP 502` behind Caddy
- `nvcr.zhangxuemin.work` currently returns `HTTP 502` behind Caddy
- `elastic.zhangxuemin.work` currently returns `HTTP 502` behind Caddy

## Confirmed runtime components
Currently running on 2026-03-16:
- `reg-docker-hub` -> host `51000` -> container `5000`
- `reg-ghcr` -> host `52000` -> container `5000`
- `reg-k8s` -> host `55000` -> container `5000`
- `reg-mcr` -> host `57000` -> container `5000`

Currently absent from `docker ps` and with backend ports refusing local connections on 2026-03-16:
- `registry-ui` -> expected host `50000`
- `hubcmd-ui` -> expected host `30080`
- `reg-gcr` -> expected host `53000`
- `reg-k8s-gcr` -> expected host `54000`
- `reg-quay` -> expected host `56000`
- `reg-elastic` -> expected host `58000`
- `reg-nvcr` -> expected host `59000`

## Known issue
- The current problem is broader than the earlier `registry-ui`-only diagnosis: several Caddy routes now point at inactive local backends, so today's `HTTP 502` responses line up with missing listeners rather than only OCI manifest/UI compatibility behavior.

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
