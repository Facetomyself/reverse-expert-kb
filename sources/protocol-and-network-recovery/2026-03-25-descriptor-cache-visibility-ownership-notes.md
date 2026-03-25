# Descriptor Cache Visibility / Ownership Transfer Notes

Date: 2026-03-25
Branch: protocol / firmware practical
Seam: descriptor ownership-transfer / completion-visibility
Search artifact: `sources/firmware-protocol/2026-03-25-descriptor-cache-visibility-search-layer-2020.txt`

## Why this note exists
The descriptor-ownership branch already preserved publication, freshness, and reclaim semantics well.

What still deserved a tighter source-backed reminder was the operator split between:
- **shared coherent descriptor memory** where the main issue is publish ordering / freshness / ownership
- **streaming or non-coherent DMA-backed visibility** where completion-looking bytes can still be untrustworthy until explicit CPU/device ownership transfer or cache synchronization occurs

That distinction matters because analysts often over-read:
- "I can see the completion bytes in RAM"
- or "the slot contents look right in a dump"

as if those alone prove trustworthy completion visibility.

## Retained source-backed reminders

### 1. Linux DMA API: ownership transfer is an explicit question, not a vibe
Kernel DMA API docs preserve two practical reminders:
- coherent memory lets both sides observe memory without ordinary cache-coherency surprises, though ordering/write-buffer issues can still matter
- streaming/non-coherent mappings may require explicit sync/ownership transfer, and Linux exposes this directly through APIs like `dma_sync_single_for_cpu()` / `dma_sync_single_for_device()` and `dma_need_sync()`

Operator consequence:
- if a target appears descriptor/ring-heavy but its completion/storage path behaves like streaming DMA or non-coherent sharing, the analyst should freeze the **first explicit CPU-may-trust-this-now** boundary rather than stopping at visible bytes

### 2. Linux DMA howto: cacheline sharing and non-coherent receive semantics are first-class failure modes
The DMA howto is useful because it warns that DMA-from-device buffers can still be corrupted or misread when CPU-written fields share cache lines or when non-coherent cache behavior is not respected.

Operator consequence:
- when a completion record sits near driver-owned metadata, flags, or software bookkeeping, a structurally correct slot dump is still weaker than proving the alignment/ownership/sync contract the runtime actually trusts

### 3. Virtio ordering: publish index movement is itself a trust boundary
Virtio material remains useful as a family example because it makes one rule unusually explicit:
- descriptor/ring contents must be fully visible before the publish/index movement that tells the peer to trust them

Operator consequence:
- the practical proof object is often not "descriptor bytes exist" but the tighter chain:
  - fill
  - order/barrier/sync
  - publish index/owner/freshness move
  - consumer trust
  - reclaim

## Practical KB refinement worth preserving
A tighter operator stop rule for descriptor-heavy cases:
- do not stop at "completion bytes are visible"
- separate these questions explicitly:
  1. were the bytes written?
  2. did ownership/freshness/publish state change?
  3. does this memory class require explicit sync before CPU trust?
  4. what reclaim/reuse fact proves the consumer actually trusted it?

A useful compact comparison language is:
- **published bytes**
- **trustworthy completion visibility**
- **consumer-owned after sync/order boundary**
- **reclaimed / reusable**

## Conservative synthesis
This note does **not** claim all descriptor systems implement Linux DMA APIs or virtio-style rings.

It preserves a narrower workflow lesson:
- descriptor or completion bytes can be visible before they are trustworthy
- on some targets the missing boundary is freshness/owner/phase publication
- on others it is CPU/device synchronization for non-coherent or streaming mappings
- the analyst should prove which one actually owns the case before broadening taxonomy

## Primary sources retained
- Linux kernel docs — Dynamic DMA mapping Guide
  - <https://docs.kernel.org/core-api/dma-api-howto.html>
- Linux kernel docs — Dynamic DMA mapping using the generic device
  - <https://kernel.org/doc/html/latest/core-api/dma-api.html>
- OASIS virtio specification / rendered virtqueue ordering reference
  - <https://stefanha.github.io/virtio/vhost-user-slave.html>
