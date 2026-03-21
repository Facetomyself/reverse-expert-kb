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
