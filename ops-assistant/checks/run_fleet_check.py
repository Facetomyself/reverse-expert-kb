#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
TZ = timezone(timedelta(hours=8))
REPORT_DIR = ROOT / 'reports' / datetime.now(TZ).strftime('%Y-%m-%d')
STATE_DIR = ROOT / 'state'
HISTORY_DIR = STATE_DIR / 'history'
TMP_DIR = Path('/tmp')

CHECKS = [
    ('host_health', ROOT / 'checks' / 'host_health.py'),
    ('docker_inventory', ROOT / 'checks' / 'docker_inventory.py'),
    ('systemd_inventory', ROOT / 'checks' / 'systemd_inventory.py'),
    ('drift_scan', ROOT / 'checks' / 'drift_scan.py'),
    ('reconcile_projects', ROOT / 'checks' / 'reconcile_projects.py'),
]


def run_py(script, out_path):
    try:
        p = subprocess.run(['python3', str(script)], text=True, capture_output=True, timeout=180)
        out_path.write_text(p.stdout if p.stdout else '')
        return {'code': p.returncode, 'stderr': p.stderr.strip(), 'out': str(out_path)}
    except subprocess.TimeoutExpired as e:
        out_path.write_text(e.stdout if e.stdout else '')
        return {'code': 124, 'stderr': f'timeout after 180s: {script.name}', 'out': str(out_path)}


def build_summary():
    host = json.loads((TMP_DIR/'ops_host_health.json').read_text())
    docker = json.loads((TMP_DIR/'ops_docker_inventory.json').read_text())
    systemd = json.loads((TMP_DIR/'ops_systemd_inventory.json').read_text())
    drift = json.loads((TMP_DIR/'ops_drift_scan.json').read_text())
    recon = json.loads((TMP_DIR/'ops_reconcile_projects.json').read_text())
    by = {}
    for name, payload in [('host', host), ('docker', docker), ('systemd', systemd), ('drift', drift)]:
        for item in payload['results']:
            by.setdefault(item['host'], {})[name] = item
    recon_map = {x['host']: x for x in recon['results']}
    lines = ['# Fleet Summary', '']
    p1 = []
    p2 = []
    host_overall = {}
    for hn in sorted(by):
        d = by[hn]
        ok = all(d[k].get('ok') for k in d)
        host_overall[hn] = ok
        lines.append(f'## {hn}')
        lines.append(f"- overall: {'OK' if ok else 'ATTENTION'}")

        if not d.get('host', {}).get('ok'):
            p1.append(f'{hn}: reachability failure')
        else:
            failed_checks = [name for name in ('docker', 'systemd', 'drift') if not d.get(name, {}).get('ok', True)]
            if failed_checks:
                p2.append(f"{hn}: core inspection partial failure -> {', '.join(failed_checks)}")

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
    return out, {'p1': p1, 'p2': p2, 'overall': host_overall}


def best_effort_send_alerts():
    send_script = ROOT / 'checks' / 'send_alerts.py'
    if not send_script.exists():
        return
    subprocess.run(['python3', str(send_script)], text=True, capture_output=True)


def append_history(state):
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(TZ)
    day_path = HISTORY_DIR / f"{stamp.strftime('%Y-%m-%d')}.jsonl"
    entry = {
        'recordedAt': stamp.isoformat(),
        'lastRunAt': state.get('lastRunAt'),
        'summaryPath': state.get('summaryPath'),
        'alerts': state.get('alerts', {}),
        'alertRuleNotes': state.get('alertRuleNotes', []),
    }
    with day_path.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + '\n')


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    results = {}
    for name, script in CHECKS:
        out = TMP_DIR / f'ops_{name}.json'
        results[name] = run_py(script, out)
    summary_path, alerts = build_summary()
    state = {
        'lastRunAt': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
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
            filtered = json.loads(p.stdout)
            lines = ['# Fleet Summary', '']
            overall = filtered.get('alerts', {}).get('overall') or state.get('alerts', {}).get('overall') or {}
            if not overall:
                host = json.loads((TMP_DIR/'ops_host_health.json').read_text())
                overall = {item['host']: item.get('ok') for item in host['results']}
            for hn in sorted(overall):
                ok = overall[hn]
                lines.append(f'## {hn}')
                lines.append(f"- overall: {'OK' if ok else 'ATTENTION'}")
                lines.append('')
            p1 = filtered.get('alerts', {}).get('p1', [])
            p2 = filtered.get('alerts', {}).get('p2', [])
            if p1 or p2:
                lines += ['## Alert candidates (filtered)', '']
                if p1:
                    lines.append('### P1')
                    lines += [f'- {x}' for x in p1]
                if p2:
                    lines.append('### P2')
                    lines += [f'- {x}' for x in p2]
                lines.append('')
            summary_path.write_text('\n'.join(lines) + '\n')
            append_history(filtered)
            best_effort_send_alerts()
            print(json.dumps(filtered, ensure_ascii=False, indent=2))
            return
    append_history(state)
    best_effort_send_alerts()
    print(json.dumps(state, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
