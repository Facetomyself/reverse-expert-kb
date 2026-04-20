#!/usr/bin/env bash
set -euo pipefail

fc-cache -f >/dev/null 2>&1 || true

exec python /app/server.py \
  --bind 0.0.0.0 \
  --port 18781 \
  --storage-dir /data
