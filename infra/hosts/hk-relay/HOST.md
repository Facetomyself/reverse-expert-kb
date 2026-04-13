# hk-relay

## 1. Identity
- Host label: `hk-relay`
- Static hostname: `019d8575-3c0b-778e-84a1-5a3332db9a56`
- Provider: unknown / user-added Hong Kong VPS
- Primary role: 三网优化流量中转 / relay host with monthly transfer cap
- SSH alias: `hk-relay`
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
Current first-observed runtime on 2026-04-13:
- SSH on TCP `22`
- local systemd-resolved listener on `127.0.0.53:53`
- no additional public TCP/UDP application listeners observed yet

External connectivity smoke check on 2026-04-13:
- `https://www.google.com` -> `HTTP/2 200`
- `https://github.com` -> `HTTP/2 200`

Interpretation:
- baseline outbound foreign access appears healthy without additional proxy bootstrap
- machine is currently clean enough to treat as a fresh relay candidate

## 6. Machine-Level Infrastructure Notes
- cloud-init currently owns `/etc/netplan/50-cloud-init.yaml`
- hostname is still the provider-generated UUID-like name and has not yet been semantically renamed on-host
- this host currently has no swap; if future relay software proves memory-spiky, swap may become the first low-risk stabilization lever
- because the user called out a **bidirectional 800G/month** transfer limit, any future documentation should record whether a service is ingress-heavy, egress-heavy, or symmetric

## 7. Documentation Scope
This host's docs should focus on:
- SSH/bootstrap access
- relay / proxy / transit role design
- transfer-budget-aware operational rules
- any future public listener map and traffic-accounting notes
