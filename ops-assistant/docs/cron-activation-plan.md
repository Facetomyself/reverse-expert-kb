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

## Activation status
Enabled on 2026-03-17:
- `ops-assistant:high-frequency`
- cadence: every 10 minutes
- delivery mode: none (Telegram alerts only via `send_alerts.py` and the dedicated `telegram:alerts` bot)

## Approval note
Cron creation was explicitly approved by the user on 2026-03-17 after validating `run_fleet_check.py` syntax and runtime behavior.
