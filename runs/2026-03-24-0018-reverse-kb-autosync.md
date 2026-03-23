# Reverse KB Autosync Run Report — 2026-03-24 00:18 CST

Mode: external-research-driven

## Scope this run
- Performed the required direction review and branch-balance check before choosing work.
- Chose a thinner practical seam in the protocol / firmware branch instead of doing another internal wording/index-only pass.
- Ran a real external multi-source search through `search-layer --source exa,tavily,grok` focused on descriptor ownership transfer, completion freshness, ordered publication, and reclaim semantics.
- Materially extended the canonical KB workflow note for descriptor ownership-transfer / completion visibility.
- Added a new source-backed notes page capturing the external evidence and why the resulting KB change is practical.

## Direction review / branch-balance awareness
Recent autosync runs were showing a real risk of drift toward internal maintenance and canonical-sync-only work, with some recent practical additions still clustering around already-established branches.

Current balance judgment for this run:
- **Still easy to overfeed:** browser runtime anti-bot / request-signature work; mobile protected-runtime / mixed WebView timing work
- **Now materially established but still worth feeding carefully:** malware practical branch; protocol / firmware practical branch; protected-runtime ladder work
- **Good target for this run:** protocol / firmware, specifically a narrow queue/descriptor contract seam where practical operator value was higher than another top-level sync edit

Why this branch was chosen now:
- the anti-stagnation rule explicitly disfavors repeated internal-only sync runs
- the protocol / firmware practical branch had the right leaf shape already, but this specific trust/freshness/reclaim seam was still comparatively underfed
- external research could materially improve a canonical workflow page rather than just produce isolated notes

## New findings
- The practically important object in descriptor/ring cases is often not the ring layout but the smaller **trust-and-reclaim contract**:
  - contents become complete
  - owner/index/freshness publication occurs
  - the peer becomes entitled to trust the slot
  - reclaim/head-advance/slot-reuse proves durable consequence
- Completion visibility is often governed by **owner/phase/index freshness semantics**, not by interrupts alone.
- “Completion-shaped bytes are present in memory” is not enough; stale-slot and stale-cache traps deserve explicit workflow treatment.
- Reclaim boundaries such as `RD_IDX`, `CQ head`, used-index advancement, or later slot reuse are often stronger durable proof objects than callback/ISR observation alone.
- Ordered publication/barrier semantics belong in practical RE workflow guidance because they explain many close-but-wrong rehosting and emulation failures.

## Sources consulted
Search-layer search output:
- `sources/firmware-protocol/2026-03-24-descriptor-ownership-completion-visibility-search-layer.txt`

External sources that informed the resulting KB update:
- VirtIO spec / ring material surfaced by search-layer
- Red Hat virtqueue walkthrough
- Linux virtio ring implementation / barrier discussion surfaced by search-layer
- SPDK NVMe submission/completion queue explanation
- Microsoft NVMe completion queue head doorbell documentation
- Linux amdgpu ring-buffer documentation

Detailed source notes recorded in:
- `sources/protocol-and-network-recovery/2026-03-24-descriptor-ownership-transfer-and-completion-visibility-notes.md`

## Reflections / synthesis
This was the right kind of external-research-driven maintenance run.

It improved the KB itself rather than merely collecting links, and it fed a thinner practical continuation branch instead of over-polishing a dense one.

The most durable cross-source pattern was not vendor-specific queue trivia; it was the recurring analyst discipline:
- separate contents from publication
- separate publication from freshness/visibility
- separate visibility from interrupting
- separate completion from reclaim

That pattern is exactly the sort of case-driven operator guidance the reverse KB should preserve.

## Candidate topic pages to create or improve
Improved this run:
- `topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md`

Candidate next improvements nearby if future evidence justifies them:
- sharpen `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md` with a more explicit handoff rule into freshness/owner/phase-specific continuation
- add a thinner protocol/firmware continuation specifically for **pending completion freshness vs stale-slot diagnosis** only if repeated cases justify a dedicated leaf
- cross-link mailbox/descriptor/MMIO/ISR pages more explicitly if this branch keeps accumulating queue-contract notes

## Next-step research directions
- Look for another underfed practical branch before touching browser/mobile again unless there is a blocking continuity reason.
- Good future candidates:
  - thinner firmware/peripheral continuations around queue-to-register realism
  - native desktop/server practical branch gaps with concrete async ownership or worker consequence notes
  - deeper malware continuation on source-backed consumer/proof seams rather than broad persistence taxonomy
- For the protocol / firmware branch specifically, future external-research-driven work should prefer another concrete operator seam, not repeated wording polish around the same ownership note.

## Concrete scenario notes or actionable tactics added this run
Added or strengthened in the canonical workflow note:
- explicit `freshness` handling via owner/phase/tag semantics
- stronger rule that completion bytes in memory are not necessarily fresh completion
- stronger reclaim/slot-reuse stop rule
- clearer checklist around publish order, consume order, cache visibility, freshness rule, and identity continuity
- new concrete scenario for populated-but-stale completion slots under phase/owner semantics

## Files changed
- Added: `research/reverse-expert-kb/sources/protocol-and-network-recovery/2026-03-24-descriptor-ownership-transfer-and-completion-visibility-notes.md`
- Updated: `research/reverse-expert-kb/topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md`
- Added: `research/reverse-expert-kb/runs/2026-03-24-0018-reverse-kb-autosync.md`

## Search audit
Search sources requested: exa,tavily,grok
Search sources succeeded: exa,tavily,grok
Search sources failed: none
Exa endpoint: `http://158.178.236.241:7860`
Tavily endpoint: `http://proxy.zhangxuemin.work:9874/api`
Grok endpoint: `http://proxy.zhangxuemin.work:8000/v1`

## Commit / sync status
- KB changes detected: yes
- Planned action: commit the KB changes and run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
- If sync fails, preserve local KB progress and leave the failure noted here
