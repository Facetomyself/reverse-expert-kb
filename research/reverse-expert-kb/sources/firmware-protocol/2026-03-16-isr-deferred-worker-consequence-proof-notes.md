# Source Notes — ISR / deferred-worker consequence-proof workflow

Date: 2026-03-16
Purpose: support a practical firmware/protocol workflow note for the recurring case where command families, MMIO/register paths, or peripheral-facing helpers are already partly visible, but the first decisive behavior change only becomes clear at an ISR, deferred worker, bottom-half/tasklet, workqueue, or completion-callback boundary.

## Scope
This note does not try to survey interrupt-driven firmware design in general.
It consolidates practical signal already present in the KB into one operator-facing workflow frame for a common firmware bottleneck:

- parser or command-routing visibility already exists
- candidate MMIO/peripheral effect-bearing writes may also already exist
- yet the case still stalls because the visible write is not the first trustworthy consequence boundary
- the real decisive edge may instead be:
  - an interrupt enable / ack path
  - an ISR entry that consumes or latches the earlier hardware-side effect
  - a deferred worker or queue callback that turns hardware completion into policy-visible behavior
  - a bottom-half or scheduler edge that performs the first stable state reduction

## Supporting source signals

### 1. Existing firmware/context synthesis already frames downstream utility and used-context recovery as central
From:
- `topics/firmware-and-protocol-context-recovery.md`
- `sources/datasets-benchmarks/2026-03-14-firmware-protocol-context-notes.md`

High-signal points reused here:
- firmware RE often stalls on missing environmental understanding rather than only code readability
- used-context recovery matters more than nominal hardware completeness
- rehosting/fuzzing value depends on identifying which environmental edges actually affect behavior

Why it matters:
- once MMIO visibility exists, the next real leverage point may be the first interrupt/deferred consequence edge rather than broader peripheral labeling

### 2. Existing peripheral/MMIO workflow logic already separates visibility from effect proof
From:
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`

High-signal points reused here:
- register or parser visibility is not the same as behavior-changing consequence visibility
- queue/timer/retry/deferred work is often the real leverage point
- one representative compare pair is better than wider but shallower trace collection

Why it matters:
- some firmware cases remain ambiguous even after the first MMIO write is isolated because the real proof target is the first ISR/deferred worker that converts that write or completion into durable state or reply behavior

### 3. Existing runtime/proof-oriented notes reinforce consequence-first proof discipline
From:
- `topics/runtime-behavior-recovery.md`
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`
- `topics/native-interface-to-state-proof-workflow-note.md`

High-signal points reused here:
- the useful move is often to localize one causally predictive edge instead of narrating an entire subsystem
- deferred work, callback families, and downstream emitters are often better proof targets than upstream visibility alone
- one proved boundary should hand the analyst to one smaller next task

Why it matters:
- ISR/deferred-worker firmware cases fit the same cross-KB pattern: visible structure exists, but the analyst still needs the first consequence-bearing handoff

## Distilled practical pattern
A useful interrupt-driven firmware workflow pattern is:

```text
command / state trigger visible
  -> MMIO/peripheral path partly visible
  -> candidate write or arm exists
  -> ISR / deferred worker / completion callback consumes that condition
  -> one durable state/reply/scheduler effect proves the real consequence boundary
```

## Operator heuristics to preserve
- Do not assume the first MMIO write is the best proof boundary if the visible behavioral change only appears after interrupt or deferred-work handling.
- Treat these as separate milestones:
  - trigger visibility
  - MMIO/peripheral effect candidate
  - interrupt/ack/arm boundary
  - ISR/deferred-worker consequence boundary
  - later proof-of-effect boundary
- Prefer one representative compare pair with one changed trigger/state condition over broad logging of every interrupt path.
- Useful anchors include:
  - first interrupt enable/ack/mask path differing across the pair
  - first ISR entry only reached on the interesting side
  - first deferred worker/tasklet/workqueue callback that performs a meaningful state write or reply-family selection
  - first completion/status/reply edge proving the ISR/deferred path mattered
- If the MMIO write appears in both runs but only one run reaches the later deferred worker or durable state change, downgrade confidence that the write alone is the decisive proof target.
- If rehosting still fails after modeling registers or basic peripheral transitions, suspect that the missing minimal model is the completion/interrupt/deferred consequence edge rather than the register map itself.

## Candidate canonical KB mapping
This note most directly supports:
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`

It also strengthens:
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/runtime-behavior-recovery.md`

## Bottom line
Some firmware cases do not really unblock when the analyst finds the first MMIO/peripheral write.
They unblock when the analyst proves which ISR, deferred worker, completion callback, or bottom-half path turns that earlier hardware-facing edge into the first durable state, reply, scheduler, or policy consequence that can guide the next experiment confidently.
