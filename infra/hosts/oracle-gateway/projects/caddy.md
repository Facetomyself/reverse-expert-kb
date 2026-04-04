# caddy on oracle-gateway

## 1. Summary
This document is now mostly historical/auxiliary. Caddy is no longer the primary public front-door on this host. After the 2026-04-03 DERP cutover, public TCP `80/443` moved to `derper`, and host Caddy was retained only as a local helper on alternate ports for the legacy `backup.zhangxuemin.work` content path.

## 2. Access / Entry Points
- Current listeners: `*:8080`, `*:8443`
- Admin API: `127.0.0.1:2019`
- Config file: `/etc/caddy/Caddyfile`
- systemd unit: `caddy.service`
- Host SSH entry: `ssh oracle-gateway`

## 3. Deployment Layout
- Host-level Caddy installation managed by systemd
- Site config stored in a single `/etc/caddy/Caddyfile`
- Current role is reduced/local helper behavior only

## 4. Runtime Topology
Current retained behavior is centered around the legacy `backup.zhangxuemin.work` content path on alternate ports rather than the earlier registry front-door topology.

## 5. Purpose and Workflow
Caddy is now a helper layer for this host rather than its main public ingress. The primary public ingress is:
- `derper` on TCP `80/443`
- `hysteria` on UDP `443`

## 6. Configuration
- Main config file: `/etc/caddy/Caddyfile`
- Config validation works: `caddy validate --config /etc/caddy/Caddyfile`

## 7. Operations
### Validate config
```bash
ssh oracle-gateway
caddy validate --config /etc/caddy/Caddyfile
```

### Inspect current config
```bash
ssh oracle-gateway
sed -n '1,260p' /etc/caddy/Caddyfile
```

### Check listeners
```bash
ssh oracle-gateway
ss -ltnp | egrep ':(8080|8443|2019)\b'
```

## 8. Health Checks
Healthy signs:
- `caddy.service` active/running
- `*:8080` and `*:8443` listening
- expected local helper behavior remains intact when explicitly probed

## 9. Data and Persistence
- config persisted in `/etc/caddy/Caddyfile`
- certificate/storage paths not yet documented

## 10. Common Tasks
- inspect retained helper behavior around `backup.zhangxuemin.work`
- validate config before/after edits
- keep in mind that Caddy is no longer supposed to own public `80/443` on this host

## 11. Failure Modes / Troubleshooting
### Symptom: expected public DERP behavior is broken
Check the DERP doc first, not this Caddy doc.

### Symptom: helper content path is broken
Check:
- `/etc/caddy/Caddyfile`
- whether local helper backends still exist
- whether `caddy.service` is running

Known current status:
- On 2026-03-21 stale reverse-proxy routes for deleted/inactive backends were pruned from `/etc/caddy/Caddyfile`.
- On 2026-04-03, public TCP `80/443` were intentionally displaced by `derper`, and host Caddy was moved to alternate ports `8080/8443` so the host could serve as a proper custom DERP node.
- On 2026-04-04, a leftover `/tmp-upload` route block was removed from `/etc/caddy/Caddyfile`; Caddy now only retains the reduced helper behavior for the legacy `backup.zhangxuemin.work` content path.
- Treat the earlier registry-front-door description associated with this host as historical context, not as the current primary role.

## 12. Dependencies / Cross-links
- See `projects/hysteria-gateway.md`
- See host docs for the canonical current role

## 13. Change History
- 2026-03-15: First documented from on-host inspection.
- 2026-04-03: Reframed as a retained helper service after DERP cutover displaced Caddy from public `80/443`.
