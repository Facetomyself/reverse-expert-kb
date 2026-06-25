# home-nas / Network

## 1. Network Identity
- Tailnet IPv4: `100.73.212.89`
- Current Tailnet hostname: `NAS`
- MagicDNS name: `nas.tail646ee3.ts.net`
- Home LAN snapshot during 2026-03-27 diagnostics:
  - NAS local IPv4: `192.168.8.16`
  - observed gateway / router: `192.168.8.1`

## 2. Documented Access Paths
### Tailscale / Tailnet
- Primary remote administration path: Tailscale
- Confirmed working addresses:
  - `ssh home-nas`
  - `ssh zhangxuemin@100.73.212.89`
  - `ssh zhangxuemin@nas.tail646ee3.ts.net`
- DSM over Tailnet:
  - `https://100.73.212.89:5001/`
  - `https://nas:5001/`
  - `https://nas.tail646ee3.ts.net:5001/`
- Practical caveat: DSM over Tailnet is reachable, but browser TLS is currently not clean because the active DSM certificate does not match the Tailscale hostname / IP; browsers therefore show the usual "not secure" warning unless a matching certificate is installed later.

### SSH
- SSH on TCP `22` is enabled and reachable over Tailnet
- Verified login user: `zhangxuemin`
- Passwordless SSH from the OpenClaw host is enabled via installed public key
- As of 2026-03-27, `zhangxuemin` also has passwordless sudo on the NAS via `/etc/sudoers.d/zhangxuemin`

## 3. Tailscale Runtime Notes
- Synology package path for direct CLI use:
  - `/var/packages/Tailscale/target/bin/tailscale`
- The NAS shell PATH does not include the package bin directory by default, so plain `tailscale` may show `command not found` over SSH unless PATH is adjusted.
- Synology package control is partially misleading here:
  - `/usr/syno/bin/synopkg status Tailscale` may report `stop` with status code `263`
  - while `/var/packages/Tailscale/target/bin/tailscale status` and `tailscale netcheck` still work and the node remains reachable
- Operationally, prefer the direct Tailscale CLI and real connectivity checks over Synology package status alone.

## 4. 2026-03-27 Tailscale Diagnostics Snapshot
Observed from the NAS itself:
- `UDP: true`
- `IPv4: yes`
- `PortMapping: UPnP`
- `MappingVariesByDestIP: true`
- `Nearest DERP: San Francisco`
- Tailscale version: `1.96.2`

## 5. Path-Quality Findings
This NAS is **not** globally stuck behind DERP; path behavior is peer-specific.

Observed on 2026-03-27:
- OpenClaw host -> `home-nas`: direct connectivity succeeded (example observed direct endpoint `180.107.192.11:*`, latency around `180-210 ms`)
- `company` Windows node -> `home-nas`: repeated probes still fell back to `via DERP(sfo)` around `480-570 ms`

Current working interpretation:
- this does **not** look like a simple DSM misconfiguration or a basic "Tailscale is broken on the NAS" situation
- it looks more like a `company <-> home-nas` pair-specific NAT / path-quality problem
- the effect is likely amplified by the NAS-side network currently preferring **SFO** as its nearest DERP region

## 6. Practical Operator Guidance
- If Tailnet access works but DSM feels slow from `company`, check `tailscale ping 100.73.212.89` first.
- If it shows `via DERP(sfo)`, the slowness is expected and is not by itself evidence that DSM or SSH is misconfigured.
- When administering this NAS over SSH, prefer:
  - `/var/packages/Tailscale/target/bin/tailscale status`
  - `/var/packages/Tailscale/target/bin/tailscale netcheck`
- Do not rely solely on `synopkg status Tailscale` for health conclusions on this host.
