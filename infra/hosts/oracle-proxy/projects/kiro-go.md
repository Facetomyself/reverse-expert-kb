# Kiro-Go

## 1. Summary
- Project: Kiro-Go
- Host: `oracle-proxy`
- Upstream: `https://github.com/Quorinex/Kiro-Go`
- Purpose: Convert Kiro accounts into OpenAI / Anthropic compatible API service with multi-account pooling and a web admin panel.
- Runtime status: running
- Priority: Tier 2

## 2. Entry Points
- Global/direct panel: `https://kiro.zhangxuemin.work/admin`
- Domestic/HK-optimized panel: `https://kiro-cn.zhangxuemin.work/admin`
- API paths on both entrypoints:
  - Anthropic-compatible: `/v1/messages`
  - OpenAI-compatible: `/v1/chat/completions`

Topology:

```text
Browser/API client -> kiro.zhangxuemin.work -> oracle-proxy:caddy-cpam -> 127.0.0.1:18766 -> Kiro-Go:8080
Browser/API client -> kiro-cn.zhangxuemin.work -> hk-relay Caddy -> https://kiro.zhangxuemin.work -> same Kiro-Go origin
```

## 3. Deployment Layout
- Compose directory: `/root/containers/kiro-go`
- Compose file: `/root/containers/kiro-go/docker-compose.yml`
- Secret env file: `/root/containers/kiro-go/.env` (`0600`; contains `ADMIN_PASSWORD`)
- Data directory: `/root/containers/kiro-go/data`
- Config file: `/root/containers/kiro-go/data/config.json` (`0600`; sensitive runtime config)
- Image: `ghcr.io/quorinex/kiro-go:latest`
- Container name: `kiro-go`
- Local published port: `127.0.0.1:18766 -> 8080`
- Image ID at first deployment: `sha256:6051d62efd1d7d45384e34dd3da02368b7257f542f773778d3e16f11831eba3e`

Security stance:
- Kiro-Go is not published directly on `0.0.0.0`; the container port is loopback-only.
- Public access is through `caddy-cpam` on `oracle-proxy:443`.
- The CN entrypoint terminates TLS on `hk-relay` and forwards to the global/source hostname.
- Do not copy `.env`, admin password, account exports, tokens, or `data/config.json` contents into docs or chat.

## 4. TLS / Front Doors

### Global/source front door on `oracle-proxy`
- Caddy compose directory: `/root/containers/caddy-cpam`
- Caddyfile: `/root/containers/caddy-cpam/Caddyfile`
- Site: `kiro.zhangxuemin.work` -> `127.0.0.1:18766`

### CN/HK front door on `hk-relay`
- Caddyfile: `/etc/caddy/Caddyfile`
- Site: `kiro-cn.zhangxuemin.work` -> `https://kiro.zhangxuemin.work`
- Host header and TLS SNI are set to `kiro.zhangxuemin.work`.

## 5. Operations

### Status
```bash
ssh oracle-proxy
cd /root/containers/kiro-go
docker compose ps
docker logs --tail 100 kiro-go
```

### Restart / update
```bash
ssh oracle-proxy
cd /root/containers/kiro-go
docker compose pull kiro-go
docker compose up -d kiro-go
```

### Health / smoke checks
```bash
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:18766/admin
curl -sS -o /dev/null -w '%{http_code}\n' https://kiro.zhangxuemin.work/admin
curl -sS -o /dev/null -w '%{http_code}\n' https://kiro-cn.zhangxuemin.work/admin
```

Expected signs:
- `kiro-go` container is `Up`
- local `/admin` returns HTTP `200`
- global and CN `/admin` return HTTP `200`
- unauthenticated GETs to API endpoints may return `405 Method Not Allowed`; that is not a deployment failure.

## 6. DNS / Edge
Cloudflare DNS records created on 2026-06-06:
- `kiro.zhangxuemin.work` -> `158.178.236.241` (`oracle-proxy`)
- `kiro-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay`)

## 7. Change History
- 2026-06-06: Deployed Kiro-Go on `oracle-proxy` using `ghcr.io/quorinex/kiro-go:latest`; bound service to loopback `127.0.0.1:18766`; added global `kiro.zhangxuemin.work` and domestic/HK `kiro-cn.zhangxuemin.work` Caddy entrypoints; created Cloudflare DNS records; verified both `/admin` URLs returned HTTP 200.
