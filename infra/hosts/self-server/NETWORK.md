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

Operational note:
- `30008/tcp` fits inside the user-confirmed allowed allocation.
- historical listeners `5837`, `9090`, `1053`, and `111` were removed from active service during the same-day cleanup pass to bring this VM closer to a true 1Panel-only shape.
- Intended steady-state role after 2026-04-04 cleanup: keep this VM as the cleaner `1Panel` rebuild box for this shared-IP pair.
- Final same-day outbound model is explicit rather than transparent: this VM now keeps a local `dnsmasq` listener on `127.0.0.1:53`, forwards DNS to `106.15.239.221#1053`, and uses `ali-cloud` authenticated proxy ingress on `:2081` / `:2080` for shell and Docker egress; the short-lived transparent TUN experiment was removed after proving unstable for general HTTPS traffic.
