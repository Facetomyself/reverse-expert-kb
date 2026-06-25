#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

cfg = Path('/root/.openclaw/workspace/infra/cloudflare-dns/terraform.auto.tfvars')
text = cfg.read_text(encoding='utf-8')
zone = re.search(r'^zone_id\s*=\s*"([^"]+)"', text, re.M)
token = re.search(r'^cloudflare_api_token\s*=\s*"([^"]+)"', text, re.M)
if not zone or not token:
    raise SystemExit('missing zone_id or cloudflare_api_token')
zone_id = zone.group(1)
api_token = token.group(1)
base = 'https://api.cloudflare.com/client/v4'
headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json',
    'User-Agent': 'openclaw-cf-email-probe/1.0',
}
paths = [
    f'/zones/{zone_id}/email/routing',
    f'/zones/{zone_id}/email/routing/dns',
    f'/zones/{zone_id}/email/routing/settings',
    f'/zones/{zone_id}/email/routing/rules',
    f'/zones/{zone_id}/email/routing/addresses',
    f'/zones/{zone_id}/email/security/settings',
]
out = []
for path in paths:
    req = urllib.request.Request(base + path, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode('utf-8', errors='replace')
            try:
                data = json.loads(body)
            except Exception:
                data = body[:1000]
            out.append({'path': path, 'http': resp.getcode(), 'data': data})
    except urllib.error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        try:
            data = json.loads(body)
        except Exception:
            data = body[:1000]
        out.append({'path': path, 'http': exc.code, 'data': data})
    except Exception as exc:
        out.append({'path': path, 'error': str(exc)})
print(json.dumps(out, ensure_ascii=False, indent=2))
