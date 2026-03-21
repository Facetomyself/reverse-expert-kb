# Reverse KB Autosync Run Report — 2026-03-21 23:20 CST

Mode: external-research-driven

## Summary
This run intentionally avoided another small internal canonical-sync-only pass.

Recent runs were already strong on internal branch maintenance, so this cycle prioritized an underfed but still practical protocol / firmware seam: the point where accepted local output handling becomes a descriptor/ring publish edge, and where later completion / ISR / deferred reduction proves that the earlier publish actually mattered.

The result was a new practical continuation page:
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`

plus a supporting source note:
- `sources/firmware-protocol/2026-03-21-descriptor-tail-kick-and-completion-chain-notes.md`

and branch-memory synchronization so the protocol / firmware subtree now remembers this seam explicitly rather than forcing analysts to jump directly from reply-emission into generic MMIO or generic ISR reasoning.

## Direction review
Recent protocol / firmware work had already covered:
- output handoff
- MMIO effect proof
- ISR/deferred consequence proof

But there was still a practical operator gap between them for descriptor-driven or ring-driven systems.

Without preserving that seam, the branch risked recurring analyst mistakes:
- stopping at reply-object construction instead of the first publish-to-hardware edge
- treating descriptor field visibility as equivalent to descriptor commit
- treating interrupt visibility as enough without tying it back to one earlier publish edge
- widening ring/DMA taxonomy before one trustworthy publish-to-consequence chain existed

This run therefore stayed practical and case-driven by adding a workflow note specifically about:
- descriptor preparation vs descriptor publication
- producer/tail/owner/doorbell/notify as likely commit boundaries
- later completion/ISR/deferred reduction as proof that the earlier publish mattered

## Branch-balance review
Bias this run intentionally toward a thinner protocol / firmware branch instead of denser browser/mobile maintenance.

Why this branch:
- browser/mobile and protected-runtime leaves are already easy to overfeed
- protocol / firmware practical branch had strong neighboring notes, but this concrete seam was still missing as a named operator move
- adding it increases practical ladder fidelity rather than just leaf count

Net branch effect:
- protocol / firmware branch becomes more internally continuous from:
  - reply-emission / transport handoff
  - to descriptor publish / completion chain
  - to MMIO effect proof
  - to ISR/deferred consequence proof

## External research performed
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries:
1. `firmware reverse engineering mmio effect proof interrupt deferred worker workflow`
2. `embedded firmware interrupt bottom half workqueue reverse engineering consequence proof`
3. `protocol reverse engineering dma ring buffer descriptor transmit completion workflow`

## Search audit
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- exa
- tavily
- grok

Failed sources:
- none

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Execution note:
- search itself was not degraded; all requested sources were invoked successfully
- direct `web_fetch` extraction for PDF-backed sources was still degraded/raw in this environment, so those PDFs were used conservatively and mainly as directional support unless the search-layer snippets already carried the needed claim

## Newly discovered / emphasized information
- The KB needed an explicit workflow note for the seam between output-side proof and hardware-side proof in descriptor-driven systems.
- The practical boundary that matters is often not descriptor fill and not interrupt visibility, but the chain:
  - prepare
  - publish/kick
  - complete
  - reduce consequence
- A good proof object is often one compare pair around publish-vs-no-publish, not a complete recovered ring schema.
- Producer/tail/doorbell/owner/notify changes are often better publish anchors than broad descriptor-field narration.
- Completion often becomes behaviorally useful only in a later ISR/deferred-worker reduction rather than at interrupt visibility alone.

## Deduplicated / already-known information reused
- Existing protocol / firmware pages already strongly supported:
  - reply-emission / transport handoff
  - MMIO effect proof
  - ISR/deferred consequence proof
- Existing branch logic already favored proving one consequence-bearing edge instead of cataloging broad taxonomy.
- Existing source base already supported cautious effect-first reasoning for MMIO-heavy and firmware-heavy cases.

## Source-backed synthesis
The most useful synthesis from this run is:
- descriptor-driven systems repeatedly create a late-stage analyst seam where local protocol acceptance is already visible, but the first trustworthy output-side proof is actually the publish-to-hardware edge rather than the earlier object build
- the next trustworthy proof is then the first completion-side reduction that demonstrates durable software consequence

That justified preserving a dedicated workflow note rather than burying the idea inside:
- `protocol-reply-emission-and-transport-handoff-workflow-note`
- `peripheral-mmio-effect-proof-workflow-note`
- `isr-and-deferred-worker-consequence-proof-workflow-note`

## KB changes made
Added:
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`
- `sources/firmware-protocol/2026-03-21-descriptor-tail-kick-and-completion-chain-notes.md`

Updated:
- `topics/protocol-firmware-practical-subtree-guide.md`
  - inserted descriptor publish / completion-chain routing as a distinct branch step
  - adjusted ladder and routing guidance so output-handoff no longer jumps directly to generic MMIO/ISR notes
- `index.md`
  - added the new workflow note to the protocol / firmware branch listing
  - added branch-summary language so the new seam is visible at top-level branch memory

## Practical operator value added
This run added a reusable answer to a concrete stuck state:
- "I can see the reply path and I can see the ring, but what is the smallest trustworthy proof object now?"

The preserved answer is:
- prove one descriptor publish edge
- tie it to one completion-side durable consequence
- only then widen toward MMIO realism, ISR modeling, or richer ring taxonomy

That is more practical than another wording pass or another family-count/index sync.

## Files changed
- `index.md`
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`
- `sources/firmware-protocol/2026-03-21-descriptor-tail-kick-and-completion-chain-notes.md`

## Commit / sync plan
If the working tree validates cleanly:
1. commit KB changes
2. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
3. leave this report as the archival record for the run

## Next directions
Prefer one of these in upcoming protocol / firmware external-research-driven runs:
- a concrete case-driven continuation around mailbox publish / completion semantics when the target is not ring/DMA-centric
- a narrower receive-side counterpart if the branch starts to overweight output-side continuations
- one source-backed workflow note on model realism / rehosting failure diagnosis once publish and completion are already proved but behavior is still close-but-wrong

Avoid next run drift into:
- small wording-only sync passes
- branch-count/index-only repair
- adding another dense browser/mobile leaf unless branch-balance truly demands it
