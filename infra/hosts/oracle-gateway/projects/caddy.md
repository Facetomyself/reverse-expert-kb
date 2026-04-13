# caddy on oracle-gateway

This document is now mostly historical/auxiliary. Caddy is no longer the primary public front door on this host.

## Current role
- retained local/helper web server
- alternate ports: `8080` and `8443`
- admin API: `127.0.0.1:2019`
- legacy content path support for `backup.zhangxuemin.work`

## Operator guidance
- treat Caddy here as a helper service, not the main identity of the host
- keep public gateway responsibilities centered on the documented Hysteria runtime
- avoid expanding this host back into a mixed catch-all front door
