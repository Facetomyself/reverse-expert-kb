set -eu
cd /opt/outlook-email-plus
cp Caddyfile Caddyfile.bak.$(date +%Y%m%d%H%M%S)
python3 - <<'PY'
from pathlib import Path
p = Path('Caddyfile')
s = p.read_text()
block = '''

# WA app global/source entry. Runtime lives in /opt/wa-app; dashboard auth is handled by wa-app.
wa.zhangxuemin.work {
    encode gzip zstd
    reverse_proxy wa-app:8080 {
        flush_interval -1
    }
}
'''
if 'wa.zhangxuemin.work {' not in s:
    p.write_text(s.rstrip() + block)
PY
docker compose exec -T caddy caddy validate --config /etc/caddy/Caddyfile
docker compose exec -T caddy caddy reload --config /etc/caddy/Caddyfile
sed -n '1,140p' Caddyfile
