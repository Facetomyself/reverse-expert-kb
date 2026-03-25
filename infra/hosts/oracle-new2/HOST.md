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
  - `docker` group membership is already present for `ubuntu`

## Notes
- This host was initially unreachable because OCI networking was incomplete (missing effective IPv4 ingress / internet path). SSH became reachable after the user added IPv4 ingress and internet gateway routing.
- Uses the same provided private key material currently stored locally as `~/.ssh/oracle-new1.pem`.
- `fwupd-refresh.service` showed as failed during first baseline check; not currently treated as a blocker for server use.
- Suitable as a lightweight ARM Docker worker / utility host; left otherwise mostly idle after base provisioning.
