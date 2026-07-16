---
name: diagnosing-bugs
description: "Diagnose hard bugs, regressions, flaky failures, broken services, or slow behavior with a tight feedback loop before fixing."
homepage: "https://github.com/mattpocock/skills"
license: "MIT"
---

# Diagnosing Bugs

Use when something is broken, failing, throwing, flaky, slow, or needs root-cause analysis.
Adapted from `mattpocock/skills`; upstream reference is in `references/upstream-diagnosing-bugs.md`.

## Non-negotiable principle

Build a red-capable feedback loop before theorizing. A bug is not understood until there is one command, script, test, curl, browser check, trace replay, or harness that can catch the user's exact symptom.

If no loop can be built, say so, list what was tried, and ask for the missing artifact/access: logs, HAR, fixture, repro env, screen recording, or permission for temporary instrumentation.

## OpenClaw workflow

1. **Frame the symptom**
   - Restate the exact user-visible failure.
   - Identify the likely seam: CLI, HTTP endpoint, UI flow, function boundary, service health, data pipeline, or remote host.
   - Read local project docs first when present: `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `docs/adr/`.

2. **Create the tightest feedback loop available**
   Prefer, in order:
   - failing test at the correct public seam
   - single-file test / integration test / e2e test
   - curl or HTTP script against a running service
   - CLI command with fixture input and asserted output
   - browser automation with DOM/console/network assertions
   - replayed trace / captured request / fixture
   - throwaway harness
   - stress / fuzz / repeated loop for nondeterministic bugs
   - `git bisect run`-ready harness when the regression range matters

   Completion for this phase requires evidence: paste or summarize the command actually run and the failing output/signal.

3. **Reproduce and minimise**
   - Run the loop until it shows the failure.
   - Confirm it is the same symptom the user reported, not a nearby failure.
   - Cut inputs/config/steps one at a time until every remaining element is load-bearing.

4. **Hypothesize before changing**
   - Generate 3–5 ranked, falsifiable hypotheses.
   - Format: `If X is the cause, changing/observing Y should make Z happen.`
   - If user/domain knowledge could materially re-rank them, mention the ranking and proceed unless blocked.

5. **Instrument one variable at a time**
   - Prefer debugger/REPL inspection when practical.
   - Otherwise add targeted logs at boundaries that distinguish hypotheses.
   - Tag temporary logs with a unique prefix like `[DEBUG-a4f2]` so cleanup is grep-able.
   - For performance, measure first: baseline timing, profiler, query plan, or resource metric before changing code.

6. **Fix with regression protection**
   - Add a regression test before the fix when a correct seam exists.
   - If no correct seam exists, document that architecture/testing gap and still verify with the best available loop.
   - Apply the smallest fix that satisfies the red loop.

7. **Cleanup and close**
   Before declaring done:
   - original repro/feedback loop is green
   - regression test passes, or absence of seam is documented
   - broad test/type/lint gate run when appropriate
   - `[DEBUG-*]` logs removed
   - throwaway harnesses deleted or moved to clearly marked debug artifacts
   - root cause is stated plainly

## Tooling notes

- Use `exec` for tests, scripts, services, logs, and CLI repros.
- Use `browser-automation`/`browser` for UI bugs and login-sensitive flows.
- Use `python-debugpy` or `node-inspect-debugger` when the runtime fits.
- Use `spike` for throwaway prototypes or harness feasibility checks.
- Use `long-task-watchdog`, background processes, or `sessions_spawn` when diagnosis may outlive the turn.

## Output shape

For substantial bug work, report:

- Symptom
- Feedback loop command and result
- Root cause
- Fix
- Verification
- Follow-up risk or architecture gap, if any
