# Source Notes — Peripheral / MMIO effect-proof workflow

Date: 2026-03-16
Purpose: support a practical firmware/protocol workflow note for the recurring case where peripheral ranges, MMIO handlers, or register families are already partly visible, but the first behavior-changing hardware-side consequence is still unproved.

## Scope
This note does not try to survey all firmware reversing.
It consolidates practical signal already present in the KB and source set into one operator-facing workflow frame for a common firmware bottleneck:

- candidate MMIO ranges, register handlers, or peripheral families are already visible
- parser or command-routing logic may also be partly visible
- but analysis still stalls because the first hardware-side consequence is not yet localized cleanly
- the key uncertainty is whether the decisive edge is really:
  - one register write that changes peripheral state
  - one queue / DMA / interrupt-arm boundary
  - one reply/status update only indirectly caused by hardware state
  - or merely nominal register-label visibility without proved behavioral consequence

## Supporting source signals

### 1. Existing firmware/context synthesis already frames hidden mappings and used-context recovery as central
From:
- `topics/firmware-and-protocol-context-recovery.md`
- `sources/datasets-benchmarks/2026-03-14-firmware-protocol-context-notes.md`

High-signal points reused here:
- firmware RE often stalls on limited hardware knowledge rather than only poor code recovery
- AutoMap-style work highlights hidden memory mappings between peripheral registers as a prerequisite layer of understanding
- ProtoReveal-style framing emphasizes access chains, in-use peripherals, and downstream rehosting utility rather than nominal hardware completeness
- used-vs-unused context discrimination matters because false context is expensive

Why it matters:
- this supports a practical note that starts after peripheral visibility exists, but before the analyst has proved which MMIO/register edge actually predicts later behavior

### 2. Existing protocol workflow logic already normalizes parser visibility vs consequence visibility
From:
- `topics/protocol-state-and-message-recovery.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`

High-signal points reused here:
- the useful target is often the first consequence-bearing edge, not parser visibility alone
- first stable fan-out is often more valuable than deepest field semantics
- queue/timer insertion, reply-family selection, and deferred work are common real leverage points

Why it matters:
- firmware/peripheral cases need the hardware-side sibling of the same logic:
  parser or register visibility is not enough if the first MMIO/peripheral effect is still unproved

### 3. Existing native/runtime workflow notes reinforce consequence-first proof discipline
From:
- `topics/native-interface-to-state-proof-workflow-note.md`
- `topics/runtime-behavior-recovery.md`

High-signal points reused here:
- one representative path is often better than broad subsystem browsing
- the first durable state write or ownership handoff is often the best proof target
- runtime evidence is most useful when it confirms one narrow hypothesis rather than replacing structure wholesale

Why it matters:
- firmware work also benefits from a compact proof discipline:
  one command family -> one MMIO/register edge -> one visible hardware-side or state-side consequence

## Distilled practical pattern
A useful firmware/peripheral workflow pattern is:

```text
candidate peripheral family becomes visible
  -> freeze one representative command / message / trigger pair
  -> localize first MMIO/register family or peripheral dispatch edge
  -> separate nominal register visibility from one effect-bearing write or arm
  -> prove one downstream consequence
  -> only then broaden rehosting, field recovery, or peripheral modeling
```

## Operator heuristics to preserve
- Do not stop at naming a peripheral or register block.
- Treat these as separate milestones:
  - MMIO/range visibility
  - register-role hypothesis
  - first effect-bearing write / arm / queue edge
  - later proof-of-effect boundary
- Prefer one representative pair with one changed command/state condition over a growing pile of half-labeled register accesses.
- Useful early anchors include:
  - first write to a register family that differs across the pair
  - first mask/bitfield reduction that predicts later state
  - first queue/DMA/interrupt-arm helper reached only on one side
  - first status/reply/peripheral behavior proving the hardware-side edge mattered
- If a register family is visible in many runs but no later behavior changes, downgrade confidence that it is the decisive edge.
- If rehosting or fuzzing still fails after apparent peripheral labeling success, suspect that the first useful proof target is one effect-bearing write or deferred arm that has not yet been isolated.

## Candidate canonical KB mapping
This note most directly supports:
- `topics/peripheral-mmio-effect-proof-workflow-note.md`

It also strengthens:
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`

## Bottom line
The firmware/protocol branch does not mainly need another abstract child page right now.
It needs a practical entry note for the common case where the analyst already sees candidate peripheral ranges, register handlers, or MMIO families, but still cannot tell which first effect-bearing write, arm, queue, or status-changing edge actually matters enough to guide the next experiment confidently.
