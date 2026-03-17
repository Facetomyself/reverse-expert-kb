#!/usr/bin/env python3
import json
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / 'inventory' / 'remediation-pilot.yaml'
REPORT_DIR = ROOT / 'reports' / datetime.now().strftime('%Y-%m-%d')
TARGET = '5585354085'


def run(cmd):
    p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def ssh_cmd(alias, remote):
    return f"ssh -o BatchMode=yes -o ConnectTimeout=8 {shlex.quote(alias)} {shlex.quote(remote)}"


def notify(message):
    subprocess.run([
        'openclaw', 'message', 'send',
        '--channel', 'telegram',
        '--account', 'alerts',
        '--target', TARGET,
        '--message', message,
    ], check=False)


def load_cfg():
    return yaml.safe_load(CFG.read_text())


def remediate_local_systemd(service):
    pre = run(f"systemctl is-active {shlex.quote(service)}")
    act = run(f"systemctl restart {shlex.quote(service)}")
    post = run(f"systemctl is-active {shlex.quote(service)}")
    return {'pre': pre, 'act': act, 'post': post}


def remediate_remote_container(alias, container):
    pre = run(ssh_cmd(alias, f"docker inspect -f '{{{{.State.Status}}}}' {container}"))
    act = run(ssh_cmd(alias, f"docker restart {container}"))
    post = run(ssh_cmd(alias, f"docker inspect -f '{{{{.State.Status}}}}' {container}"))
    return {'pre': pre, 'act': act, 'post': post}


def main():
    if len(sys.argv) < 3:
        print('usage: remediate_pilot.py <host> <target>')
        sys.exit(2)
    host = sys.argv[1]
    target = sys.argv[2]
    cfg = load_cfg()
    pilot = cfg.get('pilot_targets', {})
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    result = {
        'host': host,
        'target': target,
        'startedAt': datetime.utcnow().isoformat() + 'Z',
        'allowed': False,
    }

    if host == 'oracle-open_claw' and target in (pilot.get('oracle-open_claw', {}) or {}).get('systemd', []):
        result['allowed'] = True
        result['kind'] = 'systemd'
        result['details'] = remediate_local_systemd(target)
    elif host == 'oracle-proxy' and target in (pilot.get('oracle-proxy', {}) or {}).get('containers', []):
        result['allowed'] = True
        result['kind'] = 'container'
        result['details'] = remediate_remote_container('oracle-proxy', target)
    else:
        result['error'] = 'target not in pilot whitelist'

    report = REPORT_DIR / f"remediation-{host}-{target}.md"
    lines = [
        f"# Remediation attempt - {host} / {target}",
        '',
        f"- allowed: {result.get('allowed')}",
        f"- kind: {result.get('kind', 'n/a')}",
        f"- startedAt: {result.get('startedAt')}",
    ]
    if result.get('error'):
        lines.append(f"- error: {result['error']}")
    if result.get('details'):
        for phase in ['pre', 'act', 'post']:
            code, out, err = result['details'][phase]
            lines.append(f"- {phase}.code: {code}")
            if out:
                lines.append(f"- {phase}.stdout: {out}")
            if err:
                lines.append(f"- {phase}.stderr: {err}")
    report.write_text('\n'.join(lines) + '\n')
    result['reportPath'] = str(report)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if result.get('allowed'):
        status = result['details']['post'][1] if result.get('details') else 'unknown'
        notify(f"[ops-assistant remediation pilot] {host} / {target}\npost-check: {status}\nreport: {report}")
    else:
        notify(f"[ops-assistant remediation pilot] blocked\n{host} / {target}\nreason: {result.get('error')}\nreport: {report}")


if __name__ == '__main__':
    main()
