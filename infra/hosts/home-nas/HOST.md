# home-nas / HOST

## Identity
- Name: `home-nas`
- Provider: home-tailnet
- Tailnet IPv4: `100.73.212.89`
- Current Tailnet hostname: `NAS`
- MagicDNS name: `nas.tail646ee3.ts.net`
- OS: linux (as reported by Tailscale)

## Role
- Home storage node
- NAS
- Tailnet member
- Primary stable home operations entrypoint (current default)

## Access
- Confirmed online from the OpenClaw host on 2026-03-26
- SSH on TCP `22` was later enabled on 2026-03-26 and successfully verified from the OpenClaw host
- Verified login user: `zhangxuemin`
- Passwordless SSH was enabled from the OpenClaw host on 2026-03-26 by installing `/root/.ssh/id_ed25519.pub`, and local alias `home-nas` now works non-interactively
- On 2026-03-27, `zhangxuemin` was granted passwordless sudo via `/etc/sudoers.d/zhangxuemin` with `zhangxuemin ALL=(ALL) NOPASSWD:ALL`; `sudo -n whoami` now returns `root`
- Synology package control for Tailscale is inconsistent: `/usr/syno/bin/synopkg status Tailscale` may report `stop` / status code `263` even while the Tailscale daemon is actually functioning and `tailscale status` / `tailscale netcheck` succeed

## Notes
- Current visible Tailnet hostname is still the generic `NAS`; `home-nas` is the semantic documentation identity.
- MagicDNS name confirmed on 2026-03-27: `nas.tail646ee3.ts.net`.
- The shell PATH does not include the Tailscale package bin directory by default; use `/var/packages/Tailscale/target/bin/tailscale` for direct CLI diagnostics over SSH.
- 2026-03-27 Tailscale diagnostics from the NAS showed `UDP: true`, `PortMapping: UPnP`, `MappingVariesByDestIP: true`, and `Nearest DERP: San Francisco`.
- Current path behavior is peer-specific: from the OpenClaw host, probes to `home-nas` can establish direct connectivity (for example via `180.107.192.11:*`), but from the `company` Windows node the same NAS still consistently falls back to `via DERP(sfo)` around 480-570 ms.
- Current working hypothesis: this is not a simple DSM/Tailscale misconfiguration on the NAS, but a path-quality / NAT-combination issue specific to `company <-> home-nas`, likely amplified by the NAS-side network preferring SFO as nearest DERP.
- Worth standardizing the Tailnet-visible hostname later if this NAS becomes a routine remote administration target.
- A direct probe from the OpenClaw host on 2026-03-26 showed this NAS works well as a stable SSH entrypoint, but its shell environment did not expose `tailscale` or `nc`, so it should not yet be treated as a first-choice diagnostics/jump box for Tailnet reachability testing.
