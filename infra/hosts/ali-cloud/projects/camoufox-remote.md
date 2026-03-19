# camoufox-remote on ali-cloud

## 1. Summary
`camoufox-remote` is a standalone remote browser automation endpoint running the Apify Camoufox Playwright image and exposing a websocket endpoint on port `39222`.

## 2. Access / Entry Points
- Container: `camoufox-remote`
- Public port: `39222`
- Websocket endpoint: `ws://<host>:39222/camoufox`
- Local deployment scripts:
  - `/opt/camoufox-remote/run_camoufox_server.py`
  - `/opt/camoufox-remote/run_camoufox_server_compat.py`

## 3. Deployment Layout
- Image: `apify/actor-python-playwright-camoufox:latest`
- Appears manually maintained outside 1Panel app paths
- One bind mount injects the compat launcher into the container

## 4. Runtime Topology
- host `39222` -> container `39222`
- service starts under `xvfb-run`
- compat launcher calls Camoufox server startup and exposes websocket automation

## 5. Configuration / State
Key envs observed:
- `CAMOU_WS_PATH=camoufox`
- `CAMOU_HEADLESS=true`
- `CAMOU_HOST=0.0.0.0`
- `CAMOU_PORT=39222`

Observed container command / runtime details:
- Entrypoint: `./xvfb-entrypoint.sh`
- Cmd: `python3 /app/run_camoufox_server_compat.py`
- Restart policy: `unless-stopped`
- Published directly on host: `0.0.0.0:39222->39222/tcp`
- Current deployment is plain websocket (`ws://`) with no documented TLS or auth layer in front

## 6. Operations
### Check container
```bash
ssh ali-cloud
docker ps --filter name=camoufox-remote
```

### Check logs
```bash
ssh ali-cloud
docker logs --tail 120 camoufox-remote
```

### Inspect wrapper scripts
```bash
ssh ali-cloud
sed -n '1,240p' /opt/camoufox-remote/run_camoufox_server.py
sed -n '1,240p' /opt/camoufox-remote/run_camoufox_server_compat.py
```

## 7. Health Checks
Healthy signs:
- container is `Up`
- port `39222` is listening
- logs report websocket endpoint startup

Observed healthy log pattern:
- `Launching server...`
- `Server launched: ...`
- `Websocket endpoint: ws://0.0.0.0:39222/camoufox`

## 8. Failure Modes / Troubleshooting
### Symptom: remote browser clients cannot connect
Check:
- container status
- published port `39222`
- recent logs for startup failures
- whether clients are using the expected `/camoufox` websocket path

## 9. Dependencies / Cross-links
- likely used by external automation clients
- separate from 1Panel-managed apps

## 10. Change History
- 2026-03-15: First documented from on-host script/env/log inspection.
