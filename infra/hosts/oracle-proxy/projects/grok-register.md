# Grok Register Stack

## Status
- Status: retired-cleaned
- Retired on: 2026-06-07
- Previous root path: `/root/grok-register-standalone`
- Previous public adapter port: `15072`

## Retirement outcome
Per user instruction, this legacy Grok register Camoufox solver stack is no longer an active project on `oracle-proxy`.

Cleaned Docker runtime objects on 2026-06-07:
- removed container `grok-register-camoufox`
- removed container `grok-register-camoufox-adapter`
- removed local images `grok-register-standalone-camoufox:latest` and `grok-register-standalone-camoufox-adapter:latest`
- removed Docker network `grok-register-standalone_default`
- verified public listener `:15072` was gone

The source/archive directory was retained at `/root/grok-register-standalone`, but its compose entrypoint was renamed from `docker-compose.yml` to `docker-compose.retired-20260607.yml` and a `RETIRED-20260607.md` marker was written on-host to prevent accidental restart.

## Operational rule
Do not treat this stack, its containers, or port `15072` as expected runtime. Future fleet checks should flag any reappearance as intentional redeploy-needed verification or unexpected drift.

## Historical note
This stack previously provided a separate Camoufox + adapter path for Grok registration tooling. It was distinct from the Tavily registration solver stack and from the active `grok2api` service.
