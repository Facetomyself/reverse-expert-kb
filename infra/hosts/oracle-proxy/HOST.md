# oracle-proxy

## 1. Identity
- Host label: `oracle-proxy`
- Static hostname: `24-7-10-2039`
- Provider: Oracle Cloud
- Primary role: utility / proxy / registration host
- SSH alias: `oracle-proxy`
- Main purpose: 承载 Tavily 注册与代理、Grok 相关求解/转发组件、CLI proxy 等对外或半对外服务

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
- `tavily-scheduler` — Tavily 自动注册调度器
- `tavily-camoufox` / `tavily-camoufox-adapter` — Tavily 私有 Turnstile 求解链路
- `grok-register-camoufox` / `grok-register-camoufox-adapter` — Grok 独立求解链路
- `grok2api` — Grok API bridge on port 8000
- `cliproxy` — CLI proxy service on port 8317
- `nginx` — 系统级默认 Nginx（当前只见默认站点 `/var/www/html`）
- `sing-box` — 独立代理/订阅栈，自带一套专用 nginx 和多协议入站配置
- `xray` — 独立代理服务，使用 `/etc/v2ray-agent/xray/conf`
- `cloudflared` — 从监听端口看有本地实例痕迹，但当前 systemd 细节未取到完整配置

## 6. Machine-Level Infrastructure Notes
### nginx
- systemd `nginx.service` 运行中
- 当前 `/etc/nginx/sites-enabled/default` 为 Debian 默认站点
- 默认监听 `80`，根目录 `/var/www/html`
- 目前没有在系统 nginx 配置中看到明确的 `proxy_pass` 映射到 Tavily / grok2api / cliproxy

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

后续仍需补全：
- sing-box / xray 的协议细节与用途拆分
- cloudflared 的具体 tunnel 配置
- 域名与反代拓扑的完整映射
