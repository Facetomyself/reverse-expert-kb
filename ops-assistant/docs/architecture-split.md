# Stable Line vs Analysis Line

## Stable production line
Current high-frequency cron should only include:
- host_health
- docker_inventory
- systemd_inventory
- drift_scan
- reconcile_projects
- apply_alert_rules
- send_alerts

Purpose:
- reliable fleet watch
- low-noise Telegram alerting
- predictable runtime

## Analysis enhancement line
Project-entity reconciliation is intentionally separated into its own entrypoint:
- `ops-assistant/checks/run_entity_reconcile.py`

Purpose:
- deeper asset/project reconciliation
- undocumented compose project discovery
- documented-but-missing component detection
- future infra documentation sync candidates

Reason for split:
- high-frequency alert path must remain robust
- deeper reconciliation can be slower/more complex without risking pager reliability
