# hk-relay line optimization notes

Updated: 2026-05-25

## Current read-only baseline

- Host: `hk-relay` / `154.86.30.10`
- Kernel: Ubuntu 20.04 `5.4.0-26-generic`
- Previous TCP congestion control before 2026-05-25 tuning: `cubic`
- Previous qdisc before 2026-05-25 tuning: `fq_codel`
- Current persisted TCP congestion control: `bbr`
- Current persisted qdisc: `fq`
- Available runtime congestion controls before loading modules: `reno cubic`
- Kernel config has BBR available as a module:
  - `CONFIG_TCP_CONG_BBR=m`
  - `CONFIG_NET_SCH_FQ=m`
  - `CONFIG_NET_SCH_FQ_CODEL=m`
- sing-box: `1.11.0`
- sing-box Hysteria2 inbound exists on UDP `8444`; current config does not set `up_mbps` / `down_mbps`.
- Traffic accounting on 2026-05-25: about `55.50 GiB` for current month, against the user-declared 800G bidirectional cap.

## Optimization levers

### 1. Kernel TCP BBR + fq

Potential value: medium.

This host currently uses CUBIC + fq_codel. Since BBR and fq are built as modules, the likely low-risk TCP optimization is:

- load `tcp_bbr`
- load/use `sch_fq`
- set:
  - `net.core.default_qdisc=fq`
  - `net.ipv4.tcp_congestion_control=bbr`

Expected effect:
- helps TCP-based proxy surfaces: SOCKS/HTTP on `1080/1081`, VLESS Reality on `8443`, Caddy front doors on `443`
- does not directly optimize Hysteria2's QUIC congestion behavior in the same way
- may improve long-distance / lossy throughput, but should be measured before/after from representative domestic clients

Caveat:
- BBR is not magic if bottleneck is provider peering/congestion outside the VPS.
- On this old Ubuntu 20.04 kernel, BBR is classic BBR, not newer BBRv2/v3.

### 2. Upgrade sing-box for Hysteria2 BBR profile controls

Potential value: low to medium, with compatibility risk.

External docs show sing-box Hysteria2 `bbr_profile` support from sing-box `1.14.0`; this host currently runs `1.11.0`.

Potential value:
- newer Hysteria2 controls such as `bbr_profile` may allow conservative/standard/aggressive tuning.

Caveat:
- upgrading the relay core is higher risk than kernel BBR because all current inbounds depend on sing-box.
- should be staged with config validation and rollback binary first.

### 3. Hysteria2 bandwidth shaping

Potential value: workload-dependent.

Current Hysteria2 inbound does not set `up_mbps` / `down_mbps`. According to sing-box docs, those fields cap advertised max bandwidth; unset means not limited and interacts with BBR/Hysteria client congestion behavior.

Potential directions:
- leave unlimited for simplicity if clients are few and cap is managed by usage discipline
- set conservative `up_mbps` / `down_mbps` only if one client can monopolize the line or blow through the 800G monthly cap

### 4. Cloudflare preferred IP / CF 优选

Potential value: narrow.

CF preferred IP is not a general speed knob for this HK proxy machine because the main proxy nodes publish the bare server IP `154.86.30.10`, and earlier runtime reliability depended on IP literals instead of domain-form HK node entries.

Where CF 优选 can help:
- accessing Cloudflare-hosted websites from clients
- client -> Cloudflare edge -> Worker/Pages/Tunnel style designs
- selected web front doors if the service is actually proxied through Cloudflare

Where it probably will not help:
- direct Hysteria2 / VLESS Reality / SOCKS / HTTP proxy connections to `154.86.30.10`
- provider peering from mainland networks to this HK VPS
- generic outbound from HK to foreign sites

Recommendation:
- do not put CF preferred IP on the critical direct proxy node path unless a separate Cloudflare-based proxy architecture is intentionally built and tested.
- keep current direct IP nodes as primary.

## Recommended next experiment order

1. Measure baseline from representative client networks: TCP HTTP/SOCKS, VLESS Reality, Hysteria2, large download, latency/jitter/loss.
2. Enable kernel BBR + fq on `hk-relay` and re-measure.
3. If improvement is real and no regressions, persist sysctl config.
4. Only then consider a sing-box upgrade path for Hysteria2-specific tuning.
5. Treat CF preferred IP as a separate architecture experiment, not as a default optimization for current direct-IP nodes.


## 2026-05-25 BBR + fq change

Action taken:

- loaded `tcp_bbr`
- loaded `sch_fq`
- set live sysctl:
  - `net.core.default_qdisc=fq`
  - `net.ipv4.tcp_congestion_control=bbr`
- persisted module loading in `/etc/modules-load.d/99-bbr.conf`
- persisted sysctl in `/etc/sysctl.d/99-bbr-fq.conf`

Validation after persistence:

```text
net.ipv4.tcp_congestion_control = bbr
net.core.default_qdisc = fq
available=reno cubic bbr
```

Proxy smoke check after persistence from the OpenClaw host:

- `hk-socks` -> ok, ~763 ms, egress `154.86.30.10`
- `hk-http` -> ok, ~657 ms, egress `154.86.30.10`
- `home-http-via-hk` -> ok, ~1158 ms, egress `204.237.153.49`
- `home-http-direct` -> ok, ~1123 ms, egress `204.237.153.49`
- `ali-http-oracle-egress` -> ok, ~2498 ms, egress `129.150.61.78`
- `ali-socks-oracle-egress` -> ok, ~1721 ms, egress `129.150.61.78`

Interpretation:

- HK direct HTTP/SOCKS paths stayed healthy and were slightly better than the baseline smoke check.
- Ali/oracle paths still show wider latency variation; do not interpret that as HK BBR regression.
- Keep watching real client throughput before making additional Hysteria2/sing-box changes.


## 2026-05-25 14:15 GMT+8 post-BBR Mihomo test

A real local Mihomo v1.19.25 core was used to test `hk-hy2`, `hk-reality`, `hk-socks`, and `hk-http` through a temporary local mixed proxy.

Summary:

- all four HK node types worked through Mihomo
- `hk-http` and `hk-reality` looked best overall from the OpenClaw test origin
- `hk-hy2` was healthy but not clearly faster from this path
- non-Cloudflare OVH 10MB object was slower than Cloudflare speed object across all node types, indicating content/CDN path dominates part of the result

Detailed report: `test-report-2026-05-25-1415.md`.


## 2026-05-25 14:35 GMT+8 sing-box / Hysteria2 upgrade decision

Decision: do **not** upgrade sing-box or tune Hysteria2 `bbr_profile` yet.

Reasons:

- Current `hk-hy2` is healthy, but post-BBR Mihomo testing did not show it outperforming `hk-reality`, `hk-socks`, or `hk-http` from the OpenClaw test origin.
- sing-box is currently `1.11.0`; `bbr_profile` exists only since sing-box `1.14.0`.
- The current service emits a migration warning: legacy special outbounds are deprecated in 1.11.0 and removed in 1.13.0. A direct upgrade to a version new enough for `bbr_profile` therefore has config migration risk, not just a binary swap risk.
- The biggest unknown for the original goal remains mainland-client path quality. Upgrading the relay core before mainland measurements risks spending effort on a path that may not be the bottleneck.

Recommended gate before upgrade:

1. Collect mainland-client measurements for `hk-hy2`, `hk-reality`, `hk-socks`, and `hk-http` after BBR+fq.
2. Upgrade only if HY2 is the preferred path but shows instability/underperformance that a newer sing-box Hysteria2 profile could plausibly fix.
3. If upgrading, stage it as a rollbackable maintenance change:
   - backup `/usr/bin/sing-box`, `/etc/sing-box/`, and relevant systemd units
   - run new binary config check against copied config
   - fix legacy special outbound migrations first
   - test restart window with rollback command ready
   - compare `bbr_profile=conservative|standard|aggressive` from a representative mainland client, not only from the OpenClaw host

Current recommendation:

- Keep BBR+fq.
- Keep HY2 in the subscription as an option for lossy/mobile networks.
- Prefer `hk-reality` / `hk-http` for default testing until mainland data says otherwise.
