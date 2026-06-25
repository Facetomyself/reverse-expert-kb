# Oracle allowlist nightly summary

- Run time: 2026-04-15 03:04 Asia/Shanghai / 2026-04-14 19:04 UTC
- Scope held strictly to:
  - local: `oracle-open_claw`
  - remote: `oracle-proxy`, `oracle-gateway`, `oracle-mail`, `oracle-registry`, `oracle-reverse-dev`
- Explicit exclusions honored: `ali-cloud`, `self-server`, `home`, `company`, `home-macmini`, `home-nas`

## Meaningful findings

- `oracle-open_claw`
  - Local maintenance completed safely.
  - Host stayed healthy: root fs `57%` used with ~`20G` free, memory comfortable (`5.8Gi` total / `4.5Gi` available), OpenClaw gateway OK, `docker` / `cron` / `ssh` active.
  - Routine temp/cache cleanup removed ~`36.9 MB` of stale artifacts and freed ~`47.4 MB`; no pressure cleanup was needed.

- `oracle-proxy`
  - Core proxy stack remained healthy: `exafree` and `grok2api` both returned HTTP `200`; expected containers/listeners were present.
  - Meaningful delta: host uptime dropped to ~`1 day 20 hours` versus the previous nightly snapshot. Remote `last -x` shows a host reboot at `2026-04-12 22:40` local time. Services recovered cleanly after that reboot.

- `oracle-gateway`
  - Core gateway runtime remained healthy: `derper` active, `caddy` active, `hysteria` container up, expected listener split on `80/443/3478/8080/8443/18733/18081/2019` still present.
  - Meaningful delta: the previously documented Tailscale presence is currently absent. This host now has no `tailscaled.service`, no `tailscale`/`tailscaled` binary in `PATH`, and no tailnet IP available from the inspected runtime.

- `oracle-mail`
  - No meaningful delta. `outlook-email-plus-caddy` and healthy `outlook-email-plus-app` remained up; public `80/443` still present.

- `oracle-registry`
  - No meaningful delta. `/usr/local/bin/check-registry-proxies` passed local backend checks and public `/v2/` checks for `hub`, `ghcr`, `k8s`, and `mcr`; `caddy` active; expected four registry containers still running.

- `oracle-reverse-dev`
  - Meaningful drift remains present. Listener surface is not currently SSH-only:
    - `*:18080` -> `python3 /home/ubuntu/.tmp-upload-service/server.py` (started `2026-03-27`, cwd `/home/ubuntu`)
    - `*:631` -> `cupsd`
    - `*:111` -> `rpcbind`
  - Host was otherwise lightly loaded and resource-healthy.

## Write-back posture

- Per low-noise policy, no routine infra/changelog write-back was done for unchanged hosts.
- This concise summary file was kept because the run found meaningful delta/drift (`oracle-proxy` reboot, `oracle-gateway` tailnet absence, `oracle-reverse-dev` exposed drift listeners).
