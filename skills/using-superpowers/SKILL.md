---
name: using-superpowers
description: Lightweight skill-routing guidance for OpenClaw. Use when improving how skills are selected and applied across conversations, auditing whether the current environment is over- or under-using skills, or when you want a simple policy for checking relevant skills before complex or repetitive tasks without forcing heavy meta-process on every trivial interaction.
---

# Using Superpowers

This skill is a **lightweight routing guide**, not a hard gate in front of every sentence.

Its purpose is to keep skill usage disciplined without making ordinary work clumsy.

## Core idea

Prefer using a relevant skill when it clearly helps, especially for:
- recurring workflows
- multi-step tasks
- fragile operations
- domain-specific tasks
- anything with an established checklist or proven procedure

Do **not** force a heavy skill-check ritual for every tiny read-only interaction.

## OpenClaw-adapted rule

In this environment:
- follow the system/developer instructions for skill discovery
- when a task clearly matches a skill, read that skill and follow it
- when several skills might apply, choose the most specific one
- when no skill clearly applies, proceed normally without unnecessary meta-overhead

This skill should not override clearer platform-level rules about how skills are loaded.

## Good use cases

Reach for a skill early when the task is:
- repetitive
- error-prone
- operationally sensitive
- likely to benefit from a stored workflow
- likely to be repeated in future cron jobs, infra tasks, repo maintenance, or content workflows

Examples:
- GitHub issue/PR work → `github` / `gh-issues`
- weather requests → `weather`
- skill design or cleanup → `skill-creator`
- Oracle host fleet checks → `oracle-fleet-maintenance`
- reverse KB autosync / review → `reverse-kb-autosync`

## When not to overdo it

Do not let skill-routing become busywork.

Usually you can proceed directly for:
- tiny factual replies
- simple file reads
- short status checks
- straightforward follow-up questions
- obvious one-off actions with no matching specialized skill

## Practical routing heuristic

Use this simple test:

1. Is there a clearly matching skill for this task?
   - If yes, use it.
2. If not, is the task complex, repeated, or fragile enough that a skill probably should guide it?
   - If yes, look for the most specific fit.
3. If no, proceed normally.

## Red flags

These are signs of under-using skills:
- redoing the same workflow from scratch repeatedly
- forgetting an established checklist
- mixing up where to write operational knowledge
- hand-rolling a recurring cron workflow that should become a skill
- repeatedly making the same operational mistakes

These are signs of over-using skills:
- turning every tiny interaction into a meta-routing exercise
- loading broad process skills for simple direct tasks
- spending more effort choosing a skill than doing the work

## Preferred behavior

Aim for:
- **skills early for meaningful workflows**
- **directness for trivial tasks**
- **specific skills over broad generic ones**
- **platform-native loading behavior over imported assumptions from other tools**

## Bottom line

Use skills as leverage, not ceremony.

The right outcome is:
- fewer repeated mistakes
- more reuse of good workflows
- less unnecessary meta-process
