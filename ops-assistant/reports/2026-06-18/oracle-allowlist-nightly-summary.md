# Oracle Allowlist Nightly Summary

- Time: 2026-06-18 03:00 Asia/Shanghai / 2026-06-17 19:00 UTC
- Scope: `oracle-open_claw` local maintenance plus remote checks for `oracle-proxy`, `oracle-gateway`, `oracle-mail`, `oracle-registry`, `oracle-reverse-dev` only.

## Meaningful delta
- Local `oracle-open_claw` root usage is now `81%` (`45G` total / `36G` used / `9.0G` free), up from the recent `76%` nightly snapshot. This is still below the configured pressure-cleanup threshold (`>=85%` or `<=5GiB` free), so no pressure cleanup was triggered.
- Main contributors observed during this pass: `/var/log` at `4.1G`, mostly journal (`/var/log/journal` about `3.8G`), and workspace `.git` at about `5.0G`.

## Local `oracle-open_claw`
- Safe stale cleanup removed `23` old root-owned `/tmp` files, estimated `2,115,569` bytes; root usage remained `81%` after cleanup.
- Memory posture remained comfortable: `5.8Gi` total, about `4.2Gi` available; no swap.
- Docker and containerd were active. The OpenClaw gateway process was present on `--port 18789`, although no `openclaw.service` systemd unit was active.
- Detailed local maintenance output: `maintenance/nightly-system-checks/2026-06-18-030052.md`.

## Remote allowlist
- `oracle-proxy`: reachable; root `43%`; memory comfortable (`8.3Gi` available). Documented proxy/app containers remained up, including Tavily proxy, ExaFree, Grok2API, CLIProxy/backup, CPA/GPT/Kiro/Card services. Caddy owned public `80/443`; broad proxy-host listener posture matched current documentation.
- `oracle-gateway`: reachable; root `33%`; small-memory posture stable (`565Mi` available, light swap use). `derper`, UDP `hysteria`, helper Caddy `8080/8443`, and Docker `hysteria` container matched the documented gateway split.
- `oracle-mail`: reachable; root `59%`; memory comfortable (`4.0Gi` available). `outlook-email-plus-caddy`, healthy `outlook-email-plus-app`, and `wa-app` were up; public web listeners `80/443` present; no classic mail protocol listener revival observed.
- `oracle-registry` / `oracle-newapi-primary`: reachable; root `8%`; memory comfortable. `new-api` remained healthy on loopback `127.0.0.1:13000`; Caddy public `80/443` present; local HTTP headers reported `X-Newapi-Role: primary` and `X-New-Api-Version: v1.0.0-rc.10`.
- `oracle-reverse-dev` / `oracle-newapi-standby`: reachable; root `25%`; memory comfortable. `new-api` remained healthy on loopback `127.0.0.1:13000`; Caddy public `80` present; local HTTP headers reported `X-Newapi-Role: standby` and `X-New-Api-Version: v1.0.0-rc.10`.

## Writeback
- No `infra/` status/changelog writeback was made: remote allowlist state remained consistent with current documented posture, and the local disk increase is a caution rather than a reachability/lifecycle change.
- No remediation, service restarts, package updates, remote cleanup, or remote config changes were performed.
