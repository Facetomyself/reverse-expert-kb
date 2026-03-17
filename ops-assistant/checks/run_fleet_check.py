#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / 'reports' / datetime.now().strftime('%Y-%m-%d')
STATE_DIR = ROOT / 'state'
TMP_DIR = Path('/tmp')

CHECKS = [
    ('host_health', ROOT / 'checks' / 'host_health.py'),
    ('docker_inventory', ROOT / 'checks' / 'docker_inventory.py'),
    ('systemd_inventory', ROOT / 'checks' / 'systemd_inventory.py'),
    ('drift_scan', ROOT / 'checks' / 'drift_scan.py'),
    ('reconcile_projects', ROOT / 'checks' / 'reconcile_projects.py'),
]


def run_py(script, out_path):
    p = subprocess.run(['python3', str(script)], text=True, capture_output=True)
    out_path.write_text(p.stdout if p.stdout else '')
    return {'code': p.returncode, 'stderr': p.stderr.strip(), 'out': str(out_path)}


def build_summary():
    host = json.loads((TMP_DIR/'ops_host_health.json').read_text())
    docker = json.loads((TMP_DIR/'ops_docker_inventory.json').read_text())
    systemd = json.loads((TMP_DIR/'ops_systemd_inventory.json').read_text())
    drift = json.loads((TMP_DIR/'ops_drift_scan.json').read_text())
    recon = json.loads((TMP_DIR/'ops_reconcile_projects.json').read_text())
    by = {}
    for name, payload in [('host',host),('docker',docker),('systemd',systemd),('drift',drift)]:
        for item in payload['results']:
            by.setdefault(item['host'], {})[name] = item
    recon_map = {x['host']: x for x in recon['results']}
    lines = ['# Fleet Summary', '']
    p1 = []
    p2 = []
    for hn in sorted(by):
        d = by[hn]
        ok = all(d[k].get('ok') for k in d)
        lines.append(f'## {hn}')
        lines.append(f"- overall: {'OK' if ok else 'ATTENTION'}")
        if not ok:
            p1.append(f'{hn}: reachability or core inspection failure')
        rr = recon_map.get(hn)
        if rr:
            if rr.get('undocumentedHints'):
                p2.append(f"{hn}: undocumented hints -> {', '.join(rr['undocumentedHints'])}")
            if hn != 'oracle-mail' and rr.get('staleHints'):
                p2.append(f"{hn}: stale hints -> {', '.join(rr['staleHints'])}")
        lines.append('')
    if p1 or p2:
        lines += ['## Alert candidates', '']
        if p1:
            lines.append('### P1')
            lines += [f'- {x}' for x in p1]
        if p2:
            lines.append('### P2')
            lines += [f'- {x}' for x in p2]
        lines.append('')
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORT_DIR / 'fleet-summary.md'
    out.write_text('\n'.join(lines) + '\n')
    return out, {'p1': p1, 'p2': p2}


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    results = {}
    for name, script in CHECKS:
        out = TMP_DIR / f'ops_{name}.json'
        results[name] = run_py(script, out)
    summary_path, alerts = build_summary()
    state = {
        'lastRunAt': datetime.utcnow().isoformat() + 'Z',
        'summaryPath': str(summary_path),
        'alerts': alerts,
        'checks': results,
    }
    last_run = STATE_DIR / 'last-run.json'
    last_run.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    rules_script = ROOT / 'checks' / 'apply_alert_rules.py'
    if rules_script.exists():
        p = subprocess.run(['python3', str(rules_script)], text=True, capture_output=True)
        if p.returncode == 0 and p.stdout.strip():
            print(p.stdout)
            return
    print(json.dumps(state, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
