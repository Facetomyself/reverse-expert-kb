#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path('/root/.openclaw/workspace/ops-assistant')
STATE_DIR = ROOT / 'state'
LAST_RUN = STATE_DIR / 'last-run.json'
ALERT_STATE = STATE_DIR / 'alert-state.json'
TARGET = '5585354085'


def send(msg):
    subprocess.run([
        'openclaw', 'message', 'send',
        '--channel', 'telegram',
        '--account', 'alerts',
        '--target', TARGET,
        '--message', msg,
    ], check=True)


def sig(alerts):
    raw = json.dumps(alerts, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def main():
    if not LAST_RUN.exists():
        return
    state = json.loads(LAST_RUN.read_text())
    alerts = state.get('alerts', {})
    cur_sig = sig(alerts)
    prev = json.loads(ALERT_STATE.read_text()) if ALERT_STATE.exists() else {}
    prev_sig = prev.get('signature')
    prev_alerts = prev.get('alerts', {})
    msgs = []
    if cur_sig != prev_sig:
        p1 = alerts.get('p1') or []
        p2 = alerts.get('p2') or []
        if p1 or p2:
            lines = ['[ops-assistant] 巡检发现新的告警状态']
            if p1:
                lines.append('P1:')
                lines.extend([f'- {x}' for x in p1])
            if p2:
                lines.append('P2:')
                lines.extend([f'- {x}' for x in p2[:8]])
            lines.append(f"报告: {state.get('summaryPath')}")
            msgs.append('\n'.join(lines))
        elif prev_alerts.get('p1') or prev_alerts.get('p2'):
            msgs.append(f"[ops-assistant] 之前的巡检告警已恢复或清空。\n报告: {state.get('summaryPath')}")
    for m in msgs:
        send(m)
    ALERT_STATE.parent.mkdir(parents=True, exist_ok=True)
    ALERT_STATE.write_text(json.dumps({'signature': cur_sig, 'alerts': alerts}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
