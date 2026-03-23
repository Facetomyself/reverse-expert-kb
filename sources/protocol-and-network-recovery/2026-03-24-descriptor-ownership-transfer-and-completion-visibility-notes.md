# 2026-03-24 Descriptor Ownership-Transfer and Completion-Visibility Notes

Scope: practical source-backed continuation notes for descriptor/ring cases where queue structure is already visible, but the remaining bottleneck is narrower: ordered publication, ownership transfer, completion freshness, and reclaim-vs-completion proof.

## Mode
external-research-driven

## Why this run
Recent autosync work was drifting toward internal branch-sync and wording maintenance. The protocol / firmware practical branch already had the right leaf family shape, but this specific ownership-transfer / completion-visibility seam was still comparatively thin in practical, source-backed operator guidance.

This run therefore prioritized a real external research pass and turned it into KB-facing workflow improvements rather than another index-only or family-count cleanup.

## Search intent
Need stronger, source-backed practical guidance for cases like:
- descriptor/completion bytes are visible in memory, but software still does not trust them
- publish/tail/doorbell logic seems right, but the peer never consumes or reclaims the slot
- completion interrupts exist, but they do not prove freshness or durable completion
- rehosting/emulation gets queue structure right but still fails on ownership, barrier, or visibility semantics

## Search inputs
Executed via local `search-layer` skill with explicit multi-source request:
- sources requested: `exa,tavily,grok`
- query set:
  - `virtio vring avail used idx ownership barriers reverse engineering`
  - `descriptor ring ownership transfer completion visibility dma coherent memory barrier driver firmware`
  - `NVMe submission completion queue phase tag ownership doorbell reverse engineering`

Raw captured output:
- `sources/firmware-protocol/2026-03-24-descriptor-ownership-completion-visibility-search-layer.txt`

## External sources consulted
Primary practical sources that actually informed the resulting note:
- OASIS VirtIO 1.1/1.2 material surfaced by search-layer
  - `https://docs.oasis-open.org/virtio/virtio/v1.1/csprd01/virtio-v1.1-csprd01-diff.html`
  - `https://docs.oasis-open.org/virtio/virtio/v1.2/cs01/virtio-v1.2-cs01.pdf`
- Red Hat virtqueue explanation
  - `https://www.redhat.com/en/blog/virtqueues-and-virtio-ring-how-data-travels`
- Linux virtio ring implementation / barrier discussion surfaced by search-layer
  - `https://docs.huihoo.com/doxygen/linux/kernel/3.7/virtio__ring_8c_source.html`
  - `https://mails.dpdk.org/archives/dev/2020-April/161651.html`
- SPDK NVMe queue/completion explanation
  - `https://spdk.io/doc/nvme_spec.html`
- Microsoft NVMe completion queue head doorbell docs
  - `https://learn.microsoft.com/en-us/windows/win32/api/nvme/ns-nvme-nvme_completion_queue_head_doorbell`
- Linux amdgpu ring-buffer documentation
  - `https://docs.kernel.org/next/gpu/amdgpu/ring-buffer.html`

## Source-bearing takeaways

### 1. Publication is usually a smaller contract than “the descriptor exists”
Useful external signal:
- VirtIO split ring material repeatedly separates descriptor contents, avail-ring publication, and used-ring return
- Red Hat’s virtqueue explanation explicitly notes that once a descriptor head is published into the avail ring, the driver should stop modifying the exposed descriptor/buffer because it is now under device control

Conservative takeaway:
- the useful RE target is often not broad queue layout but the one smaller edge where contents become peer-trustable
- analyst notes should preserve record contents and publication marker as different proof objects

### 2. Completion freshness is often tracked by ownership/phase/index semantics, not by interrupts alone
Useful external signal:
- SPDK’s NVMe explanation emphasizes that completions are detected by phase-bit freshness in the next expected slot, with the completion-queue head doorbell written only after consumption
- Microsoft’s CQ head doorbell documentation emphasizes that head advancement communicates processed completion entries and frees them for controller reuse

Conservative takeaway:
- completion visibility and completion notification are not the same
- a visible interrupt without freshness/owner/phase proof is weaker than a visible owner/phase/index transition plus later reclaim

### 3. Reclaim or slot reuse is a better durable proof object than “the callback fired” alone
Useful external signal:
- NVMe queue mechanics strongly separate completion detection from host acknowledgement/reuse through CQ head movement
- ring-buffer documentation in other domains (e.g. amdgpu) similarly treats producer publication and later pointer advancement as separate operations

Conservative takeaway:
- in descriptor/ring cases, the durable proof often lives in the return-of-ownership boundary: CQ head advance, RD_IDX update, used-slot reclaim, or later slot reuse
- KB notes should explicitly tell the analyst not to stop at “completion record observed”

### 4. Ordered publication and barrier semantics are practical RE concerns, not implementation trivia
Useful external signal:
- VirtIO and virtio-ring implementation material surfaced by search-layer repeatedly mention ordering/barrier semantics around making avail/used progress visible
- DPDK virtio barrier discussion reinforces that even when the data model is simple, the publish edge is still about ordering guarantees, not just field presence

Conservative takeaway:
- when replay or rehosting is close-but-wrong, analysts should explicitly test whether bytes, owner/index publication, and peer trust are happening in the right order
- this belongs in workflow guidance, not just in an implementation appendix

### 5. “Completion bytes exist” can still be a stale-read or wrong-boundary trap
Useful external signal:
- SPDK/NVMe material emphasizes reading the next expected completion freshness condition before treating the slot as new
- broader DMA/shared-ring material surfaced in search results reinforced stale-read and coherency failure modes

Conservative takeaway:
- presence of bytes in backing memory is not sufficient proof that the consumer may trust them
- the workflow should force analysts to mark freshness/visibility boundaries explicitly

## KB changes driven by this run
Materially extended:
- `topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md`

What was sharpened in the canonical note:
- stronger distinction between descriptor/record contents and publish visibility
- stronger distinction between completion visibility and interrupt visibility
- explicit reclaim/slot-reuse stop rule
- better operator framing around ordered publication, freshness markers, and return-of-ownership boundaries
- clearer route from descriptor-visible cases into a smaller practical trust-and-reclaim contract

## Why this addition is practical
This helps with recurring real-world reverse-engineering and rehosting failures such as:
- “I can see the completion entry in RAM, but the software path still ignores it”
- “The queue structure is obvious, but I still cannot tell when the device/driver truly owns the slot”
- “An interrupt fires, but no durable consequence follows”
- “My emulator writes the right bytes, but not in a way the peer will trust”
- “The completion callback exists, but I still lack a durable proof that the queue contract is correct”

## Evidence-quality note
This run intentionally used mixed authoritative/spec-adjacent and implementation/practitioner sources.
That is acceptable here because the KB output is workflow-centered and conservative rather than claiming one universal queue architecture.

The durable cross-source pattern was stable:
- contents and publication are separate
- freshness and interrupt are separate
- completion and reclaim are separate
- return-of-ownership is often the durable proof boundary

## Search audit
Search sources requested: exa,tavily,grok
Search sources succeeded: exa,tavily,grok
Search sources failed: none
Exa endpoint: `http://158.178.236.241:7860`
Tavily endpoint: `http://proxy.zhangxuemin.work:9874/api`
Grok endpoint: `http://proxy.zhangxuemin.work:8000/v1`
