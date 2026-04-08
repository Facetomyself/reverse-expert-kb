#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

import yaml

ROOT = Path('/root/.openclaw/workspace/ops-assistant')
STATE_DIR = ROOT / 'state'
LAST_RUN = STATE_DIR / 'last-run.json'
ALERT_STATE = STATE_DIR / 'alert-state.json'
MANAGED = ROOT / 'inventory' / 'managed-hosts.yaml'
TARGET = '5585354085'


def send(msg):
    subprocess.run([
        'openclaw', 'message', 'send',
        '--channel', 'telegram',
        '--account', 'alerts',
        '--target', TARGET,
        '--message', msg,
    ], check=True)


def sig(payload):
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def load_managed_hosts():
    data = yaml.safe_load(MANAGED.read_text()) or {}
    return {item['name']: item for item in data.get('hosts', [])}


def build_significant_view(alerts, host_map):
    overall = alerts.get('overall') or {}
    p1 = sorted(alerts.get('p1') or [])
    critical_down = sorted([
        host for host, ok in overall.items()
        if ok is False and host_map.get(host, {}).get('alert_profile') in ('core', 'standard')
    ])
    return {
        'p1': p1,
        'criticalDown': critical_down,
    }


def render_new_incident_message(new_p1, new_down, state):
    lines = ['[ops-assistant] 重大巡检异常']
    if new_down:
        lines.append('失联/不可达主机:')
        lines.extend([f'- {host}' for host in new_down])
    if new_p1:
        lines.append('P1:')
        lines.extend([f'- {item}' for item in new_p1])
    lines.append('说明: 日常噪声已收敛；此消息仅针对重大异常。')
    lines.append(f"报告: {state.get('summaryPath')}")
    return '\n'.join(lines)


def render_recovery_message(recovered_p1, recovered_down, state):
    lines = ['[ops-assistant] 重大异常恢复']
    if recovered_down:
        lines.append('恢复可达主机:')
        lines.extend([f'- {host}' for host in recovered_down])
    if recovered_p1:
        lines.append('已恢复的 P1:')
        lines.extend([f'- {item}' for item in recovered_p1])
    lines.append(f"报告: {state.get('summaryPath')}")
    return '\n'.join(lines)


def main():
    if not LAST_RUN.exists():
        return
    host_map = load_managed_hosts()
    state = json.loads(LAST_RUN.read_text())
    alerts = state.get('alerts', {})
    significant = build_significant_view(alerts, host_map)
    cur_sig = sig(significant)
    prev = json.loads(ALERT_STATE.read_text()) if ALERT_STATE.exists() else {}
    prev_sig = prev.get('signature')
    prev_significant = prev.get('significant') or {'p1': [], 'criticalDown': []}

    msgs = []
    if cur_sig != prev_sig:
        cur_p1 = set(significant.get('p1') or [])
        prev_p1 = set(prev_significant.get('p1') or [])
        cur_down = set(significant.get('criticalDown') or [])
        prev_down = set(prev_significant.get('criticalDown') or [])

        new_p1 = sorted(cur_p1 - prev_p1)
        new_down = sorted(cur_down - prev_down)
        recovered_p1 = sorted(prev_p1 - cur_p1)
        recovered_down = sorted(prev_down - cur_down)

        if new_p1 or new_down:
            msgs.append(render_new_incident_message(new_p1, new_down, state))
        elif recovered_p1 or recovered_down:
            msgs.append(render_recovery_message(recovered_p1, recovered_down, state))

    for m in msgs:
        send(m)
    ALERT_STATE.parent.mkdir(parents=True, exist_ok=True)
    ALERT_STATE.write_text(json.dumps({
        'signature': cur_sig,
        'alerts': alerts,
        'significant': significant,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
