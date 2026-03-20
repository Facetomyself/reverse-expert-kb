# oracle-mail / PROJECTS

## Current confirmed assets
### 1. Mailu deployment footprint
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

But currently:
- `docker compose ps` shows no running Mailu services
- `docker ps -a` is empty

### 2. moemail repository
Located at:
- `/root/moemail`

Observed characteristics:
- Next.js app (`next 15.x`)
- Cloudflare/Wrangler deployment tooling
- DB migration scripts
- email worker scripts
- local `.env` present

## Current operational conclusion
This host has been repurposed from a dormant/retired mail-stack machine into an active web-app host for `Outlook Email Plus`. Historical Mailu/moemail assets still matter as archived context, but the live public service on this host is now the containerized Outlook/IMAP management UI at `mail.zhangxuemin.work`.

## Next operational step
- if Outlook OAuth is needed in production, verify the Microsoft app registration uses the exact redirect URI configured in `/opt/outlook-email-plus/.env`
- decide later whether `autoconfig` / `autodiscover` should remain Cloudflare-only or be realigned to the host
- keep archived mail-stack directories for rollback/reference only; do not assume mail protocols are active
d characteristics:
- Next.js app (`next 15.x`)
- Cloudflare/Wrangler deployment tooling
- DB migration scripts
- email worker scripts
- local `.env` present

## Current operational conclusion
This host had a prepared Mailu mail-stack deployment plus a separate `moemail` codebase, but neither was actively serving traffic. Per user instruction, both local stacks were retired/archived on 2026-03-15 because a different Cloudflare-based temporary mail deployment is now in use.

## Next operational step
- treat this host as a retired/staging mail host unless the user later decides to revive it
- keep archived directories only for rollback/reference
- avoid assuming DNS currently matches active service reality
