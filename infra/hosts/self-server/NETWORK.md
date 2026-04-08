# self-server / NETWORK

## Public ingress model
Same public IP hosts two separate SSH-reachable targets behind different forwarded ports:

- `211.144.221.229:44001` -> machine currently observed as hostname `181`
- `211.144.221.229:44005` -> machine currently observed as hostname `host185`

Preferred operator access from OpenClaw is via `ali-cloud` transit rather than direct access from the current OpenClaw host.

## User-confirmed port constraints (2026-04-04)
Because public-IP resources are limited on this virtualization side, each machine only has a small TCP allocation:

### Target `:44001` (`181`)
Allowed public TCP range:
- `30011-30025`

Observed listening TCP ports during same-day read-only inspection:
- `22/tcp` - sshd
- `30011/tcp` - `1panel-core`
- `30012/tcp` - `frps`
- `30013/tcp` - `frps`

Operational note:
- The observed listeners fit inside the user-confirmed allowed allocation.
- Intended steady-state role after 2026-04-04 cleanup: keep this VM as the `1Panel + FRPS` box for this shared-IP pair.
- Final same-day outbound model is explicit rather than transparent: this VM now keeps a local `dnsmasq` listener on `127.0.0.1:53`, forwards DNS to `106.15.239.221#1053`, and uses `ali-cloud` authenticated proxy ingress on `:2081` / `:2080` for shell and Docker egress.

### Target `:44005` (`host185`)
Allowed public TCP range:
- `30001-30010`

Observed listening TCP ports during initial same-day read-only inspection:
- `22/tcp` - sshd
- `5837/tcp` - sshd additional listener
- `30008/tcp` - `1panel-core`
- `9090/tcp` - `mihomo`
- `1053/tcp` - `mihomo`
- `111/tcp` - rpcbind
- `25/tcp` loopback-only / localhost-bound by postfix
- `7890/tcp` loopback-only by `mihomo`

Post-cleanup state observed later on 2026-04-04:
- `22/tcp` - sshd
- `30008/tcp` - `1panel-core`

Additional deployment observed on 2026-04-06:
- `30001/tcp` - `prompt-optimizer-studio` (Docker Compose, self-hosted Next.js app)

Read-only validation on 2026-04-08:
- actual listening ports on the VM were `22/tcp`, `30001/tcp`, and `30008/tcp`
- `firewalld` was active and already allowed `30003/tcp`, `30004/tcp`, `30005/tcp`, `30006/tcp`, `30007/tcp`, `30009/tcp`, and `30010/tcp`
- a stale `firewalld` forward-port still existed: `30007/tcp -> 9090/tcp`; this collides with the cleaner future FRP use of the `30001-30010` budget and should be removed when the FRPS role is actually deployed

Operational note:
- `30008/tcp` and `30001/tcp` currently fit inside the user-confirmed allowed allocation.
- historical listeners `5837`, `9090`, `1053`, and `111` were removed from active service during the same-day cleanup pass to bring this VM closer to a true 1Panel-only shape, but the later 2026-04-08 firewall check showed residual allow/forward rules still remain and should be normalized during FRPS rollout.
- Updated intended steady-state role on 2026-04-08: keep this VM as the `FRPS` relay box for exposing selected `home-macmini` / `home-nas` services over the shared public IP.
- Recommended public TCP allocation for that role:
  - `30001` -> existing `prompt-optimizer-studio`
  - `30008` -> existing `1panel-core`
  - `30009` -> `frps` bind/control port
  - `30010` -> optional `frps` dashboard (prefer disabled or restricted)
  - `30002-30007` -> application-facing proxy ports published by `frps` for home services
- Protocol caution:
  - the documented forwarding allocation for `:44005` is currently TCP-only; do not assume extra UDP budget for FRP features such as KCP/QUIC without separate confirmation
- Firewall caution:
  - do not broadly open `30001-30010` just because the VM owns that range; only keep the ports that are actually assigned to running services
  - if `frps` is deployed, explicitly remove obsolete `9090` exposure and the `30007 -> 9090` forward rule first so `30007` can be safely reclaimed
  - 2026-04-08 implementation outcome on `:44005`: `9090` and `30007 -> 9090` were removed during rollout
  - later same-day live validation showed active FRP-published listeners on `30002` and `30003`, so the effective current public opens are `30001`, `30002`, `30003`, `30008`, `30009`, `30010` plus baseline `22/80/443`
  - final active mapping corrected on 2026-04-08:
    - `30002/tcp` -> `home-macmini` ComfyUI via FRP (`127.0.0.1:8188`)
    - `30003/tcp` -> `home-nas` DSM WebUI via FRP (`127.0.0.1:5001`, HTTPS)
- Final outbound model remains explicit rather than transparent: this VM keeps a local `dnsmasq` listener on `127.0.0.1:53`, forwards DNS to `106.15.239.221#1053`, and uses `ali-cloud` authenticated proxy ingress on `:2081` / `:2080` for shell and Docker egress; the short-lived transparent TUN experiment was removed after proving unstable for general HTTPS traffic.
