# Oracle Fleet Maintenance Workflow

## Goal

Continuously inspect the documented Oracle remote hosts and keep the `infra/` knowledge base current.

This workflow is about safe recurring observability and documentation maintenance, not autonomous repair.

---

## Primary operating rules

### 1. Default to read-only inspection

Allowed by default:
- SSH reachability checks
- host identity confirmation
- uptime/load checks
- disk and memory checks
- docker/container summaries
- listener/socket summaries
- lightweight service/process visibility checks
- writing findings back into `infra/`

Not allowed by default:
- restarting services
- deleting files
- upgrading packages
- changing firewall/SSH/network settings
- changing compose/systemd/runtime configs
- mutating remote repos or project files

### 2. Use `infra/` as source of truth

Start with:
- `infra/inventory.yaml`
- `infra/host-status.yaml`
- `infra/QUICKMAP.md`

Then inspect host-specific docs before deciding what matters operationally.

### 3. Inspect Oracle remote hosts as a fleet, but preserve host-specific context

Default host selection rules:
- include `provider: oracle`
- exclude the local machine entry (`oracle-open_claw`) unless the user explicitly wants it
- skip clearly unreachable hosts only after a direct SSH/connectivity attempt confirms that

### 4. Prefer concise operational deltas

The purpose is not to rewrite entire host docs every run.

Prefer concise updates such as:
- host still healthy / healthy with caution
- resource pressure increased
- key containers missing or newly present
- listeners changed materially
- host role still matches docs / no longer matches docs
- retired host still dormant / unexpectedly revived

### 5. Write back into the right places

Typical write targets:
- per-host inspection summary → `infra/hosts/<host>/CHANGELOG.md`
- changed reachability/lifecycle/importance → `infra/host-status.yaml`
- only if host identity or role meaningfully drifted → `HOST.md` / `PROJECTS.md` / `NETWORK.md`

### 6. Commit and sync

If `infra/` changed:
- commit inside `/root/.openclaw/workspace/infra`
- run `infra/bin/sync-infra.sh`

---

## Recommended inspection shape per host

For each selected Oracle host, aim to gather a lightweight snapshot such as:
- hostname
- uptime / load
- root disk usage
- memory / swap posture
- active Docker containers (if Docker exists)
- important listeners
- one short judgment:
  - healthy
  - healthy but capacity-tight
  - retired and still dormant
  - reachable but suspicious drift
  - unreachable

Do not over-collect. Prefer a compact, repeatable health snapshot.

---

## Special heuristics for the current fleet

### oracle-proxy
Treat as a multi-role active utility host. Pay attention to:
- tavily stack
- grok-related containers
- cliproxy
- proxy/network front-door components
- whether resource posture still looks comfortable

### oracle-docker_proxy
Treat as a small-footprint registry/proxy host. Pay attention to:
- long-lived registry containers
- caddy front-door presence
- memory pressure / swap use
- avoid recommending service sprawl on this host

### oracle-mail
Treat as a retired/dormant host unless evidence shows otherwise. Pay attention to:
- unexpected public listeners
- accidental container revival
- whether dormant/archived state still matches documentation

---

## Best-effort documentation rule

If an exact changelog edit misses because text drifted:
- re-read the file
- append a concise new dated line or bullet
- do not fail the whole run just because a documentation splice missed exact text

If one host check fails but others succeed:
- record the failure for that host
- continue the fleet run
- do not collapse the entire maintenance pass unnecessarily

---

## Suggested cadence

This workflow is better suited to:
- every 12 hours
- or daily

It normally does not need hourly execution.

---

## Example successful run outcome

A good run typically ends with:
- 2–4 Oracle remote hosts checked
- 0–3 changelog/status doc updates
- 0 or 1 `infra` commit
- `infra/bin/sync-infra.sh` run if changes were made
- no chat delivery unless explicitly requested by the user or cron delivery policy
