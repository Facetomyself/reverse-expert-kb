#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

REPORT = Path('/root/.openclaw/workspace/ops-assistant/reports/2026-03-17/fleet-summary.md')
TARGET = '5585354085'


def send(msg):
    subprocess.run([
        'openclaw', 'message', 'send',
        '--channel', 'telegram',
        '--account', 'alerts',
        '--target', TARGET,
        '--message', msg,
    ], check=True)


def main():
    if not REPORT.exists():
        return
    text = REPORT.read_text()
    alerts = []
    if '## self-server\n- overall: ATTENTION' in text:
        alerts.append('[P2][self-server] SSH 连接仍超时，不可达；已在 fleet summary 记录。')
    if '/root/AntiCAP-WebApi-docker/docker-compose.yml' in text:
        alerts.append('[P2][oracle-proxy] 巡检发现多项 compose 项目痕迹，存在未归档/漂移候选，请查看 fleet summary。')
    if alerts:
        send('\n'.join(alerts) + '\n\n报告: ops-assistant/reports/2026-03-17/fleet-summary.md')


if __name__ == '__main__':
    main()
