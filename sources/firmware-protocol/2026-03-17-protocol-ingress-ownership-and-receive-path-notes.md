# Source Notes — Protocol ingress ownership and receive-path workflow

Date: 2026-03-17
Purpose: support a practical protocol / firmware workflow note for the recurring case where packets or bytes are visible on the wire or device side, but the analyst still has not proved which local ingress path actually owns the receive-side handoff into parsing, buffering, dispatch, or later stateful handling.

## Scope
This note does not try to survey all transport architectures.
It consolidates practical signal already present in the KB into one operator-facing workflow frame for a common early-middle bottleneck:

- one message family, packet family, or inbound event is already visible externally
- some parser, state, or reply logic may already be suspected
- but the analyst still has not proved where the relevant inbound bytes first become one locally owned receive object, queue entry, descriptor completion, callback, or parser feed
- the real missing edge is often not more protocol semantics, but the first receive-side ownership boundary such as:
  - DMA/ring/descriptor completion
  - driver callback or socket-read handoff
  - mailbox/queue dequeue into a parser feed
  - ISR/deferred receive worker handoff
  - stream/frame reassembly commit into one message object

## Supporting source signals

### 1. Existing protocol-state workflow already assumes message-family visibility is not enough
From:
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`

High-signal points reused here:
- message visibility is not parser-to-consequence visibility
- one representative compare pair is better than broad trace growth
- the useful target is the first local edge that predicts later behavior

Why it matters:
- some cases stall even earlier than parser-to-state work because the analyst still cannot prove which receive path actually feeds the parser, queue, or state machine for the message family of interest

### 2. Existing firmware/MMIO and ISR notes already separate hardware-side visibility from later consequence ownership
From:
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`

High-signal points reused here:
- the useful edge is often the first local handoff that predicts later durable behavior
- generic peripheral visibility or interrupt visibility is not yet solved ownership
- queue, DMA, interrupt, and deferred-worker boundaries are often more valuable than broader labeling

Why it matters:
- receive-side protocol ownership often sits exactly at that kind of boundary:
  - visible ingress bytes exist
  - one queue/ring/callback/worker family is reachable
  - but the first locally owned receive handoff is still unproved

### 3. Existing replay and reply-emission notes imply a missing earlier sibling on the protocol branch
From:
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`

High-signal points reused here:
- protocol workflows already have strong notes for acceptance gating and send/output-side ownership
- accepted-vs-stalled compare pairs and emitted-vs-not-emitted compare pairs are useful later in the chain

Why it matters:
- there was still no canonical receive-side sibling for the earlier question:
  - before parser/state or replay work deepens, which local ingress path actually owns these bytes and turns them into one parser-relevant receive object?

### 4. Existing mobile/browser ownership notes show a transferable pattern: transport visibility is not the same as consumer ownership
From:
- `topics/cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note.md`
- `topics/mobile-response-consumer-localization-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`

High-signal points reused here:
- network visibility is not the same as local ownership
- the decisive analytical step is often identifying the first consumer or finalization boundary that actually drives later behavior
- compare-run discipline is best anchored on one concrete consumer boundary rather than broad flow narration

Why it matters:
- protocol / firmware receive-side work has the same shape:
  - bytes or frames are visible
  - several callbacks, queues, or wrappers look plausible
  - the decisive step is finding the first local receive owner that actually feeds parse/state behavior rather than only buffering, copying, or generic plumbing

## Distilled practical pattern
A useful workflow pattern for protocol / firmware receive-side ownership stalls is:

```text
inbound bytes / frames / packets visible
  -> transport / device / driver activity visible
  -> several receive callbacks, queues, rings, or workers are plausible
  -> one local receive handoff actually commits bytes into parser-relevant ownership
  -> later parse/state/reply behavior proves that handoff mattered
```

## Operator heuristics to preserve
- Do not assume visible traffic or one likely parser means the receive path is solved.
- Treat these as separate milestones:
  - external inbound visibility
  - transport / device activity visibility
  - receive-path ownership visibility
  - parse visibility
  - parser-to-state / acceptance visibility
  - reply-emission / send visibility
- Prefer one narrow compare pair such as:
  - same inbound message family present on two runs, but only one reaches the parser of interest
  - same wire packet seen in both runs, but only one reaches a queue/deferred-worker family that later predicts state change
  - same receive interrupt/callback family with one ring/descriptor ownership difference and one later parse difference
- Useful local anchors include:
  - first descriptor/ring entry consumed only on interesting runs
  - first socket-read / recv callback or mailbox dequeue that feeds a target buffer family
  - first reassembly/frame-commit helper that turns stream bytes into one message object
  - first deferred receive worker or parser-feed callback reached only when the message family of interest is really consumed
  - first buffer ownership transfer, queue insertion, or parser invocation that consistently precedes the later parse/state consequence
- If multiple receive helpers fire, prefer the first one whose output survives into parser input or one stable receive object, not the broadest driver or ISR catalog.
- If parser visibility is intermittent or misleading, suspect receive-side ownership differences such as:
  - descriptor/ring exhaustion
  - wrong queue or mailbox family
  - deferred worker fan-out
  - framing/reassembly drift
  - pending-slot ownership
  before assuming the parser model itself is incomplete.

## Candidate canonical KB mapping
This note most directly supports:
- `topics/protocol-ingress-ownership-and-receive-path-workflow-note.md`

It also strengthens:
- `topics/protocol-state-and-message-recovery.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`

## Bottom line
Some protocol / firmware cases do not really unblock when the analyst finds visible traffic, a likely parser, or even one promising callback family.
They unblock when the analyst proves which local ingress / receive-path boundary actually takes ownership of inbound bytes and turns them into one parser-relevant object, queue entry, deferred callback, or receive-state transition that predicts the later behavior.