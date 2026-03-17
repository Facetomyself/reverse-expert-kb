# Source Notes — 2026-03-17 — `sperm/md` Protocol / network batch 1

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-Protobuf 协议逆向解析 - APP 爬虫 .md`
- `simpread-某某 App protobuf 协议逆向分析.md`
- `simpread-猿人学 2022 逆向比赛第七题 quic.md`
- `simpread-分析 okhttp3-retrofit2 - 截流某音通信数据.md`
- `simpread-逆向某物 App 登录接口：抓包分析 + Frida Hook 还原加密算法.md`

One intended `M3U8` file path did not resolve locally during this pass, so it was not used in this batch.

## Why these articles were grouped together
This first protocol/network batch coheres around one practical branch:
- **protocol recovery becomes tractable when you stop treating the wire format as the first-class object and instead localize the nearest stable plaintext/structured boundary that owns framing, serialization, or secret-bearing fields**

The subthemes are:
- Protobuf structure recovery from opaque bytes
- QUIC traffic recovery by moving away from ciphertext capture toward endpoint/control of destination
- OkHttp/Retrofit response interception above transport encryption
- request parameter recovery at Java/native serialization boundaries
- choosing between wire capture, framework interception, and local reimplementation

## Strong recurring ideas

### 1. “Encrypted response” is often really a serialization problem first
The Protobuf articles are useful because they correct a common analytical mistake.
Opaque bytes are not always cryptographic secrecy; they may simply be structured serialization.

The durable lesson is:
- first determine whether the blob is encrypted, privately serialized, or serialized with a known scheme
- if it is a known scheme like Protobuf, the work becomes structure recovery rather than brute-force crypto guessing

### 2. Protobuf recovery is best modeled as structure reconstruction from stack/field evidence
The two Protobuf articles reinforce a repeatable workflow:
- obtain a binary sample (`.bin` or captured response body)
- use `protoc --decode_raw` or structure-inspection tooling to expose stack-like field output
- map field ids, nesting, and type hints into a candidate `.proto`
- compile and iteratively refine until parse/serialization is stable

This is strong KB material because it turns “protobuf逆向” into a concrete artifact-building pipeline.

### 3. Variable names are irrelevant; field numbers and types are the real invariants
A subtle but very useful Protobuf lesson from the batch:
- analyst-chosen field names can be arbitrary
- what matters is field numbering, nesting, scalar/message/repeated shape, and compatible types

That is a useful general rule for serialization RE:
- **names are commentary, shape is truth**.

### 4. QUIC recovery often requires abandoning passive capture in favor of endpoint control
The QUIC article is especially valuable because it shows a decisive shift in approach:
- encrypted UDP/QUIC payloads plus unavailable keys make passive traffic capture unattractive
- instead of insisting on decrypting the wire, redirect the target to an analyst-controlled server and observe the application-layer contract there

This is one of the strongest cross-branch lessons in the repo.
It is pure observation-surface selection, now applied to protocol work.

### 5. For encrypted transport, the best boundary may be framework/request construction rather than the socket
The OkHttp/Retrofit interception article strongly reinforces that protocol recovery can happen above the wire:
- hook Retrofit-wrapped response objects
- descend into `TypedInput` / byte getters
- recover plaintext response bytes there

This is a powerful reminder that the “protocol boundary” analysts care about is often not the network stack but the first structured byte owner above transport protections.

### 6. Secret-bearing fields are best recovered at the serializer/assembler boundary
The login/sign article contributes another useful protocol lesson:
- instead of reasoning about the full request body as one opaque object,
- recover the few decisive fields (`userName`, `password`, `newSign`, etc.) at the point where they are assembled or transformed,
- then recreate the request externally.

This gives the KB a nice operator rule:
- **treat protocol requests as field pipelines, not monoliths**.

### 7. A stable protocol-recovery ladder is emerging
Across this batch, a very useful escalation/selection ladder appears:
1. decide whether the opaque data is crypto or serialization
2. if serialization, reconstruct structure first
3. if transport is encrypted and passive capture is poor, move upward to framework/plaintext boundaries
4. if even that is awkward, redirect destination or emulate the server side
5. recover only the secret-bearing fields needed for faithful replay

This is excellent canonical-KB material later.

## Concrete operator takeaways worth preserving

### A. Serialization-vs-crypto triage workflow
Reusable sequence:
1. do not assume opaque bytes imply encryption
2. classify among:
   - known serialization (protobuf, etc.)
   - private serialization
   - actual crypto wrapping
   - mixed serialization + crypto
3. choose the next workflow accordingly

### B. Protobuf structure-recovery workflow
Reusable sequence:
1. capture a representative binary sample
2. inspect with `decode_raw` or structure-inspector tooling
3. recover nested message boundaries and repeated/scalar patterns
4. draft a candidate `.proto`
5. compile and iteratively refine until parse stability is good enough
6. remember that field numbers/types matter more than names

### C. Endpoint-redirection workflow for encrypted transports like QUIC
Reusable sequence:
1. recognize when passive wire capture is unlikely to yield plaintext affordably
2. redirect the target endpoint (hook host copy, patch address, alter resolution, or otherwise reroute)
3. stand up an analyst-controlled endpoint/server
4. inspect the application contract there
5. only return to full client-side algorithm recovery when the contract boundary is clear

### D. Framework-plaintext-boundary interception workflow
Reusable sequence:
1. identify app/framework objects that own plaintext payloads (Retrofit response wrappers, typed byte containers, serializers)
2. hook the first stable byte getter above transport encryption
3. recover structured plaintext there
4. treat lower socket/proxy capture as optional once the stable higher boundary is found

### E. Field-pipeline recovery workflow for request protocols
Reusable sequence:
1. identify the few secret-bearing fields in the request body
2. recover each field at its own assembler/transform boundary
3. classify per-field transform family (AES/MD5/serialization/native helper/etc.)
4. rebuild the full request externally from the recovered field pipeline
5. avoid over-reading the entire application when a handful of fields determine replay viability

## Candidate KB implications
This batch strongly supports or suggests improvements to:
- protocol/network subtree notes
- `topics/runtime-behavior-recovery.md`
- mobile runtime / network boundary selection notes

Potential future child-note opportunities:
- serialization-vs-crypto triage note
- Protobuf structure-recovery workflow note
- endpoint-redirection workflow for encrypted transports
- framework-plaintext-boundary interception note
- field-pipeline recovery for request protocols

## Confidence / quality note
This is a strong first protocol/network batch.
Its best contribution is the repeated lesson that protocol RE usually becomes easier once the analyst stops worshipping the wire and instead finds the nearest trustworthy owner of structure or plaintext.

That framing aligns very well with the broader KB direction built in the Android and browser branches.
