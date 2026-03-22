# Protocol Pending-Request Correlation and Async-Reply Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, protocol/service reply consumption, outstanding-request ownership localization
Maturity: practical
Related pages:
- topics/protocol-firmware-practical-subtree-guide.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md
- topics/protocol-reply-emission-and-transport-handoff-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/protocol-ingress-ownership-and-receive-path-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/analytic-provenance-and-evidence-management.md

## 1. When to use this note
Use this note when a request/response, RPC, mailbox, or completion-shaped case has already progressed far enough that:
- one representative request family is already trustworthy enough to name
- a response, completion, callback, or reply-like artifact is already visible or reconstructable
- but the target still does not advance, complete, wake the waiting caller, or consume the response in the expected way
- and the most likely missing edge is no longer broad parser discovery or whole-session modeling, but one **outstanding-request ownership** rule

Typical entry conditions:
- the analyst can already point to one request family and one candidate response family
- replayed or injected response-like traffic is structurally plausible, maybe even parser-acceptable
- yet the client/runtime silently drops it, leaves the request pending, or routes nothing to the waiting consumer
- one pending slot, async handle, callback queue, correlation ID, sequence slot, or request-table owner is likely deciding whether the response counts

Use it for cases like:
- proprietary request/reply protocols where a seemingly correct response is ignored because it does not match one live pending-request entry
- Windows RPC / local RPC / ALPC-adjacent cases where the response only matters if it is tied to the correct async call state or completion path
- firmware mailbox / command queue cases where a completion is only consumed if it matches one descriptor, token, or outstanding command slot
- message-queue RPC patterns where reply queue routing exists, but the client still filters by correlation or pending-request identity
- mobile or browser-adjacent service bridges where a callback response exists but does not wake the waiting promise/future/callback holder without one request-owner match

Do **not** use this note when:
- the response family itself is still speculative
- the real bottleneck is still serializer/framing visibility or output-side emission
- replay is still broadly failing due to auth/freshness/session gates
- the real missing edge is still the first receive owner or parser entry for the inbound bytes

In those cases, start with:
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- `topics/protocol-ingress-ownership-and-receive-path-workflow-note.md`

## 2. Core claim
A recurring practical replay failure is not:
- “the reply bytes are wrong”
- “the parser is still unknown”
- “the whole state machine is still missing”

It is:
- the candidate reply is not owned by the **right outstanding request state**

The useful next analyst target is often one of these:
- pending-request table entry
- async-call state object
- correlation-ID matcher
- callback queue selector
- request token / slot / descriptor owner
- completion event / port / future / promise associated with one live request

The key discipline is:
- separate **response shape correctness** from **response ownership correctness**
- localize the first place where the runtime decides “this reply belongs to that request”

## 3. Target pattern
The recurring shape is:

```text
one request family already known
  -> one response/completion artifact already visible
  -> response-like replay still no-ops or leaves caller pending
  -> one owner-match check decides whether the response is consumed
  -> later callback/return/state-advance only appears when that match succeeds
```

This note exists because that bottleneck is narrower than general replay gating and deserves a dedicated operator move.

## 4. What counts as a high-value ownership gate
Treat these as high-value targets:
- first lookup from response-like data into a pending-request table/map/list
- first comparison against correlation ID, request ID, sequence token, message tag, slot index, or descriptor token
- first async handle / promise / future / event object that must be the live owner of the completion
- first branch that decides “matched outstanding request” vs “ignore / stale / unknown / unexpected reply”
- first dequeue or consume step that removes an entry from a pending set only on successful match
- first completion callback or wakeup path that only fires after owner match succeeds

Treat these as useful but often one layer too early:
- parser visibility alone
- response serializer visibility alone
- broad request/response family naming alone
- transport arrival proof alone

## 5. Practical workflow

### Step 1: Freeze one waiting-request vs ignored-reply compare pair
Prefer one narrow compare pair over broad traffic collection.

Good pairs include:
- same response family tied to a live request vs replayed after the request slot is gone
- same payload fields delivered with matching vs non-matching correlation token
- same completion shape received while one async handle is pending vs after timeout/cleanup
- same mailbox completion code with one descriptor token difference and one clear consume-vs-ignore behavioral difference

Record only what matters:
- request family identity
- candidate response/completion identity
- visible waiting state before arrival
- visible consequence difference after arrival

If you do not yet have a useful waiting-vs-ignored pair, you are too early for this note.

### Step 2: Mark five boundaries explicitly
Before hunting semantics, mark these five boundaries:

1. **request issuance boundary**
   - where the outstanding request becomes live
2. **pending-owner creation boundary**
   - where the runtime allocates/inserts one pending slot, handle, future, callback registration, or table entry
3. **response arrival boundary**
   - where the response/completion-like object first becomes visible on the inbound side
4. **ownership-match boundary**
   - first place that compares the arrival against one pending owner
5. **consume/wake/complete boundary**
   - first callback, future resolution, state advance, dequeue, or return path that only happens on successful match

This prevents “response arrived” from being mistaken for “response consumed.”

### Step 3: Prefer the earliest stable owner-match reduction
When multiple checks exist, prioritize the earliest stable reduction that predicts later completion:
- pending-table lookup by token
- correlation-ID equality check
- descriptor/slot match
- async state object association
- callback queue / request owner routing

That is usually more useful than naming every late completion callback first.

### Step 4: Label the local roles clearly
Useful local role labels here:
- `request-issue`
- `pending-insert`
- `response-arrival`
- `owner-match`
- `unknown/stale-drop`
- `consume/dequeue`
- `wake/resolve/callback`
- `timeout/cancel cleanup`
- `post-completion cleanup`

If a region cannot be given one of these roles, it may be churn rather than leverage.

### Step 5: Prove the owner with one downstream consequence
Do not stop at “this field looks like a correlation ID.”

Prove it by tying successful owner match to one downstream effect such as:
- a waiting future/promise resolves only when the match succeeds
- one pending entry disappears only on the matched case
- one callback/event/completion port notification fires only for the matched case
- one return value or out-buffer becomes valid only when the right async handle completes
- one later dependent request becomes legal only after one completion is consumed

A weaker but still useful proof is:
- matched vs ignored behavior correlates with one token/slot/owner object across a small compare set

### Step 6: Check lifecycle before blaming parse or crypto
Before escalating back into freshness, auth, or parser theory, explicitly ask whether the outstanding owner is still alive when the reply arrives.

High-value lifecycle questions:
- was the pending owner removed by timeout before the reply was delivered?
- did cancellation, disconnect, channel teardown, or queue consumer reuse invalidate the owner?
- is there a generation/epoch/reuse boundary where the same visible token no longer names the same live request?
- does the runtime route late replies into a stale/unknown-reply path even when correlation fields still look structurally correct?

This matters because a late reply after cleanup often looks like:
- a parser-visible response
- a plausible correlation field
- but no wakeup/consume effect because the runtime already retired the owner and now treats the reply as stale, unknown, or late

That is still an ownership-lifecycle failure, not automatically a parser failure.

### Step 7: Hand off narrowly
Once the owner-match edge is localized, hand the case to one next task only:
- replay stabilization when the response now needs correct token generation, generation/epoch preservation, or slot lifetime preservation
- reply-emission/handoff work if the real unresolved issue is whether the response is emitted at all
- parser/state consequence work if the owner match is solved and the next unknown is later local state change
- provenance packaging if the hard part is preserving the compare slices and assumptions

Do not widen immediately back into generic replay theory.

## 6. Breakpoint / hook placement guidance
Useful anchors for this stage:
- request enqueue / pending-map insertion
- async handle initialization and completion APIs
- callback registration or promise/future allocation
- correlation-ID copy or comparison sites
- pending-slot dequeue/removal
- unknown/stale reply discard branches
- completion event / APC / IOC / callback delivery
- mailbox descriptor / queue token checks in firmware or driver-like code

If traces are noisy, anchor on:
- the first pending-owner creation
- the first response-to-owner compare
- the first matched-only wakeup/consume effect

## 7. Failure patterns this note helps prevent

### 1. Mistaking structural reply correctness for consumed reply correctness
A response can be well-formed and still be operationally irrelevant if it is not owned by a live request.

### 2. Overcollecting more traffic after one useful compare pair already exists
Once one waiting-vs-ignored pair exists, more captures often widen the corpus without proving the owner gate.

### 3. Treating parser visibility as the end of the hunt
The stronger target is often the first comparison that maps arrival -> pending owner -> consume/drop.

### 4. Mistaking timeout cleanup or late-reply discard for parser failure
A reply can parse correctly and still be irrelevant because the runtime already retired the pending owner, marked the request timed out, or reused the slot/channel/generation before the reply arrived.

### 5. Blaming freshness/auth too early
Those can matter, but in some cases the real hidden gate is simply that the reply is unmatched to any live outstanding request state.

### 6. Staying too broad in “replay gating” after the bottleneck has narrowed
Once the case has clearly collapsed to pending ownership, general replay-gate narration becomes less useful than one precise owner-match proof.

## 8. Concrete scenario patterns

### Scenario A: Async RPC completion handle is the true reply owner
Pattern:

```text
reply exists
  -> call is still pending
  -> one async-call state object must complete the reply path
  -> no completion happens until the right handle-owned state is satisfied
```

Best move:
- anchor on async state creation, notification method, and completion path rather than more transport commentary

### Scenario B: Callback queue + correlation ID is the real consumer gate
Pattern:

```text
response arrives on the right broad channel
  -> client still filters it
  -> one correlation value decides whether it belongs to the outstanding request
```

Best move:
- prove the first equality/match check and matched-only callback/future resolution

### Scenario C: Firmware/mailbox completion matches one pending descriptor slot
Pattern:

```text
completion code is visible
  -> parser/dispatch can read it
  -> command still appears pending
  -> one descriptor token / slot / queue entry must match before completion is consumed
```

Best move:
- localize descriptor ownership and dequeue-on-match behavior

### Scenario D: Late reply after timeout looks valid but has already lost its owner
Pattern:

```text
reply arrives with plausible structure and correlation material
  -> earlier wait path already timed out or cleaned up
  -> pending entry / callback registration / request future is gone or retired
  -> runtime logs or follows stale/unknown-reply handling instead of wakeup
```

Best move:
- compare live-pending vs timed-out arrival on the same request family
- prove where timeout/cancel cleanup retires the owner
- treat late-reply discard as an ownership-lifecycle question before widening into parser or crypto theories

## 9. Relationship to nearby pages
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
  - this page is a narrower child for cases where the broad gate has already collapsed to outstanding-request ownership
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
  - use that when the representative request/response fixture is still not frozen yet
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
  - use that when the missing proof is whether a reply is emitted/committed at all, not whether the receiver matches it to a pending owner
- `topics/protocol-ingress-ownership-and-receive-path-workflow-note.md`
  - use that when the first inbound owner is still unknown before response-consumption logic even starts
- `topics/analytic-provenance-and-evidence-management.md`
  - use that when the technical proof is already good enough and the problem is preserving the compare slices and owner assumptions

## 10. Minimal operator checklist
Use this note best when you can answer these in writing:
- what is the one outstanding request being waited on?
- where is that pending owner created or inserted?
- where does the candidate reply first arrive?
- what is the first owner-match comparison?
- what downstream effect proves successful consumption?

If you cannot answer those, the case likely needs a more upstream note first.

## 11. Source footprint / evidence quality note
This note is intentionally workflow-first.

Primary retained support:
- `sources/firmware-protocol/2026-03-22-pending-request-correlation-and-async-reply-notes.md`
- `sources/firmware-protocol/2026-03-23-pending-request-timeout-and-late-reply-lifecycle-notes.md`
- Microsoft Learn async RPC reply/completion documentation
- Microsoft Learn `RPC_ASYNC_STATE` structure documentation
- Microsoft Learn MS-RPCE connection timeout note
- Trail of Bits RPC Investigator note for active-call/ETW-aware RPC visibility
- ALPC transport internals overview for pending communication-object context
- RabbitMQ RPC tutorial as a clear generic correlation-ID ownership model
- Spring AMQP request/reply timeout and late-reply handling documentation
- Berkeley BitBlaze / Replayer framing for dialogue replay as a practical protocol-RE end state

Confidence note:
- strong for the recurring workflow shape
- intentionally conservative about protocol/framework universality
- does not claim ownership mismatch is the only reason a reply may be ignored

## 12. Bottom line
When a structurally plausible response, completion, or reply-like artifact still fails to wake, complete, or advance the waiting side, the next high-value move is often not more packet labeling and not another broad replay discussion.

It is to localize the first **pending-request ownership** check that decides whether the arriving artifact belongs to one live outstanding request state at all.
