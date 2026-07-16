# CPA Manager Plus

## 1. Summary
- Project: CPA Manager Plus
- Host: `oracle-proxy`
- Purpose: Web 管理面板 + Manager Server，用于管理本机 `cliproxy` / CLI Proxy API 并持久化请求统计
- Runtime status: running
- Priority: Tier 2

## 2. Entry Points
- Global/direct entry: `https://cpam.zhangxuemin.work/management.html`
- Domestic/HK-optimized entry: `https://cpam-cn.zhangxuemin.work/management.html`
- Local container port: `18317`
- Internal upstream CPA URL used by Manager Server: `http://host.docker.internal:8317`

Topology:

```text
Browser -> cpam.zhangxuemin.work -> oracle-proxy:caddy-cpam -> 127.0.0.1:18317 -> CPA Manager Plus -> host.docker.internal:8317 -> cliproxy
Browser -> cpam-cn.zhangxuemin.work -> hk-relay Caddy -> https://cpam.zhangxuemin.work -> same Manager Server
```

## 3. Deployment Layout
- Compose directory: `/root/containers/cpa-manager-plus`
- Compose file: `/root/containers/cpa-manager-plus/docker-compose.yml`
- Secret env file: `/root/containers/cpa-manager-plus/.env` (`0600`; contains admin key, data key, and CPA Management Key)
- Image: `ghcr.io/seakee/cpa-manager-plus:latest` (updated from `v0.7.0-beta` on 2026-06-06; checked in unified CPA stack updates)
- Container name: `cpa-manager-plus`
- Docker volume: `cpa-manager-plus_cpa-manager-plus-data`
- Volume mountpoint observed at deployment: `/var/lib/docker/volumes/cpa-manager-plus_cpa-manager-plus-data/_data`
- SQLite database inside container: `/data/usage.sqlite`

## 4. TLS / Front Door
Because `oracle-proxy` already has `1panel` owning public port `80`, the direct HTTPS front door uses a dedicated host-network Caddy container instead of native Caddy/system nginx.

- Compose directory: `/root/containers/caddy-cpam`
- Caddyfile: `/root/containers/caddy-cpam/Caddyfile`
- Image: `caddy:2.8.4-alpine`
- Container name: `caddy-cpam`
- Network mode: `host`
- Public listener: `*:443`
- Site: `cpam.zhangxuemin.work` -> `127.0.0.1:18317`

Notes:
- `1panel` still owns `0.0.0.0:80`; this caused Caddy HTTP-01 ACME to fail, but TLS-ALPN-01 on `443` succeeded.
- Do not assume native `caddy` exists on this host; the active CPAM front door is containerized.

## 5. Manager Configuration
- `CPA_UPSTREAM_URL=http://host.docker.internal:8317`
- `USAGE_COLLECTOR_MODE=http` to avoid RESP/pubsub ambiguity through reverse-proxy-style paths and use CPA HTTP usage queue
- `USAGE_POLL_INTERVAL_MS=500`
- `USAGE_DB_PATH=/data/usage.sqlite`
- CPA Management Key is sourced from the existing `cliproxy` management password and stored only in `/root/containers/cpa-manager-plus/.env`.

Security notes:
- Do not copy `.env` contents into docs or chat.
- The admin key is explicit in `.env`; use it for panel login. Current requested value is documented as a known operational password pattern, but the full secret must stay only on-host in `/root/containers/cpa-manager-plus/.env`.
- `/data` contains usage metadata and encrypted manager config; treat the Docker volume as sensitive operational data.

## 6. Operations

### Status
```bash
ssh oracle-proxy
cd /root/containers/cpa-manager-plus
docker compose ps
docker logs --tail 100 cpa-manager-plus
```

### Front-door status
```bash
ssh oracle-proxy
cd /root/containers/caddy-cpam
docker compose ps
docker logs --tail 100 caddy-cpam
```

### Health checks
```bash
curl -sS https://cpam.zhangxuemin.work/usage-service/info
curl -sS -o /dev/null -w '%{http_code}\n' https://cpam.zhangxuemin.work/management.html
curl -sS -o /dev/null -w '%{http_code}\n' https://cpam-cn.zhangxuemin.work/management.html
```

### Update helpers
```bash
ssh oracle-proxy
/root/update_cpa_stack.sh
```

The stack wrapper updates primary `cliproxy`, backup `cliproxy-backup`, and `cpa-manager-plus` as one batch. Use the service-specific implementation helper under `/root/lib/cpa-stack/` only for targeted maintenance:

```bash
ssh oracle-proxy
/root/lib/cpa-stack/update_cpa_manager_plus.sh
```

Force recreate even when the pulled `latest` image ID is unchanged:

```bash
ssh oracle-proxy
/root/update_cpa_manager_plus.sh --force-recreate
```

The helper defaults to `ghcr.io/seakee/cpa-manager-plus:latest`, supports temporary override via `CPA_MANAGER_PLUS_IMAGE=...`, and compares the running container's immutable image SHA against the pulled target image ID. It recreates through Docker Compose, then checks container health plus local `/management.html`, `/health`, and `/usage-service/info` HTTP 200 responses. It also checks both public panel entrypoints, `https://cpam.zhangxuemin.work/management.html` and `https://cpam-cn.zhangxuemin.work/management.html`, so the HK/CN edge path is validated together with the source host. If startup or health checks fail, it attempts rollback to the previous running image SHA while preserving the existing Docker volume.

Expected signs:
- `cpa-manager-plus` container healthy
- `caddy-cpam` container up
- direct and CN management pages return HTTP `200`
- `/usage-service/info` reports `service=cpa-manager-plus`, `configured=true`, `adminReady=true`, `setupRequired=false`

## 7. DNS / Edge
Cloudflare DNS records created on 2026-05-30:
- `cpam.zhangxuemin.work` -> `158.178.236.241` (`oracle-proxy`)
- `cpam-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay`)

HK edge Caddy site on `hk-relay`:
- `cpam-cn.zhangxuemin.work` -> `https://cpam.zhangxuemin.work`
- Host header and TLS SNI are set to `cpam.zhangxuemin.work`.

## 8. Change History
- 2026-07-10: Added unified `/root/update_cpa_stack.sh` on `oracle-proxy` and changed the daily cron to update primary CLIProxy, backup CLIProxy, and CPA Manager Plus together at `06:30`. CPA Manager Plus image was already current (`ghcr.io/seakee/cpa-manager-plus:latest`, `sha256:3ac2ab1af87873de1e4b9164f64f92552798f60ad24bc30ffedfab354448ae83`), while the two CLIProxy pools were aligned to the same latest image. Verified direct and HK/CN management pages returned HTTP 200.
- 2026-06-17: Forced Plus manager upgrade with `/root/update_cpa_manager_plus.sh --force-recreate`; `docker pull` downloaded a newer `ghcr.io/seakee/cpa-manager-plus:latest` image `sha256:064beb4c...` (digest `sha256:194bafe7...`). The recreated container became healthy, and both public panel entrypoints `cpam` and `cpam-cn` returned HTTP 200. The helper now treats both public panel URLs as post-update health checks.
- 2026-06-17: Added `/root/update_cpa_manager_plus.sh` for the Plus manager service. The helper uses the same immutable running-image-SHA comparison pattern as the fixed primary CPA helper, so mutable `latest` tags do not hide a stale running container. Dry-run verified current Plus was already on image `sha256:4f4a2919...`; local `/management.html`, `/health`, and `/usage-service/info` checks returned HTTP 200.
- 2026-05-30: Deployed CPA Manager Plus v0.7.0-beta on `oracle-proxy`; added direct `cpam` and HK/CN `cpam-cn` entrypoints; verified both returned HTTP 200 for `/management.html`.
- 2026-05-30: Updated `CPA_MANAGER_ADMIN_KEY` in `/root/containers/cpa-manager-plus/.env` per user request and recreated the container; `/usage-service/info` still reported `configured=true`, `adminReady=true`, `setupRequired=false`.
- 2026-06-06: Updated deployment from `ghcr.io/seakee/cpa-manager-plus:v0.7.0-beta` to `ghcr.io/seakee/cpa-manager-plus:latest` (`after_image_id=sha256:4f4a29195eea7bc7dd095c254fe664ca3f69ff2be1bbefa0a9b97aefee2d3ceb`). Pre-update backup stored on `oracle-proxy` at `/root/containers/cpa-manager-plus-backup-20260606-051247`. Verified container health plus direct and HK/CN management URLs returning HTTP 200.
