---
name: oracle-fleet-maintenance
description: Read-only recurring maintenance and health-check workflow for Oracle remote hosts documented under `infra/`. Use when a task is about periodic Oracle host fleet checks, remote Oracle machine inspection, SSH-based Oracle host health review, infra documentation refresh for Oracle hosts, or a cron/reminder should inspect Oracle remote machines and write findings back into `infra/`.
---

# Oracle Fleet Maintenance

Use this skill for recurring inspection of documented Oracle remote hosts.

## Scope

Default scope is:
- Oracle remote hosts from `infra/inventory.yaml`
- reachable over SSH
- excluding the local machine (`oracle-open_claw`) unless explicitly requested

Typical included hosts:
- `oracle-proxy`
- `oracle-docker_proxy`
- `oracle-mail`

## Core behavior

- Default mode is **read-only inspection**.
- Do not restart services, clean remote hosts, update packages, or mutate remote configs unless explicitly asked.
- Treat this workflow as:
  - fleet health check
  - infra knowledge-base refresh
  - changelog/status maintenance
- Prefer writing concise factual deltas back into `infra/` over verbose prose.

## Required read path

Start with:
- `infra/inventory.yaml`
- `infra/host-status.yaml`
- `infra/QUICKMAP.md`

Then read relevant host docs as needed:
- `infra/hosts/<host>/HOST.md`
- `infra/hosts/<host>/PROJECTS.md`
- `infra/hosts/<host>/NETWORK.md`
- `infra/hosts/<host>/CHANGELOG.md`

## Detailed workflow

Read and follow:
- `references/workflow.md`

## Output contract

A normal successful run should usually produce:
- read-only checks across the Oracle remote host set
- concise per-host findings
- updates to `infra/hosts/<host>/CHANGELOG.md` when there is a meaningful new observation
- optional refresh of `infra/host-status.yaml` if reachability/lifecycle/importance meaningfully changed
- an `infra` git commit if files changed
- GitHub sync of the `infra` repo via `infra/bin/sync-infra.sh`

Do not fail the whole run only because one minor documentation update missed exact text. Prefer re-read + small local rewrite, then continue with best-effort documentation if the core inspection completed.
