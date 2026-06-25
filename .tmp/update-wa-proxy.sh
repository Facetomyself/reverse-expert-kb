set -eu
cd /opt/wa-app
stamp=$(date +%Y%m%d%H%M%S)
cp -a .env ".env.bak-proxy-${stamp}"
python3 - <<'PY'
from pathlib import Path
p = Path('.env')
proxy = 'socks5://VbyYbQEAVhrp:lPgcIWCHPKQ9@204.237.153.49:60088/'
lines = p.read_text().splitlines()
out = []
seen = False
for line in lines:
    if line.startswith('WA_COMMON_PROXY='):
        out.append('WA_COMMON_PROXY=' + proxy)
        seen = True
    else:
        out.append(line)
if not seen:
    out.append('WA_COMMON_PROXY=' + proxy)
p.write_text('\n'.join(out) + '\n')
PY
chmod 600 .env
if docker compose version >/dev/null 2>&1; then
  dc='docker compose'
else
  dc='docker-compose'
fi
$dc up -d wa-app
sleep 3
echo '--- compose-ps'
$dc ps
echo '--- container-env'
docker exec wa-app sh -c 'env | grep -E "^WA_COMMON_PROXY=|^WA_APP_"' | sed -E 's#(socks5://[^:]+:)[^@]+@#\1***@#'
echo '--- logs'
docker logs --tail 40 wa-app 2>&1 | sed -E 's#(socks5://[^:]+:)[^@]+@#\1***@#'
