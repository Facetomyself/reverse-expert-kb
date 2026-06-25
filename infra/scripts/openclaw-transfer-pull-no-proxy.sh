#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage: openclaw-transfer-pull-no-proxy.sh <url> <output-file> [sha256|-] [user:pass]

Pull a large file with proxy environment disabled, resume enabled, and optional
SHA256 verification. Intended for self-server/domestic side pulling from a
foreign/Oracle temporary source.

Examples:
  openclaw-transfer-pull-no-proxy.sh http://158.178.236.241:18080/big.tar ./big.tar <sha256> transfer:password
  openclaw-transfer-pull-no-proxy.sh http://158.178.236.241:18080/big.tar ./big.tar - transfer:password
EOF
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" || $# -lt 2 ]]; then
  usage
  exit $([[ $# -lt 2 ]] && echo 2 || echo 0)
fi

URL=$1
OUT=$2
EXPECTED_SHA=${3:-}
AUTH=${4:-}

mkdir -p "$(dirname "$OUT")"

CURL_ARGS=(
  -fL
  -C -
  --connect-timeout "${OPENCLAW_TRANSFER_CONNECT_TIMEOUT:-15}"
  --max-time "${OPENCLAW_TRANSFER_MAX_TIME:-0}"
  --retry "${OPENCLAW_TRANSFER_RETRY:-5}"
  --retry-delay "${OPENCLAW_TRANSFER_RETRY_DELAY:-3}"
  -o "$OUT"
  -w "http=%{http_code} ip=%{remote_ip} total=%{time_total} speed=%{speed_download} size=%{size_download}\\n"
)

if [[ -n "$AUTH" ]]; then
  CURL_ARGS=(-u "$AUTH" "${CURL_ARGS[@]}")
fi

env -u http_proxy -u https_proxy -u all_proxy \
    -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY \
    curl "${CURL_ARGS[@]}" "$URL"

if [[ -n "$EXPECTED_SHA" && "$EXPECTED_SHA" != "-" ]]; then
  ACTUAL=$(sha256sum "$OUT" | awk '{print $1}')
  if [[ "$ACTUAL" != "$EXPECTED_SHA" ]]; then
    echo "ERROR: sha256 mismatch" >&2
    echo "expected: $EXPECTED_SHA" >&2
    echo "actual:   $ACTUAL" >&2
    exit 1
  fi
  echo "sha256 OK: $ACTUAL"
else
  sha256sum "$OUT"
fi
