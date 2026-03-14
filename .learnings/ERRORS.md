# Errors Log

Command failures, exceptions, and unexpected behaviors.

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

---
