# Source Notes — 2026-03-17 — `sperm/md` Protocol / network batch 2

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-猿人学 - app 逆向比赛第四题 grpc 题解.md`
- `simpread-某车联网 App 通讯协议加密分析 (三) Trace Block.md`
- `simpread-某电子书阅读器加密协议分析.md`
- `simpread-逆向某短视频 App 搜索协议：破解加密通信，还原真实数据！.md`
- `simpread-对 APP 逆向抓包的实践.md`
- `simpread-抖音抓包.md`

## Why these articles were grouped together
This batch coheres around one practical branch:
- **private or framed protocol work is often solved by peeling layers in the right order: transport admission, framing, compression/encoding, structure, and finally field-level crypto/signature logic**

The subthemes are:
- gRPC as framed RPC over HTTP/2 + protobuf
- Trace Block comparison to correct execution-assisted protocol/sign recovery
- custom container / DRM / document-stream decoding as layered protocol recovery
- TTNet/Cronet interception and compressed request-body recovery
- custom SSL/Cronet verification bypass to regain traffic visibility

## Strong recurring ideas

### 1. gRPC is best treated as a stacked protocol, not a black box
The gRPC article is valuable because it turns a scary modern protocol into a layered object:
- HTTP/2 transport
- gRPC method contract
- protobuf request/response messages
- native sign/field generation

Once framed that way, the analyst does not need to “understand gRPC in general” first.
They need to reconstruct the specific request/response schema and service entry that matter.

### 2. Framed protocols become tractable when you recover the service contract, not just the bytes
The gRPC material shows a strong reusable workflow:
- infer or recover `.proto` message types
- define the RPC service/method shell
- invoke the server with a compatible client stub
- treat sign generation as a separate field-generation problem

This is more powerful than manual byte stitching because it restores the **semantic contract layer**.

### 3. When execution-assisted recovery disagrees with the app, compare block flow before reading more code
The Trace Block article is excellent because it contributes a very transferable debugging workflow:
- if unidbg/emulated execution produces the wrong result,
- compare control-flow blocks against the real app,
- locate the first divergence,
- then repair the missing environment/input/IO assumption.

This is strong protocol-adjacent KB material because many protocol/signature recoveries depend on execution-assisted reconstruction.

### 4. IO/environment mismatches often hide behind protocol failures
The Trace Block article’s `/proc/%d/cmdline` example is very important.
The recovered function was wrong not because the algorithm itself was misunderstood, but because the emulated environment failed to satisfy an IO expectation.

That gives a durable rule:
- **when a reconstructed protocol/sign routine is “almost right,” suspect environment or IO mismatches before assuming the core math is wrong**.

### 5. Compressed/encoded request bodies are separate layers from request semantics
The short-video search protocol article is especially useful because it teases apart multiple layers:
- request object assembly
- form/body wrapper objects
- compression (`zstd`)
- optional body encryption/interception
- TTNet/Cronet interception points

This is exactly the layering the KB should preserve.
The request’s semantic fields are not the same thing as its compressed wire body.

### 6. Body recovery often works best by dumping the framework object, then decoding externally
The TTNet/FormUrlEncodedTypedOutput material suggests a powerful operator workflow:
- intercept the request/response wrapper object in-app
- serialize its fields to JSON/loggable form
- externally decode `buf`, compression, URL encoding, or wrapper metadata
- only then reason about the business semantics

This is a great example of using the app as a structure oracle while keeping the heavy decoding logic outside the target.

### 7. Custom SSL/Cronet stacks turn traffic recovery into a trust-boundary problem
The Cronet/custom-SSL articles reinforce a durable lesson:
- generic pinning bypass scripts may fail when the app uses custom SSL/Cronet verification paths
- the analyst must then move to the app’s actual trust boundary:
   - patch `SSL_CTX_set_custom_verify`
   - patch the final verdict in `libsscronet.so`
   - intercept a higher framework response object instead of insisting on proxy capture

This aligns tightly with earlier Android and protocol findings.

### 8. Complex “protocol” targets are often layered artifact pipelines, not single algorithms
The ebook/article material is especially useful because it broadens the notion of protocol recovery:
- database key recovery
- container/header parsing
- custom transform layers (base64 / RC4 / custom table codecs / AES / decompression)
- PDF/EPUB stream-level filter removal

This gives the KB a better general category:
- **protocol/container recovery as layered artifact decoding**, not just socket traffic reversal.

## Concrete operator takeaways worth preserving

### A. Framed-RPC recovery workflow
Reusable sequence:
1. identify the framing family (gRPC/HTTP2, protobuf payloads, custom RPC shell)
2. recover the message schema separately from the transport
3. recover the service/method contract separately from field-level sign generation
4. use a compatible stub/client shell when possible instead of stitching raw bytes by hand

### B. Trace-Block divergence workflow for execution-assisted recovery
Reusable sequence:
1. if emulator/unidbg output is wrong, do not immediately read more pseudocode
2. trace executed basic blocks in the emulated path
3. trace the same path in the real app
4. compare and find the first divergence
5. inspect the divergence for missing IO, environment, file, process-name, or hook assumptions
6. repair that precondition before resuming algorithm work

### C. Compression/encoding peel workflow for request bodies
Reusable sequence:
1. distinguish semantic request fields from body wrappers/compression/encryption
2. dump the wrapped body object if possible
3. identify content type, compression type, and wrapper flags
4. decode compressed/encoded buffers externally
5. only then reason about business parameters and signatures

### D. Trust-boundary relocation workflow for custom SSL/Cronet stacks
Reusable sequence:
1. determine whether generic proxy/pinning tooling fails because the app owns its own trust stack
2. locate the actual trust-verdict boundary (custom verify callback, patched SSL verdict, framework response object)
3. choose among:
   - patch trust verdict
   - hook custom verify setup
   - intercept framework plaintext objects
4. stop insisting on ordinary system-SSL hooks once the app’s custom trust boundary is clear

### E. Layered container/protocol artifact recovery workflow
Reusable sequence:
1. separate metadata/key sources (db/config/headers) from content-transform layers
2. reconstruct the key pipeline first
3. identify per-layer transforms (table codec, RC4, AES, compression, custom PDF filter, etc.)
4. decode one layer at a time
5. rebuild a clean analysis artifact before trying to consume the final content

## Candidate KB implications
This batch strongly supports or suggests improvements to:
- protocol/network subtree notes
- runtime-behavior and execution-assisted recovery notes
- transport/trust-boundary selection notes

Potential future child-note opportunities:
- framed-RPC recovery note (gRPC/protobuf over transport shells)
- Trace-Block divergence workflow note
- compression/encoding peel workflow note
- custom trust-boundary relocation note for Cronet/custom SSL stacks
- layered container/protocol artifact recovery note

## Confidence / quality note
This is a strong second protocol batch because it broadens “protocol RE” beyond packets while staying practical.

Its best contribution is the recurring lesson that modern protocol recovery is often a question of **peeling layers in the right order and choosing the right boundary to observe or patch**, not of heroic raw-byte reasoning.
