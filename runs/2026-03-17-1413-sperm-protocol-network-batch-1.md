# Run Report — 2026-03-17 14:13 Asia/Shanghai — `sperm/md` Protocol / network batch 1

## Summary
This run began the third planned major lane after Android/protected-runtime and Browser/JS:
- **Protocol / network**

The first protocol batch focused on:
- Protobuf structure recovery
- QUIC recovery by endpoint redirection rather than passive decrypt-first capture
- OkHttp/Retrofit plaintext-boundary interception
- field-pipeline recovery for request parameters

As before, this was a source-first extraction pass with no canonical topic edits yet.

## Scope this run
- start the protocol/network branch from the most reusable and cross-branch-compatible themes
- extract durable workflows rather than target-specific recipes
- preserve the results as a source note and run report

## Sources consulted
From `Facetomyself/sperm/tree/main/md`:
- `simpread-Protobuf 协议逆向解析 - APP 爬虫 .md`
- `simpread-某某 App protobuf 协议逆向分析.md`
- `simpread-猿人学 2022 逆向比赛第七题 quic.md`
- `simpread-分析 okhttp3-retrofit2 - 截流某音通信数据.md`
- `simpread-逆向某物 App 登录接口：抓包分析 + Frida Hook 还原加密算法.md`

One intended `M3U8` file path did not resolve locally and was therefore skipped in this batch.

## New findings
### 1. Serialization-vs-crypto triage is a crucial early decision
The Protobuf material shows how much effort is saved when opaque bytes are correctly classified as structured serialization rather than “mystery encryption.”

### 2. Protobuf recovery is a practical structure-reconstruction pipeline
Sample -> stack/field inspection -> candidate `.proto` -> iterative compile/refine is a strong durable workflow.

### 3. QUIC recovery benefits from observation-surface relocation
Endpoint redirection and analyst-controlled server observation can be dramatically more productive than passive decrypt-first strategies.

### 4. Framework-level plaintext boundaries are often better than wire capture
The OkHttp/Retrofit material reinforces the value of intercepting the first stable byte owner above transport encryption.

### 5. Request protocols are often better treated as secret-bearing field pipelines
Recovering the decisive fields individually is a highly reusable operator strategy.

## Reflections / synthesis
The protocol/network branch starts in a way that fits very neatly with the previous branches.

Android work kept emphasizing:
- cut-point and observation-surface choice.

Browser work kept emphasizing:
- artifact pipelines and topology choice.

Protocol work now begins by emphasizing:
- the owner of structure/plaintext rather than the wire itself.

That symmetry is a strong sign that later canonical synthesis across branches will be productive.

## Candidate topic pages to create or improve
No canonical topic pages were edited this run.

Likely future canonical targets after more protocol batches accumulate:
- protocol/network subtree notes
- a note on serialization-vs-crypto triage
- a note on Protobuf structure recovery
- a note on endpoint redirection for encrypted transports
- a note on framework-plaintext-boundary interception

## Next-step research directions
Continue the protocol/network lane with likely next families including:
- more app-specific protocol/signature cases
- streaming or segment-protocol cases if present
- transport ownership / downgrade / protocol forcing cases
- any additional QUIC / protobuf / framed-binary materials remaining in the source set

## Concrete scenario notes or actionable tactics added this run
This run preserved several reusable tactics in the new source note, including:
- classifying serialization vs crypto before deeper work
- reconstructing `.proto` from field-stack evidence
- redirecting encrypted transports to analyst-controlled endpoints
- intercepting plaintext at framework byte-owner boundaries
- rebuilding requests from secret-bearing field pipelines

## Files changed this run
- `research/reverse-expert-kb/sources/protocol-and-network-recovery/2026-03-17-sperm-protocol-network-batch-1-notes.md`
- `research/reverse-expert-kb/runs/2026-03-17-1413-sperm-protocol-network-batch-1.md`

## Outcome
The reverse KB now has its first Protocol / network extraction note from the `sperm/md` repository, centered on structure-owner selection, plaintext-boundary interception, and endpoint redirection for encrypted transports.
