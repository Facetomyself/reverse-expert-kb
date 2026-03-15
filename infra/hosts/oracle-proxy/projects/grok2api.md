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

## 4. Runtime Topology
- Host exposure: `0.0.0.0:8000 -> 8000/tcp`
- Container image: `grok2api-official-local:latest`
- Likely acts as the backend behind `http://proxy.zhangxuemin.work:8000/v1` used elsewhere on this infrastructure

## 5. Purpose and Workflow
Known from surrounding infrastructure usage:
- local tools and proxies on this host use a Grok/OpenAI-compatible API path via port `8000`
- this project appears to be the local Grok API service backing that path

## 6. Configuration
Documented to inspect later:
- `.env`
- `config.defaults.toml`
- compose env bindings

At this stage, only surface-level deployment facts are documented.

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
- upstream caller target URL

## 12. Dependencies / Cross-links
- Related host docs: `../HOST.md`, `../NETWORK.md`
- Related clients may include cliproxy and local tooling using `/v1`

## 13. Change History
- 2026-03-15: documented first-pass deployment and access details
