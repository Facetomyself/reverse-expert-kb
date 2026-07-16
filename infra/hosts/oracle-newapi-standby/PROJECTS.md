# oracle-newapi-standby / PROJECTS

## Summary
`oracle-newapi-standby` currently has no active project deployment.

Former identities / compatibility aliases:
- `oracle-reverse-dev`
- formerly used as New API standby, retired on 2026-07-07 per user instruction

## Current project state
As of 2026-07-07 17:06 GMT+8 cleanup:
- no Docker containers
- no Docker images
- no Docker volumes
- no Docker build cache
- `/opt/new-api` removed
- `/opt/new-api-docs` removed
- Caddy stopped and disabled; `/etc/caddy/Caddyfile` intentionally emptied
- `/home/ubuntu` cleaned to login/shell basics only (`.ssh`, shell rc/profile files)

## Operational baseline
```bash
ssh oracle-newapi-standby
docker ps -a
docker images
docker volume ls
docker system df
ss -ltnp
```

Expected public project listeners after cleanup:
- none

Expected remaining listeners:
- `22/tcp` SSH
- system/local control listeners such as DNS stub and rpcbind may remain

## Retired project groups
- Former New API standby deployment under `/opt/new-api`, including static docs under `/opt/new-api-docs`, was removed on 2026-07-07.
- Former `aBaiAutoplus` and `GPT-FULL-REGIST-AND-PAYMENT-FLOW` runtime/source payloads were retired on 2026-06-08.
- Older reverse/dev/MCP/Grok user-home residue was removed from `/home/ubuntu` on 2026-07-07.
