# mattpocock/skills OpenClaw Adaptation

Source: https://github.com/mattpocock/skills
Pinned upstream HEAD: e9fcdf95b402d360f90f1db8d776d5dd450f9234
License: MIT
Imported: 2026-07-16

## Import policy

- Do not run the upstream `skills.sh` installer or Claude Code plugin in this workspace.
- Keep `upstream/` as a read-only vendor snapshot for audit and diffing.
- Enable only hand-adapted OpenClaw skills under `skills/`.
- Do not let upstream setup flows mutate root `AGENTS.md`, `MEMORY.md`, `TOOLS.md`, or other global identity/control files.
- Treat upstream `SKILL.md` content as external prompt-code: review before copying, adapt to local tools, then validate.

## Initial adapted skills

- `skills/diagnosing-bugs/` — bug diagnosis loop adapted to OpenClaw tools and evidence requirements.
- `skills/tdd/` — red/green/refactor discipline adapted to the user's low-back-and-forth preference.
- `skills/code-review/` — two-axis review adapted to OpenClaw subagents (`sessions_spawn` / `sessions_yield`).

## Deferred / reference-only

- `setup-matt-pocock-skills`: do not run globally; only useful after rewriting as a project-local initializer.
- `ask-matt`: unnecessary; OpenClaw already routes skills.
- `implement`: too opinionated about committing; absorb principles only.
- `triage`, `to-spec`, `to-tickets`, `wayfinder`, `domain-modeling`: candidates for later project-level workflows.

## OpenClaw adaptation principles

- Prefer acting with explicit assumptions over repeated interviews.
- Ask only for decisions that block safe progress or change architecture/risk materially.
- Replace Claude Code slash/tool references with OpenClaw native tools and skills.
- Long or stall-prone work should use `long-task-watchdog`, background process handling, `sessions_spawn`, or `taskflow` rather than vague promises.
- Completion claims need evidence: test/build/lint, diff, command output, screenshot, or a named blocker.
