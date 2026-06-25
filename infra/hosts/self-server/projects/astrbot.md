# AstrBot on `self-server-44005`

## Purpose
Domestic self-hosted AstrBot deployment on `host185` for WebUI access plus QQ/WeChat-side bot connectivity within the constrained `30001-30010` public TCP budget of the `:44005` VM.

## Placement
- Host: `self-server-44005` / hostname `host185`
- Public IP: `211.144.221.229`
- Main public WebUI entrypoint: `http://211.144.221.229:30007`
- Reason for placement:
  - fits the `:44005` application-port budget
  - colocated with the cleaner 1Panel-managed application stack
  - keeps `:44001` focused on `1Panel + FRPS`

## Runtime shape
- Deployment root: `/opt/1panel/apps/astrbot/astrbot`
- Runtime manager: 1Panel-managed Docker app
- Main container: `astrbot`
- Image: `soulter/astrbot:v4.26.0-beta.4`
- Compose file: `/opt/1panel/apps/astrbot/astrbot/docker-compose.yml`
- Env file: `/opt/1panel/apps/astrbot/astrbot/.env`
- Main data directory: `/opt/1panel/apps/astrbot/astrbot/data`
- Main config file: `/opt/1panel/apps/astrbot/astrbot/data/cmd_config.json`
- Additional per-UMO config directory: `/opt/1panel/apps/astrbot/astrbot/data/config/`
- Shared state DB: `/opt/1panel/apps/astrbot/astrbot/data/data_v4.db`

## Port mapping
Confirmed from `.env` + `docker-compose.yml` on 2026-04-11:
- `30007 -> 6185/tcp` (`WebUI`)
- `10000 -> 6194/tcp` (`微信官方`)
- `10001 -> 6195/tcp` (`企微`)
- `30006 -> 6196/tcp` (`QQ 官方`)
- `30005 -> 6199/tcp` (`QQ 个人`)
- `10002 -> 11451/tcp` (`微信个人`)

## Reverse proxy / 502 rule
The AstrBot WebUI listens on container-internal `6185`, but the host publishes it on `30007`.

That means:
- host-local success path: `http://127.0.0.1:30007`
- Docker-network success path: `http://astrbot:6185`
- host-local failure path: `http://127.0.0.1:6185`

If a 1Panel website / Nginx / OpenResty / other host-level reverse proxy points at host `:6185`, expect `502 Bad Gateway`.

## Provider/model configuration notes
### Default/system config
`data/cmd_config.json` is the default AstrBot config and currently contains the OpenAI-compatible provider source pointing at the cliproxy endpoint:
- `api_base = http://proxy.zhangxuemin.work:8317/v1`

### Per-UMO config routing
AstrBot uses per-UMO config routing stored in `data/data_v4.db` (`preferences` table, key `umop_config_routing`).

Confirmed on 2026-04-11:
- `爱丽丝:*:* -> dd547db0-c864-43a8-a0a7-46675d251c52`
- specific webchat route also pointed to the same config id
- that config is mapped in `abconf_mapping` as:
  - `dd547db0-c864-43a8-a0a7-46675d251c52 -> abconf_dd547db0-c864-43a8-a0a7-46675d251c52.json`
  - friendly name: `ForAlice`

### Root cause of the initial model-usage failure
The `ForAlice` abconf initially had:
- `provider_sources = []`
- `provider = []`

but still referenced provider IDs like:
- `openai/gpt-5.4`
- `openai/gpt-5.4-mini`
- `openai/gpt-5.2`

As a result, `爱丽丝` traffic was routed away from the healthy default `cmd_config.json` into a per-UMO config with no actual provider definitions, leading to the earlier “provider disabled / not found” behavior.

### Fix applied on 2026-04-11
A minimal repair was applied:
- backed up the old file as
  - `data/config/abconf_dd547db0-c864-43a8-a0a7-46675d251c52.json.bak-20260411-161133`
- copied only these sections from `cmd_config.json` into `ForAlice`:
  - `provider_sources`
  - `provider`
- restarted container `astrbot`

Post-restart logs confirmed AstrBot now loads:
- `openai_chat_completion(openai/gpt-5.4)`
- `openai_chat_completion(openai/gpt-5.4-mini)`
- `openai_chat_completion(openai/gpt-5.2)`

## Connectivity note: proxy vs direct
On 2026-04-11 both the host and the AstrBot container could reach `proxy.zhangxuemin.work` directly and receive HTTP auth errors (`401/403` without valid auth), which is enough to prove routing/connectivity is present.

Operational conclusion:
- the immediate model failure was **not** caused by lack of network reachability to `oracle-proxy`
- adding a container-wide HTTP proxy was **not required** to fix the issue

If a future network regression appears, the least-invasive fallback is:
- prefer setting the per-provider `proxy` field inside AstrBot provider config
- only use container-wide `HTTP_PROXY` / `HTTPS_PROXY` envs if broad egress control is intentionally desired

## Update / repair workflow
1. Back up the targeted config file first.
2. Check whether the traffic is using default `cmd_config.json` or a per-UMO `abconf`.
3. If provider issues appear only on one bot/session, inspect:
   - `data/data_v4.db` -> `preferences.key = umop_config_routing`
   - `data/data_v4.db` -> `preferences.key = abconf_mapping`
4. If a routed `abconf` has empty provider definitions, sync the needed provider sections from `cmd_config.json` instead of blindly deleting the routing.
5. Restart the container:
   - `docker restart astrbot`
6. Verify startup logs show provider adapters loading successfully.

## Upgrade note (2026-06-17)
- User requested upgrading the self-hosted AstrBot at `http://211.144.221.229:30007` to the latest available version.
- Latest GitHub/Docker Hub release observed at upgrade time: `v4.26.0-beta.4`; live container image updated from `soulter/astrbot:v4.22.3` to `soulter/astrbot:v4.26.0-beta.4`.
- Pre-upgrade backup on host185: `/opt/backups/astrbot/astrbot-pre-upgrade-20260617-150324.tgz` containing `docker-compose.yml`, `.env`, and `data/`.
- Direct Docker Hub pull from `host185` stalled / timed out on final layers despite Docker daemon proxy config. Stable transfer path used instead:
  1. Pull `soulter/astrbot:v4.26.0-beta.4` on the OpenClaw/Oracle side.
  2. `docker save | gzip` to a temporary image tarball.
  3. Copy tarball to `oracle-proxy` and serve it temporarily via Python HTTP server.
  4. Pull from `host185` with proxy variables unset, verify SHA256, then `docker load`.
- Temporary image tarballs and HTTP servers were removed after deployment.
- Validation after upgrade:
  - `docker inspect astrbot` showed `soulter/astrbot:v4.26.0-beta.4`, state `running`, restart count `0`.
  - host-local WebUI `GET http://127.0.0.1:30007/` returned `200`; note `HEAD /` returned `405` on this version, so use GET for health checks.
  - ali-cloud transit-side public WebUI `GET http://211.144.221.229:30007/` returned `200`.
  - startup logs showed `AstrBot v4.26.0-beta.4 WebUI is ready`, providers loaded, and OneBot reverse listener running on `0.0.0.0:6199`.
  - startup logs included many Python `DEPRECATION: Unexpected import ... after pip install started` warnings from package imports; no `Traceback` / fatal `ERROR` was observed in the verification window.

## Novel rank plugin note (2026-04-19)
Confirmed on `self-server-44005` / container `astrbot`:
- plugin path: `/opt/1panel/apps/astrbot/astrbot/data/plugins/astrbot_plugin_novel_rank`
- plugin config path: `/opt/1panel/apps/astrbot/astrbot/data/config/astrbot_plugin_novel_rank_config.json`
- plugin data path: `/opt/1panel/apps/astrbot/astrbot/data/plugin_data/astrbot_plugin_novel_rank/`

Runtime verification on 2026-04-19 showed:
- plugin loads successfully during AstrBot startup
- real smoke runs for `小说榜单` (`qidian 月票榜`) and `跨站榜单对比 hot` both returned valid text results
- current Qidian desktop rank route can still return a challenge-style `202 Accepted` response, but the plugin's mobile fallback path succeeded and returned real榜单数据

Current operational issue was **not** plugin import or crawler failure. The failing component was AstrBot's HTML-to-image render path:
- live warning observed in `astrbot` logs: `HTML 渲染图片失败，已降级为文本输出: All endpoints failed: HTTP 502`
- the failing upstream shown by the host logs was `https://t2i.soulter.top/text2img`

Stability fix sequence on 2026-04-19:
- first confirmed the immediate failure mode by live smoke and host logs:
  - AstrBot `html_render()` for this plugin depended on the remote endpoint behind `https://t2i.soulter.top/text2img`
  - that upstream was returning Cloudflare-side `HTTP 502`
- temporary stop-loss:
  - backed up `astrbot_plugin_novel_rank_config.json`
  - changed `basic.output_format` from `image` to `text`
  - restarted container `astrbot`
  - this restored stable plugin output immediately while the render chain was still broken
- final same-session repair, phase 1:
  - patched plugin `main.py` so custom HTML image rendering failure no longer falls straight back to plain text
  - new fallback chain is:
    - try plugin HTML card via `html_render()`
    - if that remote-only path fails, fall back to AstrBot `text_to_image()`
    - if AstrBot remote T2I also fails, let AstrBot's own built-in local renderer generate a local image
  - after deploying that patch to the live plugin directory and restarting `astrbot`, the config was switched back to `basic.output_format = image`
  - live smoke then returned a real `image_result` again, with logs confirming this path:
    - plugin HTML render failed on `HTTP 502`
    - AstrBot remote T2I also failed on `HTTP 502`
    - AstrBot renderer then fell back to local rendering successfully and produced a local temp image path
- final same-session repair, phase 2 on 2026-04-19 first restored the rich HTML-card path through an OpenClaw-hosted replacement endpoint, but that was later superseded on 2026-04-20 by a **host185-local renderer deployment** to remove the OpenClaw-host tunnel hop and fix Chinese font rendering more cleanly.
- current renderer shape as of 2026-04-20:
  - deployment root: `/opt/astrbot-t2i-renderer`
  - compose file: `/opt/astrbot-t2i-renderer/docker-compose.host185.yml`
  - container name: `astrbot-t2i-renderer`
  - image base: `soulter/astrbot:v4.22.3` with Playwright + Chromium added during local build
  - host bind: `0.0.0.0:18783 -> 18781/tcp`
  - renderer API shape remains:
    - `POST /text2img/generate`
    - `GET /text2img/<id>`
    - `GET /text2img/health`
- AstrBot-side `t2i_endpoint` remained unchanged and still points at the local host185 address in both:
  - `data/cmd_config.json`
  - `data/config/abconf_dd547db0-c864-43a8-a0a7-46675d251c52.json`
  - current value: `http://10.10.21.185:18783/text2img`
- migration/behavior notes from 2026-04-20:
  - old OpenClaw-host services `astrbot-t2i-renderer.service` and `astrbot-t2i-host185-tunnel.service` were stopped and disabled after host185-local cutover
  - old host185 relay service `astrbot-t2i-host185-relay.service` was stopped and disabled
  - standalone local smoke against `http://127.0.0.1:18783/text2img/health` returned `{"ok": true, "service": "astrbot-t2i-renderer"}`
  - a direct Chinese HTML render smoke on host185 succeeded and returned a real PNG id
- template-side hardening also landed on 2026-04-20:
  - plugin template font stacks were expanded beyond `"Microsoft YaHei", "PingFang SC", sans-serif`
  - current live templates now include Linux-side CJK fallbacks such as:
    - `Noto Sans CJK SC`
    - `Noto Sans SC`
    - `WenQuanYi Micro Hei`
    - `AR PL UKai CN`
    - `AR PL UMing CN`

Operational implication:
- image mode is now backed by a renderer that actually runs on the AstrBot machine itself (`host185`), not a remote tunnel chain through the current OpenClaw host
- richer HTML card output remains available through the custom renderer endpoint
- the plugin-local fallback patch still provides a second safety net if the custom renderer breaks later

## NapCat / OneBot v11 sidecar bootstrap (2026-04-13)
Confirmed on `self-server-44005`:
- deployment root: `/opt/napcat-astrbot`
- compose file: `/opt/napcat-astrbot/docker-compose.yml`
- image: `mlikiowa/napcat-docker:latest`
- container name: `napcat`
- WebUI bind: `127.0.0.1:6099 -> 6099/tcp` (loopback-only, no public exposure)
- network attachment: `1panel-network`
- live container IP: `172.22.0.3`
- AstrBot container IP on same network: `172.22.0.2`
- container-side DNS resolution of `astrbot` from `napcat` succeeded
- host-local WebUI probe: `http://127.0.0.1:6099/` returned `200 OK`

Current runtime state after container bootstrap:
- NapCat starts successfully and exposes WebUI locally
- NapCat generated a WebUI token and waited for QQ login via QR code
- observed WebUI token at bootstrap time: `7bccbc3738e8`
- observed local user panel URL at bootstrap time: `http://127.0.0.1:6099/webui?token=7bccbc3738e8`
- NapCat log also saved the QR image path inside the container: `/app/napcat/cache/qrcode.png`

Final activation state after 2026-04-13 follow-up:
- QQ login was completed successfully in NapCat
- `prompt-optimizer-studio` on public `30001` was intentionally retired; `30001/tcp` is now permanently repurposed for NapCat WebUI
- NapCat runtime now publishes both:
  - `127.0.0.1:6099 -> 6099/tcp`
  - `0.0.0.0:30001 -> 6099/tcp`
- public WebUI entrypoint is now:
  - `http://211.144.221.229:30001/webui/`
- NapCat OneBot v11 client config was confirmed present in:
  - `/app/napcat/config/onebot11.json`
  - `/app/napcat/config/onebot11_3366925614.json`
- confirmed reverse WebSocket target from NapCat to AstrBot:
  - `ws://astrbot:6199/ws`
- AstrBot-side OneBot activation required editing **both** config layers, not just the routed per-UMO abconf:
  - `/opt/1panel/apps/astrbot/astrbot/data/cmd_config.json`
  - `/opt/1panel/apps/astrbot/astrbot/data/config/abconf_dd547db0-c864-43a8-a0a7-46675d251c52.json`
- required AstrBot platform item shape that actually brought up the reverse-WS listener:
  - `type = aiocqhttp`
  - `id = napcat-onebot`
  - `enable = true`
  - `ws_reverse_host = 0.0.0.0`
  - `ws_reverse_port = 6199`
  - `ws_reverse_token = ""`
- post-restart AstrBot logs confirmed full OneBot bring-up:
  - `载入 aiocqhttp(napcat-onebot) 平台适配器 ...`
  - `Running on http://0.0.0.0:6199`
  - `aiocqhttp(OneBot v11) 适配器已连接。`

Operational implication:
- the original deployment goal of colocating NapCat with AstrBot on `1panel-network` and avoiding public exposure for the original loopback-only NapCat WebUI was achieved first, then intentionally relaxed by user request so `30001` became the permanent public NapCat WebUI entrypoint
- full OneBot v11 activation is now complete: QQ login done, AstrBot reverse WebSocket listener up, and NapCat ↔ AstrBot connection established

## Read-only maintenance checklist
Useful recurring checks:
- `docker ps` shows `astrbot` running
- `curl http://127.0.0.1:30007/` returns `200`
- no host-level reverse proxy is targeting `127.0.0.1:6185`
- `data/data_v4.db` routing entries still point where expected
- routed `abconf` files still contain non-empty `provider_sources` / `provider`
- startup logs still show the expected OpenAI-compatible providers loading
- `docker ps` shows `napcat` running
- `curl http://127.0.0.1:6099/` returns `200`
- both `astrbot` and `napcat` remain attached to `1panel-network`
