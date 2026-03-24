# Pending-owner generation / epoch / slot-reuse notes
Date: 2026-03-24
Branch: protocol / firmware practical continuation
Status: retained synthesis notes for KB workflow shaping

## Why this note exists
Recent protocol/firmware runs already covered:
- broad replay-precondition / state-gate diagnosis
- narrower pending-request correlation / async-reply ownership
- descriptor ownership / completion visibility

What still looked thinner was the practical seam where a reply or completion appears to match the right broad owner, yet is still ignored because the runtime distinguishes:
- current live owner
- stale retired owner
- reused slot with a new generation / epoch / phase

That seam is practical and case-driven because it explains recurring failures where:
- the same slot index appears correct
- the same broad correlation field appears correct
- the same completion queue or callback family is used
- but the target still drops or ignores the reply/completion after timeout, reuse, reconnect, or wrap

## External support consulted this run
Search was attempted via search-layer with explicit sources `exa,tavily,grok`.
Result quality:
- Exa: succeeded
- Tavily: succeeded
- Grok: attempted but failed

Useful support recovered from explicit fetches / returned source list:
- gRPC C++ `CompletionQueue` documentation: tag is arbitrary per-event identity and completion delivery is tied to per-call state
- gRPC C++ best-practices: final completion / callback semantics reinforce that per-call state lifetime matters, not only broad message correctness
- liburing `io_uring_cqe_get_data` documentation: completion identity is carried through `user_data`; useful as a pattern for request->completion identity contracts
- search-layer returns also surfaced practical `io_uring` and gRPC discussions around request context identity, queue-delivered completion semantics, and object lifetime pitfalls

These sources are not being overclaimed as one universal protocol model.
They are useful because they repeatedly reinforce the same operator lesson:
- delivery on the right queue is not enough
- broad ID match is not always enough
- per-request state lifetime and generation realism matter

## Practical synthesis
### 1. Identity match and lifetime match are not the same thing
A useful recurring failure pattern is:
- request A creates pending owner in slot N
- request A times out / cancels / retires
- slot N or equivalent storage is reused by request B
- a late completion for A still points at N or carries a plausible outer token
- runtime rejects it as stale because the live ownership generation has changed

This is narrower than broad pending-request correlation and deserves its own continuation note.

### 2. Good operator language for this seam
Good practical labels:
- pending-owner creation
- generation / epoch / phase carrier
- retire / invalidate boundary
- slot or tag reuse boundary
- late arrival
- current-vs-stale owner check
- consume vs stale-drop consequence

These are more useful than broad statements like:
- “response ignored somehow”
- “maybe parser still wrong”
- “probably freshness”

### 3. Descriptor/ring work and async RPC work rhyme here
This seam usefully bridges two families already present in the KB:
- request/reply / callback / completion-queue style ownership
- descriptor/ring / phase-bit / owner-bit / reclaim style ownership

The shared operator lesson is:
- visible slot/index/tag equality is often not enough
- trust depends on one smaller liveness or generation contract

That makes the note valuable for both protocol-style and firmware-style cases.

### 4. Replay fixtures often fail because they preserve bytes but not lifecycle
A strong practical lesson for the KB:
- preserving request and response bytes alone is often insufficient
- the fixture may also need timeout ordering, current pending-owner state, generation/phase value, or slot/tag reuse assumptions

This is a practical continuation from `protocol-method-contract-to-minimal-replay-fixture` and from the pending-request ownership note.

## Candidate scenario shapes worth preserving
### A. Timeout / late reply
- same reply accepted while owner is live
- same reply ignored after timeout cleanup
- practical target: first owner-retire boundary and stale-drop branch

### B. Slot reuse
- same slot index reused for a later request
- broad index match is deceptive
- practical target: generation/phase change and current-vs-stale check

### C. Per-call object replacement
- queue-delivered completion reaches broad framework path
- original request context/call object already replaced or destroyed
- practical target: per-request state lifetime rather than transport arrival

### D. Ring phase / owner-bit realism
- same descriptor/completion index reappears after wrap
- only matching phase/owner generation is trusted
- practical target: phase transition and reclaim/consume contract

## KB maintenance conclusion from this run
This should be added as a thinner practical continuation page, not merely folded into generic replay gating, because:
- it is narrower than broad replay-precondition work
- it is narrower than broad pending-request correlation work
- it helps explain repeated “looks right but still ignored” failures
- it links protocol async ownership and descriptor/ring ownership in a concrete operator-friendly way
