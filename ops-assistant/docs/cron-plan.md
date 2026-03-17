# Cron Plan (Draft)

## High frequency
Every 10 minutes:
- host reachability
- core service presence
- critical endpoint checks

## Medium frequency
Every hour:
- docker inventory
- systemd inventory
- disk/memory/load
- certificate and reverse-proxy spot checks

## Low frequency
Daily:
- undocumented project discovery
- infra drift scan
- retired host observation
- report synthesis

## Weekly
- deeper inventory reconciliation
- stale domain/project review
- unresolved incident rollup

## Execution principles
- do not create cron jobs until approved
- each run writes a report file
- Telegram only for P1/P2
- repeated failures should be deduplicated into incident threads/reports
