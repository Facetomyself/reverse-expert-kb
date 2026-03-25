# Native Completion-Port and Thread-Pool First-Consumer Workflow Note

Topic class: workflow note
Ontology layers: workflow/sensemaking, runtime-evidence bridge, native baseline practical branch
Maturity: emerging
Related pages:
- topics/native-binary-reversing-baseline.md
- topics/native-practical-subtree-guide.md
- topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/causal-write-and-reverse-causality-localization-workflow-note.md
- topics/runtime-behavior-recovery.md
- sources/native/2026-03-25-native-completion-port-stop-rules-notes.md

## 1. What this workflow note is for
This note covers a recurring native case where the analyst has already reduced a target into an async worker or completion-driven shape, but the remaining uncertainty is narrower than the broad callback/event-loop note.

Typical symptoms:
- service, daemon, network, or filesystem code is readable enough to follow
- `CreateThreadpool*`, `SubmitThreadpoolWork`, `CreateThreadpoolIo`, `StartThreadpoolIo`, IOCP, overlapped I/O, worker-factory, libuv worker, or equivalent queue helpers are visible
- direct caller/callee reading stops being trustworthy once work is posted or completions are dequeued
- many callbacks or work-item wrappers look plausible, but the first consequence-bearing consumer is still unclear

The goal is to move from:

```text
visible posted work, completions, queue objects, and callback wrappers
```

to:

```text
one proved chain from enqueue or completion delivery
through one scheduler/dequeue reduction
into one callback body or helper-owned consumer
that actually changes later behavior
```

This note is for cases that are still fundamentally native-baseline shaped, but where behavioral ownership now lives at the **completion-packet / work-item / worker-thread handoff boundary**.

## 2. When to use this note
Use this note when most of the following are true:
- one route, one loaded owner, or one service-owned worker path is already plausible enough that broad route selection is no longer the main bottleneck
- the target uses completion ports, thread pools, posted work items, futures/promises backed by worker queues, or equivalent completion-driven delivery
- the main uncertainty is no longer “which broad subsystem?” but “which dequeued packet or work callback first becomes behaviorally real?”
- one narrow runtime proof against a dequeue helper, callback wrapper, or follow-on state write would collapse a lot of uncertainty

Common concrete shapes include:
- Windows IOCP consumers built around `GetQueuedCompletionStatus` or thread-pool I/O callbacks
- Windows user-mode thread-pool work, wait, timer, or I/O helpers where helper wrappers obscure the real callback owner
- service/daemon worker loops that post control, I/O, or retry work into one shared queue
- libuv-style worker completion paths where background work completes on a worker thread but the real consequence appears only after a loop-thread async handoff

Do **not** use this as the primary note when:
- the first trustworthy semantic anchor is still unstable
- the broad service-owned worker path is still unclear and `topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md` is the better first stop
- the target is better framed as generic callback/event-loop reduction without strong queue/completion ownership
- the remaining uncertainty is specifically GUI message/subclass or Qt signal-slot ownership, where `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md` is the thinner continuation

## 3. Core claim
Completion-driven native targets are easy to misread because visible callback registration and queue plumbing do **not** by themselves identify the first consumer that matters.

The practical move is to separate:
- enqueue or completion production
- scheduler / dequeue reduction
- callback wrapper or helper trampoline
- first consequence-bearing callback body or downstream consumer
- proof-of-effect

In many real cases, the analyst should stop asking:

```text
Where are all the possible callbacks?
```

and instead ask:

```text
Which dequeued packet, work item, or helper-owned callback first predicts
one state write, one ownership transfer, one reply family, or one next-stage enqueue?
```

## 4. The five boundaries to mark explicitly

### A. Work-production boundary
This is where the relevant async work becomes eligible to run.
Typical anchors include:
- `SubmitThreadpoolWork`, `TrySubmitThreadpoolCallback`, `CreateThreadpoolIo` + `StartThreadpoolIo`
- `PostQueuedCompletionStatus`
- overlapped I/O issuance with an `OVERLAPPED` and associated completion object
- worker-queue push helpers, task/future completion, or queue insertion wrappers
- libuv work submission or async-send helpers

What to capture here:
- which enqueue/completion family matters for the target question
- which packet key, callback pointer, context pointer, or task object survives long enough to anchor later proof

### B. Queue / port / scheduler boundary
This is where eligible work becomes one delivered item rather than a family of possibilities.
Typical anchors include:
- `GetQueuedCompletionStatus` or wrapper loops around it
- thread-pool internal dequeue wrappers
- worker-factory or queue-pop helpers
- worker-pool dequeue plus callback-pointer extraction
- libuv worker-complete queue handoff back into the event loop

What to capture here:
- the first reduction from many possible work items to one delivered item
- the fields that distinguish ownership at dequeue time: completion key, `OVERLAPPED*`, task node, callback slot, context pointer, object pointer, queue family
- for IOCP specifically, keep `completion key` and `OVERLAPPED*` conceptually separate: the key often identifies the handle or queue family, while `OVERLAPPED*` often leads back to the concrete request/session owner embedded around it

### C. Helper-wrapper boundary
This is where frameworks often hide the real callback behind one shared trampoline.
Typical anchors include:
- thread-pool helper callbacks that unpack a work structure before invoking the real routine
- completion wrappers that recover object/context from `OVERLAPPED`
- generic queue worker helpers that switch on task kind before dispatch
- libuv completion adapters that move worker results into pending callbacks on the loop thread

What to capture here:
- which fields are only framework plumbing
- which field or recovered object actually selects the real consumer
- whether the wrapper itself mutates behavior or only forwards control

### D. Consequence-bearing consumer boundary
This is the first callback body or downstream consumer that changes later behavior.
Typical anchors include:
- one state write or mode transition
- one retry/backoff decision
- one ownership transfer into a session/request object
- one next-stage enqueue that is more specific than the shared queue family
- one reply/emit/log/error family selection

What to capture here:
- the narrowest consumer that predicts later behavior better than the wrapper or queue helper alone

### E. Proof-of-effect boundary
This is where the analyst proves the chosen consumer matters.
Typical anchors include:
- one visible output, reply, IPC emission, or network write
- one later state difference in a compare run
- one follow-on task enqueue or queue-family switch
- one crash/guard/log family difference caused by suppressing or forcing the consumer

What to capture here:
- one concrete downstream effect linked back to one dequeued work item or completion family

## 5. Default workflow

### Step 1: pick one queue family, not the whole scheduler
Do not start by cataloging every callback supported by the thread pool or every possible completion consumer.
Choose one queue family with:
- a visible late effect
- a stable context carrier (`OVERLAPPED*`, completion key, task node, request object, work item pointer)
- the smallest number of competing wrapper layers

### Step 2: separate production from delivery
Write the local chain explicitly as:
- work production / async issuance
- queue or completion-port reduction
- helper wrapper / trampoline
- consequence-bearing consumer
- effect

This prevents a common mistake: treating queue submission or registration as if it already proved behavioral ownership.

### Step 3: localize the first dequeue reduction
Find the first place where the runtime turns queued possibility into one delivered work item.
Usually this is one of:
- `GetQueuedCompletionStatus` returning one completion packet
- one thread-pool dequeue helper recovering one callback object
- one worker queue pop retrieving one task node
- one worker-complete path promoting one finished request into one loop-thread callback family

For IOCP-shaped cases, preserve one narrower stop rule immediately:
- treat **completion key** and **`OVERLAPPED*`** as different ownership carriers
- the completion key often reduces the queue family or handle family
- the `OVERLAPPED*` often leads back to the concrete embedded request/session owner
- do not stop at “this worker dequeued the packet” until one of those carriers predicts one later state edge, retry/degrade branch, or emitted reply more truthfully than queue chronology alone

If you cannot identify this reduction, you are probably still reading queue setup rather than behavior.

### Step 4: unwrap the shared helper layer
Many completion-driven systems execute a shared wrapper before the real callback.
Your job is to decide whether the wrapper:
- only unpacks context and forwards control
- or already chooses one branch/task kind that meaningfully changes later behavior

Prefer the first point where callback identity becomes specific enough to predict a later effect.
Do **not** stop at a pretty helper name if the real ownership lives one field dereference later.

### Step 5: prove one consequence-bearing consumer
Among candidate consumers, prefer the one that:
- writes durable or semi-durable state
- selects success/failure/retry policy
- moves a request/session object into a more specific stage
- emits one observable reply or command
- enqueues one narrower downstream task family

### Step 6: use one narrow runtime move
Typical minimal proofs include:
- breakpoint/log on one dequeue helper and the first downstream callback pointer/context extraction
- watchpoint on one request/session field written by the chosen consumer
- compare run that toggles one completion-producing event while observing one next-stage enqueue
- hook/log on one follow-on emitter or queue insertion that only occurs after the chosen callback

The aim is **not** maximum queue tracing.
It is one proof that links a delivered work item to a behavior-changing consumer.

### Step 7: rewrite the subsystem map after proof
Once proved, rewrite the working model as:

```text
work production -> dequeue reduction -> helper unwrap -> consequence-bearing consumer -> effect
```

Only then broaden to sibling callback families, different queue classes, or neighboring retry/timer paths.

## 6. Common scenario patterns

### Pattern 1: Windows IOCP worker loop
Symptoms:
- `CreateIoCompletionPort`, overlapped I/O, and one worker loop are visible
- many packet consumers look symmetrical
- the analyst knows completions matter, but not which consumer first changes request/session behavior

Best move:
- choose one completion-producing operation
- anchor on one `OVERLAPPED*` or completion key
- localize the first `GetQueuedCompletionStatus` consumer or wrapper that recovers the owning object
- prove one state transition, reply emission, or follow-on queue insertion from that consumer

Practical reminder from the source base:
- completion packets may be queued FIFO but waiting threads are released in LIFO order and actual processing depends on port concurrency and scheduler state, so do not over-trust naive “submit order == consumer order” assumptions
- not every dequeued packet is a true I/O completion: `PostQueuedCompletionStatus` can inject control packets that look similar at the worker loop level, and Microsoft explicitly notes the system does not validate the returned values and that `lpOverlapped` need not even point to a real `OVERLAPPED`, so first separate control-plane packets from I/O-owned packets before claiming behavioral ownership
- keep `completion key` family identity separate from `OVERLAPPED*` owner recovery: the key often narrows the queue/handle/control family, while the `OVERLAPPED*` often leads back to the concrete request/session owner embedded around it
- a FALSE return from `GetQueuedCompletionStatus` does not always mean “nothing happened”; if `lpOverlapped` is non-NULL, a failed I/O completion was still dequeued and may own retry/backoff/degrade behavior

### Pattern 2: Windows thread-pool work / I/O helper path
Symptoms:
- `TP_WORK`, `TP_IO`, wait/timer helpers, or thread-pool callback APIs are visible
- framework helper structures or wrappers obscure the real callback body
- the broad worker path is obvious, but the first effect-bearing consumer is not

Best move:
- separate API-level submission from internal helper-owned callback delivery
- identify the field/object that carries the real callback identity or request ownership
- prove the first callback body that changes policy, object lifecycle, or emitted behavior

Practical reminder:
- thread-pool helper wrappers often execute shared cleanup/unpack code before the real callback, so avoid stopping the analysis at the wrapper name alone
- for `TP_IO` specifically, do not flatten “I created a thread-pool I/O object” into “every overlapped success will produce the callback”: Microsoft’s `CreateThreadpoolIo` contract requires `StartThreadpoolIo`, and when the handle uses `FILE_SKIP_COMPLETION_PORT_ON_SUCCESS`, immediately successful overlapped I/O can skip the callback path and instead require `CancelThreadpoolIo`; if the callback never fires, verify this notification mode before claiming the consumer is dead or unrelated

### Pattern 3: Service queue with retry/timer/control packets
Symptoms:
- service command ingress is already understood
- a shared worker queue mixes control, retry, timeout, and I/O completion work
- several task kinds are visible but ownership remains vague

Best move:
- choose the queue family tied to the user-visible effect
- prove the first dequeue-time task-kind reduction
- follow only the first consumer that changes session/request state or selects reply/error behavior

### Pattern 4: libuv or equivalent worker-complete bridge
Symptoms:
- worker-thread code is readable
- background work completes, but the meaningful effect only happens after results are reintroduced to the loop thread
- broad async ownership is visible, but the crucial loop-thread consumer is still unclear

Best move:
- treat worker completion as production, not final ownership
- localize the handoff that moves finished work back into pending/async delivery
- in libuv specifically, remember the concrete split: `uv_queue_work()` stores `work_cb` and `after_work_cb`; worker threads run `work_cb`, then `uv__work_done()` / `uv__queue_done()` drive `after_work_cb` back on the loop thread
- prove the first loop-thread callback that mutates later behavior or emits a visible result
- if the visible symptom is absence of a later effect, inspect cancellation/error delivery in the loop-thread completion path before concluding the worker body is the decisive consumer
- preserve one extra stop rule here: do not flatten `uv_queue_work()` into a generic “background worker owns the outcome” claim. The worker-side `work_cb` and loop-thread `after_work_cb` are different ownership boundaries, and source-backed guidance indicates libuv internally synchronizes the work/done handoff while `uv_async_send()` does not automatically provide the same memory-order guarantee. If a result seems to vanish only at the loop-thread side, verify whether the real consumer is the `after_work_cb` boundary or an `uv_async_send()` continuation rather than reopening worker-body analysis

## 7. What this note adds to the native branch
The native branch previously had:
- broad service-owned worker reduction
- broad callback/event-loop consumer reduction
- one thinner GUI continuation

What it lacked was a concrete continuation for **completion-port / thread-pool / queue-dequeue ownership**, where the broad async note is true but still too wide.

This page fills that gap by making one narrower routing rule explicit:
- use `topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md` when the main uncertainty is still which service-owned worker path matters
- use `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md` when the target is broadly async and the delivery shape is not yet reduced
- use `topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md` when the async bottleneck has already narrowed specifically into posted work, completion packets, thread-pool callbacks, or queue-dequeue ownership

A compact continuation rule is:
- do not enter this note just because the target has threads or callbacks
- enter it when one service/worker or async path is already plausible and the next truthful question is now “which delivered work item or completion callback first owns behavior?”

## 8. Practical handoff rule
Leave this note as soon as the main uncertainty stops being “which dequeued packet/work item/callback first changes behavior?” and becomes one narrower follow-on proof.

The most common next handoffs are:
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md` when one callback family is already good enough and the next bottleneck is the first state write, branch, or causal edge behind a later visible effect
- `topics/runtime-behavior-recovery.md` when the remaining gap is broader observability, replay-worthiness, or evidence strategy rather than queue ownership itself
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md` when the consumer is already known and the remaining gap has narrowed into one serializer/transport/output-side continuation

## 9. Failure modes this note helps prevent
- treating queue submission as if it already proved callback ownership
- over-trusting helper wrapper names and never proving the real callback body
- assuming completion delivery order from issue order in ways the scheduler does not guarantee
- failing to distinguish posted control packets from true I/O-owned completions in an IOCP worker loop
- treating all `GetQueuedCompletionStatus` failure returns as if no real completion was dequeued
- cataloging every thread-pool callback type before grounding one effect-bearing consumer
- confusing worker-thread completion with the later loop-thread consumer that actually changes behavior

## 10. Compact operator checklist
- Pick one queue/completion family, not the whole scheduler.
- Separate production, dequeue reduction, helper unwrap, consumer, and effect.
- Prefer the first effect-bearing callback over the prettiest shared wrapper.
- Use one narrow runtime proof, not maximal tracing.
- Rewrite the subsystem map only after one delivered work item is linked to one real consequence.

## 11. Topic summary
In completion-driven native reversing, the analyst often already knows that async work matters; the real bottleneck is proving which delivered packet, work item, or helper-owned callback first becomes behaviorally real.

The practical cure is to separate work production from dequeue, unwrap the shared helper layer, choose one consequence-bearing consumer, and prove one downstream effect. That turns a noisy queueing framework into a smaller, trustworthy working map.
