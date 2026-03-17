# Run Report — 2026-03-17 14:13 Asia/Shanghai — `sperm/md` Protocol / network batch 2

## Summary
This run continued the protocol/network branch with a second cluster focused on:
- framed RPC recovery (especially gRPC + protobuf)
- Trace Block comparison for correcting execution-assisted recovery
- TTNet/Cronet wrapped-body and compressed-body decoding
- custom SSL/Cronet trust-boundary bypass
- layered container / DRM / document artifact decoding as protocol-adjacent work

This remained a source-first extraction pass with no canonical topic edits yet.

## Scope this run
- move beyond basic serialization and wire capture into framed-RPC and layered-body recovery
- preserve durable workflows rather than app/vendor trivia
- add another protocol source note and run report

## Sources consulted
From `Facetomyself/sperm/tree/main/md`:
- `simpread-猿人学 - app 逆向比赛第四题 grpc 题解.md`
- `simpread-某车联网 App 通讯协议加密分析 (三) Trace Block.md`
- `simpread-某电子书阅读器加密协议分析.md`
- `simpread-逆向某短视频 App 搜索协议：破解加密通信，还原真实数据！.md`
- `simpread-对 APP 逆向抓包的实践.md`
- `simpread-抖音抓包.md`

## New findings
### 1. Framed RPC recovery works best when the service contract is restored
The gRPC material shows a useful progression from bytes to messages to methods to replay-capable stubs.

### 2. Trace Block comparison is a strong debugging primitive for protocol/sign recovery
It is especially valuable when unidbg or other execution-assisted methods are close-but-wrong.

### 3. Compression and encoding layers deserve their own explicit recovery stage
The TTNet/FormUrlEncodedTypedOutput material demonstrates this very clearly.

### 4. Custom trust stacks require trust-boundary relocation
Cronet/custom SSL flows often invalidate generic pinning-bypass playbooks and force the analyst toward the app’s real verification boundary.

### 5. Layered artifact decoding belongs in the same operator family as protocol recovery
The ebook/document example widens the branch in a useful way without making it vague.

## Reflections / synthesis
After two protocol batches, the branch is becoming nicely coherent.

Batch 1 emphasized:
- structure-owner selection
- serialization-vs-crypto triage
- endpoint redirection and plaintext boundary interception

Batch 2 now adds:
- framed service-contract restoration
- Trace-Block divergence debugging
- compression/encoding peel workflows
- trust-boundary relocation for custom SSL/Cronet stacks

That is a strong and practical structure for later canonical synthesis.

## Candidate topic pages to create or improve
No canonical topic pages were edited this run.

Likely future canonical targets after more accumulation:
- a note on framed-RPC recovery
- a note on Trace-Block divergence debugging
- a note on compression/encoding peel workflows
- a note on custom trust-boundary relocation
- a note on layered container/protocol artifact recovery

## Next-step research directions
With protocol/network now reasonably covered, the final planned major lane is:
- **iOS**

Given the standing instruction to keep going without interruption, moving into the iOS branch next is the natural next step.

## Concrete scenario notes or actionable tactics added this run
This run preserved several reusable tactics in the new source note, including:
- recovering service contracts for framed RPC protocols
- using Trace Block divergence to debug execution-assisted recovery
- peeling compression/encoding layers before business semantics
- relocating interception to custom trust boundaries under Cronet/custom SSL
- decoding layered content containers as artifact pipelines

## Files changed this run
- `research/reverse-expert-kb/sources/protocol-and-network-recovery/2026-03-17-sperm-protocol-network-batch-2-notes.md`
- `research/reverse-expert-kb/runs/2026-03-17-1413-sperm-protocol-network-batch-2.md`

## Outcome
The reverse KB now has a second Protocol / network extraction note from the `sperm/md` repository, centered on framed-RPC recovery, Trace-Block divergence debugging, compression/encoding peel workflows, and custom trust-boundary relocation.
