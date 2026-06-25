#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage: openclaw-transfer-serve-dufs.sh <directory> [port]

Start an authenticated foreground dufs file source for large-file transfer.
Designed for foreign/Oracle-side serving; domestic receivers should pull with
openclaw-transfer-pull-no-proxy.sh or equivalent curl -C - command.

Defaults:
  port: 18080
  auth user: transfer

Security model:
  - random password is generated per run
  - service runs in foreground; stop with Ctrl-C or by killing this process
  - do not leave it running after transfer
EOF
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" || $# -lt 1 ]]; then
  usage
  exit $([[ $# -lt 1 ]] && echo 2 || echo 0)
fi

DIR=$1
PORT=${2:-18080}
USER_NAME=${OPENCLAW_TRANSFER_USER:-transfer}

if [[ ! -d "$DIR" ]]; then
  echo "ERROR: directory does not exist: $DIR" >&2
  exit 2
fi
if ! command -v dufs >/dev/null 2>&1; then
  echo "ERROR: dufs not found in PATH" >&2
  exit 2
fi
if ss -ltn "sport = :$PORT" | awk 'NR>1 {found=1} END {exit found?0:1}'; then
  echo "ERROR: port already listening: $PORT" >&2
  ss -ltnp "sport = :$PORT" >&2 || true
  exit 2
fi

PASS=$(python3 - <<'PY'
import secrets, string
alphabet = string.ascii_letters + string.digits
print(''.join(secrets.choice(alphabet) for _ in range(24)))
PY
)
HOST_IP=$(curl -fsS --connect-timeout 3 --max-time 5 https://ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')

cat >&2 <<EOF
OpenClaw transfer source starting
Directory: $DIR
Port:      $PORT
Auth:      $USER_NAME:$PASS
URL:       http://$HOST_IP:$PORT/

Receiver example:
  openclaw-transfer-pull-no-proxy.sh 'http://$HOST_IP:$PORT/<file>' '<output-file>' '<optional-sha256>' '$USER_NAME:$PASS'

Raw curl example:
  env -u http_proxy -u https_proxy -u all_proxy -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY \\
    curl -fL -C - -u '$USER_NAME:$PASS' -o '<output-file>' 'http://$HOST_IP:$PORT/<file>'

Stop this server with Ctrl-C when done.
EOF

exec dufs "$DIR" \
  --bind 0.0.0.0 \
  --port "$PORT" \
  --auth "$USER_NAME:$PASS@/:rw" \
  --allow-hash
