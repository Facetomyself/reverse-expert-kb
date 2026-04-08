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

Before FRPS rollout:
1. remove stale `9090` exposure
2. remove stale `30007 -> 9090` forward rule
3. keep only the actually-used FRP-related opens (`30009`, optional `30010`, and whichever of `30002-30007` are currently assigned)
4. do not expose the dashboard publicly unless there is a real operator need

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
