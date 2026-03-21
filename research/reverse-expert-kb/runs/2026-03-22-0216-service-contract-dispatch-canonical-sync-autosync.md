# Reverse KB Autosync Run Report — 2026-03-22 02:16 CST

Mode: external-research-driven

## Summary
This run targeted a thinner but still practical seam in the protocol / firmware branch: the gap between layer-peeling / smaller-contract recovery and later schema-externalization or parser/state work.

The KB already had a dedicated leaf for `protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`, but the branch’s canonical memory was still uneven. This run used fresh multi-source search to revalidate that seam, then synchronized the parent pages and branch map so service-shell / dispatch recovery is remembered as a real operator step rather than a leaf that is easy to forget.

## Why this branch / task was chosen
Recent runs were still practical and externally pressured, so the anti-stagnation rule did not require a total branch pivot.
But the protocol branch still had one underfed practical seam:
- a service-oriented / RPC-shaped family can already be recognized
- one smaller contract can already be seen
- yet the real next bottleneck is still recovering one reusable service shell, interface roster, dispatch table, or representative method contract

That seam already existed as a leaf note, but not strongly enough in parent-page memory.
So this run focused on **source-backed canonical sync** rather than inventing another adjacent leaf.

## External research performed
Queries used through `search-layer`:
- `reverse engineering gRPC protobuf service contract method dispatch workflow binary analysis`
- `reverse engineering protobuf rpc dispatch table schema extraction workflow`
- `firmware rpc service method dispatch reverse engineering workflow`

Retained sources reviewed:
- <https://www.ioactive.com/breaking-protocol-buffers-reverse-engineering-grpc-binaries/>
- <https://arkadiyt.com/2024/03/03/reverse-engineering-protobuf-definitiions-from-compiled-binaries/>
- <https://clearbluejar.github.io/posts/surveying-windows-rpc-discovery-tools/>
- <https://github.com/marin-m/pbtk>
- <https://github.com/mildsunrise/protobuf-inspector>

## Search audit
Requested sources: exa, tavily, grok
Succeeded sources: exa, tavily, grok
Failed sources: none recorded at search-layer stage

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Notes:
- This run explicitly invoked all three requested sources via `search-layer --source exa,tavily,grok`.
- Search-layer returned blended results carrying all three source families, so this run counts as a real external multi-source pass.
- Source quality still varied by item; retained synthesis stayed conservative and was anchored to the higher-signal pages above.

## What changed
### Canonical branch sync
Updated protocol-branch parent and routing pages so the service-contract / dispatch seam is explicitly preserved:
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `index.md`

### New source note
Added:
- `sources/firmware-protocol/2026-03-22-service-contract-dispatch-canonical-sync-notes.md`

This note captures why the service-contract / dispatch step deserves canonical retention in the protocol branch, rather than remaining only a leaf-specific detail.

## Practical synthesis gained
The branch memory is now more explicit about this operator order:
1. choose the right boundary
2. peel one visible object into one smaller contract
3. if the family is service-oriented or RPC-shaped, recover one service shell or representative method-bearing contract
4. externalize that contract into one reusable schema or harness target
5. then prove consequence, acceptance, output, or hardware-side edges

The important practical correction is that:
- “I can decode the payload”
- and “I know which callable surface or method family this payload belongs to”

are adjacent but different proofs.

## Direction review
This run stayed aligned with the KB’s current direction rules:
- practical and case-driven rather than abstract taxonomy growth
- branch-balance aware rather than polishing already-dense mobile/browser branches
- focused on preserving a real operator bottleneck in the protocol branch’s canonical memory
- avoided another small wording-only pass by requiring fresh external-source pressure first

## Branch-balance review
Current branch-balance implication:
- protocol / firmware remains materially established, but its practical operator ladder still benefits from parent-page synchronization whenever a useful seam would otherwise disappear into leaves
- this run improved branch memory without overfeeding dense browser/mobile areas
- the branch is now slightly healthier because the service-shell / dispatch bridge is represented both as a leaf and as a remembered routing step

## Files changed
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/topics/firmware-and-protocol-context-recovery.md`
- `research/reverse-expert-kb/topics/protocol-state-and-message-recovery.md`
- `research/reverse-expert-kb/topics/protocol-firmware-practical-subtree-guide.md`
- `research/reverse-expert-kb/sources/firmware-protocol/2026-03-22-service-contract-dispatch-canonical-sync-notes.md`

## Commit / sync
If KB-only changes are still the only staged modifications at commit time, commit them and run:
- `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

## Next useful directions
Good next protocol/firmware continuations now include:
- a case-driven note around choosing between service-shell recovery and immediate schema externalization when both are partially available
- a thinner practical continuation on how to tie one recovered method contract to one first replay fixture without overreaching into full client rebuilds
- a source-backed comparison note distinguishing dispatch-bearing service families from content-pipeline families so analysts do not misroute one into the other too early