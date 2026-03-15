# Errors Log

Command failures, exceptions, and unexpected behaviors.

---
## [ERR-20260315-006] web-fetch-doc-redirect-fragility-on-official-docs

**Logged**: 2026-03-15T07:17:59Z
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
During reverse-expert-kb source gathering, `web_fetch` failed on some official documentation URLs because redirect chains exceeded the tool limit, even though the final canonical pages were public and readable when fetched directly.

### Error
```text
web_fetch: Too many redirects (limit: 3)
```

### Context
- Operation attempted: fetch Android Developers WebView bridge documentation and Android WebView API reference during hybrid WebView/native bridge workflow research
- Initial URLs used stable official docs, but the fetcher hit redirect chains and aborted
- Workaround used: continue with search-layer results and manually fetch the final canonical OWASP MASTG path directly when available
- This is a source-access fragility issue, not a blocker for conservative KB synthesis

### Suggested Fix
When `web_fetch` hits redirect limits on official docs, try the final canonical path directly or fall back to search-layer/result snippets instead of retrying the same redirecting URL.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/research/reverse-expert-kb/
- See Also: ERR-20260315-003

---
## [ERR-20260315-005] exact-edit-miss-on-drifted-kb-navigation

**Logged**: 2026-03-15T10:19:30+08:00
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
A precise `edit` call failed during reverse-expert-kb navigation updates because the expected bullet block in `index.md` had drifted and no longer matched the exact old text.

### Error
```text
Could not find the exact text in /root/.openclaw/workspace/research/reverse-expert-kb/index.md.
The old text must match exactly including all whitespace and newlines.
```

### Context
- Operation attempted: insert the new YouTube workflow-note link into the browser subtree list in `index.md`
- The failure did not block work; a targeted read of the surrounding section made it easy to repair with a second exact edit
- This is a recurring workflow gotcha when repeatedly editing evolving Markdown indices with exact-match replacement

### Suggested Fix
When updating fast-moving KB navigation pages with `edit`, read the local surrounding block first or anchor on a smaller/more stable exact string instead of a larger assumed stanza.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/research/reverse-expert-kb/index.md
- See Also: ERR-20260315-003

---
## [ERR-20260315-003] host-research-source-access-fragility-cluster

**Logged**: 2026-03-15T09:45:00+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
On this host, recurring research/source-gathering failures cluster around fragile `web_fetch` extraction for academic PDFs, anti-bot/interstitial pages, and some Chinese content platforms; Grok-backed search may also emit parse-noise after returning usable results.

### Error
```text
Representative pattern:
- web_fetch returns 403 / interstitial / degraded extraction
- direct PDF fetch returns raw %PDF bytes instead of readable text
- some Chinese article hosts fail with 403/521
- search-layer Grok backend may emit trailing parse noise after usable results
```

### Context
- Recurred across reverse-expert-kb collection runs and related source-gathering tasks
- Failures often did not fully block work because fallback sources still existed
- Main operational risk is wasting time forcing brittle fetch paths or overclaiming from weak sources

### Suggested Fix
Treat this as a host-level workflow constraint:
- prefer HTML landing pages, abstracts, rendered GitHub pages, and official docs before direct PDFs
- treat anti-bot/interstitial-prone article hosts as best-effort corroboration
- use search-layer/source clustering plus conservative workflow-centered synthesis when direct extraction is weak
- treat Grok parse-noise with usable results as a soft failure, not an automatic blocker

### Metadata
- Reproducible: yes
- Related Files: AGENTS.md, TOOLS.md, MEMORY.md, /root/.openclaw/workspace/research/reverse-expert-kb/
- Cluster-Members: ERR-20260314-002, ERR-20260314-001, ERR-20260313-003, ERR-20260314-001, ERR-20260315-001, ERR-20260315-002

---
## [ERR-20260315-004] brave-web-search-unconfigured-cluster

**Logged**: 2026-03-15T09:45:30+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
Raw Brave-backed `web_search` is repeatedly unavailable in this environment because the Brave API key is not configured for the gateway/tool path.

### Error
```text
missing_brave_api_key
web_search (brave) needs a Brave Search API key.
```

### Context
- Recurred across KB research and auxiliary source-gathering runs
- Work was usually able to continue through `search-layer` or other fallback paths
- This is now a stable environment fact, not a surprising one-off failure

### Suggested Fix
Do not assume raw Brave `web_search` is available on this host. Prefer `search-layer` for research. Only configure Brave later if direct Brave coverage is specifically needed.

### Metadata
- Reproducible: yes
- Related Files: TOOLS.md, MEMORY.md, /root/.openclaw/workspace/skills/search-layer/SKILL.md
- Cluster-Members: ERR-20260314-001, ERR-20260314-001, ERR-20260314-001, ERR-20260315-001

---
## [ERR-20260315-001] web_fetch-github-raw-404-during-kb-source-expansion

**Logged**: 2026-03-15T01:18:00+08:00
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
During reverse-expert-kb browser source expansion, a `web_fetch` attempt for a guessed GitHub raw README path returned 404.

### Error
```text
web_fetch failed (404): raw.githubusercontent.com/.../README.md not found
```

### Context
- Operation attempted: broaden source coverage while exploring whether an additional browser anti-bot family deserved a concrete workflow page
- The failure did not block the run because official hCaptcha docs were already sufficient for the practical page created that run
- This is a reminder to verify repository file paths or inspect repo contents before assuming raw GitHub filenames

### Suggested Fix
When using GitHub raw URLs for KB source collection, prefer verifying the repository tree or use the rendered GitHub page first before assuming `README.md` exists at repository root.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/research/reverse-expert-kb/runs/2026-03-15-0100-hcaptcha-submit-siteverify-workflow.md

---
## [ERR-20260314-002] web_fetch-ssrn-403-and-pdf-raw-bytes

**Logged**: 2026-03-14T07:42:30Z
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
During reverse-expert-kb source collection, SSRN abstract fetch returned a Cloudflare/holding-page 403 and direct PDF fetch from USENIX returned raw `%PDF` bytes instead of extracted text.

### Error
```text
web_fetch SSRN abstract: 403 / "Just a moment..."
web_fetch USENIX PDF: raw PDF bytes rather than readable extracted text
```

### Context
- Operation attempted: collect readable source text for browser anti-debugging literature
- Successful fallback: use USENIX presentation/landing page and other HTML sources instead of direct PDF/SSRN fetches
- This is a recurring source-access pattern rather than a workflow blocker

### Suggested Fix
Prefer HTML landing pages / abstracts first for academic sources; treat direct PDF fetch and SSRN as fragile on this host and only use when extraction quality is acceptable.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/research/reverse-expert-kb/runs/
- See Also: ERR-20260315-003

---
## [ERR-20260313-001] official_grok2api_docker_image_entrypoint_mismatch

**Logged**: 2026-03-13T13:40:00+08:00
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
Official `chenyme/grok2api:latest` container failed to start with the repository `docker-compose.yml` command because `granian` was not present in the image.

### Error
```
sh: granian: not found
```

### Context
- Operation attempted: start official `chenyme/grok2api` in parallel test deployment on `oracle-proxy`
- Compose source: official repository `docker-compose.yml`
- Image: `ghcr.io/chenyme/grok2api:latest`
- Result: container restart loop, health check unavailable

### Suggested Fix
Prefer local `docker build` from the checked-out official repo for validation, or inspect the image for the intended entrypoint/runtime before using the upstream compose file as-is.

### Metadata
- Reproducible: yes
- Related Files: /root/grok2api-official/docker-compose.test.yml

---
## [ERR-20260313-002] camoufox_official_server_null_proxy_bug

**Logged**: 2026-03-13T14:19:00+08:00
**Priority**: high
**Status**: pending
**Area**: browser/infra

### Summary
Official `python -m camoufox server` crashed in Docker on oracle-proxy because it passed `proxy: null` into the underlying Playwright launch server flow.

### Error
```
Error launching server: proxy: expected object, got null Failed to launch browser.
RuntimeError: Server process terminated unexpectedly
```

### Context
- Project: grok-register-standalone
- Service: grok-register-camoufox
- Image: official-package-based camoufox server build
- Environment: no proxy configured

### Suggested Fix
Use a minimal wrapper around official Camoufox launch logic that removes the `proxy` key when it is null/None before launching the websocket server.

---
## [ERR-20260313-001] github-gh-json-field-mismatch

**Logged**: 2026-03-13T09:09:00Z
**Priority**: medium
**Status**: resolved
**Area**: infra

### Summary
`gh run list --json displayTitle,workflowName` failed on this host because the installed GitHub CLI version exposes older JSON fields.

### Error
```
Unknown JSON field: "displayTitle"
Available fields:
  conclusion
  createdAt
  databaseId
  event
  headBranch
  headSha
  name
  status
  updatedAt
  url
  workflowDatabaseId
```

### Context
- Command attempted while checking PR/CI status for `Facetomyself/grok2api_sdk`
- Host baseline already notes GitHub CLI is `/usr/bin/gh 2.4.0+dfsg1`
- Newer examples from docs may not be compatible with this packaged version

### Suggested Fix
Prefer `gh run list --json name,...` on this host and avoid assuming newer fields unless verified with local `gh` help/output.

### Metadata
- Reproducible: yes
- Related Files: MEMORY.md

### Resolution
- **Resolved**: 2026-03-13T09:09:30Z
- **Notes**: Re-ran with supported fields only and completed the PR status check.

---
## [ERR-20260313-002] github-pr-sequential-mergeability-shift

**Logged**: 2026-03-13T09:30:00Z
**Priority**: low
**Status**: resolved
**Area**: infra

### Summary
After merging PR #4, PR #3 immediately became non-mergeable, likely due to base branch movement requiring GitHub to recalculate or update the branch.

### Error
```
Message: Pull Request is not mergeable
```

### Context
- Repository: `Facetomyself/grok2api_sdk`
- Intended merge order: #4 -> #3 -> #2
- #4 merged successfully; #3 then failed merge on first retry

### Suggested Fix
After merging dependent/base-changing PRs, re-check PR merge state and update/rebase the next PR branch before retrying merge.

### Metadata
- Reproducible: yes
- Related Files: .learnings/ERRORS.md

### Resolution
- **Resolved**: 2026-03-13T09:30:30Z
- **Notes**: Captured as an operational GitHub CLI/GitHub merge-state learning; follow-up inspection initiated before retrying.

---
## [ERR-20260313-003] git-push-missing-gh-credential-bridge

**Logged**: 2026-03-13T09:33:00Z
**Priority**: medium
**Status**: resolved
**Area**: infra

### Summary
A local clone could authenticate with `gh`, but plain `git push` over HTTPS failed because credential bridging was not configured for git.

### Error
```
fatal: could not read Username for 'https://github.com': No such device or address
```

### Context
- While resolving merge conflicts for PR #3 in `Facetomyself/grok2api_sdk`
- `gh auth status` had previously been OK on this host
- Local manual merge commit succeeded; push failed

### Suggested Fix
Prefer `gh pr update-branch` / `gh`-mediated operations on this host, or explicitly run `gh auth setup-git` before relying on `git push` over HTTPS.

### Metadata
- Reproducible: yes
- Related Files: MEMORY.md, TOOLS.md

### Resolution
- **Resolved**: 2026-03-13T09:33:30Z
- **Notes**: Switched to GitHub CLI-managed branch update path instead of raw git push.

---
## [ERR-20260313-004] old-gh-missing-auth-token-subcommand

**Logged**: 2026-03-13T09:36:00Z
**Priority**: low
**Status**: resolved
**Area**: infra

### Summary
This host's packaged `gh` lacks newer helper subcommands like `gh auth token`, so scripts that assume modern GitHub CLI behavior will fail.

### Error
```
unknown command "token" for "gh auth"
```

### Context
- Host baseline already indicates `/usr/bin/gh 2.4.0+dfsg1`
- Failure occurred while trying to bridge Git auth for pushing a resolved PR branch

### Suggested Fix
On this host, prefer reading the token from `~/.config/gh/hosts.yml` when absolutely necessary, or avoid workflows that depend on newer `gh` features.

### Metadata
- Reproducible: yes
- Related Files: MEMORY.md, .learnings/ERRORS.md

### Resolution
- **Resolved**: 2026-03-13T09:36:30Z
- **Notes**: Switched to reading the stored token from `hosts.yml` for a one-off authenticated push.

---
## [ERR-20260313-005] anticap-host-import-missing-libgl

**Logged**: 2026-03-13T12:37:00Z
**Priority**: medium
**Status**: resolved
**Area**: infra

### Summary
Host-side Python import of `AntiCAP` failed after dependency refresh because OpenCV runtime library `libGL.so.1` is missing on the host, even though the Docker image may still be valid.

### Error
```
ImportError: libGL.so.1: cannot open shared object file: No such file or directory
```

### Context
- Repository: `/root/.openclaw/workspace/tmp/AntiCAP-WebApi-docker`
- Validation step imported `AntiCAP` directly on host Python 3.10
- `AntiCAP` 3.3.5 pulls code paths that require cv2/ultralytics runtime libs
- Dockerfile already installs mesa/gl runtime packages inside the container

---
## [ERR-20260314-001] reverse_kb_research_source_access_fragility

**Logged**: 2026-03-14T01:19:00+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
Hourly reverse-engineering KB research hit external source access failures: Brave search unavailable due to missing key, and some academic/data sites blocked or degraded fetches.

### Error
```
web_search: missing_brave_api_key
web_fetch: 403 Forbidden from Zenodo
web_fetch: ACM/IEEE/NDSS pages partially blocked or poorly extracted
```

### Context
- Task: `research:reverse-expert-kb` hourly collection run
- Search-layer still produced results via exa/tavily/grok
- Failures mainly affected direct source verification and lightweight fetch extraction

### Suggested Fix
For recurring research workflows on this host, prefer search-layer first, treat Brave as optional, and expect selective fallback/manual citation capture for gated academic and dataset-hosting sites.

### Metadata
- Reproducible: yes
- Related Files: research/reverse-expert-kb/runs/2026-03-14-0100.md
- See Also: ERR-20260315-003, ERR-20260315-004

---
## [ERR-20260314-001] git-commit-missing-identity

**Logged**: 2026-03-14T02:19:00+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
Git commit failed in the workspace because user.name and user.email are not configured for this repository/environment.

### Error
```
Author identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.

fatal: unable to auto-detect email address
```

### Context
- Operation attempted: commit research KB updates in /root/.openclaw/workspace
- Command reached commit stage after staging targeted files
- Environment: workspace repo under root on OpenClaw host

### Suggested Fix
Configure git user.name and user.email either locally in the repository or globally for this environment before future commits.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/.git/config

---
## [ERR-20260313-003] search-layer-grok-trailing-json-parse-noise

**Logged**: 2026-03-13T20:18:43Z
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
`search-layer/scripts/search.py` returned usable merged results, but the Grok source emitted a trailing JSON parse error after completion.

### Error
```
[grok] error: Extra data: line 3 column 1 (char 2275)
```

### Context
- Task: hourly `research:reverse-expert-kb` run
- Command mode: deep exploratory search with `--source exa,tavily,grok`
- Outcome: result set was still returned and usable; this appears to be output-cleanliness/error-handling noise rather than a hard failure

### Suggested Fix
Harden Grok response parsing in `search-layer` so partial-success cases do not append confusing parse-noise after a successful merged result.

### Metadata
- Reproducible: unknown
- Related Files: /root/.openclaw/workspace/skills/search-layer/scripts/search.py
- See Also: ERR-20260315-003

---
## [ERR-20260314-001] exec-printf-sh-dash

**Logged**: 2026-03-14T03:16:00Z
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
Used `printf '--- ...'` under `/bin/sh` and hit dash option parsing because the format string began with `--`.

### Error
```sh
/bin/sh: 3: printf: Illegal option --
```

### Context
- Command attempted a simple directory listing prelude.
- Shell is `/bin/sh` on Ubuntu, which is dash here.
- Safer pattern is `printf '%s\n' '--- RUNS ---'` or `echo`.

### Suggested Fix
Avoid bare `printf` format strings starting with hyphens in POSIX sh/dash scripts.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/.learnings/ERRORS.md

---
## [ERR-20260314-001] web_search missing_brave_api_key

**Logged**: 2026-03-14T04:16:00Z
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
Brave-backed `web_search` is unavailable in this environment because the Brave API key is not configured.

### Error
```
missing_brave_api_key
web_search (brave) needs a Brave Search API key. Run `openclaw configure --section web` to store it, or set BRAVE_API_KEY in the Gateway environment.
```

### Context
- Operation attempted: web_search during hourly reverse-expert-kb research cron
- Fallback used: search-layer via local script with Grok source plus direct page fetches
- Impact: research can continue, but Brave multi-source coverage is reduced

### Suggested Fix
Configure Brave Search for the gateway if broader search coverage is desired for future research runs.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/research/reverse-expert-kb/
- See Also: ERR-20260315-004

---
## [ERR-20260314-001] search-and-fetch-sources

**Logged**: 2026-03-14T07:17:58Z
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
Grok-backed search-layer returned usable results but also emitted a JSON parse error; Brave-backed web_search is unavailable on this host due to missing API key; several PDF fetches returned raw PDF bytes rather than extracted text.

### Error
```text
[grok] error: Extra data: line 3 column 1 (char 2844)
web_search: missing_brave_api_key
web_fetch on several PDFs returned raw %PDF bytes instead of readable extracted content
```

### Context
- Operation attempted: literature/source collection for reverse-expert-kb cron workflow
- Tools involved: search-layer/scripts/search.py, web_search, web_fetch
- Environment: headless OpenClaw host; default search-layer policy currently prefers Grok source only unless others are explicitly enabled

### Suggested Fix
- Treat Grok parse-error-with-results as soft failure and continue using returned items
- Prefer landing pages / abstracts over direct PDF fetches when readable extraction matters
- Optionally configure Brave key if broader multi-source coverage is desired on this host

### Metadata
- Reproducible: yes
- Related Files: skills/search-layer/SKILL.md, .learnings/ERRORS.md
- See Also: ERR-20260315-003, ERR-20260315-004

---

## [ERR-20260314-001] web_search_brave_missing_key

**Logged**: 2026-03-14T22:16:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Raw web_search failed because Brave Search API credentials are not configured in this OpenClaw environment

### Error
```
missing_brave_api_key
web_search (brave) needs a Brave Search API key. Run `openclaw configure --section web` to store it, or set BRAVE_API_KEY in the Gateway environment.
```

### Context
- Operation attempted: auxiliary Brave queries during reverse-expert-kb research cron
- Workaround used: continued with search-layer local search.py flow instead of blocking the run
- Impact: direct web_search unavailable; search-layer local path still usable

### Suggested Fix
Configure Brave Search credentials if direct web_search is desired, or remember to prefer search-layer script path in this environment.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/skills/search-layer/SKILL.md
- See Also: ERR-20260315-004

---
## [ERR-20260315-001] web-search-and-fetch-integration

**Logged**: 2026-03-15T02:18:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Brave-backed `web_search` was unavailable due to missing API key, and one public page fetch returned a 403 interstitial during KB source gathering.

### Error
```text
web_search: missing_brave_api_key
web_fetch: Web fetch failed (403) ... Just a moment...
```

### Context
- Operation attempted: external source gathering for reverse-expert-kb Akamai workflow research
- Inputs: Brave searches for Akamai Bot Manager workflow; web fetch of Stack Overflow discussion
- Environment: OpenClaw main session / cron maintenance run

### Suggested Fix
Prefer search-layer fallback sources as done here; keep recording tool gaps in run reports. If broader web search is needed later, configure Brave API key or rely on Grok/Exa/Tavily-backed search-layer paths.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/research/reverse-expert-kb/runs/2026-03-15-0200-akamai-sensor-cookie-workflow.md
- See Also: ERR-20260315-003, ERR-20260315-004

---
## [ERR-20260315-002] web-fetch-chinese-content-interstitials

**Logged**: 2026-03-15T07:19:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
During reverse-expert-kb source gathering, `web_fetch` remained unreliable for some Chinese content platforms (Zhihu 403 interstitial, CSDN 521/empty), even when search-layer and GitHub/open-source sources were usable.

### Error
```text
web_fetch zhihu: Web fetch failed (403)
web_fetch csdn: Web fetch failed (521)
```

### Context
- Operation attempted: source collection for a Xiaohongshu `x-s` / `x-t` / `x-s-common` workflow note
- Inputs: Zhihu/CSDN practitioner posts, GitHub repos, search-layer Grok result cluster
- Workaround used: rely on search-layer result snippets + readable GitHub pages + previously curated KB source notes, then write conservative workflow-centered synthesis instead of brittle internal claims

### Suggested Fix
When collecting practitioner material for Chinese reverse-engineering targets in this environment, expect some article hosts to block or degrade `web_fetch`. Prefer search-layer result clustering plus GitHub/open-source materials first, and treat blog/article hosts as best-effort corroboration rather than required inputs.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/research/reverse-expert-kb/sources/browser-runtime/2026-03-15-xiaohongshu-web-signature-workflow-notes.md
- See Also: ERR-20260315-001, ERR-20260315-003

---
## [ERR-20260315-001] registry-ui-live-debug-container-stopped

**Logged**: 2026-03-15T12:00:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
A live-debug command path for `registry-ui` failed because the target container transitioned to stopped state between earlier inspection and later `docker exec` probes.

### Error
```
cannot exec in a stopped state: unknown
```

### Context
- Operation attempted: deeper in-container probing with `docker exec registry-ui ...`
- Environment: `oracle-docker_proxy` on host `24-7-10-2055`
- Prior state: `registry-ui` had been running earlier and exposed via host port `50000`
- Follow-up evidence: public `ui.zhangxuemin.work` had already been returning `502`, and earlier local probing saw connection reset behavior

### Suggested Fix
Before using `docker exec` in iterative diagnostics, re-check container liveness with `docker ps -a --filter name=<container>` or `docker inspect ... .State.Status`. For unstable services, capture status + logs first, then exec only if still running.

### Metadata
- Reproducible: unknown
- Related Files: infra/hosts/oracle-docker-proxy/projects/registry-ui.md
- See Also: none

---

## [ERR-20260315-001] search-layer-grok

**Logged**: 2026-03-15T09:16:00Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Grok backend in search-layer returned empty/non-JSON output during KB research search, while Tavily still produced usable results.

### Error
```
[grok] error: Expecting value: line 1 column 1 (char 0)
```

### Context
- Command/operation attempted: search-layer search.py deep tutorial query for reCAPTCHA workflow research
- Input or parameters used: --source grok,tavily with three reCAPTCHA-focused queries
- Environment details if relevant: OpenClaw workspace hourly KB maintenance run

### Suggested Fix
Treat Grok as degraded for this run; continue with Tavily/official docs and inspect Grok response handling later if recurrence continues.

### Metadata
- Reproducible: unknown
- Related Files: skills/search-layer/scripts/search.py

---
## [ERR-20260315-WEBFETCH-ANDROID-DOCS] web_fetch

**Logged**: 2026-03-15T10:17:54Z
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
`web_fetch` failed with repeated redirect loops on Android Developers reference pages during KB source collection.

### Error
```
Too many redirects (limit: 3)
```

### Context
- Operation attempted: fetch Android WebView / WebViewClient / WebMessagePort docs for grounding a hybrid WebView practical workflow note
- URLs included `developer.android.com/reference/android/webkit/WebView`, `.../WebViewClient#shouldOverrideUrlLoading(...)`, and `.../WebMessagePort`
- Existing KB source notes plus search-layer results were sufficient to continue conservatively without forcing brittle claims

### Suggested Fix
Prefer search-layer result synthesis and existing curated source notes when Android reference pages trip redirect limits in `web_fetch`; if needed, fall back to browser/manual docs fetch instead of repeated `web_fetch` retries.

### Metadata
- Reproducible: unknown
- Related Files: research/reverse-expert-kb/sources/mobile-runtime-instrumentation/2026-03-15-webview-native-bridge-payload-recovery-notes.md

---
