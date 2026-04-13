# self-server FRP relay migration note

## Current decision
FRP relay responsibilities were migrated away from `self-server-44005` (`host185`) and consolidated onto `self-server` / `:44001` (`181`).

The reason is simple:
- `:44001` has the cleaner long-term role as `1Panel + FRPS`
- `:44005` has the tighter `30001-30010` public-port budget and is now needed mainly for application traffic (`NapCat`, `AstrBot`, `1Panel`)
- keeping FRPS on `:44005` created avoidable contention with the application ports

## Historical note
`host185` / `:44005` did previously run `frps` and served active home-lab mappings such as:
- `30002/tcp` -> `home-macmini` ComfyUI (`127.0.0.1:8188`)
- `30003/tcp` -> `home-nas` DSM WebUI (`127.0.0.1:5001`, HTTPS)
- `30004/tcp` -> `home-nas` Synology Drive Server (`127.0.0.1:6690`)
- `30009/tcp` -> `frps` control port
- `30010/tcp` -> `frps` dashboard

That was a real intermediate state, but it is no longer the intended steady-state design.

## New steady-state relay layout (`:44001` / `181`)
- `30011/tcp` -> `1panel-core`
- `30012/tcp` -> `frps` bind/control port
- `30013/tcp` -> `frps` dashboard
- `30014/tcp` -> `home-macmini` ComfyUI (`127.0.0.1:8188`)
- `30015/tcp` -> `home-nas` DSM WebUI (`127.0.0.1:5001`, HTTPS)
- `30016/tcp` -> `home-nas` Synology Drive Server (`127.0.0.1:6690`)
- `30017-30025/tcp` -> reserved spare FRP payload capacity for future home-service exposure

## Corresponding `frpc` migration
### `home-macmini`
`/Users/mengma/frp/frpc.toml`
- `serverAddr = "211.144.221.229"`
- `serverPort = 30012`
- `remotePort = 30014`

### `home-nas`
`/usr/local/etc/frpc-nas.toml`
- `serverAddr = "211.144.221.229"`
- `serverPort = 30012`
- `nas-webui.remotePort = 30015`
- `nas-drive.remotePort = 30016`

## `:44005` target steady state after migration
`host185` should no longer carry FRPS responsibilities.
Its intended public-port occupancy should instead stay focused on application traffic:
- `30001/tcp` -> NapCat WebUI
- `30005/tcp` -> AstrBot / QQ personal / OneBot v11 reverse WS host publish
- `30006/tcp` -> AstrBot auxiliary publish
- `30007/tcp` -> AstrBot WebUI
- `30008/tcp` -> `1panel-core`

And these former FRPS ports on `:44005` should remain cleared unless there is a future explicit redesign:
- `30002/tcp`
- `30003/tcp`
- `30004/tcp`
- `30009/tcp`
- `30010/tcp`

## Operational caution
During the cutover, `host185` showed evidence that the old `frps` process could be relaunched by local startup residue even after a manual stop. If FRPS listeners reappear on `:44005`, re-check:
- stray `frps` process restarts
- old startup hooks or service wrappers
- residual firewall opens for `30002/30003/30004/30009/30010`

The design intent is now unambiguous:
- `:44001` = FRPS relay
- `:44005` = application host
