# oracle-docker-proxy

## 1. Identity
- Host label: `oracle-docker-proxy`
- Static hostname: `24-7-10-2055`
- Provider: Oracle Cloud
- Primary role: former shared Docker/image proxy host (now rollback standby)
- SSH alias: `oracle-gateway` (legacy-compatible aliases `oracle-registry-legacy` and `oracle-docker_proxy` retained locally)
- Main purpose: 当前承担 Hysteria 网关/中转角色；历史上承载过 registry mirror/proxy 服务，但旧 registry/Harbor 残留已按用户要求永久删除

## 2. System Baseline
- OS: Ubuntu 20.04.6 LTS (Focal)
- Kernel: `5.15.0-1081-oracle`
- Architecture: `x86_64`
- Root disk: `45G total / 17G used / 29G free` (2026-03-23 snapshot)
- Memory: `952 MiB`
- Swap: `2.0 GiB`

## 3. Usage Pattern
- Host style: small-footprint long-lived utility host
- Change sensitivity: high; public registry proxy domains share the same front door and low-resource box
- Operational preference: 保持运行面精简，优先只保留确实在用的 registry backends，避免再把杂项 UI 或重型服务堆回这台机器

## 4. Access Notes
- Main SSH alias: `oracle-gateway`
- Expected user: `root`
- Tailnet IPv4: `100.116.171.76` (joined 2026-03-25)
- Useful first checks:
  ```bash
  ssh oracle-docker_proxy
  hostnamectl
  docker ps
  ss -ltnp
  caddy validate --config /etc/caddy/Caddyfile
  ```

## 5. High-Level Service Map
Current observed runtime:
- `hysteria` — Hysteria 2 gateway service on UDP `443`
- `caddy` — public HTTPS config-distribution front door on TCP `80/443`, with admin API on `127.0.0.1:2019`

Historical / inactive footprints:
- old registry proxy containers were removed on 2026-03-25 after migration to `oracle-registry`
- old registry and Harbor residual files were permanently deleted on 2026-03-25 per user instruction

## 6. Machine-Level Infrastructure Notes
- current listener set is intentionally narrow: public `80/443`, SSH, rpcbind, plus the four local registry backend ports
- recurring checks on 2026-03-20, 2026-03-21, and 2026-03-23 all show the same reduced four-container runtime
- memory remains the main caution on this host: it is stable, but still a small box with limited free RAM and light swap use
- current runtime no longer matches the earlier broader historical DNS surface; docs should treat the reduced registry set as the authoritative live role

## 7. Documentation Scope
This host's docs should focus on:
- the live reduced registry-proxy runtime
- Caddy hostname -> localhost backend mappings
- low-memory operational constraints
- the distinction between active custom registry proxies and inactive Harbor / removed UI residue
