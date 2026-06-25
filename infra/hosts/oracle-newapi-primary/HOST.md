# oracle-newapi-primary / HOST

## Identity
- Name: `oracle-newapi-primary`
- Former name / compatibility alias: `oracle-registry`
- Provider: Oracle Cloud Infrastructure
- Public IP: `140.245.33.114`
- SSH alias: `oracle-newapi-primary`
- Legacy SSH alias retained: `oracle-registry`
- Default SSH user: `ubuntu`
- Created: 2026-03-25

## Access
- OpenClaw-side SSH key path: `~/.ssh/oracle-registry.pem`
- Current SSH verification: success on 2026-03-25
- Hostname set on 2026-06-08: `oracle-newapi-primary`

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
- Swap:
  - `/swapfile` enabled at 2G and persisted in `/etc/fstab`
- Docker:
  - daemon enabled and started
  - `hello-world` run succeeded during validation
- User notes:
  - `ubuntu` has sudo access
  - `docker` group membership may require a fresh login session to apply cleanly for non-sudo docker usage

## Notes
- This host was initially unreachable because OCI networking was incomplete. SSH became reachable after the user added IPv4 ingress and internet gateway routing.
- Uses the same provided private key material currently stored locally as `~/.ssh/oracle-registry.pem`.
- On 2026-03-25, this host was promoted from empty ARM utility host to the live registry-proxy front door for `hub.zhangxuemin.work`, `ghcr.zhangxuemin.work`, `k8s.zhangxuemin.work`, and `mcr.zhangxuemin.work`.
- On 2026-06-08, the user requested the no-longer-needed deployed projects on this host be cleaned. The registry-proxy and NexusVault monitor workloads, project directories, and project images were removed; Docker/base tooling remains for future reuse.
- Current stance: primary New API relay host, paired with `oracle-newapi-standby` for backup/failover.
- Historical helper `/usr/local/bin/check-registry-proxies` may exist as residue, but the registry proxy service it checked is retired and should not be treated as live.

## New API deployment baseline
- Role: primary
- App directory: `/opt/new-api`
- Compose project: `newapi`
- Container: `new-api`
- Image: `calciumion/new-api:latest`
- Data directory: `/opt/new-api/data`
- Backup directory: `/opt/new-api/backups`
- App listener: `127.0.0.1:13000 -> container:3000`
- Public front door: Caddy on `:80`, reverse-proxying to `127.0.0.1:13000`
- Planned DNS name: `newapi.zhangxuemin.work`
- Current access until DNS/TLS is finalized: `http://140.245.33.114/`
- Verification on 2026-06-08: container healthy, `/` returns `HTTP/1.1 200 OK`, `X-New-Api-Version: v1.0.0-rc.10`, Caddy adds `X-NewAPI-Role: primary`.

## 2026-06-08 upstream integration note
- CPA/CLIProxy and Kiro-Go upstream channels were provisioned directly in the New API database on this host.
- `channel_info` must be stored as BLOB JSON with `multi_key_mode` as string enum (`"random"`), not as text/number, otherwise New API channel selection fails with scan/unmarshal errors.
- New API tokens are stored in DB without the `sk-` prefix, while user-facing token files include the `sk-` prefix.
