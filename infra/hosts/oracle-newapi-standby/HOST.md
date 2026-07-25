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
- Primary role: empty Ubuntu ARM utility host / candidate deployment target

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
- It was formerly positioned as a reverse-development machine, then as standby New API relay. As of 2026-07-07, user confirmed New API standby is unused and requested cleanup to a no-project baseline.
- Current stance: ARM utility host now running Sub2API as its only active project deployment. Do not assume any New API service, static docs site, reverse/dev app, or user-home project residue remains active.
- On 2026-06-08, user-requested cleanup removed the no-longer-needed `GPT-FULL-REGIST-AND-PAYMENT-FLOW` and `aBaiAutoplus` Docker/runtime/source payloads. Docker/base reverse-dev tooling remains for future use.
- Snap CUPS public listener drift was stopped/disabled during the same cleanup; treat any future `:631` reappearance as drift unless explicitly re-approved.

## Current active baseline
- 2026-07-07 cleanup removed the New API standby deployment and user-home project residue.
- 2026-07-07 follow-up removed Firefox snap with `snap remove --purge firefox`, deleted any remaining Firefox snap directories, and reset stale systemd failed state; `systemctl --failed` then reported `0 loaded units listed`.
- 2026-07-22 deployed Sub2API under `/opt/sub2api` via Docker Compose.
- Active Docker containers: `sub2api`, `sub2api-postgres`, `sub2api-redis`.
- Caddy is active for `sub2api.zhangxuemin.work` on `80/443`, reverse-proxying to the loopback app listener `127.0.0.1:18088`.
- `/home/ubuntu` is cleaned to login/shell basics only (`.ssh`, shell rc/profile files).
- Expected public project listeners: `22`, `80`, `443`.
- Baseline after Sub2API deployment: root disk remained low-use with ample free space; memory headroom remains large for this service class.

## Retired New API deployment baseline
- Former role: standby
- Former app directory: `/opt/new-api` (removed 2026-07-07)
- Former compose project: `newapi` (removed 2026-07-07)
- Former container: `new-api` (removed 2026-07-07)
- Former image: `calciumion/new-api:latest` (removed 2026-07-07)
- Former data directory: `/opt/new-api/data` (removed 2026-07-07)
- Former backup directory: `/opt/new-api/backups` (removed 2026-07-07)
- Former app listener: `127.0.0.1:13000 -> container:3000` (gone)
- Former public front door: Caddy on `:80` (stopped/disabled)
- Former planned DNS name: `newapi-standby.zhangxuemin.work`
- Last verification before retirement on 2026-06-08: container healthy, `/` returned `HTTP/1.1 200 OK`, `X-New-Api-Version: v1.0.0-rc.10`, Caddy added `X-NewAPI-Role: standby`.

## Retired 2026-06-08 upstream integration note
- CPA/CLIProxy and Kiro-Go upstream channels were provisioned directly in the New API database on this host.
- `channel_info` must be stored as BLOB JSON with `multi_key_mode` as string enum (`"random"`), not as text/number, otherwise New API channel selection fails with scan/unmarshal errors.
- New API tokens are stored in DB without the `sk-` prefix, while user-facing token files include the `sk-` prefix.
