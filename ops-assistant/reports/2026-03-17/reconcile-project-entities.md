# Project Entity Reconciliation - 2026-03-17

## oracle-proxy
Matched documented projects:
- Tavily Proxy
- Tavily Key Generator
- ExaFree
- Grok Register Stack
- Grok2API
- CLIProxy
- OpenAi (migrated) [archive]

Undocumented project candidates:
- /root/AntiCAP-WebApi-docker/docker-compose.yml
- /root/FlareSolverr/docker-compose.yml
- /root/ProxyCat/docker-compose.yml
- /root/backups/grok2api-20260313-133823/docker-compose.yml
- /root/clove/docker-compose.yml
- /root/gpt-load/docker-compose.yml

## oracle-docker-proxy
Matched documented projects:
- Registry Proxies
- Harbor footprint [dormant]

Documented but missing in runtime:
- registry-ui
- hubcmd-ui

Interpretation:
- This host is no longer just "some registry hints"; the runtime registry proxy stack is clearly real and matched.
- `registry-ui` and `hubcmd-ui` currently look like explicit missing/inactive documented projects.

## ali-cloud
Matched documented projects:
- EasyImages
- camoufox-remote

Missing documented infra/control-plane item:
- 1Panel control plane

Interpretation:
- 1Panel should be treated primarily as machine-level control plane; not as a noisy app drift warning.

## oracle-mail
Known retired footprints:
- Mailu deployment footprint [retired]
- moemail repository [retired]
