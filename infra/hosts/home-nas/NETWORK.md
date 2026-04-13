# home-nas / Network

## 1. Network Identity
- Home LAN snapshot during 2026-03-27 diagnostics:
  - NAS local IPv4: `192.168.8.16`
  - observed gateway / router: `192.168.8.1`

## 2. Documented Access Paths
### SSH
- Verified login user: `zhangxuemin`
- Passwordless SSH from the OpenClaw host is enabled via installed public key
- `zhangxuemin` has passwordless sudo on the NAS via `/etc/sudoers.d/zhangxuemin`

### FRP-published services
- DSM HTTPS target: local DSM `5001`
- Synology Drive target: current published service set should track the FRP mappings documented under `self-server`
- Current intended public publication on `self-server(:44001)`:
  - `30015/tcp` -> DSM HTTPS
  - `30016/tcp` -> Synology Drive

## 3. Operator Notes
- Synology package control can be misleading; validate using real listeners/processes where possible
- Prefer documenting stable LAN identity, FRP exposure, and local service ports here
