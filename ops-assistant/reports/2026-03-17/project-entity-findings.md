# Project Entity Findings - 2026-03-17

This report records the stronger entity-level reconciliation pass. It is currently treated as an enhancement layer alongside the stable hint-based cron path.

## oracle-proxy
Documented projects positively matched to runtime:
- Tavily Proxy
- Tavily Key Generator
- ExaFree
- Grok Register Stack
- Grok2API
- CLIProxy
- OpenAi (migrated) [archive]

High-confidence undocumented project candidates:
- /root/AntiCAP-WebApi-docker/docker-compose.yml
- /root/FlareSolverr/docker-compose.yml
- /root/ProxyCat/docker-compose.yml
- /root/backups/grok2api-20260313-133823/docker-compose.yml
- /root/clove/docker-compose.yml
- /root/gpt-load/docker-compose.yml

Interpretation:
- `oracle-proxy` is no longer just hint-misaligned; it has several real compose-level project candidates worth formal documentation or archival classification.

## oracle-docker-proxy
Documented projects positively matched to runtime:
- Registry Proxies
- Harbor footprint [dormant]

Documented but currently missing in runtime:
- registry-ui
- hubcmd-ui

Interpretation:
- Runtime registry proxies are real and should be treated as a concrete project entity, not just `reg-` hints.
- `registry-ui` and `hubcmd-ui` are better framed as documented-but-inactive/missing components.

## ali-cloud
Documented projects positively matched to runtime:
- EasyImages
- camoufox-remote
- 1Panel control plane [infra-only]

Interpretation:
- `1Panel` should remain a control-plane / infra entity, not an app-project drift warning.

## oracle-mail
Known retired entities:
- Mailu deployment footprint [retired]
- moemail repository [retired]
