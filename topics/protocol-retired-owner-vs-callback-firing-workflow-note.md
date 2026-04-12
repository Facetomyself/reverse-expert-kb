# Protocol Retired-Owner vs Callback-Firing Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, protocol/service reply consumption, pending-owner retirement realism
Maturity: practical
Related pages:
- topics/protocol-firmware-practical-subtree-guide.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md
- topics/protocol-pending-request-generation-epoch-and-slot-reuse-workflow-note.md
- topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/analytic-provenance-and-evidence-management.md

## 1. When to use this note
Use this note when a case has already narrowed past broad replay gating, past broad pending-request owner match, and even past the first timeout/cancel cleanup suspicion.

Typical entry conditions:
- one request/completion family is already trustworthy enough to name
- one pending owner, waiter, tag, or per-request state object is already visible
- timeout/cancel/deadline cleanup already looks like the main liar more than parsing or correlation do
- yet one callback, handler, completion-queue tag, future completion, or wakeup still appears near or after that retire-looking boundary
- and the missing question is now whether that fired delivery still belongs to the same live request, only proves queued cleanup, or is already stale/abort-shaped noise

Use it for cases like:
- async RPC runtimes where `TryCancel()` or deadline expiry happened, but pending queue tags still arrive
- event-loop clients where timeout cleanup removes the logical owner, yet one handler still executes with abort/success-shaped status
- task/future runtimes where timeout is visible, but actual cancellation/retirement is delayed and one callback/future completion still races in
- request/reply stacks where the broad owner lifetime story is already plausible, but the remaining confusion is exactly whether one fired callback means “still-live request” or only “late delivery after retire”

Do **not** use this note when:
- the first pending owner is still unknown
- the first owner-match check is still unknown
- the response/completion family itself is still speculative
- the real missing edge is whether any reply/output was emitted at all
- the decisive remaining problem is actually generation/epoch/slot reuse rather than callback/tag/handler delivery fate

In those cases start with:
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md`
- `topics/protocol-pending-request-generation-epoch-and-slot-reuse-workflow-note.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`

## 2. Core claim
A practical stop rule worth preserving for this narrower seam is:

```text
timeout/cancel/retire boundary observed
  != pending callback/tag/handler cannot still fire
  != fired callback/tag still belongs to the same live owner
  != callback status or ok-bit explains ownership by itself
  != later consequence truth
```

Treat these as different proof objects until one is frozen:
- timeout/deadline/cancel request or boundary fact
- owner-retire / invalidate / remove-from-pending truth
- callback/tag already queued or still deliverable truth
- callback delivery plus status/`ok`/error code truth
- current-owner acceptance or stale-drop truth
- later wakeup/state/result/logging consequence

A second compact split is often useful:

```text
callback/tag delivered
  != operation escaped cancellation
  != owner was still live at delivery time
  != downstream consumer accepted it as current work
  != same-request durable consequence
```

The point is not to deny that callbacks matter.
It is to stop flattening **retire observed**, **delivery observed**, and **same live owner proved** into one vague async story.

## 3. Target pattern
The recurring pattern is:

```text
one live owner already exists
  -> timeout/cancel/deadline/close/TryCancel path runs
  -> owner retirement looks plausible
  -> one pending callback/tag/handler is still queued or still deliverable
  -> callback fires with success/abort/false/timeout-shaped status
  -> runtime still checks whether a current owner is allowed to accept it
  -> stale-drop / cleanup-only / no-op / late effect / real wakeup wins
```

The key discipline is:
- separate **retirement boundary** from **delivery boundary**
- separate **delivery boundary** from **current-owner acceptance**
- separate **status code or `ok` bit** from **behavior-bearing consequence**

## 4. What counts as a high-value compare pair
Prefer a narrow pair where the broad request family stays similar but callback fate differs across the retire boundary.

Good pairs include:
- same request family with one callback firing before retirement and one after retirement
- same completion-queue tag family with one `ok` result on a live call and one delivered tag after `TryCancel()` or a dead call
- same timer/future wait where cancel produces an abort-shaped callback in one case, but an already-queued success-shaped callback in another
- same timeout wrapper where one inner task cancels promptly and another only retires later
- same visible callback path with one case waking the live waiter and one case hitting stale-drop / ignore / late-reply handling

Record only:
- the retire-looking boundary
- the queued-or-deliverable callback object/tag/handler
- the callback delivery result (`ok`, error code, exception, success)
- the first current-owner acceptance or stale-drop branch
- the later consume-vs-no-effect difference

If you cannot produce a pair where the callback family looks deceptively similar across retirement, you may still be one step too early for this note.

## 5. Practical workflow

### Step 1: Freeze one retire-vs-deliver compare pair
Choose a pair that holds the broad request family constant.

Avoid starting from:
- a completely different request type
- a completely different channel/session
- a parse-broken failure
- a case where callback delivery itself is still speculative

The whole value here is that the callback/tag family should look similar enough to tempt overclaim.

### Step 2: Mark seven boundaries explicitly
1. **live-owner creation**
   - where the runtime creates the waiter, per-request object, pending map entry, or callback/tag contract
2. **retire request boundary**
   - where timeout/deadline/cancel/close/TryCancel is requested or observed
3. **retire completion boundary**
   - where the runtime actually removes, invalidates, or marks the owner stale
4. **delivery eligibility boundary**
   - where one callback/tag/handler is already queued or remains deliverable despite retirement pressure
5. **callback/tag delivery boundary**
   - where the handler actually runs or the tag is dequeued
6. **current-owner acceptance boundary**
   - where the runtime decides whether the delivered object still belongs to a live current owner
7. **durable consequence boundary**
   - first wakeup, state change, result delivery, stale-drop log, cleanup-only path, or other behavior-bearing effect

This prevents “timeout happened and a callback fired” from being misread as a solved ownership story.

### Step 3: Prefer the earliest truthful delivery boundary over framework folklore
When docs, blog posts, or implementation names tempt you into broad claims like:
- “cancel means the callback won’t fire”
- “tag arrived so the call must still be live”
- “timeout already killed the work”
- “success return proves the request beat cancellation”

reduce earlier:
- where could the callback have already been queued?
- where does retirement actually become durable?
- where is current-owner acceptance checked after delivery?
- what one downstream effect proves real acceptance versus cleanup noise?

### Step 4: Prove one fired-after-retire case, not only one live case
Do not stop at the accepted case.

Also prove at least one of these:
- timeout/close/cancel boundary occurred, yet callback still fired
- callback/tag still delivered, yet the owner was already gone
- delivered callback carried abort/failure shape and no longer woke the original waiter
- delivered callback carried success-ish shape, yet the same current owner was no longer the one that mattered
- callback was suppressed in one run but only because retirement beat queueing, not because the framework guarantees suppression in general

This keeps the workflow practical instead of collapsing back into vague “async races happen” narration.

### Step 5: Tie delivery status to one durable consequence
Useful downstream proofs:
- only live-owner deliveries resolve the waiter/future/promise
- post-retire deliveries still run cleanup/logging but not the original effect
- a delivered tag with `ok=false` proves dead-call classification, not callback non-delivery
- a success-shaped callback after a retire-looking boundary still needed one owner check before state changed
- the same callback family has different consequences before and after retirement because acceptance, not delivery alone, is the real gate

### Step 6: Preserve the smallest truthful compare object
Once the boundary is known, preserve one compare object that includes:
- request family
- owner creation point
- retire request point
- retire completion point
- callback/tag/handler identity
- delivery status/`ok`/error
- first accept-vs-drop branch

Otherwise later analysts will reproduce the same “the callback still fired, so maybe timeout/cancel was fake” confusion.

### Step 7: Hand off narrowly
Once this seam is localized, hand the case to one next task only:
- generation/epoch/slot-reuse work if the remaining liar is now hidden owner reuse rather than delivery fate
- reply-emission work if the supposedly delivered completion never really corresponded to an emitted reply or transport-visible output
- evidence packaging if the proof is already good enough and now mainly needs preservation
- broader runtime-evidence work only if callback delivery itself remains too noisy to compare honestly

## 6. Source-backed reminders worth preserving

### Reminder A: Boost.Asio timer cancel proves cancel request is weaker than handler fate
Boost.Asio documents that `basic_waitable_timer::cancel()` forces completion of pending waits and cancelled handlers are invoked with `operation_aborted`.
But it also documents the narrower trap that matters here:
- if the timer has already expired when `cancel()` is called
- handlers may already have been invoked, or queued for near-future invocation
- those queued handlers can no longer be cancelled and may still report successful completion

For operator purposes, the practical reduction is:
- do not stop at `cancel()` call or return value
- freeze whether the relevant handler was already queued
- then decide whether the later callback is live-owner truth or only already-queued delivery truth

### Reminder B: gRPC `TryCancel()` proves pending-tag delivery is weaker than live-call truth
gRPC C++ documents that `ClientContext::TryCancel()` is best-effort, there is no guarantee the call will be cancelled, and pending completion-queue tags are not removed; they are still delivered.
The completion queue documentation separately states that each tag is delivered regardless of whether the operation succeeded, while `ok` carries the success/failure classification.

For operator purposes, the practical reduction is:
- do not stop at `TryCancel()` visibility
- do not stop at tag delivery visibility
- do not stop at one `ok` value alone
- freeze the post-delivery current-owner acceptance or dead-call classification that actually answers the analyst’s question

### Reminder C: `asyncio.wait_for()` proves timeout boundary is weaker than actual retirement completion
Python documents that `asyncio.wait_for()` cancels the task on timeout, but then waits until the future is actually cancelled, so the total wait time may exceed the timeout.

For operator purposes, the practical reduction is:
- treat timeout observation as boundary truth first
- then freeze actual cancellation/retirement completion
- only after that classify later callback/task activity as live-owner truth, cleanup lag, or swallowed-cancellation pathology

### Reminder D: Tokio timeout proves deadline machinery is weaker than cooperative task fate
Tokio documents that timeout is checked before polling the future, so a future that does not yield can complete and exceed the timeout without returning an error.
It also documents that cancelling the timeout wrapper is done by dropping the future wrapper and needs no extra cleanup work.

For operator purposes, the practical reduction is:
- do not overread a deadline boundary without confirming cooperative yield/retirement behavior
- keep wrapper cancellation separate from the fate of the underlying work object
- do not flatten “deadline crossed” into “callback/consequence impossible now” without one runtime-backed compare slice

Use all of these sources conservatively as operator analogies, not as a claim that every target implements the same callback API, queue contract, or scheduler behavior.

## 7. Breakpoint / hook placement guidance
Useful anchors for this stage:
- timeout/deadline setter and cancel/close/TryCancel request sites
- pending-owner removal / invalidation / stale-mark writes
- callback/tag enqueue or posting sites
- callback/handler entry or completion-queue dequeue sites
- post-delivery `ok` / error / exception classification
- first current-owner acceptance or stale-drop branch after delivery
- first waiter resolution / future completion / log / no-op consequence

If traces are noisy, anchor on:
- one retire request
- one retire completion
- one callback still delivered after retirement pressure
- one first accept-vs-drop branch
- one later effect difference

## 8. Failure patterns this note helps prevent

### 1. Treating cancel request as callback suppression
Many runtimes only promise best-effort cancellation or late retirement.

### 2. Treating callback delivery as live-owner proof
A callback can fire because it was already queued, because tags are always delivered, or because cleanup finished later than assumed.

### 3. Treating status/`ok` as the whole story
Abort/failure/success classification is weaker than proving who still owns the result.

### 4. Reopening parser/crypto theories too early
When timeout/cancel cleanup is already the main liar, callback fate often needs one smaller compare first.

### 5. Saving bytes but not retirement timing
Replay fixtures that preserve payloads but not retire-vs-deliver ordering often recreate the same confusion.

## 9. Concrete scenario patterns

### Scenario A: Cancel requested, handler still fires because it was already queued
Pattern:

```text
wait/request nearly completes
  -> cancel/timeout path runs
  -> relevant handler was already queued
  -> handler still fires
  -> analyst overreads this as proof cancellation was meaningless
```

Best move:
- freeze queueing-before-retire versus retire-before-queueing as the compare boundary.

### Scenario B: `TryCancel()` runs, but completion-queue tags still drain
Pattern:

```text
client issues TryCancel
  -> call enters dead/cancelled classification
  -> pending CQ tags still deliver
  -> ok/result classification changes
  -> only one later acceptance branch proves whether the original live owner still mattered
```

Best move:
- tie tag delivery to one post-delivery ownership/acceptance branch, not to broad “call survived cancel” narration.

### Scenario C: Timeout observed, actual retirement lags behind
Pattern:

```text
timeout boundary reached
  -> cancel requested
  -> runtime still waits for actual cancellation / cooperative yield
  -> later callback/task activity still appears
  -> analyst overreads timeout as already-complete teardown
```

Best move:
- freeze timeout request, actual retirement completion, and first post-retire callback separately.

### Scenario D: Delivery status changes, but same-request ownership is still the real question
Pattern:

```text
callback/tag delivered with abort/success-ish shape
  -> status looks informative
  -> live-owner check still decides whether downstream effect happens
```

Best move:
- follow the first accept-vs-drop consumer after status classification rather than stopping at the status itself.

## 10. Relationship to nearby pages
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
  - broader replay-gate parent when the case has not yet narrowed to pending-owner lifetime realism
- `topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md`
  - immediate parent when the real unknown is still the first owner-match check rather than retirement-vs-delivery fate
- `topics/protocol-pending-request-generation-epoch-and-slot-reuse-workflow-note.md`
  - use that when the main remaining lie is hidden generation/epoch/reuse realism rather than one already-known retire boundary versus callback fate
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
  - use that when the replay object itself is still too weak to hold retire-vs-deliver ordering steady
- `topics/runtime-behavior-recovery.md`
  - use that when callback delivery itself is still too noisy to compare honestly and the case needs broader runtime observation restructuring first

## 11. Source footprint / evidence quality note
This note is intentionally workflow-first.

Primary retained support:
- `sources/protocol/2026-04-13-retired-owner-vs-callback-firing-notes.md`
- `sources/protocol/2026-04-13-0450-retired-owner-callback-firing-search-layer.txt`
- Boost.Asio `basic_waitable_timer::cancel` documentation
- gRPC C++ `ClientContext::TryCancel()` and `CompletionQueue::Next()` documentation
- gRPC cancellation guide
- Python `asyncio.wait_for()` documentation
- Tokio `time::timeout` documentation
- `topics/protocol-pending-request-generation-epoch-and-slot-reuse-workflow-note.md`

Confidence note:
- strong for the narrow workflow lesson that retirement boundaries and delivery boundaries must stay separate
- strong for the specific documented reminders around Boost.Asio and gRPC delivery-after-cancel semantics
- moderate for exact cross-framework vocabulary because runtimes differ in how they expose handlers, tags, callbacks, and cooperative cancellation

## 12. Bottom line
When timeout/cancel cleanup already looks like the main liar, the next useful move is often not another round of packet labeling, parser doubt, or broad replay theory.

It is to localize the first **retired-owner vs callback-firing** boundary that decides whether a delivered handler/tag/callback still belongs to a live request, only proves queued cleanup, or has already become stale delivery noise.
