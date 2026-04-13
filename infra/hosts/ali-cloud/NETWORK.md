# ali-cloud / NETWORK

## Public identity
- Public IP: `106.15.239.221`

## Active public services
- `1panel` on host port `80`
- `camoufox-remote` websocket endpoint on `39222`
- authenticated SOCKS5 proxy on `2080`
- authenticated HTTP proxy on `2081`
- DNS forwarder on `1053`

## Proxy gateway implementation
Validated on 2026-04-13:
- `:2080` / `:2081` are not direct foreign exits by themselves; they are sing-box inbounds from `/opt/sing-box-gateway/config.json`
- sing-box currently forwards all traffic to one final outbound tag: `oracle-egress`
- `oracle-egress` is a SOCKS5 upstream at `127.0.0.1:18080`
- `127.0.0.1:18080` is provided by the local Hysteria client from `/opt/hysteria-egress/client.yaml`
- the current Hysteria upstream is `backup.zhangxuemin.work:443`
- practical interpretation: domestic servers that use `106.15.239.221:2080/:2081` are currently exiting through `ali-cloud` only as a stable authenticated ingress, while the real foreign egress path is the local Hysteria client chained to `oracle-gateway`

## DNS notes
- Alibaba DHCP previously supplied unusable internal resolvers `100.100.2.136` / `100.100.2.138`
- persistent netplan override now forces `223.5.5.5` / `223.6.6.6`
- local stub resolution through `127.0.0.53` recovered after the override
