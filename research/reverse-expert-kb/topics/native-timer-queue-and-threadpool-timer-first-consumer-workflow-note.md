# Native Timer Queue and Threadpool Timer First-Consumer Workflow Note

Topic class: concrete workflow note
Ontology layers: native practical workflow, Windows async ownership, timer object truth, callback-queue truth, first-consumer proof
Maturity: practical
Related pages:
- topics/native-practical-subtree-guide.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md
- topics/native-apc-alertable-wait-first-consumer-workflow-note.md
- topics/runtime-behavior-recovery.md
Related source notes:
- sources/native-binary/2026-04-04-native-timer-queue-threadpool-timer-notes.md

## 1. Why this note exists
Windows-heavy native cases often show a timer object, timer queue registration, or threadpool timer setup and then stop too early.

The common overclaim is:

```text
CreateTimerQueueTimer / SetThreadpoolTimer seen
  == callback will run
  == callback already owns later behavior
```

The smaller truthful ladder is:

```text
timer object created/set
  != timer still armed at the moment that matters
  != callback queued truth
  != callback not already cancelled/replaced
  != callback running truth
  != first behavior-changing consumer truth
```

This note is for the narrower case where the broad async problem is already known to be timer-shaped and the next useful output is one first consumer, not generic callback taxonomy.

## 2. When to use this note
Use this note when most of these are true:
- the case is native Windows-heavy
- the async boundary has already narrowed specifically to timer queues or threadpool timers
- you can already see `CreateTimerQueueTimer`, `SetThreadpoolTimer`, or equivalent timer setup/cancel paths
- the remaining uncertainty is whether the timer actually queues or delivers the callback that changes behavior

Do **not** use this note when:
- the real bottleneck is still broad callback plumbing or event-loop routing
- the case is more honestly IOCP, APC, GUI-message, or signal-slot shaped
- the first consumer is already known and the remaining problem is inside its body

## 3. Conservative doc-backed anchors
From Microsoft Learn:
- `CreateTimerQueueTimer` creates a timer-queue timer and calls the callback when the timer expires
- if both due time and period are nonzero, the timer fires first at due time and then periodically
- periodic timer callbacks can be queued whether or not the previous callback has finished executing
- `SetThreadpoolTimer` sets a threadpool timer, replacing the previous timer if any
- if `SetThreadpoolTimer` is called with a NULL due time, the timer ceases to queue new callbacks, but already queued callbacks can still occur

From Raymond Chen’s Windows thread-pool note:
- cancelling a timer prevents future callbacks from being created, but there is a race if the callback was already scheduled
- `Set...Ex` returning FALSE can mean the callback has gone too far to be recalled
- waiting for outstanding callbacks is the way to learn that cancellation is really complete

Operator consequence:
- “timer was set” is weaker than “callback was queued,” and “callback was queued” is weaker than “this callback body first changed behavior.”

## 4. Boundary objects to keep separate
### A. Timer-object truth
Freeze:
- which timer API family is used
- due-time / period / window-length or flags
- one timer object handle / pointer identity

### B. Armed-versus-cancelled truth
Ask:
- was the timer later replaced?
- was it cancelled/unset with NULL due time or a delete path?
- was cancellation early enough to prevent queuing?

### C. Callback-queued truth
A timer can be configured without a callback yet being queued at the moment you care about.
Do not flatten configuration into queueing.

### D. Callback-running truth
A callback may already be queued but not yet running, or it may run after you think the timer was “closed.”

### E. First-consumer truth
Only after D should you claim the callback owns later behavior.
The useful unit is one callback body or one immediate downstream consumer that first changes state/behavior.

## 5. Default workflow
### Step 1: freeze one representative timer object
Pick one timer object and record:
- API family (`CreateTimerQueueTimer` vs `SetThreadpoolTimer`)
- due time
- periodic vs one-shot
- flags / window length
- callback pointer + parameter pointer if visible

### Step 2: separate set/unset from queue/delivery
Write the smaller label explicitly:

```text
timer created/set
  -> callback may become eligible
  -> callback may be queued
  -> callback may run
  -> callback body / first consumer may change behavior
```

This keeps you from stopping at registration.

### Step 3: look for replacement/cancellation races
Cheap discriminants:
- another `SetThreadpoolTimer` replaces the previous timer
- NULL due time stops new callbacks from being queued
- delete/close paths can still race with already queued callbacks

Do not narrate “timer cancelled, therefore callback impossible” without checking whether a callback was already on its way.

### Step 4: prove one callback body or first downstream consumer
For one representative timer, prove either:
- the callback body itself first changes behavior
- or one immediate downstream consumer (work item, state write, follow-on dispatch) does

### Step 5: handle periodic timers honestly
For periodic timers, do not assume one callback instance implies stable ordering or single-instance ownership.
Microsoft explicitly notes that periodic callbacks can be queued even if the previous callback has not finished.

## 6. Practical failure patterns this note prevents
- “timer registration exists, so the watchdog/worker definitely ran”
- “timer was cancelled, so no callback could have raced through”
- “periodic timer means one linear callback chain”
- “threadpool timer closed, therefore no outstanding callback can still matter”

## 7. Sources
See: `sources/native-binary/2026-04-04-native-timer-queue-threadpool-timer-notes.md`

Primary references:
- https://learn.microsoft.com/en-us/windows/win32/api/threadpoollegacyapiset/nf-threadpoollegacyapiset-createtimerqueue
- https://learn.microsoft.com/en-us/windows/win32/api/threadpoollegacyapiset/nf-threadpoollegacyapiset-createtimerqueuetimer
- https://learn.microsoft.com/en-us/windows/win32/api/threadpoolapiset/nf-threadpoolapiset-setthreadpooltimer
- https://devblogs.microsoft.com/oldnewthing/20230428-00/?p=108110
