# Descriptor consumed-vs-reclaim and slot-return notes

Date: 2026-03-27
Branch: protocol / firmware practical branch
Seam: completion visibility / consumption proof vs reclaim / slot-return proof

## Why this note exists
A recurring practical mistake in descriptor-, virtqueue-, completion-ring-, and CQE-shaped cases is stopping too early at one of these weaker proof objects:
- completion bytes became visible
- used entry or CQE is readable
- callback says a request finished
- interrupt or wakeup happened

Those facts matter, but they still do not automatically prove the stronger thing many later workflows need:
- the representative slot is now actually consumed and returned for reuse
- the ownership contract really crossed back
- later reuse/reclaim proof exists rather than only one momentary completion observation

This note preserves a practical stop rule:
- `published != notified != completion-visible != consumed != reclaimed/reusable`

The strongest practical addition this run is the narrower split:
- `completion-visible != slot-returned`

That matters because many cases only become trustworthy for replay, emulation, or harnessing after the analyst freezes one reclaim/seen/head-advance/reuse boundary rather than stopping at completion visibility.

## Conservative retained takeaways from sources
### 1. Virtio split queues preserve a real used-ring return boundary
From the virtio material and explanatory implementations/docs:
- the driver publishes descriptor heads in the avail ring
- the device later adds an entry in the used ring and increments used idx
- used-buffer notification is separate from the used-ring update itself
- descriptor ownership and notification suppression are separate concerns

Operator meaning:
- seeing a used entry or interrupt is not yet the same as proving the driver-side reclaim path that makes the slot durably reusable in the analyst’s case

### 2. io_uring preserves an explicit seen/advance boundary
The `io_uring_cqe_seen(3)` man page states that completions must be marked as consumed so their slot can get reused.

Operator meaning:
- completion retrieval and completion-slot reuse are explicitly not the same proof object
- a practical ring/CQE stop rule can therefore preserve `completion observed != slot reusable`

### 3. Practical queue implementations often separate completion visibility from later notification policy and later reuse
The rust-vmm virtio queue README and Red Hat virtqueue explanation both preserve distinct roles for:
- descriptor publication
- notify policy
- device adding used entries
- later notification back to the driver

Operator meaning:
- notification behavior should not be flattened into completion truth
- completion truth should not be flattened into reclaim / reuse truth

## Practical operator rule added to branch memory
When a descriptor- or CQ-shaped case is already good enough to show completion visibility, the next most valuable question is often not “did completion happen?”
It is:
- who still owns the representative slot right now?
- what exact API/helper/index write marks the completion as consumed?
- what exact head/seen/reclaim/free/reuse step returns the slot to a reusable state?
- which later compare-run difference first depends on that return?

Compact shorthand worth preserving:
- `published != notified != completion-visible != consumed != reclaimed/reusable`
- especially: `completion-visible != slot-returned`

## Good continuation targets this supports
This seam is especially useful when the next task is:
- proving truthful queue ownership for replay or emulation
- avoiding false “done” claims in interrupt/callback-heavy traces
- explaining why a ring stalls even though completion bytes are visible
- localizing whether the missing realism is consumer-side seen/advance, reclaim, or later slot reuse

## Sources used conservatively
- Virtio 1.1 spec: https://docs.oasis-open.org/virtio/virtio/v1.1/csprd01/virtio-v1.1-csprd01-diff.html
- rust-vmm virtio-queue README: https://github.com/rust-vmm/vm-virtio/blob/main/virtio-queue/README.md
- Red Hat virtqueue explanation: https://www.redhat.com/en/blog/virtqueues-and-virtio-ring-how-data-travels
- io_uring_cqe_seen(3): https://man7.org/linux/man-pages/man3/io_uring_cqe_seen.3.html

## Evidence quality note
This is a workflow-oriented source note, not a claim that all queues share one exact reclamation API.
The retained point is narrower and safer:
- completion visibility, completion consumption, and slot reuse are often different proof objects
- practical RE workflows should stop on the smallest one that actually matters for the next experiment
