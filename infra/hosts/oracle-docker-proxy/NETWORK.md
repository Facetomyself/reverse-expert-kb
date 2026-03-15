# oracle-docker-proxy / NETWORK

## 1. Public Network Identity
- Public IP: `129.150.61.78` (from Cloudflare DNS export)
- Domain group label from export comments: `docker_proxy`
- Provider: To be confirmed

## 2. Domains currently mapped here
Based on the 2026-03-15 Cloudflare DNS export for `zhangxuemin.work`, the following A records point to `129.150.61.78`:

- `backup.zhangxuemin.work`
- `elastic.zhangxuemin.work`
- `gcr.zhangxuemin.work`
- `ghcr.zhangxuemin.work`
- `hubcmd.zhangxuemin.work`
- `hub.zhangxuemin.work`
- `k8sgcr.zhangxuemin.work`
- `mcr.zhangxuemin.work`
- `nvcr.zhangxuemin.work`
- `quay.zhangxuemin.work`
- `ui.zhangxuemin.work`

All were exported with comment-style annotation `docker_proxy` and `cf-proxied:false`.

## 3. Interpretation
Current best hypothesis:
- this host is a shared entrypoint for multiple registry/proxy/UI endpoints
- external HTTP probing strongly suggests TLS termination / front-door behavior via **Caddy**
- DNS alone is still insufficient to determine whether these names terminate on one reverse proxy, multiple containers, or upstream tunnels

Observed external probes on 2026-03-15:
- `https://hub.zhangxuemin.work` -> `HTTP/2 200`, `server: Caddy`, `via: 1.1 Caddy`
- `https://ghcr.zhangxuemin.work` -> `HTTP/2 200`, `server: Caddy`, `via: 1.1 Caddy`
- `https://gcr.zhangxuemin.work` -> `HTTP/2 200`, `server: Caddy`, `via: 1.1 Caddy`
- `https://quay.zhangxuemin.work` -> `HTTP/2 200`, `server: Caddy`, `via: 1.1 Caddy`
- `https://ui.zhangxuemin.work` -> `HTTP/2 502`, `server: Caddy`

## 4. To Be Confirmed
- actual listening ports
- exact Caddy deployment location/config
- backend targets behind each domain
- whether `ui.zhangxuemin.work` backend is currently down/misconfigured
- nginx/traefik/cloudflared/sing-box involvement behind or alongside Caddy
