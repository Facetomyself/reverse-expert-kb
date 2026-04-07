# MEMORY.md

- 2026-04-07: User preference: in this private direct-control environment, OpenClaw should avoid requiring manual click approvals for routine execution. Keep exec approvals configured for low-friction operation on the gateway unless the user asks to tighten security.

- 2026-03-07: For openclaw-search-skills on this host, only use the user-provided API tokens from ~/.openclaw/credentials/search.json. When a search source is not explicitly specified, default to using Grok only (exa/tavily disabled unless the user asks).

- 2026-03-12: Headless cloud server (no GUI). Prefer CLI-only instructions; do not ask the user to "look at the screen"—have them paste terminal output when needed. Tooling/runtime baselines:
  - OS: Ubuntu 22.04.5 LTS (arm64/aarch64)
  - OpenClaw: /usr/bin/openclaw — OpenClaw 2026.3.11 (updated 2026-03-13)
  - Node.js: /usr/bin/node v22.22.1
  - Python: /usr/bin/python3 3.10.12
  - uv: /root/.local/bin/uv 0.10.7
  - summarize CLI: /usr/bin/summarize 0.12.0
  - GitHub CLI: /usr/bin/gh 2.4.0+dfsg1
  - TLS/CA note: Node HTTPS may fail with "unable to get local issuer certificate" unless NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt is set (system bundle at /etc/ssl/certs/ca-certificates.crt).

- 2026-03-13: Post-maintenance notes:
  - System upgraded + rebooted to kernel 6.8.0-1044-oracle; verified SSH(22)/Nginx(80/443)/OpenClaw gateway(127.0.0.1:18789) OK.
  - Fixed ufw.service failure (xtables lock contention) by disabling netfilter-persistent; ufw active allowing 22/80/443.
  - Fixed root PATH overrides to include /usr/sbin:/sbin.
  - GitHub: gh auth configured and working.
  - Workspace skills: removed symlink-escape by copying search-layer/content-extract/mineru-extract into workspace; search-layer works; MinerU tools need MINERU_TOKEN.
  - grok2api_sdk PRs opened: #1 (hardening/dotenv/examples), #2 (responses + /v1/videos), #3 (robust SSE parser), #4 (tests + CI).
  - `summarize` is now configured and working through the local OpenClaw cliproxy OpenAI-compatible endpoint, using default model `openai/gpt-5.4`.
  - Effective summarize setup:
    - `~/.summarize/config.json` sets model to `openai/gpt-5.4`
    - `~/.profile` exports `OPENAI_BASE_URL=http://proxy.zhangxuemin.work:8317/v1` and the cliproxy API key
  - Important caveat: `summarize` worked with GPT models via the proxy, but `summarize` + `openai/gemini-3-flash` returned empty summaries even though direct proxy calls to the Gemini model worked.
  - Added a silent hourly OpenClaw cron workflow `research:reverse-expert-kb` that builds a reverse-engineering expert knowledge base under `research/reverse-expert-kb/` (research/synthesis only, Markdown outputs, sources organized, no chat delivery).

- 2026-03-14: reverse-expert-kb direction hardened from abstract taxonomy toward concrete, case-driven, code-adjacent workflow material. The KB now uses a paired structure where mature synthesis branches are being complemented by practical workflow notes. Notable new mobile/protected-runtime workflow notes added on 2026-03-14 include:
  - `topics/mobile-signature-location-and-preimage-recovery-workflow-note.md`
  - `topics/mobile-challenge-trigger-and-loop-slice-workflow-note.md`
  - `topics/android-observation-surface-selection-workflow-note.md`
  - `topics/environment-differential-diagnosis-workflow-note.md`
  This means the KB is evolving from a topic map into a more usable investigator playbook with a diagnosis layer (classifying drift as execution / trust / session / observation) and deeper operational branches for signature recovery, challenge-loop analysis, and observation-surface selection.

- 2026-03-15: On oracle-proxy, `skernelx/tavily-key-generator` is now working end-to-end against the private tmail worker. The verification-mail blocker was fixed by making the mail parser handle quoted-printable / soft-wrapped Auth0 verification links and by supporting richer private-worker mail reads. Full flow verified: signup, Turnstile solve, email verification, login, and API-key capture.

- 2026-03-15: Tavily is intentionally isolated from Grok's Turnstile solver stack on oracle-proxy. Grok keeps its existing `grok-register-camoufox-adapter` on host port `15072`; Tavily now has its own `camoufox` + `camoufox-adapter` stack under `/root/tavily-key-generator`, exposed on host port `16072`, and uses `TURNSTILE_ADAPTER_URL = "http://camoufox-adapter:5072"` inside its compose network. A smoke test confirmed Tavily hits its private adapter, not Grok's. Related git commit in `/root/tavily-key-generator`: `fa6ea2c` (`isolate tavily turnstile solver from grok stack`).

- 2026-03-15: Tavily on oracle-proxy now also has a compose-based scheduler instead of relying on accidental container restarts. The deployed service set is `tavily-scheduler` + `tavily-camoufox` + `tavily-camoufox-adapter`, with `TAVILY_INTERVAL_SECONDS=2160` so it attempts roughly one registration every 36 minutes (about 5 per 3 hours). Scheduler interpolation bugs in compose were fixed by escaping shell variables. Related git commit in `/root/tavily-key-generator`: `1ff1f5d` (`add scheduled isolated tavily registration stack`).

- 2026-03-15: Additional host workflow realities now worth remembering:
  - Raw Brave-backed `web_search` is currently unavailable/unconfigured here; prefer the `search-layer` skill path for research.
  - `web_fetch` is unreliable for some academic/PDF/anti-bot sources and some Chinese content platforms; prefer HTML landing pages, abstracts, GitHub pages, and official docs when readable extraction matters.
  - For GitHub work on this host, `gh` is old enough that newer examples/subcommands/JSON fields may fail; verify locally instead of assuming current upstream CLI behavior.
  - Host inventory correction: SSH alias `oracle-open_claw` / IP `64.110.106.11` is this local machine, not a separate remote Oracle host to audit next. The Cloudflare export note on `dev.zhangxuemin.work` (`n8n`) is stale and should not be treated as current role truth without fresh verification.

- 2026-03-15: Tavily proxy/search-layer integration is now wired end-to-end.
  - On oracle-proxy, the Tavily proxy Web console runs at `http://proxy.zhangxuemin.work:9874` with admin password `Zxm971004`.
  - The Tavily registration pipeline is now connected to the proxy: historical keys were imported, and newly registered keys auto-upload into the proxy pool.
  - Inside the oracle-proxy registration container, the working proxy target is `PROXY_URL = "http://host.docker.internal:9874"`; for external/client use, prefer the public domain `http://proxy.zhangxuemin.work:9874`.
  - On this host, `~/.openclaw/credentials/search.json` now configures Tavily for the `search-layer` skill in object form with:
    - `apiUrl`: `http://proxy.zhangxuemin.work:9874/api`
    - `apiKey`: the current Tavily proxy token
  - `skills/search-layer/scripts/search.py` was updated to support Tavily object credentials (`apiUrl` + `apiKey`) and a custom Tavily base URL instead of assuming only the official `https://api.tavily.com` endpoint.
  - Verified locally: `search.py --mode answer --source tavily` now returns results successfully through `proxy.zhangxuemin.work:9874`.

- 2026-03-23: For oracle-proxy `/root/grok2api`, the safe long-term git topology is now:
  - `origin = Facetomyself/grok2api` (personal fork)
  - `upstream = chenyme/grok2api` (canonical upstream)
  - `legacy-tqzhr = TQZHR/grok2api` (historical reference only)
  - preserved production custom branch: `oracle-proxy/local-custom-20260321` @ `2413e6c`
  - selective integration branch: `oracle-proxy/safe-sync-20260323`
  Direct full-sync to `chenyme/main` is considered unsafe because current oracle-proxy deployment contains registration-sensitive local customizations and older code layout; future updates should be manually ported in small commits and pushed to the fork before any deployment.
