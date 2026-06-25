#!/bin/sh
set -eu

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <host-name> <ssh-alias> [provider]" >&2
  exit 1
fi

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
NAME=$1
ALIAS=$2
PROVIDER=${3:-unknown}
DIR="$ROOT/hosts/$NAME"
TEMPLATE_DIR="$ROOT/templates/host-template"

if [ -e "$DIR" ]; then
  echo "Host directory already exists: $DIR" >&2
  exit 1
fi

mkdir -p "$DIR/projects"
for f in HOST.md NETWORK.md PROJECTS.md CHANGELOG.md; do
  sed \
    -e "s/<host-name>/$NAME/g" \
    -e "s/<ssh-alias>/$ALIAS/g" \
    -e "s/<provider>/$PROVIDER/g" \
    "$TEMPLATE_DIR/$f" > "$DIR/$f"
done

cat <<EOF
Created host skeleton:
- $DIR/HOST.md
- $DIR/NETWORK.md
- $DIR/PROJECTS.md
- $DIR/CHANGELOG.md

Next steps:
1. Update inventory.yaml with name=$NAME, ssh_alias=$ALIAS
2. Update host-status.yaml with lifecycle / reachability / importance
3. Fill in HOST.md / NETWORK.md / PROJECTS.md
4. Commit in infra repo; post-commit hook should auto-push
EOF
