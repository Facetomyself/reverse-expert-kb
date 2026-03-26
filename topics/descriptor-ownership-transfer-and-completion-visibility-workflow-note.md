# Descriptor Ownership-Transfer and Completion-Visibility Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, protocol/firmware continuation, descriptor/ring consequence proof
Maturity: practical
Related pages:
- topics/protocol-firmware-practical-subtree-guide.md
- topics/protocol-reply-emission-and-transport-handoff-workflow-note.md
- topics/mailbox-doorbell-command-completion-workflow-note.md
- topics/descriptor-tail-kick-and-completion-chain-workflow-note.md
- topics/peripheral-mmio-effect-proof-workflow-note.md
- topics/isr-and-deferred-worker-consequence-proof-workflow-note.md
- topics/runtime-behavior-recovery.md

## 1. When to use this note
Use this note when a protocol / firmware / driver case has already advanced far enough that queue, descriptor, or ring structures are real, but the analysis still smears together three different facts:
- descriptor preparation
- ownership transfer / publish visibility
- completion visibility back to software

Typical entry conditions:
- one request, command, packet, or reply family is already isolated
- one local preparation path is visible enough to name a descriptor, slot, buffer, or ring entry
- one tail / producer / owner / valid / doorbell update is already plausible
- one completion entry, used index, status writeback, interrupt, callback, or reclaim path is also plausible
- but the analyst still cannot state exactly **when ownership changed**, **when that change became visible**, and **what later software-side fact proves the earlier publish mattered**

Use it for cases like:
- DMA completion rings where the device writes descriptors or records into shared memory and software later consumes them
- transmit or receive rings where descriptor fill is easy to see, but the meaningful proof is the point of ownership transfer plus the first completion-side reuse or reclaim
- firmware queues where publish is memory-backed and only later signaled with an interrupt or pollable index
- rehosting or emulation work where the model already has queue structure, but still fails because ownership, cache visibility, or ordered publication is wrong
- driver reverse engineering where tail/doorbell notes are already useful, but the missing leverage is the narrower question of when software or hardware may truthfully trust the descriptor contents

Do **not** use this note when the real bottleneck is earlier, such as:
- the command family itself is still unclear
- the first output-side handoff is still unproved in general
- there is no credible descriptor/ring object yet
- the real unknown is a narrower MMIO effect-bearing write rather than shared-memory publication and consumption semantics

In those cases, start with:
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- `topics/mailbox-doorbell-command-completion-workflow-note.md`
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`

## 2. Core claim
A recurring descriptor-driven bottleneck is not finding the ring.
It is proving the smaller **ownership-transfer and completion-visibility contract**.

The useful analyst target is often:
- not the first descriptor struct you can annotate
- not the first tail index you can label
- not the first interrupt you can see
- not the broadest ring taxonomy you can reconstruct

It is the smaller chain that predicts trustworthy behavior:
- one side finishes writing a descriptor or completion record
- one ownership or publish edge makes that record visible to the other side
- ordering / cache / shadow-index / freshness semantics determine when the other side may trust it
- one later completion-side reclaim, head advance, used-index advance, wakeup, or slot reuse proves that the earlier publish was actually consumed

That chain is often more valuable than a broader catalog of queue fields.

## 3. Target pattern
The recurring target pattern is:

```text
request / command family visible
  -> descriptor or completion record is prepared in shared memory
  -> one owner / valid / WR_IDX / RD_IDX / tail / doorbell edge publishes that fact
  -> the opposite side consumes only after the publication becomes visible in the right order
  -> one reclaim / callback / used-entry / wakeup / slot reuse proves durable consequence
```

The key discipline is:
- separate **record contents** from **record visibility**
- separate **publish visibility** from **interrupt visibility**
- separate **completion visibility** from **durable software consequence**
- preserve exactly which side owns the slot before and after the boundary

## 4. What counts as ownership-transfer proof
Treat these as high-value proof surfaces:
- owner, valid, or phase/freshness transitions that clearly switch the slot from local-prepared to peer-consumable
- producer / tail / WR_IDX / used-index publication that changes which range is considered valid
- shadow index or freshness-marker updates in memory that software reads before trusting completion records
- MMIO RD_IDX, CQ head, or similar reclaim write that explicitly returns ownership to hardware or peer logic
- compare-run evidence where identical descriptor fill exists in both runs, but only one run performs the publish edge that later leads to completion or reclaim

Treat these as useful but often too early:
- descriptor field fill alone
- naming head/tail fields without showing which one is the visibility point
- seeing a completion record in memory without proving when software is allowed to trust it
- broad interrupt observation without slot-identity continuity

## 5. What counts as completion-visibility proof
Treat these as high-value proof surfaces:
- completion record becomes trustworthy only after the matching WR_IDX / owner / valid / phase publication
- software invalidates or otherwise synchronizes cache state before reading fresh completion content on non-coherent systems
- freshness is checked through the next expected slot, owner bit, or phase/tag rule before the record is treated as new
- used-index, reclaim path, CQ head advance, or slot reuse occurs only after the completion record is visible and consumed
- callback / waiter / worker carries the same request ID, descriptor ID, slot index, or queue position through the handoff
- software writes the reclaim index or release marker only after consuming the completion record

Treat these as useful but weaker:
- generic ISR entry
- polling loops with no record-to-reclaim continuity
- broad queue-drain logs with no slot identity or ownership explanation

## 6. Practical workflow

### Step 1: Freeze one compare pair around ownership change
Prefer pairs like:
- same descriptor contents written in both runs, but only one run flips owner/valid or advances WR_IDX
- same publish edge reached in both runs, but only one run sees completion after the necessary cache/order boundary
- same completion record format visible in memory, but only one run reclaims the slot or wakes the waiter
- same ring structure visible in both runs, but only one side returns ownership through RD_IDX / reclaim logic

If you cannot freeze one pair where ownership or visibility differs, you are still too early for this note.

### Step 2: Mark six boundaries explicitly
Before widening queue taxonomy, write down these six boundaries:

1. **record-preparation boundary**
   - where the descriptor or completion entry contents become materially complete
2. **publish boundary**
   - where one owner / valid / tail / WR_IDX / doorbell edge makes the record eligible for peer consumption
3. **visibility boundary**
   - where the consuming side can truthfully observe that publication
4. **consume boundary**
   - where the peer actually parses, reclaims, or otherwise acts on the record
5. **return-ownership boundary**
   - where ownership is handed back through RD_IDX, reclaim, free, or slot-reuse logic
6. **durable-consequence boundary**
   - where callback, wakeup, reply completion, or later state proves the whole chain mattered

This prevents “we saw the ring entry” from being mistaken for “we proved the contract.”

### Step 3: Preserve side-of-ownership labels aggressively
For each representative slot or record, label which side owns it at each phase:
- `producer-owned`
- `consumer-owned`
- `prepared-not-published`
- `published-not-consumed`
- `consumed-not-reclaimed`
- `reclaimed`

This matters because many debugging mistakes come from treating one descriptor as simultaneously trustworthy to both sides.

### Step 4: Prefer visibility semantics over full descriptor layout
When there are many fields, prioritize:
- the first field or index that changes trust semantics
- the first ordering rule that explains why the index must not move before the contents are complete
- the first cache / invalidate / barrier rule that explains stale reads
- the first reclaim step that returns ownership

A perfect field map is usually less valuable than knowing the exact publication and reclaim boundaries.

### Step 5: Tie completion to one reclaim or reuse fact
Do not stop at “completion exists.”

Prove completion visibility with one downstream effect such as:
- only after the new WR_IDX becomes visible does software read the matching completion entry
- only after that read does software advance RD_IDX or free the slot
- only after consumption does a waiter wake or a callback copy out the result
- only after reclaim does hardware or peer logic reuse the slot later
- one compare run has the same apparent completion bytes in memory but no durable consequence because the visibility / cache / ownership step never really occurred

### Step 6: Hand the result into one next task only
Once the ownership-transfer contract is good enough, route it into one next task:
- rehosting or emulation model refinement for cache/order/ownership realism
- narrower MMIO proof if the remaining unknown is now the exact doorbell or reclaim register effect
- ISR/deferred consequence proof if completion is visible but the durable state transition still hides later
- representative harness work if the truthful publication/reclaim conditions are now known

Do not immediately widen into full ring-family documentation unless a later experiment truly needs it.

## 7. Cache, shadow-index, and ordering checklist
This topic is especially valuable when analysts keep tripping over "the bytes are there, why doesn't software trust them?"

A practical stop rule worth preserving: once the ring shape is already good enough, do **not** keep widening descriptor anatomy until you have frozen the narrower trust contract.
Freeze, in writing, these five things first:
- which side owns the representative slot before publication
- what exact owner / valid / WR_IDX / tail / phase edge publishes it
- whether that edge is only a notify / publish edge or also the full trust boundary
- what ordering or freshness rule makes that publication trustworthy
- whether non-coherent cache synchronization is required before the consumer may trust the bytes
- what reclaim / reuse / wakeup fact proves durable consequence

Check explicitly for:
- **publish order**
  - completion / descriptor contents written before the publish index, owner bit, or freshness marker moves
- **notify-vs-trust split**
  - tail / avail-idx / WR_IDX / doorbell / notify may only announce availability; do not collapse that into “the peer may already trust descriptor or completion contents” unless ordering, ownership, and freshness semantics actually justify it
- **consume order**
  - consuming side reads the visibility or freshness marker before treating the record contents as valid
- **memory class / trust model**
  - decide whether this slot behaves like coherent shared descriptor memory or like streaming / non-coherent DMA-backed memory where explicit CPU/device ownership transfer still matters
- **CPU->device trust transfer**
  - on streaming or non-coherent transmit-style paths, preserve whether a `dma_sync_*for_device()`-style boundary, write-buffer flush, or equivalent handoff is required before ringing the doorbell or advancing the producer-visible index
- **device->CPU trust transfer**
  - on streaming or non-coherent completion-style paths, preserve whether a `dma_sync_*for_cpu()`-style boundary, invalidate, or equivalent ownership return is required before CPU code may trust the completion bytes
- **cache visibility**
  - non-coherent or streaming paths may require invalidation, `dma_sync_*`-style synchronization, or another explicit trust boundary before completion bytes become CPU-trustworthy
- **shadow-vs-MMIO split**
  - some designs publish progress into host memory first and only later reclaim through MMIO
- **freshness rule**
  - ring wrap, phase/tag toggles, or owner-bit polarity may define whether the next slot is actually new
- **identity continuity**
  - request ID, slot index, descriptor pointer, or sequence tag survives from publish through reclaim

If these are still unmarked, the chain is probably not trustworthy yet.

## 8. Breakpoint / hook placement guidance
Useful anchors include:
- final descriptor field fill
- owner / valid bit write
- tail / WR_IDX / producer publication
- cache invalidate or barrier-adjacent helper
- completion read path
- callback / worker / waiter using the same record or ID
- RD_IDX / reclaim / free / slot-reuse write

If traces are noisy, anchor on:
- first publication edge that differs across the compare pair
- first trustworthy completion-read point rather than every memory access
- first reclaim / slot-reuse action rather than all later worker churn

## 9. Failure patterns this note helps prevent

### 1. Treating descriptor presence as descriptor visibility
A completion record present in RAM is not the same thing as a completion record published and consumable.

### 2. Treating interrupt arrival as publication proof
Interrupts often accompany visibility; they are not the same thing as the ownership-transfer boundary.

### 2.25 Treating notify or doorbell as full trust proof
A tail/doorbell/avail update may only announce candidate work.
It does not automatically prove the device has seen the final descriptor contents, nor that later CPU reads are already trustworthy, unless the case's ordering and ownership rules support that claim.

### 2.5 Treating populated completion bytes as fresh completion proof
A slot can look structurally correct while still being stale under an owner/phase/tag rule.

### 3. Ignoring cache-coherency and stale-read problems
If the system is non-coherent, software may still read stale completion bytes after the device wrote them.

### 4. Losing track of which side owns the slot
Without explicit ownership labels, analysts quickly overclaim that both sides can trust the same record at the same time.

### 5. Over-modeling structure while under-modeling contract
Knowing every descriptor field is less useful than knowing when the entry becomes trustworthy and when it becomes free again.

## 10. Concrete scenario patterns

### Scenario A: Device writes completion, but WR_IDX is the real visibility point
Pattern:

```text
device DMA-writes completion record
  -> software still sees nothing trustworthy
  -> WR_IDX update appears
  -> software consumes and later reclaims
```

Best move:
- anchor on the record-write -> WR_IDX publication ordering, not the record bytes alone.

### Scenario A2: Completion slot looks populated, but phase/owner freshness is still old
Pattern:

```text
completion-shaped bytes are visible in the next slot
  -> consumer still ignores the slot
  -> wrap/phase/owner rule shows the slot is not fresh yet
  -> later freshness transition occurs
  -> only then do consumption and reclaim happen
```

Best move:
- treat freshness semantics as part of the proof object rather than as an afterthought once the bytes "look right."

### Scenario B: Completion bytes exist, but stale cache or unsatisfied ownership transfer hides them
Pattern:

```text
completion bytes present in memory backing store
  -> software path still reads old state or still treats the slot as device-owned
  -> invalidate / synchronization / ownership-transfer step occurs
  -> now completion path and reclaim logic execute
```

Best move:
- preserve cache visibility or explicit CPU-trust handoff as part of the proof object, not as an implementation footnote.

### Scenario C: Publish is solved, reclaim is the real missing proof
Pattern:

```text
owner transfer / publish edge is already known
  -> completion read path is known
  -> durable consequence only becomes trustworthy when RD_IDX or slot reuse occurs
```

Best move:
- preserve the reclaim or slot-return boundary as the completion-side proof of consequence.

## 11. Relationship to nearby pages
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
  - use that when the missing proof is still the first committed outbound handoff in general
- `topics/mailbox-doorbell-command-completion-workflow-note.md`
  - use that when command IDs, slots, and mailbox publication are the better practical anchors than generic shared-ring ownership semantics
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`
  - use that when the core bottleneck is the build -> publish -> complete -> reduce chain broadly; this note is the narrower continuation when ownership-transfer, visibility ordering, or reclaim semantics are the specific missing edge
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
  - use that when the real unknown is still one narrower effect-bearing MMIO write rather than shared-memory visibility semantics
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`
  - continue there when publication and completion visibility are already good enough and the durable consequence now hides later in worker logic

## 12. Minimal operator checklist
Use this note best when you can answer these in writing:
- what is the one request / command / completion family?
- what exact record or slot is the representative object?
- when is it prepared but not yet published?
- what field or index changes ownership or visibility?
- how does the consuming side know it may trust the record?
- what reclaim / free / reuse step proves durable completion?
- what single next task becomes easier once this contract is known?

## 13. Source footprint / evidence quality note
This note is intentionally workflow-first.

It is grounded by:
- `topics/mailbox-doorbell-command-completion-workflow-note.md`
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `sources/protocol-and-network-recovery/2026-03-22-descriptor-ownership-transfer-and-completion-visibility-notes.md`
- `sources/protocol-and-network-recovery/2026-03-24-descriptor-ownership-transfer-and-completion-visibility-notes.md`
- `sources/protocol-and-network-recovery/2026-03-25-descriptor-cache-visibility-ownership-notes.md`
- `sources/firmware-protocol/2026-03-26-descriptor-publish-vs-trust-and-dma-sync-notes.md`

The external evidence used for this run repeatedly emphasized:
- ordered publication of completion entries before publishing progress indices
- ownership transfer via shared ring indices rather than only via interrupts
- cache-coherency and stale-read pitfalls on non-coherent systems
- explicit return-of-ownership through reclaim indices or slot reuse
- the practical split between coherent shared descriptor memory and streaming / non-coherent DMA-backed visibility where explicit CPU/device trust transfer can still be the decisive boundary
- the practical danger of overreading kick / notify / doorbell edges as full trust transfer when publication, trust, and reclaim are still separate boundaries
- the practical value of treating ownership transfer as a trust contract shaped by ordering, freshness, notification scope, and sometimes explicit CPU/device synchronization rather than by descriptor bytes alone

That is enough for a conservative practical continuation note because the point is not to claim one universal ring architecture.
The point is to preserve a recurring analyst move that repeatedly appears once queue structure is already visible.

## 14. Bottom line
When a descriptor-driven case already exposes the ring, the next useful question is often not “what does every field mean?”

It is:
- when does the record become **published**?
- when may the other side **trust** it?
- when is it **consumed and reclaimed**?
- and what later consequence proves that the earlier ownership transfer actually mattered?

That gives one compact operator chain worth preserving:
- prepare
- publish
- observe
- consume
- reclaim
- prove consequence
