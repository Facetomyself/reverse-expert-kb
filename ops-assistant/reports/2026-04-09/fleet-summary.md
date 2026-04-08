# Fleet Summary

## Scope enforced
- local maintenance target: `oracle-open_claw`
- remote Oracle hosts inspected: `oracle-proxy`, `oracle-gateway`, `oracle-mail`, `oracle-registry`, `oracle-reverse-dev`
- explicitly excluded and not inspected: `ali-cloud`, `self-server`, `home`, `company`, `home-macmini`, `home-nas`

## Meaningful deltas

### oracle-open_claw
- Safe local nightly maintenance completed via the existing nightly cleanup logic, with report output intentionally kept ephemeral in `/tmp` to avoid routine workspace noise.
- Cleanup removed:
  - `ops-assistant/checks/__pycache__`
  - a large set of stale `/tmp/node-compile-cache/...` files
- Cleanup summary:
  - removed items: `1764`
  - estimated removed bytes: `4178689`
  - root/workspace free-space gain observed by `df`: `10170368` bytes
- No storage-pressure mode was needed: root stayed at `54%` used with ~`21G` free.
- Local health remained comfortable: memory available ~`4.5Gi`, OpenClaw gateway healthy on loopback `127.0.0.1:18789`, and no local service-health issue required action.

### oracle-proxy
- Host remained reachable and operationally healthy: root disk `51%` used, memory posture still comfortable, and the expected public/runtime surfaces were still present (`80`, `7860`, `8000`, `8317`, `9874`, `15072`, documented sing-box/xray ports).
- One doc-drift candidate was confirmed during this pass: an additional long-lived internal-only compose sidecar container exists under the `grok2api` project:
  - container: `grok2api-camoufox-solver`
  - compose service: `camoufox-solver`
  - image: `grok2api-official-local:latest`
  - observed state: running since `2026-03-26T05:28:16Z`
- Important boundary note: this sidecar did **not** introduce a new public listener in this pass; it exposed only internal container port metadata (`8000/tcp`) in `docker inspect`.

## Stable / no-new-action hosts
- `oracle-gateway`: still matched the documented gateway shape, including `derper` on public TCP `80/443` + UDP `3478`, `hysteria` on UDP `443`, helper `caddy` on local `8080/8443`, and the already-documented temporary `:18733` distribution endpoint.
- `oracle-mail`: still matched the currently documented web-app role; `outlook-email-plus-caddy` and `outlook-email-plus-app` remained up, public `80/443` stayed present, and the previously documented `*:9527` `r_client` residue was still present.
- `oracle-registry`: remained healthy and consistent with docs; public `80/443` plus backend listeners `51000/52000/55000/57000` were present, and the four expected registry containers remained running.
- `oracle-reverse-dev`: remained healthy and intentionally light; no long-lived containers, previously documented public listeners `:18080` and `:631` remained present, and local-only Chromium debug listeners `127.0.0.1:9222/:9223/:9224` were still live.

## Write-back decision
- No `infra/` host docs or changelogs were updated in this pass.
- Reason: the remote fleet mostly matched existing documentation, and the only remote drift (`oracle-proxy` internal sidecar) did not justify nightly `infra/` churn on top of the already-dirty repos.
- This report is the only durable artifact intentionally created for the nightly Oracle-scoped pass.
