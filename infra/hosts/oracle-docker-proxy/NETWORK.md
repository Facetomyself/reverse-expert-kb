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

Observed on-host listeners / mapping:
- Caddy listens on `*:80` and `*:443`
- Caddy admin API listens on `127.0.0.1:2019`
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

## 4. To Be Confirmed
- whether `backup.zhangxuemin.work` has been removed from Caddy or handled elsewhere
- why `ui.zhangxuemin.work` backend on `50000` resets local connections
- exact data volumes for each registry proxy
- any nginx/traefik/cloudflared involvement behind or alongside Caddy
