# oracle-gateway / CHANGELOG

- 2026-04-04: A user-directed low-risk cleanup kept DERP as the primary public entrypoint and pruned the stale `/tmp-upload` block from `/etc/caddy/Caddyfile`. Caddy validation and reload succeeded afterward, leaving the host in the intended split shape: `derper` on public TCP `80/443`, `hysteria` on UDP `443`, and helper `caddy` only on local `8080/8443`.

- 2026-04-03: Deployed a custom Tailscale DERP server (`derper`) on `oracle-gateway` for `derp.zhangxuemin.work`.
  - DNS for `derp.zhangxuemin.work` was switched to direct origin resolution before cutover.
  - `derper` now owns public TCP `80/443` and UDP `3478`.
  - Hysteria remains on UDP `443`.
  - Host `caddy` was moved off public `80/443` and retained only on alternate local ports `8080/8443` so DERP could bind directly without HTTP-proxy interference.
  - Local and public validation both succeeded: DERP debug page rendered over HTTPS, and `systemd` now keeps `derper.service` running.
  - Same-day hardening follow-up aligned `derper` to the host's `tailscaled` version line (`1.96.4`) and enabled `-verify-clients`.
  - Documentation and directory layout were cleaned up so `oracle-gateway` is now the only active identity used for this host in `infra/`.

- 2026-03-25: Registry proxy live front door was migrated away to `oracle-registry`; old registry containers on this host were stopped and local Caddy front door for those domains was disabled, while rollback data under `/data/registry-proxy` was retained.
- 2026-03-25: Host role was repurposed into an Hysteria gateway/relay using `backup.zhangxuemin.work`.
- 2026-03-25: Deployed Hysteria 2 under `/opt/hysteria` with domain `backup.zhangxuemin.work`, ACME-issued certificate, password auth, Salamander obfuscation, and masquerade upstream `https://dreamhorse.eu.cc/`.
- 2026-03-25: Added a Clash Verge downloadable config endpoint at `https://backup.zhangxuemin.work/clash-verge.yaml` via host Caddy on TCP 443 while Hysteria continues to use UDP 443.
- 2026-03-25: Verified from `ali-cloud` using the official Hysteria client that the relay works end-to-end; client connected successfully and local SOCKS5 proxying returned external HTTP responses.
- 2026-03-25: Host identity was repurposed semantically into `oracle-gateway` as the focused gateway role replaced the old mixed docker/registry-proxy purpose.
- 2026-03-25: Per user direction, historical mixed runtime residue was cleaned up so this host can be observed as a focused gateway. Stopped legacy registry containers were removed.
- 2026-03-25: User then explicitly requested no archive retention; old registry files / Harbor residuals were permanently deleted instead of being kept under `/root/retired-services/`.
- 2026-03-26: Read-only health check reconfirmed `oracle-gateway` remains healthy in its narrowed gateway role. Snapshot at `2026-03-26 00:24 UTC`: uptime ~230 days, load low (`0.08 0.02 0.01`), root disk `45G total / 14G used / 32G free` (`31%` used), memory stable for host size (`952Mi` total, `553Mi` available) with light swap use (`88Mi / 2.0Gi`). Runtime matched expectation: host `caddy` active on TCP `80/443` with `caddy validate` returning `Valid configuration`, one `hysteria` container up on UDP `443`, SSH on `22`, and Tailscale still present on `100.116.171.76`.
- 2026-03-27: Temporarily enabled a browser-authenticated upload path at `https://backup.zhangxuemin.work/tmp-upload/` to receive Codex config files from a sender without SSH. Implementation used host Caddy `basic_auth` + reverse proxy and a localhost Python backend on `127.0.0.1:18081`, with uploaded files landing in `~/tmp-upload-drop`.
- 2026-03-27: After transfer, intentionally removed the public `/tmp-upload/` route, stopped the localhost backend, and restored `backup.zhangxuemin.work` to its baseline Hysteria/config-distribution-only Caddy shape. Reusable host-side notes/scripts were retained under `~/.tmp-upload-gateway/` for future short-lived re-enable if explicitly needed.
- 2026-03-28: Recurring read-only fleet check reconfirmed `oracle-gateway` remains reachable and healthy in its focused gateway role. Snapshot at `2026-03-28 07:29 UTC`: uptime ~233 days, load low (`0.12 0.10 0.04`), root disk `45G total / 14G used / 32G free` (`31%` used), memory still tight-but-stable for host size (`952Mi` total, `542Mi` available) with light swap use (`93Mi / 2.0Gi`), host `caddy` still owned public `80/443`, and the single `hysteria` container remained up on UDP `443`.
- 2026-03-28: One documentation-relevant delta only: the temporary upload route remained absent from the public listener surface as intended, but a localhost helper backend `python3` process was still bound on `127.0.0.1:18081`. This is now tracked as low-risk local residue rather than a renewed public exposure.
