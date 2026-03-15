# .learnings Quick Guide

Use this folder to capture mistakes, lessons, and missing capabilities so they can be reused later instead of rediscovered.

## Three-Way Split

### 1) ERRORS.md
Use when something **should have worked, but didn't**.

Examples:
- command failed
- API/tool returned an error
- fetch/search timed out or was blocked
- config was missing and caused failure
- behavior was unexpectedly wrong

Question to ask:
> Did this fail or break?

If yes, log to `ERRORS.md`.

---

### 2) LEARNINGS.md
Use when we now know a **better rule, correction, constraint, or best practice**.

Examples:
- the human corrected the approach
- prior understanding was outdated or wrong
- a more reliable workflow was discovered
- a recurring pattern is now obvious

Question to ask:
> Did we learn how to do this better next time?

If yes, log to `LEARNINGS.md`.

---

### 3) FEATURE_REQUESTS.md
Use when the human wants a capability that **does not exist yet**.

Examples:
- automate a recurring task
- turn a workflow into a skill
- add a button/shortcut/scheduled task
- support a new integration/path

Question to ask:
> Is this a missing capability rather than a broken existing one?

If yes, log to `FEATURE_REQUESTS.md`.

---

## Tie-Breakers

- If it both failed **and** taught a lesson: log the failure first, then write the durable rule as a learning.
- If it feels like "I wish you could do X" rather than "X broke": it is probably a feature request.
- If it is mainly a host/tool/environment gotcha that should guide future work, consider promoting it from `LEARNINGS.md` into `TOOLS.md` or `AGENTS.md`.

## Promotion Path

Typical flow:

1. incident/request happens
2. log to `ERRORS.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
3. if it repeats or proves broadly useful, promote it to:
   - `AGENTS.md`
   - `TOOLS.md`
   - `MEMORY.md`
   - a reusable skill under `skills/`
