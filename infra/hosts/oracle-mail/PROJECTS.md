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
- additional front-door route: `dreamhorse.eu.cc` -> reverse proxy to local `rbot` on `https://140.83.52.216:9527`
- TLS: automatic Let's Encrypt issuance handled by Caddy
- app runtime: Flask/Gunicorn on internal port `5000`
- compose action: `cd /opt/outlook-email-plus && docker compose up -d --build`

Operational notes:
- login is gated by `LOGIN_PASSWORD` in `.env` on first deployment
- `SECRET_KEY` is persisted in `.env`; losing it may affect decryption of stored sensitive fields
- current deployment intentionally does **not** repoint `autoconfig` / `autodiscover`
- Outlook OAuth can be postponed until actual import time
- Cloudflare temporary mailbox integration was evaluated on 2026-03-20 and intentionally deferred
- `Caddyfile` now multiplexes two HTTPS sites on shared `80/443`: the Outlook app on `mail.zhangxuemin.work`, and the `rbot` browser entrypoint on `dreamhorse.eu.cc`

### 1.1 Radiance OCI Bot (`rbot`) deployment
Located at:
- `/root/rbot/client_config`
- `/root/rbot/oci_api_key.pem`
- `/root/rbot/r_client`
- `/etc/systemd/system/rbot.service`

Deployment characteristics:
- systemd service: `rbot.service`
- local listener: `https://0.0.0.0:9527`
- public browser entrypoint: `https://dreamhorse.eu.cc`
- bot/web credentials currently bound through `radiance_helper_bot`
- current configured external URL: `local_address=https://dreamhorse.eu.cc`

Operational notes:
- direct browser access on `mail.zhangxuemin.work:9527` was abandoned because host-level HSTS for `mail.zhangxuemin.work` plus the app's self-signed `radiance` certificate caused hard browser failures
- the stable browser path is now via Caddy + Let's Encrypt on `dreamhorse.eu.cc`
- as of 2026-03-25 the client successfully loads Oracle config from `client_config` and logs `oracle配置获取成功 -> 当前profile为:DEFAULT,地区为:ap-singapore-2`
- the configured OCI private key lives at `/root/rbot/oci_api_key.pem`
- runtime currently warns `非闪电用户只能使用1个，请去【客户端管理】删除其他客户端`; this is an account/service-side limitation rather than a local process failure

### 2. Mailu deployment footprint
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

### 3. moemail repository
Located at:
- `/root/moemail`

Observed characteristics:
- Next.js app (`next 15.x`)
- Cloudflare/Wrangler deployment tooling
- DB migration scripts
- email worker scripts
- local `.env` present
- retained only as historical project context, not active public service

### 4. Deferred Cloudflare temp-mail integration note
Evaluated target:
- `dreamhunter2333/cloudflare_temp_email`

Conclusion:
- not directly compatible with Outlook Email Plus temporary-mail module
- Cloudflare project uses a different API and auth model (`x-custom-auth`, optional address password, JWT-based mailbox access)
- Outlook Email Plus temp-mail module expects a GPTMail-style backend (`X-API-Key` plus fixed `/api/generate-email`, `/api/emails`, `/api/email/:id` contract)
- integration is feasible later via a compatibility adapter layer, but is explicitly deferred for now

## Current operational conclusion
This host has been repurposed from a dormant/retired mail-stack machine into an active web-app host for `Outlook Email Plus`. Historical Mailu/moemail assets still matter as archived context, but the live public service on this host is now the containerized Outlook/IMAP management UI at `mail.zhangxuemin.work`.

## Next operational step
- if Outlook OAuth is needed in production, verify the Microsoft app registration uses the exact redirect URI configured in `/opt/outlook-email-plus/.env`
- decide later whether `autoconfig` / `autodiscover` should remain Cloudflare-only or be realigned to the host
- if Cloudflare temp-mail management is revisited later, prefer a small GPTMail-compatible adapter instead of patching Outlook Email Plus directly
- keep archived mail-stack directories for rollback/reference only; do not assume mail protocols are active
