#!/usr/bin/env python3
import json
import shlex
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANAGED = ROOT / 'inventory' / 'managed-hosts.yaml'
TRANSIENT_SSH_ERRORS = (
    'Connection timed out during banner exchange',
    'Connection reset by peer',
    'kex_exchange_identification',
)


def load_hosts():
    import yaml
    data = yaml.safe_load(MANAGED.read_text())
    return data.get('hosts', [])


def run(cmd):
    p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def run_with_retry(cmd, attempts=3, delay_seconds=2):
    last = None
    for idx in range(1, attempts + 1):
        code, out, err = run(cmd)
        last = (code, out, err, idx)
        if code == 0:
            return last
        if not any(marker in err for marker in TRANSIENT_SSH_ERRORS):
            return last
        if idx < attempts:
            time.sleep(delay_seconds)
    return last


def ssh_cmd(alias, remote):
    return f"ssh -o BatchMode=yes -o ConnectTimeout=8 {shlex.quote(alias)} {shlex.quote(remote)}"


def check(host):
    name = host['name']
    profile = host.get('check_profile', '')
    if profile in ('tailnet-interactive-only', 'unstable-tailnet-observe', 'nas-tailnet-minimal'):
        return {
            'host': name,
            'ok': True,
            'containers': [],
            'error': '',
            'skipped': True,
            'skipReason': f'profile={profile}',
        }
    base = "docker ps --format '{{.Names}}\t{{.Status}}'"
    if name == 'oracle-open_claw':
        cmd = base
        code, out, err, attempt = (*run(cmd), 1)
    else:
        alias = host.get('ssh_alias')
        cmd = ssh_cmd(alias, base)
        code, out, err, attempt = run_with_retry(cmd)
    error = err if code != 0 else ''
    if code != 0 and attempt > 1 and error:
        error = f"after {attempt} attempts: {error}"
    return {
        'host': name,
        'ok': code == 0,
        'containers': [line for line in out.splitlines() if line.strip()],
        'error': error,
    }


def main():
    print(json.dumps({'results': [check(h) for h in load_hosts() if h.get('enabled', True)]}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
