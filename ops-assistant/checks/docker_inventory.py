#!/usr/bin/env python3
import json
import shlex
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANAGED = ROOT / 'inventory' / 'managed-hosts.yaml'


def load_hosts():
    import yaml
    data = yaml.safe_load(MANAGED.read_text())
    return data.get('hosts', [])


def run(cmd):
    p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def ssh_cmd(alias, remote):
    return f"ssh -o BatchMode=yes -o ConnectTimeout=8 {shlex.quote(alias)} {shlex.quote(remote)}"


def check(host):
    name = host['name']
    base = "docker ps --format '{{.Names}}\t{{.Status}}'"
    if name == 'oracle-open_claw':
        cmd = base
    else:
        alias = host.get('ssh_alias')
        cmd = ssh_cmd(alias, base)
    code, out, err = run(cmd)
    return {
        'host': name,
        'ok': code == 0,
        'containers': [line for line in out.splitlines() if line.strip()],
        'error': err if code != 0 else '',
    }


def main():
    print(json.dumps({'results': [check(h) for h in load_hosts() if h.get('enabled', True)]}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
