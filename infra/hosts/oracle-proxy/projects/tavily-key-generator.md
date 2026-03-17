# Tavily Key Generator

## 1. Summary
- Project: Tavily Key Generator
- Host: `oracle-proxy`
- Purpose: 自动注册 Tavily 账号，产出新的 Tavily API keys，并自动上传到 Tavily Proxy
- Runtime status: running
- Priority: Tier 1

## 2. Access / Entry Points
- Repo path: `/root/tavily-key-generator`
- Main runtime container: `tavily-scheduler`
- Supporting containers:
  - `tavily-camoufox`
  - `tavily-camoufox-adapter`
- External solver adapter exposure: `158.178.236.241:16072`
- Internal adapter target: `http://camoufox-adapter:5072`

## 3. Deployment Layout
- Project root: `/root/tavily-key-generator`
- Compose file: `/root/tavily-key-generator/docker-compose.yml`
- Main config: `/root/tavily-key-generator/config.py`
- Output file: `/root/tavily-key-generator/output/api_keys.md`

## 4. Runtime Topology
Components:
- `tavily-scheduler`: periodically runs `python main.py`
- `tavily-camoufox`: browser runtime for solving / automation support
- `tavily-camoufox-adapter`: adapter exposed as host port `16072`

Key dependency chain:
- email backend: `https://tmail.zhangxuemin.work`
- CAPTCHA solver mode: `adapter`
- Turnstile adapter internal URL: `http://camoufox-adapter:5072`
- proxy upload target from inside container: `http://host.docker.internal:9874`

## 5. Purpose and Workflow
Workflow:
1. scheduler wakes up every 2160 seconds
2. `python main.py` runs one registration cycle
3. account created with `zhangxuemin.work` mailbox via private tmail worker
4. Turnstile challenge solved through adapter stack
5. verification email is parsed
6. API key is extracted after login
7. result appended to `output/api_keys.md`
8. fresh key is auto-uploaded to Tavily Proxy

## 6. Configuration
Observed key settings in `config.py`:
- `EMAIL_DOMAIN = "zhangxuemin.work"`
- `EMAIL_API_URL = "https://tmail.zhangxuemin.work"`
- `CAPTCHA_SOLVER = "adapter"`
- `DEFAULT_PASSWORD = "TavilyAuto123!"`
- `API_KEYS_FILE = "output/api_keys.md"`
- `PROXY_AUTO_UPLOAD = True`
- `PROXY_URL = "http://host.docker.internal:9874"`
- `TURNSTILE_ADAPTER_URL = "http://camoufox-adapter:5072"`

Important rule:
- **Inside the container, `127.0.0.1:9874` is wrong for proxy upload.** The working target is `host.docker.internal:9874`.

## 7. Operations

### Check status
```bash
ssh oracle-proxy
cd /root/tavily-key-generator
docker compose ps
docker ps | grep -E 'tavily-(scheduler|camoufox|camoufox-adapter)'
```

### Start / ensure stack is up
```bash
ssh oracle-proxy
cd /root/tavily-key-generator
docker compose up -d
```

### Rebuild stack
```bash
ssh oracle-proxy
cd /root/tavily-key-generator
docker compose up -d --build
```

### Follow scheduler logs
```bash
ssh oracle-proxy
docker logs -f tavily-scheduler
```

### Trigger one manual registration run now
```bash
ssh oracle-proxy
docker exec tavily-scheduler python main.py
```

## 8. Health Checks
Healthy signs:
- `tavily-scheduler` is `Up`
- `output/api_keys.md` continues gaining new lines over time
- scheduler logs show successful key extraction
- logs include successful auto-upload to proxy

Useful checks:
```bash
ssh oracle-proxy
tail -n 5 /root/tavily-key-generator/output/api_keys.md
docker logs --tail 100 tavily-scheduler
```

## 9. Data and Persistence
- Generated keys file: `/root/tavily-key-generator/output/api_keys.md`
- Runtime config file: `/root/tavily-key-generator/config.py`
- Compose stack state: Docker-managed

Backup considerations:
- `output/`
- `config.py`
- any local patches in repo

## 10. Common Tasks

### Force one fresh registration for validation
```bash
docker exec tavily-scheduler python main.py
```

### Confirm new key was generated
```bash
tail -n 3 /root/tavily-key-generator/output/api_keys.md
```

### Confirm auto-upload succeeded
Check logs for:
```text
☁️ 已自动上传到 Proxy
```

## 11. Failure Modes / Troubleshooting

### Symptom: registration succeeds but proxy pool does not grow
Likely causes:
- `PROXY_AUTO_UPLOAD = False`
- wrong `PROXY_URL`
- proxy unreachable from container

Checks:
- inspect `config.py`
- run manual registration and read final upload log line
- verify proxy on host is reachable from container network

### Symptom: verification email not processed
Likely causes:
- tmail worker issue
- parser regression
- Auth0 email formatting drift

Checks:
- logs around email parsing
- direct inspection of worker mail endpoints if needed

### Symptom: Turnstile solving fails
Checks:
- `tavily-camoufox` status
- `tavily-camoufox-adapter` status
- host port `16072`
- internal adapter URL in config

## 12. Dependencies / Cross-links
- Related service: `./tavily-proxy.md`
- Host docs: `../HOST.md`, `../NETWORK.md`, `../PROJECTS.md`

## 13. Change History
- 2026-03-15:
  - schedulerized deployment confirmed
  - auto-upload path fixed to use `host.docker.internal:9874`
  - verified fresh registration can auto-upload to proxy
- 2026-03-16:
  - confirmed runtime config uses `EMAIL_ADMIN_PASSWORD = "Zxm971004"`, `EMAIL_SITE_PASSWORD = "Zxm971004"`, and `PROXY_ADMIN_PASSWORD = "Zxm971004"`
  - changed batch target to `RUN_COUNT = 5`
  - changed scheduler cadence to `TAVILY_INTERVAL_SECONDS = 10800` (~3 hours per batch)
  - effective behavior is now approximately 5 registration attempts every 3 hours, not a strict rate guarantee
