# oracle-newapi-standby / HOST

## Identity
- Name: `oracle-newapi-standby`
- Former name / compatibility alias: `oracle-reverse-dev`
- Provider: Oracle Cloud Infrastructure
- Public IP: `140.245.61.236`
- SSH alias: `oracle-newapi-standby`
- Legacy SSH alias retained: `oracle-reverse-dev`
- Default SSH user: `ubuntu`
- Created: 2026-03-25
- Primary role: standby New API / AI API relay host

## Access
- OpenClaw-side SSH key path: `~/.ssh/oracle-registry.pem`
- Current SSH verification: success on 2026-03-25
- Domestic/HK SSH edge added 2026-06-01: `ssh -p 22061 ubuntu@reverse-cn.zhangxuemin.work` (Cloudflare DNS-only A -> `hk-relay`, TCP relay -> this host `:22`)
- Local convenience aliases on the OpenClaw host: `oracle-reverse-dev-cn` / `reverse-cn`
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
- It was formerly positioned as a reverse-development machine; as of 2026-06-08 its primary role is standby New API relay.
- Suitable as a lightweight ARM reverse/dev workstation for MCP-based browser automation, JS reverse workflows, tooling experiments, and ad-hoc development.
- On 2026-06-08, user-requested cleanup removed the no-longer-needed `GPT-FULL-REGIST-AND-PAYMENT-FLOW` and `aBaiAutoplus` Docker/runtime/source payloads. Docker/base reverse-dev tooling remains for future use.
- Snap CUPS public listener drift was stopped/disabled during the same cleanup; treat any future `:631` reappearance as drift unless explicitly re-approved.

## New API deployment baseline
- Role: standby
- App directory: `/opt/new-api`
- Compose project: `newapi`
- Container: `new-api`
- Image: `calciumion/new-api:latest`
- Data directory: `/opt/new-api/data`
- Backup directory: `/opt/new-api/backups`
- App listener: `127.0.0.1:13000 -> container:3000`
- Public front door: Caddy on `:80`, reverse-proxying to `127.0.0.1:13000`
- Planned DNS name: `newapi-standby.zhangxuemin.work`
- Current access until DNS/TLS is finalized: `http://140.245.61.236/`
- Verification on 2026-06-08: container healthy, `/` returns `HTTP/1.1 200 OK`, `X-New-Api-Version: v1.0.0-rc.10`, Caddy adds `X-NewAPI-Role: standby`.

## 2026-06-08 upstream integration note
- CPA/CLIProxy and Kiro-Go upstream channels were provisioned directly in the New API database on this host.
- `channel_info` must be stored as BLOB JSON with `multi_key_mode` as string enum (`"random"`), not as text/number, otherwise New API channel selection fails with scan/unmarshal errors.
- New API tokens are stored in DB without the `sk-` prefix, while user-facing token files include the `sk-` prefix.
