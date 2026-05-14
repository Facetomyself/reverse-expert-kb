# iOS AsyncStream Yield, Buffering, Consumption, and Termination Workflow Note

Topic class: concrete workflow note
Ontology layers: mobile practical workflow, iOS runtime branch, Swift-concurrency stream consequence bridge
Maturity: practical
Related pages:
- topics/ios-practical-subtree-guide.md
- topics/ios-swift-concurrency-continuation-to-policy-workflow-note.md
- topics/ios-result-callback-to-policy-state-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md
- topics/ios-mitigation-aware-replay-repair-workflow-note.md
- topics/mobile-reversing-and-runtime-instrumentation.md

Related source notes:
- sources/ios/2026-04-08-asyncstream-yield-vs-consumer-notes.md
- sources/ios/2026-05-15-asyncstream-yield-buffer-consume-termination-notes.md

## 1. When to use this note
Use this note when a modern iOS case already exposes a truthful Swift `AsyncStream` / `AsyncThrowingStream` path, but the first stream-owned consequence boundary is still unclear.

Typical entry conditions:
- the case is already clearly iOS-shaped and reachable enough to study
- callback/block landing work is already good enough, or a Swift async path is already plausible enough, that broad owner search should stop
- visible result material moves through `AsyncStream`, `AsyncThrowingStream`, `AsyncSequence`, `Task`, or similar Swift-owned machinery
- the current bottleneck is no longer “is this callback real?” but “where does yielded material first become one durable consumer-side consequence?”
- the analyst can already name one likely producer family, yet still cannot prove which iterator-side / task-side / MainActor-side reducer actually changes behavior

Use it for cases like:
- a delegate or callback already looks truthful, but the meaningful behavior now seems owned by `AsyncStream` buffering and the first iterator-side consumer
- a Swift stream appears to carry all the important values, but the question is still whether `yield(...)` actually enqueued anything or whether termination cut the path earlier
- replay is good enough to produce visible stream activity, but it is still unclear where task-owned logic turns that activity into allow / retry / challenge / degrade behavior

Do **not** use this note when:
- traffic topology, environment normalization, or broad packaging/jailbreak/runtime-gate drift still dominate
- the callback/block landing itself is still too ambiguous to trust
- the remaining gap is already clearly one narrower runtime-table, initialized-image, or object-materialization obligation
- the case is already simple enough that the ordinary result-to-policy note can prove the first consumer without preserving stream ownership explicitly

In those cases, route to the broader or narrower page first.

## 2. Core claim
Once an iOS case has already frozen one truthful stream-producing family or one plausible imported-async owner path, the next best move is often **not** broader callback hunting and **not** immediate high-level policy interpretation.
It is to prove the first **stream-owned consequence boundary**.

The central question is usually:

```text
Where does yielded stream material first resume into Swift-owned control flow,
and which first iterator-side / task-side / MainActor-side consumer
there actually predicts later app behavior?
```

A practical stop rule worth keeping explicit is:
- once callback truth is already good enough, do not reopen broad owner search by default
- instead, try to freeze one five-part proof object:
  - one already-frozen stream-producing family or imported-async owner path
  - one buffering / enqueue boundary
  - one iterator-side consumption boundary
  - one termination / cancellation boundary if relevant
  - one first behavior-changing consumer or downstream effect

Until that is proved, modern iOS analysis often stalls in three kinds of confusion:
- imported async surfaces that look like final ownership but still only wrap older completion machinery
- truthful stream producers whose real consequence only appears after buffering and iterator-side resumption
- readable Swift wrappers that normalize results nicely but still do not own the first behavior-changing decision

## 3. The five boundaries to separate explicitly

### A. Producer truth vs buffering acceptance
A visible `yield(...)` call is not the same thing as accepted buffering.

What to separate:
- the stream-producing site
- the `yield(...)` attempt
- the buffering policy / acceptance result
- whether the value was accepted, dropped, or rejected because the stream was already terminal

Useful reminder:
- Apple’s `AsyncStream.Continuation.YieldResult` and buffering-policy surfaces are a real proof boundary, not decoration
- producer traffic is weaker than proving the stream actually accepted the element

### B. Buffering acceptance vs iterator-side consumption
Even accepted buffering is not yet proof that the consumer used the value.

What to separate:
- `yield(...)` visibility
- enqueue / buffering acceptance
- iterator-side `next()` / `for await` / resumed task consumption
- later reducer or consumer logic

Useful reminder:
- do not narrate `yield(...)` visibility as equivalent to first behavior-changing ownership
- a stream can accept a value without the app-side consumer yet doing anything meaningful with it

### C. Consumption vs termination
End-state is not the same thing as consequence.

What to separate:
- first iterator-side use
- explicit `finish()` / termination / cancellation
- later policy or UI effect

Useful reminder:
- do not collapse finish/cancellation into later UI/policy behavior
- keep stream mechanics separate from MainActor-owned or policy-bearing effect

### D. Termination vs durable effect
Seeing stream end-state is still weaker than proving later state change.

What to separate:
- termination or cancellation truth
- first durable consumer-side state change
- one later visible effect

Useful reminder:
- termination is lifecycle truth, not by itself durable consequence

### E. Stream-side truth vs continuation discipline
Some cases still involve continuation wrappers around the stream or around related async bridges.

What to separate:
- continuation creation/storage
- actual resume or delivery
- missing-resume leak/suspend
- double-resume misuse
- first stream-side consumer

Useful reminder:
- exact-once continuation discipline is a real operator boundary and should not be flattened into vague async drift

## 4. Default workflow

### Step 1: freeze one representative stream-shaped flow
Pick one flow only.
Examples:
- callback/delegate -> `AsyncStream` yield -> iterator-side consumer -> policy change
- imported async path -> buffering acceptance -> stream consumption -> next request family
- delegate -> `AsyncThrowingStream` delivery -> task consumer -> challenge/retry state

Avoid mixing several tasks, streams, or callback families.

### Step 2: draft one stream-owned consequence chain
Write a compact draft before deeper tracing:

```text
stream-producing family:
  callback / delegate / async wrapper / producer

candidate buffer boundary:
  yield attempt / buffering policy / enqueue result

candidate iterator-side boundary:
  next() / for await / resumed task consumption

candidate termination boundary:
  finish / cancellation / end-state

candidate first consumer:
  coordinator / controller / task body / MainActor state write

visible effect:
  allow / retry / challenge / degrade / block / follow-up request
```

This draft may be wrong.
Its purpose is to stop uncontrolled async wrapper accumulation.

### Step 3: prove whether producer truth is already good enough
Before going deeper into buffering or consumption, answer:
- is the producing family already frozen strongly enough?
- is the stream surface clearly tied to that family, or is that still speculative?
- would stronger producer proof change the meaning of everything downstream?

If not settled, route back first.

### Step 4: choose the first truthful buffer or consumption boundary
Good candidates include:
- the exact `yield(...)` result edge
- the first enqueue/acceptance event that wakes the relevant consumer
- the first `for await` / iterator-consumption edge that turns delivery into app-owned reduction
- the narrowest boundary where result material becomes available to app-owned Swift logic

Bad default choices include:
- the highest-level public async method name with no proof of downstream consequence
- every task/wrapper near the flow
- every helper that only creates or stores the stream without owning delivery
- treating stream construction as equivalent to consumer ownership

### Step 5: separate normalization from policy mapping
Use small role labels:
- **yield** — producer attempts to supply a value
- **enqueue** — buffering policy accepts or rejects the value
- **consume** — one iterator-side or resumed task-side consumer uses the value
- **terminate** — finish/cancellation/end-state becomes true
- **effect** — one later consumer or state write changes behavior

This prevents a common error:
- mistaking a visible producer call or end-state for the actual behavior-changing decision

### Step 6: stop at the first durable consumer-side consequence
The continuation succeeds when you can rewrite the request as:

```text
stream producer
  -> enqueue/buffering result
  -> iterator-side consumption
  -> termination/cancellation if relevant
  -> one durable consumer-side consequence
```

If the stream is already stable and the remaining gap is now the first app-local policy consumer, hand off downstream instead of staying in stream mechanics.

## 5. Practical scenario patterns

### Pattern A: visible yield, unknown acceptance
If `yield(...)` is visible but the consumer still looks weak:
- check the `YieldResult` / buffering-policy result first
- do not jump directly to later policy meaning
- ask whether the stream was already terminal or whether the element was accepted but not yet consumed

### Pattern B: accepted buffering, unknown consumer
If buffering acceptance is visible but the consumer still looks weak:
- freeze the first iterator-side `next()` / `for await` consumer
- separate wakeup/availability from actual behavior change
- keep later policy or UI state distinct

### Pattern C: termination visible, effect still unclear
If `finish()` / cancellation is visible but the effect is still unclear:
- treat termination as lifecycle truth only
- prove which consumer actually owned the last meaningful effect
- do not overread termination as durable behavior by itself

### Pattern D: continuation wrapper around the stream
If the stream is wrapped in a continuation bridge:
- keep continuation creation/storage separate from actual delivery
- preserve exact-once continuation discipline if relevant
- do not call a stream consumer proved until one resumed or delivered element actually reaches a downstream reducer

## 6. Stop rules worth preserving
A compact stream-shaped stop rule is:

```text
yielded != enqueued != consumed != terminated != durable-effect
```

That is the compact ladder for this seam and should stay visible during compare runs.

A few other useful reminders:
- producer-side `yield(...)` traffic is weaker than proving the app-side consumer actually used the value
- buffering acceptance is weaker than later iterator-side consumption
- termination is weaker than durable effect
- exact-once continuation discipline still matters if a stream is bridged from a continuation wrapper
- for UI-bound cases, preserve one extra split between resumed task-side consumer truth and the first `@MainActor`-isolated state write / route selection / coordinator handoff

## 7. What this note is not
This note is not a broad Swift async-stream theory page.
It is a practical stream-owned consequence boundary for iOS analysis.

Do not let it absorb unrelated owner-localization work, trust-path work, or generic runtime-gate repair.
