# self-server `:44005` / `host185` — FRPS relay plan

## Purpose
Repurpose `self-server-44005` (`host185`) into the dedicated `frps` relay for exposing selected services from:
- `home-macmini`
- `home-nas`

The relay uses the shared public IP `211.144.221.229` but must stay inside the user-confirmed `:44005` TCP allocation: `30001-30010`.

## Current public-port occupancy
- `30001/tcp` — `prompt-optimizer-studio`
- `30008/tcp` — `1panel-core`

## Recommended FRP allocation
- `30009/tcp` — `frps` bind/control port
- `30010/tcp` — optional `frps` dashboard (prefer disabled, loopback-only, or tightly restricted)
- `30002-30007/tcp` — service exposure pool for `frpc` clients

This leaves the port plan as:
- `30001` -> Prompt Optimizer Studio
- `30002-30007` -> home-service proxy ports via `frps`
- `30008` -> 1Panel
- `30009` -> `frps`
- `30010` -> optional dashboard

## Why this map
- avoids conflict with already-running services on `30001` and `30008`
- keeps `frps` control separate from published business/service ports
- preserves a small contiguous pool for future `home-macmini` / `home-nas` exposures
- fits the known forwarding budget without assuming undocumented extra ports

## Firewall / network notes
Read-only check on 2026-04-08 found:
- `firewalld` active
- existing public opens included `30003`, `30004`, `30005`, `30006`, `30007`, `30009`, `30010`
- stale public open `9090/tcp`
- stale forward-port rule `30007/tcp -> 9090/tcp`

Rollout result on 2026-04-08:
- FRPS deployed at `/opt/frps-44005` with ports `30009` (bind) and `30010` (dashboard)
- `9090/tcp` removed
- `30007/tcp -> 9090/tcp` forward rule removed
- initial post-rollout state had only `30001`, `30008`, `30009`, `30010` publicly opened plus baseline `22/80/443`

Validated live state on 2026-04-08 later the same day:
- `frps` process is actively listening on `30009` and `30010`
- published proxy listeners are already active on:
  - `30002/tcp` -> `home-macmini` SSH (`frpc` running from `/Users/mengma/frp/frpc.toml`)
  - `30003/tcp` -> `home-nas` SSH (`frpc` running from `/usr/local/etc/frpc-nas.toml`)
- from `ali-cloud`, public TCP connect checks to `211.144.221.229:30002`, `:30003`, `:30009`, and `:30010` all succeeded
- `ssh-keyscan` via `ali-cloud` confirmed `30002` and `30003` are exposing real SSH daemons behind FRP rather than just open sockets
- current `firewalld` public opens on `:44005` are therefore effectively: `22/80/443`, `30001`, `30002`, `30003`, `30008`, `30009`, `30010`

Ongoing discipline:
- treat `30002` and `30003` as now claimed by the active SSH mappings above
- only re-open / reuse `30004-30007` when a specific additional home-side service mapping is decided
- dashboard on `30010` is BasicAuth-protected, but still consider restricting exposure further if not needed

## Suggested exposure discipline
Prefer explicit one-port-per-service mapping and document each one.
Example planning shape:
- `30002` -> `home-macmini` SSH / admin endpoint
- `30003` -> `home-nas` SSH or SFTP
- `30004` -> `home-nas` web app A
- `30005` -> `home-macmini` web app B
- `30006-30007` -> future spare capacity

Actual assignment should be chosen only after confirming which services really need public exposure.

## FRP protocol caution
The documented forwarding budget for this VM is currently TCP-only.
Do not assume UDP/KCP/QUIC exposure is available for FRP without separate confirmation from the virtualization/provider side.

## Security posture
- Prefer token-authenticated `frps` / `frpc`
- Prefer dashboard disabled; if enabled, bind to loopback or protect it strongly
- Expose only the minimum necessary service ports
- Re-check `firewalld` after deployment so the rule set matches the real listeners
- Keep a written mapping between public port and home-side target in this `infra/` tree
