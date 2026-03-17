# Protocol Layer-Peeling and Contract-Recovery Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, protocol state/message recovery, firmware/protocol context bridge
Maturity: practical
Related pages:
- topics/protocol-state-and-message-recovery.md
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/protocol-reply-emission-and-transport-handoff-workflow-note.md
- topics/runtime-behavior-recovery.md

## 1. When to use this note
Use this note when protocol visibility already exists, but the visible bytes are still too semantically collapsed to support good parser, replay, or content-recovery work.

Typical entry conditions:
- one request family, response body, socket buffer, or captured artifact is already visible
- but the visible object is still a stack of layers rather than one directly useful protocol object
- the analyst has not yet separated framing, compression, serialization, crypto wrapping, service contract, or downstream content-pipeline continuation
- the main bottleneck is no longer “where can I see it?” and not yet “which state write matters?”
- the real problem is deciding **which layer should be treated as the first trustworthy contract**

Use it for cases like:
- protobuf or framed-RPC traffic where bytes are visible, but the analyst still needs to separate transport shell, framing, and message schema
- custom overlay protocols where socket-boundary plaintext exists, yet framing/compression/crypto/serialization are still entangled
- app traffic where request/response wrapper objects expose `buf` or typed payloads, but business semantics still hide behind one more decoding layer
- gRPC / HTTP2 / protobuf style targets where service/method contract recovery is more useful than manual byte stitching
- stream or document targets where the visible response is only an API step in a later manifest/key/content pipeline

Do **not** use this note when the real bottleneck is earlier, such as:
- important traffic is still not meaningfully visible from any trustworthy surface
- the current capture path itself is still in doubt
- transport ownership or receive-path ownership is still unclear
- parser or dispatch visibility already exists and the missing edge is now the first state/reply/peripheral consequence

In those cases, start with:
- `topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md`
- `topics/protocol-ingress-ownership-and-receive-path-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`

## 2. Core claim
A recurring protocol RE bottleneck is not capture failure and not yet parser/state reduction.
It is **layer-peeling and contract recovery**.

The useful analyst target is often:
- not the raw wire bytes
- not the first buffer dump alone
- not the deepest crypto guess
- not a full protocol specification

It is the first decomposition that turns one opaque transport-visible object into a smaller, trustworthy contract such as:
- a framed message family
- a protobuf or TLV schema candidate
- a gRPC service/method contract
- a compressed-but-otherwise-structured payload
- a manifest/key/content continuation path
- a preimage object that can be mutated, replayed, or externally decoded

That decomposition is often more valuable than both premature parser-state theory and premature crypto fixation.

## 3. Target pattern
The recurring target pattern is:

```text
some traffic / buffer / artifact is visible
  -> visible object still mixes several layers
  -> one disciplined peel separates the layers in order
  -> one smaller contract becomes trustworthy
  -> later parser, replay, or content recovery becomes practical
```

The key discipline is:
- separate **visibility** from **interpretability**
- separate **layer decomposition** from **later semantic/state reconstruction**
- stop once one smaller contract is good enough for the next experiment

## 4. What counts as a high-value layer-peeling target
Treat these as high-value targets:
- first framing/header split that turns one blob into repeated message units
- first proof that a body is compressed/encoded rather than encrypted
- first protobuf / TLV / JSON / custom-struct boundary that yields stable field shape
- first service/method shell for an RPC family
- first serializer/preimage object that can be logged before final wrapping
- first manifest/key/content continuation that shows the protocol object does not end at the initial response
- first decomposition of a private overlay into serialization + compression + crypto + framing

Treat these as useful but often too weak alone:
- “the bytes look random”
- “the app probably uses protobuf”
- “this might be QUIC/gRPC/custom crypto”
- “there is a `buf` field somewhere”
- “the response body is encrypted” without proving whether one simpler layer explains it first

## 5. Practical workflow

### Step 1: Freeze one representative object
Prefer one disciplined representative object over a large corpus.

Good objects include:
- one captured request/response pair
- one socket write/read buffer from the target family
- one typed wrapper payload with an embedded `buf`
- one downloaded binary/protobuf sample
- one API response that obviously leads into manifest/key/content continuation

Record only what you need:
- where the object was captured
- one visible family identity
- one suspected layer stack
- one downstream behavior that would become easier if the object were decomposed correctly

If you do not yet have one stable representative object, you are still too early for this note.

### Step 2: Classify the visible stack before decoding anything deeply
Explicitly classify the object into candidate layers.

A useful starter checklist is:
1. **transport or carrier shell**
   - HTTP, HTTP2, websocket, socket stream, RPC envelope, file/container wrapper
2. **framing layer**
   - length/tag/opcode/header/chunk boundaries
3. **transform layer**
   - compression, encoding, packing, chunk merge, base64, zstd, gzip, custom table transform
4. **serialization layer**
   - protobuf, TLV, JSON, flat structs, RPC arguments, message objects
5. **crypto or authenticity layer**
   - encryption, MAC, sign, key lookup, challenge token wrapping
6. **contract or continuation layer**
   - service/method shell, manifest/key/segment path, downstream artifact contract

This avoids jumping straight from raw bytes to “custom encryption.”

### Step 3: Prefer the shallowest peel that reduces uncertainty the most
Ask, in order:
- can framing explain the blob before crypto needs to be discussed?
- can compression/encoding explain apparent entropy before encryption is assumed?
- can serialization explain the structure once framing/transform are stripped?
- does a service/method contract explain the remaining fields better than raw byte-by-byte interpretation?
- is the real product a later manifest/key/content object rather than the current response body?

A strong operator rule here is:
- **names are commentary, shape is truth**

That means:
- field numbers, lengths, nesting, repeated/scalar shape, and layer ordering usually matter more than guessed business names

### Step 4: Mark five boundaries explicitly
Before widening into protocol theory, mark these five boundaries:

1. **capture boundary**
   - where this representative object was obtained
2. **outer-shell boundary**
   - the first carrier/frame distinction that explains how the object is packaged
3. **first successful peel boundary**
   - the first transform removed cleanly: framing, compression, wrapper, or encoding
4. **smallest trustworthy contract boundary**
   - the first message/schema/service/preimage/manifest object that can now be reasoned about directly
5. **proof-of-utility boundary**
   - one later parser, replay, stub invocation, key retrieval, segment fetch, or external decode that only becomes possible after the peel

This prevents “we unpacked one layer” from being mistaken for “we found the useful protocol object.”

### Step 5: Hand each layer to the right next workflow
After each peel, ask what kind of object now exists.

Common outcomes:
- **capture problem still dominates**
  - go back to `protocol-capture-failure-and-boundary-relocation`
- **message family and parser entry now exist**
  - go to `protocol-parser-to-state-edge-localization`
- **replay is now structurally plausible but still rejected**
  - go to `protocol-replay-precondition-and-state-gate`
- **accepted local path exists but outbound commit is unclear**
  - go to `protocol-reply-emission-and-transport-handoff`
- **real product is manifest/key/content**
  - continue the contract deeper instead of pretending packet semantics are the final stop

### Step 6: Stop once one smaller contract is good enough
Do not insist on decoding every layer completely.

Often the right stopping point is:
- one stable `.proto` candidate
- one RPC service/method shell and message schema
- one externally decodable compressed body
- one serializer preimage object
- one manifest/key/content ladder

The goal is not maximal decoding.
It is one smaller contract that unlocks the next experiment.

## 6. Breakpoint / hook placement guidance
Useful anchor classes:
- response/request wrapper objects just above transport
- socket write/read boundaries for private overlays
- serializer and pre-serializer object construction sites
- compression/decompression helpers
- framing helpers that add length, tags, or opcodes
- RPC method dispatch or stub-generation boundaries
- manifest parse, key retrieval, or segment URL construction boundaries

If traces are noisy, anchor on:
- the shallowest layer transition that changes the object’s interpretability
- one wrapper or buffer family rather than all network traffic
- one representative body sample rather than full session capture
- preimage or service-contract objects rather than final encrypted or packed forms

## 7. Failure patterns this note helps prevent

### 1. Treating entropy as proof of encryption
Many protocol objects are merely compressed, framed, serialized, or nested before they are truly cryptographic.

### 2. Treating wire format as the only real object
The nearest useful object may be a serializer input, protobuf message, framed-RPC contract, or manifest pipeline.

### 3. Overfitting names before structure is stable
Guessed field names are weak evidence compared with stable numbering, nesting, lengths, and repeated/scalar shape.

### 4. Mixing contract recovery with state recovery too early
A stable message or service contract often needs to exist before parser-to-state or replay-gate work can be trustworthy.

### 5. Stopping at the first visible response when the real object continues deeper
Some protocol cases only become useful when followed through API -> manifest -> key -> segment or API -> wrapper -> preimage -> external decode.

## 8. Concrete scenario patterns

### Scenario A: Protobuf-looking blob is really a structure-recovery problem
Pattern:

```text
response bytes look opaque
  -> framing is simple enough
  -> protobuf-like field structure appears after shallow inspection
  -> candidate schema can be reconstructed iteratively
```

Best move:
- recover stable field numbering, nesting, and scalar/repeated shape before guessing business names.

### Scenario B: gRPC-like target is easier as contract recovery than byte stitching
Pattern:

```text
HTTP2 or framed RPC transport exists
  -> payload family is protobuf-shaped
  -> service/method shell can be inferred
  -> compatible stub invocation becomes easier than manual packet crafting
```

Best move:
- recover the service contract and message schema separately from sign/auth field generation.

### Scenario C: Private overlay is layered, not monolithic
Pattern:

```text
socket-boundary object is visible
  -> header/framing separates messages
  -> body still mixes compression + serialization + crypto
  -> one ordered peel yields a stable preimage object
```

Best move:
- decompose the overlay into framing, transform, serialization, and crypto layers instead of treating it as one mystery blob.

### Scenario D: Visible API response is only the start of a content pipeline
Pattern:

```text
authenticated API call succeeds
  -> response returns manifest or content reference
  -> later key/segment or document-stream retrieval matters more than the initial body
```

Best move:
- continue contract recovery through the artifact pipeline rather than stopping at the API payload.

## 9. Relationship to nearby pages
- `topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md`
  - use that when the main problem is still choosing a trustworthy visibility boundary at all
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
  - use that once one smaller message/parser contract already exists and the next bottleneck is the first consequence-bearing edge
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
  - use that once replay becomes structurally plausible but still fails because acceptance conditions remain hidden
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
  - use that once accepted local handling exists and the next missing edge is outbound commit
- `topics/firmware-and-protocol-context-recovery.md`
  - explains why protocol work often depends on choosing the right environmental and object-of-recovery boundary first
- `topics/protocol-state-and-message-recovery.md`
  - explains the broader message/state recovery family that this note narrows into one practical operator move

## 10. Minimal operator checklist
Use this note best when you can answer these in writing:
- what is the one representative object?
- what layers are plausibly mixed inside it?
- what is the first successful peel?
- what is the smallest trustworthy contract after that peel?
- what concrete next experiment becomes possible once that contract is isolated?

If you cannot answer those, the case likely still needs earlier boundary work.

## 11. Source footprint / evidence quality note
This note is intentionally workflow-first.

It is grounded by:
- `topics/protocol-state-and-message-recovery.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md`
- `sources/protocol-and-network-recovery/2026-03-17-sperm-protocol-network-batch-1-notes.md`
- `sources/protocol-and-network-recovery/2026-03-17-sperm-protocol-network-batch-2-notes.md`
- `sources/protocol-and-network-recovery/2026-03-17-sperm-protocol-network-batch-3-notes.md`

The evidence base here is sufficient for a practical workflow note because the point is not to claim one universal protocol stack.
The point is to normalize a recurring operator move the KB was still missing: peel visible layered objects in the right order until one smaller contract becomes trustworthy enough for replay, parser work, or artifact recovery.

## 12. Bottom line
When protocol work already has visibility but still does not have a usable object, the next high-value move is often not more capture and not deeper parser speculation.

It is to peel the visible object layer by layer until one **smaller trustworthy contract** appears: a framed message family, schema candidate, service contract, serializer preimage, or manifest/key/content continuation that can drive the next experiment.