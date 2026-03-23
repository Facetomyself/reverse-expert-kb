# iOS Swift-Concurrency Continuation to Policy Workflow Note

Topic class: concrete workflow note
Ontology layers: mobile practical workflow, iOS runtime branch, Swift-concurrency continuation consequence bridge
Maturity: practical
Related pages:
- topics/ios-practical-subtree-guide.md
- topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md
- topics/ios-result-callback-to-policy-state-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md
- topics/ios-mitigation-aware-replay-repair-workflow-note.md
- topics/mobile-reversing-and-runtime-instrumentation.md

## 1. When to use this note
Use this note when a modern iOS case already exposes a truthful callback/delegate family or a plausible Swift `async` owner path, but the first **continuation-owned or stream-owned consequence boundary** is still unclear.

Typical entry conditions:
- the case is already clearly iOS-shaped and reachable enough to study
- callback/block landing work is already good enough, or a Swift `async` path is already plausible enough, that broad owner search should stop
- visible result material seems to move through `async`, `await`, `Task`, `CheckedContinuation`, `UnsafeContinuation`, `AsyncStream`, or similar Swift-owned machinery
- the current bottleneck is no longer “is this callback real?” but “where does resumed result material first become one durable app-local policy state?”
- the analyst can already name one likely completion/delegate family or imported-async owner, yet still cannot prove which Swift-side reducer / mapper / consumer actually changes behavior

Use it for cases like:
- an Objective-C completion path appears to import cleanly as a Swift `async throws` function, but the behavioral consequence only becomes visible after continuation resume
- a delegate or block already looks truthful, yet the app’s meaningful behavior now seems owned by `AsyncStream` buffering, task wakeup, or one Swift reducer after resume
- a Swift `Result`-like wrapper is visible, but the first decisive consumer lives after a continuation-owned state-machine hop rather than at the callback landing
- replay is good enough to produce visible async results, but it is still unclear where task-owned logic turns those results into allow / retry / challenge / degrade behavior

Do **not** use this note when:
- traffic topology, environment normalization, or broad packaging/jailbreak/runtime-gate drift still dominate
- the callback/block landing itself is still too ambiguous to trust
- the remaining gap is already clearly one narrower runtime-table, initialized-image, or object-materialization obligation
- the case is already simple enough that the ordinary result-to-policy note can prove the first consumer without preserving continuation ownership explicitly

In those cases, route to the broader or narrower page first.

## 2. Core claim
Once a modern iOS case has already frozen one truthful callback/delegate family or one plausible imported-async owner path, the next best move is often **not** broader callback hunting and **not** immediate high-level policy interpretation.
It is to prove the first **continuation-owned consequence boundary**.

The central question is usually:

```text
Where does callback- or async-visible result material first resume into
Swift-owned task/continuation logic, and which first reducer / consumer
there actually predicts later app behavior?
```

A practical stop rule worth keeping explicit is:
- once callback truth is already good enough, do not reopen broad owner search by default
- instead, try to freeze one four-part proof object:
  - one already-frozen callback/delegate/completion family or imported-async owner path
  - one continuation resume / stream delivery / task wakeup boundary
  - one Swift-side normalization or policy-mapping reducer
  - one first behavior-changing consumer or downstream effect

Until that is proved, modern iOS analysis often stalls in three kinds of confusion:
- imported `async` surfaces that look like final ownership but still only wrap older completion machinery
- truthful callback landings whose real consequence only appears after Swift task/stream resumption
- readable Swift wrappers that normalize results nicely but still do not own the first behavior-changing decision

## 3. The four boundaries to separate explicitly

### A. Callback/delegate truth vs imported-async surface
A Swift `async` function being visible is not yet proof that the high-level async surface owns the consequence.
Sometimes it is only the imported face of an Objective-C completion API.

What to separate:
- the original completion/delegate family
- the imported or wrapped async entry point
- whether the callback truth itself is already settled strongly enough

Useful reminder:
- if callback truth is still doubtful, route back to callback/block landing work first
- if callback truth is already good enough, treat the async surface as a handoff candidate rather than automatic ownership

### B. Resume/delivery boundary vs surrounding wrappers
Continuation-owned logic usually has one narrower boundary where result material becomes active in Swift-owned control flow.

Typical forms:
- `withCheckedContinuation` / `withUnsafeContinuation` resume sites
- continuation wrappers around completion handlers
- `AsyncStream` buffering or yield-to-consumer wakeups
- `URLSession.AsyncBytes` or similar `AsyncSequence` delivery loops where header-time truth and body-consumption truth should not be collapsed
- task wakeup or state-machine resume points after `await`

What to separate:
- wrapper/setup code that only prepares the continuation
- the actual resume/delivery boundary
- whether the flow is really **single-shot continuation**, **multi-value stream**, or **sequence-consumption** shaped
- later reducers and consumers that matter behaviorally

Useful reminder:
- the first useful proof object is often not the prettiest async function name, but the first truthful resume/delivery edge
- a resume call is also not automatically the first behavior-changing consumer: Swift continuation material can be resumed first and only later rescheduled into the task/executor context where one reducer, mapper, or coordinator finally changes behavior
- do not flatten single-shot continuation cases, `AsyncStream` cases, and `AsyncSequence`/bytes-consumption cases into one generic “async callback” bucket, because their truthful stop rules differ

### C. Resume visibility vs policy reduction
Seeing result material after resume is still not the same thing as understanding app-local meaning.

What to separate:
- raw resumed payload or thrown error
- result normalization into an app-local enum/object family
- policy mapping into allow / retry / degrade / challenge / block buckets

Useful reminder:
- continuation-owned code often looks cleaner than callback code, which makes it easy to overread the first visible Swift object as final meaning

### D. Reducer/mapper visibility vs first behavior-changing consumer
A nice Swift reducer is still not always the boundary that changes behavior.

What to separate:
- the first reducer/mapper that makes the result understandable
- the first coordinator/controller/task consumer that writes durable state, schedules work, selects a route, or changes later behavior
- the later user-visible effect

Useful reminder:
- this page ends at the first continuation-owned consequence boundary that predicts later behavior, not at the most elegant async wrapper

## 4. Default workflow

### Step 1: freeze one representative async-facing flow
Pick one flow only.
Examples:
- completion/delegate -> imported `async throws` call -> first policy change
- callback -> `CheckedContinuation` resume -> Swift reducer -> next request family
- delegate -> `AsyncStream` delivery -> task consumer -> challenge/retry state

Avoid mixing several tasks, streams, or callback families.

### Step 2: draft one continuation-owned consequence chain
Write a compact draft before deeper tracing:

```text
callback or imported-async owner:
  completion / delegate / async function

candidate resume or delivery boundary:
  continuation resume / stream yield / task wakeup

possible normalization or policy reducer:
  Swift enum/object mapper / error reducer / mode selector

candidate first consumer:
  coordinator / controller / task body / scheduler / state write

visible effect:
  allow / retry / challenge / degrade / block / follow-up request
```

This draft may be wrong.
Its purpose is to stop uncontrolled async wrapper accumulation.

### Step 3: prove whether callback truth is already good enough
Before going deeper into continuation-owned logic, answer:
- is the callback/block/delegate family already frozen strongly enough?
- is the imported async surface clearly tied to that family, or is that still speculative?
- would stronger landing/signature proof change the meaning of everything downstream?

If not settled, route back first.

### Step 4: choose the first truthful resume/delivery boundary
Good candidates include:
- the exact continuation resume edge
- the first stream yield/dequeue pair that wakes the relevant consumer
- the first `for await` / iterator-consumption edge that turns `AsyncSequence` delivery into app-owned reduction
- the first resumed task frame that consistently appears only on the frozen flow
- the narrowest boundary where result material becomes available to app-owned Swift logic

Bad default choices include:
- the highest-level public async method name with no proof of downstream consequence
- every task/wrapper near the flow
- every helper that only creates or stores the continuation without owning delivery
- treating `URLSession.bytes(...)` header return as equivalent to the later byte-consumer that actually parses, frames, or classifies the stream

A source-backed discipline worth preserving here:
- continuation setup runs immediately in the current async context, but task progress after `resume(...)` is still scheduler/executor mediated rather than “inline callback code just kept going”
- in practical terms, separate three moments instead of collapsing them:
  - continuation creation/storage
  - resume or stream-delivery event
  - first resumed task-side reducer / consumer that actually predicts later behavior
- for stream-shaped cases, also separate:
  - stream construction
  - first yield / delivery
  - first iterator-side consumption that actually changes later behavior

### Step 5: separate normalization from policy mapping
Use small role labels:
- **resume** — continuation or stream delivery boundary
- **normalize** — raw payload/error becomes app-local object/enum family
- **map** — app-local object becomes allow/retry/challenge/degrade bucket
- **consume** — one coordinator/task/controller state change or scheduler choice
- **effect** — one later visible consequence

This prevents a common error:
- mistaking a pretty Swift enum conversion for the actual behavior-changing decision

### Step 6: prove one continuation-owned consumer with one compare pair
Use one narrow compare pair:
- accepted run vs challenged/degraded run
- callback-truthful run vs replay-close run with one missing obligation
- target action vs nearby non-target action

What you want to learn:
- does the same continuation/resume boundary appear in both runs?
- does normalization differ, or only later policy mapping?
- which first consumer best predicts later behavior?

A particularly useful compare question in continuation-shaped cases is:
- does the frozen callback family fire in both runs, yet one run never reaches the same resumed task-side reducer/consumer?

If yes, the best next proof object is often not more callback work at all.
It is one narrower resume-to-consumer explanation such as:
- missing exact-once resume
- stream delivery that buffers but does not wake the same consumer
- cancellation / timeout / stale-task handling that concludes the async surface differently
- a resumed value that normalizes the same way, but a later coordinator chooses a different policy bucket

### Step 7: stop at the first continuation-owned consequence boundary
The workflow succeeds when you can rewrite the path as:

```text
callback/delegate or imported-async owner
  -> continuation resume / stream delivery / task wakeup
  -> Swift normalization or policy mapper
  -> first behavior-changing consumer
  -> one later effect
```

At that point, route forward:
- to `topics/ios-result-callback-to-policy-state-workflow-note.md` when continuation ownership is no longer the hard part and the remaining work is ordinary policy-bucket / first-consumer reduction
- to `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md` when the path is still replay-close and the best explanation is one missing runtime table, initialized-image, object-materialization, or init/context obligation
- to `topics/ios-mitigation-aware-replay-repair-workflow-note.md` when the strongest remaining uncertainty is still replay-close authenticated-context or object-materialization repair

Do not keep this page open once continuation ownership is no longer the bottleneck.

## 5. Practical scenario patterns

### Scenario A: imported `async` call is visible, but the decisive effect happens after resume
Pattern:

```text
async call site easy to spot
  -> result arrives cleanly
  -> later task-owned reducer actually chooses challenge / allow / retry
```

Best move:
- stop treating the visible async call itself as final ownership
- prove the first resumed consumer that predicts the later effect

### Scenario B: callback landing is truthful, but `AsyncStream` owns the usable consequence
Pattern:

```text
delegate/callback already frozen
  -> stream buffering or delivery follows
  -> later consumer wakes and changes behavior
```

Best move:
- keep the callback proof fixed
- localize the first stream delivery / consumer boundary instead of reopening callback search

### Scenario C: async bytes / sequence delivery is visible, but the decisive effect lives at the first parser or classifier
Pattern:

```text
URLSession async bytes or similar AsyncSequence starts cleanly
  -> headers / sequence object appear truthful
  -> later for-await parser, framer, or classifier decides behavior
```

Best move:
- do not stop at “the async sequence exists”
- separate sequence construction from first iterator-side consumer that turns bytes/events into app-local meaning
- prove whether the first decisive boundary is framing, parsing, reduction, or later coordinator use

### Scenario D: replay is good enough to expose results, but policy still looks hidden
Pattern:

```text
replay-close path returns plausible result
  -> continuation resume happens
  -> app-local reducer / consumer still unclear
```

Best move:
- distinguish replay-close infrastructure success from consequence proof
- find the first continuation-owned mapper or consumer before assuming the replay path is fully explained

### Scenario E: nice Swift enum/object exists, but task coordinator owns the real consequence
Pattern:

```text
result normalized into readable Swift enum/object
  -> analyst overreads it as the answer
  -> controller/task scheduler later selects the actual behavior
```

Best move:
- treat the readable enum/object as normalization
- prove the first consumer/state write/scheduler decision that changes later behavior

## 6. Breakpoint / hook placement guidance
Useful anchors include:
- the frozen callback/delegate/completion family or imported-async owner path
- the candidate continuation resume, stream delivery, or iterator-consumption boundary
- the first Swift reducer that collapses raw resumed output or streamed bytes/events into one smaller app-local family
- the first task/coordinator/controller consumer that writes state or selects the next route
- one later effect that proves the chosen consumer mattered

If evidence is noisy, prefer:
- one async-facing flow and one compare pair
- one resume/delivery/iterator boundary, not every task helper nearby
- one reducer and one consumer, not every Swift wrapper
- one downstream effect, not every later async hop

## 7. Failure patterns this note helps prevent

### 1. Treating a visible async API as final ownership
Imported or wrapped async surfaces may still only expose an earlier completion family.

### 2. Treating callback truth and continuation-owned consequence as the same problem
They are adjacent, but not identical.

### 3. Treating the first readable Swift enum/object as the behavior-changing decision
Normalization is often easier to read than consequence ownership.

### 4. Confusing continuation setup, continuation resume, and post-resume consequence
Creating/storing a continuation, calling `resume`, and reaching the first resumed task-side reducer are related but not identical proof objects.

### 5. Flattening continuation, `AsyncStream`, and `AsyncSequence`/bytes-consumption cases into one bucket
Single-shot resume, multi-value stream delivery, and iterator-side consumption often have different truthful stop rules.

### 6. Reopening broad owner search when the real next gap is continuation-owned delivery or consumption
Once callback truth is already good enough, widening too early usually wastes effort.

### 7. Confusing replay-close infrastructure success with proved behavioral ownership
A result returning through async machinery is still not the same thing as proving the first policy-bearing consumer.

## 8. Relationship to nearby pages
- `topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md`
  - use first when the callback/block/delegate landing itself is still not trustworthy enough to support downstream claims
- `topics/ios-result-callback-to-policy-state-workflow-note.md`
  - use when continuation ownership is no longer the hard part and the remaining bottleneck is ordinary result normalization, policy mapping, or first-consumer proof
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`
  - use when replay remains close-but-wrong and the missing proof is now one narrower runtime obligation rather than continuation-owned consequence routing
- `topics/ios-mitigation-aware-replay-repair-workflow-note.md`
  - use when the path is replay-close and the strongest remaining uncertainty is one authenticated-context, object-materialization, or init/runtime repair target

## 9. Minimal operator checklist
Use this note best when you can answer these in writing:
- what single callback/delegate or imported-async path am I freezing?
- what is my best current continuation resume / stream delivery / task wakeup candidate?
- is callback truth already strong enough, or do I still need landing proof first?
- what is the first Swift-side normalization or policy mapper?
- what first consumer would make the flow operationally explainable?
- what one later effect would prove that consumer mattered?
- which narrower note should take over after continuation-owned consequence is proved?

If you cannot answer those, the case likely still needs broader callback landing proof or narrower replay/init-obligation repair first.

## 10. Source footprint / evidence quality note
This note is intentionally workflow-first and conservative.

It is grounded by:
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/ios-practical-subtree-guide.md`
- `topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md`
- `topics/ios-result-callback-to-policy-state-workflow-note.md`
- `sources/mobile-runtime-instrumentation/2026-03-23-ios-swift-concurrency-continuation-notes.md`

The evidence base is sufficient because the claim stays modest:
- Objective-C completion handlers are often bridged into Swift async entry points
- modern Swift code often routes callback/delegate delivery into continuation or stream-owned logic
- continuation setup and later task progress after `resume(...)` should not be collapsed into one proof boundary
- checked-continuation misuse patterns and delayed post-resume scheduling are practical reasons analysts should separate callback truth, resume truth, and first resumed consumer truth
- a practical iOS continuation note adds operator value by separating callback truth from post-resume consequence proof

## 11. Bottom line
When a modern iOS case already has a truthful callback/delegate family or a plausible async owner path, the next best move is often not more callback hunting.
First freeze the continuation-owned or stream-owned delivery boundary, then prove the first Swift-side reducer or consumer that changes behavior.
That single proof usually turns readable-but-slippery async machinery into a tractable next step.
