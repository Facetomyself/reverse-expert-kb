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

### 2. Historical Mailu note
Previously observed Mailu facts before final deletion:
- root domain: `zhangxuemin.work`
- historical hostname: `mail.zhangxuemin.work`
- the old stack was capable of owning classic mail ports (`25/465/587/110/995/143/993/4190`) if started

Cleanup outcome on 2026-04-14 after explicit user confirmation that Mailu is no longer used:
- deleted host-side Mailu persistent data directory: `/mailu`
- deleted archived Mailu copy: `/root/retired-services/2026-03-15/mailu`
- removed historical Mailu DKIM record from Cloudflare live zone: `dkim._domainkey.zhangxuemin.work`

Current reality:
- no Mailu files should be treated as part of the live host state anymore
- do not assume Mailu is available for rollback unless it is reintroduced later from a fresh deployment path

### 3. Historical moemail note
Previously observed before final cleanup:
- Next.js app (`next 15.x`)
- Cloudflare/Wrangler deployment tooling
- DB migration scripts
- email worker scripts
- project documentation/code path indicated temporary-address sending via **Resend**
- archived `.env` snapshot had `CUSTOM_DOMAIN=""`, so the saved checkout itself did not prove which custom domain was last bound in production

Cleanup outcome on 2026-04-14 after explicit user request to clean moemail residuals:
- deleted archived moemail copy: `/root/retired-services/2026-03-15/moemail`
- deleted 3 moemail-specific Wrangler logs under `/root/.config/.wrangler/logs/`
- removed historical moemail / Resend DKIM record from Cloudflare live zone: `resend._domainkey.zhangxuemin.work`

Current reality:
- no moemail files should be treated as part of the live host state anymore
- moemail should now be treated as historical context only, not a retained local fallback

### 4. Deferred Cloudflare temp-mail integration note
Evaluated target:
- `dreamhunter2333/cloudflare_temp_email`

Conclusion:
- not directly compatible with Outlook Email Plus temporary-mail module
- Cloudflare project uses a different API and auth model (`x-custom-auth`, optional address password, JWT-based mailbox access)
- Outlook Email Plus temp-mail module expects a GPTMail-style backend (`X-API-Key` plus fixed `/api/generate-email`, `/api/emails`, `/api/email/:id` contract)
- integration is feasible later via a compatibility adapter layer, but is explicitly deferred for now

## Current operational conclusion
This host has been repurposed from a dormant/retired mail-stack machine into an active web-app host for `Outlook Email Plus`. Both Mailu and moemail should now be treated as removed local history rather than retained host components. The live public service on this host is the containerized Outlook/IMAP management UI at `mail.zhangxuemin.work`.

## Next operational step
- if Outlook OAuth is needed in production, verify the Microsoft app registration uses the exact redirect URI configured in `/opt/outlook-email-plus/.env`
- decide later whether `autoconfig` / `autodiscover` should be reintroduced for this host or remain absent from the live zone
- if Cloudflare temp-mail management is revisited later, prefer a small GPTMail-compatible adapter instead of patching Outlook Email Plus directly
- keep only high-level historical context that still matters; do not assume mail protocols are active
