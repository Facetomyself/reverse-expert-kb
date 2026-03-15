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
- `nginx` / `1panel` / `cloudflared` / `sing-box` / `xray` — 机器级网络与面板类组件（需后续继续细化）

## 6. Documentation Scope
本主机目录的文档重点覆盖：
- Tavily 相关完整链路
- Grok/Grok2API 的基本运维入口
- cliproxy 的基本入口

后续仍需补全：
- nginx / 1panel / sing-box / xray / cloudflared 的角色与配置关系
- 域名与反代拓扑的完整映射
