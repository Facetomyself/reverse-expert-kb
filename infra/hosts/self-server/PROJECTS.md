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
  - `ruyipage 151-ruyi`
  - `ChatGpt Image Studio`
  - `proxy_pool`
  - `firefox-fingerprintBrowser 151-3`
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
  - `30002/tcp` for `ruyipage 151-ruyi` static release mirror
  - `30003/tcp` for `proxy_pool` API (`/opt/proxy_pool`, Docker Compose; reassigned from temporary TextDrop on 2026-06-16)
  - `30004/tcp` is now free/unassigned after EasyAI removal
  - `30005-30007/tcp` for `AstrBot`
  - `30008/tcp` for `1Panel`
  - `30009/tcp` for `firefox-fingerprintBrowser 151-3` WebDriver BiDi / Firefox remote-debug service
  - `30010/tcp` for `ChatGpt Image Studio`

#### Active project added on 2026-06-24: firefox-fingerprintBrowser 151-3
- upstream release: `https://github.com/LoseNine/firefox-fingerprintBrowser/releases/tag/151-3`
- deployment path: `/opt/firefox-fingerprintBrowser-151-3`
- runtime shape: Docker Compose on `host185`, container name `firefox-fingerprintbrowser-151-3`, image `firefox-fingerprintbrowser:151-3`
- public port mapping:
  - `30009/tcp -> container 30009/tcp`
- internal runtime shape:
  - Firefox binary from the 151.0a1 Linux x86_64 release runs headless with `--remote-debugging-port 30090`
  - `socat` listens on container `0.0.0.0:30009` and forwards to Firefox's internal `127.0.0.1:30090` WebDriver BiDi/debug listener
- important note:
  - the upstream release includes `fp-default.txt`, but direct Firefox CLI startup rejected `--fpfile`; the deployed service removed that invalid flag and should be treated as verified Firefox/BiDi remote-debug exposure, not as proof that fingerprint-profile injection is active
- validation on 2026-06-24:
  - container `firefox-fingerprintbrowser-151-3` was `Up` with Docker publish `0.0.0.0:30009->30009/tcp`
  - host-local `GET http://127.0.0.1:30009/` returned Firefox `Bad request`
  - ali-cloud transit-side TCP connect to `211.144.221.229:30009` succeeded; `GET /` returned `HTTP/1.1 400 Bad Request` / `Bad request`, expected for plain HTTP against this BiDi/debug service
  - direct OpenClaw-host probe to `211.144.221.229:30009` timed out, consistent with prior Oracle/OpenClaw-side direct reachability caveats for this domestic shared-IP service-port topology
- operational commands:
  - `cd /opt/firefox-fingerprintBrowser-151-3 && /usr/local/bin/docker-compose ps`
  - `cd /opt/firefox-fingerprintBrowser-151-3 && /usr/local/bin/docker-compose logs -f`
  - `curl -i --max-time 5 http://127.0.0.1:30009/`

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

#### Removed project on 2026-06-08: EasyAI
- former deployment path: `/opt/easyai`
- former runtime shape: Docker Compose application on `host185`
- former public ports: `30002` WebUI, `30003` API, `30004` WS gateway, `30009` ASG / governance API
- removal decision: user explicitly requested all EasyAI-related projects on `44005` be cleaned with no archive and ruyipage deployed to `44005` instead
- cleanup performed on 2026-06-08:
  - `docker-compose down --remove-orphans` from `/opt/easyai`
  - removed known EasyAI containers: `easyai-asg`, `easyai-wsgateway`, `agent-memory`, `easyai-web`, `easyai-server`, `video-edit`, `rabbitmq`, `easyai-watchtower-1`, `mongo`, `redis`, `sandbox`, `easyai-pgvector`, `dozzle`
  - removed `/opt/easyai` without archive
  - removed known EasyAI images and EasyAI networks
  - freed listeners on `30002`, `30003`, `30004`, `30009`, and helper ports `8080`, `8888`, `8000`, `5672`, `15672`, `27017`, `3004`
- cleanup follow-up:
  - one cleanup command initially exposed that the broader host also had redis-named volumes `crawl4ai_redis_data`, `linovel_scrapy_redis_data`, and `mailu_api_redis_data`
  - user explicitly confirmed on 2026-06-08 14:41 GMT+8 that these three volumes should also be cleaned, and follow-up `docker volume inspect` confirmed all three are removed
  - future cleanup should still use Compose labels or exact project prefixes by default unless the user explicitly widens the cleanup scope

#### Active project added on 2026-06-08: ruyipage 151-ruyi
- deployment path: `/opt/ruyipage-151`
- runtime shape: systemd-managed Python static HTTP server
- service: `ruyipage-151.service`
- public port mapping: `30002/tcp -> python3 http.server`
- contents:
  - landing page: `/opt/ruyipage-151/index.html`
  - Linux package only: `/opt/ruyipage-151/files/firefox-151.0a1.en-US.linux-x86_64.tar.xz`
  - Windows package intentionally not mirrored because the user said it is not needed
- source release: `https://github.com/LoseNine/ruyipage/releases/tag/151-ruyi`
- validation on 2026-06-08:
  - file size verified: `103125296` bytes
  - host-local `curl -I http://127.0.0.1:30002/` returned `200 OK`
  - host-local package `HEAD` returned `Content-Length: 103125296`
  - transit-side probe from `ali-cloud` to `http://211.144.221.229:30002/` returned `200 OK`
  - transit-side package `HEAD` returned `Content-Length: 103125296`
- update path:
  - replace files under `/opt/ruyipage-151/files`
  - `systemctl restart ruyipage-151.service` if the service definition changes

#### Active project added on 2026-04-24: ChatGpt Image Studio
- deployment path: `/opt/chatgpt-image-studio`
- runtime shape: Docker Compose deployment on `host185`; current live image is the local patched tag `chatgpt-image-studio:patched-20260424-refresh-serial`, derived from upstream `ghcr.io/peiyizhi0724/chatgpt-image-studio:v1.2.6`
- compose file: `/opt/chatgpt-image-studio/docker-compose.yml`
- persistent data/config path: `/opt/chatgpt-image-studio/backend-data`
- container/service name shape: `chatgpt-image-studio`
- public port mapping: `30010 -> container 7000`
- current active runtime decisions after the same-day repair:
  - active image mode is `studio`
  - `sync.enabled = true`, still pointed at the existing oracle-proxy cliproxy/CPA management surface on `http://proxy.zhangxuemin.work:8317`
  - `cpa.base_url` remains configured for future retests, but it is not the active image path in the repaired runtime
  - direct ChatGPT/offline-refresh traffic now uses the ali-cloud authenticated HTTP explicit proxy on `106.15.239.221:2081` instead of the earlier unstable fixed SOCKS path
  - the local patched image serializes account refresh requests (`/backend-api/me` then `/backend-api/conversation/init`) instead of issuing those two calls concurrently
  - `proxy.sync_enabled = false`, so sync / CPA management requests are not redundantly wrapped by that outbound proxy layer
- deployment + repair validation on 2026-04-24:
  - local `curl http://127.0.0.1:30010/health` returned `{"status":"ok"}`
  - transit-side validation from `ali-cloud` confirmed public `211.144.221.229:30010/health` returned `200 OK`
  - additional ali-cloud-side probes confirmed `POST /auth/login` and `GET /v1/models` work with the configured app credentials
  - first deployment completed with `26` synced local accounts visible to the service
  - after the proxy switch + patched image rollout, live quota refresh for a non-disabled `Plus` account succeeded with empty `refresh_error` and a populated `image_gen` quota window
- operational note:
  - secrets for app login/API and upstream CPA/proxy access live only in the on-host `backend-data/config.toml`; do not copy them into `infra/`
- update path:
  - `cd /opt/chatgpt-image-studio`
  - `/usr/local/bin/docker-compose up -d`
  - if upstream image refresh is desired later, re-evaluate whether the local patched image must be rebuilt before switching away from the local tag
- logs:
  - `docker logs -f chatgpt-image-studio`
- detailed runbook: `infra/hosts/self-server/projects/chatgpt-image-studio.md`

#### Disabled temporary project added on 2026-06-10: TextDrop
- deployment path: `/opt/textdrop`
- runtime shape: systemd-managed Python 3 HTTP service
- service: `textdrop.service`
- former public port mapping: `30003/tcp -> python3 /opt/textdrop/app.py`
- purpose: short-term browser-based transfer of long text/scripts from chat-constrained devices to another computer
- access control: random token stored on-host at `/opt/textdrop/token.txt`; do not commit the token into `infra/`
- storage path: `/opt/textdrop/files`
- validation on 2026-06-10:
  - host-local `curl http://127.0.0.1:30003/health` returned `ok`
  - transit-side probe from `ali-cloud` to `http://211.144.221.229:30003/?t=<token>` returned `200 OK`
- 2026-06-16 status:
  - `textdrop.service` was disabled/stopped so `30003/tcp` could be reassigned to `proxy_pool`
  - `/opt/textdrop` was not recorded as deleted
  - do not re-enable TextDrop on `30003` unless `proxy_pool` is moved or removed first

#### Active project added on 2026-06-16: proxy_pool
- upstream: `https://github.com/jhao104/proxy_pool`
- deployment path: `/opt/proxy_pool`
- runtime shape: Docker Compose on `host185`
- compose file: `/opt/proxy_pool/docker-compose.yml`
- containers:
  - `proxy_pool_server` (`jhao104/proxy_pool:latest`, entrypoint `python proxyPool.py server`)
  - `proxy_pool_scheduler` (`jhao104/proxy_pool:latest`, entrypoint `python proxyPool.py schedule`)
  - `proxy_pool_redis` (`redis:7-alpine`, internal-only, AOF enabled)
- persistent storage:
  - Compose volume `proxy_pool_redis_data` mounted to Redis `/data`
- public port mapping:
  - `30003/tcp -> proxy_pool_server:5010`
- key deployment note:
  - the upstream `jhao104/proxy_pool:latest` image entrypoint uses `bash proxy_pool.sh start --fg`, but the image did not contain `bash`; the stock single-container entrypoint restarted with exit `127`
  - deployed stable shape avoids that broken entrypoint by splitting API and scheduler into two Compose services with explicit Python entrypoints
- validation on 2026-06-16:
  - host-local `GET http://127.0.0.1:30003/` returned the API index
  - host-local `GET http://127.0.0.1:30003/count/` returned JSON
  - ali-cloud transit-side `GET http://211.144.221.229:30003/count/` returned JSON and `HEAD /` returned `HTTP/1.1 200 OK` from gunicorn
  - scheduler logs showed active fetch attempts from enabled proxy sources
  - initial pool count was `0`, expected shortly after startup before validation admits proxies
- operational commands:
  - `cd /opt/proxy_pool && /usr/local/bin/docker-compose ps`
  - `cd /opt/proxy_pool && /usr/local/bin/docker-compose logs -f proxy_pool_server proxy_pool_scheduler`
  - `cd /opt/proxy_pool && /usr/local/bin/docker-compose up -d`
- caution:
  - avoid reverting to the upstream stock entrypoint unless the image is fixed to include `bash` or the entrypoint is changed upstream
