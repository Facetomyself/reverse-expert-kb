# Cron Activation Plan

## Planned jobs

### 1. ops-assistant:high-frequency
Cadence: every 10 minutes
Purpose:
- host reachability
- core fleet check
- alert evaluation and Telegram push

Suggested command:
```bash
cd /root/.openclaw/workspace && python3 ops-assistant/checks/run_fleet_check.py && python3 ops-assistant/checks/send_alerts.py
```

### 2. ops-assistant:daily-reconcile
Cadence: daily
Purpose:
- deeper reconciliation report
- undocumented project detection
- drift summary accumulation

Suggested command:
```bash
cd /root/.openclaw/workspace && python3 ops-assistant/checks/run_fleet_check.py
```

## Approval note
Per current safety policy, cron creation is pending explicit user approval.
