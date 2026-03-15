# hubcmd-ui on oracle-docker-proxy

## 1. Summary
`hubcmd-ui` is a separate UI service exposed as `hubcmd.zhangxuemin.work`. Unlike `registry-ui`, it is currently responding normally.

## 2. Access / Entry Points
- Public URL: `https://hubcmd.zhangxuemin.work`
- Caddy mapping: `hubcmd.zhangxuemin.work` -> `localhost:30080`
- Host-published port: `30080 -> container 3000`
- SSH entry: `ssh oracle-docker_proxy`

## 3. Deployment Layout
- Container name: `hubcmd-ui`
- Image: `dqzboy/hubcmd-ui:latest`
- Status observed: `Up 6 months`

## 4. Runtime Topology
- public hostname -> Caddy -> `localhost:30080` -> container `3000`

## 5. Purpose and Workflow
Likely provides a human-facing web UI related to the Docker Hub mirror/proxy workflow. Exact feature scope still needs app-level inspection.

## 6. Configuration
Not yet documented.

## 7. Operations
### Probe local backend
```bash
ssh oracle-docker_proxy
curl -I http://127.0.0.1:30080
```

### Check logs
```bash
ssh oracle-docker_proxy
docker logs --tail 80 hubcmd-ui
```

## 8. Health Checks
Current healthy signs observed:
- local probe to `127.0.0.1:30080` returns `HTTP 200`
- public endpoint is expected to be healthy through Caddy

## 9. Data and Persistence
Not yet documented.

## 10. Common Tasks
- verify UI availability
- inspect logs if public route fails

## 11. Failure Modes / Troubleshooting
### Symptom: public `hubcmd.zhangxuemin.work` fails
Check:
- Caddy mapping
- local port `30080`
- `hubcmd-ui` container status/logs

## 12. Dependencies / Cross-links
- Fronted by `projects/caddy.md`

## 13. Change History
- 2026-03-15: First documented from runtime inspection.
