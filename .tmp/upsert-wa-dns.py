#!/usr/bin/env python3
import json, re, sys, urllib.request, urllib.error
from pathlib import Path

cfg = Path('/root/.openclaw/workspace/infra/cloudflare-dns/terraform.auto.tfvars').read_text()
zone_id = re.search(r'zone_id\s*=\s*"([^"]+)"', cfg).group(1)
token = re.search(r'cloudflare_api_token\s*=\s*"([^"]+)"', cfg).group(1)
base = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
wanted = [
    {'type':'A','name':'wa.zhangxuemin.work','content':'140.83.52.216','ttl':300,'proxied':False,'comment':'WA app global/source on oracle-mail'},
    {'type':'A','name':'wa-cn.zhangxuemin.work','content':'154.86.30.10','ttl':300,'proxied':False,'comment':'CN/HK edge via hk-relay for WA app'},
]

def req(method, url, data=None):
    body = None if data is None else json.dumps(data).encode()
    r = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            out = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(e.read().decode(), file=sys.stderr)
        raise
    if not out.get('success'):
        raise SystemExit(out)
    return out

for rec in wanted:
    q = req('GET', base + '?' + urllib.parse.urlencode({'type': rec['type'], 'name': rec['name']}))
    results = q.get('result', [])
    payload = dict(rec)
    if results:
        rid = results[0]['id']
        current = {k: results[0].get(k) for k in ['type','name','content','ttl','proxied','comment']}
        if all(current.get(k) == payload.get(k) for k in payload):
            print(f"unchanged {rec['name']} -> {rec['content']}")
        else:
            req('PUT', f'{base}/{rid}', payload)
            print(f"updated {rec['name']} -> {rec['content']}")
    else:
        req('POST', base, payload)
        print(f"created {rec['name']} -> {rec['content']}")
