# ali-cloud / NETWORK

## Public identity
- Public IP: `106.15.239.221`

## Active public services
- `1panel` on host port `80`
- `camoufox-remote` websocket endpoint on `39222`
- authenticated SOCKS5 proxy on `2080`
- authenticated HTTP proxy on `2081`
- DNS forwarder on `1053`

## DNS notes
- Alibaba DHCP previously supplied unusable internal resolvers `100.100.2.136` / `100.100.2.138`
- persistent netplan override now forces `223.5.5.5` / `223.6.6.6`
- local stub resolution through `127.0.0.53` recovered after the override
