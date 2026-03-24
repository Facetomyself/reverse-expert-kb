# Protocol Replay Precondition and State-Gate Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, protocol state/message recovery, runtime-evidence bridge
Maturity: practical
Related pages:
- topics/protocol-state-and-message-recovery.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/record-replay-and-omniscient-debugging.md
- topics/firmware-and-protocol-context-recovery.md
- topics/post-validation-state-refresh-and-delayed-consequence-workflow-note.md
- topics/browser-request-finalization-backtrace-workflow-note.md
- topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md
- topics/protocol-pending-request-generation-epoch-and-slot-reuse-workflow-note.md

## 1. When to use this note
Use this note when the case already has meaningful protocol visibility, but the next operational step still fails.

Typical entry conditions:
- one message family or request/reply pair is already isolated
- parser, dispatch, or field-role visibility already exists
- the analyst can already generate or replay a structurally plausible message
- yet the target still rejects, degrades, retries, challenges, silently ignores, or no-ops that message
- the missing edge is likely one local session/state precondition rather than broad parser ignorance

Use it for cases like:
- proprietary protocol replay where the same packet shape works only after one earlier exchange or local phase change
- firmware service mutation where parsing succeeds but the reply family or action path still diverges
- stateful request fuzzing where mutations mostly die at a hidden capability or freshness gate
- challenge/response style targets where visible fields exist but acceptance still depends on one local mode, pending-request, or post-handshake state bit

Do **not** use this note when the real bottleneck is earlier, such as:
- message families are not stable yet
- sessions or flows are not separable yet
- parser or decode visibility is still missing
- environment reconstruction is still the primary unknown
- the real issue is browser/mobile transport ownership, native/page handoff, or anti-instrumentation visibility

In those cases, start with:
- `topics/protocol-state-and-message-recovery.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/firmware-and-protocol-context-recovery.md`
- or the more specific mobile/browser workflow notes

## 2. Core claim
A recurring protocol RE bottleneck is not parser discovery and not field labeling.
It is **acceptance localization**.

The useful analyst target is often:
- not the first parser you can name
- not the broadest state-machine diagram you can sketch
- not the full meaning of every field

It is the first local gate that decides whether a structurally plausible interaction is:
- accepted
- rejected
- retried
- challenged
- rate-limited
- silently ignored
- downgraded into a smaller behavior bucket

That gate is often more valuable than another round of global protocol formalization.

## 3. Target pattern
The recurring target pattern is:

```text
message family visible
  -> parser / dispatch / field roles partly visible
  -> replay or mutation still fails
  -> one local state/precondition gate decides accept / reject / degrade / no-op
  -> later reply, transition, retry, or state advance proves that gate mattered
```

The key discipline is:
- separate **message correctness** from **acceptance correctness**
- localize the first gate that predicts later advance or stall

## 4. What counts as a high-value acceptance gate
Treat these as high-value gate targets:
- first session-phase, mode, or epoch check after parse
- first capability/auth/authz reduction from many parsed values into a smaller local bucket
- first sequence, nonce, freshness, or replay-window check
- first pending-request / correlation-id / ownership check
- first branch that maps parsed message + current state into reject / retry / challenge / accept
- first helper that decides whether to advance local state, emit a reply, or schedule deferred handling
- first state bit, enum, or context member whose value differs systematically between accepted and stalled runs

Treat these as useful but often one layer too early:
- parser identification alone
- parsed-struct construction alone
- broad field labeling alone
- traffic clustering alone
- a clean message serializer/deserializer pair alone

## 5. Practical workflow

### Step 1: Freeze one narrow accepted-vs-stalled pair
Prefer one narrow compare pair over a wider corpus.

Good pairs include:
- same opcode accepted after handshake vs rejected before handshake
- same message family with one freshness/counter difference and one downstream behavior difference
- same replay attempted in two local states, only one of which advances
- same structurally plausible packet under two session timelines where only one yields the interesting reply or state change

Record only what you need:
- message family identity
- local state context around send/receive
- later visible consequence difference

If you do not yet have a stable accepted-vs-stalled pair, you are still too early for this note.

### Step 2: Mark five boundaries explicitly
Before chasing more field semantics, mark these five boundaries:

1. **message-family discriminator**
   - opcode, route, command tag, or family bucket
2. **parse boundary**
   - where bytes become fields, objects, or normalized locals
3. **candidate acceptance gate**
   - first state/precondition branch that could explain accept vs stall
4. **state-advance or effect boundary**
   - first local state write, reply-family choice, queue/timer, or action that only appears on accepted runs
5. **proof-of-advance boundary**
   - later reply, transition, side effect, or follow-up valid interaction proving the gate mattered

This prevents “we can parse it” from being mistaken for “we can make it work.”

### Step 3: Prefer the earliest stable accept/reject reduction
When multiple checks exist, prioritize the earliest stable reduction that cleanly predicts behavior:
- state enum + opcode gate
- sequence/freshness acceptance helper
- pending-request ownership branch
- capability/mode bucket reduction
- handshake-complete / session-ready check

This is usually a better anchor than fully reconstructing every transition first.

### Step 4: Localize the first branch that collapses protocol possibility into behavior
After the parse boundary, ask:
- where is the first branch that depends on both parsed message and current state?
- where is the first helper that reduces many candidate cases into one smaller local action bucket?
- where is the first place accepted and stalled runs diverge in a way that predicts later reply, retry, or no-op behavior?

Useful local role labels:
- `parse`
- `normalize`
- `state-read`
- `acceptance-gate`
- `state-write`
- `reply-select`
- `retry/challenge`
- `queue/timer`
- `effect-proof`

If a region cannot be given one of these roles, it may be churn rather than leverage.

### Step 5: Prove the gate with one downstream advance or rejection effect
Do not stop at “this branch probably checks freshness.”

Prove the candidate gate by tying it to one downstream effect such as:
- a reply family appears only when the gate passes
- a retry/challenge/degrade path appears only when the gate fails
- a session enum or bitfield advances only on accepted runs
- a later dependent message becomes valid only after one specific precondition passes
- a queue/timer/deferred action appears only when the gate resolves one way

A weaker but still useful proof is:
- accepted vs stalled behavior correlates with one branch or state member across a small compare set

### Step 6: Hand the result back to the next concrete task
Once localized, route the result into one next task only:
- replay stabilization
- targeted mutation or fuzzing design
- protocol-state note refinement
- firmware action modeling
- one deeper static proof target

Do not immediately widen back out into a full protocol specification unless the next task really needs it.

## 6. Breakpoint / hook placement guidance
Useful anchor classes:
- first parser return / decode-success boundary
- first session/context read after parse
- first phase/mode/epoch/handshake-ready check
- first sequence/nonce/window/freshness helper
- first pending-request or correlation-id ownership check
- first branch choosing accept / reject / retry / challenge / no-op
- first state-advance write or reply-serialization path only present on accepted runs
- first deferred queue/timer/retry arm after acceptance decision

If traces are noisy, anchor on:
- compare-run divergence around the earliest stable acceptance reduction
- state members that differ before later behavior diverges
- accepted-only reply or state-advance boundaries rather than all parser internals

## 7. Failure patterns this note helps prevent

### 1. Mistaking parser visibility for operational readiness
A named parser is not yet leverage if the first acceptance gate is still unknown.

### 2. Overcollecting more traffic after a good accepted-vs-stalled pair already exists
Once one useful pair exists, more captures often add breadth without explaining the first decisive gate.

### 3. Treating field labeling as the end of the hunt
The stronger target is often the first reduction from parsed values into:
- accepted vs rejected
- retry vs proceed
- challenge vs normal path
- queue/defer vs immediate action

### 4. Confusing explicit protocol state with the real operational precondition
The meaningful precondition may live in:
- one small enum
- a freshness timestamp/window
- a bitfield
- a pending request slot
- a capability bucket
- a local phase marker rather than a clean state-machine object

### 5. Chasing complete protocol formalization too early
A partial but proven acceptance gate is often enough to unblock replay, mutation, fuzzing, or explanation.

## 8. Concrete scenario patterns

### Scenario A: Handshake-complete is the real precondition
Pattern:

```text
same message shape is visible
  -> parser accepts both runs
  -> only post-handshake run advances
  -> one local phase/mode check decides whether reply or state advance occurs
```

Best move:
- anchor on the first phase/mode reduction, not on more packet labeling

### Scenario B: Sequence or freshness gate is the real bottleneck
Pattern:

```text
message family and field roles look correct
  -> replay still stalls or is rejected
  -> one helper checks counter/window/nonce freshness
  -> later reply or state advance only occurs when it passes
```

Best move:
- prove the first freshness acceptance helper before widening the field model

### Scenario C: Pending-request ownership is the real acceptance edge
Pattern:

```text
response-like message parses correctly
  -> visible fields look right
  -> no behavioral advance occurs
  -> one correlation-id / pending-slot check decides whether the message is consumed
```

Best move:
- treat pending-request ownership as the first consequence-bearing gate
- if that owner-match question has become the whole bottleneck, continue with `topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md`

## 9. Relationship to nearby pages
- `topics/protocol-state-and-message-recovery.md`
  - explains the broader message/state recovery family
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
  - use that when the missing bottleneck is still the first parser-to-state consequence edge itself
- `topics/firmware-and-protocol-context-recovery.md`
  - use that when environment reconstruction or peripheral context is still the main bottleneck
- `topics/post-validation-state-refresh-and-delayed-consequence-workflow-note.md`
  - this page is a protocol-side sibling for cases where visible data is not yet the decisive local acceptance/advance boundary
- `topics/browser-request-finalization-backtrace-workflow-note.md`
  - use that when the decisive consumer request still lives in browser/runtime request finalization rather than a protocol-state gate

## 10. Minimal operator checklist
Use this note best when you can answer these in writing:
- what is the one accepted-vs-stalled compare pair?
- where is the parse boundary?
- what is the first candidate acceptance gate?
- what later effect proves that gate mattered?
- what single next task becomes easier once the gate is known?

If you cannot answer those, the case likely needs a more upstream note first.

## 11. Source footprint / evidence quality note
This note is intentionally workflow-first.

It is grounded by:
- `topics/protocol-state-and-message-recovery.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/protocol-content-pipeline-recovery-workflow-note.md`
- `topics/runtime-behavior-recovery.md`
- `topics/record-replay-and-omniscient-debugging.md`
- `sources/firmware-protocol/2026-03-17-protocol-replay-precondition-and-state-gate-notes.md`
- `sources/protocol-and-network-recovery/2026-03-17-sperm-protocol-network-batch-3-notes.md`

The evidence base here is sufficient for a practical workflow note because the point is not to claim one universal protocol-state architecture.
The point is to normalize a recurring operator move that the KB previously lacked.

## 12. Bottom line
When protocol RE already has parser and field visibility, the next high-value move is often not more field labeling and not a broader state-machine sketch.

It is to localize the first **acceptance gate** that decides whether a structurally plausible replay, mutation, or stateful interaction is actually accepted, rejected, retried, challenged, or silently ignored.

## 13. Practical handoff rule
Stay on this note while the missing proof is still the first local acceptance gate that decides whether a structurally plausible replay, mutation, or stateful interaction advances, rejects, retries, challenges, degrades, or silently no-ops.

Leave broad replay/acceptance work once one acceptance gate is already good enough and the real bottleneck has shifted to one of these narrower next steps:
- `topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md` when the broad replay gate has already collapsed to one outstanding-request owner, correlation-id match, async handle, pending slot, or completion-state association deciding whether a response-like artifact is consumed at all
- `topics/protocol-pending-request-generation-epoch-and-slot-reuse-workflow-note.md` when broad owner-match is already good enough, but the remaining failure is now about late replies, retired owners, generation/epoch drift, phase/wrap mismatch, or slot/tag reuse realism
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md` when accepted local state is already good enough, but the first concrete emitted reply, serializer/framing path, queue/descriptor commit, or transport/peripheral handoff is still unproved
- `topics/peripheral-mmio-effect-proof-workflow-note.md` when acceptance and output handoff are already good enough, but the first hardware-facing write, queue/DMA/interrupt arm, or status-latch edge is still missing
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md` when even some peripheral-effect visibility already exists, but the later durable consequence still hides in interrupt/completion/deferred handling

A durable failure mode worth avoiding is staying too long in handshake/freshness/pending-slot discussion after one acceptance gate is already good enough and the real unresolved question has become emitted output, hardware-side effect, or later completion-driven consequence.