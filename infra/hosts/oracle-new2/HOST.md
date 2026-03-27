# oracle-new2 / HOST

## Identity
- Name: `oracle-new2`
- Provider: Oracle Cloud Infrastructure
- Public IP: `140.245.61.236`
- SSH alias: `oracle-new2`
- Default SSH user: `ubuntu`
- Created: 2026-03-25

## Access
- OpenClaw-side SSH key path: `~/.ssh/oracle-new1.pem`
- Current SSH verification: success on 2026-03-25
- Hostname observed: `instance-20260325-1818`
- Tailnet IPv4: `100.79.183.3` (joined 2026-03-25)
- Tailscale-visible name is still the generic instance hostname; this machine has not yet been semantically renamed the way `oracle-registry` has

## System baseline
- OS: Ubuntu 24.04.4 LTS
- Kernel: `6.17.0-1007-oracle`
- Arch: `aarch64`
- Resources observed on 2026-03-25:
  - CPU: 2 vCPU
  - RAM: ~11 GiB
  - root disk: 100G (`/` had ~94G free at first check)
- Installed baseline packages on 2026-03-25:
  - common ops tooling (`curl`, `wget`, `git`, `jq`, `tmux`, `htop`, `tree`, `rsync`, `ripgrep`, `dnsutils`, etc.)
  - build/runtime basics (`build-essential`, `python3`, `python3-pip`, `python3-venv`, `pipx`)
  - Docker stack (`docker.io`, `docker-compose-v2`)
- Additional runtime installed on 2026-03-27 for JS reverse MCP validation:
  - Node.js `v22.22.0` (NodeSource)
  - npm `10.9.4`
  - Chromium snap `146.0.7680.80` at `/snap/bin/chromium`
- Swap:
  - `/swapfile` enabled at 2G and persisted in `/etc/fstab`
- Docker:
  - daemon enabled and started
  - `hello-world` run succeeded during validation
- User notes:
  - `ubuntu` has sudo access
  - `docker` group membership is already present for `ubuntu`

## Notes
- This host was initially unreachable because OCI networking was incomplete (missing effective IPv4 ingress / internet path). SSH became reachable after the user added IPv4 ingress and internet gateway routing.
- Uses the same provided private key material currently stored locally as `~/.ssh/oracle-new1.pem`.
- `fwupd-refresh.service` showed as failed during first baseline check; not currently treated as a blocker for server use.
- Suitable as a lightweight ARM Docker worker / utility host; left otherwise mostly idle after base provisioning.
- `js-reverse-mcp` has now been validated here in a minimal headless deployment shape using Chromium rather than official Google Chrome Stable.
- Current validated launcher shape for that project is:
  - `node build/src/index.js --headless --executablePath=/snap/bin/chromium --chrome-arg=--no-sandbox --chrome-arg=--disable-dev-shm-usage`
- Convenience wrappers were created on-host:
  - `~/bin/js-reverse-mcp-run`
  - `~/bin/js-reverse-mcp-smoke`
- Deployment notes for that project live at `~/js-reverse-mcp/.deploy/README.md` on the remote host.
- Codex on this host was later localized into a Linux-first `~/.codex` layout and trimmed to a smaller active MCP set rather than carrying over the full Windows-oriented setup.
- Current enabled Codex MCP servers on this host are:
  - `DrissionPageMCP` → `uv --directory /home/ubuntu/DrissionPageMCP_rebuild run main.py`
  - `Playwright` → `npx -y @playwright/mcp@latest --cdp-endpoint http://127.0.0.1:9224`
  - `context7` → `npx -y @upstash/context7-mcp --api-key ...`
  - `js-reverse` → `~/bin/js-reverse-mcp-run --browserUrl http://127.0.0.1:9222`
  - `shrimp-task-manager` → `npx -y mcp-shrimp-task-manager`
- To support those MCPs on a headless server, reusable Chromium remote-debug wrappers were added on-host:
  - `~/.local/bin/start-chromium-9222`
  - `~/.local/bin/start-chromium-9223`
  - `~/.local/bin/start-chromium-9224`
- The Chromium debug profiles are intentionally rooted under snap-compatible paths:
  - `~/snap/chromium/common/chrome-js-reverse`
  - `~/snap/chromium/common/chrome-mcp-dp`
  - `~/snap/chromium/common/chrome-mcp-pw`
- The imported Codex skills/prompts set was also pruned so entries that explicitly depended on undeployed MCP stacks (for example autoproxy/search-layer/markmap-related pieces) were removed instead of being left as dead routing noise.
