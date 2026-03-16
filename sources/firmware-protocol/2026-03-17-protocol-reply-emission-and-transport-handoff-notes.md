# Source Notes — Protocol reply-emission and transport-handoff workflow

Date: 2026-03-17
Purpose: support a practical protocol / firmware workflow note for the recurring case where message families, parsers, state edges, and even acceptance gates are already partly visible, but the analyst still has not proved the first local boundary that actually emits, queues, serializes, or hands the accepted result to the transport/peripheral side.

## Scope
This note does not try to survey protocol reply logic in the abstract.
It consolidates practical signal already present in the KB into one operator-facing workflow frame for a common bottleneck:

- one message family is already isolated
- parser or dispatch visibility already exists
- some field or opcode semantics are already plausible
- one state edge or acceptance gate may already be partly understood
- yet the investigation still stalls because the analyst cannot prove where the accepted path becomes:
  - one concrete reply-family selection
  - one serialization or buffer-fill path
  - one queue / descriptor / send-slot insertion
  - one transport / peripheral handoff
  - one externally visible response boundary

## Supporting source signals

### 1. Existing protocol-state synthesis already treats downstream utility as the real bar
From:
- `topics/protocol-state-and-message-recovery.md`

High-signal points reused here:
- protocol understanding is incomplete without operational structure
- downstream value depends on whether the recovered model supports replay, fuzzing, generation, and explanation
- message/field visibility is not the same as a useful control point

Why it matters:
- some protocol cases already have enough parser/state understanding for explanation, yet still lack the one reply-emission or send-handoff proof boundary needed for generation, mutation, or transport modeling

### 2. Existing parser-to-state workflow logic already stops one layer too early for some cases
From:
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`

High-signal points reused here:
- parser visibility is not consequence visibility
- one representative compare pair is better than wider trace accumulation
- the first reduction from parsed material into one smaller action bucket is the important move

Why it matters:
- in some cases that move is already done: the analyst already knows the message was accepted or reduced into one local action/state bucket, but still does not know where that accepted result becomes one concrete emitted reply, queued output object, or transport handoff

### 3. Existing replay-precondition workflow shows that acceptance is not yet transport proof
From:
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`

High-signal points reused here:
- structurally plausible replay can still fail because one hidden local gate remains unproved
- accepted-vs-stalled compare pairs are the useful shape
- phase/freshness/pending-request ownership checks are often decisive

Why it matters:
- even after the gate is understood, there is still often one more practical bottleneck:
  - accepted parse/state does not yet explain where the target actually commits to reply emission, output queueing, or transport/peripheral send behavior

### 4. Existing firmware notes reinforce the difference between internal state proof and external effect proof
From:
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`

High-signal points reused here:
- the useful edge is the first local boundary that predicts later visible behavior
- queue / DMA / interrupt-arm boundaries often matter more than broader labeling
- later externally visible consequences should be used as proof-of-effect boundaries

Why it matters:
- protocol reply-emission cases have the same operator shape on the protocol/output side:
  - one accepted local state or reply object is not yet enough
  - the useful proof target is the first queue / serialize / send / descriptor / write boundary that predicts the actual outgoing behavior

### 5. Existing mobile/browser notes show a transferable pattern: visible success is not the same as first emitted consumer request
From:
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/mobile-response-consumer-localization-workflow-note.md`
- `topics/post-validation-state-refresh-and-delayed-consequence-workflow-note.md`

High-signal points reused here:
- visible tokens, parsed values, or even successful validation can still be one layer too early
- the decisive edge is often the first local consumer or finalization boundary
- compare-run discipline is strongest when anchored on an actual emitted or externally visible consequence

Why it matters:
- protocol/firmware reply work has the same shape:
  - visible parsed values or accepted state may exist
  - but the analyst still needs the first concrete output-finalization or transport-handoff edge that explains why one run emits/replies/sends and the other stalls, degrades, retries, or only updates local state

## Distilled practical pattern
A useful workflow pattern for protocol reply / send-side stalls is:

```text
message family visible
  -> parser / dispatch / state edge partly visible
  -> acceptance may already be visible
  -> first reply object / reply-family / output buffer exists or is suspected
  -> one local serialize / queue / transport-handoff edge decides emitted behavior
  -> one later wire reply, device output, queue drain, or peripheral send proves that edge mattered
```

## Operator heuristics to preserve
- Do not assume parser visibility, accepted state, or a plausible reply object means the transport side is solved.
- Treat these as separate milestones:
  - message-family visibility
  - parse visibility
  - state / acceptance visibility
  - reply-object or reply-family visibility
  - reply-emission / transport-handoff visibility
  - externally visible proof-of-send / proof-of-reply
- Prefer one narrow compare pair such as:
  - accepted request with emitted reply vs accepted request with no emitted reply
  - same opcode and same accepted state with one pending-request slot occupied vs free
  - same handler family before vs after one queue/descriptor/state condition changes
  - same reply-family object created in both runs but serialized/sent only in one
- Useful local anchors include:
  - first reply-family selector after state reduction
  - first length/CRC/sequence fill into an outbound object
  - first enqueue / descriptor submission / ring write / mailbox insertion / send-slot ownership check
  - first serializer or framing helper that turns internal state into transport-shaped bytes
  - first transport callback, driver call, socket send helper, or peripheral-output write only reached on emitted runs
  - first output-complete / queue-drain / ack / externally visible reply boundary proving the handoff mattered
- If the reply object seems visible but no emitted behavior follows, suspect:
  - pending-slot ownership
  - output queue saturation
  - later serializer failure
  - send eligibility / session-phase reduction
  - deferred worker or interrupt-side output ownership
  before assuming the parser or state model is still wrong.

## Candidate canonical KB mapping
This note most directly supports:
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`

It also strengthens:
- `topics/protocol-state-and-message-recovery.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`

## Bottom line
Some protocol / firmware cases do not really unblock when the analyst finds the parser, the first state edge, or even the local acceptance gate.
They unblock when the analyst proves which local reply-emission, serialization, queue, or transport-handoff boundary actually turns that accepted state into one externally visible reply or send behavior.