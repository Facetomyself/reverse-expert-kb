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
- OS: Ubuntu 24.04
- Kernel: `6.17.0-1007-oracle`
- Arch: `aarch64`
- Initial groups for default user: `adm`, `sudo`, `lxd`, etc.

## Notes
- This host was initially unreachable because OCI networking was incomplete (missing effective IPv4 ingress / internet path). SSH became reachable after the user added IPv4 ingress and internet gateway routing.
- Uses the same provided private key material currently stored locally as `~/.ssh/oracle-new1.pem`.
