# self-server / PROJECTS

Read-only inventory captured on 2026-04-04 to support later cleanup/reorganization.
Do not treat every directory below as an actively important project; this is a triage snapshot for deciding what can be archived or removed.

## `:44001` / hostname `181`
Current shape appears relatively small and panel-centric.

### Live services / runtime hints
- `1panel-core.service`
- `1panel-agent.service`
- `docker.service`
- `firewalld.service`
- `sshd.service`
- running container:
  - `1Panel-frps-aOX6` (`snowdreamtech/frps:0.64.0`)

### Filesystem hints
- `/opt/1panel/*`
- `/root/docker`
- `/root/1panel-v2.0.4-linux-amd64`

### Likely interpretation
- this machine currently looks like a light 1Panel host with FRP-related function and not much additional payload left alive
- likely easier cleanup candidate than `host185`

## `:44005` / hostname `host185`
Current shape is noticeably heavier and contains more development residue / operator tooling.

### Live services / runtime hints
- `1panel-core.service`
- `1panel-agent.service`
- `docker.service`
- `mihomo.service`
- `postfix.service`
- `sshd.service`
- running container:
  - `funny_dewdney` (`local/jshookmcp:node22`)
- exited containers still present:
  - `camoufox-fetch`
  - `relaxed_torvalds`
  - `suspicious_almeida`

### Filesystem hints
- `/opt/1panel/*`
- `/opt/clash/*`
- `/root/mcp-shrimp-task-manager`
- `/root/mcp/jshookmcp-docker`
- `/root/codex-config`
- `/root/.codex/*`
- `/root/.cursor*`
- `/root/.vscode-server/*`
- `/root/miniconda/*`
- `/root/test_skill/reverse_skill`
- `/root/mcp/*`

### Likely interpretation
- this machine had accumulated a mix of panel management, proxy tooling (`mihomo`), MCP/dev tooling, and editor/agent residue
- on 2026-04-04 an aggressive cleanup removed the running `jshookmcp` container, disabled `mihomo` and postfix, removed most MCP/editor/dev-tool directories, later removed the extra SSH listener `5837` plus `rpcbind`, and finally deleted the stale 1Panel-managed MySQL application/data residue under `/opt/1panel/apps/mysql`, leaving the machine much closer to a true 1Panel-only box

## Frozen operating intent after 2026-04-04 cleanup
### `181` / `:44001`
- treat as the retained `1Panel + FRPS` machine
- future additions should be sparse and deliberate
- avoid turning it back into a general experimentation box
- keep the same-day stable outbound helper shape in place:
  - local `dnsmasq` on `127.0.0.1:53`
  - upstream DNS to `106.15.239.221#1053`
  - shell/Docker explicit proxying via `ali-cloud`
- validated after cutover: `docker pull hello-world` and `docker pull coredns/coredns:latest` both succeeded

### `host185` / `:44005`
- current intent after the 2026-04-13 migration is application-focused rather than FRPS-focused
- expected long-lived projects on this VM now are:
  - `1Panel`
  - `AstrBot`
  - `NapCat`
  - `EasyAI`
- `prompt-optimizer-studio` was intentionally retired and its former `30001/tcp` slot was repurposed for `NapCat WebUI`
- the temporary FRPS role that briefly lived on this VM was moved away; do not treat `host185` as the steady FRP relay box anymore
- future workloads should still be introduced intentionally from a low-noise baseline
- if new projects are added later, document them explicitly rather than letting residue accumulate again
- keep the same-day stable outbound helper shape in place:
  - local `dnsmasq` on `127.0.0.1:53`
  - upstream DNS to `106.15.239.221#1053`
  - shell/Docker explicit proxying via `ali-cloud`
- validated after cutover: `docker pull hello-world` and `docker pull coredns/coredns:latest` both succeeded; the discarded transparent `sing-box-global` experiment should not be treated as an active project
- current intended externally published application slots on this VM are primarily:
  - `30001/tcp` for `NapCat WebUI`
  - `30002-30004/tcp` for `EasyAI`
  - `30005-30007/tcp` for `AstrBot`
  - `30008/tcp` for `1Panel`

#### Active project added on 2026-04-06: Prompt Optimizer Studio
- deployment path: `/opt/prompt-optimizer-studio`
- runtime shape: Docker Compose local source build on host `host185`
- public port: `30001 -> container 3000`
- storage path: `/opt/prompt-optimizer-studio/data` mounted to `/app/data`
- service/container name shape: `prompt-optimizer-studio-app-1`
- health check: `GET /api/health`
- update path: refresh source tree on a better-connected host if needed, sync to `host185`, then `docker-compose up -d --build`
- operational note: direct GitHub/GHCR shell access from this host was flaky during bootstrap, but Docker base-image pulls and local source-build deployment succeeded through the established explicit-proxy shape
- detailed runbook: `infra/hosts/self-server/projects/prompt-optimizer-studio.md`

#### Active project confirmed on 2026-04-11: AstrBot
- deployment path: `/opt/1panel/apps/astrbot/astrbot`
- runtime shape: 1Panel-managed Docker app, container name `astrbot`, image `soulter/astrbot:v4.22.3`
- compose path: `/opt/1panel/apps/astrbot/astrbot/docker-compose.yml`
- env path: `/opt/1panel/apps/astrbot/astrbot/.env`
- confirmed host-port mapping from 1Panel app env/compose:
  - `30007 -> container 6185` (`WebUI`)
  - `10000 -> container 6194` (`微信官方`)
  - `10001 -> container 6195` (`企微`)
  - `30006 -> container 6196` (`QQ 官方`)
  - `30005 -> container 6199` (`QQ 个人`)
  - `10002 -> container 11451` (`微信个人`)
- runtime logs on 2026-04-11 confirmed:
  - AstrBot boot completed normally
  - WebUI started on container `0.0.0.0:6185`
  - host-side direct check `curl http://127.0.0.1:30007/` returned `200 OK`
  - host-side direct check `curl http://127.0.0.1:6185/` returned connection refused, because `6185` is container-internal only
- operational implication: any host-level reverse proxy should target `http://127.0.0.1:30007` (or Docker-network target `http://astrbot:6185` if sharing the same network), not host `:6185`; otherwise a `502 Bad Gateway` is expected.
- model/provider follow-up on the same day:
  - AstrBot traffic for `爱丽丝` was not using the healthy default `cmd_config.json`; it was routed by `data/data_v4.db` (`preferences.key = umop_config_routing`) into a per-UMO config named `ForAlice`
  - that routed file `data/config/abconf_dd547db0-c864-43a8-a0a7-46675d251c52.json` initially had empty `provider_sources` and `provider`, which explained the earlier provider-disabled / provider-not-found symptoms
  - host and container both proved they could reach `proxy.zhangxuemin.work` directly, so the immediate issue was config routing rather than missing reachability to `oracle-proxy`
  - minimal repair applied on 2026-04-11: copied `provider_sources` + `provider` from `cmd_config.json` into the routed `ForAlice` abconf and restarted `astrbot`
  - post-restart logs confirmed provider adapters now load successfully for `openai/gpt-5.4`, `openai/gpt-5.4-mini`, and `openai/gpt-5.2`
- detailed runbook: `infra/hosts/self-server/projects/astrbot.md`

#### Active project confirmed on 2026-04-16: EasyAI
- deployment path: `/opt/easyai`
- runtime shape: Docker Compose application on `host185`, started successfully after offline image staging from `ali-cloud`
- main intended published ports:
  - `30002 -> EasyAI WebUI`
  - `30003 -> EasyAI API`
  - `30004 -> EasyAI WS gateway`
- notable host-bound helper/runtime ports currently present from the shipped compose:
  - `8080` (`dozzle`)
  - `8888` (`sandbox`)
  - `8000` (`video-edit`)
  - `5672` / `15672` (`rabbitmq`)
  - `27017` (`mongo`)
- recovery note from the first successful bring-up:
  - compose initially failed because its custom network wanted `172.21.0.0/16`
  - the real overlap was a stale Docker network `one-mcp_default` from an abandoned compose project `one-mcp`
  - verification before cleanup showed `one-mcp_default` had no attached containers and `/opt/1panel/mcp` was empty
  - removing that stale network allowed `docker-compose up -d` to complete successfully
- offline-transfer note:
  - all required images were confirmed present on `host185`
  - temporary `.tar.gz` bundles were cleaned from both `host185:/data` and `ali-cloud:/tmp/easyai-image-cache/http-root` after import
- current runtime verification on 2026-04-16:
  - local probe: `30002` returned `302 -> /home`
  - local probe: `30003` returned `200 OK`
  - external probe from `ali-cloud`: `30002` and `30003` were reachable
  - external probe from `ali-cloud`: `30004` still returned connection refused even though Docker bound the port locally, so verify whether external WS exposure is actually required before depending on it
- detailed runbook: `infra/hosts/self-server/projects/easyai.md`
