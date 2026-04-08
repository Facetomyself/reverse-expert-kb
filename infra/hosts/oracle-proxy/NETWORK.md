# oracle-proxy / Network

## 1. Addressing
- Public IP: `158.178.236.241`
- Primary documented domain: `proxy.zhangxuemin.work`
- Observed local/private addresses at snapshot:
  - `10.0.0.68`
  - multiple docker bridge ranges (`172.x.x.x`)

## 2. Open / Listening Ports (observed)

| Port | Bind | Component | Exposure guess | Notes |
|---|---:|---|---|---|
| 22 | 0.0.0.0 | sshd | public | SSH access |
| 80 | 0.0.0.0 | 1panel | public/internal-mgmt | Needs policy confirmation |
| 8000 | 0.0.0.0 | grok2api | public/direct | Grok API bridge |
| 8317 | 0.0.0.0 | cliproxy | public/direct | OpenAI-compatible CLI proxy |
| 9874 | 0.0.0.0 | Tavily proxy | public/direct | Web console + `/api/*` |
| 15072 | 0.0.0.0 | grok-register adapter | public/direct | Grok solver adapter |
| 30011 | 0.0.0.0 | nginx | public | exact purpose TBD |
| 30001 / 30004-30010 | * | sing-box | mixed | proxy/tunnel related, TBD |
| 14391 | * | xray | mixed | TBD |
| 20241 | 127.0.0.1 | cloudflared | local-only | tunnel local listener |

## 3. Domain Resolution
- `proxy.zhangxuemin.work` → `158.178.236.241`

## 4. Tavily-related entry points
- Web console: `http://proxy.zhangxuemin.work:9874/`
- API base: `http://proxy.zhangxuemin.work:9874/api`

## 5. Nginx / Proxy Layer Notes
### System nginx
- `nginx.service` is active
- enabled site: `/etc/nginx/sites-enabled/default`
- current config is the Debian default static site:
  - `listen 80 default_server`
  - `root /var/www/html`
  - `server_name _`
- No meaningful reverse-proxy mapping was found in system nginx during this pass

### sing-box embedded nginx
- `sing-box.service` also owns nginx processes via `/etc/sing-box/nginx.conf`
- This strongly suggests a separate proxy/subscription delivery layer independent of system nginx

## 6. Tunnel / Proxy Stack Notes
### sing-box
- Config root: `/etc/sing-box/conf/`
- Notable subscription artifacts:
  - `/etc/sing-box/subscribe/*`
- Cert paths observed:
  - `/etc/sing-box/cert/cert.pem`
  - `/etc/sing-box/cert/private.key`
- Treat ports `30001`, `30004-30011` as sing-box-owned until proven otherwise

### xray
- Config root: `/etc/v2ray-agent/xray/conf`
- Active ports observed:
  - `*:14391`
  - `127.0.0.1:45987`
- Recent logs show accepted traffic forwarded toward local `127.0.0.1:45987`

### cloudflared
- Local listener previously observed on `127.0.0.1:20241`
- Exact tunnel config still TBD

## 7. Notes / Caveats
- This host does **not** currently have `ufw` installed (`ufw: command not found` at snapshot time).
- Several ports are directly bound on `0.0.0.0`; future hardening review is recommended.
- Network documentation is now better than the first pass, but cloudflared and full sing-box/xray semantics still need a dedicated audit.
