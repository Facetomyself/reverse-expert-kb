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
- Confirmed working maintenance path on 2026-04-13: Oracle/OpenClaw side should reach this host via `ali-cloud` transit + FRP SSH relay on `self-server(:44001)` rather than any direct legacy path
- Validated chain shape: `ali-cloud -> ssh -p 30017 mengma@211.144.221.229`
- Practical operator note: `ProxyJump ali-cloud` to this FRP-backed macOS SSH target showed intermittent banner-exchange instability from the Oracle/OpenClaw side, while the durable routing rule still remains "via ali-cloud"; if needed, prefer an explicit two-hop model through `ali-cloud` instead of assuming `ProxyJump` itself is always stable for this specific host
- 2026-04-13 access hardening follow-up: agent forwarding from the Oracle/OpenClaw side was unavailable (`SSH_AUTH_SOCK` empty on `ali-cloud`), so a dedicated `ali-cloud`-local ED25519 key was generated and installed onto `home-macmini` root. This successfully established a durable reusable maintenance path of the form `ali-cloud -> ssh -i ~/.ssh/id_ed25519_home_macmini -p 30017 root@211.144.221.229`, avoiding dependence on forwarded agent state or `ProxyJump` stability for this host.
- Same-day operator convenience hardening also added an `ali-cloud` SSH config alias `home-macmini-via-frp`, but when invoking remote commands non-interactively it is safer to prefer explicit `ssh -F /root/.ssh/config home-macmini-via-frp ...` or the fully explicit parameter form instead of assuming the default config lookup path will always be honored in every automation context.
- The FRP SSH relay depends on `home-macmini` `frpc` registering `remotePort = 30017` to `self-server(:44001)` FRPS `30012`

## Notes
- Access path and runtime docs are being refreshed under the new FRP + explicit-proxy-only direction.
- Do not depend on any removed overlay-network path for future operator access.
- 2026-04-13 confirmed that the FRP SSH path is viable.
- Same-day follow-up initially observed root-owned residuals from the removed overlay client (`/Applications/Tailscale.app`, `/Library/Tailscale`, `/usr/local/bin/tailscale`, launchd items).
- Access hardening then established a reusable `ali-cloud`-local root maintenance path over FRP. A later 2026-05-25 read-only check found that the earlier `TS_REMOVED` note was too strong: root-owned filesystem paths such as `/Applications/Tailscale.app`, `/Library/Tailscale`, and `/usr/local/bin/tailscale` were absent, but a Tailscale NetworkExtension launchd entry (`NetworkExtension.io.tailscale.ipn.macsys.network-extension...`) was still loaded and listening on loopback. Treat this as overlay-client residual state, not a preferred access path.
- 2026-05-25 cleanup attempt: terminated the live Tailscale NetworkExtension process and moved package receipts aside into `/var/root/tailscale-systemextension-cleanup-20260525-165013`, but macOS immediately respawned the SystemExtension from `/Library/SystemExtensions/2139BF59-01B2-485A-8A0D-D41180A822F7/...`. `systemextensionsctl uninstall W5364U7YZB io.tailscale.ipn.macsys.network-extension` is blocked while SIP is enabled, and `launchctl bootout/remove` returns permission errors even as root. Full removal therefore requires local GUI/System Settings approval or Recovery/SIP-off maintenance; do not attempt further blind deletion over SSH.
- 2026-05-25 status snapshot: host reachable through `ali-cloud -> self-server(:44001) FRP :30017`; macOS 15.4.1 build 24E263; uptime ~59d19h; disk healthy (`/System/Volumes/Data` 50Gi used / 137Gi available); root `frpc` publishes SSH `remotePort=30017`; user `frpc` publishes ComfyUI `remotePort=30014`; local ComfyUI on `127.0.0.1:8188` responded OK.
- 2026-05-25 ComfyUI cleanup: prior unsuitable model/workflow payloads were first moved out of active ComfyUI paths into reversible quarantine `/Users/mengma/ai/_cleanup_quarantine/comfyui-models-workflows-20260525-165630` (~15G), then permanently deleted after user confirmation. Removed models included ChenkinNoob XL RF, SSD-1B, SD1.5 fp16, AnimateDiff motion, and SD1.5 OpenPose ControlNet. Active `/Users/mengma/ai/ComfyUI/models` now has no large model files, `workflows` is empty, and `user/default/workflows` only has an empty/minimal directory. Disk improved from `/System/Volumes/Data` 50Gi used / 137Gi available to 35Gi used / 152Gi available; ComfyUI HTTP stayed OK after deletion.
- 2026-05-25 Anima bootstrap: created `/Users/mengma/ai/anima-training`, cloned `Moeblack/AnimaLoraToolkit` (`c6bd6b6`) and `Moeblack/ComfyUI-AnimaTool` (`2a9c5fc`), downloaded Anima base resources into ComfyUI (`models/diffusion_models/anima-base-v1.0.safetensors` 3.9G, `models/text_encoders/qwen_3_06b_base.safetensors` 1.1G, `models/vae/qwen_image_vae.safetensors` 242M), downloaded official Turbo LoRA to `models/loras/_Anima/anima-turbo-lora-v0.1.safetensors` (SHA256 `68ed0aec6ff4ebc3add1180e191797adb5aa6b69dd8b0fc8aa9e680145f65aac`), and saved upstream `anima_comparison.json` + `example.png` under `anima-training/workflows/upstream`. Also saved Civitai `Anima LoRA Trainer for ComfyUI` archive at `anima-training/tools/animaLoraTrainerFor_v10.zip`. Local `/Volumes` scan found no NAS mount and no local `lyy` image candidates, but NAS FRP search found canonical candidate set `/volume1/homes/zhangxuemin/lyy/MENGMA/D/python_project/danbooru/output/lyy/_all` with 533 image files (~173M); manifest copied to `anima-training/datasets/lyy_candidates/manifests/lyy-nas-files-20260525.tsv`. Images were not bulk-copied to Mac yet; use the manifest for later curation/copy.
