---
name: reverse-kb-autosync
description: Maintain and grow the reverse-engineering expert knowledge base under `research/reverse-expert-kb/` through recurring autonomous runs. Use when a task is about periodic KB maintenance, reverse-knowledge-base autosync, branch-balance review, run-report generation, KB consolidation, or archival sync of the reverse KB to GitHub. Also use when a cron/reminder/automation should run the reverse KB workflow on a schedule.
---

# Reverse KB Autosync

Use this skill for recurring maintenance of `research/reverse-expert-kb/`.

## Core behavior

- Keep the KB cumulative, structured, and practical.
- Prefer concrete, case-driven workflow notes over abstract taxonomy growth.
- Treat browser anti-bot and mobile protected-runtime branches as strong existing branches; do not let them monopolize growth forever.
- Always preserve provenance, run reports, git history, and GitHub archival sync.

## Required read order

Start with:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent files in `research/reverse-expert-kb/runs/`
- relevant pages in `research/reverse-expert-kb/topics/`
- recent source notes in `research/reverse-expert-kb/sources/`

## Detailed workflow

Read and follow:
- `references/workflow.md`

## Output contract

Every run should normally produce:
- KB improvements and/or structural consolidation
- one run report under `research/reverse-expert-kb/runs/`
- a git commit if files changed
- archival sync via `scripts/sync-reverse-expert-kb.sh`

If logging to `.learnings/ERRORS.md` fails, treat it as best-effort only and do not fail the whole run.
