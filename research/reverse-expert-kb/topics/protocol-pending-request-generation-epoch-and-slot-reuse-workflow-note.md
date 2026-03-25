# Protocol Pending-Request Generation, Epoch, and Slot-Reuse Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, protocol/service reply consumption, pending-owner lifecycle realism
Maturity: practical
Related pages:
- topics/protocol-firmware-practical-subtree-guide.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md
- topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md
- topics/protocol-reply-emission-and-transport-handoff-workflow-note.md
- topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/analytic-provenance-and-evidence-management.md

## 1. When to use this note
Use this note when a case has already narrowed past broad replay gating and even past broad pending-request ownership, and the remaining failure is now about **owner lifetime realism**.

Typical entry conditions:
- one request family and one response/completion family are already trustworthy enough to name
- one pending-request owner or completion-owner concept is already visible
- correlation fields, tags, `user_data`, slot indexes, descriptor tokens, or callback handles already look mostly right
- yet the target still drops, ignores, or misroutes some seemingly correct late replies or completions
- and the missing edge is likely that the runtime distinguishes **same visible identifier** from **same live request generation**

Use it for cases like:
- reply paths where the same slot index is reused after timeout, cancel, reconnect, or retry
- RPC-like runtimes where a completion tag or per-call state object is logically per-request even if some visible token value repeats
- firmware mailbox / ring / descriptor systems where a slot number is stable but ownership changes across wraps, epochs, or valid-bit generations
- async client runtimes where a late completion lands after the original waiter was retired and a new waiter reused the storage
- request/completion systems where the practical bug is not bad parsing and not missing correlation, but stale completion acceptance versus stale completion discard

Do **not** use this note when:
- the first pending owner is still unknown
- the first owner-match check is still unknown
- the reply/completion path itself is still speculative
- the real issue is still earlier broad replay acceptance or output emission

In those cases start with:
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`

## 2. Core claim
A recurring late replay failure is not merely:
- wrong reply shape
- missing correlation ID
- wrong queue or callback family

It is:
- the analyst has matched the **name** of the owner but not the **lifetime contract** of the owner

In practice, many runtimes do not trust:
- slot number alone
- correlation field alone
- queue position alone
- pointer-sized tag alone

They trust one smaller contract such as:
- slot + generation
- token + epoch
- pointer/tag + object liveness
- descriptor index + wrap/owner phase
- request ID + still-live pending entry

The useful next analyst target is often the first place that distinguishes:
- live owner
- stale owner
- reused slot
- late completion
- wrong generation
- retired request state

## 3. Target pattern
The recurring pattern is:

```text
one pending-owner model already exists
  -> one visible token/slot/tag appears to match
  -> late or replayed completion still no-ops or is discarded
  -> runtime checks whether the owner is still live in the same generation/epoch
  -> only generation-correct completions are consumed or wake the waiting side
```

The key discipline is:
- separate **identity match** from **liveness/generation match**
- separate **same slot** from **same ownership epoch**

## 4. What counts as a high-value generation / epoch gate
Treat these as high-value targets:
- first generation counter, epoch field, wrap bit, phase bit, or valid-owner toggle attached to a pending slot
- first place that retires a pending owner while leaving the outer slot/index reusable
- first compare that distinguishes current outstanding request state from stale late completion state
- first timeout/cancel/reconnect path that increments or invalidates request ownership generation
- first reuse path that allocates the same visible slot/tag storage for a new request
- first stale/late-reply branch that is taken even though a broad correlation field still looks plausible

Treat these as useful but often one layer too early:
- slot number alone
- request ID field alone when lifetime is still ambiguous
- descriptor index alone
- tag visibility alone without object lifetime proof
- pending-table presence alone without proving reuse or retirement

## 5. Practical workflow

### Step 1: Freeze one live-match vs stale-match compare pair
Prefer a narrow pair where the outer identifier stays deceptively similar.

Good pairs include:
- same slot index with one completion that lands before timeout and one after cleanup/reuse
- same correlation field with one request still pending and one request already retired
- same descriptor index across two wraps where only the current phase/owner bit is consumed
- same completion-queue tag storage reused by a new call object after the earlier one is gone
- same `user_data` style value carried across submissions where one completion belongs to an earlier now-invalid request context

Record only:
- the reused visible identifier
- the live-vs-stale timing difference
- the owner-retire or reuse event
- the later consume-vs-drop difference

If you cannot produce a compare pair where the broad identifier looks deceptively similar, you may still be one step too early for this note.

### Step 2: Mark seven boundaries explicitly
1. **pending-owner creation**
   - where one live request state becomes current
2. **generation/epoch carrier**
   - where the runtime stores phase, generation, wrap, owner bit, or liveness token
3. **retire/invalidate boundary**
   - where timeout, cancel, shutdown, completion, or reconnect makes the old owner stale
4. **reuse boundary**
   - where the same visible slot/tag/index/storage becomes available for reuse
5. **arrival boundary**
   - where the reply/completion first becomes visible
6. **live-vs-stale check**
   - where the runtime decides current generation versus stale generation
7. **consume-or-discard consequence**
   - first wakeup, dequeue, reclaim, callback, or stale-drop effect

This prevents “same slot” from being mistaken for “same request”.

### Step 3: Prefer the earliest stable liveness contract over full schema explanation
When many fields are present, prioritize the earliest reduction that predicts stale-drop behavior:
- generation increment
- phase/wrap bit toggle
- pending entry pointer replacement
- callback owner swap
- timeout-driven invalidation bit
- completion record phase match

That is usually more valuable than fully decoding every completion structure first.

Two practical source-backed reminders are worth preserving here.

#### Reminder A: completion-queue delivery is not the same as stable per-request ownership
In async RPC-style runtimes such as gRPC C++, a completion queue can return a tag for an event, but the useful analyst question is still which per-call state that tag represents and whether that state is still the current live owner.

A good operator reduction is:
- first freeze where the tag or per-call object is created
- then freeze where that same object is retired, replaced, or deleted
- only then decide whether a late returned tag proves current completion or stale delivery against dead per-call state

This is why a broad statement like “the completion arrived on the right queue” is too weak once the case has narrowed to owner lifetime realism.

#### Reminder B: shared reply channels still need current-owner proof
Request/reply systems such as QMUX- or RabbitMQ-style flows remind us that broad queue correctness and broad correlation-field correctness are only the outer layer.

Even when:
- the reply reaches the expected callback or receive queue
- the broad correlation field still looks right

The remaining practical question can still be whether the current live requester, pending marker, or waiting object is the same one that the runtime still trusts to consume the reply.

Use those source families conservatively as operator analogies, not as a claim that every target implements the same exact field or callback machinery.

#### Reminder C: ring wraps and stable indexes often hide a phase-owned lifetime contract
Firmware / storage / queue-driven systems such as NVMe-style completion handling are a practical reminder that the same visible slot or completion index can remain legible while ownership silently changes across wrap and phase transitions.

A good operator reduction is:
- freeze one completion that is accepted before wrap or before the phase changes
- compare it with one later completion record at the same visible index after wrap or reuse
- prove where the consumer trusts the current phase/owner state rather than the stable index alone
- only then decide whether a repeated index is current work or stale ring noise

This keeps ring bookkeeping from being dismissed as mere implementation detail when it is actually the request-lifetime contract.

#### Reminder D: direct-reply or callback-queue success is still weaker than waiter-liveness proof
RabbitMQ-style tutorials and direct-reply examples are useful because they show both halves of the trap:
- a reply can arrive on the right callback path
- a matching correlation field can still be only the outer identifier

For operator purposes, the stronger question is whether the waiter map, pending marker, future, or reply consumer that the runtime still trusts is the same current one that was created for the request under study.

That narrower liveness question is often the bridge from broad async-reply reasoning into one concrete stale-drop or matched-only wakeup branch.

#### Reminder E: wrapped completion queues often hide a stale-entry stop rule rather than a parser problem
NVMe-style queue discussions are useful here because they make one operator distinction unusually explicit:
- a visible completion index can stay stable across wrap
- the consumer still stops only when the phase-owned entry is no longer current
- reclaim/doorbell advance then reflects what was actually consumed, not merely what looked index-aligned

For analyst purposes, the practical reduction is:
- do not stop at “same slot index reached again”
- freeze one accepted entry before wrap and one later same-index entry after wrap
- prove where the consumer treats the later same-index record as stale because phase/ownership changed
- then decide whether the target is really suffering parser mismatch, or simply rejecting stale ownership at the queue-lifetime boundary

Use all of these source families conservatively as operator analogies, not as a claim that every target implements the same exact field, callback, queue, or ring machinery.

### Step 4: Prove one retire/reuse path, not only one consume path
Do not stop at the accepted case.

Also prove one of these:
- timeout retires the owner before a late reply arrives
- cancellation invalidates the pending state before a completion lands
- slot reuse allocates a new pending owner into the same visible index
- a phase/wrap bit changes while the index remains stable
- a new call/context object replaces the old one even when broad queue delivery still looks similar

This keeps the workflow practical instead of collapsing back into generic “late replies are ignored somehow”.

### Step 5: Tie the stale/liveness check to one durable consequence
Useful downstream proofs:
- only generation-correct completions resolve the waiter
- stale arrivals enter unknown/late/stale discard logging or cleanup
- only current-phase descriptors are reclaimed or advanced
- only still-live tags/call objects produce callback/future resolution
- the same visible slot/index produces different behavior before and after reuse because one hidden generation boundary changed

### Step 6: Preserve the smallest truthful replay object
Once the lifetime contract is known, preserve one replay object that includes:
- visible request/reply fields
- owner-creation timing
- owner-retire timing
- generation/phase state
- slot/tag reuse assumption

Otherwise later analysts often reproduce the same “looks right but still ignored” failure.

### Step 7: Hand off narrowly
Once the generation/epoch gate is localized, hand the case to one next task only:
- replay fixture repair if the fixture lacks lifecycle realism
- descriptor ownership/visibility modeling if the same issue is really a ring phase/reclaim contract
- reply-emission work if the response was never actually emitted on the accepted path
- provenance packaging if the proof is now technically good enough and mainly needs preservation

## 6. Breakpoint / hook placement guidance
Useful anchors for this stage:
- pending-slot allocation and insertion
- timeout/cancel cleanup paths
- generation/epoch increment sites
- wrap/phase/owner-bit toggles on rings or descriptors
- object replacement paths for per-request call state
- completion arrival and stale-drop branches
- slot reclaim and slot reuse paths
- callback/future resolution sites that only fire for current owners

If traces are noisy, anchor on:
- one retire event
- one reuse event
- one stale-drop branch
- one current-generation consume path

## 7. Failure patterns this note helps prevent

### 1. Treating correlation correctness as sufficient
A completion can carry the expected outer identifier and still be stale.

### 2. Treating slot equality as ownership equality
Stable slot numbers often hide per-use generations or phase bits.

### 3. Treating late replies as parser failures
Some late replies parse perfectly and are still discarded because the owner is already retired.

### 4. Missing reuse because storage looks the same
Reused queue entries, tags, or descriptor slots often look identical at a coarse level.

### 5. Building unrealistic replay fixtures
A fixture that saves only request/reply bytes but not owner lifetime or generation state is often too weak for truthful replay.

## 8. Concrete scenario patterns

### Scenario A: Timeout retires the owner before the late reply arrives
Pattern:

```text
request issues
  -> pending owner exists
  -> timeout path retires owner
  -> late reply still arrives with plausible fields
  -> stale-drop path wins because no live generation remains
```

Best move:
- prove timeout-driven retire/invalidate first, then compare live arrival versus late arrival on the same family.

### Scenario B: Slot index is reused with a new generation
Pattern:

```text
slot N carries request A
  -> request A retires
  -> slot N reused for request B
  -> late completion for A still names slot N
  -> consume path requires current generation, not slot number alone
```

Best move:
- localize the generation/phase carrier and the first current-vs-stale compare.

### Scenario C: Completion tag storage is reused but logical owner changed
Pattern:

```text
async completion arrives on the right broad queue
  -> visible tag path looks familiar
  -> underlying call/request object was already destroyed or replaced
  -> no waiter resolves because the old logical owner is gone
```

Best move:
- follow the smallest per-request state carrier across allocation, completion registration, retirement, and reuse.

### Scenario D: Descriptor phase bit, owner bit, or wrap epoch is the real guard
Pattern:

```text
descriptor index looks correct
  -> ring/completion record is visible
  -> consumer trusts only records with the current phase/owner generation
  -> same index under the wrong phase is stale noise
```

Best move:
- treat phase/owner transitions as the ownership-lifetime contract, not as ring bookkeeping.

## 9. Relationship to nearby pages
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
  - broader replay-gate parent when the case has not yet narrowed to pending-owner lifecycle realism
- `topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md`
  - immediate parent when the real unknown is still the first owner-match check rather than generation/reuse specifics
- `topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md`
  - use that when the same underlying problem is best modeled as ring phase / trust / reclaim semantics
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
  - use that when the fixture itself is still not truthful enough to freeze before doing lifecycle realism work

## 10. Minimal operator checklist
Use this note best when you can answer these in writing:
- what visible identifier is being deceptively reused?
- where is the old owner retired or invalidated?
- where can the same slot/tag/index/storage be reused?
- what field or object encodes current generation, phase, or liveness?
- what downstream effect proves current-generation consume versus stale-generation discard?

If you cannot answer those, the case likely needs the broader pending-request ownership note first.

## 11. Source footprint / evidence quality note
This note is intentionally workflow-first.

Primary retained support:
- `sources/firmware-protocol/2026-03-24-pending-owner-generation-epoch-and-slot-reuse-notes.md`
- `sources/firmware-protocol/2026-03-23-pending-request-timeout-and-late-reply-lifecycle-notes.md`
- `sources/firmware-protocol/2026-03-24-pending-owner-generation-reuse-search-layer.txt`
- `sources/protocol-and-network-recovery/2026-03-25-pending-request-generation-slot-reuse-search-layer.txt`
- `topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md`
- gRPC C++ completion-queue documentation and async tutorial material on per-call tag/state and final completion behavior
- RabbitMQ RPC and direct-reply tutorial/doc material on callback-queue delivery plus correlation-based pending-request completion
- NVMe queue/completion explanations used conservatively as a ring phase/owner analogy rather than as a direct protocol claim

Confidence note:
- strong for the recurring workflow shape
- moderate for exact cross-framework vocabulary because implementations differ
- intentionally conservative about universal field names or universal discard semantics

## 12. Bottom line
When a reply or completion still looks right but is ignored after timeout, cancel, reconnect, ring wrap, or slot reuse, the next useful move is often not more packet labeling and not broader replay theory.

It is to localize the first **generation / epoch / slot-reuse** contract that decides whether the visible identifier still names the current live request at all.
