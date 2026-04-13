# Infra Overview

## Canonical Oracle host set
- `oracle-open_claw` — current OpenClaw host; local maintenance target for disk / memory / safe cleanup / basic service health
- `oracle-proxy` — proxy/search/tooling host
- `oracle-gateway` — gateway / Hysteria host
- `oracle-mail` — web-app host with archived mail-stack footprints
- `oracle-registry` — current registry front-door host
- `oracle-reverse-dev` — reverse-development utility host

## Naming policy
- Use only the semantic names above in current docs and automation.
- Transitional names such as `oracle-docker-proxy`, `oracle-new1`, and `oracle-new2` are no longer canonical and should not be used in active inventory or operational automation.

## Current role highlights
### `oracle-gateway`
- primary gateway / Hysteria machine
- helper `caddy` reduced to local/helper ports

### `oracle-registry`
- current registry front-door host
- use this name everywhere instead of earlier generic host naming

### `oracle-reverse-dev`
- current reverse-development / MCP utility host
- use this name everywhere instead of earlier generic host naming
