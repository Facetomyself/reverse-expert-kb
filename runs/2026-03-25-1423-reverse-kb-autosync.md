# Reverse KB Autosync Run Report

Date: 2026-03-25 14:23 Asia/Shanghai / 2026-03-25 06:23 UTC
Mode: external-research-driven
Scope: `research/reverse-expert-kb/`
Primary branch worked: protocol / firmware practical subtree
Chosen seam: method-contract -> minimal replay-fixture cases where the body/argument bundle is already mostly truthful, but the representative replay object still lies because per-call call-context semantics outside the body were never frozen explicitly

## Summary
This run deliberately avoided another broad internal sync or branch-wide wording pass.

The protocol / firmware subtree already had solid practical coverage for:
- boundary relocation
- layer peeling
- service-contract extraction
- schema externalization
- minimal replay fixtures
- replay-precondition / acceptance gating

The thinner practical gap was narrower and more operational:
- one representative method-bearing contract may already be externalized
- one protobuf body or RPC argument bundle may already look “right enough”
- yet replay still lies because the real representative call also depended on one narrower **call-context truth** outside the body

This run therefore did a real explicit multi-source search attempt and then made a canonical refinement rather than adding another sibling leaf:
- extended the existing minimal replay-fixture workflow note with an explicit split between **body/argument truth** and **call-context truth**
- anchored that split in practical gRPC and Windows RPC examples
- synchronized the protocol subtree guide, the firmware/protocol parent page, and the top-level index so the refinement survives as branch memory rather than living only inside one leaf
- preserved a source note and raw search artifact for continuation

## Direction review
This run stayed aligned with the KB’s intended direction:
- maintain and improve the KB itself, not just collect notes
- keep work practical and case-driven
- preserve a real operator stop rule instead of generic middleware taxonomy
- avoid dense-branch drift by refining an existing canonical practical note rather than spawning another near-duplicate page

Why this seam was worth working:
- it is small, but it changes live replay workflow behavior
- it affects both gRPC-like and Windows RPC-like families, giving the branch broader practical value without turning abstract
- it prevents a common analyst mistake: overreading a truthful body or argument bundle as the whole replay object
- it cleanly bridges contract externalization and later replay-gate debugging

## Branch-balance awareness
Current balance judgment after this run:
- **still easy to overfeed:** browser anti-bot / captcha, broad mobile protected-runtime, generic malware family polish, and broad protocol wording/index synchronization without new operator value
- **recently improved enough to preserve canonically:** iOS continuation/MainActor stop rules, runtime-evidence practical ladders, pending-request lifetime realism, descriptor ownership / completion visibility, and method-fixture basics
- **good target for this run:** the protocol / firmware practical subtree, specifically the thin seam where one method contract already exists but the representative replay object still omits decisive per-call call-context semantics

Why this was the right maintenance move instead of a new leaf:
- the subtree already had a dedicated method-contract -> minimal replay-fixture page
- the real gap was not absence of a page; it was a still-too-weak stop rule inside that page
- parent/subtree/index synchronization around this narrower rule is more valuable than creating another micro-topic for “RPC metadata quirks”

## External research performed
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries used:
1. `gRPC deadline metadata authority replay fixture reverse engineering minimal replay`
2. `gRPC metadata call credentials deadline authority semantics replay debugging`
3. `Windows RPC binding handle authn level context handle replay reverse engineering`

Saved raw search artifact:
- `sources/firmware-protocol/2026-03-25-replay-fixture-call-context-search-layer.txt`

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

Endpoints used on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Degraded-mode note:
- none for this run
- this was a full explicit multi-source external-research attempt, not Grok-only degraded execution

## Sources used conservatively
Readable retained anchors:
- gRPC docs — Metadata
- gRPC docs — Deadlines
- Microsoft Learn — Binding and Handles
- Microsoft Learn — Using Binding Handles and Making RPC Calls
- Microsoft Learn — RpcBindingInqAuthClientEx

Conservative source-backed cues retained:
- gRPC metadata is a real call-associated side channel rather than a detail of the serialized body
- gRPC deadlines and cancellation posture can materially change practical replay outcome even when the request body stays the same
- Windows RPC binding handles and context handles are first-class call-shaping objects, not accidental transport noise
- Windows RPC authentication level/service posture is queryable and can be part of the live call contract
- for both families, one representative replay object may need a separate explicit **call-context truth** layer before later acceptance-gate debugging is honest

## KB changes made
### New source note
Added:
- `sources/firmware-protocol/2026-03-25-replay-fixture-call-context-notes.md`

Purpose:
- preserve the narrower operator rule around body/argument truth versus call-context truth
- keep the retained source-backed basis for this refinement close to the protocol/firmware practical branch

### Canonical minimal replay-fixture page materially refined
Updated:
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`

Material improvements:
- strengthened the core claim so a minimal fixture is no longer treated as only body/argument truth plus constructor path
- replaced the three-bucket request split with a four-bucket replay split that explicitly includes **call-context truth**
- added practical gRPC and Windows RPC stop rules for when deadline/metadata/authority or binding/authn/context-handle posture still decide whether a replay object is honest
- refined fixture-package preservation guidance and hook-placement guidance around metadata injection, deadline-setting, credential attachment, binding-handle construction, and other call-context surfaces
- extended concrete gRPC and Windows/custom RPC scenarios so analysts do not reopen generic payload doubt when the missing replay object is actually call-context truth

### Protocol subtree guide updated
Updated:
- `topics/protocol-firmware-practical-subtree-guide.md`

Change:
- preserved branch memory that the method-contract -> minimal replay-fixture seam may require separate call-context truth for gRPC-like and Windows RPC-like families rather than treating the serialized body or argument bundle as the whole replay object

### Firmware/protocol parent page updated
Updated:
- `topics/firmware-and-protocol-context-recovery.md`

Change:
- added the same branch-memory to the compact practical ladder so parent-level reading preserves the call-context distinction

### Top-level branch memory updated
Updated:
- `index.md`

Change:
- the top-level protocol/firmware practical-branch summary now preserves the call-context truth reminder for minimal replay-fixture work

## Practical operator value added
This run improved a real replay-workflow stop rule.

Before this refinement, the branch already helped analysts separate:
- contract recovery
- schema externalization
- representative fixture freezing
- later replay acceptance gating

But it still left one avoidable ambiguity:
- if the method path/opnum is known and the request body or argument bundle looks right, is the representative replay object already honest?

After this refinement, the branch more honestly supports a narrower split:
- route/body/argument truth
- call-context truth
- later gate-bearing fields and acceptance behavior
- later output or consequence proof

That changes real case handling:
- analysts are less likely to misread `DEADLINE_EXCEEDED`, routing drift, auth mismatch, or context-handle invalidity as generic payload-shape failure
- gRPC-heavy cases are less likely to drift back into broad protobuf/schema doubt when metadata, deadline, authority, or credential posture is the thinner missing object
- Windows RPC-heavy cases are less likely to overclaim from interface/opnum visibility before freezing binding/authn/context-handle posture
- the subtree now better supports honest handoff into later replay-precondition / state-gate work

This is practical operator value because it is:
- small enough to apply immediately in live reversing cases
- source-backed enough to preserve conservatively
- broad enough to help two important RPC families without turning into abstract middleware taxonomy

## Files changed
Added:
- `sources/firmware-protocol/2026-03-25-replay-fixture-call-context-search-layer.txt`
- `sources/firmware-protocol/2026-03-25-replay-fixture-call-context-notes.md`
- `runs/2026-03-25-1423-reverse-kb-autosync.md`

Updated:
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `index.md`

## Best-effort errors logging note
No `.learnings/ERRORS.md` update was necessary for the main workflow.
Search/runtime degradation would have been recorded here if present, but all requested search sources were successfully attempted in this run.

## Commit / sync status
Plan for this run:
1. commit the reverse-KB files changed by this workflow
2. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
3. leave this run report as the archival record

## Bottom line
This was a real external-research-driven maintenance run on a thinner but practical protocol / firmware seam.

The KB now preserves a sharper replay-fixture stop rule:
- body/argument truth is not always the whole replay object
- some families also require explicit call-context truth
- and in gRPC-like or Windows RPC-like cases, deadline/metadata/authority or binding/authn/context-handle posture may be the missing representative fixture object that must be frozen before later replay-gate conclusions are trustworthy
