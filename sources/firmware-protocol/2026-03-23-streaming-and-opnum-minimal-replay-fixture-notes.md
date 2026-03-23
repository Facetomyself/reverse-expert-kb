# Source Notes — 2026-03-23 — streaming / half-close and opnum-level minimal replay fixture continuation

## Source set
External sources consulted through explicit multi-source search (`exa,tavily,grok`):
- IOActive — *Breaking Protocol (Buffers): Reverse Engineering gRPC Binaries*
  - <https://www.ioactive.com/breaking-protocol-buffers-reverse-engineering-grpc-binaries/>
- Arkadiy Tetelman — *Reverse Engineering Protobuf Definitions from Compiled Binaries*
  - <https://arkadiyt.com/2024/03/03/reverse-engineering-protobuf-definitiions-from-compiled-binaries/>
- `pbtk` repository
  - <https://github.com/marin-m/pbtk>
- gRPC reflection guide
  - <https://grpc.io/docs/guides/reflection>
- gRPC half-close / END_STREAM discussion
  - <https://groups.google.com/g/grpc-io/c/M2sCDFw8vT8>
  - <https://stackoverflow.com/questions/67610502/how-do-i-perform-a-half-close-on-a-grpc-bidirectional-stream-using-tonic>
  - <https://github.com/hyperium/tonic/issues/1066>
- Windows RPC interface / opnum reversing material
  - <https://posts.specterops.io/uncovering-rpc-servers-through-windows-api-analysis-5d23c0459db6>
  - <https://www.akamai.com/blog/security-research/rpc-toolkit-fantastic-interfaces-how-to-find>
  - <https://shelltrail.com/research/manageengine-adaudit-reverse-engineering-windows-rpc-to-find-cve-2024-36036-and-cve-2024-36037-part1>

Search trace archived separately via:
- `/tmp/reverse-kb-2026-03-23-1216-search.txt`

Existing KB pages consulted for fit:
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- `topics/protocol-schema-externalization-and-replay-harness-workflow-note.md`

## Why this batch was chosen
Recent protocol/firmware work had already established:
- service-contract extraction
- schema externalization
- a first practical note for method-contract -> minimal replay fixture
- a narrower streaming-oriented continuation

But one practical gap still remained under-preserved in canonical memory:
- the minimal replay object is not just “a sample request”
- for streaming RPC it must preserve ordered slice and close semantics
- for Windows RPC it often needs to be remembered as one representative **opnum + argument bundle + binding/context handle assumptions** rather than as a broad interface inventory

This batch was chosen to strengthen those narrower operator rules.

## Strong recurring ideas

### 1. Stream shape belongs in fixture identity, not just route identity
The gRPC sources reinforce that unary, server-streaming, client-streaming, and bidi methods need different fixture boundaries.

Durable rule:
- a minimal replay fixture for streaming work is often an **ordered slice** plus the relevant **close / half-close boundary**
- not just one isolated payload blob

That means the first truthful fixture may be:
- first request plus first server event
- first two client messages plus explicit client half-close
- one short bidi interleave window with preserved relative order

### 2. Half-close is often a behavior-bearing boundary, not transport trivia
The gRPC half-close references were useful because they expose a common analyst failure mode:
- the request payload shape looks right
- per-message serialization looks right
- but the interaction still stalls, times out, or appears semantically incomplete
- because the stream-finish / half-close signal was never reproduced truthfully

Durable rule:
- when a streaming RPC only yields the decisive reply or completion after client close / half-close, the close boundary must be treated as part of the representative fixture contract
- do not treat it as optional replay polish

### 3. Reflection-disabled cases should narrow claims, not widen speculation
Reflection is optional and often absent.
Descriptor extraction, embedded metadata recovery, generated stubs, path strings, and client-side artifacts still help — but when those are partial, the right move is to freeze one narrower truthful fixture instead of pretending to recover the full service.

Durable rule:
- if reflection is unavailable, label the fixture around the evidence actually proved:
  - route/path/opnum candidate
  - ordered request slice
  - close semantics if applicable
  - argument bundle or context-handle assumptions if known

### 4. Windows RPC replay readiness is usually one opnum call bundle, not full interface coverage
The SpecterOps / Akamai / Shelltrail-style material reinforced a practical point that the KB should preserve more explicitly:
- interface UUID, endpoint, and opnum discovery are necessary
- but replay becomes practical only after freezing one representative **call bundle**

A good first Windows RPC replay object is often:
- interface UUID / endpoint / binding shape
- opnum identity
- one representative argument bundle
- one statement of whether context handles, authn level, transfer syntax, or connection-bound state are still ambient obligations

Durable rule:
- for opnum-oriented protocols, the right minimal fixture is usually **opnum + representative arguments + binding/context assumptions**, not raw packet inventory or broad IDL folklore.

### 5. The first harness should preserve method/opnum semantics before broad client recreation
Across both gRPC and Windows RPC sources, a useful shared lesson held up:
- prefer the smallest stub / helper / builder / invocation path that preserves callable semantics
- avoid first-harness designs that hide missing obligations inside giant client setup or broad framework glue

### 6. Provenance for fixtures should include lifecycle role
For this class of work, provenance should record not just stack layer but also lifecycle role:
- opener / mid-stream / close-bearing / response-bearing
- pre-wrap / serialized body / framed request / stub arguments
- live binding state and ambient obligations already true at capture time

That extra provenance is what keeps later replay-gate debugging honest.

## Concrete operator takeaways worth preserving

### A. Streaming fixture rule
For streaming RPCs:
1. classify unary vs server-stream vs client-stream vs bidi
2. preserve the smallest truthful ordered slice
3. explicitly record whether client half-close / close is inside the slice
4. do not let the first compare pair change message count or close timing

### B. Reflection-disabled rule
When reflection is absent:
1. try descriptor blobs, generated stubs, path strings, registration surfaces, or client artifacts
2. if still partial, freeze one narrow route/path/opnum fixture rather than speculating about the full service
3. make confidence boundaries explicit in the fixture package

### C. Windows RPC representative call-bundle rule
For Windows RPC / MIDL-shaped cases:
1. freeze one interface + endpoint + opnum target
2. preserve one representative argument bundle
3. separately mark context handles, auth/session/binding, and transfer-syntax assumptions
4. avoid widening into whole-interface inventory before one call object is replay-worthy

### D. Conservative compare design rule
For the first compare pair:
1. hold route/opnum identity constant
2. hold stream ordering and close semantics constant when streaming is involved
3. mutate one benign payload/argument field first
4. only later vary correlation/auth/session/close timing

## Candidate KB implications
This batch most strongly supports:
- strengthening `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- tightening subtree-guide wording so this thinner seam is remembered canonically, not only in leaf/source notes

## Confidence / quality note
This batch is strong for:
- streaming fixture identity and half-close stop rules
- reflection-disabled conservative workflow behavior
- the Windows RPC reduction from interface discovery to one opnum-level representative call bundle

It is medium-confidence for:
- tool-specific replay shortcuts
- target-specific transport edge cases once wrappers or custom runtimes distort the usual stack

That is acceptable here because the resulting KB claims remain workflow-centered, conservative, and operator-useful.
