# Reverse Expert KB Autosync Run Report

Date: 2026-03-21 10:18 Asia/Shanghai
Mode: external-research-driven
Area: protocol / firmware practical branch
Focus: schema externalization / service-contract extraction / replay-harness bridge

## Summary
This run intentionally avoided another KB-internal canonical-sync-only pass.
Recent reverse-KB autosync history showed several branch-balance / family-count / index-alignment runs, with only limited recent protocol/firmware branch growth.
Per the anti-stagnation rule, this run performed a real external research pass and used it to add a concrete practical rung on a thinner branch.

The chosen gap was the protocol/firmware branch’s underdescribed bridge between:
- recovering one smaller trustworthy contract, and
- turning that contract into one reusable schema/service artifact plus one representative replay/edit/fuzz harness target.

The work product was a new workflow note focused on schema externalization and minimal harness generation, plus the source note and the minimum parent/subtree/index synchronization needed to make the branch remember the new rung canonically.

## Direction review
Recent maintenance risk:
- too many recent runs leaning toward internal synchronization, family-count maintenance, and top-level wording repair
- protocol/firmware branch was established, but still had a practical gap between contract recovery and replay-gate work
- easy dense branches were not the right place to spend this run

Direction decision for this run:
- make this an external-research-driven run
- bias toward a thinner but practical branch
- add a concrete workflow note rather than another top-level wording-only pass
- preserve branch-balance by strengthening protocol/firmware instead of feeding already-dense branches again

## Branch-balance review
Branch-balance judgment at start of run:
- browser/mobile/protected-runtime remain easier to overfeed
- malware had just received a substantive practical bridge recently
- protocol/firmware still had a practical gap around externalizing recovered contracts into reusable artifacts

Branch-balance action taken:
- strengthened protocol/firmware practical branch with a new explicit rung after layer-peeling / contract recovery
- synchronized subtree guide, protocol parent page, firmware/protocol parent page, and top-level index so the branch keeps the new memory canonically

## External research performed
Queries used:
- `protocol reverse engineering schema extraction replay harness generation`
- `binary protocol reverse engineering service contract extraction workflow`
- `protobuf thrift capnp reverse engineering schema inference replay automation`

Search intent/mode:
- deep exploratory multi-source pass

Retained external signals:
- Netzob reinforced the message-format -> grammar -> simulation/fuzzing chain as a practical operator target rather than taxonomy trivia
- BitBlaze protocol-RE material reinforced that recovered protocol structure becomes most useful when it supports analyzers, dialogue replay, or other reusable interaction tooling
- Arkadiy Tetelman’s protobuf descriptor-recovery write-up reinforced the shortcut rule that embedded descriptors / reflection metadata can outperform blind blob inference when they exist
- `protobuf-inspector` reinforced the provisional-schema workflow from stable shape when names are missing
- `pbtk` reinforced the practical bridge from recovered protobuf structures to endpoint replay/edit/fuzz manipulation

Conservative synthesis applied:
- did not assume protobuf is universal
- did not claim schema externalization alone solves replay acceptance
- separated schema/message contract from service shell and from state/auth/freshness obligations
- kept the new note scoped to one representative contract plus one minimal harness surface, not full client reimplementation

## KB changes made
Added:
- `topics/protocol-schema-externalization-and-replay-harness-workflow-note.md`
- `sources/firmware-protocol/2026-03-21-schema-externalization-and-replay-harness-notes.md`
- `runs/2026-03-21-1018-protocol-schema-externalization-harness-autosync.md`

Updated:
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-state-and-message-recovery.md`
- `index.md`

## Practical value added
New protocol/firmware ladder step added:
- **externalize** one recovered contract into one reusable schema, service-contract artifact, or representative replay/edit/fuzz harness target

This materially improves the branch because it now has an explicit practical answer for cases where:
- visibility is no longer the main problem
- one smaller contract already exists
- but replay or tooling work keeps stalling because the contract still lives only in traces or prose

The branch can now remember a narrower operator sequence:
- see the right boundary
- peel to one smaller trustworthy contract
- externalize that contract into one reusable artifact
- then continue into replay gates, output handoff, parser consequence, or content continuation

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
- none observed in this run

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Notes:
- This run explicitly requested `exa,tavily,grok` via search-layer as required.
- No degraded-mode fallback was needed for this run.

## Files changed in KB scope
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/topics/firmware-and-protocol-context-recovery.md`
- `research/reverse-expert-kb/topics/protocol-firmware-practical-subtree-guide.md`
- `research/reverse-expert-kb/topics/protocol-state-and-message-recovery.md`
- `research/reverse-expert-kb/topics/protocol-schema-externalization-and-replay-harness-workflow-note.md`
- `research/reverse-expert-kb/sources/firmware-protocol/2026-03-21-schema-externalization-and-replay-harness-notes.md`
- this run report

## Next useful continuations
Good next protocol/firmware continuations after this run would be:
- one concrete case-driven continuation below the new externalization rung for a specific schema family or replay gate
- one narrower workflow note for service-shell extraction when RPC framing is the dominant remaining gap
- or a return to KB-internal synchronization only if this new rung drifts out of alignment with parent/subtree/index memory

## Commit / sync status
Pending at report write time.
