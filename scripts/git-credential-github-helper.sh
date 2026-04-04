#!/bin/sh
set -eu

action=${1:-get}
case "$action" in
  get|fill) ;;
  store|erase|approve|reject)
    exit 0
    ;;
  *)
    exit 0
    ;;
esac

protocol=''
host=''
while IFS='=' read -r key value; do
  [ -n "$key" ] || break
  case "$key" in
    protocol) protocol=$value ;;
    host) host=$value ;;
  esac
done

[ "$protocol" = "https" ] || exit 0
[ "$host" = "github.com" ] || exit 0

python3 - <<'PY'
from pathlib import Path
p = Path.home() / '.config' / 'gh' / 'hosts.yml'
if not p.exists():
    raise SystemExit(0)
text = p.read_text()
token = None
current = None
for raw in text.splitlines():
    line = raw.rstrip('\n')
    if not line.strip():
        continue
    if not line.startswith(' ') and line.endswith(':'):
        current = line[:-1].strip()
        continue
    if current == 'github.com':
        s = line.strip()
        if s.startswith('oauth_token:'):
            token = s.split(':', 1)[1].strip()
            break
if not token:
    raise SystemExit(0)
print('username=x-access-token')
print(f'password={token}')
print()
PY
