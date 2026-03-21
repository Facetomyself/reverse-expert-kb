# Reverse KB Autosync Run Report — 2026-03-21 17:19 Asia/Shanghai

Mode: external-research-driven

## Summary
This run intentionally avoided another internal-only protocol branch wording/count sync.
Recent same-day runs had already spent meaningful effort on internal branch balancing and practical ladder cleanup, so this pass prioritized a real external research attempt on a thinner but still practical seam in the protocol / firmware branch.

Chosen branch gap:
- protocol / firmware
- specifically the gap between:
  - broad layer peeling into one smaller trustworthy contract, and
  - later schema externalization / replay-gate / handler-consequence work
- target addition: **service-contract extraction / method-dispatch recovery** for RPC-shaped or service-oriented protocol families

Outcome:
- added one new source-backed practical workflow note
- added one new source-note file capturing the external research synthesis
- updated subtree routing so the protocol branch now explicitly distinguishes:
  - layer peeling
  - service-shell / method-dispatch extraction
  - schema externalization
- updated top-level index routing to reflect the new practical rung

## Why this work was chosen
Branch-balance and anti-stagnation review:
- recent runs already covered several internal KB maintenance passes in adjacent branches, including branch routing, practical ladder sharpening, and narrow protocol/malware/runtime wording sync
- the protocol / firmware branch explicitly had room for a practical leaf around service-contract extraction and method-dispatch recovery
- that gap had operator value because many cases stall after “this is protobuf/RPC-like” but before there is one reusable callable contract surface

So this run favored:
- a thinner branch
- a practical continuation page
- external-source-backed synthesis
instead of another family-count/index-only repair

## New / changed KB artifacts
### New files
- `research/reverse-expert-kb/topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- `research/reverse-expert-kb/sources/firmware-protocol/2026-03-21-service-contract-extraction-and-method-dispatch-notes.md`

### Updated files
- `research/reverse-expert-kb/topics/protocol-firmware-practical-subtree-guide.md`
- `research/reverse-expert-kb/index.md`

## What was added
### 1. New practical workflow note
Added:
- `topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`

This note captures a distinct practical bottleneck:
- one smaller trustworthy contract already exists
- the family already looks RPC-like or service-oriented
- but the first reusable service shell, interface roster, dispatch table, or representative method contract is still implicit

It now gives operators a cleaner answer to:
- when to stop broad “RPC-like” narration
- when to recover registration / dispatch anchors first
- how to separate:
  - message/schema recovery
  - service-contract extraction
  - handler consequence proof
  - replay-gate debugging

### 2. New source note
Added:
- `sources/firmware-protocol/2026-03-21-service-contract-extraction-and-method-dispatch-notes.md`

The source note distilled practical lessons such as:
- registration-first anchor selection for RPC-shaped targets
- dispatch-table / interface-structure recovery as a contract shell even when names are sparse
- tying protobuf/schema recovery to one callable method surface instead of keeping it detached
- using one service shell plus one representative method as the right first stop point

### 3. Branch routing improvements
Updated the protocol / firmware subtree guide so it now explicitly models a twelve-family practical ladder, inserting:
- **service-contract / method-dispatch uncertainty**

This makes the protocol branch read more cleanly as:
- boundary selection
- socket/private-overlay truth recovery
- layer peeling
- service-shell / representative-method recovery
- schema externalization / harness generation
- later ownership / consequence / replay / output / hardware-side proof

### 4. Top-level branch map improvements
Updated `index.md` so the top-level protocol / firmware branch description now includes the new practical rung and no longer jumps directly from layer peeling to schema externalization.

## Research synthesis
The external research supported a practical claim that was missing clean expression in the KB:

A recovered message shape is often still not the most useful next object.
For RPC-shaped or service-oriented targets, the more useful next object is frequently:
- one registered service shell
- one interface or dispatch-bearing structure
- one representative method tied to one request/response family

That matters because it prevents two common failure modes:
- staying stuck in detached schema polishing with no callable surface
- over-jumping into handler semantics or replay debugging before one representative contract-bearing object exists

The resulting workflow note intentionally keeps these jobs separate:
- layer peeling / smaller-contract recovery
- service-contract extraction / method-dispatch recovery
- schema externalization / replay harness generation
- parser/state consequence proof
- replay-precondition localization

That separation materially improves branch practicality.

## Direction review
This run stayed aligned with the KB’s current direction rules:
- practical over abstract
- case-driven over taxonomy-driven
- branch-balancing over dense-branch polishing
- one smaller trustworthy operator object over broad family narration

This was not a wording-only cleanup.
It produced:
- a concrete new continuation page
- a new source-backed branch seam
- routing changes that should make future protocol runs less likely to drift into repetitive internal synchronization

## Branch-balance review
### Before this run
The protocol branch already had stronger coverage for:
- boundary relocation
- socket-boundary truth recovery
- layer peeling
- schema externalization
- replay gating
- reply/output handoff

But it was thinner on:
- the intermediate service-shell / method-dispatch step for RPC-like cases

### After this run
The branch is now more balanced across the practical ladder:
- visible object selection
- smaller-contract isolation
- service-contract recovery
- schema/harness handoff
- later consequence/gate/output proof

This should reduce future pressure to repeatedly patch the same transition indirectly through wording in nearby notes.

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

Search invocation policy used:
- explicit multi-source search via `search-layer --source exa,tavily,grok`
- no implicit/default source selection

Endpoints in use for this environment:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Queries used:
- `rpc reverse engineering service contract extraction method dispatch workflow`
- `protobuf thrift grpc reverse engineering service method recovery workflow`
- `binary protocol reverse engineering rpc service shell dispatch schema harness`

Representative retained sources:
- <https://labs.ioactive.com/2021/07/breaking-protocol-buffers-reverse.html>
- <https://blog.xpnsec.com/analysing-rpc-with-ghidra-neo4j>
- <https://specterops.io/blog/2023/10/18/uncovering-rpc-servers-through-windows-api-analysis/>
- <https://github.com/marin-m/pbtk>

Conservative note:
- search returned some noisy or weaker side results as expected for broad RPC phrasing
- retained synthesis was anchored to the higher-signal registration/dispatch/schema-to-endpoint sources above rather than to the noisier peripheral hits

## Files changed in this run
- `research/reverse-expert-kb/topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- `research/reverse-expert-kb/sources/firmware-protocol/2026-03-21-service-contract-extraction-and-method-dispatch-notes.md`
- `research/reverse-expert-kb/topics/protocol-firmware-practical-subtree-guide.md`
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/runs/2026-03-21-1719-protocol-service-contract-method-dispatch-autosync.md`

## Next likely directions
Good next protocol / firmware follow-ups now include:
- a concrete case-driven page for blind/partial gRPC service enumeration when descriptors are incomplete but registration or reflection remnants still exist
- a practical note around representative method selection after service-shell recovery when many dispatch slots exist but only one should drive the next trace
- a case-driven continuation on contract-to-handler reduction for proprietary opcode dispatchers that behave like private RPC

## Commit / sync intent
If the working tree is clean enough for a focused KB commit:
- commit the reverse KB changes
- run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
- record the result in git history rather than leaving this run as local-only drift
