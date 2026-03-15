# caddy on oracle-docker-proxy

## 1. Summary
Caddy is the front-door reverse proxy for the shared docker/registry proxy host `oracle-docker-proxy` (`24-7-10-2055`). It terminates public HTTP/HTTPS traffic for multiple `*.zhangxuemin.work` names and forwards each hostname to a distinct localhost backend port.

## 2. Access / Entry Points
- Public listeners: `*:80`, `*:443`
- Admin API: `127.0.0.1:2019`
- Config file: `/etc/caddy/Caddyfile`
- systemd unit: `caddy.service`
- Host SSH entry: `ssh oracle-docker_proxy`

## 3. Deployment Layout
- Host-level Caddy installation managed by systemd
- Site config stored in a single `/etc/caddy/Caddyfile`
- Backends are local Docker-published ports

## 4. Runtime Topology
Hostname to backend mapping currently observed:
- `ui.zhangxuemin.work` -> `localhost:50000`
- `hub.zhangxuemin.work` -> `localhost:51000`
- `ghcr.zhangxuemin.work` -> `localhost:52000`
- `gcr.zhangxuemin.work` -> `localhost:53000`
- `k8sgcr.zhangxuemin.work` -> `localhost:54000`
- `k8s.zhangxuemin.work` -> `localhost:55000`
- `quay.zhangxuemin.work` -> `localhost:56000`
- `mcr.zhangxuemin.work` -> `localhost:57000`
- `elastic.zhangxuemin.work` -> `localhost:58000`
- `nvcr.zhangxuemin.work` -> `localhost:59000`
- `hubcmd.zhangxuemin.work` -> `localhost:30080`

## 5. Purpose and Workflow
Caddy provides a stable domain-based front door so users/clients can consume registry mirrors and UI services through memorable hostnames instead of raw high ports.

## 6. Configuration
- Main config file: `/etc/caddy/Caddyfile`
- Config validation works: `caddy validate --config /etc/caddy/Caddyfile`
- Current validation notes:
  - config is valid
  - file formatting is inconsistent (`caddy fmt --overwrite` suggested)
  - some `header_up` directives are unnecessary because Caddy already forwards them by default

## 7. Operations
### Validate config
```bash
ssh oracle-docker_proxy
caddy validate --config /etc/caddy/Caddyfile
```

### Inspect current config
```bash
ssh oracle-docker_proxy
sed -n '1,260p' /etc/caddy/Caddyfile
```

### Check listeners
```bash
ssh oracle-docker_proxy
ss -ltnp | egrep ':(80|443|2019)\\b'
```

## 8. Health Checks
Healthy signs:
- `caddy.service` active/running
- `*:80` and `*:443` listening
- expected hostnames return `HTTP 200` or expected upstream behavior

## 9. Data and Persistence
- config persisted in `/etc/caddy/Caddyfile`
- certificate/storage paths not yet documented

## 10. Common Tasks
- add/remove hostname mappings
- verify a hostname points to the intended localhost backend
- diagnose edge `502` by checking the mapped local backend port first

## 11. Failure Modes / Troubleshooting
### Symptom: public hostname returns `502`
Check:
- mapped backend port in `/etc/caddy/Caddyfile`
- local backend response via `curl -I http://127.0.0.1:<port>`
- whether target container is up and healthy

Known current issue:
- `ui.zhangxuemin.work` -> `localhost:50000` is currently failing with local connection reset

## 12. Dependencies / Cross-links
- Depends on Docker-published backend ports
- See host docs and future `registry-ui` / registry proxy project docs

## 13. Change History
- 2026-03-15: First documented from on-host inspection.
