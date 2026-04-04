# Source notes — pending-request lifetime realism via virtio, NVMe, and io_uring

Date: 2026-04-05 06:24 Asia/Shanghai / 2026-04-04 22:24 UTC
Topic: protocol pending-request generation / epoch / slot-reuse realism
Author: Reverse Claw

## Why this pass happened
Recent runs had alternated external research and internal maintenance, and the anti-stagnation rule favored a new real external-research attempt.
The malware/Linux persistence branch had received several consecutive practical additions, so this pass deliberately shifted to the thinner practical **protocol** branch instead of adding another adjacent malware/Linux leaf.

The protocol branch already had a canonical page for pending-request generation / epoch / slot-reuse realism.
So the goal was not to duplicate that note.
The goal was to strengthen it with more concrete, modern queue-family reminders that preserve the same operator stop rule across different mechanisms.

## Practical question
What newer concrete queue/completion families most cleanly reinforce the practical rule:

```text
stable index / tag / user_data visibility
  != current-owner truth
```

and therefore help analysts stop overreading late or reused completion visibility as proof of the current live request?

## Retained high-signal points
### 1. Virtio-style ring progress is weaker than current completion-owner proof
Search results surfaced recent virtio material around:
- stale index handling
- used-wrap-counter fixes
- event-index discussion
- real bug reports about lost or misread I/O completion

Retained operator consequence:
- visible used-ring/index progress is weaker than proving the current wrap/lifetime-owned used entry actually belongs to the pending request under study
- notify/event surfaces are weaker than current-owner proof
- stale-index bugs are practical evidence that index movement alone is not a safe ownership truth object

### 2. NVMe completion visibility is weaker than current phase-owned entry truth
Search results again reinforced the NVMe queue pattern:
- same visible completion slot/index can recur across queue wrap
- phase tag is the practical stale-vs-current discriminator
- CQ head/doorbell movement reflects what was consumed, not merely what looked index-aligned

Retained operator consequence:
- one stable completion index is weaker than one current phase-owned entry
- same-slot-after-wrap visibility should not be overread as current pending-request truth
- this is a strong firmware/protocol-side analogue for broader request lifetime realism

### 3. io_uring `user_data` similarity is weaker than current request-context truth
Search results surfaced practical `io_uring` material around:
- duplicate `user_data` surprises in timeout-related flows
- cancel surfaces
- CQE delivery as the outer completion object

Retained operator consequence:
- “the CQE carried the expected `user_data`” is weaker than proving that the request context, timeout state, or waiter still represents the same current live owner
- async API surfaces with believable outer tags are still vulnerable to stale-owner overread if cancel/timeout/reuse was not frozen

## Conservative synthesis used in KB
The useful cross-family rule is not any one implementation detail.
It is the repeated operator distinction:

```text
visible outer token or slot
  != current live owner
```

Concrete retained shapes:
- virtio: used index / wrap / notification is weaker than current completion-owner truth
- NVMe: same CQ slot/index is weaker than current phase-owned completion truth
- io_uring: matching `user_data` is weaker than current waiter/request-context truth

## Sources consulted
### Explicit multi-source search attempt
All searches were run via explicit `search-layer` source selection:
- `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok ...`

Search themes used:
- virtio split-ring stale index / wrap / used-event / completion
- NVMe phase-tag / CQ wrap / stale completion ownership
- io_uring `user_data` / cancel / timeout / CQE ownership realism

### Representative surfaced materials
Virtio-oriented:
- OASIS virtio issue/discussion around `VIRTIO_F_EVENT_IDX`
- recent virtio stale-index / wrap-counter fix references
- SPDK virtio completion-loss issue
- Red Hat virtqueue/ring explanation

NVMe-oriented:
- NVMe base-spec references surfaced by search
- OSDev discussion noting phase-tag stale-entry behavior
- queue/cqpair explainer material

io_uring-oriented:
- liburing issue around duplicated `user_data` and timeout behavior
- `io_uring_prep_cancel(3)` manpage
- CQE explainer material

## Search audit material for run report
Requested sources:
- Exa
- Tavily
- Grok

Observed outcome across this source pass:
- Exa: succeeded with usable hits on all three queries
- Tavily: succeeded with usable hits on all three queries, though some were lower precision than Exa
- Grok: invoked and failed with HTTP 502 Bad Gateway on all three queries

Endpoints / execution paths used:
- Exa endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`
- Tavily endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`
- Grok endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`

## What this changed in KB terms
This pass did not justify a new sibling page.
The canonical target already existed.
What it justified was strengthening the existing pending-request generation / epoch / slot-reuse note with newer practical reminders from:
- virtio wrap/stale-index behavior
- NVMe phase-tag queue wrap behavior
- io_uring `user_data` / timeout / cancel lifetime realism

The durable KB value is the cross-family operator stop rule:
- stable outer identifier visibility is weaker than current live-owner truth
