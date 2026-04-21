# hk-relay / NETWORK

## 1. Public Network Identity
- Public IP: `154.86.30.10`
- Canonical domain: `hk.zhangxuemin.work`
- Additional domains:
  - `drop.hk.zhangxuemin.work`
  - `clash.hk.zhangxuemin.work`
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
- TCP `8080` -> authenticated Caddy browse/download entry for `hk.zhangxuemin.work`
- TCP `8088` -> local `dufs` upload/download backend (publicly surfaced via `drop.hk.zhangxuemin.work` through Caddy reverse proxy)
- TCP `8443` -> sing-box VLESS + Reality inbound
- UDP `8444` -> sing-box Hysteria2 inbound
- TCP `443` -> Caddy HTTPS front door serving:
  - `hk.zhangxuemin.work` (browse/download with Basic Auth)
  - `drop.hk.zhangxuemin.work` (HTTPS upload/download front door)
  - `clash.hk.zhangxuemin.work` (public Clash config download endpoint)
- TCP `80` -> ACME / HTTP redirect handling for the above hostnames

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

## 7. Current distribution endpoints
Validated on 2026-04-13, then hardened on 2026-04-21:
- `https://hk.zhangxuemin.work/` -> authenticated browse/download entry
- `https://drop.hk.zhangxuemin.work/` -> HTTPS upload/download entry backed by local `dufs`
- `https://clash.hk.zhangxuemin.work/` -> Clash distribution hostname, but YAML download now requires a randomized private path segment rather than the old public `/clash-meta.yaml`

Subscription hardening on 2026-04-21:
- legacy public paths `/clash-meta.yaml`, `/clash-compat.yaml`, and `/clash-classic.yaml` were disabled and now return 404
- active subscription files are served only from randomized private paths on the same host
- the exact secret path is intentionally not stored in repo-tracked docs; treat it as a credential

The published Clash config intentionally aggregates both newly deployed HK relay entries and pre-existing usable proxy entries, currently including:
- `hk-hy2`
- `hk-reality`
- `hk-socks`
- `hk-http`
- `oracle-gateway-hy2-backup`
- `ali-socks-oracle-egress`
- `ali-http-oracle-egress`

Runtime note confirmed on 2026-04-13:
- the HK relay services themselves were healthy (HTTP/SOCKS direct tests via `1080/1081` succeeded), but Clash-side HK node runtime only stabilized after the subscription was changed to use the bare server IP `154.86.30.10` for all HK node entries instead of `hk.zhangxuemin.work`
- keep `hk.zhangxuemin.work`, `drop.hk.zhangxuemin.work`, and `clash.hk.zhangxuemin.work` for web/file/distribution use
- for published proxy node definitions on this host, prefer IP literals over the hostname unless/until a specific client population proves domain-form entries are equally reliable
- for subscription sharing, do not publish repo-visible docs or public messages containing the randomized private path; rotate the path if it is ever widely exposed

## 8. To Be Confirmed
Still worth documenting once the host role is finalized:
- whether the initial Hysteria2 self-signed certificate should later be replaced with a domain-valid certificate for better client UX
- whether traffic monitoring / accounting / caps should be enforced on-host
- whether the provider offers a panel/API for monthly transfer inspection
- whether a dedicated file-transfer ingress (Caddy/Nginx/SFTP landing area) should become part of the standard design
