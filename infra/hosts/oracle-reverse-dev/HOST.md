# oracle-reverse-dev / HOST

## Identity
- Name: `oracle-reverse-dev`
- Provider: Oracle Cloud Infrastructure
- Public IP: `140.245.61.236`
- SSH alias: `oracle-reverse-dev`
- Default SSH user: `ubuntu`
- Created: 2026-03-25
- Primary role: reverse-development machine for reverse engineering work

## Access
- OpenClaw-side SSH key path: `~/.ssh/oracle-registry.pem`
- Current SSH verification: success on 2026-03-25
- Hostname observed: `instance-20260325-1818`

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

## Notes
- This host was initially unreachable because OCI networking was incomplete. SSH became reachable after the user added IPv4 ingress and internet gateway routing.
- Uses the same provided private key material currently stored locally as `~/.ssh/oracle-registry.pem`.
- It is semantically positioned as a dedicated reverse-development machine rather than a generic utility worker.
- Suitable as a lightweight ARM reverse/dev workstation for MCP-based browser automation, JS reverse workflows, tooling experiments, and ad-hoc development.
- Read-only fleet check found temporary upload backend / snap cups listeners as runtime drift rather than intended long-term surface unless explicitly kept.
