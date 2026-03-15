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
- Host identity: not yet confirmed by SSH
- Runtime topology: partially inferred from external probes
- Front-door reverse proxy: likely Caddy
- Project docs: not yet created

## Confirmed external behavior
- `hub.zhangxuemin.work` returns `HTTP 200` behind Caddy
- `ghcr.zhangxuemin.work` returns `HTTP 200` behind Caddy
- `gcr.zhangxuemin.work` returns `HTTP 200` behind Caddy
- `quay.zhangxuemin.work` returns `HTTP 200` behind Caddy
- `ui.zhangxuemin.work` currently returns `HTTP 502` behind Caddy

## Next operational step
Obtain the correct SSH identity/user for the machine behind `129.150.61.78`, then create:
- project-specific docs under `infra/hosts/oracle-docker-proxy/projects/`
- host-level service map
- Caddy config and backend mapping
- port-to-domain mapping
