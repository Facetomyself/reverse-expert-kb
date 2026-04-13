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
- 2026-04-13 live validation after the FRP migration confirmed the active published payload listeners expanded to:
  - `30014/tcp` -> `home-macmini` ComfyUI
  - `30015/tcp` -> `home-nas` DSM HTTPS
  - `30016/tcp` -> `home-nas` Synology Drive
- External validation from `ali-cloud` confirmed:
  - `http://211.144.221.229:30014/` served ComfyUI
  - `https://211.144.221.229:30015/` returned `HTTP/2 200`
  - `http://211.144.221.229:30015/` returned `400 Bad Request`, which is expected because the FRP target is DSM HTTPS on `5001`
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
- 2026-04-13 migration decision moved the active FRPS relay role off `:44005` and back onto `:44001`, so this VM should no longer be treated as the long-term FRP relay host.
- Effective application-focused public TCP allocation after the migration is intended to be:
  - `30001/tcp` -> `NapCat WebUI`
  - `30005/tcp` -> `AstrBot` / QQ personal / OneBot v11 host publish
  - `30006/tcp` -> `AstrBot` auxiliary publish
  - `30007/tcp` -> `AstrBot WebUI`
  - `30008/tcp` -> `1panel-core`
- Former FRPS-related ports on `:44005` that should now stay free unless explicitly redesigned:
  - `30002/tcp`
  - `30003/tcp`
  - `30004/tcp`
  - `30009/tcp`
  - `30010/tcp`
- Historical note:
  - `:44005` did temporarily host the live FRPS relay and business-service mappings on 2026-04-08 through 2026-04-12
  - those mappings were migrated on 2026-04-13 to the cleaner `:44001` FRPS layout using `30012` control and payload ports beginning at `30014`
- Protocol caution:
  - the documented forwarding allocation for this VM is currently TCP-only; do not assume extra UDP budget for FRP features such as KCP/QUIC without separate confirmation
- Firewall caution:
  - do not broadly open `30001-30010` just because the VM owns that range; only keep the ports that are actually assigned to running services
  - after FRPS removal, normalize any residual public opens for `30002/30003/30004/30009/30010` so the rule set matches the new application-focused reality
- Final outbound model remains explicit rather than transparent: this VM keeps a local `dnsmasq` listener on `127.0.0.1:53`, forwards DNS to `106.15.239.221#1053`, and uses `ali-cloud` authenticated proxy ingress on `:2081` / `:2080` for shell and Docker egress; the short-lived transparent TUN experiment was removed after proving unstable for general HTTPS traffic.
