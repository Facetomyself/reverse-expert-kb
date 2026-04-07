#!/bin/sh
set -eu

REPO_ROOT="/root/.openclaw/workspace"
OWNER="Facetomyself"
REPO="reverse-expert-kb"
SPLIT_BRANCH="kb-sync-temp"
PREFIX="research/reverse-expert-kb"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
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
BACKUP_REF="refs/heads/archive/pre-subtree-resync-${STAMP}"

cd "$REPO_ROOT"

if ! gh auth status >/dev/null 2>&1; then
  echo "gh auth is not ready. Run: gh auth login"
  exit 1
fi

if git show-ref --verify --quiet "refs/heads/$SPLIT_BRANCH"; then
  git branch -D "$SPLIT_BRANCH" >/dev/null 2>&1 || true
fi

REMOTE_MAIN_SHA="$(git ls-remote "$REMOTE_URL" refs/heads/main | awk '{print $1}')"
if [ -z "$REMOTE_MAIN_SHA" ]; then
  echo "remote main branch not found for ${OWNER}/${REPO}" >&2
  exit 1
fi

git subtree split --prefix="$PREFIX" -b "$SPLIT_BRANCH" >/dev/null
LOCAL_SPLIT_SHA="$(git rev-parse "$SPLIT_BRANCH")"

if [ "$REMOTE_MAIN_SHA" = "$LOCAL_SPLIT_SHA" ]; then
  echo "Reverse KB archival repo already in sync at $LOCAL_SPLIT_SHA"
  exit 0
fi

echo "Backing up remote main ${REMOTE_MAIN_SHA} to ${BACKUP_REF#refs/heads/}"
git push "$REMOTE_URL" "$REMOTE_MAIN_SHA:$BACKUP_REF" >/dev/null

echo "Updating remote main from $REMOTE_MAIN_SHA -> $LOCAL_SPLIT_SHA"
git push --force-with-lease=main:"$REMOTE_MAIN_SHA" "$REMOTE_URL" "$SPLIT_BRANCH":main >/dev/null

echo "Synced $PREFIX -> https://github.com/${OWNER}/${REPO} (branch main); previous remote main saved as ${BACKUP_REF#refs/heads/}"
