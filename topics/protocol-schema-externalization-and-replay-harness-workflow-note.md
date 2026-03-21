# Protocol Schema-Externalization and Replay-Harness Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, protocol state/message recovery, contract-to-harness bridge
Maturity: practical
Related pages:
- topics/protocol-state-and-message-recovery.md
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-layer-peeling-and-contract-recovery-workflow-note.md
- topics/protocol-content-pipeline-recovery-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/protocol-reply-emission-and-transport-handoff-workflow-note.md
- topics/runtime-behavior-recovery.md

## 1. When to use this note
Use this note when one protocol object is already visible and already peeled enough that the next bottleneck is no longer broad contract recovery, but also not yet narrow replay-gate debugging.

Typical entry conditions:
- one protobuf/TLV/RPC/custom-message family is already visible enough to inspect
- the analyst already has one smaller trustworthy contract such as a message shape, service/method shell, descriptor-like object, or serializer preimage
- the main missing step is turning that recovered contract into something reusable outside the target
- the next useful output is one externalized schema/service artifact plus one representative replay/edit/fuzz surface
- replay work is close, but still weak because the recovered contract remains analyst-private rather than tool-usable

Use it for cases like:
- protobuf-shaped traffic where field numbers and nesting are visible, but no reusable `.proto` or schema artifact exists yet
- binaries or APKs that may embed reflection/descriptor metadata which can be externalized into schema files
- RPC or framed-message families where the useful next object is a service/method shell or serializer input model rather than more byte commentary
- targets where a representative request family can likely be mutated or replayed once serialization/deserialization exists outside the target
- cases where the branch has already peeled to one contract, but keeps stalling because that contract has not been converted into a scriptable harness target

Do **not** use this note when:
- the current surface is still too weak and the real bottleneck is broader visibility or boundary relocation
- the object is still too layered and one smaller trustworthy contract does not yet exist
- replay is already structurally plausible and the real bottleneck is now acceptance, freshness, auth, state, or session gating
- the accepted local path already exists and the missing edge is the first concrete outbound send / queue / transport handoff

In those cases, start with:
- `topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md`
- `topics/protocol-socket-boundary-and-private-overlay-recovery-workflow-note.md`
- `topics/protocol-layer-peeling-and-contract-recovery-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`

## 2. Core claim
A recurring protocol RE bottleneck appears after one smaller contract has already been recovered:
- the analyst can see enough structure to talk about the protocol,
- but not yet enough externalized structure to **exercise** the protocol outside the target.

The useful next target is often not:
- more field renaming
- a full protocol specification
- a broad state-machine theory
- a general client reimplementation

It is:
- one externalized schema, descriptor, or service-contract artifact
- one serializer/deserializer round-trip proof
- one representative replay/edit/fuzz harness target
- one explicit note about the remaining state/auth/gating obligations

This note exists to keep the branch practical:
- **externalize one recovered contract before overgrowing protocol narration**.

## 3. Target pattern
The recurring pattern is:

```text
one smaller trustworthy contract already exists
  -> but it is still trapped inside notes, traces, or analyst memory
  -> externalize it into one reusable schema / service artifact
  -> prove one serializer or parser round-trip outside the target
  -> attach one representative replay or fuzz surface
  -> only then continue into narrow replay-gate or send-boundary work
```

The key discipline is:
- separate **contract recovery** from **contract externalization**
- separate **externalization** from **state acceptance**
- stop after one representative harness target is good enough

## 4. What counts as a high-value externalization target
Treat these as high-value targets:
- one `.proto` or equivalent schema candidate
- one descriptor-bearing artifact extracted from a binary or generated code
- one service/method shell for an RPC family
- one serializer/preimage object that can be recreated outside the target
- one message family model stable enough for encode/decode round-trips
- one request/response fixture set good enough to drive replay or fuzz mutation

Treat these as useful but often too weak alone:
- screenshots of pretty-printed fields
- guessed business names without stable field numbering or nesting
- broad statements like “it uses protobuf” without an external artifact
- a parser that only works inside the original process and cannot be reused in a script or tool
- raw hex fixtures without any representation of message structure

## 5. Practical workflow

### Step 1: Freeze one representative contract and one operator goal
Pick one message family only.

Good representative targets include:
- one request family you want to replay or mutate
- one response family you want to parse, classify, or feed into later state reasoning
- one service/method shell you want to make externally callable
- one descriptor-like binary artifact that should be convertible into source schema

Write down only:
- what the contract currently looks like
- where it came from
- what external task it should unlock next
  - parse
  - serialize
  - mutate
  - replay
  - fuzz

If you cannot name one representative family, you are still too early for this note.

### Step 2: Prefer descriptor or reflection shortcuts before blind reconstruction
If the family looks protobuf- or IDL-backed, first ask whether the target already ships recoverable metadata.

Common shortcut surfaces:
- embedded descriptor blobs
- `.proto` strings or file names inside binaries
- generated-code reflection metadata
- APK / JAR / binary resources containing schema-like artifacts
- client stubs or method tables exposing service and message names

Strong rule:
- if the target already contains source-like contract metadata, recover that first
- do not spend a long blind inference pass on blobs when a descriptor shortcut exists

### Step 3: If no descriptor exists, write a provisional schema from stable shape
When shortcut metadata is absent or incomplete, externalize a provisional schema using:
- field numbers
- wire types / scalar widths
- nesting
- repeated vs optional behavior
- compare-run presence/absence
- stable enum/value clusters if visible

Use intentionally generic names if needed.
The point is not semantic beauty.
The point is a stable external artifact.

Useful rule:
- **shape first, names later**

A good provisional schema is one that lets tools or scripts round-trip the message family with conservative confidence.

### Step 4: Separate message contract from service or state assumptions
Do not let these collapse into one vague object.

Keep separate notes for:
1. **message or schema contract**
   - fields, nesting, types, framing, serialization
2. **service or endpoint contract**
   - method, path, opcode family, request/response pairing
3. **state or gate assumptions**
   - freshness, session, auth, key lookup, pending-request expectations

This separation matters because:
- you may be able to externalize the message cleanly before you can satisfy replay gating
- and that is still a valid success boundary for this stage

### Step 5: Prove one external round-trip
Before widening into harness work, prove one of these minimal loops:
- parse fixture -> structured object -> re-emit bytes
- schema -> deserialize sample -> serialize equivalent sample
- service shell -> construct one representative request object
- descriptor extraction -> regenerate readable schema and inspect it against known fixtures

This step is the real proof that the contract has left analyst-private space.

Without it, you usually still have notes, not an externalized artifact.

### Step 6: Build the smallest useful harness surface
A first good harness should be small.

Typical good first harnesses:
- one script that loads a sample, edits one field, and reserializes it
- one script that builds one representative request family from the recovered schema
- one fuzz/edit surface for a single endpoint or message family
- one simulator or replay surface for a single request/response pair

Typical bad first harnesses:
- a whole fake client stack
- a giant “support every field” framework
- a broad protocol emulator without one proved representative family
- a state-machine reimplementation before one representative request family works at all

### Step 7: Record remaining replay blockers explicitly
At the end of this note’s scope, list what still blocks live success.

Typical blockers:
- freshness token generation
- auth/signature fields
- session bootstrapping
- transport wrapping or channel binding
- pending-request / sequence expectations
- local device or environment prerequisites
- output-side transport commit uncertainty

This prevents an externalized schema from being mistaken for a fully replayable protocol.

### Step 8: Hand off to the next narrower workflow
After one schema/service artifact and one harness surface exist, ask what remains:
- if the interaction is structurally plausible but still rejected -> `protocol-replay-precondition-and-state-gate-workflow-note`
- if local acceptance exists but emitted output is unclear -> `protocol-reply-emission-and-transport-handoff-workflow-note`
- if one parser/dispatch family now exists and the next question is consequence -> `protocol-parser-to-state-edge-localization-workflow-note`
- if the “protocol object” actually continues into manifest/key/content -> `protocol-content-pipeline-recovery-workflow-note`

### Practical handoff rule
Stay on this note while the missing proof is still:
- how to externalize one recovered contract into a reusable schema/service artifact
- how to obtain one external round-trip proof
- how to produce one representative replay/edit/fuzz surface

Leave this note once one representative contract is already externalized well enough and the real bottleneck becomes:
- replay acceptance / state gating
- outbound send / transport handoff
- parser/state consequence proof
- content/artifact continuation

A recurring failure mode is staying too long in contract externalization after one useful artifact already exists:
- more field renaming
- more schema polishing
- more generalization to unused message families
when the real bottleneck has already shifted into acceptance or output proof.

## 6. Breakpoint / hook placement guidance
Useful anchors for this stage:
- descriptor-bearing data or reflection metadata in binaries/generated code
- serializer constructors and builder objects
- parser entry points that already materialize structured messages
- method tables, stub layers, or RPC wrappers exposing service shells
- request/response fixture capture points with stable family identity
- code paths that convert message objects to outbound bytes

If traces are noisy, anchor on:
- one family only
- one descriptor or fixture cluster only
- the shallowest object that is already structured enough to externalize
- one serializer boundary rather than all parser and transport traffic

## 7. Failure patterns this note helps prevent

### 1. Leaving a recovered contract trapped in prose
A good contract that only lives in notes is still hard to replay, diff, fuzz, or hand off.

### 2. Mistaking field renaming for progress
Cleaner names do not matter if the contract still cannot be encoded or decoded outside the target.

### 3. Collapsing schema, service, and state obligations together
You can often externalize the message contract before you can satisfy auth/session/state gates.
That is fine and should be recorded explicitly.

### 4. Jumping from one recovered message family to a whole client reimplementation
That usually overgrows the evidence and hides the next true blocker.

### 5. Treating one externalized schema as proof of replay success
Externalization only earns the next experiment.
It does not prove freshness, auth, acceptance, or output handoff.

## 8. Concrete scenario patterns

### Scenario A: Protobuf-like blobs with no names but stable structure
Pattern:

```text
socket/plaintext object visible
  -> fields and nesting are stable
  -> no descriptor recovered yet
  -> provisional schema can still be written from shape
  -> parser / serializer round-trip becomes possible
```

Best move:
- write the provisional schema with generic names
- prove one round-trip
- then move to replay gates instead of polishing names forever

### Scenario B: Embedded descriptor metadata short-circuits blob archaeology
Pattern:

```text
binary / generated code inspected
  -> descriptor-like metadata exists
  -> readable source schema can be regenerated
  -> representative request family can be externalized quickly
```

Best move:
- externalize the descriptor first
- use it to drive one representative request family
- do not continue blind wire-format inference longer than needed

### Scenario C: RPC family is visible, but service shell is still implicit
Pattern:

```text
request body can be parsed
  -> endpoint or opcode family is known
  -> service/method shell still not explicitly modeled
  -> replay is awkward because contract is half message and half transport folklore
```

Best move:
- write down one explicit service contract surface
- separate message schema from path/opcode identity
- build one representative call harness

### Scenario D: Good external schema exists, but live replay still fails
Pattern:

```text
message family externalized
  -> serializer/deserializer works
  -> replayed interaction still rejects or silently no-ops
```

Best move:
- leave this note
- move to replay-precondition / state-gate work
- do not keep blaming the schema unless a round-trip mismatch is actually proved

## 9. What good output looks like
A strong result from this workflow usually contains:
- one externalized schema, descriptor dump, or service-contract artifact
- one representative fixture set
- one parser/serializer or constructor proof outside the target
- one minimal harness for a single family
- one short list of the remaining live replay blockers

That is enough.
The goal is not a full reimplementation.
It is one reusable interaction object.

## 10. Relationship to the broader protocol branch
This note sits after:
- `protocol-layer-peeling-and-contract-recovery-workflow-note`

and before the most common narrower continuations:
- `protocol-replay-precondition-and-state-gate-workflow-note`
- `protocol-reply-emission-and-transport-handoff-workflow-note`
- `protocol-parser-to-state-edge-localization-workflow-note`
- `protocol-content-pipeline-recovery-workflow-note`

In ladder form:

```text
see the right boundary
  -> peel to one smaller trustworthy contract
  -> externalize that contract into one reusable artifact
  -> prove one representative harness surface
  -> only then debug acceptance, output, or later continuation
```

## 11. Sources and confidence
Primary source notes for this page:
- `sources/firmware-protocol/2026-03-21-schema-externalization-and-replay-harness-notes.md`

This note is grounded in:
- protocol-RE-to-dialogue-replay framing from BitBlaze/Reverser material
- format/grammar/simulation framing from Netzob
- protobuf descriptor extraction practice from Arkadiy Tetelman’s descriptor-recovery write-up
- provisional unknown-schema inspection from `protobuf-inspector`
- schema extraction plus replay/fuzz manipulation workflow from `pbtk`

Confidence note:
- strong for the workflow shape and stop rules
- intentionally conservative about claiming tool universality
- does not assume protobuf is the answer in every case
- does not claim externalized schema alone solves replay acceptance
