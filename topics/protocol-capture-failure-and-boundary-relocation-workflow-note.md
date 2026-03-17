# Protocol Capture-Failure and Boundary-Relocation Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, protocol state/message recovery, firmware/protocol context bridge
Maturity: practical
Related pages:
- topics/protocol-state-and-message-recovery.md
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-ingress-ownership-and-receive-path-workflow-note.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/protocol-reply-emission-and-transport-handoff-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/android-network-trust-and-pinning-localization-workflow-note.md

## 1. When to use this note
Use this note when protocol or traffic analysis is stalling **before** parser, state, or replay work can even become trustworthy.

Typical entry conditions:
- the target clearly communicates with something important, but ordinary proxy capture is partial, empty, misleading, or unstable
- pinning bypass has already been attempted, yet the decisive requests still do not appear
- QUIC / HTTP3 / UDP / custom-overlay suspicion exists, but the analyst has not proved which diagnosis is actually true
- some transport activity is visible, but the nearest trustworthy object may still be elsewhere: transparent interception, socket write/read plaintext, framework object boundaries, or manifest/key/content pipelines
- the real product of the traffic is not the packet alone, but a later artifact such as a stream manifest, content key, or merged media object

Use it for cases like:
- mobile apps that ignore the system proxy and keep the key requests off the usual MITM path
- proprietary overlays where raw socket bytes matter more than HTTP-level tooling
- region/device-conditioned apps where traffic visibility itself changes with environment state
- stream/content targets where the useful recovery object is really API -> manifest -> key -> segment pipeline, not the first visible URL

Do **not** use this note when the case already has a good local input boundary, such as:
- the inbound message family is already visible and the real missing edge is receive ownership
- parser visibility exists and the missing edge is now parser-to-state consequence
- replay is failing because a local acceptance gate is still unproved
- the output side is the real bottleneck rather than capture/visibility/boundary selection

In those cases, start with:
- `topics/protocol-ingress-ownership-and-receive-path-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`

## 2. Core claim
A recurring protocol / network bottleneck is not parser complexity.
It is **capture-failure diagnosis and boundary relocation**.

The useful analyst target is often:
- not another generic pinning bypass attempt
- not broader packet collection from the same blind surface
- not premature parser taxonomy built on partial captures
- not confident claims that the target is "using QUIC" or "doing custom crypto" before the missing visibility path is proved

It is the first boundary that makes the traffic legible enough to support later protocol work, such as:
- proving the app is bypassing the system proxy and needs transparent interception
- proving the useful boundary is socket write/read plaintext rather than wire capture
- proving visibility depends on region, device, session, or environment gates
- proving the real object of recovery is a content pipeline such as authenticated API -> manifest -> key -> segment retrieval

That boundary is often more valuable than deeper field inference attempted too early.

## 3. Target pattern
The recurring target pattern is:

```text
important behavior clearly exists
  -> ordinary capture is partial / empty / misleading
  -> several failure explanations are plausible
  -> one diagnosis is proved with a narrow compare pair
  -> one better boundary is selected
  -> later parser/state/content work becomes trustworthy
```

The key discipline is:
- separate **missing visibility** from **hard protocol semantics**
- localize the first boundary where the target becomes legible enough to support the next experiment

## 4. What counts as a boundary-relocation target
Treat these as high-value targets:
- first proof that the app is using ordinary transport outside the configured system proxy
- first proof that transparent proxy / transparent MITM sees the previously missing requests
- first socket write/read boundary where structured plaintext or pre-encryption objects exist
- first framework or serializer object that explains the wire data better than packet capture alone
- first environment or topology change that turns invisible traffic into visible traffic
- first manifest, key, or downstream content artifact that reveals the protocol’s real product
- first compare-run divergence that distinguishes proxy bypass, trust rejection, private overlay, or environment gate

Treat these as useful but often too weak alone:
- "I saw some requests in Charles/mitmproxy"
- "pinning bypass did not fix it"
- "the app might be using QUIC"
- "the traffic looks encrypted"
- "the video URL is in an m3u8 somewhere"

## 5. Practical workflow

### Step 1: Freeze one narrow representative failure pair
Prefer one disciplined pair over a growing pile of failed captures.

Good pairs include:
- same app action with ordinary proxy vs transparent interception
- same action with environment gate unsatisfied vs satisfied
- same request family with HTTP tooling visibility vs socket-boundary visibility
- same content fetch where only the authenticated API call reveals the later manifest/key path

Record only what you need:
- one user-visible action or request family
- one already-observed capture failure shape
- one candidate explanation
- one later proof boundary

If you do not yet have a stable failure pair, you are still too early for this note.

### Step 2: Classify the failure before bypassing anything else
Explicitly classify the current failure among a small set first:
1. **proxy-bypass / NO_PROXY path**
2. **trust rejection / pinning / native validation path**
3. **non-HTTP or private overlay path**
4. **environment-conditioned visibility path**
5. **content-pipeline continuation path**

This avoids spending five more iterations on the wrong family.

### Step 3: Mark five boundaries explicitly
Before widening into protocol semantics, mark these five boundaries:

1. **user-visible action boundary**
   - what exact action should have produced the traffic?
2. **ordinary-capture boundary**
   - what did the normal proxy or packet tooling actually show?
3. **first diagnosis boundary**
   - what compare-run or block test distinguishes the leading explanations?
4. **relocated boundary**
   - where does the target become newly legible: transparent MITM, socket write/read, framework object, or content-artifact pipeline?
5. **proof-of-better-boundary boundary**
   - what later request, parser object, manifest, key, or content artifact proves this new boundary was the right move?

This prevents "we saw more traffic" from being mistaken for "we selected the right recovery object."

### Step 4: Prefer proof of failure family over folklore
Ask small, falsifiable questions:
- does blocking non-proxied egress break the target action?
- does transparent interception reveal the missing family?
- do socket write/read hooks expose structured plaintext before encryption or framing?
- does changing region/device/session state make the traffic appear or disappear?
- does the visible API response merely hand back a manifest or key reference that must be followed deeper?

Good local role labels:
- `user-action`
- `ordinary-capture`
- `proxy-bypass-test`
- `trust-reject`
- `socket-plaintext`
- `overlay-frame`
- `env-gate`
- `manifest-path`
- `key-path`
- `content-proof`

If a suspected explanation cannot be tied to one of these roles, it may still be guesswork.

### Step 5: Relocate to the nearest trustworthy object
Once the failure family is narrowed, relocate deliberately:
- for proxy bypass -> use transparent interception and prove the missing family appears there
- for private overlays -> move to socket write/read plaintext or nearest serializer/framer object
- for environment gates -> satisfy or spoof the gate before drawing protocol conclusions
- for content pipelines -> follow the authenticated API to manifest, key, and segment boundaries rather than stopping at the first URL

The target is not "more data."
It is one **trustworthy object** that supports the next protocol experiment.

### Step 6: Hand the result to the next narrower workflow note
Once the new boundary is proved, route forward only once:
- receive ownership localization
- parser-to-state consequence localization
- replay/state-gate diagnosis
- output-side emission/handoff proof
- content/artifact automation or reconstruction

Do not keep reopening boundary diagnosis after a good boundary has already been proved.

## 6. Breakpoint / hook placement guidance
Useful anchor classes:
- target action trigger points on the app side
- system-proxy vs transparent-proxy divergence tests
- first socket write/read helpers attributable to the missing request family
- serializer/framing helpers immediately before crypto or transport handoff
- environment or region gate checks that suppress later traffic
- authenticated API responses that return manifest references, signed URLs, key paths, or segment lists
- first manifest parse, key retrieval, or media-segment fetch used as proof-of-object

If traces are noisy, anchor on:
- compare-run boundary tests rather than full traffic dumps
- first plaintext owner rather than raw encrypted packets
- first content-manifest or key object rather than all downstream media bytes
- one decisive missing-family request rather than every request in the app

## 7. Failure patterns this note helps prevent

### 1. Treating all capture failure as pinning
Many important failures are actually proxy bypass, non-HTTP overlays, or environment-gated behavior.

### 2. Naming QUIC/HTTP3 too early
Transport-family guesses are weak until the missing visibility path is proved.

### 3. Overcollecting partial captures from the wrong surface
If the current surface is wrong, more traffic from it usually adds noise rather than leverage.

### 4. Confusing encrypted wire bytes with semantic hardness
The easier object may still exist at socket plaintext, serializer, manifest, or key-retrieval boundaries.

### 5. Stopping at the first visible URL in stream/content cases
When the real product is a manifest/key/content pipeline, the protocol object continues past the initial URL.

## 8. Concrete scenario patterns

### Scenario A: Partial MITM capture, but the important requests still vanish
Pattern:

```text
same target action
  -> ordinary proxy shows some traffic
  -> key requests stay missing
  -> blocking non-proxied egress breaks the action
  -> transparent interception restores visibility
```

Best move:
- prove proxy bypass, then relocate to transparent interception instead of deepening pinning work.

### Scenario B: The app is speaking a private overlay, not useful HTTP
Pattern:

```text
target behavior clearly communicates
  -> wire capture looks opaque or unhelpful
  -> socket write/read hooks expose structured plaintext or framed objects
  -> serialization/compression/crypto/framing can now be decomposed
```

Best move:
- treat the socket-boundary object as the real protocol entry surface.

### Scenario C: The traffic is gated by environment realism
Pattern:

```text
same nominal action
  -> capture is weak or absent in one environment
  -> region/device/session change alters visibility
  -> later requests become legible only after the gate is satisfied
```

Best move:
- treat environment satisfaction as part of the visibility workflow, not as separate housekeeping.

### Scenario D: Stream/content recovery is really an API-to-artifact pipeline
Pattern:

```text
authenticated API call succeeds
  -> response yields manifest reference
  -> manifest yields key/segment paths
  -> key retrieval and segment merge are required for the final artifact
```

Best move:
- continue recovery through manifest, key, and segment boundaries instead of stopping at the first returned URL.

## 9. Relationship to nearby pages
- `topics/protocol-state-and-message-recovery.md`
  - explains the broader message/state recovery family
- `topics/firmware-and-protocol-context-recovery.md`
  - explains why context and boundary selection often dominate before semantics do
- `topics/protocol-ingress-ownership-and-receive-path-workflow-note.md`
  - use that once a good input boundary already exists and the next bottleneck is local receive ownership
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
  - use that once traffic and parser visibility exist but replay still fails because of protocol-state preconditions
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
  - use that when the missing edge is now on the send/output side
- `topics/android-network-trust-and-pinning-localization-workflow-note.md`
  - use that when the same diagnosis problem appears in a mobile trust-path setting and the app-side transport owner still has to be separated

## 10. Minimal operator checklist
Use this note best when you can answer these in writing:
- what is the one target action or missing request family?
- what exactly does the ordinary capture surface show?
- what are the top two failure-family hypotheses?
- what one compare-run or block test distinguishes them?
- where is the relocated boundary that becomes newly trustworthy?
- what concrete later object proves that the relocation was right?

If you cannot answer those, the case likely needs cleaner orientation first.

## 11. Source footprint / evidence quality note
This note is intentionally workflow-first.

It is grounded by:
- `topics/protocol-state-and-message-recovery.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-ingress-ownership-and-receive-path-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/runtime-behavior-recovery.md`
- `sources/protocol-and-network-recovery/2026-03-17-sperm-protocol-network-batch-3-notes.md`

The evidence base here is sufficient for a practical workflow note because the point is not to claim one universal transport architecture.
The point is to normalize a recurring operator move the KB was still missing: diagnose why capture failed, then relocate to the first boundary that actually makes later protocol work trustworthy.

## 12. Bottom line
When protocol / network analysis is stalled because the important traffic still is not really visible, the next high-value move is often not more proxy retries and not premature parser theory.

It is to classify the capture failure, prove the failure family with one narrow compare pair, and relocate to the first trustworthy boundary — transparent interception, socket plaintext, environment-normalized visibility, or manifest/key/content pipeline — that turns the case into one legible protocol object again.
