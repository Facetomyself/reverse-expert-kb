# oracle-gateway

## 1. Identity
- Host label: `oracle-gateway`
- Static hostname: `24-7-10-2055`
- Provider: Oracle Cloud
- Primary role: gateway / relay / custom DERP host
- SSH alias: `oracle-gateway`
- Main purpose: 当前承担 Hysteria 网关 + 自建 Tailscale DERP 角色；历史上的 docker/registry proxy 职能已退役，旧 registry/Harbor 残留也已按用户要求永久删除

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
- `derper` — Tailscale custom DERP server on TCP `80/443` and UDP `3478` for `derp.zhangxuemin.work` (deployed 2026-04-03)
- `caddy` — retained locally for the legacy `backup.zhangxuemin.work` content path, but no longer on public `80/443`; now shifted to alternate local ports with admin API on `127.0.0.1:2019`

Historical / inactive footprints:
- old registry proxy containers were removed on 2026-03-25 after migration to `oracle-registry`
- old registry and Harbor residual files were permanently deleted on 2026-03-25 per user instruction

## 6. Machine-Level Infrastructure Notes
- as of 2026-04-03, the public listener set is intentionally split by protocol/function:
  - TCP `80/443` -> `derper`
  - UDP `3478` -> `derper` STUN
  - UDP `443` -> `hysteria`
  - TCP `8080/8443` -> local `caddy` fallback content path for legacy `backup.zhangxuemin.work` handling
  - Caddy admin remains on `127.0.0.1:2019`
- recurring 2026-03-26 check showed the expected focused runtime only: one `hysteria` container, host `caddy`, idle load, `32G` free on root, and light swap use (`91Mi / 2.0Gi`)
- memory remains the main caution on this host: it is stable, but still a small box with limited free RAM and light swap use
- current runtime should be treated as gateway-only; the older registry-proxy surface is now historical rather than live
- a temporary browser-authenticated upload channel was successfully staged here on 2026-03-27 using host Caddy + a localhost Python backend; the public route had already been removed after transfer, and the stale `/tmp-upload` Caddyfile block was finally pruned on 2026-04-04 so config now matches the intended reduced helper role. Reusable host-side notes/scripts were retained under `~/.tmp-upload-gateway/` and uploaded payloads remained under `~/tmp-upload-drop`

## 7. Documentation Scope
This host's docs should focus on:
- the live Hysteria gateway runtime
- the live custom DERP runtime on `derp.zhangxuemin.work`
- the reduced/local-only retained Caddy behavior around `backup.zhangxuemin.work`
- low-memory operational constraints
- the distinction between the current gateway role and the now-retired docker/registry/Harbor history
