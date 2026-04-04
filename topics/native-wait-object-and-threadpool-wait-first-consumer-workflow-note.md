# Native Wait Object and Threadpool Wait First-Consumer Workflow Note

Topic class: workflow note
Ontology layers: workflow/sensemaking, runtime-evidence bridge, native baseline practical branch
Maturity: emerging
Related pages:
- topics/native-practical-subtree-guide.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md
- topics/native-apc-alertable-wait-first-consumer-workflow-note.md
- topics/runtime-behavior-recovery.md
Related source notes:
- sources/native/2026-04-04-native-wait-object-threadpool-wait-notes.md

## 1. What this workflow note is for
This note covers a recurring Windows-native async case where the analyst has already reduced the target into a wait-shaped callback path, but the remaining bottleneck is narrower than the broad callback/event-loop note and narrower than generic completion-port ownership.

Typical symptoms:
- `CreateThreadpoolWait`, `SetThreadpoolWait`, `RegisterWaitForSingleObject`, or equivalent wait-registration helpers are visible
- static reading shows one signaled handle or one registered wait that *could* explain later behavior
- the analyst keeps overreading registration sites or object-signal folklore instead of proving which wait callback first becomes behaviorally real

The goal is to move from:

```text
one or more visible registered waits and plausible callback targets
```

to:

```text
one proved chain from wait registration
through signal-or-timeout truth
into one first consequence-bearing wait callback consumer
and one downstream effect
```

## 2. When to use this note
Use this note when most of the following are true:
- broad callback/event-loop ownership is already plausible enough that generic routing is no longer the main bottleneck
- the target visibly uses threadpool waits or legacy registered waits
- the main uncertainty is not “is there a wait?” but “which signaled/timeout-driven callback actually matters first?”
- one narrow runtime proof against one wait object or one callback family would collapse a lot of uncertainty

Common shapes include:
- `CreateThreadpoolWait` + `SetThreadpoolWait` on one event/process/thread/waitable-timer handle
- `RegisterWaitForSingleObject` based service/worker control paths
- watchdog or state-transition flows where a signal or timeout triggers one callback-owned branch
- mixed async systems where registered waits, timers, and IOCP all coexist and queue-family ownership is easy to confuse

Do **not** use this as the primary note when:
- the broad async path is still unclear and generic callback registration is the better first stop
- the case is more honestly timer-shaped (use the timer queue / threadpool timer note)
- the real remaining bottleneck is IOCP packet dequeue or APC alertable delivery rather than wait-object signaling

## 3. Core claim
In wait-shaped native work, **wait registration is weaker than signaled-or-timeout truth**, and signaled/timeout truth is weaker than proving the first callback-owned consumer that changes behavior.

The practical move is to separate:
- wait registration
- signal-or-timeout truth
- callback queue/delivery truth
- first consequence-bearing wait consumer
- proof-of-effect

The wrong question is often:

```text
Where is CreateThreadpoolWait / RegisterWaitForSingleObject called?
```

The better question is:

```text
Which registered wait actually becomes active because of one signal or timeout,
and which first callback-owned consumer changes later behavior?
```

## 4. Boundary objects to mark explicitly
### A. Wait-registration truth
This is where the target creates or registers one wait object.
Typical anchors include:
- `CreateThreadpoolWait`
- `SetThreadpoolWait`
- `RegisterWaitForSingleObject`

What to capture here:
- one wait object identity
- one callback pointer + context value
- one target handle family
- one timeout posture

### B. Signal-or-timeout truth
This is where callback eligibility becomes real.
Typical anchors include:
- the target handle reaching signaled state
- the configured timeout expiring
- one explicit re-registration step

What to capture here:
- whether the callback was driven by signal or timeout
- whether the same wait had to be re-registered before the next signal mattered
- whether the object remains signaled in a way that can cause repeated callbacks

### C. Callback-queued/delivered truth
A registered wait can exist without the callback yet being the one that matters.
Do not flatten registration or signal visibility into actual callback-owned behavior.

### D. Consequence-bearing consumer truth
This is the first callback body or immediate downstream consumer that changes later behavior.
Typical anchors include:
- one state write or mode change
- one retry/backoff/teardown decision
- one follow-on enqueue or emitter
- one later-visible service/protocol/UI effect

### E. Proof-of-effect truth
This is where the analyst proves the chosen wait callback matters.

## 5. Default workflow
### Step 1: choose one wait family, not every registered wait
Do not start by cataloging every signaled object.
Pick one wait object with:
- a visible late effect
- a stable callback/context tuple
- the clearest signal-or-timeout story

### Step 2: separate registration from activation
Write the local chain explicitly:
- wait registration
- signal/timeout truth
- callback queue/delivery
- consequence-bearing consumer
- effect

This prevents the classic mistake of treating registration as if it already explains behavior.

### Step 3: freeze the signal-vs-timeout story
From Microsoft docs:
- `SetThreadpoolWait` causes a worker thread callback after the handle becomes signaled **or** after timeout expires
- if `h` is NULL, the wait object ceases to queue new callbacks, but already queued callbacks can still occur
- `RegisterWaitForSingleObject` queues the callback when the object is signaled **or** timeout elapses

Practical stop rules:
- do not overread “callback ran” until you know whether signal or timeout owned it
- do not overread “wait unset/cancelled” as proof that no callback was already queued

### Step 4: preserve re-registration truth
Microsoft documents that you must re-register the event with the wait object before signaling it each time to trigger the wait callback.

Operator consequence:
- repeated signal folklore is weaker than one proved re-registration + signal path
- if the object remains signaled, callback repetition semantics depend on wait style and flags; do not assume one clean linear callback chain

### Step 5: prove one consequence-bearing wait consumer
Among candidate callbacks, prefer the one that:
- predicts later behavior better than registration alone
- distinguishes signal handling from timeout handling
- turns “registered wait exists” into one trustworthy subsystem map

### Step 6: use one narrow runtime move
Typical minimal proofs include:
- breakpoint/log on the wait callback plus the immediate downstream state write
- compare run that forces timeout versus actual signal while watching one later effect
- watchpoint on one object/state updated only after the wait callback fires

The aim is not maximum wait tracing.
It is one proof that links a registered wait to a behavior-changing consumer.

## 6. Practical stop rules this note preserves
- `registered wait exists != object actually signaled in the relevant run`
- `object signaled != callback queued/delivered in the way that matters`
- `wait unset/cancelled != no callback already queued`
- `same handle still signaled != repeated callbacks are automatically explained without re-registration/flag truth`

## 7. Sources
See: `sources/native/2026-04-04-native-wait-object-threadpool-wait-notes.md`

Primary references:
- https://learn.microsoft.com/en-us/windows/win32/api/threadpoolapiset/nf-threadpoolapiset-createthreadpoolwait
- https://learn.microsoft.com/en-us/windows/win32/api/threadpoolapiset/nf-threadpoolapiset-setthreadpoolwait
- https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-registerwaitforsingleobject
