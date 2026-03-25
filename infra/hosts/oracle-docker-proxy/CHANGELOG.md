# oracle-docker-proxy / CHANGELOG

- 2026-03-25: Registry proxy live front door was migrated away to `oracle-new1`; old registry containers on this host were stopped and local Caddy front door for those domains was disabled, while rollback data under `/data/registry-proxy` was retained.
- 2026-03-25: Host role was repurposed into an Hysteria gateway/relay using `backup.zhangxuemin.work`.
- 2026-03-25: Deployed Hysteria 2 under `/opt/hysteria` with domain `backup.zhangxuemin.work`, ACME-issued certificate, password auth, Salamander obfuscation, and masquerade upstream `https://dreamhorse.eu.cc/`.
- 2026-03-25: Added a Clash Verge downloadable config endpoint at `https://backup.zhangxuemin.work/clash-verge.yaml` via host Caddy on TCP 443 while Hysteria continues to use UDP 443.
- 2026-03-25: Verified from `ali-cloud` using the official Hysteria client that the relay works end-to-end; client connected successfully and local SOCKS5 proxying returned external HTTP responses.
- 2026-03-25: SSH alias naming was updated semantically: live alias is now `oracle-gateway`, while `oracle-registry-legacy` and `oracle-docker_proxy` remain as compatibility aliases.
- 2026-03-25: Per user direction, historical mixed runtime residue was cleaned up so this host can be observed as a focused gateway. Stopped legacy registry containers were removed.
- 2026-03-25: User then explicitly requested no archive retention; old registry files / Harbor residuals were permanently deleted instead of being kept under `/root/retired-services/`.
