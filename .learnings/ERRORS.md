## [ERR-20260316-001] remote-heredoc-config-patching

**Logged**: 2026-03-16T17:22:47+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Remote config patching on `oracle-proxy:/root/ExaFree` failed due to brittle inline Python/heredoc quoting and an unavailable YAML dependency.

### Error
```text
ModuleNotFoundError: No module named 'ruamel'
SyntaxError: invalid syntax
```

### Context
- Attempted to patch `.env`, `docker-compose.yml`, and `data/settings.yaml` over SSH using inline Python.
- First approach depended on `ruamel.yaml`, which is not installed on the remote host.
- Second approach still had quoting/substitution issues inside the inline script, so compose env substitution did not update as intended.

### Suggested Fix
- Prefer simple `sed`/explicit file rewrite for small remote config changes.
- Do not depend on non-default Python packages on remote hosts unless pre-verified.
- Avoid complex nested quoting in one-shot SSH heredoc commands when editing YAML/compose env lines.
- For multi-line remote script installation, base64 + remote Python file write is more reliable than nested shell/heredoc quoting on heterogeneous `/bin/sh` environments.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/.learnings/ERRORS.md
- See Also: none

---

## [ERR-20260316-001] git-status-cached-old-cli

**Logged**: 2026-03-16T17:30:00+08:00
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
Used `git status --cached` on this host; the local Git CLI does not support that option.

### Error
```
error: unknown option `cached'
```

### Context
- Command/operation attempted: `git -C /root/.openclaw/workspace status --short --cached`
- Environment detail: older Git tooling on host; use `git diff --cached --name-only` or plain `git status --short` after staging instead.

### Suggested Fix
For staged-file inspection on this host, avoid `git status --cached`; prefer `git diff --cached --name-only`.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/TOOLS.md

---

## [ERR-20260317-001] search_layer_tavily_proxy_401

**Logged**: 2026-03-17T15:45:00+08:00
**Area**: research
**Severity**: medium

### What happened
A reverse-KB multi-source search smoke test forced `--source exa,tavily,grok` through the local `search-layer` script. The run succeeded partially, but Tavily failed with `401 Unauthorized` against `http://proxy.zhangxuemin.work:9874/api/search` while Exa and Grok both returned results.

### Impact
Reverse-KB autosync can now be forced into explicit multi-source mode with audit logging, but current real behavior is degraded to `exa + grok` until the Tavily proxy/auth configuration is fixed. Without audit, this would be easy to misread as generic “multi-source search”.

### Evidence
- `scripts/reverse-kb-search-audit.py`
- `/tmp/reverse-kb-search-audit-smoke.json`
- stderr: `[tavily] error: 401 Client Error: Unauthorized for url: http://proxy.zhangxuemin.work:9874/api/search`

### Mitigation
- Keep explicit source auditing in reverse-KB runs.
- Treat Grok-only or Exa+Grok execution as degraded mode, not normal mode.
- Fix Tavily proxy credentials/config before claiming full three-source execution.

---

## [ERR-20260319-001] ali-cloud docker compose invocation mismatch

**Logged**: 2026-03-19T08:40:00Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Attempted to use `docker compose -f` on `ali-cloud`, but the host only has legacy `docker-compose`, not the Compose v2 plugin.

### Error
```
unknown shorthand flag: 'f' in -f
See 'docker --help'.
```

### Context
- Command/operation attempted: start a temporary Camoufox replacement stack on `ali-cloud`
- Environment details: remote host `ali-cloud` has `/usr/bin/docker-compose` but not `docker compose`
- Follow-up complication: shortly after the failed attempt, SSH to `ali-cloud` began timing out during banner exchange, interrupting the replacement workflow.

### Suggested Fix
Before remote Docker orchestration on older hosts, explicitly detect whether the target supports `docker compose` or only `docker-compose`, and branch commands accordingly.

### Metadata
- Reproducible: yes
- Related Files: TOOLS.md, infra/hosts/ali-cloud/PROJECTS.md

---

## [ERR-20260407-001] ssh-batch-inline-quoting-breakage

**Logged**: 2026-04-07T15:57:00+08:00
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
A first-pass batch SSH health-check command for the Oracle fleet failed because nested inline shell quoting broke command substitution on the remote side.

### Error
```text
bash: -c: line 3: unexpected EOF while looking for matching `)'
```

### Context
- Command/operation attempted: one-shot multi-host SSH inspection with several nested `$(...)`, `awk`, and quoted format strings.
- Impact: the first batch returned partial hostnames but failed before resource/listener sampling.
- Recovery: reran the inspection with simpler `printf`/`df --output`/`sed -n` forms and completed the read-only fleet check successfully.

### Suggested Fix
For recurring SSH fleet checks, avoid dense nested quoting in single-quoted remote one-liners. Prefer simpler field extraction primitives or a small uploaded script when the command shape grows.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/.learnings/ERRORS.md
- See Also: ERR-20260316-001

---

## [ERR-20260406-001] remote-docker-compose-assumption-on-centos7

**Logged**: 2026-04-06T16:35:00+08:00
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
A remote deployment precheck on `self-server-44005` initially assumed Compose v2 syntax (`docker compose`), but the host only provides legacy `docker-compose`.

### Error
```text
docker: unknown command: docker compose
```

### Context
- Command/operation attempted: remote precheck for deploying `prompt-optimizer-studio`
- Environment details: `self-server-44005` is CentOS 7 with Docker 28.1.1 and legacy `/usr/bin/docker-compose`
- This also makes quick probes like `docker compose version` misleading on older domestic hosts.

### Suggested Fix
Before remote Docker orchestration, explicitly detect whether the target supports `docker compose` or only `docker-compose`, and branch commands accordingly. For old CentOS-style hosts, prefer `docker-compose` by default unless verified otherwise.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/.learnings/ERRORS.md, /root/.openclaw/workspace/TOOLS.md
- See Also: ERR-20260319-001

---

## [ERR-20260406-002] domestic-host-git-github-reset-by-peer

**Logged**: 2026-04-06T16:40:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Direct `git clone https://github.com/...` from `self-server-44005` failed with `Send failure: Connection reset by peer` even though Docker image pulls from Docker Hub succeeded through the host's configured proxy path.

### Error
```text
fatal: unable to access 'https://github.com/XBigRoad/prompt-optimizer-studio.git/': Send failure: Connection reset by peer
```

### Context
- Command/operation attempted: bootstrap remote source checkout for deploying `prompt-optimizer-studio`
- Environment details: domestic CentOS 7 host with Docker daemon proxying through `ali-cloud`, but shell/git HTTPS path to GitHub remained unreliable
- Operational implication: remote source-based deployments should not assume GitHub clone works just because Docker pulls work.

### Suggested Fix
For domestic hosts with mixed proxy paths, prefer one of:
- fetch source on a better-connected host and copy it over
- configure git/curl proxying explicitly for the shell path
- or deploy from a prebuilt image/tarball instead of remote `git clone`

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/.learnings/ERRORS.md
- See Also: ERR-20260406-001

---

## [ERR-20260408-001] workspace-memory-gitignore-blocked-routine-commit

**Logged**: 2026-04-08T03:04:00+08:00
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
A routine commit for a new daily memory note initially failed because the workspace `.gitignore` excludes the entire `memory/` directory.

### Error
```text
The following paths are ignored by one of your .gitignore files:
memory
hint: Use -f if you really want to add them.
```

### Context
- Command/operation attempted: `git add memory/2026-04-08.md && git commit -m "docs(memory): log nightly promotion check"`
- Environment details: workspace root `.gitignore` contains `memory/`
- Impact: routine memory logging cannot be committed with a normal `git add`; must use `git add -f` when a memory file should be versioned deliberately.

### Suggested Fix
When committing selected daily memory notes in this workspace, force-stage them explicitly with `git add -f <path>` instead of assuming the directory is tracked.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/.gitignore, /root/.openclaw/workspace/.learnings/ERRORS.md
- See Also: none

---

## [ERR-20260406-003] remote-inline-python-quoting-compose-edit

**Logged**: 2026-04-06T22:13:00+08:00
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
A remote one-shot Python edit used through SSH failed because nested shell quoting mangled the intended multi-line replacement string while patching `docker-compose.yml`.

### Error
```text
SyntaxError: invalid syntax
```

### Context
- Command/operation attempted: remove the extra `3000` public port from `self-server-44005` by patching remote compose files inline
- Environment details: nested SSH + shell + Python quoting on a heterogeneous remote shell path
- The deployment itself was healthy; only the config-patching helper failed.

### Suggested Fix
For small remote compose changes, prefer explicit file rewrite with `cat > file <<"EOF"` or simple `sed`, rather than nested inline Python string replacement over SSH.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/.learnings/ERRORS.md
- See Also: ERR-20260316-001

---

## [ERR-20260406-004] workspace-write-followed-by-missing-path

**Logged**: 2026-04-06T22:16:00+08:00
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
A file written under the nested `infra/` tree was reported as successfully created, but an immediate follow-up `chmod` using the same absolute path failed with `No such file or directory`, indicating path/layout drift between the workspace view and shell view.

### Error
```text
chmod: cannot access '/root/.openclaw/workspace/infra/bin/check-prompt-optimizer-self-server.sh': No such file or directory
```

### Context
- Command/operation attempted: create an infra health-check helper script and mark it executable
- Environment detail: `infra/` is a separate git repo with some path/layout oddities in this workspace

### Suggested Fix
Always verify the actual shell-visible path with `find`/`ls` after creating new files inside nested repo areas before assuming follow-up shell operations will hit the same location.

### Metadata
- Reproducible: unknown
- Related Files: /root/.openclaw/workspace/.learnings/ERRORS.md
- See Also: none

---

## [ERR-20260320-001] sh-pipefail-incompatible

**Logged**: 2026-03-20T13:57:00+08:00
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
Tried to use `set -o pipefail` in an `exec` shell command, but the OpenClaw `exec` default shell on this host is `/bin/sh`, which does not support that option.

### Error
```text
/bin/sh: 1: set: Illegal option -o pipefail
```

### Context
- Command/operation attempted: run the ops-assistant cron workflow while preserving stdout/stderr to files.
- Environment details: `exec` uses `sh` here unless explicitly invoking `bash -lc ...`.
- The run was immediately retried with POSIX-compatible shell logic and then completed successfully.

### Suggested Fix
For future `exec` calls on this host, avoid Bash-specific shell options unless explicitly wrapping the command in `bash -lc`.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/.learnings/ERRORS.md

---
## [ERR-20260321-001] remote-inline-python-quoting

**Logged**: 2026-03-21T11:33:00Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
A remote inline Python replacement command failed due to malformed quoting while editing `config.defaults.toml` over SSH.

### Error
```text
File "<stdin>", line 5
    text = text.replace(api_key = Zxm971004, api_key = )
                                                       ^
SyntaxError: invalid syntax
```

### Context
- Operation attempted: sanitize hardcoded default keys in `/root/grok2api/config.defaults.toml` on `oracle-proxy`
- Method used: `ssh ... python3 - <<"PY" ...`
- Cause: replacement expression lost the intended string quoting in the inline script

### Suggested Fix
When patching remote files via SSH, prefer single-quoted here-doc payloads with fully literal Python strings, or use `sed -i` only for trivial replacements after verifying exact matches.

### Metadata
- Reproducible: yes
- Related Files: /root/grok2api/config.defaults.toml

---
## [ERR-20260321-2116] search-layer-cli-json-flag

**Logged**: 2026-03-21T13:16:00Z
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
Assumed local `skills/search-layer/scripts/search.py` supported `--json`, but this host copy does not.

### Error
```
search.py: error: unrecognized arguments: --json
```

### Context
- Command attempted during reverse KB autosync external research run
- Tool: `/root/.openclaw/workspace/skills/search-layer/scripts/search.py`
- Fallback worked by capturing stdout with `tee`

### Suggested Fix
Document the actual supported flags in the skill or add structured output support if needed.

### Metadata
- Reproducible: yes
- Related Files: skills/search-layer/SKILL.md

---
## [ERR-20260323-001] git-commit-identity-missing

**Logged**: 2026-03-23T06:33:00Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Temporary git worktree commit failed because local git user.name/user.email were not configured on this OpenClaw host.

### Error
```
Author identity unknown
fatal: unable to auto-detect email address (got 'root@instance-20250911-1634.(none)')
```

### Context
- Operation attempted: create and commit a new safe-sync branch for the user's fork of grok2api
- Environment: local OpenClaw host, ephemeral clone under /tmp
- GitHub auth via gh was available, but git commit identity was unset

### Suggested Fix
Set repository-local git identity for temporary worktrees used for automated fork-sync commits. Avoid relying on global git identity being present.

### Metadata
- Reproducible: yes
- Related Files: .learnings/ERRORS.md

---
## [ERR-20260324-001] docker-compose-recreate-name-conflict

**Logged**: 2026-03-24T02:21:26.406040+00:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
`docker compose up -d --build grok2api` failed on oracle-proxy because an existing manually-managed `grok2api` container already occupied the fixed container name.

### Error
```
Error response from daemon: Conflict. The container name "/grok2api" is already in use ...
```

### Context
- Operation attempted: rebuild/redeploy `/root/grok2api`
- Host: `oracle-proxy`
- Compose file pins `container_name: grok2api`
- Existing runtime was image-based (`grok2api-official-local:latest`), not direct compose build mode

### Suggested Fix
Before redeploying this service, inspect `docker-compose.yml` + current container/image topology. For this project, rebuild the local image tag first, then `docker rm -f grok2api` and recreate via compose, instead of assuming `compose up --build` can replace the existing named container cleanly.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/TOOLS.md

---
## [ERR-20260326-INFRA-PUSH-RACE] infra_git_sync

**Logged**: 2026-03-26T00:35:00Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
`infra/bin/sync-infra.sh` push was rejected because remote `main` advanced unexpectedly before push.

### Error
```
To https://github.com/Facetomyself/openclaw-infra.git
 ! [remote rejected] main -> main (cannot lock ref refs/heads/main: is at de32e453a273b8990e6b899536569637c5591666 but expected bfb499abbe872230d1d69d1ee8ad27503caa7d0b)
error: failed to push some refs to https://github.com/Facetomyself/openclaw-infra.git
```

### Context
- Local commit succeeded in `/root/.openclaw/workspace/infra`
- Failure happened during the sync step
- Safe recovery path is `git fetch` + inspect + `git pull --rebase` (or explicit rebase) + push

### Suggested Fix
Harden infra sync workflow so remote-fast-forward races are handled explicitly and reported as sync-pending rather than silently implying completion.

### Metadata
- Reproducible: unknown
- Related Files: /root/.openclaw/workspace/infra/.git
- See Also: none

---
## [ERR-20260326-001] cf_refresh browser label breaks reverse impersonation

**Logged**: 2026-03-26T13:02:00+08:00
**Priority**: high
**Status**: pending
**Area**: backend

### Summary
`cf_refresh.refresh_once()` wrote solver-reported `browser=camoufoxcustom` into runtime config, but `curl_cffi` does not support impersonating that label, causing reverse requests to fail locally before reaching upstream.

### Error
```
curl_cffi.requests.exceptions.ImpersonateError: Impersonating camoufoxcustom is not supported
```

### Context
- Operation: refresh solver-derived Cloudflare clearance and then reuse it in reverse requests
- Project: `/root/grok2api`
- Affected path: `app/services/cf_refresh/scheduler.py` writing `proxy.browser` directly from solver output
- Solver could successfully return `cf_clearance/cookies/user_agent/browser`, and `refresh_once()` successfully updated config, but subsequent reverse requests crashed because `proxy.browser` became `camoufoxcustom`.

### Suggested Fix
Do not overwrite runtime `proxy.browser` with solver-local labels unsupported by `curl_cffi` (e.g. `camoufoxcustom`). Keep writing `cf_clearance/cf_cookies`; only write browser when it is a known supported impersonation profile or map it explicitly.

### Metadata
- Reproducible: yes
- Related Files: app/services/cf_refresh/scheduler.py, app/services/reverse/utils/session.py

---

## [ERR-20260327-001] sh-vs-bash-pipefail

**Logged**: 2026-03-27T02:32:47.903181+00:00
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
Local exec command failed because the default shell is `sh`, but the script assumed bash-only `set -o pipefail` support.

### Error
```
/bin/sh: 1: set: Illegal option -o pipefail
```

### Context
- Operation: build a Linux-localized Codex config bundle from uploaded files
- Cause: used bash-specific shell options without invoking `bash -lc` explicitly

### Suggested Fix
When a command relies on bash features in this workspace, wrap it with `bash -lc` instead of assuming `/bin/sh` compatibility.

### Metadata
- Reproducible: yes
- Related Files: .learnings/ERRORS.md

---

## [ERR-20260327-002] oracle-new2-mcp-bootstrap

**Logged**: 2026-03-27T02:58:18.848957+00:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Bulk MCP bootstrap on oracle-new2 failed after DrissionPageMCP dependency install, likely during Chromium debug-profile startup or subsequent MCP registration steps.

### Error
```
Composite remote bootstrap command exited with code 1 after uv sync completed.
```

### Context
- Host: oracle-new2
- Completed: uv install, DrissionPageMCP_rebuild uv sync
- Pending/failing area: browser debug endpoints / codex mcp add chain

### Suggested Fix
Break the bootstrap into smaller remote checks: verify each debug port starter individually, then add MCP servers one by one.

### Metadata
- Reproducible: unknown
- Related Files: .learnings/ERRORS.md

---

## [ERR-20260404-001] exec-shell-pipefail

**Logged**: 2026-04-04T14:44:00+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
A shell command failed immediately because /bin/sh on this host does not support `set -o pipefail`.

### Error
```
/bin/sh: 1: set: Illegal option -o pipefail
```

### Context
- Command/operation attempted: previously approved async exec command
- Environment details: OpenClaw exec used `/bin/sh`, not bash
- Impact: command did not run past shell option setup

### Suggested Fix
When `pipefail` is needed here, run the script via `bash -lc \"...\"` or remove `pipefail` if POSIX `sh` compatibility is required.

### Metadata
- Reproducible: yes
- Related Files: .learnings/ERRORS.md

---

## [ERR-20260404-002] infra_sync_push_race_false_alarm

**Logged**: 2026-04-04T07:57:57Z
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
`infra/bin/sync-infra.sh` reported a non-fast-forward push rejection during an `infra` sync, but an immediate fetch showed `origin/main` had already advanced to the same local commit, so the failure signal was transient/misleading rather than a real unsynced divergence.

### Error
```text
To https://github.com/Facetomyself/openclaw-infra.git
 ! [remote rejected] main -> main (cannot lock ref 'refs/heads/main': is at db6b2189dae69ade7e652b8cc8ff1e6bbb8aa57e but expected 851f996d70e09312fec1220447ca7c4e7a361e04)
error: failed to push some refs to 'https://github.com/Facetomyself/openclaw-infra.git'
```

### Context
- Operation attempted: recurring Oracle fleet maintenance run committed small `infra/` doc updates and then ran `./bin/sync-infra.sh`
- Immediate follow-up `git fetch origin` showed `HEAD` and `origin/main` both at `db6b2189dae69ade7e652b8cc8ff1e6bbb8aa57e`
- This means the sync path can emit a scary remote-rejected message during a ref-update race even when the target commit is already present remotely by the time of inspection

### Suggested Fix
After any `sync-infra.sh` push rejection, automatically run `git fetch origin` and compare `HEAD` vs `origin/main` before treating it as a real sync failure. If they already match, report the push rejection as a transient race/false alarm instead of an outstanding sync problem.

### Metadata
- Reproducible: unknown
- Related Files: /root/.openclaw/workspace/infra/bin/sync-infra.sh, /root/.openclaw/workspace/.learnings/ERRORS.md
- See Also: ERR-20260326-INFRA-PUSH-RACE

---

## [ERR-20260404-001] oracle-registry compose patch quoting failure

**Logged**: 2026-04-04T16:38:30+08:00
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
A Python inline patch command failed because multiline YAML text was embedded with broken shell quoting.

### Error
```
SyntaxError: invalid decimal literal
```

### Context
- Target: `oracle-registry:/opt/registry-proxy/docker-compose.yml`
- Intended change: switch only `reg-docker-hub` to its own storage directory
- Failure cause: unsafe shell quoting around multiline Python string literals inside SSH command

### Suggested Fix
Use line-oriented sed/awk edits or write a temporary script/heredoc with stable quoting instead of embedding multiline YAML blocks directly in a Python one-liner over SSH.

### Metadata
- Reproducible: yes
- Related Files: infra/hosts/oracle-registry/PROJECTS.md
- See Also: none

---

## [ERR-20260404-002] exact-replacement-drift-in-doc-edit

**Logged**: 2026-04-04T16:54:40+08:00
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
An exact-text file edit failed because the target block in `infra/hosts/ali-cloud/HOST.md` had drifted from the previously read snapshot.

### Error
```
Could not find the exact text ... The old text must match exactly including all whitespace and newlines.
```

### Context
- Operation: `edit` tool exact replacement
- Target file: `infra/hosts/ali-cloud/HOST.md`
- Cause: attempted to replace a larger block by stale exact text instead of re-reading and appending/patching a smaller unique anchor

### Suggested Fix
When editing docs that may have changed recently, re-read the file and patch against a short unique anchor or append a new bullet instead of replacing a long previously-copied block.

### Metadata
- Reproducible: yes
- Related Files: infra/hosts/ali-cloud/HOST.md, .learnings/ERRORS.md
- See Also: ERR-20260316-001

---
## [ERR-20260407-001] reverse-kb-autosync source-artifact-path-and-fetch-degradation

**Logged**: 2026-04-07T08:24:17+00:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
Autosync research run used a wrong subtree path for one saved search artifact, and two fetch URLs degraded/redirected during source collection.

### Error
```
/bin/sh: 1: cannot create /root/.openclaw/workspace-reverse/research/reverse-expert-kb/sources/mobile-and-protected-runtime/2026-04-07-1621-topology-selection-search-layer.txt: Directory nonexistent
web_fetch 404 / redirect failures on docs.ebpf.io and source.android.com path used in this run
```

### Context
- Operation: recurring reverse-kb-autosync external-research run
- Intended artifact path should match an existing KB source subtree before redirecting output there
- Continued conservatively with available search results plus usable seccomp docs instead of failing the run

### Suggested Fix
- Prefer creating/checking the target sources subtree before redirecting search output
- Reuse known existing source subtrees consistently for mobile/protected-runtime runs
- Treat docs.ebpf.io/source.android fetches as opportunistic and not required for run success unless they are the only anchor

### Metadata
- Reproducible: yes
- Related Files: research/reverse-expert-kb/sources/
- See Also: none

---
