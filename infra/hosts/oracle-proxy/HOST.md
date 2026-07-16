# oracle-proxy

## 1. Identity
- Host label: `oracle-proxy`
- Static hostname: `24-7-10-2039`
- Provider: Oracle Cloud
- Primary role: utility / proxy host
- SSH alias: `oracle-proxy`
- Main purpose: 承载 Tavily Proxy、ExaFree 注册服务、Grok 相关求解/转发组件、CLI proxy 等对外或半对外服务

## 2. System Baseline
- OS: Ubuntu 20.04.6 LTS (Focal)
- Kernel: `5.15.0-1081-oracle`
- Architecture: `arm64 / aarch64`
- CPU: 1 vCPU (`Neoverse-N1`)
- Memory: 11 GiB
- Swap: none
- Root disk: 45G total / 18G used / 28G free (snapshot time)

## 3. Usage Pattern
- Host style: 长期运行型“pet”主机，不是可随手销毁重建的 cattle
- Change sensitivity: 中高；多个项目共享这台机器，错误修改容易互相影响
- Operational preference: 优先做增量修改，改完立刻验证端口、容器状态和关键接口

## 4. Access Notes
- Main SSH alias: `oracle-proxy`
- Expected user: `root`
- Useful first checks:
  ```bash
  ssh oracle-proxy
  hostnamectl
  docker ps
  ss -ltnp
  ```

## 5. High-Level Service Map
当前确认运行中的主要服务：
- `proxy-tavily-proxy-1` — Tavily key pool + Web console + API proxy
- `grok2api` — Grok API bridge on port 8000
- `cliproxy` — CLI proxy service on port 8317
- `exafree` — Exa 注册 / 刷新 / 管理面板服务 on port 7860
- `kiro-rs` — Rust Anthropic-compatible Kiro proxy on loopback port 18769
- `nginx` — 系统级默认 Nginx（当前只见默认站点 `/var/www/html`）
- `sing-box` — 独立代理/订阅栈，自带一套专用 nginx 和多协议入站配置
- `xray` — 独立代理服务，使用 `/etc/v2ray-agent/xray/conf`
- `cloudflared` — 从监听端口看有本地实例痕迹，但当前 systemd 细节未取到完整配置

## 6. Machine-Level Infrastructure Notes
### nginx / 1Panel
- systemd `nginx.service` 仍然存在于主机上，但本轮 `ss -ltnp` 看到 `0.0.0.0:80` 实际由 `1panel` 进程占用
- 这说明较早文档里“系统 nginx 直接监听 80 并提供默认站点”的描述已经过时，至少当前公共 `:80` 前门应优先视为 `1panel` 所拥有
- 当前机器上仍可见 Debian 默认站点配置痕迹（`/etc/nginx/sites-enabled/default`），但它不应再被当作当前 `:80` 实际入口的唯一依据
- 目前仍未在系统 nginx 配置中确认到明确的 `proxy_pass` 映射到 Tavily / grok2api / cliproxy

### sing-box
- systemd `sing-box.service` 运行中
- 使用 `/etc/sing-box/conf/` 目录化配置
- 同一 service cgroup 下还带一套 `/etc/sing-box/nginx.conf` 的 nginx 进程
- 暴露多组 30001、30004-30011 端口，显然承担代理/订阅用途

### xray
- systemd `xray.service` 运行中
- 使用 `-confdir /etc/v2ray-agent/xray/conf`
- 监听 `127.0.0.1:45987` 和 `*:14391`
- 需要后续单独梳理其协议、入口和与 sing-box 的边界

### cloudflared
- 本机监听曾见 `127.0.0.1:20241`，但本轮未抓到完整 systemd/config 信息
- 后续需要补一轮单独确认其 tunnel 角色

## 7. Documentation Scope
本主机目录的文档重点覆盖：
- Tavily 相关完整链路
- Grok/Grok2API 的基本运维入口
- cliproxy 的基本入口
- 机器级网络服务的第一轮角色说明

## 8. Non-Running Migrated Material
- `/root/OpenAi`：2026-03-16 从当前 OpenClaw 主机迁移到本机保存
- 当前状态：**仅迁移存放，未启动、未接入现有服务图、未视为线上运行项目**
- 运维含义：以后如果在本机看到该目录，不应默认推断它正在提供服务；必须单独检查进程、容器、端口或 systemd 后再下结论

后续仍需补全：
- sing-box / xray 的协议细节与用途拆分
- cloudflared 的具体 tunnel 配置
- 域名与反代拓扑的完整映射

### 2026-06-06 docs anti-abuse baseline
- `fail2ban` is now installed/enabled on this host for the public Kiro docs static site.
- Current docs-specific jails: `openclaw-docs-general`, `openclaw-docs-assets`.
- The jails read `/var/log/caddy/docs-access.log` and apply iptables bans for abusive request rates on HTTP/HTTPS.
- `hk-relay` (`154.86.30.10`) is intentionally in `ignoreip` so domestic edge traffic is not accidentally banned by the source host.

### 2026-06-06 card shop baseline
- `card-shop` now runs on this host as a loopback-only Docker service at `127.0.0.1:18767`.
- Runtime root: `/root/containers/card-shop`.
- Sensitive env: `/root/containers/card-shop/.env` (`0600`; contains admin password/session secret).
- Current card-shop fail2ban jails: `openclaw-card-general`, `openclaw-card-api`.

### 2026-06-07 retired container cleanup baseline
- The legacy Tavily registration scheduler/Camoufox runtime has been fully cleaned from Docker runtime: `tavily-scheduler`, `tavily-camoufox`, `tavily-camoufox-adapter` containers and their local images were removed.
- The legacy Grok register Camoufox solver stack has been fully cleaned from Docker runtime: `grok-register-camoufox`, `grok-register-camoufox-adapter` containers and their local images were removed.
- The old Grok register public adapter listener on `:15072` is no longer part of the active surface.
- On-host source directories were retained as retired archives, with root compose files renamed to `docker-compose.retired-20260607.yml` to avoid accidental restart.

### 2026-07-03 proxy4reverse MVP deployment
- `proxy4reverse` is deployed on this host as a loopback-only Docker Compose service under `/root/containers/proxy4reverse`.
- Container: `proxy4reverse`; compose project directory: `/root/containers/proxy4reverse`.
- Local proxy data-plane: `127.0.0.1:18773` -> container `1080`.
- Local web/API panel: `127.0.0.1:18772` -> container `5000`.
- Sensitive runtime files: `/root/containers/proxy4reverse/.env` and `/root/containers/proxy4reverse/config/config.ini` are mode `0600`; do not copy their values into docs or chat.
- Current provider config uses environment-backed Cliproxy credentials and profile mapping (`default`, `us-ca`, `us-ca-sticky-30`).
- Deployment status: service skeleton is healthy and authenticates clients, but Cliproxy upstream `us.cliproxy.io:1080` currently times out at TCP connect from this Oracle host, from `hk-relay`, and from the local OpenClaw host. Therefore no public/HK CN entrypoint has been enabled yet.
