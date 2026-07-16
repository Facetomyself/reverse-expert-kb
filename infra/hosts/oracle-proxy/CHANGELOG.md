# oracle-proxy / Change Log

## 2026-07-06 — GPT Session Converter static site deployed
- Fork status was reconciled for `gtxx3600/GPTSession2CPAandSub2API`: existing `Facetomyself/GPTSession2CPAandSub2API` fork had diverged, so the old fork main was preserved as `archive/fork-main-before-upstream-sync-20260706`, then fork `main` was aligned to upstream commit `a097eb155bb7bdf6cbbc26f1e4e75e120ab3163c`.
- Deployed the static browser-only tool under `/root/containers/gpt-session-converter`, serving `/root/containers/gpt-session-converter/docs` through `caddy-cpam` as `https://gpt-session.zhangxuemin.work/`.
- Added Cloudflare DNS-only A records for `gpt-session.zhangxuemin.work -> 158.178.236.241` and `gpt-session-cn.zhangxuemin.work -> 154.86.30.10`.
- Added HK edge route on `hk-relay`: `gpt-session-cn.zhangxuemin.work -> https://gpt-session.zhangxuemin.work` with origin Host/TLS SNI preserved.
- Verification: both global/source and CN/HK HTTPS entries returned HTTP 200 and served the expected static HTML.

## 2026-07-06 — Nightly read-only check
- Snapshot at `2026-07-06 03:00 GMT+8`: uptime 83d, load `0.17 0.19 0.20`, root disk `45G total / 21G used / 25G free` (`45%` used), memory `11Gi` total with `7.9Gi` available, no swap. 15 long-lived containers all up (same set including `proxy4reverse`). Top MEM: warp-svc 1.6GB. No new drift or concerning listeners.

## 2026-07-05 — Nightly read-only check
- Snapshot at `2026-07-05 03:01 GMT+8`: uptime 82d, load `0.10 0.16 0.18`, root disk `45G total / 21G used / 25G free` (`46%` used, +2% from last check), memory `11Gi` total with `7.9Gi` available, no swap. 15 long-lived containers up (same set including `proxy4reverse`). Top MEM: grok2api-camoufox-solver 4.96%. No new drift or concerning listeners.

## 2026-07-03 — Nightly read-only check
- Snapshot at `2026-07-03 03:02 GMT+8`: uptime 80d, load `0.35 0.20 0.22`, root disk `45G total / 20G used / 26G free` (`44%` used), memory `11Gi` total with `7.9Gi` available, no swap. 14 long-lived containers up (same set as last check). 14 zombie `[curl]` processes persistent (low risk). No new drift.

## 2026-06-25 — Nightly read-only check
- Snapshot at `2026-06-25 03:00 GMT+8`: uptime 72d, load `0.74 0.31 0.23`, root disk `45G total / 20G used / 26G free` (`44%` used), memory `11Gi` total with `8.1Gi` available, no swap. 14 long-lived containers up. **13 zombie processes detected** (new observation — low risk but worth monitoring). Ubuntu 20.04 Focal EOL (May 2025) — 167 ESM security updates pending. Journal 450MB (cap working). No concerning listener drift.

## 2026-06-24 — Nightly read-only check
- Snapshot at `2026-06-24 03:00 GMT+8`: uptime 71d, load `0.06 0.15 0.17`, root disk `45G total / 20G used / 26G free` (`44%` used), memory `11Gi` total with `8.1Gi` available, no swap. 14 long-lived containers up including `zcode2api` (up 29h, new since last check). Docker overlay2 at 15G. Journal 472MB (within cap). No concerning drift.

## 2026-06-17 / CLIProxy and CPA Manager Plus update helpers
- Fixed primary CLIProxy update helper `/root/update_cliproxy.sh`. The old helper compared the current container through mutable `Config.Image=eceasy/cli-proxy-api:latest`; after `docker pull`, that tag could already point to the new image while the running container still used an old SHA, causing a false "image unchanged" skip.
- New primary helper compares the running container's immutable image SHA (`docker inspect .Image`) against the pulled target image ID, supports `CLIPROXY_IMAGE=...`, `--dry-run`, `--force-recreate`, and rollback, and validates container running state, port `8317`, and local `/management.html` HTTP 200.
- Ran the fixed helper successfully: primary `cliproxy` was recreated from old running image `sha256:249c97b7...` (`v7.1.44` lineage) to current `eceasy/cli-proxy-api:latest` image `sha256:12f36000...`; local root and `/management.html` checks returned HTTP 200.
- Added Plus manager helper `/root/update_cpa_manager_plus.sh` for `cpa-manager-plus`, using the same immutable running-image-SHA comparison pattern with Compose recreate, `CPA_MANAGER_PLUS_IMAGE=...`, `--force-recreate`, health checks for `/management.html`, `/health`, and `/usage-service/info`, plus rollback to the previous running image SHA if needed.
- Forced a Plus manager upgrade after extending the helper to validate both public panel entrypoints. `docker pull` downloaded newer image `sha256:064beb4c...` (digest `sha256:194bafe7...`), `cpa-manager-plus` was recreated and became healthy, and both `https://cpam.zhangxuemin.work/management.html` and `https://cpam-cn.zhangxuemin.work/management.html` returned HTTP 200.
- Old primary helper backup retained at `/root/update_cliproxy.sh.bak-20260617-030559`.

## 2026-06-07 / retired Tavily and Grok Camoufox cleanup
- Per user instruction, fully removed long-unused Docker runtime objects for the legacy Tavily registration scheduler/Camoufox stack: `tavily-scheduler`, `tavily-camoufox`, and `tavily-camoufox-adapter`. These containers had already been exited for roughly two months.
- Fully removed long-unused Docker runtime objects for the legacy Grok register Camoufox stack: `grok-register-camoufox` and `grok-register-camoufox-adapter`. This closed the previous public adapter listener on `:15072`.
- Removed matching local images for the cleaned stacks and removed Docker networks `tavily-key-generator_default` and `grok-register-standalone_default`. Docker image footprint dropped from about `11.03GB` to about `4.40GB`.
- Preserved source/archive directories but disabled accidental restart by renaming root compose files to `docker-compose.retired-20260607.yml` and writing retirement marker files under `/root/tavily-key-generator` and `/root/grok-register-standalone`.
- Verified the listed containers no longer exist, matching images no longer remain, and `ss -ltnp` no longer shows `:15072` or `:16072`. Active services including `proxy-tavily-proxy-1`, `grok2api`, and the newly deployed `kiro-rs` were preserved.


## 2026-06-07 / Kiro-RS deployment
- Checked `oracle-proxy` capacity before deployment: root disk `45G total / 25G used / 21G free` (`55%` used), Docker images about `11.01GB`, containers about `1.681GB`, and memory comfortable (`11Gi total`, about `8.3Gi available`).
- Deployed `Kiro-RS` from `https://github.com/hank9999/kiro.rs` under `/root/containers/kiro-rs` using upstream image `ghcr.io/hank9999/kiro-rs:latest`.
- Runtime is loopback-only on the source host: container `kiro-rs`, Docker publish `127.0.0.1:18769 -> 8990/tcp`, restart policy `unless-stopped`.
- Initialized sensitive config under `/root/containers/kiro-rs/config`: `config.json` with generated API/Admin API keys and `credentials.json` as an empty array for later credential addition through Admin UI/API.
- Added Cloudflare DNS records: `kiro-rs.zhangxuemin.work -> 158.178.236.241` and `kiro-rs-cn.zhangxuemin.work -> 154.86.30.10`.
- Added source Caddy route in `/root/containers/caddy-cpam/Caddyfile` and HK edge route in `hk-relay:/etc/caddy/Caddyfile`; both Caddy configs validated and reloaded.
- Verified local authenticated `/v1/models` returned HTTP 200; forced-resolution HTTPS checks for both direct and CN routes also returned HTTP 200. Local resolver propagation was still pending immediately after DNS creation.


## 2026-06-06 / GPTAM automatic mailbox status filters
- Added deployment-local project commit `1f65603` (`feat: expose automatic mailbox status groups`).
- Mailbox-management UI now exposes automatic status groups as filters: “未完成注册”, “收件异常”, and “已封禁邮箱”.
- Date/manual group filters are now status-exclusive: they only include normal accounts, while unregistered/mail-error/banned accounts are pulled out into their automatic groups.
- The change remains display/filter-only and does not rewrite stored mailbox `category` values, preserving import-date metadata.
- Rebuilt/recreated the container and verified authenticated `mailboxes.html`, `mailboxes.js`, and `styles.css` contain the new filters/rules.

## 2026-06-06 / GPTAM unregistered grouping evidence fix
- Added deployment-local project commit `3f2d63c` (`fix: base unregistered grouping on verification mail evidence`).
- Corrected the previous unregistered-account classifier: “missing verification code” text is not a mailbox signal, because no email says that a code is missing.
- The mailbox-management page now reads cached `mail_type=verification` messages, filters for OpenAI/ChatGPT verification evidence, and annotates checked accounts with `has_openai_verification_mail`.
- “未完成注册账号” now means a checked mailbox has no matching OpenAI verification mail evidence (or a completed check found zero messages), not that an error string mentioned missing codes.
- Rebuilt/recreated the container and verified authenticated `mailboxes.js` plus `/client-api/messages?mail_type=verification` responses.

## 2026-06-06 / GPTAM unregistered mailbox grouping
- Added deployment-local project commit `e5e169a` (`feat: group unregistered mailbox accounts`).
- Extended mailbox-management status grouping with “未完成注册账号” for accounts whose latest mail verification/check result has no OpenAI verification code evidence.
- Classification signals: `mail_verify_status` / `last_status` = `no_code`-style states, `last_error_code` = `verification_code_missing` / related codes, Chinese/English missing-code hints, or a completed mail check with `last_message_count = 0` and no fetch error.
- Kept the change display-only: it does not rewrite account data or user-assigned group names.
- Rebuilt and recreated the `gpt-account-manager` container; verified authenticated requests served the updated JS/CSS and health became green.

## 2026-06-06 / GPTAM mailbox status grouping
- Added deployment-local project commit `dcbb8f0` (`feat: group mailbox accounts by status`).
- Existing mailbox logic already identified banned/deactivated accounts from `last_status`, `last_error`, `last_error_code`, `last_error_label`, and `last_error_hint`; the UI previously mixed these rows with normal accounts in the default list.
- Updated `static/mailboxes.js` and `static/styles.css` so the account-management table sorts and visually separates normal accounts, error accounts, and banned/deactivated accounts without changing user-assigned groups or stored account data.
- Rebuilt and recreated the `gpt-account-manager` container; verified authenticated requests served the updated JS/CSS and `mailboxes.html`.

## 2026-06-06 / GPTAM formal login
- Replaced the temporary Caddy Basic Auth stopgap with a formal app-level login page for GPT Account Manager.
- Deployment-local project commit: `43d7676` (`feat: add optional site-wide login`).
- Minimal code shape: `GPT_ACCOUNT_MANAGER_REQUIRE_LOGIN=1` enables full-site login using the existing `/login.html`, `/auth/login`, admin cookie, and `MAIL_PICKUP_ADMIN_TOKEN`; Caddy now only performs TLS/reverse proxy.
- Verified direct entry redirects unauthenticated users to `/login.html?next=/`, login page renders, token login returns success, and cookie-authenticated GET returns `<title>GPT账号管理助手`.
- Verified CN/HK entry behaves the same through `gptam-cn.zhangxuemin.work`.

## 2026-06-06 / GPTAM auth hardening
- Confirmed upstream `MAIL_PICKUP_ADMIN_TOKEN` protects `/admin.html`, `/health.html`, and `/admin-api/*`, but not the whole GPT Account Manager workbench.
- Added Caddy full-site Basic Auth to both `gptam.zhangxuemin.work` on `oracle-proxy` and `gptam-cn.zhangxuemin.work` on `hk-relay`.
- Basic Auth username: `gptam`; password is the existing `MAIL_PICKUP_ADMIN_TOKEN` stored only in `/root/containers/gpt-account-manager/.env`; Caddyfiles store bcrypt hashes only.
- Verified unauthenticated direct and CN routes return HTTP 401; authenticated GET returns `<title>GPT账号管理助手`.

## 2026-06-06
- Deployed `GPT Account Manager` from `https://github.com/margetrp-hub/gpt-account-manager` under `/root/containers/gpt-account-manager`.
- Corrected the upstream compose exposure so the app binds only to `127.0.0.1:18765` instead of exposing public `:8765`.
- Added Cloudflare DNS records `gptam.zhangxuemin.work -> 158.178.236.241` and `gptam-cn.zhangxuemin.work -> 154.86.30.10`.
- Added source Caddy route in `/root/containers/caddy-cpam/Caddyfile` and HK edge route in `hk-relay:/etc/caddy/Caddyfile`.
- Because `1panel` owns public `:80` on `oracle-proxy`, configured the GPTAM Caddy site to avoid HTTP-01 and use TLS-ALPN-01.
- Verified the container was healthy and both direct/HK GET routes returned `<title>GPT账号管理助手`.
## 2026-04-14
- Recurring Oracle-scoped nightly read-only check reconfirmed `oracle-proxy` remained reachable and otherwise healthy in its documented proxy/utility role. Snapshot at `2026-04-13 19:04 UTC`: uptime ~20.4 days, load idle (`0.00 0.02 0.02`), root disk `45G total / 23G used / 23G free` (`51%` used), memory comfortable (`11Gi` total, ~`10Gi` available), no swap configured, and the expected long-lived containers remained up (`cliproxy`, `grok2api`, `grok2api-camoufox-solver`, `exafree`, `proxy-tavily-proxy-1`, `grok-register-camoufox`, `grok-register-camoufox-adapter`).
- One concise runtime delta only: the previously documented temporary public Python HTTP residue on `:18734` was no longer present in this pass, so that stale transfer/distribution surface currently appears cleared.

## 2026-04-11
- Recurring Oracle-scoped read-only check reconfirmed `oracle-proxy` remained reachable and otherwise broadly consistent with the documented proxy/utility role (`45G total / 23G used / 23G free`, `51%` used; memory still comfortable; expected long-lived containers still up).
- One meaningful runtime delta only: the host is currently exposing an additional public temporary HTTP listener on `0.0.0.0:18734` via `python3 -m http.server 18734 --bind 0.0.0.0` running from `/root/tmp-models` (process start observed as `Apr 09`). The served directory now appears nearly empty (`http.log`, `http.pid`, `serve-models.sh` only), so this is tracked as stale temporary transfer/distribution residue rather than part of the documented baseline service map.

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

## 2026-06-06 — Kiro docs static site deployed
- Added public static Kiro documentation site on `oracle-proxy`:
  - global/source: `https://docs.zhangxuemin.work/`
  - source files: `/root/containers/kiro-docs/site`
  - Caddy static root inside container: `/srv/kiro-docs`
- Built with VitePress from `https://github.com/Facetomyself/kiro`, using only `使用说明.md` plus required image/logo assets.
- Added security headers and cache headers on the source Caddy site.
- Verification: `https://docs.zhangxuemin.work/` returned HTTP 200; sample image returned HTTP 200; existing `https://kiro.zhangxuemin.work/admin` remained HTTP 200.

## 2026-06-06 — Kiro docs anti-abuse protection added
- Installed/enabled `fail2ban` on `oracle-proxy`.
- Added Caddy JSON access log for `docs.zhangxuemin.work`: `/var/log/caddy/docs-access.log`.
- Added docs-specific fail2ban filters/jails:
  - `openclaw-docs-general`: 180 requests / 60s -> 30m ban
  - `openclaw-docs-assets`: 90 static/image requests / 60s -> 1h ban
- Added `hk-relay` to `ignoreip` so `docs-cn` origin traffic cannot ban the HK edge at source.
- Verification: synthetic 95-hit static asset log test banned/unbanned the test IP successfully; docs and Kiro-Go URLs remained HTTP 200.

## 2026-06-06 — Card Shop MVP deployed
- Deployed `card-shop` on `oracle-proxy` under `/root/containers/card-shop`, bound only to `127.0.0.1:18767`.
- Added global/source endpoint `https://card.zhangxuemin.work/` through `caddy-cpam`.
- Added Cloudflare DNS-only A record `card.zhangxuemin.work` -> `158.178.236.241`.
- Implemented public redeem/query, admin login, JSON batch generation, card search/detail/history, and SQLite persistence.
- Card code default is `KIRO-` plus 32 human-safe random characters grouped with hyphens (about 160-bit entropy).
- Added app-level Express limits and fail2ban jails `openclaw-card-general` / `openclaw-card-api`.
- Verification: global/CN public pages returned HTTP 200; admin generated test cards; unredeemed query failed; redeem/query after redeem succeeded; API fail2ban synthetic trigger test succeeded; existing Kiro/docs endpoints remained HTTP 200.


## 2026-06-06 — Card Shop admin hardening and test cleanup
- Reworked Card Shop from MVP/demo-like UI into a normal management backend.
- Visitor page text was simplified and internal/debug/test wording removed.
- Public APIs now hide internal payload/admin notes and return only minimal redeemed-card status.
- Added admin delete, bulk delete/disable/enable, per-card status controls, and global redeem on/off switch.
- Cleared smoke-test / length-check / admin-check cards plus orphan test events from the live SQLite DB. Final DB verification: no cards, no events, `redeem_enabled=1`.
- Regression: `card.zhangxuemin.work`, `card-cn.zhangxuemin.work`, and admin login returned HTTP 200 after redeploy.


## 2026-06-06 — Card Shop delivery JSON behavior corrected
- Corrected earlier over-hardening: `payload_json` is the actual card delivery content, not a hidden internal/debug field.
- Public redeem success and post-redeem query now return the stored JSON payload.
- Pre-redeem query still returns non-disclosing 404 and does not leak payload.
- Admin generation wording now explicitly says `payload` is the JSON users receive after redeeming.
- Verified with nested JSON payload; redeem and query returned intact JSON; temporary verification card was deleted.


## 2026-06-06 — Card Shop one-JSON-one-card model
- Corrected generation model to one delivery JSON per card code.
- Removed same-payload count batching semantics.
- Added canonical delivery JSON hashing and uniqueness via `delivery_hash`; duplicate JSON inputs are skipped.
- Admin generator supports a single JSON object, an object array, and multi-file JSON selection/merge.
- Card list now exposes direct per-row delete controls.
- Verified two unique JSON objects -> two card codes, duplicate resubmit -> zero new codes / two skipped, pre-redeem no leak, redeem returns matching JSON, and temporary verification cards cleaned up.


## 2026-06-06 — Card Shop select-all control fixed
- Fixed the card management list select-all checkbox.
- Replaced fragile inline checkbox handling with a `data-select-all` master checkbox and explicit script binding for row checkboxes.
- Verification: admin search page contained the master checkbox, row checkboxes, and select-all script; temporary verification cards were cleaned up; public/admin endpoints remained HTTP 200.


## 2026-06-06 — Card Shop public delivery JSON display fixed
- Removed customer-side redeem remark input; remarks are admin-only/internal and customers should not submit notes to the card site.
- Public redeem/query success now renders the delivered JSON in an editable textarea with a copy button instead of plain appended text.
- Verification: public page no longer contains `redeemed_by`/customer remark field, contains JSON textarea/copy UI script, redeem returns payload and empty `redeemed_by`, temporary verification card cleaned up, global/CN card endpoints returned HTTP 200.

## 2026-06-07
- Card Shop: cleared post-test inventory/events and listed two live `Kiro-Go / pro` delivery JSON cards from the `Facetomyself/kiro` repository. Verified DB status `new=2` and CN public entry HTTP 200. Backup created before mutation under `/root/containers/card-shop/data/cardshop.db.bak-before-kiro-prod-*`.
- Card Shop: restored live Kiro payload display order to repository JSON order and changed generation logic to preserve input key order for delivered JSON while keeping canonical duplicate hashing.
- Card Shop: corrected the two live Kiro cards to store/deliver the original repository JSON file content, including top-level array wrapper and formatting, instead of parsed object payloads.
- Card Shop: reissued the two Kiro cards from scratch using original repository JSON file content; deleted prior ambiguous rows/events and verified both new cards are `new` plus CN entry HTTP 200.
## 2026-06-07 / GPT Card Shop initial deployment
- Deployed `gpt-card-shop` under `/root/containers/gpt-card-shop`, binding only to loopback `127.0.0.1:18768 -> 3000`.
- Implemented ChatGPT account/card delivery with format-aware conversion downloads: CPA zip, sub2api merged JSON, and original JSON zip.
- Added source Caddy route for `gpt-card.zhangxuemin.work` to `127.0.0.1:18768`, with JSON access log `/var/log/caddy/gpt-card-access.log`.
- Added source fail2ban jails `openclaw-gpt-card-general` and `openclaw-gpt-card-api`.
- Verified direct health/homepage and end-to-end smoke test with synthetic account; smoke data cleaned afterward.
- Added live Cloudflare DNS-only A records for `gpt-card.zhangxuemin.work` -> `158.178.236.241` and `gpt-card-cn.zhangxuemin.work` -> `154.86.30.10`; both source and CN HTTPS health checks returned HTTP 200 after certificate issuance.
## 2026-06-07 / oracle-proxy HTTP redirect ownership fix
- Fixed `http://gpt-card.zhangxuemin.work/` showing the 1Panel page. Root cause: 1Panel was still configured on public `:80`, while Caddy only owned `:443`.
- Backed up `/opt/1panel/db/1Panel.db` and `/root/containers/caddy-cpam/Caddyfile`.
- Changed 1Panel origin `ServerPort` from `80` to `18080`, added Caddy reverse proxy `proxy.zhangxuemin.work -> 127.0.0.1:18080` to preserve domain-based 1Panel access, removed Caddy global `auto_https disable_redirects`, and restarted 1Panel + `caddy-cpam`.
- Verified Caddy now owns public `:80/:443`; `http://proxy...` redirects to HTTPS and HTTPS returns the 1Panel UI; `http://gpt-card...` and existing `http://card...` redirect to HTTPS; source/CN GPT Card Shop health checks return HTTP 200.


## 2026-06-21 — Nightly read-only check
- Snapshot at `2026-06-21 03:01 GMT+8`: uptime 68d, load `0.20 0.28 0.24`, root disk `45G total / 20G used / 26G free` (`43%` used, improved from prior ~51%), memory `11Gi` total with `8.2Gi` available, no swap.
- All 12 long-lived containers remain up: `cpa-manager-plus`, `cliproxy`, `gpt-card-shop`, `cliproxy-backup`, `kiro-rs`, `card-shop`, `caddy-cpam`, `kiro-go`, `gpt-account-manager`, `grok2api`, `grok2api-camoufox-solver`, `exafree`, `proxy-tavily-proxy-1`.
- No new drift or concerning listeners observed.

- 2026-06-26: Nightly read-only check confirmed `oracle-proxy` healthy. Snapshot at `2026-06-26 03:03 GMT+8`: uptime 73d, load `0.28 0.29 0.21`, root disk `45G total / 20G used / 26G free` (`45%` used), memory `11Gi` total with `8.1Gi` available, no swap. 14 long-lived containers up: `zcode2api` (3d), `cpa-manager-plus` (8d, healthy), `cliproxy` (8d), `grok2api` (2mo), `grok2api-camoufox-solver` (2mo), `exafree` (2mo, healthy), `proxy-tavily-proxy-1` (2mo), `gpt-account-manager` (2wk, healthy), `kiro-go` (2wk), `gpt-card-shop` (2wk), `cliproxy-backup` (2wk), `kiro-rs` (2wk), `card-shop` (2wk), `caddy-cpam` (2wk). Additional listeners: nginx `:30011`, 1panel `:18080`, python3 `:18084`. No new drift or concerning listeners observed.

- 2026-07-07: Nightly read-only check confirmed `oracle-proxy` healthy. Snapshot at `2026-07-07 03:01 GMT+8`: uptime 84d, load idle (`0.00 0.06 0.14`), root disk `45G total / 20G used / 26G free` (`43%` used, improved from 45%), memory `11Gi` total with `7.8Gi` available, no swap. 14 long-lived containers up (same set; `caddy-cpam` up 11h, `proxy4reverse` up 2d, `zcode2api` up 2w, rest 2w–2mo). No systemd failures. No concerning drift.
