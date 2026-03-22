# Source Notes — 2026-03-22 — Method contract -> minimal replay fixture / harness

## Source set
Search mode and policy:
- explicit multi-source search via `search-layer` with `--source exa,tavily,grok`
- queries centered on RPC/service contract recovery, representative replay fixtures, and method-level replay construction

Primary retained sources reviewed:
- <https://www.ioactive.com/breaking-protocol-buffers-reverse-engineering-grpc-binaries/>
- <https://clearbluejar.github.io/posts/surveying-windows-rpc-discovery-tools/>
- <https://blog.xpnsec.com/analysing-rpc-with-ghidra-neo4j/>
- <https://people.eecs.berkeley.edu/~dawnsong/bitblaze/protocol.html>

Search-only / degraded-quality signals kept conservative:
- Grok-returned pointers to grpc replay / fixture tooling and gRPC reversing walkthroughs
- Tavily result pointing to ZDI RPC interface-reversing material
- one direct `web_fetch` attempt to Arkadiy Tetelman’s protobuf-descriptor article failed during this run and was therefore not treated as a fresh source for this note

Existing KB materials consulted for fit:
- `topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- `topics/protocol-schema-externalization-and-replay-harness-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-firmware-practical-subtree-guide.md`

## Why this source cluster was chosen
Recent protocol/firmware runs had already improved:
- service-contract / method-dispatch recovery
- schema externalization / replay-harness framing
- reply emission, replay gating, and mailbox/output-side notes

But there was still a practical gap between:
- **recovering one representative method contract**, and
- **having one small, truthful, compare-friendly replay object**.

This source cluster was chosen to answer a narrower operator question:
- once one service/method shell is recovered, what should the first reusable replay boundary look like before state-gate debugging starts?

## Strong recurring ideas

### 1. Service recovery is not yet replay readiness
The IOActive gRPC article is useful here because it shows how much valuable information can be recovered statically:
- server registration surfaces
- service implementation objects
- vtable ordering
- per-method implementations

That is important, but it also highlights a gap:
- knowing the service and method shell does **not** automatically produce one representative replay object
- there is still a reduction step from method-bearing contract to one reusable request/response fixture or constructor path

### 2. RPC discovery tooling teaches where procedure truth lives, not what the first fixture should be
The Clear Blue Jar and XPN RPC materials are strong on:
- interface enumeration
- procedure discovery
- dispatch tables
- interpreter/server info structures

These sources reinforce a practical rule:
- discovery tells you where method truth lives
- but replay work still needs one deliberately chosen procedure/opnum/method fixture
- otherwise analysts keep widening interface inventory instead of freezing one compare-friendly call object

### 3. Dialogue replay is the useful practical endpoint, but it needs a representative unit
The BitBlaze/Reverser framing is still valuable because it keeps protocol RE anchored to application dialogue replay rather than taxonomy.

The extra practical lesson from this run is:
- dialogue replay becomes actionable only after the analyst chooses one smaller replay unit
- usually one method, one opcode family, one argument bundle, or one request/response pair
- not the whole service surface at once

### 4. Minimal fixture quality matters more than broad fixture quantity
Across the retained sources, a durable rule emerged:
- the first replay object should be **representative and inspectable**, not merely numerous
- a large pile of captures is weaker than one clearly sourced fixture whose method identity, request body, and expected response/completion behavior are explicit

### 5. Method identity, gate-bearing state, and decoration should be separated early
This run reinforced a practical split that the KB needed more explicitly:
- some parts of the request define the route/method identity
- some parts probably carry freshness/auth/session/pending-request obligations
- some parts are likely optional metadata or decoration

Without this split, replay-gate debugging becomes mushy because every field remains equally mysterious.

### 6. The first harness should expose missing obligations, not hide them
A useful anti-drift lesson:
- if the first “working” harness silently drags half a live process or giant session bootstrap behind it, it may hide the real acceptance gates
- the better first surface is one minimal constructor / serializer / invocation path that makes missing obligations obvious

## Concrete operator takeaways worth preserving

### A. Freeze one representative method, not the service family
When service recovery is already good enough:
1. choose one method/opnum/opcode family
2. preserve one request fixture and response/ack/completion evidence if available
3. stop broad interface inventory work there

### B. Preserve provenance before editing
For the first replay-worthy fixture, preserve:
1. where it was captured
2. whether it is pre-wrap, serialized body, or builder input
3. what environment assumptions were already true

This prevents later schema or gate conclusions from floating free of the observation boundary.

### C. Use a three-bucket field split
For the chosen request, separate:
1. route/method identity
2. likely gate-bearing fields
3. decorative / lower-priority fields

This is good enough even when names remain generic.

### D. Prefer one minimal constructor path
The first useful harness should usually be:
1. one method stub / builder / serializer path
2. one representative request object
3. one conservative mutation or compare pair

Not:
- full client reimplementation
- broad method coverage
- giant environment-carrying wrapper code

### E. A good first fixture package should support compare design
A small good package should let a later analyst:
- diff two requests
- test one benign edit
- swap one likely gate-bearing field
- observe whether failure changes category

That makes the fixture package a bridge into replay-gate work rather than a dead sample archive.

## Candidate KB implications
This source batch supports a narrower practical leaf in the protocol / firmware branch:
- a page after service-contract extraction and schema externalization
- focused on **method contract -> minimal replay fixture / harness**
- explicitly separating representative fixture construction from later acceptance-gate debugging

Likely parent-page implications:
- the protocol branch should remember that “replay harness” is still too broad once a method contract already exists
- there is real operator value in preserving one smaller step: freezing a representative replay object before wider gate or output debugging

## Confidence / quality note
This run’s external research was useful, but mixed in source quality:
- IOActive, Clear Blue Jar, XPN, and BitBlaze were strong enough to support conservative workflow claims
- search-layer also returned weaker or noisier results, especially from Grok-only snippets and tangential Exa/Tavily matches
- because of that, the synthesis is intentionally workflow-shaped and conservative rather than tool- or product-specific
