# Oracle Allowlist Nightly Summary

- Time: 2026-06-12 03:00 Asia/Shanghai / 2026-06-11 19:00 UTC
- Scope: `oracle-open_claw` local maintenance plus remote checks for `oracle-proxy`, `oracle-gateway`, `oracle-mail`, `oracle-registry`, `oracle-reverse-dev` only.

## Local `oracle-open_claw`
- Root filesystem: `45G total / 35G used / 11G free` (`76%`); below pressure threshold.
- Memory: `5.8Gi` total, `4.6Gi` available; no swap.
- Existing local cleanup found no stale cache/tmp/log files to remove; pressure cleanup was skipped. The generated no-delta local report was removed to avoid placeholder noise.

## Remote Allowlist
- `oracle-proxy`: reachable; root `42%`; memory comfortable; documented proxy/app containers remained up, including `cliproxy`, `cliproxy-backup`, `grok2api`, `exafree`, Tavily proxy, CPA/GPT/Kiro/Card services; listener surface matched current broad proxy-host documentation.
- `oracle-gateway`: reachable and stable; root `33%`; small-memory posture remained stable; `derper`, `hysteria`, and helper `caddy` matched the documented gateway split.
- `oracle-mail`: reachable; root `59%`; memory comfortable; `outlook-email-plus-caddy` and healthy app remained up; public web listeners `80/443` present; no classic mail protocol listener revival observed.
- `oracle-registry` / `oracle-newapi-primary`: reachable; root `8%`; memory comfortable; `new-api` healthy on loopback `127.0.0.1:13000`; Caddy public `80/443` present for the New API role.
- `oracle-reverse-dev` / `oracle-newapi-standby`: reachable; root `25%`; memory comfortable; `new-api` healthy on loopback `127.0.0.1:13000`. Meaningful runtime delta found: enabled `gpt-pp.service` running from `/home/ubuntu/gpt-pp`, bound only to `127.0.0.1:8888`, active since 2026-06-10 06:47 UTC.

## Writeback
- Updated `infra/hosts/oracle-newapi-standby/CHANGELOG.md` with the `gpt-pp.service` observation.
- No remediation, service restarts, package updates, config changes, or remote cleanup were performed.
