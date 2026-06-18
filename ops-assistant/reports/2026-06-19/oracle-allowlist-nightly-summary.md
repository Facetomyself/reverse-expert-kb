# Oracle Allowlist Nightly Summary

- Time: 2026-06-19 03:00 Asia/Shanghai / 2026-06-18 19:00 UTC
- Scope: `oracle-open_claw` local maintenance plus remote checks for `oracle-proxy`, `oracle-gateway`, `oracle-mail`, `oracle-registry`, `oracle-reverse-dev` only.

## Meaningful delta
- Local `oracle-open_claw` still has elevated-but-below-threshold root usage at `81%` (`45G` total / `37G` used / `9.0G` free). Pressure cleanup was not triggered because the configured threshold is `>=85%` or `<=5GiB` free.
- Local inspection found a public listener `0.0.0.0:18784` owned by `python3 -m http.server 18784 --bind 0.0.0.0`, started `2026-06-17 15:28`, with cwd `/root/.openclaw/workspace/tmp/astrbot-upgrade (deleted)`. This looks like stale temporary HTTP server residue and was not remediated during this read-only/no-remediation nightly pass.

## Local `oracle-open_claw`
- Safe stale cleanup removed only two old root-owned `/tmp` files (`/tmp/fix_textdrop.py`, `/tmp/install_textdrop.py`, ~5.7 KiB total); no material disk change.
- Memory posture remained comfortable: `5.8Gi` total, about `4.2Gi` available; no swap.
- Docker had no running containers. OpenClaw/node process remained present on local `127.0.0.1:18789`.
- Workspace `.git` remains a major local storage contributor at about `5.0G`; `/var/log` remains about `4.2G`.

## Remote allowlist
- `oracle-proxy`: reachable; root `43%` (`45G` total / `20G` used / `26G` free); memory comfortable (`8.3Gi` available). Documented proxy/app containers remained up, including Tavily proxy, ExaFree, Grok2API, CLIProxy/backup, CPA/GPT/Kiro/Card services. Fail2ban active; broad proxy-host listener posture remained consistent with current documentation.
- `oracle-gateway`: reachable; root `34%` (`45G` total / `15G` used / `31G` free); small-memory posture stable (`575Mi` available, light swap use). Docker `hysteria` container, `derper`, Caddy helper ports, and public gateway listeners matched the documented gateway split.
- `oracle-mail`: reachable; root `59%` (`36G` total / `21G` used / `15G` free); memory comfortable (`4.0Gi` available). `outlook-email-plus-caddy`, healthy `outlook-email-plus-app`, and `wa-app` were up; public web listeners `80/443` present; no classic mail protocol listener revival observed.
- `oracle-registry` / `oracle-newapi-primary`: reachable; root `8%` (`96G` total / `7.7G` used / `89G` free); memory comfortable. `new-api` remained healthy on loopback `127.0.0.1:13000`; local HTTP check returned `200 OK` and `X-New-Api-Version: v1.0.0-rc.10`.
- `oracle-reverse-dev` / `oracle-newapi-standby`: reachable; root `25%` (`96G` total / `24G` used / `73G` free); memory comfortable. `new-api` remained healthy on loopback `127.0.0.1:13000`; local HTTP check returned `200 OK` and `X-New-Api-Version: v1.0.0-rc.10`.

## Writeback
- No `infra/` status/changelog writeback was made: remote allowlist state remained consistent with current documented posture, and the local stale temporary HTTP server is a local cleanup/remediation decision rather than an infra reachability/lifecycle change.
- No service restarts, package updates, remote cleanup, remote config changes, or local process remediation were performed.
