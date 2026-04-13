# oracle-gateway / PROJECTS

## Summary
`oracle-gateway` is a focused small-footprint gateway box. Its active role is simple:
- Hysteria relay
- retained helper Caddy on alternate ports

Historical docker/registry-proxy duties are no longer part of the active runtime and should not drive current operator decisions.

## Active project groups
### 1. Hysteria
- public `UDP 443`
- domain: `backup.zhangxuemin.work`
- deployment dir: `/opt/hysteria`

### 2. Retained helper Caddy
- no longer the public front door
- current alternate ports: `8080/8443`
- helper/runtime doc: `projects/caddy.md`

## Current operational status
- host reachable and stable over SSH
- live runtime intentionally reduced to `hysteria` + retained helper `caddy`
- memory remains constrained enough that the box should stay gateway-focused

## Historical / inactive surface
Removed historical roles:
- registry proxy / mirror front door
- registry UI / hubcmd UI
- Harbor residue and old mixed runtime

Registry-facing public names now belong to `oracle-registry`, not this host.

## Recommended operator checks
```bash
ssh oracle-gateway
ss -ltnup | egrep ':(443|8080|8443)'
docker ps
```

## Cross-links
- `projects/caddy.md`
- `HOST.md`
- `CHANGELOG.md`

## Documentation principle for this host
Keep this page focused on the current gateway role.
Detailed retired registry history should live in changelog/history notes, not in the active project summary.
