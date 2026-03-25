# Hysteria Gateway on oracle-gateway

## Summary
`oracle-gateway` now serves as a lightweight Hysteria 2 relay/gateway host.

## Live surface
- Domain: `backup.zhangxuemin.work`
- Hysteria data plane: UDP `443`
- Caddy config download endpoint: TCP `443`
- Clash Verge config URL:
  - `https://backup.zhangxuemin.work/clash-verge.yaml`

## Runtime layout
- Working dir: `/opt/hysteria`
- Main config: `/opt/hysteria/config.yaml`
- Compose file: `/opt/hysteria/docker-compose.yml`
- Static subscription file: `/opt/hysteria/subscription/clash-verge.yaml`

## Validation
Verified on 2026-03-25 from `ali-cloud` with the official Hysteria client:
- server connection succeeded
- local SOCKS5 listener came up
- proxied HTTP request returned successfully

## Operational notes
- Caddy on this host must stay limited to `h1 h2`; enabling HTTP/3 would compete for UDP `443` with Hysteria.
- Keep this host lean; it is only ~1 GiB RAM and should avoid regaining old mixed workloads.
- Legacy registry/Harbor residuals were permanently deleted on 2026-03-25 per user instruction.
