# Oracle allowlist nightly summary

- Run time: 2026-05-04 03:03 Asia/Shanghai / 2026-05-03 19:03 UTC
- Scope held strictly to:
  - local: `oracle-open_claw`
  - remote: `oracle-proxy`, `oracle-gateway`, `oracle-mail`, `oracle-registry`, `oracle-reverse-dev`
- Explicit exclusions honored: `ali-cloud`, `self-server`, `home`, `company`, `home-macmini`, `home-nas`

## Meaningful findings

- `oracle-open_claw`
  - Local maintenance script completed safely.
  - Root filesystem stayed stable at `69%` used with ~`15G` free; memory was comfortable after the run (`5.8Gi` total / ~`4.0Gi` available).
  - No stale cache/temp/log removals were needed; pressure cleanup was skipped.
  - Core local runtime posture was acceptable: `docker`, `cron`, `ssh`, and `nginx` were active; OpenClaw gateway was present as a process rather than a systemd unit.

- `oracle-proxy`
  - Healthy / no new action needed. Root fs `51%` used with ~`23G` free; memory comfortable (`11Gi` total / ~`9.5Gi` available).
  - Expected proxy/application containers remained up: `cliproxy`, `grok2api`, `grok2api-camoufox-solver`, `exafree`, `proxy-tavily-proxy-1`, `grok-register-camoufox`, and `grok-register-camoufox-adapter`.
  - Local health probes returned `exafree=200`, `grok2api=307`, `tavily=200`, and host `:80=200`.

- `oracle-gateway`
  - Healthy with the known small-memory caution. Root fs `33%` used with ~`31G` free; memory available ~`538Mi`, swap use ~`111Mi / 2.0Gi`.
  - Expected gateway runtime remained present: `hysteria` container, host `derper`, host `caddy`, and the documented listener split on `80/443/3478/8080/8443/18733/18081/2019`.

- `oracle-mail`
  - Healthy / no meaningful drift. Root fs `58%` used with ~`15G` free; memory comfortable (`5.5Gi` total / ~`4.1Gi` available).
  - `outlook-email-plus-caddy` and healthy `outlook-email-plus-app` remained up; public `80/443` remained present.

- `oracle-registry`
  - Meaningful delta: host rebooted on `2026-05-02 21:26 UTC` into kernel `6.17.0-1011-oracle`; uptime at check time was ~`21h36m`.
  - Services recovered cleanly: four registry containers were up, `caddy` active, root fs only `8%` used with ~`90G` free, memory comfortable.
  - `/usr/local/bin/check-registry-proxies` passed local backend checks and public `/v2/` checks for `hub`, `ghcr`, `k8s`, and `mcr`.

- `oracle-reverse-dev`
  - Meaningful delta: host rebooted on `2026-05-02 21:36 UTC` into kernel `6.17.0-1011-oracle`; uptime at check time was ~`21h26m`.
  - The previously observed public temporary upload listener on `:18080` was no longer present.
  - Remaining listener drift is now limited to the already-known `rpcbind` (`:111`) and snap CUPS (`:631`) exposure in addition to SSH; no Docker containers were running.
  - Resource posture was healthy: root fs `11%` used with ~`86G` free; memory comfortable.

## Write-back posture

- This report was kept because there was meaningful operational delta: `oracle-registry` / `oracle-reverse-dev` rebooted into the newer Oracle kernel, and `oracle-reverse-dev` no longer exposes the previously observed temporary upload listener on `:18080`.
- No remediation or remote mutation was performed.
- No infra source-of-truth files were edited in this pass; the existing `infra/` working tree already had unrelated pending changes, so this run avoided mixing new documentation edits into that dirty state.
