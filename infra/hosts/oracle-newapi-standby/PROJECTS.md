# oracle-newapi-standby / PROJECTS

## Summary
`oracle-newapi-standby` now hosts Sub2API as its only active project deployment.

Former identities / compatibility aliases:
- `oracle-reverse-dev`
- formerly used as New API standby, retired on 2026-07-07 per user instruction

## Current project state
As of 2026-07-22 10:27 GMT+8:
- Sub2API is deployed under `/opt/sub2api` via Docker Compose.
- Active containers: `sub2api`, `sub2api-postgres`, `sub2api-redis`.
- Origin app listener: `127.0.0.1:18088 -> container:8080`.
- Caddy is active on `80/443` for `sub2api.zhangxuemin.work`.
- Domestic/CN entry is provided by `hk-relay` as `https://sub2api-cn.zhangxuemin.work`.
- `/home/ubuntu` remains cleaned to login/shell basics only (`.ssh`, shell rc/profile files).

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
