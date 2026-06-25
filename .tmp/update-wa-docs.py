from pathlib import Path

# Cloudflare baseline refresh from verified live snapshot
Path('infra/cloudflare-dns/baseline-records.json').write_text(Path('/root/.openclaw/workspace/.tmp/cloudflare-dns-audit/live-records-2026-06-16-wa.json').read_text())
Path('infra/cloudflare-dns/baseline-summary.md').write_text(Path('/root/.openclaw/workspace/.tmp/cloudflare-dns-audit/live-summary-2026-06-16-wa.md').read_text())

# inventory domains
p = Path('infra/inventory.yaml')
s = p.read_text()
s = s.replace('''    domains:\n      - mail.zhangxuemin.work\n    docs:\n''', '''    domains:\n      - mail.zhangxuemin.work\n      - wa.zhangxuemin.work\n    docs:\n''')
s = s.replace('''      - gpt-card-cn.zhangxuemin.work\n    docs:\n''', '''      - gpt-card-cn.zhangxuemin.work\n      - wa-cn.zhangxuemin.work\n    docs:\n''')
p.write_text(s)

# oracle-mail HOST
p = Path('infra/hosts/oracle-mail/HOST.md')
s = p.read_text()
s = s.replace('''- `mail.zhangxuemin.work` is currently live as the Outlook Email Plus web app via Docker Compose + Caddy\n- active containers live under `/opt/outlook-email-plus`\n- this host should be treated as an application host, not as part of any overlay-network control plane\n''', '''- `mail.zhangxuemin.work` is currently live as the Outlook Email Plus web app via Docker Compose + Caddy\n- `wa.zhangxuemin.work` is currently live as the WA app global/source dashboard entry, also fronted by the existing Outlook Email Plus Caddy container\n- active Outlook containers live under `/opt/outlook-email-plus`; WA app runtime lives under `/opt/wa-app`\n- this host should be treated as an application host, not as part of any overlay-network control plane\n''')
p.write_text(s)

# oracle-mail NETWORK
p = Path('infra/hosts/oracle-mail/NETWORK.md')
s = p.read_text()
s = s.replace('''- Primary domain: `mail.zhangxuemin.work`\n''', '''- Primary domain: `mail.zhangxuemin.work`\n- WA app global/source domain: `wa.zhangxuemin.work`\n''')
s = s.replace('''- `mail.zhangxuemin.work` is live on this host as the `Outlook Email Plus` web app\n- public `80/443` are owned by the `outlook-email-plus-caddy` container\n''', '''- `mail.zhangxuemin.work` is live on this host as the `Outlook Email Plus` web app\n- `wa.zhangxuemin.work` is live on this host as the WA app global/source dashboard entry; Caddy reverse-proxies to container `wa-app:8080`\n- domestic/HK optimized entry is `wa-cn.zhangxuemin.work` on `hk-relay`, reverse-proxied back to `https://wa.zhangxuemin.work`\n- public `80/443` are owned by the `outlook-email-plus-caddy` container\n''')
s = s.replace('''This host is no longer a dormant mail-stack candidate: runtime now clearly matches an active web application host for `mail.zhangxuemin.work`, while traditional mail protocols remain intentionally inactive.\n''', '''This host is no longer a dormant mail-stack candidate: runtime now clearly matches an active web application host for `mail.zhangxuemin.work` plus the WA app source entry `wa.zhangxuemin.work`, while traditional mail protocols remain intentionally inactive.\n''')
p.write_text(s)

# oracle-mail PROJECTS add WA section before historical Mailu
p = Path('infra/hosts/oracle-mail/PROJECTS.md')
s = p.read_text()
marker = '''### 2. Historical Mailu note\n'''
wa = '''### 2. WA app deployment\nLocated at:\n- `/opt/wa-app/docker-compose.yml`\n- `/opt/wa-app/.env`\n- persistent data volume: `wa-app-data` mounted at container path `/var/lib/wa-app`\n\nDeployment characteristics:\n- container: `wa-app`\n- image: `ghcr.io/pood1e/wa-app-service:latest`\n- global/source public domain: `wa.zhangxuemin.work`\n- CN/HK edge domain: `wa-cn.zhangxuemin.work` on `hk-relay`, reverse-proxied to `https://wa.zhangxuemin.work`\n- dashboard origin inside Docker: `wa-app:8080` on the shared `outlook-email-plus_default` Docker network\n- gRPC listener remains container-internal on `:50091`; no public host port is published\n- compose action: `cd /opt/wa-app && docker compose up -d`\n\nOperational notes:\n- dashboard login is gated by `WA_APP_AUTH_PASSWORD` in `/opt/wa-app/.env`; do not commit the password value\n- PostgreSQL and Redis are not enabled; the service currently uses embedded SQLite/runtime persistence\n- existing `outlook-email-plus-caddy` owns public `80/443` and serves this route; WA app has no direct host port publication\n\n'''
if wa not in s:
    s = s.replace(marker, wa + marker)
    s = s.replace('### 2. Historical Mailu note', '### 3. Historical Mailu note')
    s = s.replace('### 3. Historical moemail note', '### 4. Historical moemail note')
    s = s.replace('### 4. Deferred Cloudflare temp-mail integration note', '### 5. Deferred Cloudflare temp-mail integration note')
s = s.replace('''The live public service on this host is the containerized Outlook/IMAP management UI at `mail.zhangxuemin.work`.\n''', '''The live public services on this host are the containerized Outlook/IMAP management UI at `mail.zhangxuemin.work` and the WA app dashboard at `wa.zhangxuemin.work` / `wa-cn.zhangxuemin.work`.\n''')
p.write_text(s)

# oracle-mail changelog prepend
p = Path('infra/hosts/oracle-mail/CHANGELOG.md')
s = p.read_text()
entry = '''# oracle-mail / CHANGELOG\n\n- 2026-06-16: Deployed `wa-app` on `oracle-mail` under `/opt/wa-app` using Docker Compose and image `ghcr.io/pood1e/wa-app-service:latest`. Runtime container `wa-app` exposes only Docker-internal `8080` dashboard and `50091` gRPC; no direct host ports are published. Existing `outlook-email-plus-caddy` now serves `wa.zhangxuemin.work` by reverse-proxying to `wa-app:8080`, while `wa-cn.zhangxuemin.work` is served from `hk-relay` as the domestic/HK edge. Validation: both `https://wa.zhangxuemin.work/` and `https://wa-cn.zhangxuemin.work/` returned the expected HTTP 303 login redirect.\n'''
if s.startswith('# oracle-mail / CHANGELOG\n') and 'Deployed `wa-app` on `oracle-mail`' not in s:
    s = s.replace('# oracle-mail / CHANGELOG\n', entry, 1)
p.write_text(s)

# hk-relay NETWORK
p = Path('infra/hosts/hk-relay/NETWORK.md')
s = p.read_text()
s = s.replace('''  - `card-cn.zhangxuemin.work`\n''', '''  - `card-cn.zhangxuemin.work`\n  - `wa-cn.zhangxuemin.work`\n''')
s = s.replace('''- `https://card-cn.zhangxuemin.work/` -> CN/HK TLS edge for Card Shop, reverse-proxied to `https://card.zhangxuemin.work/`\n''', '''- `https://card-cn.zhangxuemin.work/` -> CN/HK TLS edge for Card Shop, reverse-proxied to `https://card.zhangxuemin.work/`\n- `https://wa-cn.zhangxuemin.work/` -> CN/HK TLS edge for WA app, reverse-proxied to `https://wa.zhangxuemin.work/`\n''')
s = s.replace('''  - Card Shop global/source: `card.zhangxuemin.work`\n''', '''  - Card Shop global/source: `card.zhangxuemin.work`\n  - WA app global/source: `wa.zhangxuemin.work`\n''')
p.write_text(s)

# hk-relay changelog prepend while preserving existing content
p = Path('infra/hosts/hk-relay/CHANGELOG.md')
s = p.read_text()
entry = '''# hk-relay / CHANGELOG\n\n## 2026-06-16 — WA app CN/HK edge added\n- Added live Cloudflare DNS-only A records:\n  - `wa.zhangxuemin.work` -> `140.83.52.216` (`oracle-mail` source/global entry)\n  - `wa-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay` CN/HK edge)\n- Added Caddy reverse-proxy site on `hk-relay`:\n  - `wa-cn.zhangxuemin.work` -> `https://wa.zhangxuemin.work` (`oracle-mail` WA app origin)\n- Verification: both `https://wa.zhangxuemin.work/` and `https://wa-cn.zhangxuemin.work/` returned HTTP 303 to `/login?next=%2F`, matching the password-protected dashboard behavior.\n- Direct/global source remains available for overseas/global fallback; the `*-cn` route is the domestic/HK optimized entrypoint.\n\n'''
if 'WA app CN/HK edge added' not in s:
    if s.startswith('# hk-relay / CHANGELOG\n\n'):
        s = s.replace('# hk-relay / CHANGELOG\n\n', entry, 1)
    else:
        s = entry + s
p.write_text(s)
