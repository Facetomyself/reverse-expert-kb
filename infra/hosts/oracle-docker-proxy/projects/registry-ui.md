# registry-ui on oracle-docker-proxy

## 1. Summary
`registry-ui` is the UI backend currently exposed as `ui.zhangxuemin.work` through Caddy. It is presently unhealthy from a user perspective because the public endpoint returns `502`, and direct local access to the backend port resets the connection.

## 2. Access / Entry Points
- Public URL: `https://ui.zhangxuemin.work`
- Caddy mapping: `ui.zhangxuemin.work` -> `localhost:50000`
- Host-published port: `50000 -> container 8080`
- SSH entry: `ssh oracle-docker_proxy`

## 3. Deployment Layout
- Container name: `registry-ui`
- Image: `dqzboy/docker-registry-ui:latest`
- Entrypoint: `/docker-entrypoint.sh`
- Command: `web`
- Restart policy: `always`
- No explicit bind mounts observed

## 4. Runtime Topology
Current environment characteristics:
- talks to `http://reg-docker-hub:5000`
- no SSL verification enabled for upstream registry access
- container listens on app port `8080`
- host maps `50000 -> 8080`

## 5. Purpose and Workflow
Provides a browser UI for browsing registry content, currently aimed at the Docker Hub mirror backend.

## 6. Configuration
Observed behavioral config:
- backend target registry is the local `reg-docker-hub` service
- environment-based app config exists

Sensitive config rule:
- do not copy full secret env values into general infra notes; record purpose and location only.

## 7. Operations
### Check container status
```bash
ssh oracle-docker_proxy
docker ps --filter name=registry-ui
```

### Check recent logs
```bash
ssh oracle-docker_proxy
docker logs --tail 120 registry-ui
```

### Probe local backend
```bash
ssh oracle-docker_proxy
curl -I http://127.0.0.1:50000
```

## 8. Health Checks
Healthy signs should be:
- `ui.zhangxuemin.work` returns `200`
- `curl -I http://127.0.0.1:50000` succeeds
- logs do not show repeated app exceptions

Current observed state:
- external endpoint returns `502`
- local probe resets connection
- logs show repeated `Faraday::ServerError` cases when fetching certain manifests/tags from `reg-docker-hub`

## 9. Data and Persistence
- no bind mounts observed from `docker inspect`
- persistence model still needs confirmation

## 10. Common Tasks
- inspect logs for broken repo/tag views
- verify target registry accessibility from inside container
- confirm whether failures are limited to certain manifests/media types

## 11. Failure Modes / Troubleshooting
### Symptom: `ui.zhangxuemin.work` returns `502`
Known current explanation:
- backend on `127.0.0.1:50000` is not serving healthy HTTP responses consistently

### Symptom: tag detail page crashes
Observed pattern:
- `tags/list` may return `200`
- subsequent manifest fetches can trigger `Faraday::ServerError`

Likely direction:
- the UI app is choking on certain manifest/media-type cases from the proxied registry
- this can bubble up as backend instability and external `502`

### Symptom: logs mention SSL on non-SSL Puma
Interpretation:
- some clients are likely speaking TLS directly to the plain HTTP backend port
- the app behind `50000` is not meant to receive HTTPS directly; TLS belongs at Caddy

## 12. Dependencies / Cross-links
- Fronted by `projects/caddy.md`
- Depends on `reg-docker-hub`

## 13. Change History
- 2026-03-15: First documented from inspect/log analysis; known unhealthy state recorded.
