# Plaintext/frame visibility vs first protocol consumer notes

Date: 2026-04-08
Branch target: protocol practical workflows / parser-to-state seam
Purpose: preserve a source-backed practical refinement for framed transport cases where decrypted/plaintext visibility exists, but the first local parser/dispatch consumer that actually owns behavior is still unproven.

## Research intent
Tighten the existing protocol parser-to-state workflow note around a narrower liar:
- decrypted/plaintext transport visibility
- framed message visibility
- parse/decode capability
- first local parser/dispatch/state consumer

The goal is not a generic TLS or gRPC page.
The goal is a reusable stop rule for protocol consequence localization.

## Search artifact
Raw multi-source search artifact:
- `sources/protocol/2026-04-08-1556-protocol-plaintext-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Exa returned usable gRPC framing, protobuf, and Wireshark/TLS surfaces
- Tavily returned usable gRPC framing, protobuf parser, and Wireshark/TLS surfaces
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` through the configured proxy path

## Retained sources
1. gRPC HTTP/2 protocol documentation
   - repeated length-prefixed messages carried inside HTTP/2 DATA frames
   - compression framing reminders
2. Protocol Buffers parser / parseFrom documentation surfaces
   - parser/stream/message parsing APIs
3. Wireshark TLS / HTTP2 documentation surfaces
   - decrypted TLS visibility and HTTP/2 inspection surfaces

## High-signal retained findings

### 1. Decrypted TLS/plaintext visibility proves transport readability, not local consumer ownership
Wireshark/TLS-style documentation already supports the narrow claim that transport encryption can be peeled back enough to observe plaintext protocol traffic.

Practical consequence:
- seeing plaintext or HTTP/2 frames is a real observation win
- it is still weaker than proving which local parser/dispatch consumer turns that material into state/reply behavior

### 2. gRPC framing keeps transport/frame truth separate from message-consumer truth
The gRPC HTTP/2 protocol material preserves that repeated length-prefixed gRPC messages ride inside HTTP/2 DATA frames and may involve compression framing.

Practical consequence:
- extracting one gRPC message from decrypted stream/frame material is still weaker than proving which local service/parser/dispatch path actually owns the behavioral consequence
- frame visibility and application-level consumer truth should remain separate

### 3. Protobuf parse capability proves decodability, not the first consequence-bearing consumer
Parser/parseFrom surfaces make it clear that bytes can be parsed into message objects through multiple parser entry points.

Practical consequence:
- one successful decode is not yet proof that the first meaningful local consumer has been frozen
- the real target is the first parse/dispatch/state edge that predicts reply, transition, queueing, or other consequence

## Practical synthesis worth preserving canonically
A compact stop-rule ladder for this seam is:

```text
decrypted/plaintext transport visibility
  != framed message visibility
  != parse/decode capability
  != first local parser/dispatch consumer
```

This keeps four different wins separate:
1. **plaintext transport visibility**
   - traffic is readable after decryption or boundary relocation
2. **framed message visibility**
   - one HTTP/2/gRPC/length-prefixed application message can be isolated
3. **parse/decode capability**
   - one message can be decoded into structured fields/objects
4. **first local parser/dispatch consumer truth**
   - one local state/reply/queue/gate owner predicts behavior

## Best KB use of this material
This material is best used to sharpen the existing protocol parser-to-state workflow note.
It should not become a broad TLS/gRPC taxonomy page.

The operator-facing value is:
- do not overclaim from plaintext visibility alone
- do not overclaim from framed-message extraction alone
- do not overclaim from successful protobuf/gRPC decode alone
- stop only when one local parse/dispatch consumer is frozen strongly enough to explain state or reply behavior

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source result set.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked; its failure is recorded clearly.
