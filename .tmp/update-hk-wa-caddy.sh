set -eu
cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.bak.$(date +%Y%m%d%H%M%S)
python3 - <<'PY'
from pathlib import Path
p = Path('/etc/caddy/Caddyfile')
s = p.read_text()
block = '''

# CN edge endpoint for WA app. Origin stays on oracle-mail; HK terminates TLS and forwards dashboard traffic.
wa-cn.zhangxuemin.work {
    encode gzip zstd
    header {
        X-Content-Type-Options "nosniff"
        Referrer-Policy "strict-origin-when-cross-origin"
    }
    reverse_proxy https://wa.zhangxuemin.work {
        header_up Host wa.zhangxuemin.work
        transport http {
            tls_server_name wa.zhangxuemin.work
        }
        flush_interval -1
    }
}
'''
if 'wa-cn.zhangxuemin.work {' not in s:
    p.write_text(s.rstrip() + block)
PY
caddy validate --config /etc/caddy/Caddyfile
systemctl reload caddy
sed -n '/wa-cn.zhangxuemin.work/,+20p' /etc/caddy/Caddyfile
