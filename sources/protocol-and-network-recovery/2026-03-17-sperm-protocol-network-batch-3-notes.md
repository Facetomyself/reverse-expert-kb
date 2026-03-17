# Source Notes — 2026-03-17 — `sperm/md` Protocol / network batch 3

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-携程抓包.md`
- `simpread-某手抓包问题分析.md`
- `simpread-记一次 tiktok 抓包过程.md`
- `simpread-M3U8 涉黄 APP 取证分析实战.md`

Existing KB materials consulted for fit:
- `sources/protocol-and-network-recovery/2026-03-17-sperm-protocol-network-batch-2-notes.md`
- `topics/runtime-behavior-recovery.md`

## Why these articles were grouped together
This batch coheres around one practical branch:
- **when “抓不到包” happens, the right move is usually not blind anti-pinning repetition but transport-path diagnosis: determine whether the target is bypassing the proxy, using a non-HTTP overlay, forcing a different trust path, or carrying a higher-level content pipeline such as HLS/M3U8 that must be recovered beyond the transport itself**

The subthemes are:
- socket-level observation for non-HTTP/private overlay protocols
- transparent-proxy/transparent-MITM as a response to `NO_PROXY` or proxy bypass
- QUIC/HTTP3 suspicion vs actual proxy-bypass diagnosis
- lock-region / environment-conditioning before protocol visibility (TikTok)
- HLS/M3U8 recovery as transport + manifest + key + content pipeline recovery

## Strong recurring ideas

### 1. “Can’t capture it” is a diagnosis problem, not a default pinning verdict
The Kuaishou and TikTok articles are especially useful because they model failure modes explicitly:
- proxy bypass / `Proxy.NO_PROXY`
- QUIC/HTTP3 or UDP suspicion
- custom trust/pinning
- region/device-environment gating
- non-HTTP overlay protocols

This reinforces a durable rule:
- **抓包 failure should first be classified, not merely bypassed**.

### 2. Transparent interception is often the decisive move when system-proxy paths are ignored
The Kuaishou article is strong because it demonstrates a tight black-box diagnostic loop:
- ordinary proxy captures some traffic but misses the key requests
- blocking non-proxied traffic breaks the app
- allowing only 80/443 still breaks it, proving the missing path is still ordinary transport but not using system proxy
- switching to transparent proxy/MITM restores visibility

That is excellent KB material because it shows how to prove the right transport diagnosis empirically.

### 3. Non-HTTP or private overlay traffic should be approached from the nearest write/read boundary
The Ctrip article adds another useful operator pattern:
- if the app is not speaking ordinary HTTPS at the boundary you expected,
- hook `socketWrite0`/`socketRead0` and inspect stack + pre-encryption buffers,
- recover the overlay’s structure, serialization, compression, and encryption pipeline there.

This is a strong generalization of earlier “framework/plaintext owner” lessons.
It just moves the owner boundary to Java socket write/read for private overlays.

### 4. Overlay protocols often still decompose cleanly into serialization + compression + crypto + framing
The Ctrip SOTP case is valuable because it turns a “small众协议” into an analyzable layered object:
- protobuf-encoded `MobData`
- gzip compression
- AES/ECB encryption
- fixed type/length framing header

That is the kind of reduction the KB should preserve.
A protocol name matters less than the layer decomposition.

### 5. Environment conditioning can be a prerequisite to protocol visibility
The TikTok article is not the deepest technically, but it contributes a useful workflow guardrail:
- if the app is region/device constrained, you may need to satisfy environment gates before traffic becomes meaningfully observable at all.

That parallels earlier mobile and browser findings about proxy/VPN/device-classification gates.

### 6. HLS/M3U8 targets are protocol-plus-content pipelines, not merely URLs to download
The M3U8 forensic article is useful because it broadens protocol recovery in a concrete way:
- app-side authenticated API returns m3u8 URL
- m3u8 manifest reveals relative key and segment paths
- key retrieval and sign/auth generation matter
- content recovery requires manifest + key + segment download + merge/decrypt pipeline

This is a perfect example of **protocol recovery continuing into content artifact recovery**.

### 7. Key/manifest recovery should be tied back to the API trust path, not treated as isolated download trivia
The M3U8 case also reinforces an important operator lesson:
- the video content pipeline is gated by the app’s API trust contract (`token`, `sign`, `noise`, etc.)
- therefore content recovery depends on recovering the app’s request-auth pipeline first
- only then can manifest/key/segment recovery be automated at scale

This fits well with the branch’s existing field-pipeline model.

### 8. A useful “capture failure to content recovery” ladder is emerging
Across this batch, a strong end-to-end ladder appears:
1. diagnose why ordinary proxy capture failed
2. relocate interception to transparent proxy or write/read boundary as needed
3. decompose private overlays into serialization/compression/crypto/framing
4. satisfy environment gates if traffic is region/device-conditioned
5. extend protocol recovery into manifest/key/content pipeline recovery when the target is stream- or container-based

This is excellent canonical-KB material.

## Concrete operator takeaways worth preserving

### A. Capture-failure diagnosis workflow
Reusable sequence:
1. classify the failure among:
   - proxy bypass / `NO_PROXY`
   - SSL pinning / trust rejection
   - QUIC/HTTP3/UDP path
   - non-HTTP private overlay
   - region/device-environment gate
2. run small black-box tests that isolate each possibility
3. only then choose the bypass/interception strategy

### B. Transparent-interception proof workflow
Reusable sequence:
1. verify ordinary proxy captures only partial traffic
2. block non-proxied egress to see whether key app behavior breaks
3. narrow by port/protocol if useful
4. if behavior proves the app is using normal transport outside system proxy, switch to transparent proxy/MITM
5. stop over-investing in pinning bypass once proxy-bypass diagnosis is confirmed

### C. Socket-boundary overlay-protocol recovery workflow
Reusable sequence:
1. hook `socketWrite0` / `socketRead0` or nearest equivalent write/read boundary
2. capture stack traces and pre-encryption buffers
3. reconstruct overlay layering:
   - serialization schema
   - compression
   - crypto
   - explicit framing header/type/length
4. recover the nearest structured plaintext before attempting full replay

### D. Environment-conditioned visibility workflow
Reusable sequence:
1. determine whether the target’s traffic behavior depends on region/network/device state
2. satisfy or spoof those gates first
3. only then evaluate capture success or protocol-path hypotheses

### E. HLS/M3U8 content-pipeline recovery workflow
Reusable sequence:
1. recover the authenticated API call that returns the content URL/manifest reference
2. recover the auth/sign field pipeline required by that API
3. fetch the manifest and resolve relative key/segment paths
4. recover/decode the content key material
5. download, decrypt, and merge segments as a continuation of protocol recovery

## Candidate KB implications
This batch strongly supports or suggests improvements to:
- protocol/network subtree notes
- `topics/runtime-behavior-recovery.md`
- transport-boundary and trust-boundary selection notes
- layered content/container recovery notes

Potential future child-note opportunities:
- capture-failure diagnosis note
- transparent-interception proof workflow note
- socket-boundary recovery for private overlay protocols
- HLS/M3U8 content-pipeline recovery note
- environment-conditioned visibility note

## Confidence / quality note
This is a very strong late protocol batch because it connects early capture failure diagnosis to later content recovery in one continuous workflow.

Its best contribution is the durable lesson that protocol/network work should often be treated as:
- diagnose the missing visibility path,
- relocate the boundary,
- peel the layers,
- then continue into content/artifact recovery when the protocol’s real product is not the packet but the downstream manifest/key/media object.
