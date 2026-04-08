# oracle-proxy / Change Log

## 2026-04-08
- Per user instruction, removed Tavily registration from active infra and ops tracking. The standalone registration stack (`tavily-scheduler`, `tavily-camoufox`, `tavily-camoufox-adapter`) is no longer treated as a documented project or maintenance target; only the active Tavily proxy surface remains in current docs.

## 2026-04-06
- Recurring read-only fleet check reconfirmed `oracle-proxy` remained reachable and generally healthy. Snapshot at `2026-04-05 19:55 UTC`: uptime ~37.7 days, load low (`0.07 0.08 0.09`), root disk `45G total / 23G used / 23G free` (`51%` used), memory comfortable (`11Gi` total, `8.0Gi` available), no swap configured, and the expected active containers remained up: `cliproxy`, `grok2api`, `exafree`, `proxy-tavily-proxy-1`, `grok-register-camoufox`, and `grok-register-camoufox-adapter`.

## 2026-03-21
- Checked `oracle-proxy:/root/grok2api` against upstream `https://github.com/TQZHR/grok2api.git` while explicitly avoiding changes to the separate Grok registration stack.
- Verified deployed `grok2api` repo was already up to date with upstream: local `HEAD` and `origin/main` both at `d6a945c` (`feat: sync model catalog and update admin/chat flows`), so no upstream pull/update was performed.
- Found that the deployed repo had substantial local uncommitted customizations focused on deployment/runtime adaptation rather than random drift: Camoufox override mounting, pre-fetched Camoufox runtime, register proxy support, private email-site password support, and Cloudflare-oriented register/account-settings refresh tolerance.
- Confirmed live `grok2api` service configuration is primarily loaded from `/root/grok2api/data/config.toml`; `config.defaults.toml` is only a baseline and should not be treated as the live secret source.
- On-host preservation step: created local branch `oracle-proxy/local-custom-20260321` in `/root/grok2api` and committed the local customization set as `2413e6c` with sanitized safe defaults (`app_key="admin"`, `api_key=""`) in `config.defaults.toml` while leaving live `data/config.toml` untouched.
- Verified `http://127.0.0.1:8000/health` remained healthy after the preservation commit.

## 2026-03-20
- Recurring read-only fleet check: `oracle-proxy` remained reachable and healthy.
- Snapshot at `2026-03-19 19:25 UTC`: uptime ~20 days, load essentially idle (`0.01 0.02 0.00`), root disk `45G total / 24G used / 22G free` (`52%` used), memory comfortable (`11Gi` total, `9.4Gi` available), no swap configured.
- Expected active containers during this pass: `cliproxy`, `exafree`, `proxy-tavily-proxy-1`, `grok-register-camoufox`, `grok-register-camoufox-adapter`, `grok2api`.
- Expected paused Tavily registration components (`tavily-scheduler`, `tavily-camoufox`, `tavily-camoufox-adapter`) remained absent from `docker ps`, which matches the intentional 2026-03-19 pause rather than fresh runtime drift.
- Public/listening surface remained broadly consistent with docs: `80`, `7860`, `8000`, `8317`, `9874`, `15072`, plus the previously documented sing-box / xray related ports (`30001`, `30004-30011`, `14391`) and localhost listeners (`20241`, `40449`, `45987`).

## 2026-03-19
- Tavily registration automation was intentionally paused to avoid repeated upstream risk-control hits and to prevent future maintenance sweeps from treating the stopped registration containers as accidental drift.
- On `oracle-proxy`, explicitly stopped and disabled restart for:
  - `tavily-scheduler`
  - `tavily-camoufox`
  - `tavily-camoufox-adapter`
- Left `proxy-tavily-proxy-1` running; the Tavily proxy service remains the active production component.
- Investigation result documented: the Auth0/Tavily signup path itself was substantially repaired (`/u/login/identifier` → `/u/signup/identifier` → `/u/signup/password`), but upstream Tavily risk control now blocks progress after password submission with `Suspicious activity detected. For any help, Please contact support@tavily.com`.
- Infra docs were updated so future host checks understand that Tavily registration is paused by design, not incidentally broken runtime drift.
- Performed a read-mostly Codex / cliproxy performance investigation for slow CLI proxy calls.
- Confirmed `cliproxy` host config currently includes a global socks5 outbound proxy and measured that it materially increases baseline upstream latency, but does not explain the full severity of observed slow requests by itself.
- Ran a short controlled no-proxy experiment on `cliproxy`: backed up config, temporarily removed `proxy-url`, restarted the container, observed live traffic, then restored the original config.
- Key result of the no-proxy experiment: real `POST /v1/chat/completions` traffic still commonly remained around low-20-second latency even without the configured proxy, so the dominant bottleneck is likely upstream/provider/account-pool behavior rather than proxy alone.
- Additional operational finding: `POST /v1/responses` appears less stable than `POST /v1/chat/completions`, and management-side `wham/usage` fetches were repeatedly producing `EOF` / `context canceled` noise during the same period.

## 2026-03-18
- Performed another read-only SSH health check. Current snapshot: uptime ~18 days, load low (`0.06 0.15 0.11`), root disk 53% used, memory comfortable (~9.2 GiB available), and the expected long-lived containers (`tavily-scheduler`, `proxy-tavily-proxy-1`, `exafree`, `grok2api`, `cliproxy`, Tavily/Grok solver support containers) all remained up.
- Recorded an important machine-level doc drift fix: current `:80` ownership is `1panel` according to live `ss -ltnp`, so older notes that treated system `nginx` as the active port-80 front door are now stale and were updated.

## 2026-03-17
- User clarified that camoufox-related support stacks on `oracle-proxy` should be treated as historical/auxiliary registration tooling rather than standalone active service surface for ops tracking.
- Updated infra docs accordingly so ops-assistant does not treat Tavily/Grok camoufox support components as separate undocumented project residue.
- Confirmed several compose-era directories on `oracle-proxy` were only historical leftovers and no longer needed:
  - `/root/AntiCAP-WebApi-docker`
  - `/root/FlareSolverr`
  - `/root/ProxyCat`
  - `/root/clove`
  - `/root/gpt-load`
  - `/root/backups/grok2api-20260313-133823`
- Cleaned the above paths from the host instead of promoting them into active project docs.
- Future ops-assistant drift scans should treat those paths as removed historical residue, not active undocumented project candidates.

## 2026-03-16
- Recorded that `/root/OpenAi` was migrated from the current OpenClaw host to `oracle-proxy` for storage only.
- Explicitly marked the migrated `OpenAi` directory as **not running** and **not part of the active service map**.
- Added dedicated archive note: `./projects/openai-migrated.md`.
- Future operational checks on `oracle-proxy` should treat `/root/OpenAi` as migrated material unless process / port / container evidence proves otherwise.
- Performed a read-only host health check over SSH. Current snapshot: uptime ~17 days, root disk 40% used, memory healthy, and main long-lived containers (`proxy-tavily-proxy-1`, `tavily-scheduler`, `tavily-camoufox*`, `grok-register-camoufox*`, `grok2api`, `cliproxy`) all appeared up. No immediate resource-pressure signal observed.
- Confirmed Tavily proxy admin password on-host is `Zxm971004` via `/root/tavily-key-generator/proxy/.env` and retained env-driven password loading instead of hardcoding compose.
- Confirmed Tavily generator on-host config now uses `EMAIL_ADMIN_PASSWORD = "Zxm971004"`, `EMAIL_SITE_PASSWORD = "Zxm971004"`, and `PROXY_ADMIN_PASSWORD = "Zxm971004"` in `/root/tavily-key-generator/config.py`.
- Changed Tavily generator batch size from `RUN_COUNT = 1` to `RUN_COUNT = 5` while keeping `RUN_THREADS = 1`.
- Changed Tavily scheduler cadence from `TAVILY_INTERVAL_SECONDS = 2160` to `10800`, making the effective behavior approximately one 5-attempt batch every 3 hours.
- Recreated `tavily-scheduler` and verified fresh startup logs show `interval=10800s` and `配置: 5 个账户 / 1 线程`.
- Verified proxy health after the change: local `/api/stats` returned HTTP 200 with a non-empty key pool (`keys_total=45`, `keys_active=45`).
- Documented `ExaFree` on this host under `/root/ExaFree` and added dedicated project note `./projects/exafree.md`.
- Set ExaFree `.env` admin key to deployed value `Zxm971004` and verified the running container is healthy on port `7860`.
- Switched ExaFree registration behavior to a low-volume jittered host-side schedule:
  - `basic.register_default_count = 1`
  - cron wakes every 30 minutes
  - each run sleeps a random `0-15` minutes before acting
  - each run attempts only one registration
  - overlapping runs / active register tasks are skipped
- Verified ExaFree health after the change: local `http://127.0.0.1:7860/health` returned HTTP 200 with `{"status":"ok"}`.
- Verified ExaFree web UI auth is separate from `ADMIN_KEY`: the portal uses `/auth/login` with username/password, while legacy admin-key auth still uses `/login`.
- Reset the on-host ExaFree `admin` web password to restore portal access; secret value intentionally omitted from infra docs.
- Connected local `search-layer` Exa source to ExaFree using an ExaFree user API key rather than an official direct Exa key.
- Standardized the local integration contract:
  - `~/.openclaw/credentials/search.json` now supports object-form Exa config: `exa.apiUrl + exa.apiKey`
  - local `skills/search-layer/scripts/search.py` routes object-form Exa config to `POST {apiUrl}/search`
  - ExaFree auth for search-layer uses a user API key, not `ADMIN_KEY` and not the web admin password
- Verified local Exa path works end-to-end with `search.py "OpenAI latest news" --mode fast --source exa --num 3` returning Exa-sourced results through ExaFree.

## 2026-03-15
- Documented oracle-proxy host baseline, network surface, and main deployed projects.
- Finalized Tavily chain integration:
  - deployed and verified Tavily proxy on port 9874
  - imported historical keys into proxy
  - fixed password handling to use `.env`
  - fixed registration auto-upload by using `host.docker.internal:9874` inside container
  - verified fresh registrations auto-upload to proxy
  - created a working proxy token and verified `/api/search`
- Updated local search-layer to consume Tavily through `proxy.zhangxuemin.work:9874/api`.
- Deepened oracle-proxy documentation with second-pass details for:
  - system nginx vs sing-box-owned nginx distinction
  - sing-box / xray machine-level network stack
  - grok2api compose/runtime details
  - cliproxy host-side config and mounts
- Third-pass documentation improvements:
  - cliproxy now documented as an OAuth/auth-file-backed OpenAI-compatible proxy with safe operational notes
  - grok2api now documents health endpoints, OpenAPI surface, admin route families, and local persistence layout
  - explicitly noted that auth/token material exists on-host and must not be copied into general infra notes
