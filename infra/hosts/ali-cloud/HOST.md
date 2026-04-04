# ali-cloud

## 1. Identity
- Host label: `ali-cloud`
- Static hostname: `iZuf658qfolzlj2t1l53uyZ`
- Provider: Alibaba Cloud ECS
- Primary role: lightweight app host with 1Panel-managed app(s) and a standalone camoufox remote service
- SSH alias: `ali-cloud`
- Main purpose: 承载 1Panel、EasyImages 图床，以及一个独立的 `camoufox-remote` 浏览器/自动化服务

## 2. System Baseline
- OS: Ubuntu 24.04.3 LTS
- Kernel: `6.8.0-90-generic`
- Architecture: `x86_64`
- Hardware vendor: Alibaba Cloud
- Hardware model: Alibaba Cloud ECS

## 3. Usage Pattern
- Host style: control-panel-managed pet host
- Change sensitivity: medium; at least one app is managed through 1Panel app lifecycle
- Operational preference: distinguish 1Panel-managed assets from manually deployed assets before making changes

## 4. Access Notes
- Main SSH alias: `ali-cloud`
- Expected user: `root`
- SSH auth: key-based login via local SSH config entry using `IdentityFile ~/.ssh/ali-cloud`
- Tailnet IPv4: `100.98.184.19` (joined 2026-03-25)
- Quick mental shortcut: machine-to-machine calls can now target `ali-cloud` directly over Tailnet instead of defaulting to public IP `106.15.239.221`

## 5. High-Level Service Map
Current observed runtime:
- `1panel.service` active
- `easyimage` container active on `10086`
- `camoufox-remote` container active on `39222`
- host port `80` is owned by `1panel`

2026-03-21 stability note:
- the host became SSH-unreachable before a manual reboot; post-reboot inspection showed repeated prior-boot global OOM events and watchdog fallout
- strongest working theory is memory exhaustion on this 1.6 GiB / no-swap host, with browser-side `WebExtensions` processes inside the Camoufox container family as the main pressure source
- low-risk mitigation applied:
  - enabled 2 GiB swap at `/swapfile`
  - set `vm.swappiness=10`
  - applied a Docker memory guardrail to `camoufox-remote`: `--memory 768m --memory-swap 1536m`
  - removed leftover local-only test container `camoufox-test`

Current Camoufox exposure model:
- public websocket endpoint: `ws://106.15.239.221:39222/camoufox`
- no documented fronting TLS or auth proxy on top of `39222`
- service is manually maintained outside 1Panel app management

## 6. Machine-Level Infrastructure Notes
- 1Panel is installed under `/opt/1panel`
- 1Panel database present at `/opt/1panel/db/1Panel.db`
- 1Panel logs under `/opt/1panel/log/`
- `camoufox-remote` appears manually deployed under `/opt/camoufox-remote`

## 7. Documentation Scope
This host should document:
- 1Panel itself as the machine control plane
- EasyImages app deployment under 1Panel
- standalone camoufox remote service

## 8. Operational posture update (2026-04-04)
- `hub.zhangxuemin.work` still exists as a self-hosted Docker Hub proxy front door, but it should no longer be treated as a life-support dependency for Docker pulls.
- Same-day deep-dive confirmed selected Docker Hub blobs could still fail with `blob unknown` even when the mirror returned healthy `/v2/` and manifest responses, and even after isolating Docker Hub onto a fresh dedicated cache directory.
- Preferred dependable path on this host is now: official registries over the local Hysteria SOCKS5 proxy at `127.0.0.1:18080`.
- Treat the self-hosted Docker Hub mirror as optional acceleration only.
