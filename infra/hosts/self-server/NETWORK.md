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

Live validation on 2026-04-11 after AstrBot deployment:
- host listeners included `30005/tcp`, `30006/tcp`, `30007/tcp`, `10000/tcp`, `10001/tcp`, and `10002/tcp` via Docker proxy for the 1Panel-managed `astrbot` container
- confirmed container/host mapping:
  - `30007/tcp` -> AstrBot WebUI (`6185/tcp` in container)
  - `10000/tcp` -> `6194/tcp`
  - `10001/tcp` -> `6195/tcp`
  - `30006/tcp` -> `6196/tcp`
  - `30005/tcp` -> `6199/tcp`
  - `10002/tcp` -> `11451/tcp`
- host-local verification:
  - `curl http://127.0.0.1:30007/` returned `200 OK`
  - `curl http://127.0.0.1:6185/` failed with connection refused because `6185` is not bound on the host
- transit-side verification from `ali-cloud`:
  - public `211.144.221.229:30007` responded `200 OK`
  - public `211.144.221.229:30005` and `:30006` still returned connection refused at probe time, so do not assume all AstrBot auxiliary ports are currently reachable externally just because Docker is listening locally

Operational note:
- `30008/tcp`, `30001/tcp`, and now `30007/tcp` fit inside the user-confirmed allowed allocation.
- historical listeners `5837`, `9090`, `1053`, and `111` were removed from active service during the same-day cleanup pass to bring this VM closer to a true 1Panel-only shape, but the later 2026-04-08 firewall check showed residual allow/forward rules still remain and should be normalized during FRPS rollout.
- Updated intended steady-state role on 2026-04-08 kept this VM focused on the `FRPS` relay function, but 2026-04-11 live checks confirmed `AstrBot` is now also using part of the same public TCP budget.
- Effective public TCP allocation after the AstrBot confirmation:
  - `30001` -> existing `prompt-optimizer-studio`
  - `30007` -> `AstrBot WebUI` (host port published by Docker; upstream inside container is `6185`)
  - `30008` -> existing `1panel-core`
  - `30009` -> `frps` bind/control port
  - `30010` -> optional `frps` dashboard (prefer disabled or restricted)
  - `30002-30006` -> remaining application-facing proxy ports published by `frps` for home services unless later repurposed
- Protocol caution:
  - the documented forwarding allocation for `:44005` is currently TCP-only; do not assume extra UDP budget for FRP features such as KCP/QUIC without separate confirmation
- Firewall caution:
  - do not broadly open `30001-30010` just because the VM owns that range; only keep the ports that are actually assigned to running services
  - if `frps` is deployed, explicitly remove obsolete `9090` exposure and the `30007 -> 9090` forward rule first so `30007` can be safely reclaimed
  - 2026-04-08 implementation outcome on `:44005`: `9090` and `30007 -> 9090` were removed during rollout
  - later same-day live validation showed active FRP-published listeners on `30002` and `30003`
  - 2026-04-11 live validation then confirmed `30007/tcp` is no longer free FRP budget; it is occupied by AstrBot WebUI
  - final active mapping currently documented:
    - `30001/tcp` -> `prompt-optimizer-studio`
    - `30002/tcp` -> `home-macmini` ComfyUI via FRP (`127.0.0.1:8188`)
    - `30003/tcp` -> `home-nas` DSM WebUI via FRP (`127.0.0.1:5001`, HTTPS)
    - `30007/tcp` -> `AstrBot WebUI`
    - `30008/tcp` -> `1panel-core`
    - `30009/tcp` -> `frps`
    - `30010/tcp` -> `frps` dashboard / admin UI when enabled
- Final outbound model remains explicit rather than transparent: this VM keeps a local `dnsmasq` listener on `127.0.0.1:53`, forwards DNS to `106.15.239.221#1053`, and uses `ali-cloud` authenticated proxy ingress on `:2081` / `:2080` for shell and Docker egress; the short-lived transparent TUN experiment was removed after proving unstable for general HTTPS traffic.
