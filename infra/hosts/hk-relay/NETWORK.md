# hk-relay / NETWORK

## 1. Public Network Identity
- Public IP: `154.86.30.10`
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

No public application listener map is documented yet.

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

## 6. To Be Confirmed
Still worth documenting once the host role is finalized:
- whether this machine will front HTTP, SOCKS5, Hysteria, sing-box, FRP, or another relay stack
- whether any domain names will be pointed here
- whether traffic monitoring / accounting / caps should be enforced on-host
- whether the provider offers a panel/API for monthly transfer inspection
