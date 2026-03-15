#!/bin/sh
set -eu

REPO_ROOT="/root/.openclaw/workspace"
OWNER="Facetomyself"
REPO="reverse-expert-kb"
SPLIT_BRANCH="kb-sync-temp"
PREFIX="research/reverse-expert-kb"
TOKEN="$(python3 - <<'PY'
from pathlib import Path
p = Path('/root/.config/gh/hosts.yml')
text = p.read_text()
for line in text.splitlines():
    s = line.strip()
    if s.startswith('oauth_token:'):
        print(s.split(':',1)[1].strip())
        break
else:
    raise SystemExit('oauth_token not found in ~/.config/gh/hosts.yml')
PY
)"
REMOTE_URL="https://x-access-token:${TOKEN}@github.com/${OWNER}/${REPO}.git"

cd "$REPO_ROOT"

if ! gh auth status >/dev/null 2>&1; then
  echo "gh auth is not ready. Run: gh auth login"
  exit 1
fi

if git show-ref --verify --quiet "refs/heads/$SPLIT_BRANCH"; then
  git branch -D "$SPLIT_BRANCH" >/dev/null 2>&1 || true
fi

git subtree split --prefix="$PREFIX" -b "$SPLIT_BRANCH"
git push "$REMOTE_URL" "$SPLIT_BRANCH":main

echo "Synced $PREFIX -> https://github.com/${OWNER}/${REPO} (branch main)"
