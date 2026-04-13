#!/bin/sh
set -eu
CFG=/opt/sing-box-gateway/config.json
SERVICE=sing-box-gateway.service
TAGS="oracle-egress hk-hy2 hk-reality hk-socks hk-http"
usage() {
  echo "usage: $0 <tag>|status" >&2
  echo "allowed: $TAGS" >&2
  exit 2
}
[ $# -eq 1 ] || usage
cmd="$1"
if [ "$cmd" = "status" ]; then
  python3 - <<'PY2'
import json
cfg=json.load(open('/opt/sing-box-gateway/config.json'))
sel=next(o for o in cfg['outbounds'] if o.get('type')=='selector' and o.get('tag')=='proxy')
print(sel.get('default',''))
PY2
  exit 0
fi
ok=0
for t in $TAGS; do
  if [ "$cmd" = "$t" ]; then ok=1; break; fi
done
[ "$ok" -eq 1 ] || usage
python3 - "$cmd" <<'PY2'
import json,sys
path='/opt/sing-box-gateway/config.json'
tag=sys.argv[1]
with open(path) as f:
    cfg=json.load(f)
for o in cfg['outbounds']:
    if o.get('type')=='selector' and o.get('tag')=='proxy':
        o['default']=tag
        break
else:
    raise SystemExit('selector proxy not found')
with open(path,'w') as f:
    json.dump(cfg,f,indent=2)
    f.write('\n')
PY2
systemctl restart "$SERVICE"
sleep 1
systemctl is-active "$SERVICE" >/dev/null
python3 - <<'PY2'
import json
cfg=json.load(open('/opt/sing-box-gateway/config.json'))
sel=next(o for o in cfg['outbounds'] if o.get('type')=='selector' and o.get('tag')=='proxy')
print(sel.get('default',''))
PY2
