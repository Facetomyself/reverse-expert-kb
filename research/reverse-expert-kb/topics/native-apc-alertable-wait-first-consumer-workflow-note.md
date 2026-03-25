# Native APC / Alertable-Wait First-Consumer Workflow Note

Topic class: workflow note
Ontology layers: workflow/sensemaking, runtime-evidence bridge, native baseline practical branch
Maturity: emerging
Related pages:
- topics/native-binary-reversing-baseline.md
- topics/native-practical-subtree-guide.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md
- topics/causal-write-and-reverse-causality-localization-workflow-note.md
- topics/runtime-behavior-recovery.md
- sources/native/2026-03-26-apc-alertable-wait-notes.md

## 1. What this workflow note is for
This note covers a recurring Windows-native async case where broad callback/event-loop ownership is already understood well enough, but the remaining bottleneck is narrower:
- `QueueUserAPC`, `NtQueueApcThread`, `NtTestAlert`, `SleepEx`, `WaitFor*Ex`, `ReadFileEx`, `WriteFileEx`, timer-completion APCs, or equivalent APC-adjacent surfaces are visible
- static reading shows that work is being queued to a thread, but not which queued APC first becomes behaviorally real
- the analyst keeps overreading queue sites, injection folklore, or API wrappers instead of proving the first alertable-delivery consumer that actually changes later behavior

The goal is to move from:

```text
one or more visible APC queue sites and plausible callback targets
```

to:

```text
one proved chain from APC production
through alertable-delivery truth
into one first consequence-bearing APC consumer
and one downstream effect
```

This note is for cases that are still fundamentally native-baseline shaped, but where ownership now breaks specifically at the **APC queued-vs-delivered boundary**.

## 2. When to use this note
Use this note when most of the following are true:
- one route, module owner, service worker, or broad callback family is already plausible enough that generic async ownership is no longer the main bottleneck
- the target visibly uses APC-backed delivery or APC-adjacent completion callbacks
- the main uncertainty is not "is there an APC?" but "which APC delivery actually matters first?"
- one narrow runtime proof against alertable wait, `NtTestAlert`, `KiUserApcDispatcher`, or the first callback-owned state edge would collapse a lot of uncertainty

Common shapes include:
- APC-backed async I/O completion via `ReadFileEx` / `WriteFileEx`
- timer or RPC-style completion callbacks that ultimately ride APC delivery
- work-queue designs that deliberately use one alertable waiter thread as a sequential callback consumer
- user-mode APC abuse or instrumentation cases where the analyst must separate queued possibility from actual delivery

Do **not** use this as the primary note when:
- the first trustworthy semantic anchor is still unstable
- the main uncertainty is still broad callback/event-loop reduction rather than APC-specific delivery
- the case has already narrowed more specifically into IOCP/thread-pool dequeue ownership
- the real remaining bottleneck is WoW64 routine encoding, special user APC internals, or kernel APC internals rather than ordinary user-mode first-consumer proof

## 3. Core claim
In APC-shaped native work, **queue visibility is weaker than delivery truth**.

The practical move is to separate:
- APC production or queue request
- delivery precondition truth
- dispatch boundary into user mode
- first consequence-bearing APC consumer
- proof-of-effect

The wrong question is often:

```text
Where is QueueUserAPC / NtQueueApcThread called?
```

The better question is:

```text
Which queued APC is actually delivered under one truthful alertable boundary,
and which first callback-owned consumer changes later behavior?
```

## 4. The five boundaries to mark explicitly

### A. APC production boundary
This is where APC work becomes eligible to execute later.
Typical anchors include:
- `QueueUserAPC`
- `NtQueueApcThread` / `NtQueueApcThreadEx`
- `ReadFileEx` / `WriteFileEx` / APC-backed timer completion APIs
- internal wrappers that recover a target thread handle and callback/context tuple

What to capture here:
- which thread is the intended delivery owner
- which routine/context value remains stable enough to anchor later proof
- whether the queued object is really ordinary user APC delivery versus some narrower special-user or WoW64 case

### B. Delivery-precondition boundary
This is where queued possibility becomes executable reality.
Typical anchors include:
- `SleepEx(..., TRUE)`
- `WaitForSingleObjectEx(..., TRUE)` / `WaitForMultipleObjectsEx(..., TRUE)`
- `MsgWaitForMultipleObjectsEx(..., MWMO_ALERTABLE)`
- `NtTestAlert`

What to capture here:
- which exact thread actually enters alertable state
- whether the relevant APC is delivered because of an alertable wait or an explicit `NtTestAlert`
- whether the case is stalling simply because the target thread never becomes alertable

### C. User-dispatch boundary
This is where the kernel-side queued APC becomes one user-mode callback delivery.
Typical anchors include:
- `KiUserApcDispatcher`
- nearby user-mode dispatch trampolines
- WoW64 APC wrappers when a 32-bit target is involved

What to capture here:
- which routine pointer is actually about to execute in user mode
- whether wrapper/trampoline code is only ABI plumbing or already rewrites ownership
- whether multiple pending APCs are being drained in sequence, so queue order alone is weaker than the actual first consequence-bearing callback

### D. Consequence-bearing consumer boundary
This is the first callback body or immediate downstream consumer that changes later behavior.
Typical anchors include:
- one state write or mode transition
- one request/session-object update
- one next-stage enqueue or retry/backoff decision
- one UI/service/protocol effect
- one error/degrade/cleanup branch that only happens after APC delivery

What to capture here:
- the narrowest consumer that predicts later behavior better than the queue site or dispatch trampoline alone

### E. Proof-of-effect boundary
This is where the analyst proves the chosen APC consumer matters.
Typical anchors include:
- one visible output, reply, log family, or UI change
- one later state difference in a compare run
- one follow-on queue insertion or durable object update
- one absence-of-effect that disappears when alertable delivery is suppressed or forced

What to capture here:
- one concrete downstream effect linked back to one delivered APC family

## 5. Default workflow

### Step 1: choose one APC family, not every queue site
Do not start by cataloging every APC queue request.
Choose one APC family with:
- a visible late effect
- a stable target-thread story
- one believable callback/context tuple
- the cleanest alertable-delivery proof opportunity

### Step 2: separate queue truth from delivery truth immediately
Write the local chain as:
- APC production
- delivery precondition
- user dispatch
- consequence-bearing consumer
- effect

This prevents the classic mistake of treating `QueueUserAPC` visibility as if it already explains behavior.

### Step 3: prove alertable-delivery realism
The first real reduction is usually not the queue API.
It is the moment the target thread becomes able to drain pending APCs.

Practical stop rules from the source set:
- if the target thread never enters an alertable wait, ordinary user APCs may never execute at all
- `NtTestAlert` is a narrower explicit drain boundary and may be cheaper to prove than broad wait-loop tracing
- if you only proved that an APC was queued to another process/thread, do not overread that as delivery; Microsoft explicitly warns cross-process APC use is fragile because of address-space, rebasing, and cross-bitness issues
- if the case is WoW64-shaped, do not flatten the dispatch boundary into an ordinary same-bitness callback story without checking routine-encoding / wrapper behavior

### Step 4: treat `KiUserApcDispatcher` as a reduction boundary, not necessarily the owner
`KiUserApcDispatcher` often proves that user-mode APC delivery is real.
But it is usually not the final behavior owner.

Prefer the first callback body or one immediate downstream consumer that:
- mutates durable or semi-durable state
- selects success/failure/retry behavior
- emits a visible effect
- moves ownership into a more specific object or stage

### Step 5: prove one consequence-bearing consumer
Among candidate APC callbacks, prefer the one that:
- predicts later behavior better than the queue call alone
- distinguishes callback plumbing from callback-owned consequence
- turns a vague "APC is involved" claim into one trustworthy subsystem map

### Step 6: use one narrow runtime move
Typical minimal proofs include:
- breakpoint/log on the alertable wait site plus one delivered callback pointer
- breakpoint on `NtTestAlert` or `KiUserApcDispatcher` plus immediate callback target recovery
- watchpoint on one request/session/UI field written by the APC callback
- compare run that toggles whether the target thread becomes alertable while observing one downstream effect

The aim is **not** maximal APC tracing.
It is one proof that links a delivered APC to a behavior-changing consumer.

### Step 7: rewrite the subsystem map after proof
Once proved, rewrite the working model as:

```text
APC production -> alertable-delivery truth -> user dispatch -> consequence-bearing consumer -> effect
```

Only then broaden into sibling APC families, neighboring waits, or adjacent async mechanisms.

## 6. Common scenario patterns

### Pattern 1: APC-backed async I/O completion
Symptoms:
- `ReadFileEx` / `WriteFileEx` or equivalent APIs are visible
- the callback looks straightforward, but completion behavior remains flaky or hard to localize
- static reading keeps stopping at the I/O issuance site

Best move:
- treat I/O issuance as production, not final ownership
- prove which thread must enter alertable wait
- localize the first callback body that mutates request/session state or emits the visible effect

### Pattern 2: Deliberate alertable-wait work queue
Symptoms:
- one thread loops in `SleepEx` / `WaitForSingleObjectEx(..., TRUE)`
- clients enqueue callbacks via APCs
- the queue design is obvious, but the first effect-bearing callback still is not

Best move:
- treat the wait loop as delivery infrastructure only
- identify the callback/context value that first predicts later behavior
- prove one consumer that writes durable state or triggers one visible downstream action

### Pattern 3: Injection / instrumentation folklore overread
Symptoms:
- `QueueUserAPC` or `NtQueueApcThread` is visible and everyone assumes execution happened
- the target thread’s real alertable behavior is unclear
- later effects look inconsistent

Best move:
- stop widening injection folklore
- prove whether the target thread actually becomes alertable
- separate queued possibility from delivered callback truth before claiming ownership

### Pattern 4: WoW64 or wrapper-heavy APC delivery
Symptoms:
- APC delivery is visible, but routine identity or argument ownership is muddy
- a wrapper or encoding layer may be rewriting the callback boundary

Best move:
- treat dispatch wrappers as ABI or compatibility boundaries first
- freeze the actual user-mode callback target that owns the later effect
- only then widen into routine encoding or deeper APC internals if they still matter

## 7. Practical source-backed reminders
- Microsoft Learn confirms ordinary user APCs execute when the target thread performs an alertable wait and that pending APCs are drained in FIFO order once alertable delivery occurs.
- Microsoft Learn also warns against queueing APCs to threads outside the caller’s process because rebasing, cross-bitness, and other factors make that weaker than it looks.
- NtDoc is useful for a compact Native API reminder: `NtQueueApcThread` exposes three callback arguments and `NtTestAlert` can be the manual drain boundary.
- repnz’s APC series is especially useful for workflow shape: separate queue request, alertable-unwait logic, and user dispatch, then avoid stopping at `KiUserApcDispatcher` when the real owner lives one callback later.
- Pavel Yosifovich’s APC writeup is useful as a practical reminder that APCs can form a natural work queue, but the elegant queue shape is still weaker than one proved consequence-bearing consumer.

## 8. Practical handoff rule
Leave this note as soon as the main uncertainty stops being APC delivery ownership and becomes one narrower follow-on proof task.

The most common handoffs are:
- move to `topics/causal-write-and-reverse-causality-localization-workflow-note.md` when one APC consumer is already good enough and the next bottleneck is the first causal write or reducer behind a later effect
- move back up to `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md` if the case turned out not to be APC-specific after all
- move to `topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md` if the real ownership boundary is actually IOCP or thread-pool delivery rather than APC alertable delivery
- move to `topics/runtime-behavior-recovery.md` when the remaining problem is broader evidence strategy rather than APC ownership itself

## 9. Failure modes this note helps prevent
- treating queue visibility as delivery proof
- assuming cross-process APC queueing means real execution happened
- stopping at `KiUserApcDispatcher` instead of the first callback-owned consequence
- overreading injection folklore when the thread may never become alertable
- broadening into all APC trivia instead of proving one behavior-changing consumer

## 10. Compact operator checklist
- Pick one APC family, not every queue site.
- Separate queue truth from alertable-delivery truth.
- Prove which thread actually drains the APC.
- Treat `KiUserApcDispatcher` as a reduction boundary, not automatically the owner.
- Prefer the first callback that changes state or emits one visible effect.
- Use one narrow runtime proof, not maximal APC tracing.

## 11. Topic summary
In Windows-native APC-shaped cases, the decisive practical split is not just between "APC exists" and "APC does not exist."
It is between **queued possibility** and **truthful alertable delivery**, and then between generic dispatch visibility and the first callback-owned consequence.

The practical cure is to choose one APC family, prove one alertable-delivery boundary, localize one first consequence-bearing callback consumer, and tie it to one downstream effect.
That turns APC folklore into a smaller trustworthy behavioral map.
