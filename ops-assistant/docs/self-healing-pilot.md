# Self-healing Pilot Plan

## Goal
在不扩大风险的前提下，为 ops-assistant 引入**白名单低风险自愈试点**。

## Pilot scope
Only these targets are in pilot scope initially:
- local host: `openclaw-gateway`
- oracle-proxy container: `proxy-tavily-proxy-1`
- oracle-proxy container: `tavily-scheduler`

## Operating mode in v1
- not auto-wired into hourly cron yet
- manual / operator-triggered first
- every action must leave a report
- every action must perform post-check
- one bounded attempt only

## Action contract
For each remediation attempt:
1. record target + reason
2. verify target is on whitelist
3. execute exactly one restart action
4. re-check target health/status
5. write a remediation report
6. send Telegram notice via alerts bot

## Not in pilot
- caddy reload/restart
- compose rebuilds
- multi-step shell fixes
- any config mutation
- any package/system action
