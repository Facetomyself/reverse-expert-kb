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

### 3. Active gateway / relay surface
- `backup.zhangxuemin.work`
  - intentionally resolves to this host's IP
  - now serves as the Hysteria gateway domain on `:443`
  - TCP 443 is used by Caddy to serve a downloadable Clash Verge YAML at `/clash-verge.yaml`
  - UDP 443 is used by Hysteria 2 server traffic
  - current masquerade upstream is `https://dreamhorse.eu.cc/`

Authentication material is intentionally not stored in infra docs in full. Runtime currently uses:
- auth mode: password
- obfuscation: salamander
- deployment dir: `/opt/hysteria`
- config file: `/opt/hysteria/config.yaml`
- compose file: `/opt/hysteria/docker-compose.yml`

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
Current post-cutover / post-cleanup status on 2026-03-25:
- host reachable and stable over SSH
- live runtime intentionally reduced to `hysteria` + `caddy` only
- root disk still comfortable enough for lean gateway use
- memory remains constrained enough that this host should stay focused on gateway duties rather than regaining heavy mixed roles

## Cleanup / archive state
- stopped legacy registry containers were removed on 2026-03-25
- previous registry stack files were archived to:
  - `/root/retired-services/2026-03-25-oracle-gateway-cleanup/registry-proxy`
- Harbor residual files, if present, should also live under the same cleanup archive path rather than the live runtime surface
- this means the live operational distinction is now simple:
  - active: `hysteria` + `caddy`
  - archived: old registry / Harbor / UI residue

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
