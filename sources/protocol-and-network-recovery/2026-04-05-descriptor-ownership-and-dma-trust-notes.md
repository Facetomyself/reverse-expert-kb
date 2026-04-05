# Source notes — descriptor ownership transfer, DMA trust handoff, and completion visibility

Date: 2026-04-05 14:28 Asia/Shanghai / 2026-04-05 06:28 UTC
Topic: descriptor ownership-transfer and completion-visibility realism
Author: Reverse Claw

## Why this pass happened
Recent runs had already strengthened malware/Linux persistence, protocol request-lifetime realism, protected-runtime next-state recovery, runtime-evidence object-identity rules, and native watcher delivery semantics.
This hour needed a real external-research-driven pass on a thinner firmware/protocol seam.

The existing descriptor-ownership workflow note was the right target:
- it already existed canonically
- it is practical and mechanism-bearing
- it still benefited from sharper source-backed reminders about coherent vs non-coherent DMA trust transfer, memory barriers, and ownership semantics

## Practical question
What narrower trust-contract reminders matter most once descriptor fill and queue shape are already visible, but the analysis still overreads publication or completion visibility?

## Retained high-signal points
### 1. DMA APIs make ownership transfer explicit
Linux DMA API material is useful because it states the driver/device ownership split directly:
- streaming mappings need explicit ownership management between CPU and device
- `dma_sync_*for_device()` and `dma_sync_*for_cpu()` style boundaries exist specifically because visibility/trust is not automatic on all paths

Retained operator consequence:
- descriptor bytes present in CPU-visible memory are weaker than device-trustworthy descriptor ownership
- completion bytes present in backing memory are weaker than CPU-trustworthy completion visibility
- this is a trust-contract problem, not just a queue-layout problem

### 2. Memory barriers and MMIO observation are narrower than “publish happened”
Kernel memory-barrier material is useful because it preserves the thinner split between:
- writing publication metadata
- the peer truthfully observing that publication
- stale data still being visible until the required ordering/observation boundary is crossed

Retained operator consequence:
- “published” is not always the same thing as “observed by peer”
- interrupts or MMIO status reads may still lag or only partially witness the real trust boundary

### 3. Virtio is a good practical reminder that ring role labels are not the whole contract
Virtio material is useful because it clearly separates driver area/device area and reinforces that the driver must not keep modifying descriptors once ownership has moved.

Retained operator consequence:
- avail/used role labeling is useful but still weaker than a trustworthy ownership-transfer story
- queue publication semantics should stay separate from later completion/reclaim semantics

### 4. DMAengine docs reinforce descriptor-lifetime ownership after submit/completion
DMAengine client docs are useful because they say the submitted descriptor belongs to the engine after submit and some metadata becomes unsafe after completion callback.

Retained operator consequence:
- ownership changes are not conceptual decoration; they affect what memory or metadata is still trustworthy to touch
- descriptor lifetime and callback-time reuse/free semantics are part of the same practical contract as publish and reclaim boundaries

## Conservative synthesis used in KB
Useful branch rule preserved:

```text
descriptor or completion bytes visible
  != peer may already trust them
  != ownership transfer is complete
  != durable completion consequence proved
```

Additional branch memory preserved:
- CPU->device trust transfer can be a first-class proof object on streaming/non-coherent paths
- memory barriers or posted-write drain can separate publication from peer observation
- completion trust can still lag behind apparent DMA-finished or interrupt-visible status
- reclaim/reuse remains the strongest consequence-side proof that the earlier trust boundary mattered

## Sources consulted
### Explicit multi-source search attempt
All searches were run via explicit `search-layer` source selection:
- `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok ...`

Search themes used:
- Linux DMA API ownership and `dma_sync_*` semantics
- virtio ring ownership / used-vs-avail / publication semantics
- memory barriers and descriptor visibility / stale data

### Representative surfaced materials
- Linux DMA API HOWTO / core DMA API docs
- Linux DMA Engine API guide
- Linux memory-barriers documentation
- OASIS virtio spec and explanatory virtio ring material
- Red Hat virtqueue explanation

## Search audit material for run report
Requested sources:
- Exa
- Tavily
- Grok

Observed outcome across this source pass:
- Exa: succeeded with usable hits on all three queries
- Tavily: succeeded with usable hits on all three queries
- Grok: invoked and failed with HTTP 502 Bad Gateway on all three queries

Endpoints / execution paths used:
- Exa endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`
- Tavily endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`
- Grok endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`

## What this changed in KB terms
This pass did not justify a new descriptor/ring sibling page.
The correct move was to strengthen the existing descriptor-ownership workflow note by preserving sharper reminders about:
- CPU->device ownership transfer
- memory-barrier / observation split
- non-coherent completion trust
- reclaim/reuse as consequence-side proof

The durable operator value is keeping descriptor presence, publication, peer trust, and durable consequence explicitly separate.
