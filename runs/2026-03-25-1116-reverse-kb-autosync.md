# Reverse KB Autosync Run Report

Date: 2026-03-25 23:16 Asia/Shanghai / 2026-03-25 15:16 UTC
Mode: external-research-driven
Scope: `research/reverse-expert-kb/`
Primary branch worked: protocol / firmware practical subtree
Chosen seam: pending-owner lifetime realism after broad owner-match is already plausible — specifically the point where queue/callback-path success and visible slot/tag/correlation plausibility are still weaker than current waiter/owner liveness

## Summary
This run intentionally avoided another KB-internal wording/index/count-only maintenance pass.

Recent protocol / firmware work had already improved:
- method-contract -> minimal replay-fixture call-context truth
- pending-request generation / slot-reuse continuation
- descriptor ownership / visibility memory

That made another generic sync pass the wrong move.
The thinner, still-practical gap was narrower:
- the broad owner-match can already look good enough
- the broad reply/completion path can already look good enough
- the visible slot/tag/correlation can still look good enough
- but the runtime may still reject the arrival because the current trusted waiter/owner contract has already changed

This run therefore did a real explicit `exa,tavily,grok` search attempt and then improved the KB itself rather than merely collecting notes:
- added one new retained source note for pending-owner lifetime deepening
- materially refined the canonical generation/epoch/slot-reuse workflow page with a stronger late-reply / unmatched-reply reminder anchored in Spring/RabbitMQ-style request/reply behavior
- repaired that canonical page’s source-footprint section so it points to truthful retained source paths instead of stale `sources/firmware-protocol/...` references
- synchronized the firmware/protocol parent page and the top-level index so this stop rule survives as branch memory rather than living only in the leaf note

This is a KB improvement, not just source collection:
- the canonical pending-owner lifetime page is sharper and more honest about explicit stale/late/unmatched-reply branches
- the parent/index branch memory now preserves pending-owner lifetime as its own narrow proof layer
- the canonical page’s provenance is cleaner and less likely to mislead later maintenance

## Direction review
This run stayed aligned with the reverse KB’s intended direction:
- maintain and improve the KB itself, not just collect notes
- keep work practical and case-driven
- prefer operator stop rules over abstract taxonomy
- include branch-balance awareness instead of overfeeding already-dense leaves

Why this seam was the right choice now:
- it is thinner than the broader pending-request correlation page, but still practical and case-driven
- it directly addresses a recurring analyst mistake: overreading broad path correctness as current-owner truth
- it improves a canonical workflow page that already sits in a useful subtree route, instead of fragmenting the branch with another near-duplicate leaf
- it satisfies the anti-stagnation rule by being a real external-research-driven run inside the rolling window

## Branch-balance awareness
Current balance judgment after this run:
- **Still easy to overfeed:** browser anti-bot / challenge continuations, broad mobile protected-runtime seams, and generic branch-memory polishing without new operator value
- **Recently improved enough to preserve canonically:** protocol method-fixture call-context truth, descriptor ownership / completion visibility, iOS continuation/MainActor memory, malware service-recovery slot selection, runtime-evidence watched-object truth selection
- **Good target for this run:** protocol / firmware pending-owner lifetime realism, specifically the thin seam where broad path correctness is already plausible but one still-live waiter/owner contract decides consume vs stale-drop

Why this seam mattered:
- the branch already had broad pending-request correlation and a thinner generation/slot-reuse continuation
- but the canonical page still under-preserved one practical stop rule around explicit late-reply / unmatched-reply handling
- and its source-footprint block still had stale provenance pointers
- fixing both is better operator value than another internal sync-only pass or another detached micro-topic

## External research performed
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries used:
1. `gRPC completion queue tag stale call object late completion reverse engineering`
2. `AMQP RPC direct reply-to correlation id pending request stale reply`
3. `NVMe completion queue phase tag slot reuse stale completion reverse engineering`

Saved raw search artifact:
- `sources/protocol-and-network-recovery/2026-03-25-pending-owner-lifetime-search-layer.txt`

Additional readable/source-adjacent follow-up fetched conservatively:
- gRPC async C++ tutorial
- gRPC completion-queue overview
- RabbitMQ direct reply-to docs
- Spring AMQP request/reply docs
- one NVMe-oriented fetch attempt that degraded under fetch restrictions

## Search audit
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- exa
- tavily

Failed sources:
- grok

Endpoints used on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Degraded-source note:
- This run explicitly attempted all three requested sources.
- Grok returned repeated `502 Bad Gateway` failures during invocation.
- Exa and Tavily returned enough usable material to continue conservatively.
- This therefore counts as a real multi-source external-research attempt under a degraded source set, not as normal mode.

## Sources used conservatively
Primary retained anchors:
- gRPC async C++ tutorial
- gRPC completion-queue overview
- RabbitMQ direct reply-to documentation
- Spring AMQP request/reply documentation
- partial NVMe/phase-tag queue evidence used only as conservative queue-ownership analogy

Retained source-backed cues:
- completion-queue/tag delivery is weaker than proving the current trusted per-call owner is still live
- direct reply-path correctness is weaker than proving the current trusted waiter/pending marker still owns the reply
- late replies and replies without usable correlation can be explicit reply-side branches, not merely accidental misses
- stable slot/index visibility is weaker than phase/owner truth
- replay fixtures that preserve bytes but not lifetime boundaries are often too weak

## KB changes made
### New source note
Added:
- `sources/protocol-and-network-recovery/2026-03-25-pending-owner-lifetime-notes.md`

Purpose:
- preserve the narrower operator rule around broad path correctness vs current owner-liveness
- explicitly record the degraded search-source set
- keep the retained reasoning close to the protocol / firmware pending-owner branch

### Canonical workflow note materially refined
Updated:
- `topics/protocol-pending-request-generation-epoch-and-slot-reuse-workflow-note.md`

Material improvements:
- added a stronger source-backed reminder that late replies / unmatched replies can surface as explicit branches rather than as vague non-consume behavior
- tightened the practical reduction toward retained waiter map / future table, timeout/retire path, and later stale-drop or unmatched-reply branch
- repaired the source-footprint block so it now points at the real retained `sources/protocol-and-network-recovery/...` notes and search artifacts from current branch work
- preserved the earlier generation/phase/slot-reuse framing while sharpening how async reply-side error handling should be read by operators

### Firmware/protocol parent page updated
Updated:
- `topics/firmware-and-protocol-context-recovery.md`

Change:
- the compact practical ladder now explicitly preserves **pending-owner lifetime contract** as a distinct proof layer once broad owner-match is already good enough

### Top-level branch memory updated
Updated:
- `index.md`

Change:
- the compact protocol/firmware branch reading now preserves pending-owner lifetime contract as its own narrower proof layer instead of flattening it into generic acceptance or ownership wording

## Practical operator value added
This run improved a real analyst stop rule.

Before this refinement, the branch already helped analysts separate:
- replay acceptance/gating
- broad pending-request correlation / owner-match
- narrower generation / phase / slot-reuse realism

But one avoidable ambiguity remained:
- if the reply/completion arrived on the right broad path and the visible identifier still looked right, was the runtime simply “not consuming it” for unspecified reasons?

After this refinement, the branch more honestly supports a narrower split:
- broad path correctness
- visible identifier plausibility
- current waiter/owner liveness truth
- explicit stale/late/unmatched-reply branch truth
- later consume or discard consequence

That changes real case handling:
- analysts are less likely to misread stale replies as generic parser/correlation failures
- callback-path or queue-path success is less likely to be overread as final proof
- compare-pair design becomes sharper because retire/reuse/timeout branches become explicit targets
- the canonical page’s provenance is now less likely to send later maintenance back to stale paths

This is practical operator value because it is:
- narrow enough to apply in live async reply / completion reversing cases
- source-backed enough to retain conservatively
- materially better than another internal sync-only pass

## Files changed
Added:
- `sources/protocol-and-network-recovery/2026-03-25-pending-owner-lifetime-notes.md`
- `runs/2026-03-25-1116-reverse-kb-autosync.md`

Updated:
- `topics/protocol-pending-request-generation-epoch-and-slot-reuse-workflow-note.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `index.md`

Saved raw search artifact:
- `sources/protocol-and-network-recovery/2026-03-25-pending-owner-lifetime-search-layer.txt`

## Best-effort errors logging note
No `.learnings/ERRORS.md` entry was required for the main workflow.
Search degradation was captured directly in this run report’s Search audit section and treated as non-blocking degraded mode.

## Commit / sync status
Plan for this run:
1. commit the reverse-KB files changed by this workflow
2. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
3. leave this run report as the archival record

## Bottom line
This was a real external-research-driven maintenance run on a thinner but practical protocol / firmware seam.

The KB now preserves a sharper pending-owner lifetime rule:
- do not stop at queue/callback-path success
- do not stop at visible slot/tag/correlation plausibility
- prove whether the current trusted waiter/owner is still live across retire/reuse/timeout/phase boundaries
- then decide whether the target is failing syntax/correlation, or correctly discarding stale ownership
