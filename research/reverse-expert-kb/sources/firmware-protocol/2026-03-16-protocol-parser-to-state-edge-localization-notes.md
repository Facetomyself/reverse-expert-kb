# Source Notes — 2026-03-16 — Protocol Parser-to-State Edge Localization

## Why this source note exists
This note supports a practical firmware/protocol workflow gap in the KB.

The KB already had solid synthesis for:
- firmware context recovery
- protocol field and message recovery
- protocol state-machine recovery

But it was still thinner on one recurring operator problem:

```text
I already have traces, packet families, or candidate handlers.
I do not need more generic protocol taxonomy.
I need to localize the first parser / state / consequence edge
that actually changes protocol behavior.
```

The goal here is not to produce a new abstract protocol hierarchy.
It is to support a workflow note for the moment after:
- traffic families are visible
- message clusters are partly known
- some parsing or dispatch code is already suspected
- but the first consequence-bearing state write, transition gate, or reply-selection branch is still unclear

## Existing source anchors used
### 1. ProtoReveal / firmware context recovery notes
From:
- `sources/datasets-benchmarks/2026-03-14-firmware-protocol-context-notes.md`
- `topics/firmware-and-protocol-context-recovery.md`

Operational value for the KB:
- reinforces that firmware/protocol RE is often blocked by missing context, not only unreadable code
- supports looking for **used** context and **used** protocol behavior rather than modeling everything nominally present
- encourages access-chain thinking: which peripheral/message path actually feeds one real protocol consequence?

### 2. BinPRE / protocol field inference notes
From:
- `sources/datasets-benchmarks/2026-03-14-firmware-protocol-context-notes.md`
- `topics/protocol-state-and-message-recovery.md`

Operational value for the KB:
- reinforces that field inference alone is not enough
- supports separating:
  - format visibility
  - field-role hypotheses
  - the first code edge that turns parsed material into behavior
- useful for reminding the analyst not to stop at "we found the parser"

### 3. State-machine inference notes
From:
- `sources/datasets-benchmarks/2026-03-14-firmware-protocol-context-notes.md`
- `topics/protocol-state-and-message-recovery.md`

Operational value for the KB:
- reinforces that protocol understanding is incomplete without transition logic
- supports treating state updates, dispatch tables, gate checks, and reply-family selection as first-class localization targets

### 4. BinaryInferno / false-positive-cost framing
From:
- `sources/datasets-benchmarks/2026-03-14-firmware-protocol-context-notes.md`
- `topics/protocol-state-and-message-recovery.md`

Operational value for the KB:
- reinforces that wrong field or state assumptions are expensive downstream
- supports a workflow bias toward the **first consequence-bearing edge** rather than wide speculative semantic labeling

### 5. Practitioner source cluster
From:
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`

Operational value for the KB:
- reinforces that real protocol RE often lives inside app signing, websocket/JCE traffic, risk-control exchange, and stateful replay work
- supports a practical workflow where traces, hooks, and message mutation are used to prove which state edge matters before attempting complete protocol formalization

## Practical synthesis taken from the source cluster
The most useful way to normalize the source material is:

```text
message family visible
  -> candidate parser / decoder / dispatch region visible
  -> parsed object or field roles partly visible
  -> one state write / gate / reply-selection edge actually changes behavior
  -> later transition, request family, or emitted reply proves the edge mattered
```

The strongest reusable insight is:
- **parser visibility is not protocol understanding**
- the more useful target is often the first local edge that turns decoded bytes into:
  - state transition
  - capability gate
  - reply-family choice
  - timer/retry arm
  - queue insertion
  - peripheral action

## Concrete localization anchors suggested by the source cluster
These are workflow anchors, not claims about one universal implementation:
- first stable message-family discriminator
- first length/opcode/session-id check that survives compare-run testing
- parsed-structure construction boundary
- switch / jump-table / callback-dispatch edge keyed by message type or state
- first write into connection/session/context structure after parse
- first branch that selects reply family, retry path, or queue insertion
- first peripheral/MMIO write or scheduler action attributable to one message family
- first downstream emitted packet or state-observable effect that only appears when that edge is taken

## Compare-run patterns worth preserving
### 1. Good packet-family visibility does not prove the decisive edge is known
If packet clustering is already clean, the unresolved bottleneck may still be:
- parser fan-out
- message-type normalization
- state-guard branch
- deferred queue/retry insertion
- reply-family selection

### 2. Parsed-object visibility can still be one layer too early
Even when fields or structures are visible, the real leverage may only begin at:
- the first state write
- the first transition-table lookup
- the first capability/phase gate
- the first handler that emits a reply or triggers a peripheral effect

### 3. More traffic often adds noise once the key family is already isolated
Once one representative success/failure pair exists, the higher-value move is often:
- localize the first consequence-bearing parser/state edge
- not collect a wider but shallower corpus of near-duplicate sessions

## How this source note should influence KB structure
This cluster argues for a concrete page such as:
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`

That page should emphasize:
- target pattern / scenario
- compare-run discipline
- parse-boundary vs consequence-boundary separation
- breakpoint / hook placement
- state-write and reply-selection localization
- proof that one localized edge actually predicts later behavior

## Limits of current evidence
- current evidence is more synthesis- and workflow-driven than source-dense
- the strongest anchors come from existing KB protocol/firmware material plus practitioner signals, not a brand-new paper sweep
- that is still sufficient for a practical workflow note because the purpose here is to turn an already-supported branch into a more usable operator playbook

## Bottom line
The useful analyst object here is not "the parser" in the abstract.
It is the concrete path from **message-family visibility to the first consequence-bearing parser/state edge** that actually predicts protocol behavior, transition, reply choice, or hardware effect.
