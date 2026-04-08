# OpenClaw remediation report — 2026-04-08

## Summary
Performed a first-pass stabilization after repeated OpenClaw gateway crashes and noisy session/cron behavior.

## Changes made
1. Updated user systemd gateway unit metadata to match current installed OpenClaw version `2026.4.8`.
   - File: `/root/.config/systemd/user/openclaw-gateway.service`
   - Updated:
     - `Description=OpenClaw Gateway (v2026.4.8)`
     - `Environment=OPENCLAW_SERVICE_VERSION=2026.4.8`
2. Reloaded user systemd and restarted `openclaw-gateway.service`.
3. Temporarily disabled the highest-noise cron jobs to reduce session churn and potential instability:
   - `research:reverse-expert-kb-autosync`
   - `infra:oracle-fleet-healthcheck`
   - `ops-assistant:high-frequency`
   - `ops-assistant:daily-report`

## Jobs intentionally left enabled
- `healthcheck:security-audit`
- `healthcheck:update-status`
- `maintenance:nightly-system-check-and-clean`
- `reverse-agent:skills-sync`
- `infra:self-server-44005:prompt-optimizer-health`
- `Memory Dreaming Promotion`

## Root cause evidence collected
- Gateway crashed repeatedly with:
  - `Unhandled promise rejection: Error: Agent listener invoked outside active run`
- Nginx errors were downstream symptoms:
  - `connect() failed (111) while connecting to upstream http://127.0.0.1:18789`

## Notes
This pass reduces noise and version-label confusion, but does not fix the upstream OpenClaw runtime bug causing `Agent listener invoked outside active run`.
A future pass should focus on reproducing/minimizing the triggering workflow and checking whether a newer OpenClaw build contains a fix.
