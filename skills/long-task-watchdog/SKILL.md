---
name: long-task-watchdog
description: Choose and attach the right continuation mechanism for long or stall-prone work. Use when a task may outlive the current turn, needs a later re-check, needs a watchdog/reminder, or the user says things like "继续盯", "稍后再看", "有结果再告诉我", "继续做", "等会再查", "check back later", or "keep watching". Prefer current-turn completion when possible; otherwise choose among background process waiting, short-lived cron watchdogs, or TaskFlow-style multi-step ownership.
---

# Long Task Watchdog

Use this skill to make long-task continuation explicit and reliable instead of vague.

## Core rule

Do **not** say "我继续" or "我盯着" unless a real continuation path has been attached.

Choose one of these, in order:
1. finish in the current turn
2. wait on an already-running background process
3. create a short-lived cron watchdog
4. use TaskFlow-style multi-step ownership for larger jobs

Heartbeat is **not** the default long-task engine.

## Decision ladder

### 1) Finish now
Use no watchdog at all when:
- next steps are clear
- low-risk
- likely to finish within about 5 minutes

### 2) Wait on an existing process
Use `process` / background execution, not cron, when:
- a command is already running
- the only missing step is waiting / polling / collecting logs
- there is no real "forget to resume" gap yet

### 3) Create a short-lived cron watchdog
Use cron when:
- the task needs a re-check in about 5–30 minutes
- the work may stall because of turn boundaries, waiting, downloads, installs, or remote background activity
- the user wording implies watch/re-check intent

Default watchdog shape:
- one-shot first check at about **+10 minutes**
- if still unresolved, create at most **1–2 more short follow-ups**
- stop/delete once the task is complete or clearly blocked

### 4) Prefer TaskFlow-style ownership
Use TaskFlow-style handling when:
- the job is expected to outlive about 30 minutes
- it has multiple dependent stages
- it needs one owner context with resumable state
- multiple child tasks or detached runs may be involved

If TaskFlow runtime is not actually wired in the current implementation path, still emulate the same discipline:
- one owner
- one current step
- one persisted state summary
- one explicit waiting reason
- one clear resume condition

## Heartbeat policy

- Do not use heartbeat as the primary continuation mechanism for one task.
- Do not lower global heartbeat frequency just to rescue a stuck task.
- If `HEARTBEAT.md` is disabled, do not try to force a heartbeat-based workaround.
- Heartbeat is for low-frequency patrol and batch checks, not exact task resumption.

## Cron construction rules

### Scheduling
Prefer:
- `schedule.kind="at"` for one-shot re-checks
- `schedule.kind="every"` only when the task truly needs repeated orchestration until completion

### Session target
Prefer:
- `sessionTarget="current"` when the follow-up should return to the same owner conversation and can wait until the current turn ends
- `sessionTarget="isolated"` when the work should start independently now and not be blocked behind the current turn

Important gotcha:
- a cron bound to the **current session** may wait until the current turn exits before it actually runs
- if you need detached execution immediately, prefer `isolated`

### Delivery
Default to:
- `delivery.mode="none"`

Only use announce/webhook delivery when the target is explicit and known-good.

Important gotcha:
- avoid vague/implicit announce targets like old `@heartbeat` patterns
- prior watchdog failures often came from delivery misconfiguration, not from the task itself

### Naming
Use a human-readable job name that includes the target and purpose, for example:
- `watch-home-nas-model-download`
- `check-self-server-image-import`
- `follow-up-remote-build`

## Prompt contract for watchdog jobs

A good watchdog prompt should always include:
- what to check
- what counts as success
- what counts as still-running
- what counts as failure/blockage
- what to do next in each case
- whether to keep waiting, schedule another follow-up, or stop

Template shape:

```text
Re-check <task>.

If complete:
- report the result
- do the next obvious step if requested
- stop/delete any temporary watchdog

If still running:
- report concrete progress (size/log tail/PID/state)
- decide whether one more short re-check is justified
- if yes, schedule one more short follow-up

If blocked or failed:
- report the exact blocker
- choose the most practical fallback or ask for intervention if needed
```

## Language triggers

Treat these as strong hints that a continuation mechanism should be attached if the work will not cleanly finish now:

### Immediate continuous intent
- `继续`
- `继续做`
- `继续处理`
- `不要停`
- `别停`
- `一直做完`

### Watch / re-check intent
- `继续盯`
- `盯一下`
- `监测`
- `稍后再看`
- `等会再查`
- `有结果再告诉我`
- `check back later`
- `keep watching`

## Anti-patterns

Do not:
- rely on heartbeat alone for one task
- create a recurring cron with no stop condition
- use announce delivery without a concrete valid target
- create a watchdog when a local/background process wait is enough
- create a long-lived cron loop for what should really be a TaskFlow-style multi-step job
- leave completion ambiguous; always define what ends the watchdog

## Minimal examples

### Example A: one-shot remote install re-check
Use a cron watchdog when a remote install is still running and you need a check in 10 minutes.

### Example B: active download already has a PID
Use background process waiting first. Add cron only if the check must survive turn boundaries.

### Example C: multi-stage deployment
Use TaskFlow-style ownership or a recurring orchestrator with explicit state/stop rules, not heartbeat.
