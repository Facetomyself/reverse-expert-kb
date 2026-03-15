# Tavily Proxy

## 1. Summary
- Project: Tavily Proxy
- Host: `oracle-proxy`
- Purpose: 聚合 Tavily keys，对外提供统一 API 和 Web 管理后台
- Runtime status: running
- Priority: Tier 1

## 2. Access / Entry Points
- Web Console: `http://proxy.zhangxuemin.work:9874/`
- API Base: `http://proxy.zhangxuemin.work:9874/api`
- Local direct access: `http://127.0.0.1:9874`
- Host public IP path: `http://158.178.236.241:9874`
- Admin secret: see credential store / `.env` on host; do not depend on memory alone
- SSH jump: `ssh oracle-proxy`

## 3. Deployment Layout
- Repo root: `/root/tavily-key-generator`
- Proxy subdir: `/root/tavily-key-generator/proxy`
- Compose file: `/root/tavily-key-generator/proxy/docker-compose.yml`
- Env file: `/root/tavily-key-generator/proxy/.env`
- Data directory: `/root/tavily-key-generator/proxy/data`
- SQLite DB: `/root/tavily-key-generator/proxy/data/proxy.db`
- Container name: `proxy-tavily-proxy-1`

## 4. Runtime Topology
- Container port: `9874`
- Host port: `9874`
- Database: local SQLite bind-mounted from host
- Upstream: official Tavily API using pooled keys
- Downstream consumers:
  - local `search-layer`
  - any client using issued proxy tokens
  - Web admin console users

## 5. Purpose and Workflow
This service is the stable client-facing layer for Tavily usage on this infrastructure.

Workflow:
1. `tavily-key-generator` registers new Tavily accounts
2. generated keys are stored in `output/api_keys.md`
3. scheduler auto-uploads fresh keys into this proxy
4. proxy stores keys in `proxy.db`
5. clients use proxy-issued tokens instead of raw Tavily keys
6. proxy fans requests out to pooled underlying Tavily keys

## 6. Configuration
Important config files:
- `/root/tavily-key-generator/proxy/docker-compose.yml`
- `/root/tavily-key-generator/proxy/.env`

Important settings:
- `ADMIN_PASSWORD` comes from `.env`
- port mapping: `9874:9874`
- persistent storage: `./data:/app/data`

Key config rule:
- **Do not hardcode the admin password in compose**. This was previously a real footgun and was corrected.

## 7. Operations

### Check status
```bash
ssh oracle-proxy
cd /root/tavily-key-generator/proxy
docker compose ps
docker ps | grep tavily-proxy
ss -ltnp | grep 9874
```

### Start
```bash
ssh oracle-proxy
cd /root/tavily-key-generator/proxy
docker compose up -d
```

### Rebuild / restart
```bash
ssh oracle-proxy
cd /root/tavily-key-generator/proxy
docker compose up -d --build --force-recreate
```

### Stop
```bash
ssh oracle-proxy
cd /root/tavily-key-generator/proxy
docker compose down
```

### Logs
```bash
ssh oracle-proxy
docker logs -f proxy-tavily-proxy-1
```

## 8. Health Checks
Expected healthy signs:
- container `proxy-tavily-proxy-1` is `Up`
- `ss -ltnp | grep 9874` shows docker-proxy listener
- authenticated `GET /api/stats` returns HTTP 200
- Web console loads in browser
- key pool is non-empty

Example local check on host:
```bash
curl -H 'X-Admin-Password: <admin-password>' http://127.0.0.1:9874/api/stats
```

## 9. Data and Persistence
- Persistent DB: `/root/tavily-key-generator/proxy/data/proxy.db`
- Password/config source: `/root/tavily-key-generator/proxy/.env`
- Container recreation should not destroy data as long as `data/` is preserved

Recommended backup targets:
- `/root/tavily-key-generator/proxy/data/`
- `/root/tavily-key-generator/proxy/.env`

## 10. Common Tasks

### View key pool summary
```bash
curl -H 'X-Admin-Password: <admin-password>' http://127.0.0.1:9874/api/stats
```

### Create a client token
```bash
curl -X POST http://127.0.0.1:9874/api/tokens \
  -H 'Content-Type: application/json' \
  -H 'X-Admin-Password: <admin-password>' \
  -d '{"name":"client-name"}'
```

### Test a token with search
```bash
curl -X POST http://127.0.0.1:9874/api/search \
  -H 'Content-Type: application/json' \
  -d '{"query":"OpenClaw","api_key":"<proxy-token>"}'
```

### Import historical keys in bulk
Use the Web UI import box or POST the contents of `output/api_keys.md` to `/api/keys` with admin auth.

## 11. Failure Modes / Troubleshooting

### Symptom: Web UI opens but password is rejected
Likely causes:
- `.env` password changed but container not recreated
- compose accidentally hardcoded an old password

Fix path:
1. inspect `/root/tavily-key-generator/proxy/.env`
2. confirm compose uses `${ADMIN_PASSWORD}`
3. run `docker compose up -d --force-recreate`

### Symptom: key pool is empty
Likely causes:
- historical keys were never imported
- generator auto-upload is disabled or broken

Checks:
- inspect generator `config.py`
- inspect `/api/stats`
- verify `output/api_keys.md` has data

### Symptom: service is listening but API behaves oddly
Checks:
- `docker logs -f proxy-tavily-proxy-1`
- verify `proxy.db` exists and is writable
- verify admin auth works against `/api/stats`

## 12. Dependencies / Cross-links
- Depends on: `./tavily-key-generator.md`
- Related host docs:
  - `../HOST.md`
  - `../NETWORK.md`
  - `../PROJECTS.md`

## 13. Change History
- 2026-03-15:
  - deployed and verified on port 9874
  - changed compose to read `ADMIN_PASSWORD` from `.env`
  - verified `/api/search` with a generated proxy token
  - confirmed local search-layer can use this proxy as Tavily backend
