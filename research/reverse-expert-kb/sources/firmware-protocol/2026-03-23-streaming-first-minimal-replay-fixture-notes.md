# Source Notes — 2026-03-23 — streaming-first minimal replay fixture continuation for gRPC / protobuf RPC reversing

## Source set
External sources consulted through explicit multi-source search (`exa,tavily,grok`):
- IOActive — *Breaking Protocol (Buffers): Reverse Engineering gRPC Binaries*
  - <https://www.ioactive.com/breaking-protocol-buffers-reverse-engineering-grpc-binaries/>
- gRPC core concepts
  - <https://grpc.io/docs/what-is-grpc/core-concepts/>
- Arkadiy Tetelman — *Reverse Engineering Protobuf Definitions from Compiled Binaries*
  - <https://arkadiyt.com/2024/03/03/reverse-engineering-protobuf-definitiions-from-compiled-binaries/>
- `pbtk` repository
  - <https://github.com/marin-m/pbtk>
- `grpcreplay` package / tooling signal
  - <https://pkg.go.dev/github.com/google/go-replayers/grpcreplay>
- gRPC reflection guide
  - <https://grpc.io/docs/guides/reflection/>
- David Vassallo — *Pentesting gRPC-Web: Recon and reverse-engineering*
  - <https://blog.davidvassallo.me/2018/10/27/pentesting-grpc-web-recon-and-reverse-engineering/>

Existing KB pages consulted for fit:
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- `topics/protocol-schema-externalization-and-replay-harness-workflow-note.md`
- `topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- `topics/protocol-firmware-practical-subtree-guide.md`

## Why this batch was chosen
This batch was chosen because recent protocol/firmware runs had already improved:
- service-contract extraction
- schema externalization
- minimal replay-fixture framing for unary-style cases

But a practical gap still remained in thinner, still-useful protocol work:
- once the analyst knows one method contract, what counts as the *smallest truthful fixture* when the call is streaming-shaped rather than unary?
- and how should the workflow behave when reflection is disabled, partial, or absent without collapsing into vague “just capture traffic” advice?

The goal of this batch was therefore not another general gRPC overview.
It was to sharpen the practical continuation from method contract -> fixture package for streaming-aware and reflection-disabled cases.

## Strong recurring ideas

### 1. Streaming shape changes what the minimal replay object actually is
The gRPC core material and IOActive reversing walkthrough both reinforce that unary, server-streaming, client-streaming, and bidi methods are not interchangeable from an operator point of view.

The smallest truthful replay object changes with stream shape:
- **unary**: one request plus one representative response or status result
- **server-streaming**: one opening request plus one representative early response slice and stream-end expectation
- **client-streaming**: one ordered request-message sequence plus one close/flush boundary and one resulting response
- **bidi**: one correlation slice that preserves interleaving, not just one isolated payload blob

Durable rule:
- **stream shape belongs in fixture identity, not just route identity.**

### 2. A bidi or client-stream fixture should preserve ordering boundaries before semantics are perfect
A recurring risk in streaming cases is to overcompress the fixture too early:
- one message is preserved
- but the close/half-close boundary is lost
- inter-message ordering is lost
- receive-side correlation is lost
- and later replay failure gets misdiagnosed as auth or schema drift

Durable rule:
- **for streaming methods, preserve the smallest truthful ordered slice, not merely the smallest payload.**

That means a valid first fixture may be:
- first two client messages plus close boundary
- first request plus first server event plus stream-finish status
- one short bidi send/recv interleave window with preserved relative order

### 3. Generated stubs and replay tooling are useful because they preserve call-shape semantics
The `grpcreplay` and generated-stub/tooling signals are useful not as universal solutions, but as workflow evidence that method invocation shape matters.

A good first replay surface often preserves:
- method path
- stream class
- metadata boundary
- per-message serialization
- message order
- close / half-close semantics

This supports a practical rule:
- **if a stub-level or call-level surface preserves stream semantics cleanly, prefer it over lower-level byte replay as the first fixture-construction boundary.**

### 4. Reflection-disabled does not mean service recovery is impossible; it means confidence should stay narrower
The reflection documentation is a helpful negative signal:
- reflection is optional
- many real systems disable it
- therefore lack of reflection is normal, not exceptional

The Arkadiy / `pbtk` / gRPC-Web reversing material reinforces the positive side:
- embedded descriptor or generated-code evidence may still exist
- path strings, registration code, stubs, and live compare pairs may still reveal enough for one representative method
- browser-side or generated-client material can sometimes recover callable shells even when the server stays opaque

Durable rule:
- **when reflection is absent, narrow the scope of the fixture claim instead of broadening speculation about the whole service.**

### 5. Fixture provenance should include stream role and closure semantics explicitly
For unary requests, provenance often stops at “captured here, serialized there.”
For streaming cases that is not enough.

Useful extra provenance fields include:
- whether the fixture is opener-only, mid-stream, close-bearing, or response-bearing
- whether client half-close already happened
- whether first server metadata / first response event was observed
- whether the slice is pre-framing, pre-compression, gRPC-message-body, or transport-visible

Durable rule:
- **stream fixtures need provenance for role-in-stream, not just layer-in-stack.**

### 6. Reflection-disabled and streaming-first often combine into a narrower, evidence-heavier workflow
When both are true:
- reflection is unavailable
- the target method is streaming

then the analyst should often avoid pretending they have a full reusable RPC client contract.
A smaller but more truthful success boundary is:
- one named or index-labeled method candidate
- one ordered fixture slice
- one statement of which ordering and close semantics are already proved
- one list of what still depends on ambient state or missing service visibility

Durable rule:
- **under partial visibility, prefer one truthful stream slice over one fake-complete method model.**

## Concrete operator takeaways worth preserving

### A. Streaming-first fixture selection workflow
Reusable sequence:
1. classify the method as unary / server-streaming / client-streaming / bidi
2. choose the smallest truthful ordered slice for that shape
3. preserve whether close / half-close / first server event is inside the slice
4. keep route identity and stream identity attached to the slice
5. only then test conservative field edits

### B. Reflection-disabled conservative continuation
Reusable sequence:
1. confirm reflection is absent or not usable
2. look for descriptor blobs, generated stubs, path strings, registration code, or client-side generated artifacts
3. if still weak, preserve one compare-friendly ordered live slice instead of overclaiming service coverage
4. label the method claim by path/index/evidence source, not by speculative full semantic name if confidence is weak

### C. Constructor-path choice for streaming cases
Reusable sequence:
1. prefer stub or helper surfaces that preserve stream role and closure semantics
2. if unavailable, prefer serializer boundaries for individual stream messages plus one explicit stream driver boundary
3. only fall back to raw transport replay first when no smaller truthful call-shape surface exists

### D. Compare-pair design for streaming fixtures
Reusable sequence:
1. hold route identity and stream ordering constant
2. mutate one payload field inside the same message position
3. avoid changing message count and close timing in the first compare pair
4. only after one stable compare pair exists, test ordering/count/close variations

## Candidate KB implications
This batch most strongly supports improving:
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`

It also supports small canonical-sync improvements for:
- `index.md` protocol/firmware branch summary, so this thinner continuation is remembered at the top level instead of living only in a leaf

## Confidence / quality note
This batch is strong for:
- preserving streaming-aware stop rules
- clarifying fixture identity for non-unary methods
- clarifying reflection-disabled conservative workflow behavior

It is medium-confidence for:
- tool-specific replay shortcuts
- target-family-specific streaming details once wrappers, proxies, or custom envelopes distort ordinary gRPC expectations

That is acceptable for KB use because the resulting claims stay workflow-centered, conservative, and operator-facing.
