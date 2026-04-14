---
name: cloudflare-dns-maintenance
description: Read-only Cloudflare DNS and zone-maintenance workflow for domains documented under `infra/`. Use when a task is about Cloudflare domain maintenance, DNS drift checks, zone reconciliation, cleanup planning, baseline refreshes, or when a cron/reminder should audit the live Cloudflare zone against `infra/` documentation without applying changes by default.
---

# Cloudflare DNS Maintenance

Use this skill for recurring Cloudflare DNS maintenance of the documented zone.

## Core behavior

- Default mode is **read-only reconciliation**.
- Do not mutate Cloudflare records unless the user explicitly asks.
- Prefer exporting a live snapshot, comparing it with committed documentation/baselines, and producing a concise proposed change set.
- Treat `infra/` as the documentation truth source and Cloudflare as the live runtime state to reconcile.

## Required read order

Start with:
- `infra/inventory.yaml`
- `infra/dns-reconciliation.md`
- `infra/dns-cleanup-plan.md`
- `infra/dns-first-wave.md`

Then read only the relevant host docs for affected names:
- `infra/hosts/<host>/NETWORK.md`
- `infra/hosts/<host>/CHANGELOG.md`

Read `infra/cloudflare-dns/terraform.auto.tfvars` only when the zone id / API token source must be confirmed. Do not echo or copy secrets into reports, commits, or chat.

## Live snapshot workflow

Use:
- `scripts/cloudflare_zone_snapshot.py`

The script can:
- load Cloudflare credentials from environment variables or `infra/cloudflare-dns/terraform.auto.tfvars`
- fetch the full live DNS record set with pagination
- normalize records into a deterministic JSON snapshot
- compare the live zone against a committed baseline snapshot
- render a concise Markdown summary without leaking secrets

Prefer these conventions:
- committed baseline: `infra/cloudflare-dns/baseline-records.json`
- committed baseline summary: `infra/cloudflare-dns/baseline-summary.md`
- change reports on meaningful delta only: `infra/cloudflare-dns/reports/YYYY-MM-DD.md`

## Reconciliation loop

1. Export the live zone snapshot.
2. Compare live records against `infra/cloudflare-dns/baseline-records.json` if it exists.
3. Compare the meaningful record set against documented host/domain truth in `infra/`.
4. Classify findings as:
   - matches reality
   - partial / needs re-check
   - stale documentation
   - suspicious live drift
5. If docs are stale and live DNS looks intentional, update the relevant `infra/` files conservatively.
6. If live DNS drift is real or risky, write a proposed change set and stop short of applying it unless the user explicitly requests live Cloudflare edits.
7. Commit only the intended files if the workspace changed.

## Output contract

A normal successful run should usually produce one of:
- **no-op audit**: conclude that live DNS matches the committed baseline/docs and write nothing
- **docs delta**: update `infra/` documentation and optionally the baseline snapshot if the live state is now the approved truth
- **live drift report**: write a concise report under `infra/cloudflare-dns/reports/` describing added/removed records and the recommended next action

Keep the workflow low-noise:
- avoid per-run placeholder files
- avoid rewriting files when content is unchanged
- avoid timestamp-only diffs in committed snapshots
- keep Cloudflare writes opt-in, not automatic
