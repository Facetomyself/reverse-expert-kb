#!/usr/bin/env python3
import json
import subprocess
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml

ROOT = Path('/root/.openclaw/workspace/ops-assistant')
STATE_DIR = ROOT / 'state'
REPORTS_DIR = ROOT / 'reports'
LAST_RUN = STATE_DIR / 'last-run.json'
HISTORY_DIR = STATE_DIR / 'history'
MANAGED = ROOT / 'inventory' / 'managed-hosts.yaml'
DAILY_STATE = STATE_DIR / 'daily-report-state.json'
TARGET = '5585354085'
TZ = timezone(timedelta(hours=8))

PROFILE_LABELS = {
    'core': '核心',
    'standard': '标准',
    'retired': '观察',
    'exception': '例外',
}


def load_json(path, default=None):
    if not path.exists():
        return {} if default is None else default
    return json.loads(path.read_text())


def load_managed_hosts():
    data = yaml.safe_load(MANAGED.read_text()) or {}
    return data.get('hosts', [])


def load_today_history(day_str):
    path = HISTORY_DIR / f'{day_str}.jsonl'
    if not path.exists():
        return []
    items = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return items


def host_status_emoji(ok, profile):
    if ok:
        return '✅'
    if profile in ('retired', 'exception'):
        return '⚠️'
    return '🚨'


def summarize_groups(hosts, overall_map):
    grouped = defaultdict(list)
    for host in hosts:
        grouped[host.get('alert_profile', 'standard')].append(host)
    lines = []
    for profile in ('core', 'standard', 'retired', 'exception'):
        items = grouped.get(profile) or []
        if not items:
            continue
        ok_count = sum(1 for item in items if overall_map.get(item['name']) is not False)
        total = len(items)
        lines.append(f"- {PROFILE_LABELS.get(profile, profile)}: {ok_count}/{total} 正常")
    return lines


def collect_transitions(history):
    transitions = []
    prev = None
    for item in history:
        current = (item.get('alerts') or {}).get('overall') or {}
        ts = item.get('lastRunAt') or item.get('recordedAt') or ''
        if prev is None:
            prev = current
            continue
        for host in sorted(set(prev) | set(current)):
            before = prev.get(host)
            after = current.get(host)
            if before is after:
                continue
            transitions.append({
                'time': ts,
                'host': host,
                'before': before,
                'after': after,
            })
        prev = current
    return transitions


def format_transition(item):
    stamp = item.get('time', '')
    hhmm = stamp[11:16] if len(stamp) >= 16 else stamp
    before = 'OK' if item.get('before') is not False else 'ATTENTION'
    after = 'OK' if item.get('after') is not False else 'ATTENTION'
    return f"- {hhmm} {item['host']}: {before} → {after}"


def render_message(day_str, state, hosts, history):
    alerts = state.get('alerts', {})
    overall = alerts.get('overall') or {}
    p1 = alerts.get('p1') or []
    p2 = alerts.get('p2') or []
    host_map = {host['name']: host for host in hosts}

    lines = [f"[ops-assistant] 每日服务器巡检日报 {day_str}", '']
    lines.append('概览:')
    lines.extend(summarize_groups(hosts, overall))
    lines.append('')

    if p1:
        lines.append('重大异常:')
        lines.extend([f'- {item}' for item in p1])
        lines.append('')
    else:
        lines.append('重大异常: 无')
        lines.append('')

    if p2:
        lines.append('一般关注项:')
        lines.extend([f'- {item}' for item in p2[:12]])
        lines.append('')

    lines.append('按服务器:')
    for host in hosts:
        name = host['name']
        profile = host.get('alert_profile', 'standard')
        ok = overall.get(name)
        emoji = host_status_emoji(ok is not False, profile)
        lines.append(f"- {emoji} {name} ({PROFILE_LABELS.get(profile, profile)})")
    lines.append('')

    transitions = collect_transitions(history)
    if transitions:
        lines.append('今日状态变化:')
        lines.extend([format_transition(item) for item in transitions[-12:]])
        lines.append('')

    known_attention = [
        host for host, ok in overall.items()
        if ok is False and host_map.get(host, {}).get('alert_profile') in ('retired', 'exception')
    ]
    if known_attention:
        lines.append('观察项:')
        lines.extend([f'- {host}: 已按观察/例外策略处理' for host in known_attention])
        lines.append('')

    lines.append(f"报告: {state.get('summaryPath')}")
    return '\n'.join(lines)


def send(msg):
    subprocess.run([
        'openclaw', 'message', 'send',
        '--channel', 'telegram',
        '--account', 'alerts',
        '--target', TARGET,
        '--message', msg,
    ], check=True)


def main():
    if not LAST_RUN.exists():
        return

    now = datetime.now(TZ)
    day_str = now.strftime('%Y-%m-%d')
    report_state = load_json(DAILY_STATE, default={})
    if report_state.get('lastSentDay') == day_str:
        return

    state = load_json(LAST_RUN, default={})
    hosts = load_managed_hosts()
    history = load_today_history(day_str)
    message = render_message(day_str, state, hosts, history)

    report_dir = REPORTS_DIR / day_str
    report_dir.mkdir(parents=True, exist_ok=True)
    out_path = report_dir / 'daily-report.md'
    out_path.write_text(message + '\n')

    send(message)
    DAILY_STATE.parent.mkdir(parents=True, exist_ok=True)
    DAILY_STATE.write_text(json.dumps({
        'lastSentDay': day_str,
        'sentAt': now.isoformat(),
        'reportPath': str(out_path),
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
