# oracle-registry / PROJECTS

## Summary
`oracle-registry` is the live registry front-door host for the current reduced registry proxy set.

## Active project groups
### 1. Registry / mirror front door
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

### 2. Front-door routing
- `caddy` owns public `80/443`
- `/etc/caddy/Caddyfile` is the hostname -> localhost backend source of truth
- health helper: `/usr/local/bin/check-registry-proxies`

## Current operational status
- host reachable and stable over SSH
- public `/v2/` validation for the four domains has repeatedly returned healthy registry responses
- this host should be treated as the authoritative live front door for the reduced registry set

## Historical note
The registry front door was migrated here from `oracle-gateway` on 2026-03-25.
That migration history matters operationally, but should not distract from the fact that this host is now the canonical live location.

## Recommended operator checks
```bash
ssh oracle-registry
/usr/local/bin/check-registry-proxies
docker ps
systemctl status caddy --no-pager
```

## Cross-links
- `HOST.md`
- `NETWORK.md`
- `CHANGELOG.md`

## Documentation principle for this host
Keep this page focused on the current live registry front door.
Detailed migration chronology belongs in `CHANGELOG.md`.
