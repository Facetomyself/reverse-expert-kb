# home-macmini / HOST

## Identity
- Name: `home-macmini`
- Provider: home
- OS: macOS

## Role
- Home workstation / Mac mini
- FRP-published home service source
- Local Clash/Mihomo outbound client target

## Current service direction
- ComfyUI should be published through FRP on `self-server(:44001)`
- This host is also in scope for local Clash/Mihomo outbound capability
- 2026-04-13 policy clarification: even though the domestic Linux servers can currently inherit centralized upstream switching from `ali-cloud`, `home-macmini` should still move toward a real host-local Clash/Mihomo install because the user explicitly wants local Clash on the home endpoints

## Access
- Confirmed working maintenance path on 2026-04-13: Oracle/OpenClaw side should reach this host via `ali-cloud` jump + FRP SSH relay on `self-server(:44001)` rather than any direct legacy path
- Validated chain: `ssh -J ali-cloud -p 30017 mengma@211.144.221.229`
- The FRP SSH relay depends on `home-macmini` `frpc` registering `remotePort = 30017` to `self-server(:44001)` FRPS `30012`

## Notes
- Access path and runtime docs are being refreshed under the new FRP + explicit-proxy-only direction.
- Do not depend on any removed overlay-network path for future operator access.
- 2026-04-13 confirmed that the FRP SSH path is viable.
- Same-day remote verification over `ssh -J ali-cloud -p 30017 mengma@211.144.221.229` still observed root-owned residuals from the removed overlay client (`/Applications/Tailscale.app`, `/Library/Tailscale`, `/usr/local/bin/tailscale`, launchd items).
- `mengma` is in `admin` and can log in over SSH, but does not currently have passwordless `sudo`, so final deletion of those root-owned residual paths still requires host-side root execution or a sudo-capable remote path.
