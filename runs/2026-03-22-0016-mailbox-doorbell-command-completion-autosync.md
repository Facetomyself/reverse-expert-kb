# Reverse KB Autosync Run Report — 2026-03-22 00:16 CST

Mode: external-research-driven

## Summary
This run deliberately avoided another small internal branch-sync / wording-only pass.

Recent protocol / firmware autosync work had already improved neighboring output-side and descriptor-side notes, so this cycle prioritized a still-practical but thinner seam inside the same branch: mailbox-style command publish / completion proof.

The result was a new practical continuation page:
- `topics/mailbox-doorbell-command-completion-workflow-note.md`

plus a supporting source note:
- `sources/firmware-protocol/2026-03-22-mailbox-doorbell-command-completion-notes.md`

and branch-memory synchronization in:
- `topics/protocol-firmware-practical-subtree-guide.md`
- `index.md`

so the firmware/protocol ladder now preserves an explicit continuation between:
- reply-emission / transport handoff
- mailbox/doorbell command publish-completion proof
- broader descriptor publish / completion proof
- peripheral/MMIO effect proof
- ISR/deferred consequence proof

## Direction review
Recent runs had already strengthened nearby protocol / firmware seams:
- reply-emission / transport handoff
- descriptor publish / completion chain
- peripheral/MMIO effect proof
- ISR/deferred consequence proof

That made this branch healthier, but it also exposed a narrower operator gap:
- many real firmware cases are command/mailbox-shaped before they need fully general descriptor/ring/MMIO treatment
- accepted local output handling is often already visible
- yet analysts still stall because they have not isolated the smaller chain between:
  - command staging
  - tail/doorbell/submit publication
  - request-linked completion or ack
  - durable software-side reduction

Without preserving that seam explicitly, the KB risks recurring analyst mistakes:
- stopping at command-object construction instead of the first peer-visible publish edge
- treating raw interrupt visibility as enough without request-linked completion proof
- widening into broad ring/register taxonomy before one publish→completion chain is trustworthy
- skipping the useful role of command ID / slot / sequence continuity as the cheapest proof object

This run therefore stayed practical and case-driven by adding a dedicated workflow note for the mailbox/doorbell continuation seam rather than only polishing branch wording.

## Branch-balance review
Bias this run intentionally toward the protocol / firmware practical branch again, but not toward another dense-branch wording cleanup.

Why this still counted as balanced:
- the target branch was still thinner than browser/mobile leaves in practical command-channel coverage
- the new page is a distinct operator continuation, not a synonym of the descriptor note
- it extends the branch in a practical direction rather than adding abstract taxonomy

Why this target specifically:
- yesterday's descriptor-tail note was broader and more generic
- this run narrowed into a mailbox/doorbell command workflow that appears often in host↔firmware channels, accelerator drivers, and embedded command processors
- this preserves a more case-driven ladder instead of forcing analysts to jump from accepted output straight into generic MMIO or generic descriptor thinking

Net branch effect:
- protocol / firmware branch now reads more continuously from:
  - output handoff
  - to mailbox publish/completion
  - to broader descriptor publish/completion
  - to MMIO effect proof
  - to ISR/deferred consequence proof

## External research performed
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries:
1. `firmware mailbox command completion acknowledgment workflow reverse engineering`
2. `embedded mailbox doorbell interrupt completion ring buffer workflow`
3. `command queue mailbox reply interrupt firmware driver completion workflow`

Follow-up source pulls used `web_fetch` on selected references surfaced by the search pass.

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
- search execution itself was not degraded; all requested sources were actually invoked successfully
- some fetched pages were truncated by extractor limits, so synthesis stayed conservative and workflow-level rather than overclaiming implementation specifics

## Newly discovered / emphasized information
- The KB needed a dedicated mailbox/doorbell continuation note between reply-emission and broader descriptor/MMIO proof.
- Mailbox-shaped command channels repeatedly expose a smaller chain that matters more than broad register narration:
  - command stage
  - tail/doorbell/submit publish
  - request-linked completion/ack
  - durable software reduction
- Command ID / slot / sequence continuity is often the cheapest trustworthy request→completion proof object.
- Interrupt visibility alone is weaker than a completion entry, ack object, waiter wakeup, or slot-reuse path tied back to one earlier publish edge.
- Read-to-clear and status-clear behavior can be part of the proof chain instead of mere cleanup noise.
- This seam is practical enough to deserve its own workflow note instead of being buried inside the descriptor or MMIO pages.

## Deduplicated / already-known information reused
- Existing branch logic already strongly supported:
  - accepted output-side proof before hardware-side widening
  - descriptor publish / completion reasoning
  - MMIO effect-first reasoning
  - ISR/deferred consequence proof
- Existing KB pages already favored one consequence-bearing compare pair over broad taxonomy growth.
- Prior protocol / firmware pages already made clear that locally visible objects are not the same as committed hardware-visible ownership.

## Source-backed synthesis
The most useful synthesis from this run is:
- many firmware command channels are easiest to reverse not by recovering the entire mailbox/register map first, but by proving one narrow publish→completion chain
- the most reusable anchors are often:
  - tail/doorbell/submit/owner writes
  - command ID / slot continuity
  - completion queue entries or ack records
  - later waiter/callback/slot-reuse reduction
- this is a practical continuation stage that naturally sits after broad reply/output handoff proof and before broader descriptor/MMIO/interrupt consequence work

That justified preserving a dedicated workflow page instead of only expanding:
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`

## KB changes made
Added:
- `topics/mailbox-doorbell-command-completion-workflow-note.md`
- `sources/firmware-protocol/2026-03-22-mailbox-doorbell-command-completion-notes.md`
- `runs/2026-03-22-0016-mailbox-doorbell-command-completion-autosync.md`

Updated:
- `topics/protocol-firmware-practical-subtree-guide.md`
  - inserted mailbox/doorbell publish-completion routing as a distinct branch step
  - updated branch-family count and routing language
- `index.md`
  - synced firmware/protocol branch listing and branch description to include the new mailbox continuation page

## Practicality check
This run improved the KB itself rather than just collecting raw notes.

Why this is practical:
- the new page is an operator workflow note, not only source capture
- it preserves concrete compare-pair and breakpoint placement tactics
- it gives analysts a named continuation point for real mailbox/command-queue cases
- it keeps the branch case-driven by focusing on publish/completion proof, not abstract queue taxonomy

## Anti-stagnation check
This run satisfies the anti-stagnation rule.

Why:
- it performed a real external-research-driven pass with explicit `exa,tavily,grok` invocation
- it did not stop at internal wording/index-only maintenance
- it produced a materially new practical continuation page on a still-underfed branch seam
- it avoided spending this cycle on small family-count or canonical-sync-only repairs

## Commit / sync actions
Planned workflow for this run:
1. commit KB changes if any
2. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh` after committing KB changes

If commit or sync fails, record it conservatively and leave the KB edits intact.

## Next research directions
Best follow-on directions from here:
1. Add one concrete firmware case note where mailbox publish/completion proof is demonstrated against a real driver/firmware pair.
2. Continue pressure on thinner protocol / firmware leaves instead of looping on branch wording.
3. If the next external pass stays in this branch, prefer either:
   - one command-ID / slot-reuse case note
   - one completion-queue drain / waiter-wakeup continuation note
   - or one practical rehosting/harness page that uses a newly proved mailbox publish/completion chain.
4. Avoid multiple consecutive runs that only resync family counts unless that bookkeeping is blocking a real practical addition.

## File status note
The workspace outside `research/reverse-expert-kb/` already contains many unrelated edits/untracked files.
For safety, commit only the KB files touched by this run.
