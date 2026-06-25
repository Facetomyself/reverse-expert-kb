#!/bin/sh
set -eu
OUT="$HOME/hysteria-client/log/selftest.txt"
{
  echo "TS=$(date '+%F %T %z' 2>/dev/null || true)"
  echo "== client log tail =="
  tail -n 20 "$HOME/hysteria-client/log/client.log" 2>/dev/null || true
  echo
  echo "== proxy ip =="
  curl -x http://127.0.0.1:10809 --max-time 20 https://api.ipify.org || true
  echo
  echo
  echo "== github head via proxy =="
  curl -x http://127.0.0.1:10809 -I --max-time 20 https://github.com 2>&1 | sed -n '1,20p' || true
  echo
  echo "== hf head via proxy =="
  curl -x http://127.0.0.1:10809 -I --max-time 30 "https://huggingface.co/ChenkinRF/ChenkinNoob-XL-v0.2-Rectified-Flow/resolve/main/ChenkinNoob-XL-v0.2-Rectified-Flow.safetensors" 2>&1 | sed -n '1,30p' || true
} > "$OUT" 2>&1
