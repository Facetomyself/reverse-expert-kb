# Oracle Allowlist Nightly Summary

- Time: 2026-06-15 03:00 Asia/Shanghai / 2026-06-14 19:00 UTC
- Scope: `oracle-open_claw` local maintenance plus remote checks for `oracle-proxy`, `oracle-gateway`, `oracle-mail`, `oracle-registry`, `oracle-reverse-dev` only.

## Local `oracle-open_claw`
- Root filesystem before cleanup: `45G total / 35G used / 11G free` (`77%`); after cleanup: `76%`. Pressure cleanup remained skipped because the host was below the configured pressure threshold.
- Memory: `5.8Gi` total, `4.4Gi` available; no swap.
- Safe stale cleanup removed `6053` old root-owned `/tmp` / cache-style entries, estimated `173,517,623` bytes; root filesystem availability increased by about `182,276,096` bytes.
- Local OpenClaw gateway process was present (`/usr/lib/node_modules/openclaw/dist/index.js gateway --port 18789`); Docker daemon/containerd were running; no local Docker workload containers were present.
- Detailed local maintenance output was compacted to avoid per-file deletion noise: `maintenance/nightly-system-checks/2026-06-15-030053.md`.

## Remote Allowlist
- `oracle-proxy`: reachable; root `42%`; memory comfortable (`8.3Gi` available); documented proxy/app containers remained up, including Tavily proxy, ExaFree, Grok2API, CLIProxy/backup, CPA/GPT/Kiro/Card services. Listener surface matched current broad proxy-host documentation.
- `oracle-gateway`: reachable; root `33%`; small-memory posture stable (`577Mi` available, light swap use); `derper`, `hysteria`, and helper `caddy` matched the documented gateway split (`80/443`, UDP `3478/443`, helper `8080/8443`).
- `oracle-mail`: reachable; root `59%`; memory comfortable (`4.1Gi` available); `outlook-email-plus-caddy` and healthy app remained up; public web listeners `80/443` present; no classic mail protocol listener revival observed.
- `oracle-registry` / `oracle-newapi-primary`: reachable; root `8%`; memory comfortable; `new-api` healthy on loopback `127.0.0.1:13000`; Caddy public `80/443` present; local HTTP header still reported `X-NewAPI-Role: primary`.
- `oracle-reverse-dev` / `oracle-newapi-standby`: reachable; root `25%`; memory comfortable; `new-api` healthy on loopback `127.0.0.1:13000`; local HTTP header still reported `X-NewAPI-Role: standby`. Previously documented `gpt-pp.service` remained active/enabled on loopback `127.0.0.1:8888`; no new drift identified.

## Writeback
- No `infra/` status/changelog writeback was made: the only meaningful new delta was safe local stale `/tmp` cleanup on `oracle-open_claw`; remote allowlist state remained consistent with the current documented posture and the previous `gpt-pp` observation.
- No remediation, service restarts, package updates, remote cleanup, or config changes were performed.
