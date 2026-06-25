#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
HOST_ALIAS=${HOST_ALIAS:-self-server-44005}
APP_DIR=${APP_DIR:-/opt/prompt-optimizer-studio}
OUT_DIR=${OUT_DIR:-$ROOT/reports/prompt-optimizer-studio}
STAMP=$(date +%F)
OUT_FILE="$OUT_DIR/$STAMP-self-server-44005.md"
mkdir -p "$OUT_DIR"

TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT

ssh "$HOST_ALIAS" '
  set -eu
  echo "host: $(hostname)"
  echo "time: $(date -Is)"
  echo ""
  echo "== docker ps =="
  docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | (grep -E "prompt-optimizer|NAMES" || true)
  echo ""
  echo "== health =="
  curl -i --max-time 15 http://127.0.0.1:30001/api/health || true
  echo ""
  echo "== listeners =="
  ss -ltnp | grep -E ":(30001|30008)\\b" || true
  echo ""
  echo "== resources =="
  df -h /
  echo ""
  free -h
  echo ""
  echo "== compose files =="
  cd /opt/prompt-optimizer-studio
  sed -n "1,120p" docker-compose.yml
' > "$TMP"

{
  echo "# prompt-optimizer-studio health check"
  echo
  printf -- '- target: `%s`\n' "$HOST_ALIAS"
  echo "- generated_at: $(date -Is)"
  echo
  cat "$TMP"
} > "$OUT_FILE"

printf '%s\n' "$OUT_FILE"
