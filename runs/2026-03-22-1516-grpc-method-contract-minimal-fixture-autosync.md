# Reverse KB Autosync Run — 2026-03-22 15:16 Asia/Shanghai

Mode: external-research-driven

## Scope this run
This run was chosen as a real external-research pass, not another internal-only canonical sync.

Chosen scope:
- review recent autosync direction and branch balance
- deliberately avoid overfeeding already-dense browser/mobile micro-branches
- perform explicit multi-source search through `search-layer --source exa,tavily,grok`
- stay on a thinner but still practical protocol/firmware seam
- materially improve the existing `protocol-method-contract-to-minimal-replay-fixture` leaf rather than polishing top-level wording
- add a new source note and run report, then commit and sync if KB files changed

## New findings
This run reinforced a narrow but important practical gap in the protocol branch:
- service-contract extraction tells you what callable shell exists
- schema externalization gets message structure out into reusable artifacts
- but real replay work still stalls if there is no preserved **minimal fixture package** for one chosen method

Material improvements made this run:
- added `sources/firmware-protocol/2026-03-22-grpc-method-contract-minimal-fixture-notes.md`
- materially strengthened `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`

The page now preserves several more concrete operator rules:
- for gRPC-like cases, freeze route identity first as method path + request/response type pairing + stream shape
- treat streaming shape as part of route identity, not decoration
- prefer a generated stub / builder / serializer entry as the first fixture-construction boundary before raw transport replay
- preserve fixture layer and provenance explicitly
- when reflection is unavailable, fall back conservatively to descriptor blobs, generated-code evidence, path strings, registration code, or live compare pairs instead of overclaiming service coverage

## Sources consulted
External sources retained or materially used:
- IOActive — *Breaking Protocol (Buffers): Reverse Engineering gRPC Binaries*
  - <https://www.ioactive.com/breaking-protocol-buffers-reverse-engineering-grpc-binaries/>
- Arkadiy Tetelman — *Reverse Engineering Protobuf Definitions from Compiled Binaries*
  - <https://arkadiyt.com/2024/03/03/reverse-engineering-protobuf-definitiions-from-compiled-binaries/>
- `pbtk` repository
  - <https://github.com/marin-m/pbtk>
- gRPC core concepts
  - <https://grpc.io/docs/what-is-grpc/core-concepts>
- Kreya — *gRPC deep dive: from service definition to wire format*
  - <https://kreya.app/blog/grpc-deep-dive>
- Adversis — *Blind Enumeration of gRPC Services*
  - <https://www.adversis.io/blogs/blind-enumeration-of-grpc-services>

Internal/canonical sources consulted:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent `research/reverse-expert-kb/runs/*.md`
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- `topics/protocol-schema-externalization-and-replay-harness-workflow-note.md`
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`

## Reflections / synthesis
This was the right kind of protocol/firmware run for the current branch state.

The protocol branch already had practical leaves, but it was still easy to drift into either:
- broad schema externalization language, or
- internal maintenance without enough new practical pressure.

The external search batch supported a more useful continuation:
- treat descriptor recovery as contract visibility, not as automatic replay readiness
- reduce one chosen method into a route core plus likely gate-bearing fields plus decoration
- preserve one truthful fixture as an evidence object before treating it as a sending object
- use generated stubs / builders when available, because they often give a cleaner fixture-construction boundary than raw transport emulation

This keeps the branch practical and case-driven.
It improves the existing leaf rather than creating another abstract side-page.

## Candidate topic pages to create or improve
Improved this run:
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`

Added this run:
- `sources/firmware-protocol/2026-03-22-grpc-method-contract-minimal-fixture-notes.md`

Still-plausible future additions:
- a narrower workflow note for streaming-first fixture packages where unary-style fixture assumptions are misleading
- a practical note for reflection-disabled gRPC / RPC service recovery when descriptors are partial and live compare pairs dominate
- a smaller continuation for deciding when to leave fixture reduction and enter pending-request correlation or freshness-gate debugging

## Next-step research directions
Good next directions for the thinner protocol branch:
- look for repetition around streaming or async reply shapes, and only then split a narrower child note
- keep practical pressure on protocol/firmware rather than letting the branch settle into only routing/index maintenance
- continue preferring concrete operator continuations over broad family-count polishing

Cross-branch direction:
- protocol/firmware remains thinner than browser/mobile and still deserves periodic external-research-driven passes
- malware and deobfuscation also remain candidates for similarly practical, source-backed branch deepening

## Concrete scenario notes or actionable tactics added this run
Concrete tactics newly preserved or sharpened this run:
- for gRPC-like targets, freeze route identity as:
  - `/{package}.{Service}/{Method}`
  - request/response type pairing
  - stream shape
- treat stream shape as part of method identity
- prefer one generated stub / builder / serializer entry over immediate raw HTTP/2 or packet recreation
- preserve whether the fixture is:
  - builder input
  - serialized protobuf body
  - gRPC message body
  - framed request
  - transport-visible unit
- when reflection is off, reduce confidence and narrow scope instead of pretending method coverage is complete

## Search audit
Search sources requested: `exa,tavily,grok`

Search sources succeeded: `exa,tavily,grok`

Search sources failed: `none`

Exa endpoint: `http://158.178.236.241:7860`

Tavily endpoint: `http://proxy.zhangxuemin.work:9874/api`

Grok endpoint: `http://proxy.zhangxuemin.work:8000/v1`

Queries used:
- `grpc reverse engineering protobuf service contract method dispatch workflow`
- `gRPC reverse engineering service descriptor protobuf method dispatch Android app`
- `protobuf rpc reverse engineering service contract extraction method handler dispatch`

Search quality notes:
- this was a real explicit three-source search attempt, satisfying the anti-stagnation external-research requirement
- all requested sources returned results
- result quality was mixed, but sufficient to support conservative workflow-level improvements
- Exa and Grok were especially useful for descriptor / gRPC binary reversing pointers
- Tavily contributed useful overlap and some noisier general-content hits, which were filtered conservatively

## Branch-balance review
Current balance impression:
- still strong / historically dense: browser anti-bot, request-signature, mobile protected-runtime, WebView hybrid loops
- improving: native practical runtime-evidence leaves, iOS practical continuations
- still thinner but high-value: protocol/firmware continuations, malware practical leaves, deeper deobfuscation case-driven reductions

Judgment this run:
- this run correctly spent effort on protocol/firmware instead of another dense-branch polish pass
- it also avoided another mostly internal wording/index-only maintenance loop
- improving an existing practical leaf with source-backed operator detail was the right anti-stagnation move for the current window

## Files changed
KB files changed this run:
- `research/reverse-expert-kb/topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- `research/reverse-expert-kb/sources/firmware-protocol/2026-03-22-grpc-method-contract-minimal-fixture-notes.md`
- `research/reverse-expert-kb/runs/2026-03-22-1516-grpc-method-contract-minimal-fixture-autosync.md`

## Commit / sync status
Pending at report write time:
- commit intended reverse-KB changes
- run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

Best-effort note:
- `.learnings/ERRORS.md` logging was not required for this run and remains best-effort only
