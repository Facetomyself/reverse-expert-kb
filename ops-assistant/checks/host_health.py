#!/usr/bin/env python3
import json
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANAGED = ROOT / 'inventory' / 'managed-hosts.yaml'


def load_hosts():
    import yaml
    data = yaml.safe_load(MANAGED.read_text())
    return data.get('hosts', [])


def run(cmd):
    p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return {
        'code': p.returncode,
        'stdout': p.stdout.strip(),
        'stderr': p.stderr.strip(),
    }


def ssh_cmd(alias, remote):
    return f"ssh -o BatchMode=yes -o ConnectTimeout=8 {shlex.quote(alias)} {shlex.quote(remote)}"


def check_host(host):
    name = host['name']
    if name == 'oracle-open_claw':
        cmd = "hostname && uptime && df -h / | tail -n 1"
    else:
        alias = host.get('ssh_alias')
        cmd = ssh_cmd(alias, "hostname && uptime && df -h / | tail -n 1")
    res = run(cmd)
    return {
        'host': name,
        'ok': res['code'] == 0,
        'summary': res['stdout'].splitlines()[:3],
        'error': res['stderr'] if res['code'] != 0 else '',
    }


def main():
    hosts = load_hosts()
    results = [check_host(h) for h in hosts if h.get('enabled', True)]
    print(json.dumps({'results': results}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
