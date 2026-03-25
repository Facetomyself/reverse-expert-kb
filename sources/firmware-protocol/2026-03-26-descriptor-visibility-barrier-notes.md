# Source Notes — descriptor visibility, notify-vs-trust, and DMA ownership-transfer boundaries

Date: 2026-03-26
Purpose: support a practical refinement of the descriptor ownership / completion visibility branch so the KB more explicitly preserves a recurring operator trap:

- a tail / avail idx / WR_IDX / doorbell / notify edge is often only a publish or announce edge
- it is not automatically the whole trust boundary
- on streaming or non-coherent paths, CPU->device and device->CPU trust may each depend on a narrower synchronization edge
- completion bytes existing in memory is still weaker than CPU-trustworthy completion

## Scope
This note is intentionally workflow-centered.
It does not try to restate all DMA, virtio, or NVMe theory.
It preserves the narrower analyst move that becomes decisive after ring anatomy is already mostly understood:

- stop asking only “where is the doorbell / avail idx / completion slot?”
- ask whether that observed edge merely announces work or actually makes the contents trustworthy to the peer/CPU
- preserve the smallest ownership/sync/freshness fact that explains why one run works and another stalls

## External research performed
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries used:
1. `Linux DMA API coherent vs streaming dma_sync_single_for_device dma_sync_single_for_cpu ring descriptor ownership visibility doorbell driver`
2. `virtio split ring avail idx used idx memory barrier notification descriptor visibility driver`
3. `NVMe submission completion queue phase tag doorbell memory ordering ownership visibility reverse engineering`

Audit artifact:
- `sources/firmware-protocol/2026-03-26-descriptor-visibility-barrier-search-layer.txt`

## Search audit
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- exa
- tavily

Failed sources:
- grok
  - actual invocation was attempted through `search-layer --source exa,tavily,grok`
  - Grok returned repeated `502 Bad Gateway` errors during this run

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Degraded-source-set note:
- this still counts as a real external-research attempt because all three requested sources were explicitly invoked
- synthesis below relies conservatively on Exa + Tavily plus direct page fetches

## High-signal source signals

### 1. Linux DMA API documentation keeps ownership-transfer explicit
Source:
- `https://docs.kernel.org/core-api/dma-api.html`

High-signal findings:
- coherent memory removes some cache-management burden, but even coherent memory may still require flushing write buffers before notifying the device
- `dma_need_sync()` exists precisely because some mappings still require explicit transfer of ownership/trust
- streaming mappings keep CPU-vs-device access as an ownership problem, not just an addressing problem
- small descriptor objects are commonly placed in coherent DMA pools because queue metadata is especially sensitive to visibility mistakes

Why it matters:
- a ring/descriptor note should not collapse “descriptor bytes exist” into “device may already trust them”
- even if the queue looks correct structurally, CPU->device trust may still hinge on one flush / sync / barrier edge before the producer-visible index or doorbell is moved

### 2. Virtio guidance keeps notification semantics narrower than content trust
Sources:
- `https://docs.oasis-open.org/virtio/virtio/v1.1/csprd01/virtio-v1.1-csprd01-diff.html`
- `https://www.redhat.com/en/blog/virtqueues-and-virtio-ring-how-data-travels`

High-signal findings:
- virtqueue publication is explicitly structured around descriptor area -> avail ring update -> notification
- the specification/search results emphasize a suitable memory barrier before publishing `idx`
- Red Hat’s explainer is clear that once the driver exposes a descriptor, ownership changes, but that statement sits on top of ordered publication rather than replacing it
- notification only standardizes that the other side should look; it does not by itself explain every architecture-specific trust/visibility condition

Why it matters:
- `avail->idx` / tail / doorbell is often the **announce** edge, not the whole proof object
- the analyst should preserve whether “notify happened” and “peer may truthfully consume the fully prepared contents” are actually the same boundary in the target

### 3. DMA ownership handoff remains the useful mental model for stale-read cases
Sources/signals:
- LWN DMA API change summary surfaced in search results
- Stack Overflow / mailing-list search hits repeatedly framed `dma_sync_single_for_cpu()` vs `dma_sync_single_for_device()` as ownership transfer

High-signal findings:
- `dma_sync_*for_device()` is the practical pattern for returning a streaming-mapped buffer to device ownership
- `dma_sync_*for_cpu()` is the practical pattern for making device-written contents trustworthy to CPU readers again
- stale-read failures are commonly explained by missing one of these ownership-transfer steps, not by missing ring structure

Why it matters:
- this gives the KB a compact stop rule:
  - do not overclaim from doorbell/idx movement alone
  - do not overclaim from completion bytes alone
  - preserve one explicit CPU->device and/or device->CPU trust boundary when the target behaves like a streaming/non-coherent path

### 4. NVMe/virtio-style queue families reinforce the difference between visible state and trustworthy state
Representative source signals:
- NVMe writeups/search results repeatedly distinguish queue progress fields, phase/freshness state, and actual command/completion interpretation
- virtio results repeatedly emphasize ordering around avail/used publication

Why it matters:
- this is the recurring operator error worth preserving in the KB:
  - visible queue movement is weaker than trustworthy queue movement
  - a populated slot is weaker than a fresh slot
  - a fresh slot is weaker than a consumed-and-reclaimed slot with downstream consequence

## Distilled practical pattern
The practical chain this run strengthens is:

```text
descriptor or completion contents prepared
  -> ownership/sync edge makes those contents trustworthy to the peer or CPU
  -> publish / idx / tail / notify edge announces availability
  -> peer or CPU consumes only under freshness/ownership rules
  -> reclaim / reuse / wakeup proves durable consequence
```

Some targets reverse the perceived order because publish and sync sit adjacent in code.
The key analyst task is to determine whether they are actually the same proof boundary.

## Practical stop rules to preserve
- Do not treat doorbell/notify as automatically equivalent to full trust.
- Do not treat coherent-looking shared memory as proof that the case is coherent in the practical ownership sense.
- On streaming/non-coherent paths, preserve CPU->device trust transfer separately from device->CPU trust transfer when needed.
- Distinguish:
  - bytes exist
  - freshness bit/index changed
  - CPU/device may trust the bytes
  - reclaim/reuse proves the handoff mattered
- When compare runs diverge, prefer one pair where the same descriptor/slot exists in both runs but only one run has the decisive sync/barrier/ownership edge.

## Candidate canonical KB mapping
Most directly supports:
- `topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md`

Also strengthens:
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/mailbox-doorbell-command-completion-workflow-note.md`
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`

## Conservative limits
This run does **not** claim:
- every queueing target should be read through Linux DMA APIs literally
- every doorbell/idx edge is separate from the trust boundary
- every coherent allocation implies the same runtime trust semantics across all firmware/RTOS/device families

This run **does** claim conservatively:
- queue-heavy reversing repeatedly benefits from separating notification/publish edges from trust/ownership edges
- streaming/non-coherent ownership transfer is a recurring practical explanation for “the bytes are there but the run still stalls”
- the KB should preserve this as a practical continuation seam because it directly changes hook placement, compare-pair choice, and when analysts stop broad structural documentation

## Bottom line
Once the ring is already visible, the next useful question is often not:
- where is the next queue field?

It is:
- is this edge only announcing work, or is it the true trust boundary?
- what returns ownership from CPU to device, and later back from device to CPU?
- what freshness rule prevents stale completion overclaim?
- what reclaim/reuse fact proves the earlier handoff actually mattered?
