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
- Durable operator rule: from Oracle/OpenClaw-side environments, SSH access to domestic servers should default to `ProxyJump ali-cloud` rather than attempting direct connections to `211.144.221.229`-side targets
- The local SSH config now reflects that preference by making `self-server` use `ProxyJump ali-cloud`
- `self-server-direct` is preserved for direct-path diagnostics only

## System baseline snapshot (2026-04-04)
### `:44001` / hostname `181`
- OS: CentOS Linux 7 (Core)
- Kernel: `5.15.60-1.el7.x86_64`
- Primary private IP: `10.10.21.181/24`
- Default route: `10.10.21.254`
- Runtime shape: lightweight 1Panel + Docker host
- Key observed listeners: `22`, `30011`, `30012`, `30013`
- Final same-day outbound shape: local `dnsmasq` on `127.0.0.1:53` with upstream `106.15.239.221#1053`, plus explicit shell/Docker proxying via `ali-cloud` authenticated HTTP/SOCKS proxy ingress (`:2081` / `:2080`)

### `:44005` / hostname `host185`
- OS: CentOS Linux 7 (Core)
- Kernel: `3.10.0-1160.119.1.el7.x86_64`
- Primary private IP: `10.10.21.185/24`
- Default route: `10.10.21.254`
- Runtime shape: aggressively reduced toward 1Panel-only; historical `mihomo`, postfix, Docker workloads, most operator tooling residue, and stale 1Panel MySQL application/data residue were removed on 2026-04-04
- Key remaining listeners after cleanup: `22`, `30008`
- Additional documented service as of 2026-04-06: `prompt-optimizer-studio` on public `30001`
- Final same-day outbound shape: local `dnsmasq` on `127.0.0.1:53` with upstream `106.15.239.221#1053`, plus explicit shell/Docker proxying via `ali-cloud` authenticated HTTP/SOCKS proxy ingress (`:2081` / `:2080`)

## User-confirmed port constraints
Recorded on 2026-04-04 because public IP / forwarding resources are limited on this virtualization side:
- `:44001` machine may use only `TCP 30011-30025`
- `:44005` machine may use only `TCP 30001-30010`

## Final intended roles (frozen on 2026-04-04)
### `:44001` / `181`
- Keep as: `1Panel + FRPS` machine
- Preferred public-use budget: `30011-30025`
- Current meaningful listeners after cleanup:
  - `30011` -> `1panel-core`
  - `30012` -> `frps`
  - `30013` -> `frps` dashboard
- Outbound access model:
  - keep local resolver pointed at `127.0.0.1`
  - keep `dnsmasq` forwarding to `ali-cloud:1053`
  - keep shell/Docker on explicit proxy mode through `ali-cloud`
  - as of 2026-04-13, this explicit-proxy model already inherits centralized upstream exit switching from `ali-cloud` without host-local Mihomo deployment
  - do not reintroduce the same-day abandoned transparent TUN experiment unless the remote ingress protocol is redesigned
- Cleanup rule:
  - keep `1Panel`, `FRPS`, and SSH
  - do not casually add unrelated long-lived dev environments here

### `:44005` / `host185`
- Current role after the 2026-04-13 cutover: application-focused host within the tighter `30001-30010` public TCP budget
- Preferred public-use budget remains: `30001-30010`
- Main intended public occupancy now is:
  - `30001` -> `NapCat WebUI`
  - `30005` -> `AstrBot` OneBot / QQ personal host publish
  - `30006` -> `AstrBot` auxiliary publish
  - `30007` -> `AstrBot WebUI`
  - `30008` -> `1panel-core`
- Historical note:
  - this VM temporarily carried the active FRPS relay role on 2026-04-08 through 2026-04-12, using `30009/30010` plus service ports like `30002-30004`
  - that relay role was intentionally migrated away on 2026-04-13 so the smaller `:44005` budget could be reclaimed for application traffic
- Desired steady state after migration:
  - keep `1Panel`, SSH, `NapCat`, and `AstrBot`
  - keep `30002/30003/30004/30009/30010` cleared unless a future redesign explicitly reassigns them
  - avoid reintroducing unrelated long-lived dev tooling
- Outbound access model:
  - keep local resolver pointed at `127.0.0.1`
  - keep `dnsmasq` forwarding to `ali-cloud:1053`
  - keep shell/Docker on explicit proxy mode through `ali-cloud`
  - as of 2026-04-13, this explicit-proxy model already inherits centralized upstream exit switching from `ali-cloud` without host-local Mihomo deployment
  - do not restore the removed transparent `sing-box-global` experiment from 2026-04-04; it was intentionally abandoned after TUN->remote-SOCKS proved unstable for general HTTPS traffic

## Operator guidance
- Prefer `ali-cloud` as the transit path for routine access from the current OpenClaw environment
- Treat `self-server` (`:44001`) and `self-server-44005` (`:44005`) as distinct machines even though they share the same public IP
- Before introducing any new externally reachable service, first map it into the user-confirmed per-VM TCP budget above
