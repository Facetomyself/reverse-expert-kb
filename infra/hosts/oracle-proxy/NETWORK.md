# oracle-proxy / Network

## 1. Addressing
- Public IP: `158.178.236.241`
- Primary documented domain: `proxy.zhangxuemin.work`
- CPA Manager Plus direct domain: `cpam.zhangxuemin.work`
- CLIProxy backup pool direct domain: `proxy-bak.zhangxuemin.work`
- Observed local/private addresses at snapshot:
  - `10.0.0.68`
  - multiple docker bridge ranges (`172.x.x.x`)

## 2. Open / Listening Ports (observed)

| Port | Bind | Component | Exposure guess | Notes |
|---|---:|---|---|---|
| 22 | 0.0.0.0 | sshd | public | SSH access |
| 80 | * | caddy-cpam | public HTTP redirect / ACME | Caddy owns HTTP after 2026-06-07 fix; redirects app hostnames to HTTPS |
| 18080 | 0.0.0.0 | 1panel | local/origin behind Caddy | 1Panel origin port; public domain access is fronted by Caddy at `proxy.zhangxuemin.work` |
| 443 | * | caddy-cpam | public/direct | TLS front door for app hostnames including `cpam`, `gptam`, `kiro`, `kiro-rs`, docs, Card Shop, and GPT Card Shop |
| 18317 | 0.0.0.0 | CPA Manager Plus | public/direct | Manager Server / management panel; normally accessed via `https://cpam.zhangxuemin.work` |
| 18765 | 127.0.0.1 | GPT Account Manager | local-only | Docker-published loopback origin for `gptam.zhangxuemin.work`; not directly public |
| 18766 | 127.0.0.1 | Kiro-Go | local-only | Docker-published loopback origin for `kiro.zhangxuemin.work`; not directly public |
| 18769 | 127.0.0.1 | Kiro-RS | local-only | Docker-published loopback origin for `kiro-rs.zhangxuemin.work`; not directly public |
| 8000 | 0.0.0.0 | grok2api | public/direct | Grok API bridge |
| 8317 | 0.0.0.0 | cliproxy | public/direct | OpenAI-compatible CLI proxy primary pool |
| 8318 | 0.0.0.0 | cliproxy-backup | public/direct | OpenAI-compatible CLI proxy backup pool; separate config/auth dir; same static residential proxy config as primary |
| 9874 | 0.0.0.0 | Tavily proxy | public/direct | Web console + `/api/*` |
| 30011 | 0.0.0.0 | nginx | public | exact purpose TBD |
| 30001 / 30004-30010 | * | sing-box | mixed | proxy/tunnel related, TBD |
| 14391 | * | xray | mixed | TBD |
| 20241 | 127.0.0.1 | cloudflared | local-only | tunnel local listener |

## 3. Domain Resolution
- `proxy.zhangxuemin.work` → `158.178.236.241`
- `proxy-bak.zhangxuemin.work` → `158.178.236.241`
- `cpam.zhangxuemin.work` → `158.178.236.241`
- `gptam.zhangxuemin.work` → `158.178.236.241`
- `kiro.zhangxuemin.work` → `158.178.236.241`
- `kiro-rs.zhangxuemin.work` → `158.178.236.241`
- `docs.zhangxuemin.work` → `158.178.236.241`
- `card.zhangxuemin.work` → `158.178.236.241`
- `zcode.zhangxuemin.work` → `158.178.236.241`
- `gpt-session.zhangxuemin.work` → `158.178.236.241`

## 4. Tavily-related entry points
- Web console: `http://proxy.zhangxuemin.work:9874/`
- API base: `http://proxy.zhangxuemin.work:9874/api`


## 4A. CPA Manager Plus entry points
- Global/direct panel: `https://cpam.zhangxuemin.work/management.html`
- Domestic/HK optimized panel: `https://cpam-cn.zhangxuemin.work/management.html`
- Direct source service on this host: `caddy-cpam` container on public `443`, reverse-proxying to `127.0.0.1:18317`
- Manager Server connects back to local cliproxy using `http://host.docker.internal:8317`


## 4B. CLIProxy backup pool entry points
- Global/direct API base: `https://proxy-bak.zhangxuemin.work/v1`
- Domestic/HK optimized API base: `https://proxy-bak-cn.zhangxuemin.work/v1`
- Direct source service on this host: `cliproxy-backup` container on public `8318`, reverse-proxied by `caddy-cpam` on public `443`
- Runtime isolation from primary `cliproxy`: separate container, separate host port, separate config path `/root/containers/cliproxy-backup/config.yaml`, separate auth directory `/root/containers/cliproxy-backup/auth-dir`
- Outbound proxy stance: seeded from the primary pool and intentionally keeps the same static residential `proxy-url` settings unless a later tuning pass changes it.
- Update automation: root crontab runs unified `/root/update_cpa_stack.sh` daily at `06:30` and logs to `/var/log/cpa-stack-update.log`, updating primary CLIProxy, backup CLIProxy, and CPA Manager Plus together.
- Operational gotcha fixed on 2026-06-09: the `/management.html` outage on the backup pool was traced to a bad upstream Docker build window rather than permanent feature removal. Direct validation on `oracle-proxy` showed `v7.1.44` OK, `v7.1.52` returning 404, and `v7.1.53` / `v7.1.56` OK again; this lines up with the upstream `v7.1.52 -> v7.1.53` Docker change adding CA certificates for HTTPS support, likely needed by the panel asset download path. The backup pool was originally pinned to `eceasy/cli-proxy-api:v7.1.56` after that outage; on 2026-07-10 it was advanced to the same `eceasy/cli-proxy-api:latest` image as the primary pool, and `/root/lib/cpa-stack/update_cliproxy_backup.sh` now defaults to `latest` while still requiring `/management.html` HTTP 200 during health checks/rollback.

## 4C. GPT Account Manager entry points
- Global/direct panel: `https://gptam.zhangxuemin.work/`
- Domestic/HK optimized panel: `https://gptam-cn.zhangxuemin.work/`
- Both panels require the application login page before the workbench is reachable; token is the on-host `MAIL_PICKUP_ADMIN_TOKEN`.
- Direct source service on this host: `gpt-account-manager` container, published only on `127.0.0.1:18765` and reverse-proxied by `caddy-cpam` on public `443`.
- The application does not support `HEAD` on `/`; use GET checks for homepage verification.


## 4D. Kiro-Go entry points
- Global/direct panel: `https://kiro.zhangxuemin.work/admin`
- Domestic/HK optimized panel: `https://kiro-cn.zhangxuemin.work/admin`
- API paths are served on the same hostnames, including `/v1/messages` and `/v1/chat/completions`.
- Direct source service on this host: `kiro-go` container, published only on `127.0.0.1:18766` and reverse-proxied by `caddy-cpam` on public `443`.
- Runtime/config directory: `/root/containers/kiro-go`; `.env` and `/root/containers/kiro-go/data/config.json` are sensitive and should not be copied into docs or chat.

## 4H. Kiro-RS entry points
- Global/direct panel: `https://kiro-rs.zhangxuemin.work/admin`
- Domestic/HK optimized panel: `https://kiro-rs-cn.zhangxuemin.work/admin`
- API paths are served on the same hostnames, including `/v1/models`, `/v1/messages`, and `/v1/messages/count_tokens`.
- Direct source service on this host: `kiro-rs` container, published only on `127.0.0.1:18769` and reverse-proxied by `caddy-cpam` on public `443`.
- Runtime/config directory: `/root/containers/kiro-rs`; `config/config.json`, `config/credentials.json`, and `deploy-secrets.txt` are sensitive and should not be copied into docs or chat.
- DNS added on 2026-06-07: `kiro-rs -> 158.178.236.241`, `kiro-rs-cn -> 154.86.30.10`; source and CN checks returned HTTP 200 for authenticated `/v1/models` using forced host resolution while public resolver propagation was still pending locally.

## 4I. zcode2api entry points
- Global/foreign API base: `https://zcode.zhangxuemin.work/v1`
- Global/foreign admin UI: `https://zcode.zhangxuemin.work/admin/login`
- Domestic/HK optimized API/admin entry: `https://zcode-cn.zhangxuemin.work`
- Source service now runs on `oracle-proxy` under `/root/containers/zcode2api`, published only on `127.0.0.1:18770` and reverse-proxied by `caddy-cpam`.
- HK edge on `hk-relay` only terminates TLS and reverse-proxies `zcode-cn.zhangxuemin.work` to `https://zcode.zhangxuemin.work` with origin Host/TLS SNI preserved.
- Earlier `ali-cloud` origin on `106.15.239.221:18084` was a mistaken first placement for this use case; it was stopped after migration on 2026-06-22 and should not be treated as live project topology.
- DNS added and verified on 2026-06-22: `zcode -> 158.178.236.241`, `zcode-cn -> 154.86.30.10`; both HTTPS entries returned HTTP 200 for `/admin/login` and `/admin/api/verify` after migration.


## 4J. proxy4reverse entry points
- Source service: `proxy4reverse` Docker container under `/root/containers/proxy4reverse`.
- Current binds are loopback-only, not public:
  - `127.0.0.1:18773` -> HTTP proxy data plane (`default`, `us-ca`, `us-ca-sticky-30` users mapped to provider profiles).
  - `127.0.0.1:18772` -> Web/API panel.
- Intended future CN edge shape, once provider health is fixed: HK Caddy/TCP edge such as `proxy4reverse-cn.zhangxuemin.work` -> Oracle `127.0.0.1:18773`, with authentication retained at proxy4reverse.
- Current blocker (2026-07-03): `us.cliproxy.io:1080` and `sg.cliproxy.io:1080` TCP-connect time out from `oracle-proxy`, `hk-relay`, and the local OpenClaw host. Smoke through `proxy4reverse` therefore returns HTTP 504 after authentication. Do not expose this service publicly until Cliproxy supplies a reachable forwarding machine/port or a working API/static endpoint.

## 4K. GPT Session Converter entry points
- Global/direct static tool: `https://gpt-session.zhangxuemin.work/`
- Domestic/HK optimized static tool: `https://gpt-session-cn.zhangxuemin.work/`
- Source static files live on `oracle-proxy` under `/root/containers/gpt-session-converter/docs`, mounted read-only into `caddy-cpam` as `/srv/gpt-session-converter`.
- HK edge on `hk-relay` only terminates TLS and reverse-proxies `gpt-session-cn.zhangxuemin.work` to `https://gpt-session.zhangxuemin.work` with origin Host/TLS SNI preserved.
- The app is browser-only static HTML/JS and does not persist submitted session/token JSON on the server.

## 5. Nginx / Proxy Layer Notes
### System nginx
- `nginx.service` is active
- enabled site: `/etc/nginx/sites-enabled/default`
- current config is the Debian default static site:
  - `listen 80 default_server`
  - `root /var/www/html`
  - `server_name _`
- No meaningful reverse-proxy mapping was found in system nginx during this pass

### caddy-cpam
- Containerized Caddy front door for `cpam.zhangxuemin.work`, `proxy-bak.zhangxuemin.work`, and `gptam.zhangxuemin.work`
- Config root: `/root/containers/caddy-cpam`
- Uses `network_mode: host` and owns public `80/443`; since 2026-06-07, Caddy is the public HTTP/HTTPS front door and proxies `proxy.zhangxuemin.work` back to 1Panel on `127.0.0.1:18080`
- For `gptam.zhangxuemin.work`, Caddy is configured to disable HTTP-01 and use TLS-ALPN-01 because public `:80` is occupied by 1Panel.
- GPT Account Manager access control is application-level (`GPT_ACCOUNT_MANAGER_REQUIRE_LOGIN=1`); Caddy should not carry a long-term Basic Auth wrapper for this app.
- Kiro-Go direct domain: `kiro.zhangxuemin.work` -> `127.0.0.1:18766` through `caddy-cpam`; CN/HK optimized domain: `kiro-cn.zhangxuemin.work` -> HK Caddy -> `https://kiro.zhangxuemin.work`.
- Kiro-RS direct domain: `kiro-rs.zhangxuemin.work` -> `127.0.0.1:18769` through `caddy-cpam`; exact `/` redirects to `/admin`. CN/HK optimized domain: `kiro-rs-cn.zhangxuemin.work` -> HK Caddy -> `https://kiro-rs.zhangxuemin.work`; exact `/` redirects to `/admin` on the HK edge to preserve the CN hostname.
- Kiro docs direct domain: `docs.zhangxuemin.work` -> static VitePress dist under `/root/containers/kiro-docs`; CN/HK optimized domain: `docs-cn.zhangxuemin.work` -> HK Caddy -> `https://docs.zhangxuemin.work`.
- GPT Session Converter direct domain: `gpt-session.zhangxuemin.work` -> static files under `/root/containers/gpt-session-converter/docs`; CN/HK optimized domain: `gpt-session-cn.zhangxuemin.work` -> HK Caddy -> `https://gpt-session.zhangxuemin.work`.

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
- By 2026-04-21, a focused Mihomo-side validation pass confirmed these directly usable public sing-box inbounds on this host:
  - `30002/udp` -> `hysteria2`
  - `30003/udp` -> `tuic`
  - `30005/tcp+udp` -> `shadowsocks` (`aes-128-gcm` family)
  - `30006/tcp+udp` -> `trojan`
- The same validation also showed that all of the above could still reach the expected public egress IP `158.178.236.241` from a fresh external Mihomo client.

### xray
- Config root: `/etc/v2ray-agent/xray/conf`
- Active ports observed:
  - `*:14391`
  - `127.0.0.1:45987`
- Recent logs show accepted traffic forwarded toward local `127.0.0.1:45987`
- By 2026-04-21, Mihomo smoke testing also confirmed the public `14391/tcp` Xray `VLESS Reality Vision` path was still usable from an external client and exited as `158.178.236.241`

### cloudflared
- Local listener previously observed on `127.0.0.1:20241`
- Exact tunnel config still TBD

## 7. Notes / Caveats
- This host does **not** currently have `ufw` installed (`ufw: command not found` at snapshot time).
- Several ports are directly bound on `0.0.0.0`; future hardening review is recommended.
- As of 2026-06-07, the legacy Grok register adapter listener `:15072` and Tavily registration adapter listener `:16072` are retired and should remain absent from `ss -ltnp` unless deliberately redeployed.
- Although the host still has a broader protocol surface than the current HK subscription exposes by default, at least five non-HK candidate exits on this machine are now externally verified and may be selectively published into private subscriptions when useful: `hysteria2`, `shadowsocks`, `trojan`, `tuic`, and `xray VLESS Reality Vision`.
- Network documentation is now better than the first pass, but cloudflared and the remaining untested sing-box/xray protocol variants still need a dedicated audit.


## Priority large-file transfer source role (2026-05-25)

This host is now prepared as the preferred foreign/Oracle-side temporary source for large-file movement into `self-server`.

Installed tooling:

```text
/usr/local/bin/dufs 0.46.0
/usr/local/sbin/openclaw-transfer-serve-dufs.sh
```

Operational stance:

- do not run a permanent public file-transfer service by default
- start authenticated dufs in the foreground only for the transfer window
- domestic `self-server` should pull with proxy variables unset and `curl -C -` resume enabled
- stop the helper and clean staging files after SHA256 verification

Canonical runbook: `../../large-file-transfer-priority-path.md`.

## 4E. Kiro docs static site entry points
- Global/direct public docs site: `https://docs.zhangxuemin.work/`
- Domestic/HK optimized docs site: `https://docs-cn.zhangxuemin.work/`
- Direct source service on this host: `caddy-cpam` static file server for `/root/containers/kiro-docs/site/docs/.vitepress/dist`, mounted read-only inside the Caddy container as `/srv/kiro-docs`.
- Source content: built from `Facetomyself/kiro` using only `使用说明.md` and required image assets under `图片/`.
- Security stance: public static documentation only; no visitor upload, no Kiro-Go admin/API proxying from the docs domain, and no secrets from Kiro-Go `.env` / `data/config.json` are copied into docs.
- Traffic stance: static assets are gzip/zstd encoded where supported; hashed assets/images carry long cache headers; HTML carries short cache headers for update agility.

### Kiro docs anti-abuse / rate-limit protection
- `docs.zhangxuemin.work` has Caddy JSON access logging to `/var/log/caddy/docs-access.log`.
- fail2ban jails protect the docs site from high-frequency page/static-asset scraping:
  - `openclaw-docs-general`: 180 requests / 60s -> 30m ban
  - `openclaw-docs-assets`: 90 static/image requests / 60s -> 1h ban
- The HK relay source IP is ignored on the source host to avoid banning domestic edge traffic.

## 4F. Card shop / card redeem entry points
- Global/direct public card shop: `https://card.zhangxuemin.work/`
- Domestic/HK optimized card shop: `https://card-cn.zhangxuemin.work/`
- Direct source service on this host: `card-shop` container, published only on `127.0.0.1:18767 -> 3000` and reverse-proxied by `caddy-cpam`.
- Runtime directory: `/root/containers/card-shop`
- Data directory: `/root/containers/card-shop/data` (`cardshop.db`, SQLite WAL enabled)
- Secret env file: `/root/containers/card-shop/.env` (`0600`; contains admin password and session secret; do not copy values into docs/chat)
- Public functions: card redeem and redeemed-card history query.
- Admin functions: authenticated backend, JSON batch generation, card search, card detail/history pages.
- Card code default: `KIRO-` prefix plus 32 human-safe random characters grouped with hyphens (about 160-bit entropy); generator enforces minimum 32 random bytes and allows up to 48.
- Query policy: only `redeemed` cards can return history; unredeemed/new cards return a non-disclosing failure.

### Card shop anti-abuse / rate-limit protection
- `card.zhangxuemin.work` has Caddy JSON access logging to `/var/log/caddy/card-access.log`.
- Application-level Express rate limits:
  - public routes: 60 requests / 60s
  - `/api/redeem` and `/api/query`: 20 requests / 60s
  - `/admin/*`: 40 requests / 60s
- fail2ban jails protect the source site:
  - `openclaw-card-general`: 180 requests / 60s -> 30m ban
  - `openclaw-card-api`: 40 `/api/redeem`, `/api/query`, or `/admin/login` requests / 60s -> 1h ban
- The HK relay source IP is ignored on the source host to avoid banning domestic edge traffic.

## 4G. GPT Card Shop entry points
- Global/direct public GPT card shop: `https://gpt-card.zhangxuemin.work/`
- Domestic/HK optimized GPT card shop: `https://gpt-card-cn.zhangxuemin.work/`
- Direct source service on this host: `gpt-card-shop` container, published only on `127.0.0.1:18768 -> 3000` and reverse-proxied by `caddy-cpam`.
- Runtime directory: `/root/containers/gpt-card-shop`
- Data directory: `/root/containers/gpt-card-shop/data` (`gpt-cardshop.db`, SQLite WAL enabled)
- Secret env file: `/root/containers/gpt-card-shop/.env` (`0600`; contains admin password and session secret; do not copy values into docs/chat)
- Public functions: multi-card redeem and download as CPA zip, sub2api merged JSON, or original JSON zip.
- DNS added and verified on 2026-06-07: `gpt-card -> 158.178.236.241`, `gpt-card-cn -> 154.86.30.10`; both source and CN health checks returned HTTP 200.



### HTTP redirect / 1Panel fronting fix (2026-06-07)
- Problem observed: `http://gpt-card.zhangxuemin.work/` returned the 1Panel page because 1Panel was configured as `ServerPort=80` and listened on `0.0.0.0:80`, while Caddy only owned HTTPS `:443`.
- Corrected shape:
  - backed up `/opt/1panel/db/1Panel.db` and `/root/containers/caddy-cpam/Caddyfile`;
  - changed 1Panel origin `ServerPort` from `80` to `18080`;
  - added Caddy site `proxy.zhangxuemin.work -> 127.0.0.1:18080`, preserving domain-based public 1Panel access;
  - removed Caddy global `auto_https disable_redirects`;
  - restarted 1Panel and `caddy-cpam`.
- Result:
  - Caddy owns public `:80` and `:443`;
  - `proxy.zhangxuemin.work` still serves the 1Panel UI via Caddy;
  - HTTP requests for app domains redirect to HTTPS with `308 Permanent Redirect`;
  - 1Panel itself is an origin behind Caddy on `:18080`, not a separate public entry the operator needs to remember.
- Verified:
  - `http://proxy.zhangxuemin.work/` -> `308` to `https://proxy.zhangxuemin.work/` and HTTPS returns 1Panel HTML;
  - `http://gpt-card.zhangxuemin.work/` -> `308` to `https://gpt-card.zhangxuemin.work/`;
  - `https://gpt-card.zhangxuemin.work/healthz` -> HTTP 200;
  - `http://gpt-card-cn.zhangxuemin.work/` -> `308` to HTTPS;
  - `https://gpt-card-cn.zhangxuemin.work/healthz` -> HTTP 200.
