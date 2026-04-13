# hk-relay

## 1. Identity
- Host label: `hk-relay`
- Static hostname: `019d8575-3c0b-778e-84a1-5a3332db9a56`
- Provider: unknown / user-added Hong Kong VPS
- Primary role: 三网优化流量中转 / relay host with monthly transfer cap
- SSH alias: `hk-relay`
- Canonical domain (from 2026-04-13): `hk.zhangxuemin.work`
- Main purpose: 作为香港中转节点使用，用户明确说明该机是“三网优化流量中转”的机器，但有**双向月流量 800G** 限制，因此后续应把它当作有带宽预算约束的转发/中继资产，而不是随便堆长期大流量任务的通用机器。

## 2. System Baseline
- OS: Ubuntu 20.04 LTS
- Kernel: `5.4.0-26-generic`
- Architecture: `x86_64`
- Virtualization: `kvm`
- CPU: `1 vCPU` (`Intel(R) Xeon(R) CPU E5-2680 v3 @ 2.50GHz` as exposed by the hypervisor)
- Memory: `981 MiB`
- Swap: `0 MiB`
- Root disk: `49G total / 2.2G used / 47G free` (first snapshot on 2026-04-13)

## 3. Usage Pattern
- Host style: lightweight bandwidth-sensitive utility relay
- Change sensitivity: medium; low hardware headroom and explicit monthly transfer budget mean this host should stay simple
- Operational preference:
  - avoid heavy Docker image churn, bulk downloads, or cache-heavy workloads here unless the user explicitly wants that tradeoff
  - treat transfer volume as a first-class operational constraint
  - prefer documenting any future tunnel/proxy role clearly before enabling public listeners

## 4. Access Notes
- Main SSH alias: `hk-relay`
- Expected user: `root`
- Authentication mode as of 2026-04-13:
  - bootstrap used password auth once
  - OpenClaw-side public key `~/.ssh/id_ed25519.pub` was installed into remote `root` `authorized_keys`
  - passwordless login was then validated successfully via `ssh hk-relay`
- Public IP: `154.86.30.10`
- Network baseline:
  - interface: `enp1s0`
  - primary address: `154.86.30.10/24`
  - default gateway: `154.86.30.254`
  - current nameservers from cloud-init netplan: `8.8.8.8`, `1.1.1.1`

## 5. High-Level Service Map
Initial first-observed runtime on 2026-04-13:
- SSH on TCP `22`
- local systemd-resolved listener on `127.0.0.53:53`
- no additional public TCP/UDP application listeners observed yet

After first relay bootstrap on 2026-04-13:
- `sing-box` active as the primary multi-protocol relay service
- public listeners now include:
  - TCP `1080` -> authenticated `mixed` inbound (HTTP + SOCKS compatible client entry)
  - TCP `1081` -> authenticated HTTP proxy inbound
  - TCP `8443` -> VLESS + Reality inbound
  - UDP `8444` -> Hysteria2 inbound
  - TCP `8080` -> authenticated Caddy-based file browse/download surface
  - TCP `8088` -> authenticated `dufs` upload/download surface for large-file transfer relay

External connectivity smoke check on 2026-04-13:
- `https://www.google.com` -> `HTTP/2 200`
- `https://github.com` -> `HTTP/2 200`

Operational interpretation:
- baseline outbound foreign access appears healthy without additional proxy bootstrap
- host is now acting as a first-class Hong Kong relay node rather than a blank candidate
- design intent is explicit-use proxying and transfer relay, not transparent gatewaying

## 6. Machine-Level Infrastructure Notes
- cloud-init currently owns `/etc/netplan/50-cloud-init.yaml`
- hostname is still the provider-generated UUID-like name and has not yet been semantically renamed on-host
- this host currently has no swap; if future relay software proves memory-spiky, swap may become the first low-risk stabilization lever
- because the user called out a **bidirectional 800G/month** transfer limit, any future documentation should record whether a service is ingress-heavy, egress-heavy, or symmetric
- first production relay stack installed on 2026-04-13 is `sing-box 1.11.0`
- first deployed access pattern is intentionally multi-entry:
  - direct server/tool usage via authenticated HTTP/SOCKS-style proxy ports
  - Clash/sing-box client usage via VLESS Reality and Hysteria2
- current firewall baseline uses `ufw` with explicit allows for `22/tcp`, `1080/tcp`, `1081/tcp`, `8080/tcp`, `8088/tcp`, `8443/tcp`, and `8444/udp`
- Hysteria2 currently uses a self-signed certificate generated on-host for initial bootstrap; if long-term client UX matters, replace this with a real certificate/domain later
- canonical public hostname for this relay node is now `hk.zhangxuemin.work` (Cloudflare DNS-only A record -> `154.86.30.10` created on 2026-04-13)

## 7. Documentation Scope
This host's docs should focus on:
- SSH/bootstrap access
- relay / proxy / transit role design
- transfer-budget-aware operational rules
- public listener map and protocol inventory
- any future file-transfer ingress and traffic-accounting notes
