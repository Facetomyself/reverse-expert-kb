# oracle-mail / PROJECTS

## Current confirmed assets
### 1. Outlook Email Plus deployment
Located at:
- `/opt/outlook-email-plus/docker-compose.yml`
- `/opt/outlook-email-plus/.env`
- `/opt/outlook-email-plus/Caddyfile`
- `/opt/outlook-email-plus/src`
- persistent data: `/opt/outlook-email-plus/app-data`
- Caddy state/certs: `/opt/outlook-email-plus/caddy`

Deployment characteristics:
- containers: `outlook-email-plus-app`, `outlook-email-plus-caddy`
- public domain: `mail.zhangxuemin.work`
- TLS: automatic Let's Encrypt issuance handled by Caddy
- app runtime: Flask/Gunicorn on internal port `5000`
- compose action: `cd /opt/outlook-email-plus && docker compose up -d --build`

Operational notes:
- login is gated by `LOGIN_PASSWORD` in `.env` on first deployment
- `SECRET_KEY` is persisted in `.env`; losing it may affect decryption of stored sensitive fields
- current deployment intentionally does **not** repoint `autoconfig` / `autodiscover`
- Outlook OAuth can be postponed until actual import time
- Cloudflare temporary mailbox integration was evaluated on 2026-03-20 and intentionally deferred


### 2. WA App deployment
Located at:
- `/opt/wa-app/docker-compose.yml`
- `/opt/wa-app/.env`
- persistent data: Docker volume `wa-app-data` mounted at `/var/lib/wa-app`

Deployment characteristics:
- container: `wa-app`
- image: `ghcr.io/pood1e/wa-app-service:latest`
- public source/global domain: `wa.zhangxuemin.work`
- domestic/HK edge domain: `wa-cn.zhangxuemin.work` via `hk-relay`
- dashboard: Docker-internal `8080`, exposed publicly only through the shared `outlook-email-plus-caddy` reverse proxy
- gRPC: Docker-internal `50091`, no host port published
- compose action: `cd /opt/wa-app && docker compose up -d wa-app`

Runtime proxy configuration:
- configured in `/opt/wa-app/.env`
- current `WA_COMMON_PROXY`: `socks5://VbyYbQEAVhrp:lPgcIWCHPKQ9@204.237.153.49:60088/`
- updated on 2026-06-16 and verified in the recreated `wa-app` container environment

Operational notes:
- login is gated by `WA_APP_AUTH_PASSWORD` in `/opt/wa-app/.env`
- the app shares the external Docker network `outlook-email-plus_default` so Caddy can reverse-proxy to `wa-app:8080`
- keep `50091` internal unless there is a specific gRPC exposure requirement

### 3. FileCodeBox deployment
Located at:
- `/opt/filecodebox/docker-compose.yml`
- persistent data: `/opt/filecodebox/data`

Deployment characteristics:
- container: `filecodebox`
- image: `lanol/filecodebox:latest`
- host/source port: `18085`, firewall-restricted to `hk-relay` (`154.86.30.10`) plus localhost
- domestic/HK entry domain: `drop-cn.zhangxuemin.work` via `hk-relay` Caddy
- FileCodeBox provides the application-level authentication/initialization; no extra HK Basic Auth is layered on top
- compose action: `cd /opt/filecodebox && /usr/local/bin/docker-compose up -d`

Operational notes:
- FileCodeBox is suitable for longer-lived personal file/text handoff than ad-hoc Python upload scripts: it supports extraction codes, expiry by time/count, admin management, local persistent storage, and curl uploads.
- Back up `/opt/filecodebox/data` to preserve SQLite/app data and uploaded files.

### 4. Mailu deployment footprint
Located at:
- `/root/mailu/docker-compose.yml`
- `/root/mailu/mailu.env`

Mailu configuration indicates:
- `DOMAIN=zhangxuemin.work`
- `HOSTNAMES=mail.zhangxuemin.work`
- `TLS_FLAVOR=letsencrypt`
- `ADMIN=true`
- `WEBMAIL=none`
- `API=true`
- `WEBDAV=radicale`
- `ANTIVIRUS=clamav`
- `FETCHMAIL_ENABLED=true`

Mailu compose exposes, if started:
- `80`, `443`
- `25`, `465`, `587`
- `110`, `995`
- `143`, `993`
- `4190`

Current reality:
- this stack remains archived / inactive
- do not assume Mailu is serving traffic on the host

### 5. moemail repository
Located at:
- `/root/moemail`

Observed characteristics:
- Next.js app (`next 15.x`)
- Cloudflare/Wrangler deployment tooling
- DB migration scripts
- email worker scripts
- local `.env` present
- retained only as historical project context, not active public service

### 6. Deferred Cloudflare temp-mail integration note
Evaluated target:
- `dreamhunter2333/cloudflare_temp_email`

Conclusion:
- not directly compatible with Outlook Email Plus temporary-mail module
- Cloudflare project uses a different API and auth model (`x-custom-auth`, optional address password, JWT-based mailbox access)
- Outlook Email Plus temp-mail module expects a GPTMail-style backend (`X-API-Key` plus fixed `/api/generate-email`, `/api/emails`, `/api/email/:id` contract)
- integration is feasible later via a compatibility adapter layer, but is explicitly deferred for now

## Current operational conclusion
This host has been repurposed from a dormant/retired mail-stack machine into an active web-app host for `Outlook Email Plus`. Historical Mailu/moemail assets still matter as archived context, but the live public service on this host is now the containerized Outlook/IMAP management UI at `mail.zhangxuemin.work`, plus the `wa-app` dashboard at `wa.zhangxuemin.work` / `wa-cn.zhangxuemin.work`.

## Next operational step
- if Outlook OAuth is needed in production, verify the Microsoft app registration uses the exact redirect URI configured in `/opt/outlook-email-plus/.env`
- decide later whether `autoconfig` / `autodiscover` should remain Cloudflare-only or be realigned to the host
- if Cloudflare temp-mail management is revisited later, prefer a small GPTMail-compatible adapter instead of patching Outlook Email Plus directly
- keep archived mail-stack directories for rollback/reference only; do not assume mail protocols are active
