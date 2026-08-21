# oracle-newapi-standby / PROJECTS

## Summary
`oracle-newapi-standby` now hosts Sub2API and PoolX (proxy pool control panel) as its active project deployments.

Former identities / compatibility aliases:
- `oracle-reverse-dev`
- formerly used as New API standby, retired on 2026-07-07 per user instruction

## Current project state
As of 2026-07-22 10:27 GMT+8 (Sub2API):
- Sub2API is deployed under `/opt/sub2api` via Docker Compose.
- Active containers: `sub2api`, `sub2api-postgres`, `sub2api-redis`.
- Origin app listener: `127.0.0.1:18088 -> container:8080`.
- Caddy is active on `80/443` for `sub2api.zhangxuemin.work`.
- Domestic/CN entry is provided by `hk-relay` as `https://sub2api-cn.zhangxuemin.work`.
- `/home/ubuntu` remains cleaned to login/shell basics only (`.ssh`, shell rc/profile files).

As of 2026-08-08 (PoolX): see PoolX section above.

## PoolX project state (2026-08-08, updated 2026-08-21)
- PoolX (`ghcr.io/rain-kl/poolx:latest`, supports linux/arm64) deployed under `/opt/poolx` via Docker Compose.
- Container: `poolx-poolx-1`, healthy, currently rebuilt from local image `poolx-local:latest` because upstream `ghcr.io/rain-kl/poolx:latest` lagged the mihomo path fix.
- Origin app listener: `127.0.0.1:18089 -> container:8000` (loopback Docker publish, avoids Sub2API's `18088`).
- Data dir `/opt/poolx/data` is owned by uid/gid `10001` (container `foam` user) — required or SQLite fails with "unable to open database file: out of memory (14)".
- Secrets live in `/opt/poolx/.env` (JWT secret, credential encryption key, bootstrap admin).
- Bootstrap admin: `admin` / user-specified default password (rotate after first login per upstream warning).
- compose gotcha fixed: upstream `docker-compose.yml` hardcodes `FOAM_BOOTSTRAP_ADMIN_PASSWORD: "12345678"`; changed to `"${FOAM_BOOTSTRAP_ADMIN_PASSWORD:-Zxm971004}"` so `.env` controls the bootstrap password. Keep this patch on upgrade.
- kernel download /测速 gotcha (2026-08-21): upstream image had the Mihomo path regression for node tests, surfacing as `未找到 Mihomo 二进制文件: mihomo`. Fixed by building `poolx-local:latest` from the current checkout and keeping `FOAM_CLASH_MIHOMO_BINARY_PATH: "/app/data/core/mihomo"` in compose. Verified real `/api/v1/admin/clash/nodes/test` succeeds after rebuild.
- Caddy on standby serves `poolx.zhangxuemin.work` -> `127.0.0.1:18089`.
- Domestic/CN entry: `https://poolx-cn.zhangxuemin.work` via `hk-relay` Caddy -> `https://poolx.zhangxuemin.work`.
- Validation: global + CN HTTPS 200; admin login OK through both entries; node test returned success after the rebuild.

## Operational baseline
```bash
ssh oracle-newapi-standby
docker ps -a
docker images
docker volume ls
docker system df
ss -ltnp
```

Expected public project listeners:
- `80/tcp` Caddy HTTP redirect / ACME
- `443/tcp` Caddy HTTPS

Expected remaining listeners:
- `22/tcp` SSH
- `127.0.0.1:18088/tcp` Sub2API origin app
- system/local control listeners such as DNS stub and rpcbind may remain

## Active projects
| Project | Status | Entry | Notes | Details |
|---|---|---|---|---|
| Sub2API | running | `sub2api.zhangxuemin.work` / `sub2api-cn.zhangxuemin.work` | AI API gateway platform backed by PostgreSQL and Redis | `./projects/sub2api.md` |

## Retired project groups
- Former New API standby deployment under `/opt/new-api`, including static docs under `/opt/new-api-docs`, was removed on 2026-07-07.
- Former `aBaiAutoplus` and `GPT-FULL-REGIST-AND-PAYMENT-FLOW` runtime/source payloads were retired on 2026-06-08.
- Older reverse/dev/MCP/Grok user-home residue was removed from `/home/ubuntu` on 2026-07-07.
