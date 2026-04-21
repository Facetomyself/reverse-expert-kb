# home-nas / local Mihomo plan

Updated: 2026-04-13

## Status
- Planning only
- Deferred by user on 2026-04-13
- Do not execute this rollout unless the user explicitly reopens it

## Goal
Install a host-local Mihomo/Clash.Meta core on `home-nas` so the NAS itself has direct outbound proxy capability, while keeping FRP-published DSM/Drive services unchanged.

## Confirmed host baseline
- DSM: `7.2.2-72806 Update 8`
- Architecture: `x86_64`
- Stable remote maintenance path: `ssh -J ali-cloud -p 30018 zhangxuemin@211.144.221.229`
- `zhangxuemin` has passwordless sudo
- Existing persistent launcher pattern already in use: `/usr/local/etc/rc.d/S99frpc-nas.sh`
- No existing `clash` / `mihomo` / `sing-box` runtime or package was present during the 2026-04-13 audit

## Deployment shape
Prefer a host-native single-binary deployment instead of a DSM package first:
- binary: `/usr/local/bin/mihomo`
- config dir: `/usr/local/etc/mihomo/`
- main config: `/usr/local/etc/mihomo/config.yaml`
- startup script: `/usr/local/etc/rc.d/S98mihomo.sh`
- logs: `/var/log/mihomo.log`
- state/downloads helper dir if needed: `/usr/local/etc/mihomo/run/`

Why this shape:
- matches the existing Synology custom-service pattern already used by FRP
- minimizes DSM package coupling
- is easy to roll back by stopping one rc.d script and removing one binary/config tree

## Initial operating mode
Start in explicit-proxy mode only.

### Do first
- bind proxy listeners on loopback only
- do not enable TUN mode initially
- do not replace system DNS globally initially
- do not redirect all host traffic through transparent proxy rules initially

### Recommended first listeners
- mixed-port: `127.0.0.1:7890`
- socks-port: optional, omit if `mixed-port` is enough
- external-controller: `127.0.0.1:9090`

## Upstream policy
Use the same managed subscription family already documented for the fleet:
- primary source: a **private randomized** `clash.hk.zhangxuemin.work/.../clash-meta.yaml` path distributed out-of-band

Recommended first-stage local policy on the NAS:
- treat `Home-Egress` as the preferred path for AI / login-sensitive sites when the managed subscription provides it
- keep ordinary HK / ali / oracle choices available for manual fallback or bulk transfer scenarios
- keep `oracle-gateway` as fallback if retained by the subscription

## Safety constraints
During first deployment, do not disturb these existing listeners/services:
- DSM HTTPS `5001/tcp`
- Synology Drive `6690/tcp`
- SSH `22/tcp`
- FRP client process launched by `/usr/local/etc/rc.d/S99frpc-nas.sh`

## Proposed rollout steps
1. Download or stage the correct `mihomo` Linux `amd64` binary onto the NAS
2. Create `/usr/local/etc/mihomo/`
3. Write first-stage `config.yaml` with loopback-only listeners
4. Install `/usr/local/etc/rc.d/S98mihomo.sh`
5. Start Mihomo manually once and verify listeners on `127.0.0.1:7890` and `127.0.0.1:9090`
6. Verify outbound with explicit env vars or `curl --proxy`
7. Confirm DSM / Drive / FRP are unaffected
8. Only after successful first-stage validation, consider whether NAS-side app downloads or package managers need wrapper env/proxy integration

## Acceptance checks
- `curl --proxy http://127.0.0.1:7890 https://ifconfig.me` returns a non-CN expected exit
- Mihomo stays up across restart via `/usr/local/etc/rc.d/S98mihomo.sh`
- DSM HTTPS and Synology Drive remain reachable through FRP
- FRP client still reconnects normally after reboot/service restart

## Deferred decisions
Do not decide these until after explicit-proxy mode is stable:
- whether to enable TUN mode on DSM
- whether to move DNS resolution through Mihomo fake-ip/redir mode
- whether to make package downloads or Docker-like workloads use the local proxy automatically
- whether to expose controller or dashboard beyond loopback

## Hold note
On 2026-04-13 the user explicitly asked to keep this as a retained option but not proceed because it felt non-essential and potentially risky right now. Treat this document as a parked implementation plan, not an active rollout checklist.
