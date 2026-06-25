#!/usr/bin/env bash
set -euo pipefail
printf 'oracle-gateway DNS/IP: '
getent ahostsv4 backup.zhangxuemin.work | head -n1 || true
printf 'ipinfo: '
curl -sS --max-time 10 https://ipinfo.io/129.150.61.78/json | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("country"), d.get("region"), d.get("city"), d.get("org"))' || true
ssh -o BatchMode=yes oracle-gateway 'hostname; docker ps --format "{{.Names}} {{.Image}} {{.Ports}}"; ss -lunp | grep -E ":443\b|:3478\b" || true'
