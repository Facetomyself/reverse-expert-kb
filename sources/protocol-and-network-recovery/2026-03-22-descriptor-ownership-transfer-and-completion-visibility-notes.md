# 2026-03-22 Descriptor Ownership-Transfer and Completion-Visibility Notes

Scope: practical source-backed notes for a protocol / firmware continuation page focused on descriptor/ring ownership transfer, ordered publication, completion visibility, cache coherency pitfalls, and reclaim semantics.

## Search intent
Need a concrete workflow continuation for descriptor/ring cases that are already beyond generic output handoff, mailbox publish, and broad descriptor-tail kick proof, but still stall on the narrower question of:
- when the record becomes owned by the other side
- when the consuming side may trust the record
- how completion visibility differs from interrupt visibility
- how reclaim or slot reuse proves durable consequence

## Search inputs
Executed via local `search-layer` skill with explicit multi-source request:
- sources requested: `exa,tavily,grok`
- query set:
  - `firmware mailbox doorbell ring buffer completion interrupt reverse engineering workflow`
  - `descriptor ring tail doorbell completion chain driver firmware reverse engineering`
  - `dma ring completion interrupt ownership reverse engineering practical workflow`

Raw captured output:
- `sources/protocol-and-network-recovery/2026-03-22-descriptor-doorbell-search-layer.txt`

## Source-bearing takeaways

### 1. Ordered publication matters more than ring presence alone
Useful external signal:
- `https://dev.to/ripan030/how-hardware-and-software-share-a-queue-understanding-dma-rings-pea`
- `https://docs.majerle.eu/projects/lwrb/en/v1.2.0/user-manual/hw-dma-usage.html`

Conservative takeaway:
- queue/ring designs depend on a publication contract, not just shared storage
- the important proof edge is often "record contents become complete" followed by "publish index / owner transition becomes visible"
- this supports treating descriptor/record bytes and visibility marker as separate proof surfaces

### 2. Completion visibility is often index-driven, not interrupt-driven
Useful external signal:
- `https://dev.to/ripan030/how-hardware-and-software-share-a-queue-understanding-dma-rings-pea`
- search-layer also surfaced related MMIO / DMA / interrupt explanations via Grok and Tavily summaries

Conservative takeaway:
- completion records may exist before software is entitled to trust them
- software often uses WR_IDX / similar progress publication as the trustworthy visibility point
- interrupts are useful notification, but not the only or always-primary trust boundary

### 3. Ownership return / reclaim is a distinct boundary worth preserving
Useful external signal:
- `https://dev.to/ripan030/how-hardware-and-software-share-a-queue-understanding-dma-rings-pea`
- `https://docs.majerle.eu/projects/lwrb/en/v1.2.0/user-manual/hw-dma-usage.html`

Conservative takeaway:
- many shared queue designs have a second boundary after consumption where ownership returns through RD_IDX advance, skip/advance, reclaim, or slot reuse
- this supports using reclaim / slot reuse as a durable proof object instead of stopping at "completion callback ran"

### 4. Cache visibility and stale-read risks deserve explicit workflow treatment
Useful external signal:
- `https://dev.to/ripan030/how-hardware-and-software-share-a-queue-understanding-dma-rings-pea`
- broader PCIe/MMIO/DMA material from `https://ctf.re/kernel/pcie/tutorial/dma/mmio/tlp/2024/03/26/pcie-part-2/`

Conservative takeaway:
- non-coherent or weakly modeled environments can show the classic failure mode where bytes are present but software still reads stale state
- for reverse-engineering and rehosting, cache/buffer visibility cannot be treated as an implementation footnote when it explains run divergence

### 5. Practical branch gap in the KB
Internal KB context reviewed:
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- `topics/mailbox-doorbell-command-completion-workflow-note.md`
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`

Observed gap:
- the KB already had broad output handoff, mailbox publish/completion, and descriptor tail-kick notes
- it was still thinner on the specific ownership-transfer / visibility / reclaim seam inside descriptor-driven cases
- especially missing was a continuation note that tells the analyst to label side-of-ownership, publish order, trust boundary, cache visibility, and reclaim boundary explicitly

## Page added from this run
- `topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md`

## Why this addition is practical
The new note is intended to help with cases like:
- "we can see the completion record in memory, but software does not act on it"
- "the tail / WR_IDX move seems right, but the peer still does not trust the descriptor"
- "interrupts happen, but reclaim or slot reuse never does"
- "our model has the bytes right, but not the ordering / cache / ownership semantics"

That is narrower and more case-driven than another top-level wording or family-count sync.

## Evidence-quality note
The external sources used here are mixed practitioner/tutorial material rather than one canonical academic source.
That is acceptable for this continuation note because the intended output is workflow-centered and conservative:
- separate contents from visibility
- separate interrupt from trust boundary
- preserve reclaim as proof
- model cache/order issues when they explain divergence

## Search audit
Requested sources: exa, tavily, grok
Succeeded sources: exa, tavily, grok
Failed sources: none

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`
