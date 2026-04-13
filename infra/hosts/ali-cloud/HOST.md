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

## 5. High-Level Service Map
Current observed runtime:
- `1panel.service` active
- `easyimage` container active on `10086`
- `camoufox-remote` container active on `39222`
- host port `80` is owned by `1panel`

Current Camoufox exposure model:
- public websocket endpoint: `ws://106.15.239.221:39222/camoufox`
- no documented fronting TLS or auth proxy on top of `39222`
- service is manually maintained outside 1Panel app management

## 6. Machine-Level Infrastructure Notes
- 1Panel is installed under `/opt/1panel`
- 1Panel database present at `/opt/1panel/db/1Panel.db`
- 1Panel logs under `/opt/1panel/log/`
- `camoufox-remote` appears manually deployed under `/opt/camoufox-remote`
- preferred dependable foreign egress path on this host is now the local Hysteria SOCKS5 path at `127.0.0.1:18080`
- 2026-04-13 runtime verification confirmed the domestic proxy gateway is currently implemented as a two-layer stack:
  - `hysteria-egress.service` -> docker-compose in `/opt/hysteria-egress`
  - `sing-box-gateway.service` -> docker-compose in `/opt/sing-box-gateway`
- Current data path:
  - authenticated public SOCKS5 `:2080` and HTTP `:2081` are exposed by sing-box
  - sing-box now fronts a selector-style outbound tag `proxy`
  - default selection remains `oracle-egress`
  - `oracle-egress` points to local SOCKS5 `127.0.0.1:18080`
  - `127.0.0.1:18080` is provided by the Hysteria client in `/opt/hysteria-egress/client.yaml`
  - that Hysteria client currently dials `backup.zhangxuemin.work:443`
  - additional candidate upstream exits are now staged inside the same sing-box gateway config: `hk-hy2`, `hk-reality`, `hk-socks`, `hk-http`
- Operational helper installed on 2026-04-13:
  - `/usr/local/bin/ali-cloud-proxy-select status`
  - `/usr/local/bin/ali-cloud-proxy-select oracle-egress|hk-hy2|hk-reality|hk-socks|hk-http`

## 7. Documentation Scope
This host should document:
- 1Panel itself as the machine control plane
- EasyImages app deployment under 1Panel
- standalone camoufox remote service
- explicit-proxy gateway responsibilities for domestic hosts
- the current sing-box -> local Hysteria -> `oracle-gateway` egress chain used by domestic servers
