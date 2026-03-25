# oracle-docker-proxy / PROJECTS

## Summary
This host has been SSH-audited and should no longer be treated as a DNS-only placeholder. The current live role is a reduced Caddy-fronted registry-proxy set on a small Oracle box.

## Active project groups
### 1. Registry / mirror / proxy endpoints
Historical stack preserved on disk under `/data/registry-proxy`, but no longer serving live traffic after the 2026-03-25 migration.

Former runtime components now stopped on this host:
- `reg-docker-hub` -> host `51000`
- `reg-ghcr` -> host `52000`
- `reg-k8s` -> host `55000`
- `reg-mcr` -> host `57000`

Current live public names have been migrated to `oracle-new1`:
- `hub.zhangxuemin.work`
- `ghcr.zhangxuemin.work`
- `k8s.zhangxuemin.work`
- `mcr.zhangxuemin.work`

### 2. Front-door routing
- old host `caddy` on this machine was stopped/disabled on 2026-03-25 after public validation succeeded on `oracle-new1`
- `/data/registry-proxy/docker-compose.yaml` and shared cache data were intentionally left in place for rollback

### 3. Attached / not-yet-fully-realized DNS
- `backup.zhangxuemin.work`
  - intentionally resolves to this host's IP
  - reaches Caddy over HTTP
  - not yet documented as a completed active HTTPS app/backend route

## Historical / inactive groups
These names/components should be treated as removed historical surface rather than current runtime:
- `ui.zhangxuemin.work` / `registry-ui`
- `hubcmd.zhangxuemin.work` / `hubcmd-ui`
- `gcr.zhangxuemin.work` / `reg-gcr`
- `k8sgcr.zhangxuemin.work` / `reg-k8s-gcr`
- `quay.zhangxuemin.work` / `reg-quay`
- `elastic.zhangxuemin.work` / `reg-elastic`
- `nvcr.zhangxuemin.work` / `reg-nvcr`

The stale Caddy routes for those backends were removed on 2026-03-21 so the front door now matches the reduced runtime.

## Current operational status
Recurring checks through 2026-03-23 show:
- host reachable and stable over SSH
- four long-lived registry proxy containers only
- root disk comfortable
- load idle
- memory still constrained enough that this should remain a lean utility host

## Harbor adjacency
Harbor files exist on-host under `/root/harbor`, but Harbor is not the live service surface.
Operationally, distinguish:
- active: custom Caddy + registry-proxy stack
- inactive: Harbor deployment footprint and removed UI residue

## Current project docs
- `projects/caddy.md`
- `projects/registry-proxies.md`
- `projects/registry-ui.md`
- `projects/hubcmd-ui.md`

## Next documentation follow-up
Only deepen docs further if there is a meaningful future change, such as:
- `backup.zhangxuemin.work` becoming a real routed service
- the reduced four-backend runtime changing again
- Harbor being intentionally reactivated
