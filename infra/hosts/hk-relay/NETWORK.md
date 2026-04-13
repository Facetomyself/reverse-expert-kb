# hk-relay / NETWORK

## 1. Public Network Identity
- Public IP: `154.86.30.10`
- Canonical domain: `hk.zhangxuemin.work`
- Provider: unknown / user-added Hong Kong VPS
- Intended role: 三网优化流量中转

## 2. Current confirmed addressing
Observed on 2026-04-13:
- interface: `enp1s0`
- primary address: `154.86.30.10/24`
- default gateway: `154.86.30.254`
- DNS via cloud-init netplan:
  - `8.8.8.8`
  - `1.1.1.1`

## 3. Current listener surface
First baseline snapshot showed only:
- TCP `22` (`sshd`)
- local-only stub resolver on `127.0.0.53:53`

After relay bootstrap on 2026-04-13, confirmed public listener map:
- TCP `22` -> SSH
- TCP `1080` -> sing-box authenticated mixed inbound (proxy/tools/general-purpose entry)
- TCP `1081` -> sing-box authenticated HTTP proxy inbound
- TCP `8080` -> authenticated Caddy browse/download entry
- TCP `8088` -> authenticated `dufs` upload/download entry
- TCP `8443` -> sing-box VLESS + Reality inbound
- UDP `8444` -> sing-box Hysteria2 inbound

## 4. Egress validation
Validated on 2026-04-13:
- `https://www.google.com` reachable (`HTTP/2 200`)
- `https://github.com` reachable (`HTTP/2 200`)

Interpretation:
- outbound Internet access is available and appears healthy at baseline
- no additional bootstrap proxy/tunnel layer was required for ordinary foreign HTTPS reachability during first contact

## 5. Budget constraint
This machine has a user-declared **bidirectional monthly traffic cap of 800G**.

Operational implication:
- treat bandwidth usage as part of the network design, not just a billing footnote
- future services on this host should document whether they are expected to consume:
  - low steady-state control traffic
  - bursty download traffic
  - sustained relay/proxy traffic
- avoid undocumented large-image mirroring, package-cache hosting, or other silent high-egress roles here

## 6. Firewall baseline
Confirmed on 2026-04-13 with `ufw` active:
- allow `22/tcp`
- allow `1080/tcp`
- allow `1081/tcp`
- allow `8080/tcp`
- allow `8088/tcp`
- allow `8443/tcp`
- allow `8444/udp`

Interpretation:
- current exposure is intentionally wider than a minimal host because the machine is being positioned as a self-use multi-role relay node
- management surface is still relatively small because there is no public dashboard/admin panel exposed yet

## 7. To Be Confirmed
Still worth documenting once the host role is finalized:
- whether any domain names will be pointed here
- whether a real TLS certificate should replace the initial self-signed Hysteria2 bootstrap certificate
- whether traffic monitoring / accounting / caps should be enforced on-host
- whether the provider offers a panel/API for monthly transfer inspection
- whether a dedicated file-transfer ingress (Caddy/Nginx/SFTP landing area) should become part of the standard design
