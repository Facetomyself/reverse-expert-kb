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

### Target `:44005` (`host185`)
Allowed public TCP range:
- `30001-30010`

Observed listening TCP ports during same-day read-only inspection:
- `22/tcp` - sshd
- `5837/tcp` - sshd additional listener
- `30008/tcp` - `1panel-core`
- `9090/tcp` - `mihomo`
- `1053/tcp` - `mihomo`
- `111/tcp` - rpcbind
- `25/tcp` loopback-only / localhost-bound by postfix
- `7890/tcp` loopback-only by `mihomo`

Operational note:
- Only the public-allocation claim is user-confirmed. The current `ss -ltnp` snapshot shows additional listeners, but not all of them are necessarily reachable from the public side.
- `30008/tcp` fits inside the user-confirmed allowed allocation.
- `9090`, `1053`, and `5837` deserve later verification before assuming they are intentionally exposed through external forwarding.
