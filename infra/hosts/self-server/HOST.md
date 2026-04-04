# self-server / HOST

## Identity
- Name: `self-server`
- Provider: unknown / domestic-hosting-side machine
- Public IP: `211.144.221.229`
- SSH aliases:
  - `self-server` -> preferred OpenClaw-side access path via `ali-cloud` jump host to `:44001`
  - `self-server-direct` -> direct probe path to `:44001` from the local OpenClaw host
  - `self-server-44005` -> preferred OpenClaw-side access path via `ali-cloud` jump host to `:44005`
  - `self-server-44005-direct` -> direct probe path to `:44005` from the local OpenClaw host
- Default SSH user: `root`

## Access
- Confirmed SSH ports from user on 2026-04-04:
  - `44001`
  - `44005`
- Authentication mode now established for both reachable paths:
  - bootstrap via password auth
  - routine access via OpenClaw-side public-key auth through `ali-cloud` jump-host transit
- Credential handling note: user-provided passwords were used interactively during bootstrap on 2026-04-04 but are intentionally **not** stored in `infra/`

## Reachability notes
Observed on 2026-04-04:
- direct probe from the current OpenClaw host to `211.144.221.229:44001` still timed out
- TCP probe from `ali-cloud` to `211.144.221.229:44001` succeeded
- a full SSH attempt through the configured `ProxyJump ali-cloud` path reached an interactive password prompt from the target host, confirming that the jump-host path is viable
- after the user corrected the password, login through `ali-cloud` succeeded
- same-day follow-up installed an OpenClaw-side public key on the remote root account behind `:44001` and confirmed passwordless login works through `ssh self-server`
- a second same-IP target behind `:44005` was later clarified by the user; direct path from the current OpenClaw host still timed out, but transit via `ali-cloud` worked
- password `Zxm971004` failed for `:44005`, while corrected password `WnhtOTcxMDA0` succeeded
- same-day follow-up then installed the same OpenClaw-side RSA public key on the remote root account behind `:44005` and confirmed passwordless login works through `ssh self-server-44005`

## Operational interpretation
- Treat `ali-cloud` as the preferred China-side transit point when testing or using this host from the current environment
- The local SSH config now reflects that preference by making `self-server` use `ProxyJump ali-cloud`
- `self-server-direct` is preserved for direct-path diagnostics

## System baseline snapshot (2026-04-04)
### `:44001` / hostname `181`
- OS: CentOS Linux 7 (Core)
- Kernel: `5.15.60-1.el7.x86_64`
- Primary private IP: `10.10.21.181/24`
- Default route: `10.10.21.254`
- Runtime shape: lightweight 1Panel + Docker host
- Key observed listeners: `22`, `30011`, `30012`, `30013`

### `:44005` / hostname `host185`
- OS: CentOS Linux 7 (Core)
- Kernel: `3.10.0-1160.119.1.el7.x86_64`
- Primary private IP: `10.10.21.185/24`
- Default route: `10.10.21.254`
- Runtime shape: aggressively reduced toward 1Panel-only; historical `mihomo`, postfix, Docker workloads, and most operator tooling residue were removed on 2026-04-04
- Key remaining listeners after cleanup: `22`, `30008`

## User-confirmed port constraints
Recorded on 2026-04-04 because public IP / forwarding resources are limited on this virtualization side:
- `:44001` machine may use only `TCP 30011-30025`
- `:44005` machine may use only `TCP 30001-30010`

## Next checks
- decide later whether `:44001` and `:44005` should keep living under one shared host doc or be split into two dedicated machine docs on the same public IP
- if `:44005` should become a cleaner long-term 1Panel box, consider whether Docker itself is still needed or whether 1Panel-only management should stay as the minimal baseline
- verify whether any additional shell-init cleanup is still needed after the environment removals on `:44005`
