# Source Notes — Descriptor ownership-transfer / completion-visibility on non-coherent paths

Date: 2026-03-24
Purpose: support a practical protocol / firmware continuation note for the recurring case where a descriptor/ring/completion chain is already visible, but the real analyst miss is still one layer narrower:

- descriptor or completion bytes exist in shared memory
- one owner / valid / tail / WR_IDX / doorbell edge may publish them
- software or the peer still cannot trust them until ordering / freshness / cache visibility conditions are satisfied
- one later reclaim / reuse / callback / wakeup proves the earlier handoff actually mattered

## Scope
This note is intentionally practical and case-driven.
It does **not** try to restate all of DMA theory.
It preserves the operator pattern that repeatedly shows up in firmware / driver / queue-heavy reversing when publication and completion are already plausible, but trust semantics still drift:

- the ring is no longer the mystery
- the real question is when ownership changes in a way the other side may trust
- non-coherent cache visibility, freshness bits, and reclaim semantics often explain why “the bytes are there” is still not enough
- the next useful output is one narrower workflow stop rule for rehosting, emulation, or static continuation

## External research performed
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries used:
1. `Linux DMA API dma_sync_single_for_cpu dma_sync_single_for_device non-coherent descriptor ring stale completion reverse engineering`
2. `descriptor ring cache coherency dma_rmb dma_wmb device sees stale descriptors completion queue embedded firmware`
3. `doorbell descriptor ownership transfer cache visibility non coherent systems DMA API barrier completion ring`

Audit artifact:
- `sources/firmware-protocol/2026-03-24-descriptor-cache-visibility-search-layer.txt`

## Search audit
Search sources requested:
- exa
- tavily
- grok

Search sources succeeded:
- exa
- tavily
- grok

Search sources failed:
- none

Exa endpoint:
- `http://158.178.236.241:7860`

Tavily endpoint:
- `http://proxy.zhangxuemin.work:9874/api`

Grok endpoint:
- `http://proxy.zhangxuemin.work:8000/v1`

Degraded-mode note:
- not degraded for search execution
- some fetched pages remained extractor-truncated, so claims below stay conservative and workflow-centered

## Supporting source signals

### 1. Linux DMA API documentation makes ownership transfer explicit
Sources:
- `https://docs.kernel.org/core-api/dma-api-howto.html`
- `https://docs.kernel.org/core-api/dma-api.html`

High-signal findings:
- the Linux DMA API treats CPU-vs-device access as an ownership problem, not just an address problem
- coherent allocations reduce cache-management burden, but even coherent memory may still need write-buffer flushing before telling the device to consume it
- non-coherent support exists specifically because some platforms require explicit synchronization for trustworthy CPU/device sharing
- DMA descriptor pools are often intentionally allocated from coherent memory because queue metadata is especially sensitive to trust/visibility mistakes

Why it matters:
- this sharpens the KB’s descriptor note: ownership transfer is not merely a tail move or interrupt arrival
- if the target is non-coherent or mixed-coherency, the analyst must preserve when software/device ownership changes and what synchronization makes that visible

### 2. Linux memory-barrier guidance reinforces publish-before-trust discipline
Source:
- `https://docs.kernel.org/core-api/wrappers/memory-barriers.html`

High-signal findings:
- device-facing ordering is not safely inferred from ordinary straight-line code alone
- DMA/cache-coherency guidance explicitly distinguishes memory contents from when another observer may trust them
- DMA-specific barriers such as `dma_rmb()` / `dma_wmb()` exist because publish/consume order at device boundaries is a narrower problem than general CPU-only ordering

Why it matters:
- this directly supports the practical stop rule for reverse engineering:
  - do not overclaim from descriptor bytes alone
  - preserve the first ordering edge that makes the peer’s trust rational
  - treat visibility semantics as part of the proof object, not just implementation trivia

### 3. Search results repeatedly emphasized ownership handoff and stale-read failure modes
Representative source signals from the search set:
- Stack Overflow discussion on `dma_sync_single_for_cpu()` vs `dma_sync_single_for_device()` framed the issue as ownership transfer between CPU and DMA engine
- LKML results around `dma_rmb()` / `dma_wmb()` and Rx descriptor reads reinforced that descriptor-consumption bugs often come from ordering and freshness, not only wrong field layout
- practical cache-coherency writeups and vendor/community notes repeatedly described the recurring embedded failure mode where DMA writes land in memory while the CPU still reads stale cache lines

Why it matters:
- this is exactly the analyst trap the KB needs to remember:
  - “completion bytes exist” is weaker than “completion is fresh and trustworthy”
  - publication, cache visibility, and reclaim should be tracked as one contract

### 4. Existing KB branch structure was already close, but one practical continuation needed tightening
Existing related pages already covered:
- broad mailbox/doorbell publish→completion proof
- broader descriptor tail-kick and completion chains
- peripheral/MMIO effect proof
- ISR/deferred consequence proof

What was still missing:
- a more explicit practical reminder that on descriptor-heavy firmware/driver targets, the next bottleneck can be **non-coherent visibility truth** rather than broader doorbell or interrupt narration
- a cleaner stop rule for when to leave broad queue anatomy and instead freeze:
  - ownership state
  - publish order
  - trust/freshness rule
  - cache/sync rule
  - reclaim proof

## Distilled practical pattern
A useful chain to preserve is:

```text
descriptor or completion record prepared
  -> publish edge moves owner / valid / tail / WR_IDX / freshness state
  -> ordering / sync makes that publication trustworthy to the peer
  -> peer consumes or software observes fresh completion
  -> reclaim / wakeup / slot reuse proves durable consequence
```

## Operator heuristics to preserve
- Do not confuse descriptor contents with descriptor visibility.
- Do not confuse interrupt arrival with freshness or trust.
- On non-coherent systems, preserve cache invalidation / sync helpers as part of the proof object, not as cleanup noise.
- Prefer one compare pair where the same bytes exist but only one side performs the trust-enabling publish/sync edge.
- Treat owner bits, phase tags, and WR_IDX/RD_IDX movement as trust semantics, not merely structural fields.
- Once this contract is frozen, hand off quickly to one next concrete task:
  - rehosting/model realism
  - narrower reclaim/MMIO effect proof
  - later ISR/deferred consequence proof

## Candidate canonical KB mapping
Most directly supports:
- `topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md`

Also strengthens:
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/mailbox-doorbell-command-completion-workflow-note.md`
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`

## Limits / conservative claims
This run does **not** claim:
- one universal non-coherent descriptor protocol
- that every target needs explicit `dma_sync_*()`-style reasoning
- that Linux DMA API semantics map one-to-one onto every proprietary RTOS or firmware implementation

This run **does** claim conservatively:
- descriptor-heavy reversing repeatedly stalls on ownership/visibility truth rather than on missing ring discovery alone
- non-coherent cache visibility and freshness rules are recurring practical causes of false confidence
- the KB should preserve this as a practical continuation seam because it changes where analysts place hooks, what compare pairs they freeze, and when they stop broad structural documentation

## Bottom line
When the ring is already visible, the next useful question is often not “what other fields can I name?”

It is:
- when does ownership really transfer?
- what makes that transfer trustworthy to the other side?
- how do cache/freshness/order rules affect that trust?
- and what reclaim or reuse fact proves the earlier handoff actually mattered?

That is the narrower practical move this source note exists to preserve.
