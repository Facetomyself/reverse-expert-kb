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
- Change sensitivity: medium-high; this is now a focused public gateway box with limited RAM, so avoid piling unrelated services back onto it
- Operational preference: 保持运行面精简，优先只保留确实在用的网关/分发组件，避免再把杂项 UI 或重型服务堆回这台机器

## 4. Access Notes
- Main SSH alias: `oracle-gateway`
- Expected user: `root`
- Tailnet IPv4: `100.116.171.76` (joined 2026-03-25)
- Tailscale-visible raw hostname currently remains `24-7-10-2055`; operationally this host should be treated as semantic identity `oracle-gateway`
- Useful first checks:
  ```bash
  ssh oracle-gateway
  hostnamectl
  tailscale ip -4
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
- current listener set is intentionally narrow: public `80/443`, UDP `443` for Hysteria, SSH, rpcbind, Caddy admin on `127.0.0.1:2019`, plus Tailscale listeners
- recurring 2026-03-26 check showed the expected focused runtime only: one `hysteria` container, host `caddy`, idle load, `32G` free on root, and light swap use (`91Mi / 2.0Gi`)
- memory remains the main caution on this host: it is stable, but still a small box with limited free RAM and light swap use
- current runtime should be treated as gateway-only; the older registry-proxy surface is now historical rather than live
- a temporary browser-authenticated upload channel was successfully staged here on 2026-03-27 using host Caddy + a localhost Python backend, then intentionally removed after file transfer; reusable host-side notes/scripts were retained under `~/.tmp-upload-gateway/` and uploaded payloads remained under `~/tmp-upload-drop`

## 7. Documentation Scope
This host's docs should focus on:
- the live Hysteria gateway runtime
- Caddy-delivered config/front-door behavior on `backup.zhangxuemin.work`
- low-memory operational constraints
- the distinction between the current gateway role and the now-retired registry/Harbor history
