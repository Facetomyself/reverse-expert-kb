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
- Image: `soulter/astrbot:v4.22.3`
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
