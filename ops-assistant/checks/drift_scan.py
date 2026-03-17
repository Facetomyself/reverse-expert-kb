#!/usr/bin/env python3
import json
import shlex
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANAGED = ROOT / 'inventory' / 'managed-hosts.yaml'

COMMON_FIND = r"find /root /opt /srv -maxdepth 3 \( -name docker-compose.yml -o -name compose.yml -o -name compose.yaml \) 2>/dev/null | sort | head -n 100"


def load_hosts():
    import yaml
    return yaml.safe_load(MANAGED.read_text()).get('hosts', [])


def run(cmd):
    p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def ssh_cmd(alias, remote):
    return f"ssh -o BatchMode=yes -o ConnectTimeout=8 {shlex.quote(alias)} {shlex.quote(remote)}"


def scan(host):
    name = host['name']
    if name == 'oracle-open_claw':
        cmd = COMMON_FIND
    else:
        cmd = ssh_cmd(host['ssh_alias'], COMMON_FIND)
    code, out, err = run(cmd)
    return {
        'host': name,
        'ok': code == 0,
        'composeFiles': [line for line in out.splitlines() if line.strip()],
        'error': err if code != 0 else '',
    }


def main():
    print(json.dumps({'results': [scan(h) for h in load_hosts() if h.get('enabled', True)]}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
