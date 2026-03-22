# Source Notes — 2026-03-22 — gRPC / protobuf method-contract to minimal fixture continuation

## Source set
External sources consulted through explicit multi-source search (`exa,tavily,grok`):
- IOActive — *Breaking Protocol (Buffers): Reverse Engineering gRPC Binaries*
  - <https://www.ioactive.com/breaking-protocol-buffers-reverse-engineering-grpc-binaries/>
- Arkadiy Tetelman — *Reverse Engineering Protobuf Definitions from Compiled Binaries*
  - <https://arkadiyt.com/2024/03/03/reverse-engineering-protobuf-definitiions-from-compiled-binaries/>
- `pbtk` repository
  - <https://github.com/marin-m/pbtk>
- gRPC core concepts / dispatch framing
  - <https://grpc.io/docs/what-is-grpc/core-concepts>
- Kreya — *gRPC deep dive: from service definition to wire format*
  - <https://kreya.app/blog/grpc-deep-dive>
- Adversis — *Blind Enumeration of gRPC Services*
  - <https://www.adversis.io/blogs/blind-enumeration-of-grpc-services>

Existing KB pages consulted for fit:
- `topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- `topics/protocol-schema-externalization-and-replay-harness-workflow-note.md`
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- `topics/protocol-firmware-practical-subtree-guide.md`

## Why this batch was chosen
This batch was chosen because the protocol/firmware branch already had:
- service-contract extraction guidance
- schema externalization guidance
- replay-gate debugging guidance

But there was still a practical middle seam that often stalls real work:
- the analyst can name one method and may even have a `.proto` or descriptor,
- yet still does not have one **smallest truthful fixture package** to replay, mutate, compare, or preserve.

This batch was meant to sharpen that seam rather than widen protocol taxonomy again.

## Strong recurring ideas

### 1. Descriptor recovery is valuable, but it still does not choose the replay object for you
The protobuf descriptor extraction sources are useful because they show that many protobuf / gRPC targets leak a lot of recoverable structure:
- `FileDescriptorProto`-like data
- service names
- method names
- request/response type pairings
- enough shape to regenerate `.proto`-like artifacts

But that still leaves an operator gap:
- which single method should be frozen first?
- which captured request is the truthful representative fixture?
- which fields are routing identity versus per-call freshness baggage?

Useful durable rule:
- **descriptor recovery solves contract visibility, not fixture selection**.

### 2. gRPC path identity gives a compact route core for fixture reduction
The gRPC sources reinforce that one useful route-identity boundary often already exists in plain form:
- `/{package}.{Service}/{Method}`

Combined with message type pairing, this gives a compact route core for a representative replay object:
- path identity
- request message type
- response message type
- unary vs streaming direction

This is valuable because it helps separate:
- method identity
from
- metadata and state obligations layered around that method.

Durable rule:
- **for gRPC-like targets, freeze route identity first, then argue about metadata and freshness.**

### 3. Service registration / stub generation is often a better constructor anchor than raw frame replay
The IOActive material is especially useful because it keeps pointing back to generated structure:
- service descriptors
- stubs / generated methods
- ordered handler surfaces
- vtable- or registration-adjacent evidence

That supports a strong practical workflow:
- if a truthful generated or semi-generated constructor path exists,
- use that as the first fixture-construction boundary,
- rather than starting from hand-built HTTP/2 or packet replay.

Durable rule:
- **prefer one small constructor/stub path over immediate raw-frame heroics**.

### 4. Reflection-disabled targets do not erase the contract; they only remove the easiest enumeration surface
The blind-enumeration source is useful not because blind enumeration should become the default, but because it reminds us of a broader workflow lesson:
- absence of reflection is not the same thing as absence of a recoverable callable shell.

When reflection is unavailable, the contract may still be recoverable from:
- embedded descriptors
- generated client/server code
- stub registration paths
- endpoint path strings
- method tables
- compare pairs from live traffic

Durable rule:
- **when the easiest enumeration surface disappears, downgrade your confidence, not your discipline**.

### 5. Minimal replay fixtures should preserve method identity and provenance before they chase acceptance
A repeating workflow lesson across the sources is that analysts often jump too quickly from:
- “I know the method”
- to “I should replay the whole call now.”

What is usually missing is a compare-friendly fixture package with preserved provenance:
- where the request was captured
- whether it is pre-wrap or post-wrap
- what metadata was already ambient
- what transport or auth state was already satisfied

Durable rule:
- **a replay fixture is first an evidence object, then a sending object**.

### 6. Streaming shape is part of method identity, not optional decoration
The gRPC sources also reinforce a subtle but important point:
- unary, client-streaming, server-streaming, and bidirectional streaming are not small implementation details
- they directly affect what the “minimal fixture” even is

A truthful fixture package therefore needs to say whether the representative object is:
- one unary request/response pair
- one first client message in a stream
- one server-stream opening request plus one representative response frame
- one correlation slice from a bidi session

Durable rule:
- **stream shape belongs in the route-identity bucket, not the decoration bucket**.

## Concrete operator takeaways worth preserving

### A. Descriptor-first but fixture-aware reduction workflow
Reusable sequence:
1. recover service and message contract data if descriptor-like metadata exists
2. choose one method only
3. write down route identity (`package.service/method` or equivalent)
4. preserve one runtime capture with provenance
5. split the fixture into route core, likely gates, and decoration
6. only then build the minimal constructor or replay surface

### B. Constructor-anchor preference workflow
Reusable sequence:
1. prefer generated stub / builder / request-construction helpers when visible
2. if unavailable, prefer serializer entry over raw transport replay
3. only use raw frame recreation as the first surface when no smaller truthful constructor path exists
4. record which layer the fixture belongs to (builder object, protobuf bytes, gRPC body, HTTP/2 frame, etc.)

### C. Reflection-disabled conservative continuation
Reusable sequence:
1. do not assume service enumeration is impossible just because reflection is off
2. look for descriptor blobs, generated code, path strings, or registration code
3. if those remain weak, preserve live compare pairs instead of overclaiming method coverage
4. keep fixture scope narrow and provenance-heavy until contract confidence improves

### D. Streaming-aware fixture selection workflow
Reusable sequence:
1. classify the representative method as unary or streaming
2. decide what the smallest truthful replay object is for that shape
3. preserve one representative response/completion slice if the interaction is not unary
4. avoid pretending a single message blob captures the whole contract when stream shape is part of the real route identity

## Candidate KB implications
This batch most strongly supports improving:
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`

It also weakly supports future practical additions around:
- streaming-first fixture packages
- reflection-disabled service recovery
- method-path identity vs metadata/gate separation
- constructor-anchor choice when both generated stubs and raw captures exist

## Confidence / quality note
This batch is strong for:
- clarifying the practical gap between schema externalization and replay-gate debugging
- reinforcing route identity / constructor path / provenance as the main minimal-fixture ingredients

It is only medium-confidence for:
- tool-specific extraction shortcuts
- target-family-specific behavior once protobuf-lite, stripped code, or custom wrappers remove the obvious descriptor surfaces

That is acceptable for KB use because the resulting claims are workflow-centered and conservative.