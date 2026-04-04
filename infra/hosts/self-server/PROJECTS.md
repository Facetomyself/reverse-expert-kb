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
- on 2026-04-04 an aggressive cleanup removed the running `jshookmcp` container, disabled `mihomo` and postfix, removed most MCP/editor/dev-tool directories, and later removed the extra SSH listener `5837` plus `rpcbind`, leaving the machine much closer to a true 1Panel-only box

## Suggested cleanup order later
1. confirm which externally reachable ports still matter on each machine
2. map live services to actual business need
3. inspect 1Panel app definitions / compose stacks before removing Docker residue
4. only then decide what to archive, delete, or rebuild from scratch
