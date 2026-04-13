# home-nas / HOST

## Identity
- Name: `home-nas`
- Provider: home
- OS: Synology DSM / Linux-based NAS
- Runtime snapshot revalidated on 2026-04-13:
  - DSM `7.2.2-72806 Update 8`
  - architecture: `x86_64`

## Role
- Home storage node
- NAS
- FRP-published home service source
- Primary stable home operations entrypoint

## Access
- Verified login user: `zhangxuemin`
- Passwordless SSH was enabled from the OpenClaw host by installing `/root/.ssh/id_ed25519.pub`, and local alias `home-nas` now works when the selected access path is available
- `zhangxuemin` has passwordless sudo via `/etc/sudoers.d/zhangxuemin` with `zhangxuemin ALL=(ALL) NOPASSWD:ALL`; `sudo -n whoami` returns `root`

## Current service direction
- DSM should be published through FRP on `self-server(:44001)`
- Synology Drive should be published through FRP on `self-server(:44001)`
- This host is also in scope for local Clash/Mihomo outbound capability
- 2026-04-13 policy clarification: even though the domestic Linux servers can currently inherit centralized upstream switching from `ali-cloud`, `home-nas` should still move toward a real host-local Clash/Mihomo install because the user explicitly wants local Clash on the home endpoints

## Access
- Confirmed working maintenance path on 2026-04-13: Oracle/OpenClaw side should reach this host via `ali-cloud` jump + FRP SSH relay on `self-server(:44001)` rather than any old direct/overlay path
- Validated chain: `ssh -J ali-cloud -p 30018 zhangxuemin@211.144.221.229`
- The FRP SSH relay depends on `home-nas` `frpc` registering `remotePort = 30018` to `self-server(:44001)` FRPS `30012`

## Notes
- Synology package/runtime management is non-standard; prefer real process/listener validation over package UI assumptions
- This NAS remains a key home-side service source and should be documented around FRP publishing + host-native outbound proxy shape, not around any removed overlay network
- 2026-04-13 host-side cleanup confirmed the removed overlay client no longer remained present (`TS_REMOVED`) before the new FRP SSH maintenance path was revalidated.
- 2026-04-13 implementation audit found no pre-existing `clash` / `mihomo` / `sing-box` runtime or package artifacts on the NAS.
- Host-native persistent launch patterns currently available and worth reusing:
  - `/usr/local/etc/rc.d/` custom startup scripts are active in practice
  - existing NAS FRP launcher lives at `/usr/local/etc/rc.d/S99frpc-nas.sh`
  - `zhangxuemin` has passwordless sudo, which makes root-owned deployment and service management practical over SSH
- Planning doc for the first host-local Mihomo rollout now lives at:
  - `infra/hosts/home-nas/projects/local-mihomo-plan.md`
