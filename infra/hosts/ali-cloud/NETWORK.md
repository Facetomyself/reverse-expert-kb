# ali-cloud / NETWORK

## 1. Public Network Identity
- Public IP: `106.15.239.221`
- Provider: Alibaba Cloud

## 2. Current Listener Map
Observed listeners:
- `22/tcp` -> SSH
- `80/tcp` -> `1panel`
- `10086/tcp` -> Docker-published `easyimage`
- `39222/tcp` -> Docker-published `camoufox-remote`

## 3. Interpretation
This host exposes a small application surface:
- one panel/control-plane HTTP endpoint on `80`
- one app endpoint on `10086`
- one remote browser/automation endpoint on `39222`

For `39222`, the currently documented contract is a direct public websocket endpoint:
- `ws://106.15.239.221:39222/camoufox`
- no confirmed TLS termination or auth gateway currently documented in front of that port

## 4. DNS / Resolver Notes
2026-04-04 DNS diagnosis on-host found that `systemd-resolved` was using Alibaba-provided internal DNS servers from DHCP on `eth0`:
- `100.100.2.136`
- `100.100.2.138`

Observed impact:
- `tailscale status` warned: `Tailscale can't reach the configured DNS servers`
- direct DNS queries to both servers timed out
- host-level lookups intermittently failed through `127.0.0.53`
- Docker pulls and Hysteria client startup both broke on name resolution when they needed uncached lookups

Minimal corrective action applied on 2026-04-04:
- added `/etc/netplan/60-openclaw-dns.yaml`
- kept DHCP for addressing, but disabled DHCP-provided DNS on `eth0`
- pinned host resolver to public AliDNS resolvers:
  - `223.5.5.5`
  - `223.6.6.6`

Result after apply:
- `resolvectl status` for `eth0` showed `223.5.5.5 223.6.6.6`
- `dig registry-1.docker.io A` through local stub `127.0.0.53` succeeded
- Hysteria client on `ali-cloud` could resolve `backup.zhangxuemin.work` and connect successfully once the host had a valid path to DNS

Caveat still observed on 2026-04-04:
- although DNS was repaired, outbound HTTPS connectivity remained uneven for some targets
- `curl -I https://hub.zhangxuemin.work/v2/tobyxdd/hysteria/manifests/latest` succeeded from `ali-cloud`
- but `curl -4 -I https://registry-1.docker.io/v2/` still timed out
- Docker logs also continued to show `TLS handshake timeout` to `hub.zhangxuemin.work` for some pull attempts and fallback stalls against `registry-1.docker.io`

So the host had two distinct issues that day:
1. broken DNS (fixed by overriding DHCP DNS)
2. remaining outbound HTTPS / registry-path instability (not fully resolved yet)

## 5. To Be Confirmed
- whether `1panel` also serves an admin UI on a non-obvious path or additional port
- any bound domain names for `10086` / `39222`
- whether TLS termination exists elsewhere (CDN / reverse proxy / 1Panel site config)
- why direct HTTPS to some registry endpoints from this host still stalls even after DNS is fixed
