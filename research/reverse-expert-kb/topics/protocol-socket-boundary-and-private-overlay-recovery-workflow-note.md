# Protocol Socket-Boundary and Private-Overlay Recovery Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, protocol state/message recovery, firmware/protocol context bridge
Maturity: practical
Related pages:
- topics/protocol-state-and-message-recovery.md
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md
- topics/protocol-layer-peeling-and-contract-recovery-workflow-note.md
- topics/protocol-ingress-ownership-and-receive-path-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/runtime-behavior-recovery.md

## 1. When to use this note
Use this note when ordinary HTTP/proxy-oriented traffic analysis is no longer the right entry surface and the nearest trustworthy object is a **socket-boundary or serializer-adjacent private-overlay object**.

Typical entry conditions:
- important app or firmware communication clearly exists, but ordinary proxy captures are partial, misleading, or semantically late
- the case already suggests a private overlay, framed RPC shell, or app-defined transport object rather than a directly useful HTTP body
- socket write/read boundaries, serializer inputs, or framing helpers look more truthful than wire capture alone
- the analyst needs one stable plaintext or pre-encryption object before parser/state, replay, or content-pipeline work can become trustworthy
- the main uncertainty is no longer “is there traffic?” but “where is the first layer where this traffic becomes an analyzable protocol object?”

Use it for cases like:
- mobile apps speaking app-defined framed payloads over ordinary sockets or TLS tunnels
- native services where the useful object appears at `send`/`recv`, `socketWrite0`/`socketRead0`, or serializer helpers rather than at the packet sniffer
- private overlay protocols where framing, compression, serialization, and crypto are all mixed together at the wire but partly separated one layer earlier
- protocol cases where the analyst already suspects protobuf/TLV/custom structs, but only socket-boundary capture can expose the relevant preimage cleanly

Do **not** use this note when the real bottleneck is still earlier, such as:
- the missing traffic family is not yet visible from any surface and the failure family itself is still unclassified
- transparent interception, environment gating, or topology relocation still has to be proved first
- inbound ownership after the bytes are already visible is the main unknown
- parser/state consequence is already the main unknown because the overlay object is already isolated well enough

In those cases, start with:
- `topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md`
- `topics/protocol-ingress-ownership-and-receive-path-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`

## 2. Core claim
A recurring protocol RE bottleneck is that the analyst keeps treating the **wire** as the only honest object even when the useful protocol object first becomes legible one layer earlier.

The high-value move is often not:
- more packet capture from the same blind or semantically-collapsed surface
- immediate full parser reconstruction from encrypted or wrapped bytes
- premature commitment to “custom crypto” when framing/serialization/transform layers are still under-separated

It is:
- relocating to the nearest socket-boundary or serializer-adjacent object
- proving one stable plaintext, pre-encryption, or post-decrypt/pre-parse object
- decomposing the overlay into smaller layers in the right order
- handing one trustworthy contract forward to the next workflow note

In many private-overlay cases, the strongest practical recovery object is:

```text
socket write/read or serializer boundary
  -> framed / transformed overlay object
  -> smaller trustworthy schema / preimage / parser input
  -> later ownership / state / replay work
```

## 3. Target pattern
The recurring target pattern is:

```text
important communication exists
  -> wire capture is partial, opaque, or semantically late
  -> socket write/read or serializer boundary exposes a more truthful object
  -> framing / compression / serialization / crypto can be peeled in order
  -> one smaller contract becomes trustworthy
  -> later parser/state/replay work becomes practical
```

The key discipline is:
- separate **transport visibility** from **overlay-object visibility**
- separate **socket-boundary truth** from **later parser/state consequence**
- stop once one overlay object is truthful enough for the next experiment

## 4. What counts as a high-value socket-boundary target
Treat these as high-value targets:
- first `socketWrite0` / `socketRead0` / `send` / `recv` / stream-write / stream-read boundary attributable to the target family
- first serializer input or post-deserializer object that is more structured than the wire blob
- first framing split that reveals repeatable type/length/opcode boundaries
- first pre-encryption or post-decryption object that proves the bytes are not just opaque crypto noise
- first ordered decomposition into framing + transform + serialization + crypto rather than one undifferentiated “private protocol” blob
- first stable schema candidate, message family, or RPC shell recoverable from socket-boundary captures

Treat these as useful but often too weak alone:
- “the app must be using a custom protocol”
- “the wire looks encrypted”
- “there is some socket activity”
- “a parser-looking function exists somewhere”
- “one packet blob repeats a lot”

## 5. Practical workflow

### Step 1: Freeze one representative overlay exchange
Prefer one disciplined representative object over a large session corpus.

Good objects include:
- one request/response pair from a target action
- one socket write and the matching later read for the same logical exchange
- one serializer input object and the resulting emitted buffer
- one repeated overlay message family with one compare variant

Record only what you need:
- one target action or message family
- where the object was captured
- whether the capture is pre-encryption, post-decrypt, serializer-input, or socket-boundary
- one downstream use you want to unlock, such as parser recovery, replay, state localization, or artifact continuation

If you do not yet have one stable representative overlay exchange, you are still too early for this note.

### Step 2: Mark five boundaries explicitly
Before naming fields or protocol families deeply, mark these five boundaries:

1. **action boundary**
   - what user or system action generated the exchange?
2. **socket / serializer boundary**
   - where does a more truthful object first appear than at the wire?
3. **outer overlay boundary**
   - what first split separates framing/header from body?
4. **smallest trustworthy contract boundary**
   - what first schema/preimage/message family becomes directly analyzable?
5. **proof-of-utility boundary**
   - what later parser/replay/state experiment only becomes possible after this decomposition?

This prevents “we found a socket hook” from being mistaken for “we found the useful protocol object.”

### Step 3: Prefer the shallowest truthful layer over the deepest glamorous guess
Ask, in order:
- does socket-boundary capture already expose framing that the wire hides?
- does one transform such as gzip/base64/custom packing explain the apparent opacity before encryption needs to be discussed?
- does a serializer or message object explain the body better than byte-level speculation?
- is the useful object a stable preimage that can be mutated or replayed rather than the final emitted blob?

A strong operator rule here is:
- **the nearest truthful object beats the most external object**

That means:
- if socket-boundary plaintext is stable, prefer it over encrypted wire bytes
- if serializer input is stable, prefer it over later packed output
- if framing can be proved, do that before inventing field semantics

### Step 4: Decompose the overlay in a fixed order
A useful default order is:
1. framing
2. transform/compression/encoding
3. serialization/object layout
4. crypto/auth wrapper
5. service/method or message-family contract

This is not universal, but it prevents a common failure pattern where the analyst calls everything “encryption” before simpler layers are removed.

Useful local role labels:
- `socket-write`
- `socket-read`
- `serializer-input`
- `frame-header`
- `frame-body`
- `transform`
- `schema-candidate`
- `crypto-wrap`
- `parser-feed`
- `utility-proof`

If a captured object cannot be given one of these roles, it may still be semantically too collapsed.

### Step 5: Prove one smaller contract before widening
Do not stop at “the socket boundary is better.”
Prove it by showing one new leverage point such as:
- one stable type/length/opcode family appears only at the socket boundary
- one protobuf/TLV/custom-struct candidate becomes recognizable only after one shallow peel
- one replay or mutation attempt becomes structurally plausible from the recovered preimage
- one downstream parser or receive-owner note now has a clean object to operate on
- one compare pair shows that overlay-object differences predict later behavior better than raw wire differences do

A weaker but still useful proof is:
- the same wire traffic stays opaque, but the socket-boundary object exposes one stable layer ordering that survives across several representative exchanges.

### Step 6: Hand off to the next narrower note
Once the overlay object is reduced enough, route forward only once:
- to `protocol-layer-peeling-and-contract-recovery` if one more decomposition layer is still the main bottleneck
- to `protocol-ingress-ownership-and-receive-path` if the local receive owner of the object is now the key uncertainty
- to `protocol-parser-to-state-edge-localization` if the parser and message family are visible and the next missing edge is consequence
- to replay/state-gate work if a structurally plausible message exists but local acceptance still fails

Do not keep reopening socket-boundary selection once one good truthful object is already in hand.

## 6. Breakpoint / hook placement guidance
Useful anchor classes:
- Java or native socket write/read helpers attributable to one target family
- serializer / marshaller / wrapper-object construction boundaries
- framing helpers adding length, type, opcode, or tag headers
- compression/decompression or pack/unpack helpers immediately adjacent to socket I/O
- crypto wrappers that still preserve a visible inner object one step earlier
- first parser-feed boundary after the overlay object is reconstructed

If traces are noisy, anchor on:
- one representative exchange rather than all sockets
- one serializer input/output pair rather than full app traffic
- first object boundaries that increase interpretability rather than last-mile transport wrappers
- one compare pair where overlay-object differences predict later behavior

## 7. Failure patterns this note helps prevent

### 1. Treating the wire as the only real object
In private-overlay cases, the wire may be one layer too late to be the cheapest truthful recovery target.

### 2. Calling every opaque blob “custom encryption” too early
Many targets still need framing, transform, or serialization separation before crypto claims become strong.

### 3. Over-collecting socket traffic without reducing one representative object
A disciplined representative exchange is often worth more than many unanalyzed captures.

### 4. Mixing overlay-object recovery with later parser/state work too early
A stable message/preimage/contract often needs to exist before state or replay claims become trustworthy.

### 5. Stopping at “I hooked socketWrite0” without proving new leverage
The point is not the hook itself; it is the smaller trustworthy contract recovered through it.

## 8. Concrete scenario patterns

### Scenario A: Socket-boundary plaintext reveals a layered overlay
Pattern:

```text
wire traffic looks opaque
  -> socketWrite0 exposes structured body
  -> framing header plus compressed/serialized body become visible
  -> schema candidate can be reconstructed
```

Best move:
- treat the socket-boundary object as the real protocol entry surface and peel layers in order.

### Scenario B: Serializer input is more useful than emitted bytes
Pattern:

```text
emitted buffer is packed and signed
  -> serializer input object still has stable field structure
  -> later wrapper logic only obscures the business object
```

Best move:
- anchor on serializer-input or pre-wrap boundaries before trying to infer semantics from final bytes.

### Scenario C: Private overlay recovery bridges directly into parser/state work
Pattern:

```text
socket-boundary object is recovered
  -> one message family and parser feed become visible
  -> the next bottleneck is no longer visibility but first consequence-bearing state edge
```

Best move:
- hand off early to parser-to-state localization instead of endlessly cataloging overlay variants.

## 9. Relationship to nearby pages
- `topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md`
  - use that when the failure family itself is still not proved and boundary selection remains broader than socket-boundary choice
- `topics/protocol-layer-peeling-and-contract-recovery-workflow-note.md`
  - use that when the visible object still needs one more peel before a smaller trustworthy contract exists
- `topics/protocol-ingress-ownership-and-receive-path-workflow-note.md`
  - use that once the overlay object is visible enough and the next question is which local receive path actually owns it
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
  - use that once one parser/message family is visible and the next question is the first consequence-bearing edge
- `topics/runtime-behavior-recovery.md`
  - explains the wider observation-topology logic behind choosing socket-boundary truth over misleading outer surfaces

## 10. Minimal operator checklist
Use this note best when you can answer these in writing:
- what is the one representative exchange?
- where is the first socket or serializer boundary that exposes a more truthful object?
- what first framing/transform/serialization split is proved?
- what is the smallest trustworthy contract after that peel?
- what concrete next experiment becomes possible once that object is isolated?

If you cannot answer those, the case likely still needs an earlier boundary or capture-diagnosis note first.

## 11. Source footprint / evidence quality note
This note is intentionally workflow-first.

It is grounded by:
- `topics/protocol-state-and-message-recovery.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md`
- `topics/protocol-layer-peeling-and-contract-recovery-workflow-note.md`
- `topics/runtime-behavior-recovery.md`
- `sources/protocol-and-network-recovery/2026-03-17-sperm-protocol-network-batch-3-notes.md`

The evidence base here is sufficient for a practical workflow note because the point is not to claim one universal socket architecture.
The point is to normalize a recurring operator move already visible in the local source reservoir: when a target speaks a private overlay, the cheapest truthful object is often at the socket or serializer boundary rather than at the raw wire.

## 12. Bottom line
When protocol work stalls because wire-visible traffic is too collapsed, opaque, or semantically late, the next high-value move is often not deeper packet speculation.

It is to relocate to the **socket-boundary or serializer-adjacent private-overlay object**, peel its layers in order, and recover one smaller trustworthy contract that can drive ownership, parser, replay, or artifact-continuation work.