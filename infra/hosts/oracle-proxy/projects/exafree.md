# ExaFree

## 1. Summary
- Project: ExaFree
- Host: `oracle-proxy`
- Purpose: Exa 相关账号注册 / 刷新 / 管理面板服务
- Runtime status: running
- Priority: Tier 2

## 2. Access / Entry Points
- Web UI / API: `http://158.178.236.241:7860`
- Local direct access: `http://127.0.0.1:7860`
- Health endpoint: `http://127.0.0.1:7860/health`
- Container name: `exafree`
- SSH jump: `ssh oracle-proxy`

## 3. Deployment Layout
- Repo root: `/root/ExaFree`
- Compose file: `/root/ExaFree/docker-compose.yml`
- Runtime env file: `/root/ExaFree/.env`
- Main config file: `/root/ExaFree/data/settings.yaml`
- Persistent data dir: `/root/ExaFree/data`
- SQLite DB: `/root/ExaFree/data/data.db`

## 4. Runtime Topology
- Host port: `7860/tcp`
- Container port: `7860/tcp`
- Main service container: `exafree`
- Current mail backend: private cfmail worker at `https://tmail.zhangxuemin.work`
- Current register proxy path: `proxy_for_auth` in `data/settings.yaml`

## 5. Current Confirmed Configuration
As of 2026-03-16 the following settings were verified on-host:

### Security / admin
- `.env` contains `ADMIN_KEY=Zxm971004`
- `docker-compose.yml` now correctly reads:
  - `ADMIN_KEY: "${ADMIN_KEY}"`
  - `SESSION_SECRET_KEY: "${SESSION_SECRET_KEY}"`
- Verified inside running container:
  - `ADMIN_KEY=Zxm971004`
  - `SESSION_SECRET_KEY` is set
- Health check: `GET /health` returned `200 OK` with `{"status":"ok"}`

### Registration / refresh cadence
- `basic.register_default_count: 5`
- `retry.scheduled_refresh_enabled: true`
- `retry.scheduled_refresh_cron: "*/180"`
- `retry.refresh_batch_size: 5`
- `retry.refresh_batch_interval_minutes: 36`

Operational interpretation:
- this is configured as an **approximate** cadence of one scheduled refresh wave every 3 hours
- each wave processes accounts in batches of 5
- if more than one batch is needed, batches are separated by ~36 minutes
- this should be treated as **roughly “3 小时 5 个”**, not a strict hard real-time guarantee

## 6. Operations

### Check status
```bash
ssh oracle-proxy
cd /root/ExaFree
docker compose ps
docker ps | grep exafree
curl http://127.0.0.1:7860/health
```

### Restart / recreate
```bash
ssh oracle-proxy
cd /root/ExaFree
docker compose up -d
```

### Follow logs
```bash
ssh oracle-proxy
docker logs -f exafree
```

### Verify admin env is wired correctly
```bash
ssh oracle-proxy
cd /root/ExaFree
docker exec exafree /bin/sh -lc 'echo "$ADMIN_KEY"; [ -n "$SESSION_SECRET_KEY" ] && echo session-set'
```

## 7. Failure Modes / Troubleshooting

### Symptom: service starts but logs say `未配置 ADMIN_KEY`
Likely causes:
- `docker-compose.yml` hardcoded placeholder / empty env instead of `${ADMIN_KEY}`
- `.env` missing `ADMIN_KEY`

Checks:
```bash
cd /root/ExaFree
sed -n '1,40p' .env
sed -n '1,60p' docker-compose.yml
docker logs --tail 100 exafree
```

### Symptom: scheduler cadence is not exactly “3 hours 5 accounts”
Expected behavior:
- ExaFree scheduler is timer/batch based, not a strict quota clock
- `*/180` + batch size `5` means approximately one 5-account wave every 3 hours
- if total candidate accounts exceed one batch, subsequent batches wait `36` minutes each

## 8. Dependencies / Cross-links
- Host docs: `../HOST.md`, `../PROJECTS.md`
- Related infra on same host: `./tavily-key-generator.md`, `./tavily-proxy.md`, `./cliproxy.md`

## 9. Change History
- 2026-03-16:
  - documented ExaFree deployment on `oracle-proxy`
  - set `.env` admin key to `Zxm971004`
  - fixed compose env wiring so container reads `ADMIN_KEY` / `SESSION_SECRET_KEY` from `.env`
  - verified running container exposes `ADMIN_KEY=Zxm971004`
  - set approximate scheduled cadence to one 5-account wave every 3 hours (`*/180`, batch size 5, inter-batch gap 36 minutes)
  - verified local health endpoint `/health` returned HTTP 200
