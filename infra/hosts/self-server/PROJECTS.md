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
- on 2026-04-04 an aggressive cleanup removed the running `jshookmcp` container, disabled `mihomo` and postfix, removed most MCP/editor/dev-tool directories, later removed the extra SSH listener `5837` plus `rpcbind`, and finally deleted the stale 1Panel-managed MySQL application/data residue under `/opt/1panel/apps/mysql`, leaving the machine much closer to a true 1Panel-only box

## Frozen operating intent after 2026-04-04 cleanup
### `181` / `:44001`
- treat as the retained `1Panel + FRPS` machine
- future additions should be sparse and deliberate
- avoid turning it back into a general experimentation box
- keep the same-day stable outbound helper shape in place:
  - local `dnsmasq` on `127.0.0.1:53`
  - upstream DNS to `106.15.239.221#1053`
  - shell/Docker explicit proxying via `ali-cloud`
- validated after cutover: `docker pull hello-world` and `docker pull coredns/coredns:latest` both succeeded

### `host185` / `:44005`
- updated intent on 2026-04-08: promote this VM from a cleaner `1Panel` rebuild machine into the dedicated `FRPS` relay box for home-lab exposure
- expected long-lived projects on this VM after repurpose:
  - `1Panel`
  - `prompt-optimizer-studio`
  - `FRPS` relay for `home-macmini` and `home-nas`
- future workloads should still be introduced intentionally from a low-noise baseline
- if new projects are added later, document them explicitly rather than letting residue accumulate again
- keep the same-day stable outbound helper shape in place:
  - local `dnsmasq` on `127.0.0.1:53`
  - upstream DNS to `106.15.239.221#1053`
  - shell/Docker explicit proxying via `ali-cloud`
- validated after cutover: `docker pull hello-world` and `docker pull coredns/coredns:latest` both succeeded; the discarded transparent `sing-box-global` experiment should not be treated as an active project
- rollout guidance for the new FRPS role:
  - reserve `30009/tcp` for the `frps` server port
  - reserve `30010/tcp` only if the dashboard is explicitly needed; prefer loopback-only or disabled
  - use `30002-30007/tcp` as the main externally published service pool for `frpc` clients from `home-macmini` / `home-nas`
  - keep `30001/tcp` for `prompt-optimizer-studio` and `30008/tcp` for `1Panel`
  - remove stale firewall exposure related to old `9090` / `30007 -> 9090` forwarding before reusing `30007`

#### Active project added on 2026-04-06: Prompt Optimizer Studio
- deployment path: `/opt/prompt-optimizer-studio`
- runtime shape: Docker Compose local source build on host `host185`
- public port: `30001 -> container 3000`
- storage path: `/opt/prompt-optimizer-studio/data` mounted to `/app/data`
- service/container name shape: `prompt-optimizer-studio-app-1`
- health check: `GET /api/health`
- update path: refresh source tree on a better-connected host if needed, sync to `host185`, then `docker-compose up -d --build`
- operational note: direct GitHub/GHCR shell access from this host was flaky during bootstrap, but Docker base-image pulls and local source-build deployment succeeded through the established explicit-proxy shape
- detailed runbook: `infra/hosts/self-server/projects/prompt-optimizer-studio.md`
