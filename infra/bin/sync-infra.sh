#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

REPO_URL=$(git remote get-url origin)
case "$REPO_URL" in
  https://github.com/*)
    ;;
  *)
    echo "Unsupported remote: $REPO_URL" >&2
    exit 1
    ;;
esac

TOKEN=$(python3 - <<'PY'
from pathlib import Path
p = Path.home()/'.config/gh/hosts.yml'
if not p.exists():
    raise SystemExit(1)
text = p.read_text()
for line in text.splitlines():
    s = line.strip()
    if s.startswith('oauth_token:'):
        print(s.split(':',1)[1].strip())
        break
else:
    raise SystemExit(1)
PY
)

if [ -z "$TOKEN" ]; then
  echo "No GitHub token available via ~/.config/gh/hosts.yml" >&2
  exit 1
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD)
CLEAN=${REPO_URL#https://github.com/}

echo "[sync-infra] pushing $BRANCH -> $CLEAN"
git push "https://x-access-token:${TOKEN}@github.com/${CLEAN}" "$BRANCH"
echo "[sync-infra] done"
