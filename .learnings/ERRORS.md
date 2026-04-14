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

## [ERR-20260413-002] easyai-deploy-aliyun-registry-timeouts

**Logged**: 2026-04-13T12:20:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Deploying `easyai` on `self-server-44005` was blocked by unstable pulls from `registry.cn-shanghai.aliyuncs.com`; repeated Docker image downloads hit `TLS handshake timeout`, and some long-running pull sessions were later cut off by exec-event `SIGKILL`.

### Error
```text
Error response from daemon: Head "https://registry.cn-shanghai.aliyuncs.com/v2/...": net/http: TLS handshake timeout
Process exited with signal SIGKILL.
```

### Context
- Target host: `self-server-44005` (`211.144.221.229:44005`, hostname `host185`).
- Project source upload and port planning succeeded, but image acquisition failed before full stack startup.
- Current Docker daemon on `:44005` already uses the documented `ali-cloud` HTTP/HTTPS proxy.
- Direct `curl` to `https://registry.cn-shanghai.aliyuncs.com/v2/` from `:44005` timed out, while proxied `curl` could at least reach the registry and return `401 Unauthorized`.
- The same registry family also showed handshake instability from the local OpenClaw host, suggesting the failure is not unique to the target VM.
- Long foreground pull sessions are a poor fit for this environment because they can also be interrupted by exec-event process kills, obscuring whether the underlying issue is network or tooling timeout.

### Suggested Fix
- Treat this as registry/network instability first, not a compose/application misconfiguration.
- Prefer shorter, resumable pull steps or a staging path: pull on a more stable host, then `docker save | ssh ... docker load` into `:44005`.
- When possible, use background/detached execution or task/session continuation for long image pulls instead of a single long foreground exec.
- If this registry remains flaky, look for alternate mirrors or preloaded images before retrying full-stack deployment.

### Metadata
- Reproducible: yes
- Related Files: /opt/easyai, infra/hosts/self-server/HOST.md, /root/.openclaw/workspace/.learnings/ERRORS.md
- See Also: ERR-20260319-001

---

## [ERR-20260413-003] wide-grep-output-signal-kill

**Logged**: 2026-04-13T16:55:00+08:00
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
Broad recursive `grep` / `find` scans against large remote or local trees can be terminated by exec-event (`SIGKILL` / `SIGTERM`) before the useful signal is returned.

### Error
```text
Process exited with signal SIGKILL.
Process exited with signal SIGTERM.
```

### Context
- On 2026-04-13, exploratory SSH commands against `ali-cloud` were killed because wide searches over `/opt` matched large 1Panel resource trees and generated far more output than needed.
- The useful signal there was small (`sing-box-gateway.service`, `hysteria-egress.service`, `/opt/sing-box-gateway/config.json`, `/opt/hysteria-egress/client.yaml`), but broad scans pulled bulky unrelated content.
- On 2026-04-14, the same pattern recurred multiple times while reconciling DNS / DKIM history on `oracle-mail`: wide searches through archived `moemail` trees and related local Wrangler/pnpm caches produced excessive output from app/component and bundled dependency content, and multiple exec sessions were terminated before completion.

### Suggested Fix
- For infra/codebase audits, prefer narrow path targets and exact filenames once likely locations are known.
- Exclude bulky trees early (`node_modules`, `.next`, `.git`, large control-panel directories, archived bundles) instead of grepping everything and trimming later.
- Use staged discovery: first identify candidate config files/directories, then read the exact files.
- When only a few hits are needed, cap output early with `head`, `sed -n`, or tighter `rg` patterns.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/.learnings/ERRORS.md, /root/.openclaw/workspace/TOOLS.md
- See Also: ERR-20260413-002

---

## [ERR-20260413-001] nas-frpc-restart-and-pkill-assumptions

**Logged**: 2026-04-13T11:50:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
FRP migration debugging on `home-nas` was prolonged by two wrong operator assumptions: treating the NAS helper script as if it supported `restart`, and using a broad `pkill -f` pattern that could kill the remote launcher path itself.

### Error
```text
usage: /usr/local/etc/rc.d/S99frpc-nas.sh {start|stop}
```

### Context
- During FRP migration from `:44005` to `:44001`, `home-nas` needed to reconnect `frpc` using `/usr/local/etc/frpc-nas.toml`.
- The local helper script `/usr/local/etc/rc.d/S99frpc-nas.sh` only supports `start|stop`; `restart` silently failed the intended recovery path.
- Some remote recovery attempts used `pkill -f "frpc.*frpc-nas.toml"`, which is risky because the current remote shell/launcher command line can also match and get killed, making the session look flaky and the daemon look non-persistent.
- Frontground validation proved the config itself was correct: `frpc` could log in and register both `nas-webui` and `nas-drive` successfully once launched correctly.

### Suggested Fix
- Read small host helper scripts before assuming subcommands like `restart` exist.
- Prefer exact process-name matching (`pkill -x frpc`) or PID-based management over broad `pkill -f` regexes in remote maintenance commands.
- When recovering FRP clients on this NAS, use explicit `stop` then `start`, then confirm listeners appeared on the server side.

### Metadata
- Reproducible: yes
- Related Files: /usr/local/etc/rc.d/S99frpc-nas.sh, /usr/local/etc/frpc-nas.toml, infra/hosts/self-server/projects/frps-relay-plan.md
- See Also: ERR-20260316-001

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

## [ERR-20260410-001] comfyui-ui-vs-api-workflow-format-mismatch

**Logged**: 2026-04-10T14:03:00+08:00
**Priority**: medium
**Status**: pending
**Area**: comfyui

### Summary
A workflow JSON was written in ComfyUI API/prompt-dict format and placed into the `workflows/` directory, but the user expected it to display normally on the ComfyUI canvas UI.

### Error
```text
Workflow file loads abnormally / does not display correctly in the WebUI canvas.
```

### Context
- The generated file used the API prompt structure keyed by node ids like `{"1": {...}, "2": {...}}`.
- ComfyUI canvas/UI workflow files instead use a graph-style structure with top-level keys like `nodes`, `links`, `groups`, `config`, `extra`, and `version`.
- Result: the file was valid as an API prompt, but not appropriate as a normal WebUI workflow artifact inside `~/ai/ComfyUI/workflows`.

### Suggested Fix
- Distinguish clearly between:
  - **API prompt JSON** for queue/API submission
  - **UI workflow JSON** for direct WebUI canvas import/display
- Before writing to `ComfyUI/workflows/`, validate that the JSON is a UI workflow (`nodes` + `links`) unless the goal is explicitly API-only.
- Archive API-format examples outside the main `workflows/` list to avoid confusing WebUI imports.

### Metadata
- Reproducible: yes
- Related Files: workflows/_archived/chenkinrf-wd14-reverse-helper.json

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

## [ERR-20260411-007] macmini-lora-train-stalled-with-stale-pgrep-signal

**Logged**: 2026-04-11T22:33:00+08:00
**Priority**: medium
**Status**: pending
**Area**: training

### Summary
A long-running SDXL LoRA training on `home-macmini` appeared to still exist because an early `pgrep` check returned a bare PID, but the actual training process had already stopped and the log had stalled at step 105/120 for many minutes.

### Error
```text
Log mtime stopped advancing at 2026-04-11 22:17:11 local time.
No new `.safetensors` files appeared after `step00000080`.
A follow-up precise `pgrep -af sdxl_train_network.py` returned no real matching process.
```

### Context
- Command/operation attempted: watchdog-style remote monitoring of `chihaya_anon__nagasaki_soyo_v2_run1` on `home-macmini`
- Initial quick checks combined `pgrep` and `ps`, which can be misleading when probing remotely and when the command wrapper itself influences matching or output interpretation.
- The reliable indicators were instead:
  - log file modification time stopped moving
  - no new checkpoint or final weight appeared
  - exact `pgrep -af` later returned empty
- Training had progressed to about `105/120` with latest logged `avr_loss=0.491`, then stopped before final outputs were written.

### Suggested Fix
For remote training watchdogs, do not treat a single PID-like `pgrep` result as proof the job is healthy. Confirm liveness using at least two of:
- exact `pgrep -af` command line match
- advancing log file mtime
- newly written checkpoint/final output files
- `ps` state/%CPU for the matched PID

If log mtime is stale and outputs stop advancing, treat the run as failed/stalled and restart from the known-good script.

### Metadata
- Reproducible: unknown
- Related Files: /root/.openclaw/workspace/tmp/run_chihaya_soyo_lora_v2.sh, /root/.openclaw/workspace/.learnings/ERRORS.md
- See Also: ERR-20260411-005, ERR-20260411-006

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
## [ERR-20260408-001] reverse-kb-autosync-path-drift

**Logged**: 2026-04-07T19:53:00Z
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
Tried to read a stale guessed iOS XPC topic path during autosync branch selection

### Error
```
ENOENT: no such file or directory, access '/root/.openclaw/workspace-reverse/research/reverse-expert-kb/topics/ios-xpc-service-lifecycle-and-first-consumer-workflow-note.md'
```

### Context
- Operation: read candidate topic page before choosing this run's scope
- The page path was inferred from memory rather than re-listed from the topics directory
- Recovery was immediate: locate the actual path before proceeding

### Suggested Fix
When revisiting candidate pages named in top-level steering text, list matching topic files first instead of guessing the filename.

### Metadata
- Reproducible: yes
- Related Files: research/reverse-expert-kb/index.md

---
## [ERR-20260408-002] ops-assistant-empty-docker-inventory-json

**Logged**: 2026-04-08T15:25:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
`ops-assistant/checks/run_fleet_check.py` crashed while building the fleet summary because `/tmp/ops_docker_inventory.json` was not valid JSON at read time.

### Error
```text
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

### Context
- Command/operation attempted: `python3 ops-assistant/checks/run_fleet_check.py`
- Failure site: `build_summary()` in `ops-assistant/checks/run_fleet_check.py`
- The script unconditionally does `json.loads((TMP_DIR/'ops_docker_inventory.json').read_text())`
- Other generated artifacts from the workflow were readable, but the docker inventory temp artifact appears to have been empty or otherwise non-JSON when the summary stage parsed it
- This prevented the current high-frequency run from refreshing `ops-assistant/state/last-run.json`; the latest recorded successful state remained the earlier one already on disk

### Suggested Fix
- In `run_fleet_check.py`, validate each temp JSON artifact before `json.loads` and surface a clear per-check failure instead of crashing the whole run
- In `docker_inventory.py` / `run_py()`, preserve stderr separately and treat empty stdout as an explicit failed payload contract
- Optionally write temp outputs under `ops-assistant/state/` instead of shared `/tmp` to reduce accidental clobbering between runs

### Metadata
- Reproducible: unknown
- Related Files: /root/.openclaw/workspace/ops-assistant/checks/run_fleet_check.py, /root/.openclaw/workspace/ops-assistant/checks/docker_inventory.py, /root/.openclaw/workspace/.learnings/ERRORS.md
- See Also: ERR-20260407-001

---

## [ERR-20260409-001] home-nas-ssh-timeout-during-hysteria-bootstrap

**Logged**: 2026-04-09T22:57:00+08:00
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
`home-nas` became SSH-timeout-prone while bootstrapping a Hysteria client and polling status through multiple non-interactive SSH exec sessions.

### Error
```\nssh: connect to host 100.73.212.89 port 22: Connection timed out\n```

### Context
- Operation attempted: bootstrap Hysteria client on Synology NAS over SSH, then poll download/log status.
- Environment: DSM 7.2.2 (`home-nas`), OpenClaw exec sessions on current host.
- Several exec/process polls were active while a background curl download on NAS was being started.

### Suggested Fix
Prefer a single idempotent remote bootstrap script that backgrounds locally on NAS and minimizes repeated SSH polling. For flaky tailnet/NAS nodes, avoid stacking many short SSH status probes during long downloads.

### Metadata
- Reproducible: unknown
- Related Files: .learnings/ERRORS.md
- Tags: nas, ssh, tailnet, hysteria, bootstrap

---

## [ERR-20260411-001] smb-mounted-dataset-shape-mismatch

**Logged**: 2026-04-11T17:09:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Role-LoRA筛选时，NAS 上经 SSH 直读统计到角色标签存在，但在 mac mini 的 SMB 挂载视图里首轮筛选结果为 0，不能假设两种读取路径下的数据形态完全一致。

### Error
```
Expected chihaya_anon matches based on NAS-side metadata stats, but SMB-mounted first-pass selector returned total_matches=0.
```

### Context
- NAS direct path: /volume1/homes/zhangxuemin/lyy
- Mac SMB mount path: ~/mnt/home-nas-lyy/zhangxuemin/lyy
- Operation: build first-pass character LoRA candidate subset for chihaya_anon

### Suggested Fix
Before running selection logic on mounted datasets, sample a few metadata files from the mounted path and confirm tag field structure/content matches the direct NAS-side path.

### Metadata
- Reproducible: unknown
- Related Files: .learnings/ERRORS.md

---

## [ERR-20260411-002] pip-macos-torch-timeout

**Logged**: 2026-04-11T18:40:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
On home-macmini, `pip install torch torchvision torchaudio` inside the LoRA training venv timed out while downloading from files.pythonhosted.org using pip default settings.

### Error
```
pip._vendor.urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host=files.pythonhosted.org, port=443): Read timed out.
```

### Context
- Host: home-macmini
- Python: 3.9.6 venv under ~/ai/train/sd-scripts/.venv
- Operation: bootstrap sd-scripts training environment

### Suggested Fix
Retry large wheel installs on macOS with `--default-timeout` and `--retries` instead of assuming a hard failure.

### Metadata
- Reproducible: yes
- Related Files: .learnings/ERRORS.md

---

## [ERR-20260411-003] sd-scripts-python39-incompatible

**Logged**: 2026-04-11T18:46:00+08:00
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
Current sd-scripts checkout on home-macmini is not runnable under Python 3.9 because imported modules use Python 3.10 union type syntax like `str | None`.

### Error
```
TypeError: unsupported operand type(s) for |: type and NoneType
```

### Context
- Host: home-macmini
- Repo: ~/ai/train/sd-scripts @ 308a0cc
- Interpreter: /Library/Developer/CommandLineTools Python 3.9.6
- Failure surfaced before training start in both `sdxl_train_network.py` and `sd3_train_network.py`

### Suggested Fix
Use Python 3.10+ (prefer 3.11 on macOS arm64), recreate the venv, then reinstall training dependencies.

### Metadata
- Reproducible: yes
- Related Files: .learnings/ERRORS.md

---

## [ERR-20260411-004] hf-tokenizer-download-timeout

**Logged**: 2026-04-11T19:02:00+08:00
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
SDXL training startup on home-macmini failed because tokenizer initialization tried to reach huggingface.co and timed out.

### Error
```
requests.exceptions.ConnectionError: HTTPSConnectionPool(host=huggingface.co, port=443): Max retries exceeded ... openai/clip-vit-large-patch14 ...
```

### Context
- Host: home-macmini
- Operation: `sdxl_train_network.py` startup
- Model: ChenkinNoob-XL-v0.2-Rectified-Flow.safetensors
- Existing training env otherwise boots and reaches tokenizer load stage.

### Suggested Fix
Pre-cache required SDXL tokenizers locally or route Hugging Face access via a mirror / `HF_ENDPOINT`, then rerun training with `--tokenizer_cache_dir`.

### Metadata
- Reproducible: yes
- Related Files: .learnings/ERRORS.md

---

## [ERR-20260411-005] sdxl-local-tokenizer-cache-workaround

**Logged**: 2026-04-11T19:34:28+08:00
**Priority**: medium
**Status**: pending
**Area**: comfyui

### Summary
SDXL LoRA training on `home-macmini` was blocked by Hugging Face / hf-mirror tokenizer downloads timing out; training was recovered by providing a local tokenizer cache directory and avoiding network fetch during startup.

### Error
```text
TimeoutError: [Errno 60] Operation timed out
curl: (28) SSL connection timeout
Error while downloading from https://hf-mirror.com/... Read timed out
```

### Context
- `sdxl_train_network.py` attempted to resolve `openai/clip-vit-large-patch14` and `laion/CLIP-ViT-bigG-14-laion2B-39B-b160k` at startup.
- Remote network to `huggingface.co` / `hf-mirror.com` was unreliable.
- Recovery path: create local directories under `~/ai/tokenizers/<model_id with slash replaced by underscore>` and pass `--tokenizer_cache_dir=/Users/mengma/ai/tokenizers`.
- For this setup, the borrowed tokenizer configs also needed `model_max_length=77`; the copied SD1 config defaulted to `8192`, which broke SDXL text encoding reshape.

### Suggested Fix
For unstable-network SDXL training hosts, pre-seed tokenizer cache locally and use `--tokenizer_cache_dir` before first launch. If tokenizers are assembled from fallback files, verify `tokenizer_config.json` fields such as `model_max_length` match SDXL expectations.

### Metadata
- Reproducible: yes
- Related Files: /Users/mengma/ai/train/scripts/run_chihaya_soyo_lora_v1.sh, /root/.openclaw/workspace/.learnings/ERRORS.md
- See Also: ERR-20260411-004

---

## [ERR-20260411-006] apple-silicon-sdxl-mps-first-run-oom-at-1024

**Logged**: 2026-04-11T19:34:28+08:00
**Priority**: medium
**Status**: pending
**Area**: comfyui

### Summary
On the mac mini MPS backend, an SDXL LoRA first run with 1024 resolution and text-encoder training enabled hit MPS memory limits after training began.

### Error
```text
RuntimeError: MPS backend out of memory (MPS allocated: 17.03 GiB, other allocations: 988.03 MiB, max allowed: 18.13 GiB). Tried to allocate 494.00 MiB on private pool.
```

### Context
- Training had already passed tokenizer loading, dataset prep, bucketing, model load, and entered the first optimization steps.
- The first attempt reached `steps: 10%|█| 1/10` before OOM on the next step.
- Stable workaround that completed training: `--network_train_unet_only --cache_latents --resolution=768,768` plus `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0`.

### Suggested Fix
For first-pass SDXL LoRA bring-up on Apple Silicon / MPS, prefer a conservative launch profile: train U-Net only, cache latents, and start at 768 resolution. After artifact generation succeeds, scale parameters back up gradually.

### Metadata
- Reproducible: yes
- Related Files: /Users/mengma/ai/train/scripts/run_chihaya_soyo_lora_v1.sh, /root/.openclaw/workspace/.learnings/ERRORS.md
- See Also: ERR-20260411-005

---
## [ERR-20260412-001] reverse-kb-autosync-search-layer-exec-preflight-and-grok-502

**Logged**: 2026-04-12T04:58:00+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
During reverse-KB autosync, an initial multi-line `python3 search.py ... > artifact` invocation was rejected by OpenClaw exec preflight, and the explicitly requested Grok search source again failed with repeated 502 errors through the configured proxy path.

### Error
```text
exec preflight: complex interpreter invocation detected; refusing to run without script preflight validation. Use a direct `python <file>.py` or `node <file>.js` command.
[grok] error: 502 Server Error: Bad Gateway for url: http://proxy.zhangxuemin.work:8000/v1/chat/completions
```

### Context
- Task: recurring reverse KB autosync external-research pass
- Attempted command shape: multi-line `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py ... > artifact`
- Successful workaround: rerun as a direct one-line `python3 search.py ...` invocation, capture output from the finished process, then write the artifact separately
- Grok failure did not block the run because Exa and Tavily succeeded and the degraded source set was recorded in the run report

### Suggested Fix
For OpenClaw exec, prefer the simplest direct one-line `python3 <script>.py ...` invocation when using `search.py`, then persist artifacts in a separate step. Treat the configured Grok proxy as degraded until 502s stop recurring.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/skills/search-layer/scripts/search.py, /root/.openclaw/workspace/.learnings/ERRORS.md, /root/.openclaw/workspace/research/reverse-expert-kb/runs/2026-04-12-0450-run-report.md
- See Also: ERR-20260411-004

---

## [ERR-20260412-002] comfyui-ui-json-direct-api-submit

**Logged**: 2026-04-12T15:21:31+08:00
**Priority**: medium
**Status**: pending
**Area**: comfyui

### Summary
Tried to convert a ComfyUI canvas/UI workflow JSON directly into an API prompt dict and submit it to `/prompt`, but the generated structure was rejected with HTTP 400.

### Error
```text
urllib.error.HTTPError: HTTP Error 400: Bad Request
```

### Context
- Operation attempted: reuse an existing UI workflow (`chenkinrf-pro-portrait-ui.json`) for automated same-seed baseline-vs-LoRA comparison generation.
- The first pass hand-built an API prompt from `nodes` / `links` / `widgets_values` and posted it to `http://127.0.0.1:8188/prompt`.
- This is brittle because UI workflow shape and API prompt shape are not 1:1; node inputs/order/hidden fields can diverge.

### Suggested Fix
- For automation, prefer a minimal native API prompt graph built explicitly from `object_info`, or use an existing known-good API example/script.
- Do not assume a canvas workflow can be mechanically transformed into a valid API payload without validating node schemas and exact input wiring.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/workspace/.learnings/ERRORS.md
- See Also: ERR-20260410-001

---
## [ERR-20260412-001] docker compose unavailable on self-server-44005

**Logged**: 2026-04-12T21:26:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Tried to use `docker compose` on `self-server-44005`, but the host only supports legacy `docker-compose`.

### Error
```
docker: unknown command: docker compose

Run `docker --help` for more information
```

### Context
- Operation: deploy NapCat alongside AstrBot on CentOS 7 host `self-server-44005`
- Initial assumption used modern Docker Compose v2 subcommand
- Host runtime is older 1Panel/CentOS-era Docker tooling

### Suggested Fix
Prefer detecting or defaulting to `docker-compose` on older CentOS/1Panel hosts unless `docker compose version` succeeds.

### Metadata
- Reproducible: yes
- Related Files: TOOLS.md, infra/hosts/self-server/projects/astrbot.md

---
## [ERR-20260413-001] local-exec-default-shell-pipefail

**Logged**: 2026-04-13T03:14:00+08:00
**Priority**: low
**Status**: pending
**Area**: config

### Summary
A local diagnostic exec failed immediately because the default tool shell here is `/bin/sh`, so plain `set -o pipefail` is invalid unless the command explicitly invokes Bash.

### Error
```text
/bin/sh: 1: set: Illegal option -o pipefail
```

### Context
- Operation: run a read-only fleet snapshot helper command from `exec`
- Initial command assumed Bash semantics directly in the `command` field
- This OpenClaw host advertises `shell=sh`, so Bash-only flags need `bash -lc '...'`

### Suggested Fix
When a command needs `pipefail`, arrays, or more complex quoting, wrap it with `bash -lc` instead of assuming the default exec shell is Bash.

### Metadata
- Reproducible: yes
- Related Files: TOOLS.md, /root/.openclaw/workspace/.learnings/ERRORS.md

---

## [ERR-20260413-003] remote-mihomo-validation-long-chain-instability

**Logged**: 2026-04-13T15:34:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Real domestic-host Clash subscription validation was obscured by long chained remote exec workflows; SSH/SCP transfer and bundled one-shot commands failed before `mihomo -t` could return a parser verdict.

### Error
```text
Observed failures included signal SIGKILL during long-running remote download/transfer and SSH/SCP exit code 255 during bundled transfer + fetch + parse flows.
```

### Context
- Goal: validate `clash-meta.yaml` / `clash-compat.yaml` on an actual domestic machine instead of guessing from local parsing.
- Attempts on `ali-cloud` and `self-server` bundled several steps together: fetch/download mihomo binary, copy to remote, fetch subscriptions, then run `mihomo -t`.
- Result: transport/process instability produced misleading failures unrelated to the YAML itself.
- Confirmed separately: the domestic machine `self-server(:44001)` could fetch both subscription URLs successfully with HTTP 200, so reachability/cert/content serving was not the immediate issue.

### Suggested Fix
- Use short, falsifiable steps for remote validation:
  1. verify subscription fetch independently
  2. verify parser binary presence independently
  3. run parser-only validation as its own short command
- Avoid bundling binary transfer + subscription fetch + parser execution into one long SSH command.
- When possible, prefer a host that already has an appropriate parser installed.

### Metadata
- Reproducible: yes
- Related Files: infra/hosts/hk-relay/clash-meta.yaml, infra/hosts/hk-relay/clash-compat.yaml, .ssh/config
- See Also: ERR-20260413-002

---

## [ERR-20260413-001] nested-ssh-python-heredoc-quoting

**Logged**: 2026-04-13T22:52:00+08:00
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
A nested ssh + python heredoc probe failed because /bin/sh quoting broke before the remote Python block executed.

### Error
```
/bin/sh: 5: Syntax error: (" unexpected
```

### Context
- Attempted a one-off file-stat probe against home-macmini through ali-cloud transit.
- Used bash -lc locally, then nested ssh commands, then embedded Python with a heredoc.
- The shell stack was too quote-fragile for this pattern.

### Suggested Fix
Prefer simpler remote primitives for this path, such as remote stat/ls commands, or upload/run a tiny temporary script instead of nesting a Python heredoc through multiple ssh layers.

### Metadata
- Reproducible: yes
- Related Files: .learnings/ERRORS.md
- See Also: none

---
## [ERR-20260413-001] nested-ssh-quoting-home-macmini-probe

**Logged**: 2026-04-13T22:53:00+08:00
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
A nested ssh probe against home-macmini failed because multi-layer shell quoting broke before the remote stat/python command executed.

### Error
```
/bin/sh: 5: Syntax error: (" unexpected
bash: -c: line 1: unexpected EOF while looking for matching `"
## [ERR-20260414-001] easyai-background-orchestrator-timeout

**Logged**: 2026-04-14T18:30:00+08:00
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
A recurring cron orchestrator for EasyAI image import kept running into network-transfer stalls and then hit its per-run 900s timeout instead of cleanly stopping itself after reaching a clearly blocked state.

### Error
```text
cron: job execution timed out
```

### Context
- Job: `easyai-background-orchestrator` (`06e218c1-ab98-42da-8cab-4644672a5f03`)
- Intended behavior: serially move missing EasyAI images from `ali-cloud` to `self-server-44005`, clean `ali-cloud` cache after each success, and disable itself on clear long-term blockage.
- Observed behavior:
  - repeated intermittent SSH failures between controller / `ali-cloud` / `self-server-44005`
  - temporary HTTP staging on `ali-cloud:18083` was not reliably re-established
  - the run kept retrying inside one cron turn until the 900s limit expired
  - subsequent scheduled runs re-fired even after the workflow had already concluded it was in a long-term blocked state
- Last useful state during diagnosis:
  - `agent-governance` had already been imported successfully
  - `dozzle.tar` was produced on `ali-cloud`, and `dozzle` eventually showed as loaded on `self-server-44005`
  - remaining missing images were reduced, but the cron design was still wrong for the link quality

### Suggested Fix
For long-running remote import workflows on unstable links, do not use one broad recurring cron turn that performs multi-step orchestration and retries until timeout. Prefer a smaller watchdog/job design, for example:
1. one image or one sub-step per run,
2. explicit stop/disable as soon as a long-term block is detected,
3. short re-check cron or detached task for transfer follow-up instead of a 900s retry loop.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/cron/jobs.json, /root/.openclaw/cron/runs/06e218c1-ab98-42da-8cab-4644672a5f03.jsonl, /root/.openclaw/workspace/.learnings/ERRORS.md
- See Also: none

---
