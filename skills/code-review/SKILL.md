---
name: code-review
description: "Review code changes against both project standards and the requested spec, using isolated reviewers when useful."
homepage: "https://github.com/mattpocock/skills"
license: "MIT"
---

# Code Review

Use when reviewing a diff, PR, branch, generated implementation, or before committing substantial code.
Adapted from `mattpocock/skills`; upstream reference is in `references/upstream-code-review.md`.

## Two-axis review

Review along two independent axes:

1. **Standards review** — does the code fit this repository's architecture, naming, test style, safety rules, and maintainability expectations?
2. **Spec review** — does the code implement what was asked, no less and no more?

Keep these axes separate until the final summary. A beautiful implementation of the wrong thing is still wrong; a correct behavior implemented with poor seams is still risky.

## Inputs to inspect

- The diff base: explicit commit/branch/tag if provided, otherwise infer from git state.
- The user's request/spec/ticket/PR body.
- Local guidance when present: `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `docs/agents/`, `docs/adr/`, project README.
- Relevant tests and existing patterns around touched files.

## OpenClaw parallel review pattern

For non-trivial reviews, use OpenClaw subagents instead of doing both axes in one pass:

- Spawn one isolated Standards reviewer.
- Spawn one isolated Spec reviewer.
- Give both the same diff/base and repo constraints.
- Use `sessions_yield` to wait for completion events.
- Merge findings, deduplicate, and rank by severity.

Do not use subagents for tiny diffs where direct review is faster.

## Severity

- **Blocker**: likely broken behavior, data loss, security issue, migration hazard, or cannot verify core requirement.
- **Major**: maintainability/test/architecture issue that should be fixed before merge.
- **Minor**: readability, naming, small test improvement, localized cleanup.
- **Nit**: optional polish; do not let nits obscure important findings.

## Review checklist

Standards:

- follows existing architecture and module boundaries
- tests target public seams rather than internals
- no hidden coupling, broad mocks, or tautological assertions
- error handling, logging, retries, and cleanup are appropriate
- no secrets or private data leaked
- no unsafe destructive operations without guardrails
- code is easy for future agents/humans to navigate

Spec:

- every requested behavior is implemented
- acceptance criteria are covered by tests or explicit verification
- edge cases from the request are handled
- no unrelated scope creep
- user-facing behavior, migration notes, or docs updated when needed

## Output shape

Return concise findings first:

- Verdict: approve / approve with fixes / request changes / blocked
- Blockers
- Major issues
- Minor issues
- Verification evidence checked
- Suggested patch plan if fixes are needed

When no issues are found, say what was checked; do not invent nits.
