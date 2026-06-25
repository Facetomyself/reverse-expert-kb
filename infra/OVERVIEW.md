# Infra Overview

## Canonical Oracle host set
- `oracle-open_claw` — current OpenClaw host; local maintenance target for disk / memory / safe cleanup / basic service health
- `oracle-proxy` — proxy/search/tooling host
- `oracle-gateway` — gateway / Hysteria host
- `oracle-mail` — web-app host with archived mail-stack footprints
- `oracle-newapi-primary` — primary New API / AI API relay host; former `oracle-registry`
- `oracle-newapi-standby` — standby New API / AI API relay host; former `oracle-reverse-dev`

## Naming policy
- Use only the semantic names above in current docs and automation.
- Transitional names such as `oracle-docker-proxy`, `oracle-new1`, and `oracle-new2` are no longer canonical and should not be used in active inventory or operational automation.

## Current role highlights
### `oracle-gateway`
- primary gateway / Hysteria machine
- helper `caddy` reduced to local/helper ports

### `oracle-newapi-primary`
- primary New API / AI API relay host, formerly `oracle-registry`
- New API lives at `/opt/new-api`, loopback app listener `127.0.0.1:13000`, Caddy public HTTP on `:80`
- prefer this canonical name; keep `oracle-registry` only as a compatibility alias

### `oracle-newapi-standby`
- standby New API / AI API relay host, formerly `oracle-reverse-dev`
- New API lives at `/opt/new-api`, loopback app listener `127.0.0.1:13000`, Caddy public HTTP on `:80`
- prefer this canonical name; keep `oracle-reverse-dev` only as a compatibility alias
