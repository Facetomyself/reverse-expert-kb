# Daily report refactor — 2026-04-08

## Goal

Reduce Telegram noise from server inspection while keeping visibility.

## New policy

- High-frequency fleet checks remain hourly.
- Hourly checks primarily update `ops-assistant/state/last-run.json` and append a compact daily history snapshot.
- Telegram immediate push is now reserved for **significant incidents only**:
  - new P1 items
  - newly down/unreachable hosts whose `alert_profile` is `core` or `standard`
  - recovery of the above significant incidents
- Host reachability uses simple flap damping:
  - host-down paging requires 2 consecutive failing runs
  - host recovery message requires 2 consecutive healthy runs
  - P1 still pages immediately
- Normal P2 churn no longer triggers Telegram pushes.
- A new daily Telegram report summarizes fleet state in a host-centric layout.

## Files

- `checks/run_fleet_check.py`
  - append filtered state snapshots into `state/history/YYYY-MM-DD.jsonl`
- `checks/send_alerts.py`
  - compute a `significant` view and only push meaningful incident deltas
- `checks/send_daily_report.py`
  - send one daily host-oriented summary to the existing Telegram alerts target

## Expected operator effect

- far fewer Telegram messages
- still get paged for truly important breakage
- receive one readable daily summary with per-host status and same-day transitions
