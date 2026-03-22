# Reverse Expert KB Autosync Run Report — 2026-03-22 22:16 Asia/Shanghai

Mode: external-research-driven

## Summary
This run deliberately avoided another dense-branch wording/index-only polish pass.
Recent autosync history already included substantial protected-runtime, malware, native GUI, opaque-predicate, and iOS-focused work, plus some internal canonical-sync behavior. To satisfy the anti-stagnation rule, this run performed a real external multi-source search pass and used it to strengthen a thinner practical branch inside the protocol / firmware subtree.

The concrete target was the gap between:
- broad mailbox/doorbell publish-completion proof
- broad descriptor tail/kick completion proof
- later MMIO effect or ISR/deferred consequence proof

The KB was still relatively light on the narrower operator seam where a descriptor or completion record is already visible, but the real missing leverage is:
- when ownership actually transfers
- when the other side may trust the record
- how ordering/cache visibility affects that trust boundary
- what reclaim/slot reuse proves durable completion

## Branch-balance / direction review
Recent run shape before this pass:
- protected-runtime and iOS branches received multiple practical additions
- malware and native branches also saw recent maintenance
- protocol / firmware had useful practical notes, but this specific ownership/visibility/reclaim seam was still thinner than the surrounding output-handoff and mailbox/descriptor notes

Direction review result:
- chose a thinner protocol / firmware continuation point instead of another dense-branch polish pass
- prioritized a case-driven workflow note rather than top-level wording or family-count sync
- kept the addition practical and operator-facing, consistent with the KB rule to prefer concrete continuation value over abstract taxonomy expansion

## Work performed
### 1. External research pass
Ran explicit multi-source search through the local `search-layer` skill with requested sources:
- exa
- tavily
- grok

Query set:
- `firmware mailbox doorbell ring buffer completion interrupt reverse engineering workflow`
- `descriptor ring tail doorbell completion chain driver firmware reverse engineering`
- `dma ring completion interrupt ownership reverse engineering practical workflow`

Captured raw search output at:
- `sources/protocol-and-network-recovery/2026-03-22-descriptor-doorbell-search-layer.txt`

### 2. Reviewed nearby KB branch surfaces
Reviewed existing protocol / firmware notes to avoid duplicating already-fed branches:
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- `topics/mailbox-doorbell-command-completion-workflow-note.md`
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`

### 3. Added source-backed practical continuation note
Created:
- `topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md`

This new note centers the practical chain:
- prepare
- publish
- observe
- consume
- reclaim
- prove consequence

It explicitly tells analysts to preserve:
- side-of-ownership labels
- publish vs visibility vs interrupt boundaries
- cache/order pitfalls when they explain divergence
- reclaim/slot reuse as durable proof instead of stopping at generic completion visibility

### 4. Added run-specific source notes
Created:
- `sources/protocol-and-network-recovery/2026-03-22-descriptor-ownership-transfer-and-completion-visibility-notes.md`

This source note records:
- why the branch was chosen
- what the external sources actually supported
- the conservative takeaways used for the new practical page
- a required Search audit section

### 5. Integrated the new page into KB routing surfaces
Updated:
- `topics/protocol-firmware-practical-subtree-guide.md`
- `index.md`

Integration changes included:
- adding the new page to protocol / firmware branch navigation lists
- promoting descriptor ownership-transfer / completion-visibility to an explicit subtree bottleneck family
- adding routing guidance for when to choose the new note versus mailbox/doorbell, broad descriptor-tail, MMIO-effect, or ISR/deferred-consequence notes
- updating the top-level index description so the new note is not orphaned

## Practical value added
This run improves the KB for cases like:
- “the completion bytes are present, but software still does not act on them”
- “the publish/tail edge exists, but the trust boundary is still unclear”
- “interrupts fire, but reclaim or slot reuse never happens”
- “the model has the queue shape right, but ordering/cache/ownership semantics are still wrong”

That is materially more practical than another internal wording-only sync.

## Files changed
Created:
- `topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md`
- `sources/protocol-and-network-recovery/2026-03-22-descriptor-ownership-transfer-and-completion-visibility-notes.md`
- `sources/protocol-and-network-recovery/2026-03-22-descriptor-doorbell-search-layer.txt`
- `runs/2026-03-22-2216-descriptor-ownership-visibility-autosync.md`

Updated:
- `topics/protocol-firmware-practical-subtree-guide.md`
- `index.md`

## Commit / sync
Planned for this run:
- commit only reverse-KB files related to this autosync pass
- run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh` after the commit

## Search audit
Requested sources: exa, tavily, grok
Succeeded sources: exa, tavily, grok
Failed sources: none

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

## Notes
- This run counts as a real external-research-driven pass for the rolling 6-hour anti-stagnation window because all three requested search sources were actually invoked successfully.
- `.learnings/ERRORS.md` logging remained best-effort only and was not treated as a blocker.
