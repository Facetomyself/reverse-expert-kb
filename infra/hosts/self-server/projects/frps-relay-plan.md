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
During the cutover, `host185` showed evidence that the old `frps` process could be relaunched after a manual stop. The actual restart source was **not** a normal `frps.service`; it was a Docker Compose container:
- container: `frps-44005`
- image: `snowdreamtech/frps:0.64.0`
- project dir: `/opt/frps-44005`
- restart policy: `unless-stopped`

So if FRPS listeners reappear on `:44005`, check Docker first, not just systemd. Effective removal required:
- `docker update --restart=no frps-44005`
- `docker stop frps-44005`
- `docker rm frps-44005`

On the NAS side, the migration also exposed two operator gotchas:
- `/usr/local/etc/rc.d/S99frpc-nas.sh` supports only `start|stop`, not `restart`
- overly broad remote `pkill -f "frpc.*frpc-nas.toml"` style commands can accidentally kill the current remote shell/launcher path and make it look like `frpc` "won't stay up"

Final live validation after the NAS-side fix on 2026-04-13:
- `:44001` listeners present: `30014`, `30015`, `30016`
- external checks from `ali-cloud` confirmed:
  - `http://211.144.221.229:30014/` -> ComfyUI reachable
  - `https://211.144.221.229:30015/` -> DSM reachable (`HTTP/2 200`)
  - plain `http://211.144.221.229:30015/` -> `400 Bad Request`, which is expected because this mapping targets DSM HTTPS on `5001`

The design intent is now unambiguous:
- `:44001` = FRPS relay
- `:44005` = application host
