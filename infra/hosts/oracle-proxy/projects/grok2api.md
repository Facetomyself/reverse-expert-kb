# Grok2API

## 1. Summary
- Project: grok2api
- Host: `oracle-proxy`
- Purpose: 将 Grok 服务暴露为 API bridge / local service
- Runtime status: running
- Priority: Tier 2

## 2. Access / Entry Points
- Local repo path: `/root/grok2api`
- Compose file: `/root/grok2api/docker-compose.yml`
- Exposed port: `8000`
- Running container: `grok2api`

## 3. Deployment Layout
Observed repo structure includes:
- `Dockerfile`
- `docker-compose.yml`
- `config.defaults.toml`
- `data/`
- `logs/`
- application source under `app/` and `src/`

Compose file path:
- `/root/grok2api/docker-compose.yml`

## 4. Runtime Topology
- Host exposure: `0.0.0.0:8000 -> 8000/tcp`
- Container image default: `ghcr.io/tqzhr/grok2api:latest`
- Running image observed: `grok2api-official-local:latest`
- Healthcheck: internal `GET /health`
- Container mounts:
  - `./data:/app/data`
  - `./logs:/app/logs`
  - `./camoufox_override:/app/camoufox_override:ro`
- Likely acts as the backend behind `http://proxy.zhangxuemin.work:8000/v1` used elsewhere on this infrastructure

## 5. Purpose and Workflow
Known from surrounding infrastructure usage:
- local tools and proxies on this host use a Grok/OpenAI-compatible API path via port `8000`
- this project appears to be the local Grok API service backing that path
- it supports local storage mode by default and can optionally use redis / pgsql / mysql profiles, though those are not active by default in the observed runtime

## 6. Configuration
Key compose/runtime facts:
- `SERVER_HOST=0.0.0.0`
- `SERVER_PORT=8000`
- `SERVER_STORAGE_TYPE=local`
- `CAMOUFOX_OVERRIDE_DIR=/app/camoufox_override`
- default timezone: `Asia/Shanghai`

Observed `config.defaults.toml` highlights:
- `[app] app_url = "http://127.0.0.1:8000"`
- `[app] admin_username = "admin"`
- `[grok] timeout = 120`
- `[register] solver_url = "http://127.0.0.1:5072"`
- optional register-related fields exist for worker domain / email / solver integration

This project is now documented beyond the first surface pass, but still deserves a future app-level audit.

## 7. Operations

### Check status
```bash
ssh oracle-proxy
docker ps | grep grok2api
ss -ltnp | grep 8000
```

### Logs
```bash
ssh oracle-proxy
docker logs -f grok2api
```

### Repo-level inspection
```bash
ssh oracle-proxy
cd /root/grok2api
ls -la
```

## 8. Health Checks
Healthy signs:
- container `grok2api` is `Up`
- port `8000` is listening
- callers using `/v1` API path succeed

## 9. Data and Persistence
Potential persistent paths observed:
- `/root/grok2api/data`
- `/root/grok2api/logs`

## 10. Common Tasks
- verify local API listener on `8000`
- inspect logs when upstream proxy clients fail

## 11. Failure Modes / Troubleshooting
### Symptom: local Grok/OpenAI-compatible endpoint fails
Check:
- `docker logs grok2api`
- port `8000`
- `GET /health`
- upstream caller target URL

### Symptom: admin pages load but state looks wrong
Check:
- `/root/grok2api/data/token.json`
- `/root/grok2api/data/api_keys.json`
- `/root/grok2api/data/stats.json`
- admin endpoints under `/api/v1/admin/*`

### Symptom: disk usage grows unexpectedly
Likely causes:
- image/video artifacts accumulating under `data/tmp/`
- cache or generated media not cleaned aggressively enough

Checks:
- inspect `/root/grok2api/data/tmp/image`
- inspect `/root/grok2api/data/tmp/video`
- inspect cache/admin endpoints

## 12. Dependencies / Cross-links
- Related host docs: `../HOST.md`, `../NETWORK.md`
- Related clients may include cliproxy and local tooling using `/v1`

## 13. Change History
- 2026-03-15: documented first-pass deployment and access details
- 2026-03-21: verified deployed repo was already current with upstream (`d6a945c` on both local `HEAD` and `origin/main`), so no upstream update was required
- 2026-03-21: documented that live secrets/config are sourced from `data/config.toml`, not from `config.defaults.toml`
- 2026-03-21: documented local deployment customizations and recorded local preservation branch `oracle-proxy/local-custom-20260321` with commit `2413e6c`
- 2026-03-21: recorded cleanup of hardcoded default keys in `config.defaults.toml` so baseline defaults are no longer treated as live production secrets
 upstream proxy clients fail

## 11. Failure Modes / Troubleshooting
### Symptom: local Grok/OpenAI-compatible endpoint fails
Check:
- `docker logs grok2api`
- port `8000`
- `GET /health`
- upstream caller target URL

### Symptom: admin pages load but state looks wrong
Check:
- `/root/grok2api/data/token.json`
- `/root/grok2api/data/api_keys.json`
- `/root/grok2api/data/stats.json`
- admin endpoints under `/api/v1/admin/*`

### Symptom: disk usage grows unexpectedly
Likely causes:
- image/video artifacts accumulating under `data/tmp/`
- cache or generated media not cleaned aggressively enough

Checks:
- inspect `/root/grok2api/data/tmp/image`
- inspect `/root/grok2api/data/tmp/video`
- inspect cache/admin endpoints

## 12. Dependencies / Cross-links
- Related host docs: `../HOST.md`, `../NETWORK.md`
- Related clients may include cliproxy and local tooling using `/v1`

## 13. Change History
- 2026-03-15: documented first-pass deployment and access details
lure Modes / Troubleshooting
### Symptom: local Grok/OpenAI-compatible endpoint fails
Check:
- `docker logs grok2api`
- port `8000`
- upstream caller target URL

## 12. Dependencies / Cross-links
- Related host docs: `../HOST.md`, `../NETWORK.md`
- Related clients may include cliproxy and local tooling using `/v1`

## 13. Change History
- 2026-03-15: documented first-pass deployment and access details
