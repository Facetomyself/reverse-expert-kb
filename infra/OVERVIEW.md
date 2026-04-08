# Infra Overview

## Canonical Oracle host set
- `oracle-proxy` — proxy/search/tooling host
- `oracle-gateway` — gateway / Hysteria / DERP host
- `oracle-mail` — web-app host with archived mail-stack footprints
- `oracle-registry` — current registry front-door host
- `oracle-reverse-dev` — reverse-development utility host

## Tailnet reference IPs
- `oracle-gateway` — `100.116.171.76`
- `oracle-mail` — `100.116.13.44`
- `ali-cloud` — `100.98.184.19`
- `oracle-registry` — `100.96.23.110`
- `oracle-reverse-dev` — `100.79.183.3`

## Naming policy
- Use only the semantic names above in current docs and automation.
- Transitional names such as `oracle-docker-proxy`, `oracle-new1`, and `oracle-new2` are no longer canonical and should not be used in active inventory or operational automation.
- Historical reports may still mention old names; treat them as historical context only.

## Current role highlights
### `oracle-gateway`
- primary gateway / DERP / Hysteria machine
- public TCP `80/443` owned by `derper`
- helper `caddy` reduced to local/helper ports

### `oracle-registry`
- current registry front-door host
- use this name everywhere instead of earlier generic host naming

### `oracle-reverse-dev`
- current reverse-development / MCP utility host
- use this name everywhere instead of earlier generic host naming
