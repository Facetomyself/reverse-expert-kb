# oracle-new1 / PROJECTS

## Summary
As of 2026-03-25, `oracle-new1` is no longer just a fresh ARM utility host. It now carries the live public registry-proxy front door that was migrated from `oracle-docker-proxy`.

## Active project groups
### 1. Registry / mirror / proxy endpoints
Current live public names intentionally served by this host:
- `hub.zhangxuemin.work`
- `ghcr.zhangxuemin.work`
- `k8s.zhangxuemin.work`
- `mcr.zhangxuemin.work`

Matching local runtime components:
- `reg-docker-hub` -> host `51000`
- `reg-ghcr` -> host `52000`
- `reg-k8s` -> host `55000`
- `reg-mcr` -> host `57000`

Shared implementation notes:
- image: `dqzboy/registry:latest`
- compose working dir: `/opt/registry-proxy`
- compose file: `/opt/registry-proxy/docker-compose.yml`
- shared cache/data dir: `/opt/registry-proxy/registry-data`
- backend config files:
  - `/opt/registry-proxy/registry-hub.yml`
  - `/opt/registry-proxy/registry-ghcr.yml`
  - `/opt/registry-proxy/registry-k8s.yml`
  - `/opt/registry-proxy/registry-mcr.yml`

### 2. Front-door routing
- `caddy` owns public `80/443`
- Caddy admin API listens on `127.0.0.1:2019`
- `/etc/caddy/Caddyfile` is the front-door source of truth for hostname -> localhost backend mapping

## Migration notes
- Cutover date: 2026-03-25
- Source host: `oracle-docker-proxy`
- Migration style: cold cutover without copying old cache data
- DNS for `hub/ghcr/k8s/mcr.zhangxuemin.work` was switched to `140.245.33.114`
- Old host containers were stopped after external validation on the new host succeeded
- Old host compose/data were intentionally retained for rollback

## Operational status
- Public HTTPS validation after cutover returned `HTTP/2 200` from `/v2/` for all four domains
- ACME issuance initially failed because local host iptables allowed only SSH; adding and persisting `80/tcp` and `443/tcp` fixed issuance
- This host should now be treated as the authoritative live front door for the four registry domains
