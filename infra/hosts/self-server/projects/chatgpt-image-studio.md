# ChatGpt Image Studio on self-server-44005 / host185

## Summary
- Host: `self-server-44005` / `host185`
- Deployment path: `/opt/chatgpt-image-studio`
- Runtime shape: Docker Compose, single container + mounted local data dir
- Container name: `chatgpt-image-studio`
- Current live image: `chatgpt-image-studio:patched-20260424-refresh-serial`
- Base image source: `ghcr.io/peiyizhi0724/chatgpt-image-studio:v1.2.6`
- Public port: `211.144.221.229:30010 -> container 7000/tcp`

## Why this shape
Initial deployment intentionally preferred the existing oracle-proxy CPA/CLIProxy surface, but two different production issues were observed on the same day:

1. `CPA` image mode hit repeated `POST /v1/images/generations` timeouts on `oracle-proxy` / `cliproxy`
2. after switching to official/studio mode, direct ChatGPT Web refresh calls (`/backend-api/me`) failed behind the old fixed outbound SOCKS proxy with repeated `connection reset by peer`

Current stable shape after the same-day repair is:
- active image mode: `studio`
- auth-file sync remains pointed at oracle-proxy CPA/CLIProxy management on `http://proxy.zhangxuemin.work:8317`
- current direct-official ChatGPT traffic uses the already-documented `ali-cloud` authenticated **HTTP** explicit proxy on `106.15.239.221:2081`
- a local patched image is used because the upstream backend was hotfixed to serialize account-refresh calls (`/backend-api/me` then `/backend-api/conversation/init`) instead of issuing those two requests concurrently

## On-host layout
```text
/opt/chatgpt-image-studio/
├── docker-compose.yml
└── backend-data/
    ├── config.toml
    ├── auths/
    ├── sync_state/
    └── tmp/image/
```

## Compose
Current deployment uses a small Compose file equivalent to:
```yaml
services:
  studio:
    image: ghcr.io/peiyizhi0724/chatgpt-image-studio:v1.2.6
    container_name: chatgpt-image-studio
    ports:
      - "30010:7000"
    environment:
      SERVER_HOST: 0.0.0.0
      SERVER_PORT: 7000
      TZ: Asia/Shanghai
    volumes:
      - ./backend-data:/app/data
    restart: unless-stopped
```

## Key config decisions
Configured in `/opt/chatgpt-image-studio/backend-data/config.toml`:
- current active `chatgpt.image_mode = "studio"`
- `sync.enabled = true`
- `sync.base_url = "http://proxy.zhangxuemin.work:8317"`
- `cpa.base_url = "http://proxy.zhangxuemin.work:8317"` is still retained for future CPA re-tests, but it is **not** the active image path in the current repaired runtime
- `proxy.enabled = true`
- `proxy.sync_enabled = false`
- current `proxy.url = "http://gateway:***@106.15.239.221:2081"` (ali-cloud authenticated HTTP explicit proxy; secret intentionally redacted in docs)

Interpretation:
- current image generation path is official/studio rather than CPA
- auth-file sync still talks to oracle-proxy cliproxy management directly
- current direct ChatGPT/offline-refresh traffic uses the ali-cloud HTTP explicit proxy instead of the earlier unstable fixed SOCKS path
- sync / CPA management requests are not recursively wrapped by that outbound proxy layer

## Secrets handling
The following are intentionally kept only on-host inside `backend-data/config.toml` and are **not** copied into `infra/`:
- app login/auth key
- app API key
- oracle-proxy CPA image API key
- oracle-proxy CPA management key
- ali-cloud HTTP proxy credential
- any historical outbound SOCKS credential that was tried before the repair

## Operations
### Health
```bash
ssh self-server-44005
curl http://127.0.0.1:30010/health
```

### Logs
```bash
ssh self-server-44005
docker logs -f chatgpt-image-studio
```

### Restart / update
```bash
ssh self-server-44005
cd /opt/chatgpt-image-studio
/usr/local/bin/docker-compose pull
/usr/local/bin/docker-compose up -d
```

### Local status checks
```bash
ssh self-server-44005
cd /opt/chatgpt-image-studio
/usr/local/bin/docker-compose ps
ss -ltnp | grep 30010
```

## Validation timeline (2026-04-24)
### Initial deployment
- container came up successfully with port publish `30010 -> 7000`
- host-local `curl http://127.0.0.1:30010/health` returned `{"status":"ok"}`
- transit-side validation from `ali-cloud` confirmed public `211.144.221.229:30010/health` returned `200 OK`
- transit-side functional validation also confirmed:
  - `POST /auth/login` works with the configured app auth key
  - `GET /v1/models` works with the configured app API key
- initial sync state on first deployment ended with `26` synced local accounts available to the service

### Same-day repair after runtime failures
- observed failure 1: `CPA` mode repeatedly timed out on `oracle-proxy` / `cliproxy` `POST /v1/images/generations`
- observed failure 2: after switching away from CPA, official/studio mode hit `/backend-api/me failed ... connection reset by peer` while using the earlier fixed SOCKS proxy
- same-day differential testing showed:
  - the old SOCKS path could appear superficially alive from host-side single `curl` probes
  - but real app refresh traffic and even container-network `curl` to `https://chatgpt.com/backend-api/me` would reset over that SOCKS path
  - the ali-cloud authenticated HTTP explicit proxy on `:2081` was stable for the same target from both the host and the app container network
- repair actions applied:
  - switched the app's fixed proxy from the old SOCKS URL to the ali-cloud HTTP explicit proxy on `106.15.239.221:2081`
  - replaced the stock image with a local patched image `chatgpt-image-studio:patched-20260424-refresh-serial`
  - the local patch serialized account refresh requests (`/backend-api/me` then `/backend-api/conversation/init`) instead of firing them concurrently
- post-fix validation:
  - `GET /api/accounts/{id}/quota` for a live non-disabled `Plus` account returned `refresh_requested=true`, `refreshed=true`, empty `refresh_error`, and a populated image window (`image_gen_remaining = 120` with reset timestamp)
  - this confirmed the previous `/backend-api/me` refresh blocker was cleared in the repaired runtime

## Routing caveat
From Oracle/OpenClaw-side environments, direct access to the domestic public IP may still be asymmetric or time out even when the service is healthy for China-side/transit probes. If an external validation from the current OpenClaw host is inconclusive, verify via `ali-cloud` first.
