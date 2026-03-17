# Protocol Ingress Ownership and Receive-Path Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, protocol state/message recovery, firmware/protocol context bridge
Maturity: practical
Related pages:
- topics/protocol-state-and-message-recovery.md
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/peripheral-mmio-effect-proof-workflow-note.md
- topics/isr-and-deferred-worker-consequence-proof-workflow-note.md
- topics/runtime-behavior-recovery.md

## 1. When to use this note
Use this note when the case already has meaningful inbound visibility, but the analysis still stalls one step before parser/state leverage.

Typical entry conditions:
- one message family, packet family, or inbound event is already visible on the wire, socket, mailbox, or device side
- one parser, decoder, or state path is already suspected
- some receive-side callbacks, queues, rings, descriptors, or deferred workers are already visible
- but the analyst still has not proved which local ingress path actually owns the inbound bytes and feeds later parsing, dispatch, or stateful handling

Use it for cases like:
- proprietary protocol binaries where traffic capture exists, but the first parser invocation is hidden behind buffering, framing, or queue ownership
- firmware services where inbound commands are visible externally, yet the decisive local receive handoff still hides behind ISR/deferred receive work, DMA/ring consumption, or mailbox fan-out
- rehosting or harness work where external packets arrive, but the target never reaches the expected parser or handler because receive-path ownership is still under-modeled
- mixed socket/driver/service targets where several callbacks read or copy bytes, but only one actually commits them into parser-relevant ownership

Do **not** use this note when the real bottleneck is later, such as:
- the receive owner is already known and the missing edge is parser-to-state consequence
- replay still fails because an acceptance gate or state precondition is unproved
- the decisive issue is reply/output-side queueing or send ownership rather than inbound ownership
- the case is really a mobile/browser transport-owner question rather than protocol/firmware receive-path ownership

In those cases, start with:
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- or the more specific mobile/browser ownership notes

## 2. Core claim
A recurring protocol / firmware bottleneck is not traffic visibility and not even parser suspicion.
It is **receive-path ownership proof**.

The useful analyst target is often:
- not the first packet capture you can label
- not the first socket-read or IRQ you can observe
- not the broadest set of driver callbacks you can enumerate
- not the first parser-looking function you can name

It is the first local edge that turns inbound traffic into one parser-relevant owned object, such as:
- a ring / descriptor / DMA completion consumed into one receive buffer
- a socket / mailbox / queue dequeue that commits bytes to one message family
- a framing or reassembly helper that turns stream data into one parser-ready object
- a deferred receive worker or callback that is the first stable owner of the message
- a buffer ownership or queue insertion boundary that consistently predicts later parse/state behavior

That edge is usually more valuable than more broad capture, ISR enumeration, or parser guessing.

## 3. Target pattern
The recurring target pattern is:

```text
inbound bytes / frame / packet visible
  -> transport / device / driver activity visible
  -> several receive callbacks, queues, rings, or workers are plausible
  -> one local receive handoff actually commits parser-relevant ownership
  -> later parse/state/reply behavior proves it mattered
```

The key discipline is:
- separate **external inbound visibility** from **local receive ownership visibility**
- localize the first edge that predicts later parser/state behavior

## 4. What counts as a receive-ownership edge
Treat these as high-value targets:
- first ring / descriptor / mailbox entry consumed only on interesting runs
- first socket-read / recv callback / stream-read helper whose output survives into the target parser input
- first reassembly, frame-boundary, or decomultiplexing helper that converts generic inbound bytes into one message-family object
- first queue insertion or dequeue that hands ownership from transport plumbing to protocol-handling logic
- first deferred receive worker, bottom-half, or callback family that consistently precedes parser entry for the target message family
- first buffer ownership transfer or context-slot write that predicts which parser/handler family runs next
- first branch that routes the inbound object into one parser family rather than another

Treat these as useful but often one layer too early:
- raw packet capture alone
- generic NIC/UART/socket activity alone
- interrupt visibility alone
- seeing a candidate parser symbol alone
- broad receive callback enumeration alone

## 5. Practical workflow

### Step 1: Freeze one narrow representative pair
Prefer one disciplined compare pair over a growing collection of captures.

Good pairs include:
- same inbound packet family visible in two runs, but only one reaches the parser/handler of interest
- same wire-visible command under two queue/ring states where only one run commits receive ownership
- same inbound bytes under two transport conditions where only one side reaches a deferred receive worker that predicts later state change
- same external input in rehosted vs more-realistic conditions where only one side reaches the expected parser path

Record only what you need:
- inbound message family identity
- already-visible transport/device activity
- candidate receive queue/ring/callback/worker family
- later visible parse/state difference

If you do not yet have a stable pair, you are still too early for this note.

### Step 2: Mark five boundaries explicitly
Before widening parser or driver taxonomy, mark these five boundaries:

1. **inbound-visibility boundary**
   - first stable external packet / frame / command / mailbox event distinction
2. **transport/device boundary**
   - where the target first shows socket, driver, DMA, interrupt, mailbox, or hardware-facing receive activity
3. **receive-ownership candidate boundary**
   - first likely ring/descriptor consume, buffer handoff, queue dequeue, framing commit, or deferred receive worker that could own the message
4. **parser-feed boundary**
   - first parser / decoder / dispatch entry plausibly fed by that receive owner
5. **proof-of-effect boundary**
   - later parse/state/reply/consequence difference that depends on the candidate receive-ownership edge

This prevents “we saw the packet” or “we found the callback” from being mistaken for “we found the receive owner.”

### Step 3: Prefer first stable ownership transfer over deepest transport semantics
When many callbacks or read helpers exist, prioritize the earliest stable ownership transfer that differs across the pair:
- descriptor consume / ring advance
- receive-buffer handoff
- queue/mailbox dequeue into a protocol object
- framing/reassembly commit
- deferred receive worker entry
- route-to-parser branch

This is usually a better anchor than fully modeling every transport helper first.

### Step 4: Localize the first handoff that predicts parser behavior
After the transport/device boundary, ask:
- where do inbound bytes first stop being generic transport activity and become one parser-relevant owned object?
- where is the first queue/ring/deferred callback only reached on the interesting side?
- where is the first framing or object-construction step that consistently precedes parser entry?
- where is the first ownership transfer whose output survives into one parser/handler family?

Useful local role labels:
- `inbound-visible`
- `transport-read`
- `descriptor/ring`
- `buffer-handoff`
- `frame-commit`
- `queue/dequeue`
- `deferred-rx`
- `parser-feed`
- `route-select`
- `effect-proof`

If a region cannot be given one of these roles, it may still be churn rather than leverage.

### Step 5: Prove the edge with one downstream parser/state consequence
Do not stop at “this looks like the receive callback.”

Prove the candidate edge by tying it to one downstream effect such as:
- the target parser runs only when this queue/deferred-worker/descriptor path is reached
- one state write or reply family appears only after this receive ownership edge
- the same external packet is visible in both runs, but only the run reaching this handoff reaches the expected handler or parser family
- one rehosting failure disappears only when this receive-ownership boundary is modeled correctly
- one stable receive object or buffer family exists only when the later parse/state effect occurs

A weaker but still useful proof is:
- visible traffic exists in both runs, but only one run reaches the candidate receive-ownership edge and later parse consequence.

### Step 6: Hand the result back to one next concrete task
Once localized, route the result into one next task only:
- parser-to-state consequence localization
- replay or harness refinement
- rehosting receive-path modeling
- one narrower static reconstruction target around the receive owner
- queue/ring/framing realism improvement

Do not immediately widen into full driver or transport-stack taxonomy unless the next experiment truly needs it.

## 6. Breakpoint / hook placement guidance
Useful anchor classes:
- first packet/message-family discriminator on the inbound side
- first socket-read / recv / mailbox-read / buffer-fill helper attributable to the target family
- first descriptor consume / ring-advance / DMA-complete path only present on interesting runs
- first framing/reassembly helper that outputs one parser-relevant object
- first queue insertion/dequeue or deferred receive worker that consistently precedes parser entry
- first route-select branch choosing one parser family over another
- first parser entry and first later state/reply effect used as proof boundaries

If traces are noisy, anchor on:
- compare-run divergence around first receive ownership transfer
- queue/ring/deferred-worker activity rather than all driver internals
- framing/object-commit boundaries rather than every buffer copy
- first parser-feed edge rather than full transport-stack understanding

## 7. Failure patterns this note helps prevent

### 1. Mistaking traffic visibility for local ownership
A visible packet or external command is not yet leverage if the local receive owner is still unknown.

### 2. Overcollecting transport traces after a good compare pair already exists
Once one good pair exists, more traffic logs often add breadth without explaining the decisive receive handoff.

### 3. Treating parser suspicion as solved ingress understanding
A parser-looking function is not yet the right target if one earlier queue, framing, or deferred receive owner still decides whether that parser ever sees the message.

### 4. Confusing generic buffering with parser-relevant ownership
A copied buffer is not yet the useful proof boundary if later framing, queue, or receive-owner selection still decides whether the message matters.

### 5. Chasing whole driver taxonomy too early
A partial but proven receive-ownership edge is often enough to unblock parser, replay, harness, or rehosting work.

## 8. Concrete scenario patterns

### Scenario A: Ring/descriptor consume is the real receive owner
Pattern:

```text
same packet visible externally
  -> generic interrupt/read activity appears in both runs
  -> only one run consumes the descriptor into the target receive buffer
  -> parser/state behavior diverges only after that consume edge
```

Best move:
- anchor on the first stable descriptor/ring consume, not broad interrupt labeling

### Scenario B: Framing/reassembly commit is the real handoff
Pattern:

```text
stream bytes arrive
  -> several read callbacks fire
  -> parser is only reached after one frame-commit helper
  -> later behavior depends on that commit, not the raw reads
```

Best move:
- treat the frame-commit or reassembly boundary as the receive owner

### Scenario C: Deferred receive worker is the real protocol owner
Pattern:

```text
inbound message visible
  -> irq/callback/read path looks active
  -> no immediate parser entry seen
  -> one deferred worker later feeds the message into stateful logic
```

Best move:
- treat the deferred worker's first parser-feed or route-select edge as the real ownership boundary

## 9. Relationship to nearby pages
- `topics/protocol-state-and-message-recovery.md`
  - explains the broader message/state recovery family
- `topics/firmware-and-protocol-context-recovery.md`
  - explains when environment/context still dominates the workflow
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
  - use that when the receive owner is already known and the missing edge is now parser-to-state consequence
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
  - use that when replay still fails because the decisive missing edge is now acceptance/state precondition rather than receive ownership
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
  - use that when the missing edge is later on the send/output side rather than the receive/input side
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`
  - use that when the decisive later edge is no longer receive ownership but an interrupt/deferred consequence after peripheral activity

## 10. Minimal operator checklist
Use this note best when you can answer these in writing:
- what is the one inbound message family or compare pair?
- where is the first transport/device activity boundary?
- what is the first candidate receive-ownership edge?
- where is the first parser-feed boundary after it?
- what later effect proves that edge mattered?
- what single next task becomes easier once that edge is known?

If you cannot answer those, the case likely needs a more upstream note first.

## 11. Source footprint / evidence quality note
This note is intentionally workflow-first.

It is grounded by:
- `topics/protocol-state-and-message-recovery.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`
- `sources/firmware-protocol/2026-03-17-protocol-ingress-ownership-and-receive-path-notes.md`

The evidence base here is sufficient for a practical workflow note because the point is not to claim one universal receive architecture.
The point is to normalize a recurring operator move that the KB previously lacked.

## 12. Bottom line
When protocol / firmware RE already has visible inbound traffic and some plausible parser or callback candidates, the next high-value move is sometimes not more traffic collection and not broader driver taxonomy.

It is to localize the first **ingress / receive-path ownership boundary** that actually takes ownership of inbound bytes and turns them into one parser-relevant object, queue entry, deferred receive callback, or routed message whose later parse/state behavior can then be proved.