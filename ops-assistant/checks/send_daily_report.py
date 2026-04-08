#!/usr/bin/env python3
import json
import re
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
PROJECT_MAP = ROOT / 'inventory' / 'project-map.yaml'
DAILY_STATE = STATE_DIR / 'daily-report-state.json'
TARGET = '5585354085'
TZ = timezone(timedelta(hours=8))
TMP_DIR = Path('/tmp')

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


def load_project_map():
    data = yaml.safe_load(PROJECT_MAP.read_text()) or {}
    return data.get('hosts', {})


def load_check(name):
    path = TMP_DIR / name
    if not path.exists():
        return {'results': []}
    return json.loads(path.read_text())


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


def normalize_container_name(line):
    return (line or '').split('\t', 1)[0].strip()


def normalize_service_name(line):
    text = (line or '').strip()
    if not text:
        return ''
    return re.split(r'\s+', text)[0]


def parse_host_basics(summary_lines):
    hostname = summary_lines[0] if len(summary_lines) > 0 else '-'
    uptime = summary_lines[1].strip() if len(summary_lines) > 1 else '-'
    disk = summary_lines[2].strip() if len(summary_lines) > 2 else '-'
    return hostname, uptime, disk


def project_runtime_status(project, docker_entry, systemd_entry, drift_entry):
    match = project.get('match', {}) or {}
    containers = {normalize_container_name(x) for x in docker_entry.get('containers', [])}
    services = {normalize_service_name(x) for x in systemd_entry.get('services', [])}
    compose_files = set(drift_entry.get('composeFiles', []))

    expected_containers = set(match.get('containers') or [])
    expected_services = set(match.get('systemd') or [])
    expected_compose = set(match.get('compose_paths') or [])

    hits = []
    misses = []
    if expected_containers:
        found = sorted(expected_containers & containers)
        missing = sorted(expected_containers - containers)
        if found:
            hits.append(f"容器 {', '.join(found)}")
        if missing:
            misses.append(f"缺容器 {', '.join(missing)}")
    if expected_services:
        found = sorted(expected_services & services)
        missing = sorted(expected_services - services)
        if found:
            hits.append(f"服务 {', '.join(found)}")
        if missing:
            misses.append(f"缺服务 {', '.join(missing)}")
    if expected_compose:
        found = sorted(expected_compose & compose_files)
        missing = sorted(expected_compose - compose_files)
        if found:
            hits.append(f"编排 {', '.join(found)}")
        if missing:
            misses.append(f"缺编排 {', '.join(missing)}")

    status = 'unknown'
    if hits and not misses:
        status = 'up'
    elif hits and misses:
        status = 'partial'
    elif misses:
        status = 'down'

    if match.get('status') in ('archive', 'retired'):
        status = 'retired'

    return status, hits, misses


def project_status_emoji(status):
    return {
        'up': '✅',
        'partial': '⚠️',
        'down': '🚨',
        'retired': '🗄️',
        'unknown': '❔',
    }.get(status, '❔')


def render_message(day_str, state, hosts, history):
    alerts = state.get('alerts', {})
    overall = alerts.get('overall') or {}
    p1 = alerts.get('p1') or []
    p2 = alerts.get('p2') or []
    host_map = {host['name']: host for host in hosts}
    project_map = load_project_map()

    host_health = {x['host']: x for x in load_check('ops_host_health.json').get('results', [])}
    docker = {x['host']: x for x in load_check('ops_docker_inventory.json').get('results', [])}
    systemd = {x['host']: x for x in load_check('ops_systemd_inventory.json').get('results', [])}
    drift = {x['host']: x for x in load_check('ops_drift_scan.json').get('results', [])}

    lines = [f"[ops-assistant] 每日服务器巡检日报 {day_str}", '']
    lines.append('今日结论:')
    if p1:
        lines.append(f"- 存在重大异常 {len(p1)} 项")
    else:
        lines.append('- 当前无重大异常')
    if p2:
        lines.append(f"- 一般关注项 {len(p2)} 项")
    else:
        lines.append('- 当前无一般关注项')
    lines.extend(summarize_groups(hosts, overall))
    lines.append('')

    if p1:
        lines.append('重大异常:')
        lines.extend([f'- {item}' for item in p1])
        lines.append('')
    if p2:
        lines.append('一般关注项:')
        lines.extend([f'- {item}' for item in p2[:16]])
        lines.append('')

    transitions = collect_transitions(history)
    if transitions:
        lines.append('今日状态变化:')
        lines.extend([format_transition(item) for item in transitions[-12:]])
        lines.append('')

    lines.append('主机与部署状态:')
    for host in hosts:
        name = host['name']
        profile = host.get('alert_profile', 'standard')
        host_ok = overall.get(name) is not False
        emoji = host_status_emoji(host_ok, profile)
        hh = host_health.get(name, {})
        hostname, uptime, disk = parse_host_basics(hh.get('summary', []))
        lines.append(f"- {emoji} {name} ({PROFILE_LABELS.get(profile, profile)})")
        lines.append(f"  - 主机名: {hostname}")
        lines.append(f"  - Uptime: {uptime}")
        lines.append(f"  - 根盘: {disk}")
        if hh.get('error'):
            lines.append(f"  - 主机检查错误: {hh.get('error')}")

        docker_entry = docker.get(name, {})
        systemd_entry = systemd.get(name, {})
        drift_entry = drift.get(name, {})
        containers = [normalize_container_name(x) for x in docker_entry.get('containers', [])]
        services = [normalize_service_name(x) for x in systemd_entry.get('services', [])]
        if containers:
            lines.append(f"  - 容器: {len(containers)} 个（{', '.join(containers[:6])}{' ...' if len(containers) > 6 else ''}）")
        elif docker_entry.get('skipped'):
            lines.append(f"  - 容器: 已跳过（{docker_entry.get('skipReason')}）")
        else:
            lines.append("  - 容器: 无 / 未发现")
        if services:
            lines.append(f"  - 关键服务样本: {', '.join(services[:4])}{' ...' if len(services) > 4 else ''}")
        elif systemd_entry.get('skipped'):
            lines.append(f"  - 服务: 已跳过（{systemd_entry.get('skipReason')}）")

        documented_projects = (project_map.get(name, {}) or {}).get('documented_projects', [])
        if documented_projects:
            lines.append('  - 已登记项目:')
            for project in documented_projects:
                status, hits, misses = project_runtime_status(project, docker_entry, systemd_entry, drift_entry)
                pe = project_status_emoji(status)
                detail = '; '.join((hits + misses)[:2]) if (hits or misses) else '暂无足够运行态样本'
                lines.append(f"    - {pe} {project.get('name')}: {detail}")
        else:
            lines.append('  - 已登记项目: 无')
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

    state = load_json(LAST_RUN, default={})
    hosts = load_managed_hosts()
    history = load_today_history(day_str)
    message = render_message(day_str, state, hosts, history)

    report_dir = REPORTS_DIR / day_str
    report_dir.mkdir(parents=True, exist_ok=True)
    out_path = report_dir / 'daily-report.md'
    out_path.write_text(message + '\n')

    if report_state.get('lastSentDay') == day_str:
        return

    send(message)
    DAILY_STATE.parent.mkdir(parents=True, exist_ok=True)
    DAILY_STATE.write_text(json.dumps({
        'lastSentDay': day_str,
        'sentAt': now.isoformat(),
        'reportPath': str(out_path),
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
