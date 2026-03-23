# Reverse KB Autosync Run Report — 2026-03-23 14:16 Asia/Shanghai

Mode: external-research-driven

## Scope this run
- Performed the required direction review before choosing scope.
- Chose a thinner practical protocol / firmware continuation instead of returning to browser/mobile or doing another internal wording/index-only pass.
- Focused this run on strengthening an existing underfed practical seam:
  - `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- Added one new supporting source note:
  - `sources/firmware-protocol/2026-03-23-opnum-and-timeout-lifecycle-minimal-replay-notes.md`
- Materially extended the topic page to preserve two practical operator rules more explicitly:
  - Windows RPC replay should freeze one opnum-level representative call bundle, not drift back into whole-interface folklore
  - async / completion-sensitive replay fixtures sometimes need explicit deadline / timeout / cancel posture so timeout or late-reply behavior is not misread as payload-shape failure

## Branch-balance review
Recent runs over the last several hours were not stagnant overall, but there was still a visible tendency for protocol work to lean toward:
- internal branch grooming
- existing acceptance / pending-request continuations
- prior streaming/minimal-fixture reinforcement

The protocol / firmware subtree was already healthier than before, but this specific seam still needed practical tightening:
- after service-contract extraction
- after schema externalization
- after the first minimal-fixture page existed
- but before analysts fall into replay debugging with an under-specified fixture

This run therefore favored:
- protocol / firmware over denser browser/mobile areas
- practical continuation over top-level wording polish
- external-research-backed refinement over internal canonical sync

## Why this branch / page was chosen
This branch is still thinner than the browser/mobile/native parts in one specific sense:
- it had the right broad ladder
- it already had a method-contract -> minimal-fixture page
- but it was still under-preserving a real field failure mode:
  - analysts freeze method or opnum identity
  - replay still "fails"
  - timeout/cancel/late-reply behavior gets blamed on argument shape or serializer shape too early

That makes the branch look complete on paper while still missing a practical stop-rule.

So this run targeted a still-practical, still-case-driven gap instead of adding another broad taxonomy page.

## New findings
- The current page already handled streaming slice / half-close and Windows RPC opnum-level representative call bundles reasonably well.
- The missing practical reinforcement was lifecycle truth for async/completion-shaped calls.
- Fresh source review supported a narrower rule worth making canonical in the KB:
  - a minimal replay fixture can be incomplete even when payload shape is plausible, if it does not preserve the expected completion style and timeout/deadline/cancel posture
- Windows RPC source material continued to support a strong practical reduction:
  - interface discovery -> one callable surface -> one representative opnum/argument bundle -> explicit ambient assumptions
- gRPC deadline material usefully reinforced a cross-protocol caution:
  - client-side timeout does not necessarily mean server-side non-completion
  - therefore timeout-shaped differences should be preserved as lifecycle evidence before being interpreted as payload-shape failure

## Sources consulted
Search-bearing source trace saved at:
- `sources/protocol-and-network-recovery/2026-03-23-protocol-minimal-replay-fixture-search-layer.txt`

External sources consulted directly during synthesis:
- Trail of Bits — *Introducing RPC Investigator*
  - https://blog.trailofbits.com/2023/01/17/rpc-investigator-microsoft-windows-remote-procedure-call/
- Shelltrail — *ManageEngine ADAudit - Reverse engineering Windows RPC to find CVEs - part 2*
  - https://shelltrail.com/research/manageengine-adaudit-reverse-engineering-windows-rpc-to-find-cve-2024-36036-and-cve-2024-36037-part2
- Zero Day Initiative — *Down the Rabbit Hole - A Deep Dive into an attack on an RPC interface*
  - https://www.thezdi.com/blog/2018/6/7/down-the-rabbit-hole-a-deep-dive-into-an-attack-on-an-rpc-interface
- gRPC blog — *gRPC and Deadlines*
  - https://grpc.io/blog/deadlines

Internal KB context consulted:
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- `topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- recent 2026-03-23 protocol run reports and source notes

## Concrete KB improvements made
Updated `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md` to preserve more practical operator guidance around:
- lifecycle-sensitive fixture identity for async/completion-shaped calls
- explicit preservation of deadline/timeout/cancel posture when that posture can explain apparent replay failure
- stronger blocker wording when timeout/deadline posture is still ambient rather than frozen into the fixture package
- a concrete scenario for "method looks right, but the client fixture lies about completion"
- stronger good-output criteria for async / timeout-sensitive fixtures

Added supporting note:
- `sources/firmware-protocol/2026-03-23-opnum-and-timeout-lifecycle-minimal-replay-notes.md`

## Reflections / synthesis
The improvement matters because this is exactly the kind of gap that causes protocol branches to look richer than they actually are.

Without this addition, analysts can already say:
- I know the method
- I know the opnum
- I have an argument bundle
- I have a request blob

But still fail practically because they do not preserve:
- whether the original path was immediate reply vs deferred completion
- whether a deadline/cancel boundary was part of the observed behavior
- whether a client-visible timeout still coexisted with server-side completion or late reply

That is small on paper, but very real in practice.

This run therefore improves the branch in the right direction:
- more practical
- more case-driven
- less likely to drift into abstract contract or serializer narration

## Candidate follow-on directions
If protocol / firmware stays productive, likely good next continuations are:
- a narrower practical continuation for timeout-observed vs stale-reply-observed compare design if enough real cases accumulate
- deeper Linux / custom-RPC equivalents only if source-backed and still operator-useful
- further protocol work should continue to bias toward concrete workflow notes or case notes, not more broad subtree wording

## KB files changed
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- `sources/firmware-protocol/2026-03-23-opnum-and-timeout-lifecycle-minimal-replay-notes.md`
- `runs/2026-03-23-1416-protocol-opnum-timeout-lifecycle-minimal-fixture-autosync.md`

## Search audit
- Search sources requested: `exa,tavily,grok`
- Search sources succeeded: `exa,tavily,grok`
- Search sources failed: none at the search-layer invocation level
- Exa endpoint: `http://158.178.236.241:7860`
- Tavily endpoint: `http://proxy.zhangxuemin.work:9874/api`
- Grok endpoint: `http://proxy.zhangxuemin.work:8000/v1`
- Notes:
  - This run satisfied the anti-stagnation rule with a real explicit multi-source search attempt.
  - Result quality was mixed but usable: Exa and Grok were strongest on RPC-facing leads; Tavily returned both useful official docs and some noisier generic RPC material.
  - No source failed at invocation level, so this was not a degraded-source-set run.

## Commit / sync status
- Pending at report-write time.
- If KB-only changes remain after final review, commit them in the reverse-KB repo and then run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh` as required.
