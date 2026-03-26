# Descriptor Publish-vs-Trust and DMA Sync Notes

Date: 2026-03-26
Branch: protocol / firmware practical
Seam: descriptor ownership-transfer / completion-visibility
Search artifact: `sources/firmware-protocol/2026-03-26-1316-descriptor-publish-vs-trust-search-layer.txt`

## Why this note exists
The descriptor-ownership branch already preserved publish ordering, freshness, reclaim, and non-coherent visibility risks.

What still deserved a tighter source-backed reminder was a thinner but very practical stop rule:
- **kick / notify / doorbell is not automatically trust transfer**
- a queue can be notified before the analyst has proved that descriptor content became device-trustworthy
- a completion-looking slot can be visible before the CPU has proved it may trust the bytes on a non-coherent or streaming-DMA path

That distinction matters because analysts repeatedly over-read:
- `avail->idx` / tail updates
- doorbell writes
- interrupts
- or completion-looking bytes in RAM

as if any one of those alone proves the full publication/trust contract.

## Retained source-backed reminders

### 1. Virtio-style queue docs make publish ordering explicit, but notify is still a narrower event than trust
Virtio material and practical virtqueue write-ups remain useful because they preserve a recurring queue discipline:
- driver prepares descriptors first
- then publishes them through the avail ring / index movement
- and only then notifies the device if notification is needed
- after publication, the driver should stop modifying the exposed descriptor/buffer because ownership has moved

Operator consequence:
- when reversing a descriptor-driven path, do not stop at a kick/doorbell write if you have not yet frozen whether descriptor contents were fully prepared and ordered before the publish edge
- treat notify as a candidate work announcement unless the case-specific ordering/ownership contract proves it is also the trust boundary

### 2. Linux DMA guidance preserves the coherent-vs-streaming split as a first-class operator question
Kernel DMA guidance remains valuable because it keeps the memory class question explicit:
- coherent/shared mappings reduce ordinary cache-visibility surprises, though ordering can still matter
- streaming or non-coherent mappings can require explicit CPU/device synchronization and ownership transfer before one side may trust the bytes
- APIs like `dma_sync_single_for_device()` and `dma_sync_single_for_cpu()` exist precisely because "bytes exist somewhere" is weaker than "the current owner may trust them now"

Operator consequence:
- classify the case early as closer to coherent shared descriptor memory or closer to streaming/non-coherent DMA-backed visibility
- if that classification is still unresolved, do not flatten the whole problem into generic ring semantics

### 3. Completion visibility is often a two-part question: publish happened, but CPU trust still needs proof
The DMA guidance and descriptor-family examples together preserve an important split:
- device-side completion publication may already have happened
- yet the CPU may still need invalidate/sync/ownership-return proof before reading fresh completion content truthfully

Operator consequence:
- when a slot looks structurally correct but software still ignores it, ask separately:
  1. did the producer publish ownership/freshness/index progress?
  2. does the consumer still need explicit CPU-side trust transfer before reading the bytes honestly?

### 4. Interrupts and doorbells are often correlation anchors, not the whole ownership story
Practical queue material remains useful because it illustrates the common split between:
- submission notification
- device processing
- used/completion publication
- interrupt/driver wakeup
- later reclaim or slot reuse

Operator consequence:
- interrupts and doorbells are good alignment anchors for compare traces
- but they are weaker than one proved ownership transition, freshness transition, or sync boundary
- do not let them become the final proof object just because they are easy to observe

## Practical stop rule worth preserving
When a descriptor-driven case is already visible enough to inspect, explicitly separate:
1. **prepared**
   - descriptor / buffer bytes were assembled
2. **published**
   - owner/index/freshness state changed so the peer could treat the work as available
3. **notified**
   - doorbell/kick/interrupt-facing signal happened
4. **trustworthy to current consumer**
   - ordering and, on non-coherent or streaming paths, explicit sync/ownership return make the bytes safe to trust
5. **reclaimed / reusable**
   - later reclaim, free, or slot-reuse proves durable completion

A compact operator warning to preserve is:
- **published != notified != trusted != reclaimed**

## Conservative synthesis
This note does **not** claim that every queueing system is virtio, that every firmware target uses Linux DMA APIs, or that every doorbell precedes/equals one universal publish edge.

It preserves a narrower practical lesson:
- if a case already shows descriptors, indices, doorbells, or completion slots, the next analyst value usually comes from freezing the exact relationship between publication, notification, trust, and reclaim
- the real trap is not missing one more field name
- the real trap is collapsing several different ownership transitions into one vague "the queue happened" story

## Primary sources retained
- OASIS virtio specification / rendered virtio materials
  - <https://docs.oasis-open.org/virtio/virtio/v1.1/virtio-v1.1.html>
- Red Hat virtqueue write-up
  - <https://www.redhat.com/en/blog/virtqueues-and-virtio-ring-how-data-travels>
- Linux kernel DMA API howto
  - <https://www.kernel.org/doc/html/latest/core-api/dma-api-howto.html>
- Linux dynamic DMA mapping guide
  - <https://www.kernel.org/doc/Documentation/DMA-API-HOWTO.txt>
