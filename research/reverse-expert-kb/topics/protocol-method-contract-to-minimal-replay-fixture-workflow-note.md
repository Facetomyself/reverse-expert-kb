# Protocol Method-Contract to Minimal Replay-Fixture Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, protocol/service contract externalization, representative replay surface construction
Maturity: practical
Related pages:
- topics/protocol-firmware-practical-subtree-guide.md
- topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md
- topics/protocol-schema-externalization-and-replay-harness-workflow-note.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/protocol-reply-emission-and-transport-handoff-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/analytic-provenance-and-evidence-management.md
Supporting source notes:
- sources/firmware-protocol/2026-03-21-schema-externalization-and-replay-harness-notes.md
- sources/firmware-protocol/2026-03-22-grpc-method-contract-minimal-fixture-notes.md
- sources/firmware-protocol/2026-03-23-streaming-first-minimal-replay-fixture-notes.md
- sources/firmware-protocol/2026-03-23-streaming-and-opnum-minimal-replay-fixture-notes.md
- sources/firmware-protocol/2026-03-23-opnum-and-timeout-lifecycle-minimal-replay-notes.md

## 1. When to use this note
Use this note when a protocol or RPC-shaped case has already progressed far enough that:
- one representative method shell, opcode family, RPC endpoint, or request/response contract is already trustworthy enough to name
- schema or message structure is already externalized enough to build objects outside the target
- but the analyst still does **not** have one small, truthful, reusable replay surface
- and the next bottleneck is no longer broad contract recovery, yet not fully reduced into narrow replay-gate debugging either

Typical entry conditions:
- a service/method family is already visible, but replay is still trapped in ad hoc notes or packet scraps
- a `.proto`, IDL-like shell, request builder shape, or serializer input model already exists, but there is no single representative fixture pair or constructor path
- several candidate fields exist, but the analyst still has not separated **must-match replay identity** from **safe-to-ignore decoration**
- the case keeps oscillating between schema polishing and replay-gate guesses because no minimal fixture/harness boundary has been frozen

Use it for cases like:
- gRPC / protobuf service families where one method contract is known and the next useful output is one fixture-backed request constructor or replay script
- streaming RPC families where the missing practical object is one truthful ordered slice plus one close / half-close boundary rather than just one payload blob
- Windows RPC or custom RPC families where one operation stub or opnum is known and the analyst needs one smallest argument bundle worth replaying
- proprietary framed protocols where one opcode + payload shape is already recovered and the missing step is shrinking it into one mutation-safe fixture surface
- firmware command/mailbox cases where one command family is already credible and the next useful object is one representative command fixture plus the few sequence / nonce / state assumptions that still matter

Do **not** use this note when:
- the service shell or representative method contract is still implicit
- the visible object is still too layered and schema/service externalization has not happened yet
- local acceptance is already partly visible and the only remaining problem is freshness/auth/session gating
- the real missing edge is already the committed send/output path rather than the representative replay surface

In those cases, start with:
- `topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- `topics/protocol-schema-externalization-and-replay-harness-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`

## 2. Core claim
A recurring practical gap appears after service-contract recovery and basic schema externalization:
- the analyst can describe one representative method
- may even parse or construct its messages outside the target
- but still cannot point to one **smallest truthful replay object** that should be preserved, edited, compared, or re-sent

The useful next output is usually not:
- more top-level protocol taxonomy
- full client reimplementation
- support for every method in the service
- broad field renaming and beautification

It is:
- one representative method fixture set
- one smallest constructor / serializer path for that fixture
- one short split between invariant request identity, likely-gated fields, and safely-ignored decoration
- one explicit split between **message/body identity truth** and **call-context truth** when the family carries meaningful per-call semantics outside the payload
- one minimal replay/edit harness that keeps later gate debugging honest

This note exists to keep the branch practical:
- **freeze one representative method replay surface before broadening into whole-client folklore**

## 3. Target pattern
The recurring shape is:

```text
one representative method contract already exists
  -> schema/externalization is already good enough to build messages
  -> but replay still lacks one frozen fixture and one smallest constructor path
  -> reduce to one request/response or request-only fixture family
  -> separate must-match fields from likely-gates and decoration
  -> build one minimal replay/edit surface
  -> then continue into state-gate or output-side proof
```

The important distinction is:
- `protocol-schema-externalization-and-replay-harness` gets the contract **out of the analyst’s head**
- this note gets the contract into one **representative, compare-friendly replay object**

## 4. What counts as a good minimal replay fixture
Treat these as good first targets:
- one request fixture and one matching response fixture for a single method
- one request fixture with a known expected no-response / ack / completion behavior, if responses are deferred or hidden
- one constructor input object plus the serialized bytes it emits
- one fixture pair captured from a truthful runtime path, with clear provenance about where it was observed
- one fixture family where the method/opcode identity, framing, and message body are all explicit
- for streaming RPC, one **ordered slice** plus the relevant close / half-close semantics
- for Windows RPC, one **opnum-level representative call bundle**: interface/binding target, opnum identity, argument bundle, and explicit context/auth assumptions

Treat these as weaker and usually incomplete:
- raw pcap slices without method identity
- isolated blobs with no statement of which serializer/builder produced them
- a giant corpus of many messages but no chosen representative family
- one replay script that silently bakes in hidden ambient state and gives no reduced fixture boundary
- generic “sample request” docs with no proof they correspond to the recovered live method contract
- for streaming methods, one payload blob that omits ordering or close semantics
- for Windows RPC, a full interface inventory with no single replay-worthy call object

## 5. Practical workflow

### Step 1: Freeze exactly one representative method family
Pick one method only.

Good choices:
- simplest consequence-bearing request family
- smallest request family that consistently reaches parser acceptance
- one method whose request/response pair already has stable captures
- one mailbox/command family whose publish/completion chain is already plausible enough to compare later
- for Windows RPC, one opnum whose argument shape and callable path are already plausible enough to preserve as a single call bundle

Bad choices:
- the busiest or most feature-rich method just because it looks central
- multiple sibling methods at once
- a method family whose only evidence is vague naming rather than one captured or reconstructed contract

Write down:
- method/opcode/path identity
- request shape already believed to be true
- response/ack expectation if known
- stream class if relevant: unary, server-streaming, client-streaming, or bidi
- for Windows RPC, binding / endpoint / interface UUID assumptions if already known
- why this family is the chosen representative replay target

### Step 2: Preserve provenance for the fixture source
Before editing anything, preserve where the fixture came from.

Record:
- capture boundary or runtime boundary
- whether bytes are pre-wrap, post-wrap, plaintext, serialized object, or builder input
- whether the fixture is request-only, request/response, request/completion-derived, or stream-slice-derived
- for streaming cases, whether the slice includes opener, mid-stream messages, half-close, first server event, or completion edge
- what environment assumptions were already true at capture time

This matters because later replay failures are often not schema failures at all; they are provenance failures.

### Step 3: Reduce the request into four buckets
For the representative request, explicitly separate the replay object into four buckets:

1. **identity / routing core**
   - method name, opcode, path, service ID, opnum
   - stream shape if it is part of the callable contract
   - message body fields that select the code path or semantic family
2. **call-context truth**
   - per-call metadata or invocation context that may not live inside the serialized body, but still changes whether the same body is treated as the same practical call
   - for gRPC-like families: deadline/timeout posture, metadata/header set, authority/host routing assumptions, and call-credential or auth-token placement when they are carried outside the body
   - for Windows RPC-like families: binding-handle / endpoint assumptions, authentication level or service assumptions, and context-handle posture when the same argument bundle only makes sense under one live binding/context family
3. **likely gate-bearing fields**
   - nonce, timestamp, session, auth token, sequence, pending-request ID, device/context binding, context handle assumptions
4. **decoration / low-priority fields**
   - optional metadata, logging hints, cosmetic labels, duplicated mirrors, seemingly inert padding when not part of MAC/signature coverage

For gRPC-like families, a compact first route core is often already available as:
- `/{package}.{Service}/{Method}`
- request message type
- response message type
- unary vs client-streaming vs server-streaming vs bidi shape

But gRPC-like fixture work should now preserve one extra stop rule:
- do not flatten **body truth** and **call-context truth** into the same bucket
- the same protobuf body can still produce a practically different call when deadline posture, metadata, authority, or call-credential routing differ
- if replay fails after the body already looks stable, first ask whether the fixture froze the same call-context contract before reopening broad payload semantics

For Windows RPC-like families, a compact first route core is often:
- interface UUID or interface binding target
- endpoint or transport family if known
- opnum
- one representative argument family

And Windows RPC-like fixture work should preserve the same extra stop rule:
- do not treat opnum plus arguments as the whole replay object when one binding family, authn level, or context-handle posture still decides whether the call is even comparable
- if one live call bundle only works under one narrower binding/context contract, freeze that separately instead of smearing it into vague “ambient runtime state”

A practical lifecycle rule worth preserving here is:
- if the representative call is async-, timeout-, or completion-shaped, fixture identity may also need one explicit statement of deadline/timeout posture and what counts as the expected completion artifact
- otherwise later `timeout`, `cancel`, or stale/late reply behavior can be misread as argument-shape failure when the real difference is request lifecycle reproduction

A practical compare rule worth preserving here is:
- if two runs keep the same body / opnum / route core but diverge in deadline posture, metadata/header set, authority/host routing, binding-handle family, authn posture, or context-handle lineage, do not reopen broad body semantics first
- treat that pair as **body-identical but call-context-different** until one truthful like-for-like call has been frozen
- only after call comparability is honest should later accept/reject behavior be overread as replay-gate or payload proof

The goal is not perfect semantics.
The goal is to stop treating every field as equally mysterious.
The related goal is to stop pretending that every meaningful replay obligation lives inside the message body.

### Step 4: Prefer one constructor path over many serializers
If multiple ways to build the request are visible, choose the smallest trustworthy constructor path.

Prefer:
- one method stub invocation path
- one generated client helper
- one builder object path
- one serializer call chain that only touches the chosen request family
- for streaming RPC, one call-level surface that preserves message order and close / half-close semantics
- for Windows RPC, one stub/helper/invocation path that preserves opnum and argument shape before broad transport recreation

Prefer these before:
- hand-built HTTP/2 or transport framing
- raw packet/frame replay
- a large generic client shell that hides which layer actually owns the request

Avoid building the first harness on top of:
- a giant generic session bootstrap script
- a monolithic transport client covering unrelated methods
- a path that only works because it drags half the live process along invisibly

The first harness should answer:
- what is the smallest code path that turns the representative fixture object into bytes or an outbound call?

A useful rule for protobuf / gRPC families is:
- if a generated or registration-adjacent stub path exists, it is usually a better first fixture-construction boundary than hand-authored transport replay
- use raw transport recreation first only when no smaller truthful constructor path is available

### Step 5: Build one compare-friendly fixture package
A good fixture package usually contains:
- one normalized request object or schema-backed text representation
- one serialized request sample
- one response / ack / completion sample if available
- one short note of the environment and gate assumptions
- one explicit note of **call-context truth** when the family carries meaningful per-call semantics outside the body
- one table or bullet list marking which fields are believed stable, variable, or unknown

Also preserve the layer and provenance explicitly:
- whether the fixture is a builder input, serialized protobuf body, gRPC message body, framed request, stream-slice, transport-visible unit, or stub-argument bundle
- where it was captured or reconstructed from
- whether reflection / descriptor metadata was available or whether the fixture was recovered under a weaker compare-driven model
- for gRPC-like families, whether the package preserves deadline/timeout posture, metadata/header set, authority/host assumptions, and any call-credential placement that materially changes the call outside the body
- for streaming methods, whether ordering and close semantics are preserved inside the fixture package
- for Windows RPC, whether the package already includes binding/context assumptions, authn-level/auth-service assumptions, or still depends on ambient runtime state
- for async / timeout-sensitive methods, whether the package preserves the original call lifecycle closely enough to explain expected `success`, `timeout`, `cancel`, `late reply`, or deferred-completion behavior

Keep the package small enough that a later analyst can:
- diff two runs
- mutate one field
- swap one likely gate-bearing field
- confirm that failures moved for the expected reason

### Step 6: Prove one edit that should not change method identity
Before attempting live replay, make one conservative edit.

Good edits:
- a benign string or count field that should stay inside the same method family
- one payload field that should change business content but not routing
- one optional field removal if it is believed decorative
- for streaming cases, one payload-field change while holding message count, ordering, and close timing constant
- for Windows RPC, one argument change while holding opnum, binding, and context assumptions constant

This proves the fixture is not just a dead recording artifact.
It gives a compare pair that helps separate route identity from gate-bearing obligations.

### Step 7: State the remaining replay blockers explicitly
At the end of this stage, list what still blocks full success.

Typical blockers:
- session bootstrapping before the representative method can be accepted
- freshness or nonce regeneration
- signature/MAC coverage not yet localized
- pending-request correlation or sequence ownership
- transport wrapper or channel binding still missing
- output-side handoff still not proved
- for streaming methods, close / half-close, message ordering, or stream-lifecycle reproduction still incomplete
- for Windows RPC, binding/authn level, transfer syntax, or context-handle lifecycle still ambient rather than frozen into the fixture package
- for async / completion-sensitive methods, timeout/deadline posture, cancellation behavior, or the difference between server-side completion and client-side timeout is still ambient rather than frozen into the fixture package

A fixture package without this blocker list invites overclaiming.

### Step 8: Hand off narrowly
After one representative fixture and one minimal harness exist:
- move to `protocol-replay-precondition-and-state-gate-workflow-note` when the fixture is structurally plausible but still rejected or inert
- move to `protocol-reply-emission-and-transport-handoff-workflow-note` when local acceptance exists but the output-side commit path is still unclear
- move to `protocol-parser-to-state-edge-localization-workflow-note` when the fixture is good enough but the real question is now what state edge or reducer this method triggers
- move to `analytic-provenance-and-evidence-management` when the main need is preserving the exact fixture assumptions and compare slices for later work

## 6. Breakpoint / hook placement guidance
Useful anchors for this stage:
- generated method stubs or RPC client helpers
- serializer entry points for the chosen request family
- builder/finalize functions that consume a stable request object
- request enqueue sites that still preserve correlation IDs or method identity
- fixture capture points just before framing/encryption and just after parse/materialization
- response dispatch sites that can tie an observed reply/completion back to the representative request
- for gRPC-like families, metadata/interceptor injection points, deadline-setting call sites, authority/host override boundaries, and credential attachment sites that still preserve per-call context outside the body
- for streaming cases, open/send/half-close boundaries and first server-event dispatch
- for Windows RPC, stub marshalling helpers, `NdrClientCall*`-adjacent invocation boundaries, binding-handle construction/configuration points, or opnum-bearing call sites that still preserve argument shape

If noise is high:
- prefer the single chosen method family
- prefer one constructor boundary and one emission boundary
- avoid cataloging all sibling serializers or all service methods at once

## 7. Failure patterns this note helps prevent

### 1. Schema exists, but replay object is still vague
A schema or service shell alone is not yet a representative replay surface.

### 2. Treating every field as equally important
That blocks useful compare design and keeps replay debugging mushy.

### 3. Dragging hidden ambient state into the first harness
The first harness should expose missing obligations, not hide them.

### 4. Overgrowing into a full client too early
That usually makes failures harder to localize, not easier.

### 5. Confusing fixture fidelity with replay acceptance
A good fixture package only earns a better gate-debugging position.
It does not prove live success.

### 6. Treating stream close semantics as optional polish
For some streaming RPCs, half-close or close timing is part of the smallest truthful fixture.

### 7. Treating Windows RPC replay as whole-interface recovery
The first replay-worthy object is often one opnum-level call bundle, not complete interface coverage.

## 8. Concrete scenario patterns

### Scenario A: gRPC method known, but no representative request package exists
Pattern:

```text
service and method names recovered
  -> .proto or descriptor-like shape partly externalized
  -> request can be described, but not yet frozen as one compare-friendly fixture
```

Best move:
- choose one method
- freeze route identity as `/{package}.{Service}/{Method}` plus request/response type pairing and stream shape
- preserve one request/response pair or one truthful request/completion slice
- mark likely gate-bearing metadata separately from body identity
- build one stub-backed or schema-backed request constructor

Extra stop rule worth preserving:
- do not stop at “the protobuf body looks right” if the original live call also depended on one deadline posture, metadata/header set, authority assumption, or call-credential attachment outside the body
- if two runs serialize the same message body but one returns `DEADLINE_EXCEEDED`, routing mismatch, auth failure, or a different server path, treat **call-context truth** as the missing replay object rather than widening back out into generic schema doubt

If reflection is unavailable or stripped:
- fall back to embedded descriptor blobs, generated-code evidence, path strings, registration code, or live compare pairs
- narrow fixture scope instead of pretending the whole service roster is already known

### Scenario B: streaming gRPC method known, but the decisive reply never appears
Pattern:

```text
method path is known
  -> per-message payloads look plausible
  -> replay still stalls or times out
  -> close / half-close behavior or message ordering is not preserved truthfully
```

Best move:
- freeze one ordered slice, not one payload blob
- record whether client half-close / close is required for the decisive reply or completion
- hold message count, ordering, and close timing constant in the first compare pair
- treat lifecycle reproduction as part of fixture identity before jumping to auth or schema guesses

### Scenario C: Windows/custom RPC opnum known, but arguments are still folklore
Pattern:

```text
interface/opnum is known
  -> stub or dispatch path is visible
  -> one live call shape exists
  -> analysts keep debating argument semantics without freezing one representative call object
```

Best move:
- preserve one representative argument bundle
- separate opnum identity from auth/context handles and per-call correlation fields
- preserve binding or endpoint assumptions explicitly
- build one minimal call surface before widening argument taxonomy
- if a context handle is involved, freeze where that handle was created, under which interface/binding family it remained valid, and whether replay is reusing truthful lineage versus inventing a stand-in token

Extra stop rule worth preserving:
- do not treat a visible opnum plus plausible arguments as the whole replay object if the live call still depended on one binding-handle family, authn/authz posture, object-UUID target, or stricter context-handle contract
- if the same argument bundle behaves differently across binding families or interface/context assumptions, freeze that call-context difference as part of the representative fixture instead of calling it generic ambient state
- if the case already has one visible context handle, ask whether replay failure is better explained by invalid handle lineage/interface ownership than by wrong scalar/string arguments before widening argument taxonomy again

### Scenario D: Async method looks right, but the client fixture lies about completion
Pattern:

```text
method/opnum identity looks right
  -> arguments or payload shape look plausible
  -> replay still appears to "fail"
  -> client times out, cancels, or declares failure before the original completion/lifecycle boundary
  -> server-side work may still complete or emit a late reply
```

Best move:
- freeze one representative lifecycle statement in the fixture package:
  - expected deadline/timeout posture
  - whether client cancellation is part of the observed path
  - whether success is synchronous reply, deferred completion, or late reply after caller patience expires
- do not immediately reinterpret this as argument-shape failure
- hold timeout/close/cancel posture constant in the first compare pair before varying payload fields

### Scenario E: Proprietary command protocol already has one opcode contract
Pattern:

```text
opcode family recovered
  -> serializer path visible
  -> many captures exist
  -> no single request fixture has been chosen for controlled edits
```

Best move:
- freeze one opcode fixture
- choose one conservative mutation
- use the resulting compare pair to decide which fields are route identity versus likely gate-bearing state

## 9. What good output looks like
A strong result from this workflow usually contains:
- one chosen representative method/opcode/opnum family
- one frozen route identity boundary
  - method/path/opcode/opnum identity
  - stream shape if relevant
- one provenance-tagged request fixture, plus response/ack fixture if available
- for streaming cases, one truthful ordered slice and explicit close / half-close statement
- for Windows RPC, one representative argument bundle plus explicit binding/context assumptions
- for async / timeout-sensitive cases, one explicit statement of expected completion style and deadline/timeout/cancel posture
- one reduced split of stable identity vs likely gate-bearing vs decorative fields
- one minimal constructor / serializer / invocation path
- one conservative edit compare pair
- one explicit list of remaining replay blockers

That is enough.
The goal is not a full client.
It is one truthful replay object that makes the next diagnostic step smaller.

## 10. Relationship to the broader protocol branch
This note sits after:
- `protocol-service-contract-extraction-and-method-dispatch-workflow-note`
- `protocol-schema-externalization-and-replay-harness-workflow-note`

and before the most common narrower continuations:
- `protocol-replay-precondition-and-state-gate-workflow-note`
- `protocol-reply-emission-and-transport-handoff-workflow-note`
- `protocol-parser-to-state-edge-localization-workflow-note`

In ladder form:

```text
recover one representative method contract
  -> externalize the contract/schema
  -> freeze one minimal replay fixture and constructor path
  -> separate identity from likely gates
  -> then debug acceptance, consequence, or output
```

## 11. Sources and confidence
Primary retained source influences for this page:
- IOActive’s gRPC reversing walkthrough for service registration, vtable ordering, and method-bearing contract recovery
- protobuf descriptor extraction and recovery material summarized in:
  - `sources/firmware-protocol/2026-03-22-grpc-method-contract-minimal-fixture-notes.md`
- streaming-first and reflection-disabled continuation material summarized in:
  - `sources/firmware-protocol/2026-03-23-streaming-first-minimal-replay-fixture-notes.md`
- streaming / half-close and Windows RPC representative call-bundle material summarized in:
  - `sources/firmware-protocol/2026-03-23-streaming-and-opnum-minimal-replay-fixture-notes.md`
- cross-family call-context continuation summarized in:
  - `sources/firmware-protocol/2026-03-26-call-context-minimal-replay-notes.md`
- Windows RPC binding/context comparability continuation summarized in:
  - `sources/firmware-protocol/2026-03-26-rpc-binding-context-fixture-notes.md`
- existing schema-externalization source note:
  - `sources/firmware-protocol/2026-03-21-schema-externalization-and-replay-harness-notes.md`

Confidence note:
- strong for the workflow gap and stop rules
- strong for preserving streaming-shape and half-close as fixture identity in streaming cases
- medium-to-strong for the Windows RPC reduction from interface discovery to one opnum-level representative call bundle
- medium for tool-specific implementation details because concrete targets vary widely
- intentionally conservative about claiming that any one fixture package solves live replay by itself
