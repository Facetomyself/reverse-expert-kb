#!/usr/bin/env python3
"""Proxy node health smoke test for a Mihomo/Clash YAML file.

Tests explicit HTTP/SOCKS nodes without printing credentials. Protocols that
need a Mihomo core (HY2/VLESS/TUIC/Trojan/SS) are listed as skipped when
--include-skipped is used.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path
from urllib.parse import quote

import yaml

DEFAULT_CONFIG = Path('/root/.openclaw/workspace/_tmp_live_private_clash_meta_v4.yaml')
DEFAULT_URL = 'https://www.gstatic.com/generate_204'


def proxy_url(node: dict) -> str | None:
    typ = node.get('type')
    host = node.get('server')
    port = node.get('port')
    if not host or not port:
        return None
    user = node.get('username') or ''
    pwd = node.get('password') or ''
    auth = ''
    if user or pwd:
        auth = f'{quote(str(user), safe="")}:{quote(str(pwd), safe="")}@'
    if typ == 'http':
        return f'http://{auth}{host}:{port}'
    if typ == 'socks5':
        return f'socks5h://{auth}{host}:{port}'
    return None


def run_check(name: str, node: dict, url: str, timeout: int) -> dict:
    purl = proxy_url(node)
    result = {
        'name': name,
        'type': node.get('type'),
        'server': node.get('server'),
        'port': node.get('port'),
        'status': 'skipped',
        'reason': 'unsupported-by-curl-light-check',
    }
    if not purl:
        return result
    cmd = ['curl', '-fsSIL', '--max-time', str(timeout), '--proxy', purl, url]
    started = time.time()
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elapsed_ms = round((time.time() - started) * 1000)
    first = ''
    for line in proc.stdout.splitlines():
        if line.startswith('HTTP/'):
            first = line.strip()
    ok = proc.returncode == 0 and any(code in proc.stdout for code in (' 204', ' 200', ' 301', ' 302'))
    result.update({
        'status': 'ok' if ok else 'fail',
        'elapsed_ms': elapsed_ms,
        'http': first,
        'returncode': proc.returncode,
    })
    if not ok:
        err_lines = (proc.stderr or proc.stdout).strip().splitlines()
        result['error'] = err_lines[-1] if err_lines else 'unknown'
    else:
        ip_cmd = ['curl', '-fsS', '--max-time', str(timeout), '--proxy', purl, 'https://api.ipify.org']
        ip_proc = subprocess.run(ip_cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if ip_proc.returncode == 0:
            result['egress_ip'] = ip_proc.stdout.strip()[:64]
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default=str(DEFAULT_CONFIG), help='Mihomo YAML path')
    ap.add_argument('--url', default=DEFAULT_URL, help='URL for HEAD connectivity check')
    ap.add_argument('--timeout', type=int, default=8)
    ap.add_argument('--include-skipped', action='store_true')
    ap.add_argument('--json', action='store_true', help='emit JSON instead of table')
    args = ap.parse_args()

    data = yaml.safe_load(Path(args.config).read_text())
    rows = []
    for node in data.get('proxies', []):
        row = run_check(node.get('name', '<unnamed>'), node, args.url, args.timeout)
        if args.include_skipped or row['status'] != 'skipped':
            rows.append(row)

    if args.json:
        print(json.dumps({'config': args.config, 'checked_at': time.strftime('%FT%T%z'), 'results': rows}, ensure_ascii=False, indent=2))
    else:
        print(f'config={args.config}')
        for r in rows:
            bits = [r['name'], r.get('type','?'), r['status']]
            if 'elapsed_ms' in r:
                bits.append(f"{r['elapsed_ms']}ms")
            if r.get('egress_ip'):
                bits.append(f"egress={r['egress_ip']}")
            if r.get('error'):
                bits.append(f"error={r['error']}")
            print(' | '.join(map(str, bits)))
    return 0 if all(r['status'] in ('ok','skipped') for r in rows) else 1


if __name__ == '__main__':
    raise SystemExit(main())
