# oracle-new1 / HOST

## Identity
- Name: `oracle-new1`
- Provider: Oracle Cloud Infrastructure
- Public IP: `140.245.33.114`
- SSH alias: `oracle-registry` (legacy-compatible alias `oracle-new1` retained locally)
- Default SSH user: `ubuntu`
- Created: 2026-03-25

## Access
- OpenClaw-side SSH key path: `~/.ssh/oracle-new1.pem`
- Current SSH verification: success on 2026-03-25
- Hostname observed / set on 2026-03-25: `oracle-registry`
- Tailnet IPv4: `100.96.23.110` (joined 2026-03-25)

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
- This host was initially unreachable because OCI networking was incomplete (missing effective IPv4 ingress / internet path). SSH became reachable after the user added IPv4 ingress and internet gateway routing.
- Uses the same provided private key material currently stored locally as `~/.ssh/oracle-new1.pem`.
- On 2026-03-25, this host was promoted from empty ARM utility host to the live registry-proxy front door for `hub.zhangxuemin.work`, `ghcr.zhangxuemin.work`, `k8s.zhangxuemin.work`, and `mcr.zhangxuemin.work`.
- During cutover, OCI-side ingress was not sufficient by itself; local iptables initially allowed only SSH and had to be extended/persisted for `80/tcp` and `443/tcp` before Caddy ACME issuance succeeded.
- Local operator health-check helper installed at `/usr/local/bin/check-registry-proxies`.
