# self-server / HOST

## Identity
- Name: `self-server`
- Provider: unknown / domestic-hosting-side machine
- Public IP: `211.144.221.229`
- SSH aliases:
  - `self-server` -> preferred OpenClaw-side access path via `ali-cloud` jump host
  - `self-server-direct` -> direct probe path from the local OpenClaw host
- Default SSH user: `root`

## Access
- Confirmed SSH port from user on 2026-04-04: `44001`
- Authentication mode currently expected: password auth
- Credential handling note: password was user-provided in chat context on 2026-04-04 but is intentionally **not** stored in `infra/`

## Reachability notes
Observed on 2026-04-04:
- direct probe from the current OpenClaw host to `211.144.221.229:44001` still timed out
- TCP probe from `ali-cloud` to `211.144.221.229:44001` succeeded
- a full SSH attempt through the configured `ProxyJump ali-cloud` path reached an interactive password prompt from the target host, confirming that the jump-host path is viable
- after the user corrected the password, login through `ali-cloud` succeeded
- same-day follow-up installed an OpenClaw-side public key on the remote root account and confirmed passwordless login works through `ssh self-server`
- the same public IP also has another user-mentioned machine/service on port `40005`, but TCP probe from `ali-cloud` to `211.144.221.229:40005` still timed out during this session, so only the `44001` path is currently integrated

## Operational interpretation
- Treat `ali-cloud` as the preferred China-side transit point when testing or using this host from the current environment
- The local SSH config now reflects that preference by making `self-server` use `ProxyJump ali-cloud`
- `self-server-direct` is preserved for direct-path diagnostics

## Next checks
- treat `211.144.221.229:40005` as a second machine/service candidate on the same public IP, but currently unreachable even from `ali-cloud`
- once either `40005` becomes reachable or more identity detail is known, split that second target into its own documented access section or dedicated host doc
- add system baseline, role, and any project/network notes for the confirmed `44001` machine once a fuller inspection is desired
