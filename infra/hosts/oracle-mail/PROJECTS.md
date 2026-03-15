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
This host has a prepared Mailu mail-stack deployment plus a separate `moemail` codebase, but neither appears to be actively serving traffic right now.

## Next operational step
- document Mailu as dormant/inactive rather than active
- inspect why Mailu is down before any attempt to start it
- inspect `moemail` README / deployment docs to understand whether it belongs on this host or is just a working tree
