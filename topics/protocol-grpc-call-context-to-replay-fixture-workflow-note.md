# gRPC Call-Context to Replay Fixture Workflow Note

Topic class: workflow note
Ontology layers: protocol / firmware practical branch, service-contract replay, call-context proof, fixture construction
Maturity: draft-practical
Related pages:
- topics/protocol-firmware-practical-subtree-guide.md
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md
- topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md
- topics/protocol-schema-externalization-and-replay-harness-workflow-note.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/protocol-reply-emission-and-transport-handoff-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
Supporting source notes:
- sources/protocol/2026-05-09-grpc-call-context-replay-fixture-notes.md

## 1. Problem shape

Use this note when a target is gRPC / protobuf / service-stub shaped and the analyst already has some mixture of:

- a service and method route such as `/{package}.{Service}/{Method}`
- generated or recovered protobuf message types
- a captured request body, serialized protobuf blob, or request builder object
- a generated stub, interceptor, channel wrapper, or call-options object
- visible metadata, auth headers, tracing headers, authority/host routing, deadline/timeout settings, or cancellation behavior
- response status, initial metadata, trailing metadata, or stream close behavior

The recurring failure is collapsing all of that into one claim:

> “I recovered the request body, so replay should be comparable.”

That is often false. In gRPC-shaped cases, the proof object is narrower:

```text
one method body, under one call-context and lifecycle posture, reached one comparable handler/result boundary
```

This note starts after broad service-contract recovery. It is not the right entry point when the service shell is still unknown or the payload is still too layered to parse.

## 2. Core split

Keep these proof objects separate:

```text
service/method route known
  != protobuf body / stream slice recovered
  != metadata/header/trailer contract frozen
  != authority / credential / channel posture matched
  != deadline / timeout / cancellation lifecycle matched
  != final status and trailing metadata interpreted
  != handler-side consumer or durable effect proved
```

Compact branch memory:

```text
route/body != call-context != lifecycle != status/trailers != consumed/effected
```

A useful stop rule:

```text
same protobuf bytes != same RPC call
```

Do not reopen broad schema or field semantics until the call-context contract is honest enough for a like-for-like comparison.

## 3. Workflow

### Step 1 — Freeze the method route and body boundary

Record:

- package, service, and method name if available
- unary / server-streaming / client-streaming / bidi shape
- request and response message types
- body provenance: builder input, serialized protobuf bytes, intercepted gRPC message, stream slice, or handler argument
- compression and message-size assumptions when visible
- generated stub or dynamic invocation path that produced the call

Stop rule:

```text
method name visible != body provenance frozen != comparable fixture exists
```

If route or body provenance is still vague, go back to service-contract or schema-externalization work instead of inventing replay context.

### Step 2 — Preserve metadata as call-context truth

Record initial metadata / request headers separately from the protobuf body:

- authorization / bearer token / call credential placement
- tenant, device, experiment, locale, trace, request-ID, quota, or custom headers
- binary metadata keys
- server response initial metadata
- trailing metadata and application-specific error details
- header-size or server-limit sensitivity if it appears relevant

Stop rule:

```text
body field found != auth/routing metadata found != server policy path matched
```

Metadata is not decoration by default. Treat it as a candidate selector for auth, routing, rate limits, experiment gates, or detailed error semantics until a compare proves otherwise.

### Step 3 — Freeze authority, channel, and credential posture

Record:

- target authority / `:authority` / host override
- channel target and resolver/load-balancer path when visible
- TLS / ALPN / SNI assumptions if they affect server selection
- per-call credentials versus channel credentials
- interceptor chain or call-options object that mutates metadata or credentials
- whether the replay path uses the same generated stub or a lower-level transport recreation

Stop rule:

```text
endpoint reachable != same authority/credential posture != same server-side call
```

If a replay fails with `UNAUTHENTICATED`, `UNIMPLEMENTED`, or routing-shaped behavior, first test authority, credential, and metadata posture before assuming the protobuf body is wrong.

### Step 4 — Preserve deadline, timeout, and cancellation lifecycle

Record:

- deadline or timeout value and how it is represented by the language/runtime
- whether a parent incoming call propagates deadline/cancellation
- wait-for-ready / fail-fast posture if visible
- explicit cancellation, context destruction, channel shutdown, or stream close boundary
- expected response, no-response, timeout, cancellation, or deferred-completion behavior

Stop rule:

```text
request sent != deadline still live != handler finished != client observed same status
```

A body-identical replay can diverge because it expired too early, waited too long, skipped propagated cancellation, or failed to reproduce a half-close / stream close edge.

### Step 5 — Interpret status and trailers conservatively

For every failed or surprising call, record:

- status code and message
- whether the code is commonly library-generated, application-returned, or ambiguous
- initial metadata and trailing metadata
- whether response parsing, request parsing, compression, flow-control, method cardinality, auth, or deadline behavior could have generated the status before handler consequence
- whether the operation may have completed even though the client saw `DEADLINE_EXCEEDED`

Stop rule:

```text
status observed != payload schema fault proved != handler consequence disproved
```

Treat status as a discriminant, not a conclusion. The next proof object is usually which layer produced it.

### Step 6 — Build the minimal replay fixture as body plus context

A good first fixture package includes:

- method route and stream shape
- normalized request body and serialized bytes
- one smallest constructor path, preferably generated stub + request object when available
- metadata/header set and relevant trailers
- authority / host / credential posture
- deadline/timeout/cancellation posture
- expected status, response body, trailers, or completion artifact
- provenance for each field: observed, inferred, default, unknown, or intentionally omitted

Bad first fixtures include:

- raw protobuf bytes with no call metadata
- a generated request object with hidden interceptor state omitted
- a hand-built HTTP/2 replay that cannot say which stub/context options it preserved
- a full client recreation that hides the one method/context contract being tested

The useful artifact is small enough that a later analyst can mutate one body field or one context field without rediscovering the entire service.

### Step 7 — Use compare pairs before widening

Good compare pairs:

- same body, original metadata vs stripped metadata
- same body, same metadata, original authority vs alternate authority
- same body/context, short deadline vs original deadline
- same body/context, with vs without parent-call deadline propagation
- same unary body, one extra/missing stream message or half-close in streaming cases
- same body/context, same status but different trailers

Interpretation discipline:

```text
body-identical but context-different -> call-context problem first
context-identical but status-layer changes -> locate status producer
context-identical and accepted -> move to handler consumer / consequence proof
```

Leave this note once one comparable call fixture exists and the remaining bottleneck is clearly a replay precondition, handler state edge, committed output handoff, or durable external effect.

## 4. Observation surfaces

### Static / decompiled surfaces

Use for:

- generated stubs and service route strings
- request/response type references
- interceptor registration
- context/call-options construction
- metadata keys and authority setters
- deadline or timeout constants

Do not use alone for:

- live metadata values
- credential validity
- current authority / server selection
- deadline/cancellation timing
- handler consequence

### Runtime hook surfaces

Useful hook targets include:

- generated stub method invocation
- request builder finalization
- metadata add/set APIs
- client context / call options construction
- authority setter or channel target resolution
- credential attachment
- deadline / timeout setter
- cancellation / close / half-close methods
- initial metadata, trailing metadata, and status receipt

Preferred stop:

```text
stub call + request object + call-context object + status/trailers
```

That tuple is usually a better first proof object than raw HTTP/2 frames.

### Transport / proxy surfaces

Use for:

- HTTP/2 `:path`, `:authority`, metadata headers, trailers
- message compression and framing clues
- deadline/timeout header clues when visible
- response status and trailing error details

Do not use alone for:

- builder provenance
- hidden interceptor state
- credential derivation
- handler-side consumer

## 5. Common false positives

- treating a decoded protobuf body as the whole replay object
- assuming metadata keys are logging noise before comparing stripped vs original calls
- assuming `DEADLINE_EXCEEDED` means the server did nothing
- assuming `UNAUTHENTICATED` means only the token is wrong, when authority or credential compatibility may be wrong
- assuming `UNIMPLEMENTED` means a bad body rather than wrong path, cardinality, method registration, or server selection
- treating trailers as optional output instead of possible application error detail
- hand-building transport replay before proving the generated stub/context path is unusable

## 6. Handoff rules

Hand off to:

- `protocol-replay-precondition-and-state-gate-workflow-note` when body and call-context are comparable but the server still rejects on auth/session/freshness/state
- `protocol-parser-to-state-edge-localization-workflow-note` when the call reaches handler parsing and the missing proof is the first state/consequence edge
- `protocol-reply-emission-and-transport-handoff-workflow-note` when handler acceptance exists but committed response/trailer/output ownership is unclear
- `protocol-method-contract-to-minimal-replay-fixture-workflow-note` if the current fixture has grown too broad and needs to be shrunk back to one representative method object

## 7. Source-backed anchors

This workflow is grounded by gRPC documentation that treats metadata as HTTP/2 header/trailer side-channel state, deadlines and cancellation as independent call-lifecycle controls, status codes as potentially library- or application-generated, and `ClientContext`-style APIs as the place where metadata, deadline, authority, credentials, compression, cancellation, and metadata/status observation come together.
