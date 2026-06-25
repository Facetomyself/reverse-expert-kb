# Kiro-RS

## Status
- Status: running
- Runtime root: `/root/containers/kiro-rs`
- Container: `kiro-rs`
- Image: `ghcr.io/hank9999/kiro-rs:latest`
- Origin bind: `127.0.0.1:18769 -> 8990/tcp`
- Public/direct entry: `https://kiro-rs.zhangxuemin.work/` (exact `/` redirects to `/admin`)
- Domestic/HK entry: `https://kiro-rs-cn.zhangxuemin.work/` (exact `/` redirects to `/admin` on HK edge, preserving the CN hostname)

## Purpose
Rust Anthropic-compatible Kiro API proxy with optional Admin UI and credential management. It is deployed side-by-side with the existing Kiro-Go service rather than replacing it.

## Runtime shape
- Docker Compose project under `/root/containers/kiro-rs`.
- Container listens on `0.0.0.0:8990` internally, but Docker publishes it only to source-host loopback `127.0.0.1:18769`.
- Source Caddy (`/root/containers/caddy-cpam/Caddyfile`) terminates TLS for `kiro-rs.zhangxuemin.work`, redirects exact `/` to `/admin`, and proxies the remaining traffic to the loopback origin.
- HK Caddy terminates TLS for `kiro-rs-cn.zhangxuemin.work`, redirects exact `/` to `/admin` locally so the CN hostname is preserved, and forwards the remaining traffic to the source HTTPS origin.

## Sensitive files
Do not copy values from these files into general docs or chat:
- `/root/containers/kiro-rs/config/config.json` — API key and Admin API key.
- `/root/containers/kiro-rs/config/credentials.json` — Kiro credentials; initialized as an empty array at deployment.
- `/root/containers/kiro-rs/deploy-secrets.txt` — deployment-time pointer/secrets note.

## Operational checks
```bash
ssh oracle-proxy 'docker ps --filter name=kiro-rs'
ssh oracle-proxy 'curl -H "x-api-key: $(python3 -c "import json;print(json.load(open(\"/root/containers/kiro-rs/config/config.json\"))[\"apiKey\"])" )" http://127.0.0.1:18769/v1/models'
```

Use the public routes for external smoke tests once DNS has propagated:
- `https://kiro-rs.zhangxuemin.work/admin`
- `https://kiro-rs-cn.zhangxuemin.work/admin`

## Deployment notes
- 2026-06-07: Initial deployment from `https://github.com/hank9999/kiro.rs` using the upstream GHCR image. Host had ~21G free on `/` before/after deployment and no space pressure. Local authenticated `/v1/models` and forced-resolution direct/CN HTTPS checks returned HTTP 200.
- 2026-06-08: User reported `https://kiro-rs-cn.zhangxuemin.work/` returned 404. Root cause: Kiro-RS app/admin UI only serves `/admin` and API paths, while exact root `/` was proxied through unchanged. Added exact-root `308` redirects to `/admin` on both source Caddy and HK edge Caddy. Verified `/` returns `308 Location: /admin`, `/admin` returns HTTP 200, and `/v1/models` still reaches the API and returns expected unauthenticated HTTP 401.
