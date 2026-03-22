# Reverse KB Autosync Run — 2026-03-22 09:16 Asia/Shanghai

Mode: external-research-driven

## Scope this run
This run deliberately avoided another internal-only canonical-sync pass.

Chosen scope:
- review branch balance and recent protocol/firmware maintenance shape
- perform a real external-research attempt through `search-layer --source exa,tavily,grok`
- prefer a thinner, still-practical protocol/firmware seam rather than another browser/mobile or top-level wording pass
- deepen the protocol branch with a narrower leaf between service-contract extraction / schema externalization and replay-gate debugging
- update nearby routing/index pages so the new note is canonically reachable
- write the run report, then commit and sync KB changes if any

## New findings
The strongest finding from this run was branch-shape, not taxonomy:
- the protocol/firmware branch already had notes for service-contract extraction and for schema externalization / replay-harness generation
- but there was still a practical operator gap between those two and later replay-precondition debugging
- that gap is: **freezing one representative method fixture and minimal constructor path before widening into state-gate guesses**

Practical additions made this run:
- added `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- added supporting source note `sources/firmware-protocol/2026-03-22-method-contract-minimal-replay-fixture-notes.md`
- updated subtree/index/canonical routing text to point at the narrower continuation

The new note keeps the problem small and operator-oriented:
- choose one method/opcode family only
- preserve fixture provenance before editing
- split fields into route identity vs likely gate-bearing vs decorative
- prefer one minimal constructor/serializer path
- build one compare-friendly fixture package
- move quickly into replay-gate, parser/state, output-side, or provenance work once that boundary exists

## Sources consulted
Primary external/useful sources:
- IOActive gRPC reversing walkthrough
  - <https://www.ioactive.com/breaking-protocol-buffers-reverse-engineering-grpc-binaries/>
- Clear Blue Jar Windows RPC discovery survey
  - <https://clearbluejar.github.io/posts/surveying-windows-rpc-discovery-tools/>
- XPN RPC internals / Ghidra workflow
  - <https://blog.xpnsec.com/analysing-rpc-with-ghidra-neo4j/>
- Berkeley BitBlaze/Reverser protocol RE framing
  - <https://people.eecs.berkeley.edu/~dawnsong/bitblaze/protocol.html>

Search-only / not promoted into core claims:
- Grok-returned gRPC replay / fixture tool and blog pointers
- Tavily-returned ZDI RPC interface reversing result
- one direct `web_fetch` attempt to Arkadiy Tetelman’s protobuf descriptor article failed during this run, so it was not treated as a fresh retained source here

Internal/canonical sources consulted:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent `research/reverse-expert-kb/runs/*.md`
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- `topics/protocol-schema-externalization-and-replay-harness-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `sources/firmware-protocol/2026-03-21-schema-externalization-and-replay-harness-notes.md`

## Reflections / synthesis
This run usefully satisfied the anti-stagnation rule.

Recent protocol/firmware work had already improved internal branch memory and several practical leaves, but it would have been easy to spend another run on internal wording/index synchronization or broad schema-externalization phrasing. Instead, external research pushed the branch toward a narrower practical continuation with clearer operator value.

The resulting synthesis is deliberately conservative:
- service or method recovery is not yet replay readiness
- schema externalization is still not enough if there is no frozen representative replay object
- the smallest useful next target is usually one method fixture package and one minimal constructor path, not a whole client
- replay-gate debugging gets meaningfully easier once route identity, likely gate-bearing fields, and decoration are split explicitly

That is the practical value of this run:
- one smaller truthful replay boundary
- not another abstract protocol-methodology page

## Candidate topic pages to create or improve
Created this run:
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`

Improved this run:
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/protocol-schema-externalization-and-replay-harness-workflow-note.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `index.md`

Still-plausible future additions:
- a narrower note for request-correlation / pending-request ownership when representative fixtures already exist but one request-to-reply/completion join still dominates replay failure
- a case-driven cookbook section for mailbox/command protocols where fixture truth depends on ring/slot ownership rather than only message structure
- a practical continuation for fixture-backed compare design when the first bad field or reducer is now the main runtime-evidence question

## Next-step research directions
Near-term good directions:
- watch whether protocol/firmware case pressure clusters more around representative fixture construction or around later request-correlation / freshness / pending-request gates
- if the latter repeats, add a narrower continuation focused on request-correlation ownership rather than broad replay-gate taxonomy
- keep protocol branch growth case-driven and avoid drifting back into only internal wording/family-count/index maintenance

Broader branch-balance direction:
- continue resisting overfeeding browser/mobile dense branches by default
- keep using real external-research-driven runs on protocol/firmware, malware, or other thinner practical seams when recent runs have tilted too far toward internal upkeep

## Concrete scenario notes or actionable tactics added this run
The new practical note adds these concrete tactics:
- freeze exactly one representative method/opcode family
- preserve fixture provenance before making edits
- split request fields into:
  - route identity
  - likely gate-bearing
  - decorative / lower-priority
- choose one smallest constructor / serializer / invocation path instead of a large generic client surface
- build one compare-friendly fixture package
- prove one conservative edit that should not change method identity
- route quickly onward once the representative replay object exists

## Search audit
Search sources requested: `exa,tavily,grok`

Search sources succeeded: `exa,tavily,grok`

Search sources failed: `none`

Exa endpoint: `http://158.178.236.241:7860`

Tavily endpoint: `http://proxy.zhangxuemin.work:9874/api`

Grok endpoint: `http://proxy.zhangxuemin.work:8000/v1`

Queries used:
- `reverse engineering rpc method contract to replay fixture workflow`
- `reverse engineering protobuf grpc replay request from binary service contract`
- `windows rpc reverse engineering interface method replay workflow`
- `reverse engineering proprietary protocol captured method to minimal replay harness`

Notes on search quality:
- the multi-source search attempt was real and all three requested sources returned results
- source quality was mixed: Grok surfaced some useful directional pointers, but several returned items were secondary or anecdotal and were kept conservative
- Exa contributed weaker/topically noisy matches for this specific query set, which is recorded here rather than hidden
- Tavily contributed at least one useful RPC-interface reversing pointer, but also some tangential results
- because of that source mix, only a small retained source set was promoted into canonical workflow claims

## Branch-balance review
Recent branch pattern:
- several recent autosync runs have been strong on native practical workflows, runtime-evidence reductions, and some iOS practical growth
- the KB remains historically dense in browser anti-bot / request-signature and mobile protected-runtime / WebView work
- protocol/firmware practical routing is materially better than before, but still thinner in case-driven leaf density and practical continuation granularity than the densest branches

Balance judgment this run:
- this run was correctly spent on protocol/firmware deepening rather than another browser/mobile pass or pure canonical sync
- choosing the method-contract -> minimal-replay-fixture seam met the anti-stagnation rule because it produced a concrete, source-backed practical continuation page rather than only top-level wording repair
- the new page helps keep the protocol branch practical and case-driven instead of allowing schema-externalization to remain too broad

Current branch-strength impression:
- strong: browser anti-bot/request-signature; mobile protected-runtime/WebView; growing native practical workflows
- medium and improving: iOS practical reversing; runtime-evidence operator ladders
- still relatively thinner but valuable: protocol/firmware practical continuations, malware thinner-family practical notes, and some deobfuscation/runtime-obligation continuations

## Files changed
KB files changed this run:
- `research/reverse-expert-kb/topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md` (new)
- `research/reverse-expert-kb/sources/firmware-protocol/2026-03-22-method-contract-minimal-replay-fixture-notes.md` (new)
- `research/reverse-expert-kb/topics/protocol-firmware-practical-subtree-guide.md`
- `research/reverse-expert-kb/topics/protocol-schema-externalization-and-replay-harness-workflow-note.md`
- `research/reverse-expert-kb/topics/protocol-state-and-message-recovery.md`
- `research/reverse-expert-kb/topics/firmware-and-protocol-context-recovery.md`
- `research/reverse-expert-kb/index.md`

## Commit / sync status
Pending at report write time:
- commit KB changes if the working tree remains limited to intended reverse-KB files
- run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

Best-effort note:
- `.learnings/ERRORS.md` logging remains best-effort only and was not required for this run
