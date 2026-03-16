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
