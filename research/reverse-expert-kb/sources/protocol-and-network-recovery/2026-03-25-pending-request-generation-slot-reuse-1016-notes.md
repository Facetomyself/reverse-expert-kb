# Pending-request generation / slot-reuse deepening notes
Date: 2026-03-25 10:16 Asia/Shanghai
Branch: protocol / firmware practical continuation
Status: retained synthesis notes for external-research-driven maintenance

## Why this batch exists
This run revisited the protocol / firmware pending-owner lifecycle seam, not to create another abstract sibling, but to sharpen one thinner continuation with more practical stop rules.

The chosen seam remains valuable because it captures a recurring failure shape:
- the visible identifier still looks right
- the arrival path still looks right
- but the runtime still trusts one narrower owner-lifetime contract than the analyst has frozen

This is exactly the kind of underfed but operator-useful continuation the KB should keep feeding.

## Search posture for this run
Search was attempted via the search-layer skill with explicit requested sources:
- Exa
- Tavily
- Grok

Saved search trace:
- `sources/protocol-and-network-recovery/2026-03-25-pending-request-generation-slot-reuse-search-layer-1016.txt`

Observed source outcome:
- Exa: succeeded
- Tavily: succeeded
- Grok: invoked but returned repeated `502 Bad Gateway`

This run therefore counts as external-research-driven and multi-source-attempted, but with a degraded retained source set.

## Retained practical support

### 1. gRPC async C++ tutorial
URL: https://grpc.io/docs/languages/cpp/async/

Retained points:
- async gRPC work is completion-queue driven
- operations are bound to unique tags
- server examples commonly use one per-call `CallData` object and the object address as the tag
- the useful analyst question is therefore not merely whether an event reached the right queue, but which per-call state object the queue event still names and whether that object is still the live owner

Operator value:
- strong reminder that queue-arrival truth is weaker than current-call-object truth
- useful analogy for async frameworks where a visible tag survives longer than the analyst’s broad mental model of request ownership

### 2. RabbitMQ RPC tutorial
URL: https://www.rabbitmq.com/tutorials/tutorial-six-go

Retained points:
- client creates a callback queue
- requests carry `reply_to` and unique `correlation_id`
- client accepts the reply only when the response-side correlation matches the outstanding request it is waiting for

Operator value:
- callback-path success is only the outer condition
- useful source-backed reminder that one live waiter / pending marker still decides whether a broadly plausible reply is actually consumed

### 3. RabbitMQ Direct Reply-To docs
URL: https://www.rabbitmq.com/docs/direct-reply-to

Retained points:
- even a pseudo-queue path that looks especially direct still preserves per-request matching on the reply side
- message return on the obvious path does not collapse the need for current-request proof

Operator value:
- helpful analogy for cases where analysts overread transport return or callback-path correctness as sufficient proof of current ownership

### 4. NVMe completion / phase discussions
URL: https://forum.osdev.org/viewtopic.php?t=38736

Retained points:
- queue indexes can wrap while remaining superficially stable
- completion handling still depends on phase-owned new-vs-stale distinction rather than naked index equality
- host-side reclaim/head advance reflects what was actually consumed, not merely what looked index-aligned

Operator value:
- strong firmware-shaped reminder that the same visible index can name different ownership generations across wraps
- useful bridge from protocol pending-owner realism into descriptor/ring ownership realism already present elsewhere in the KB

## Practical synthesis carried into the KB
A stronger operator phrasing from this batch is:

```text
same visible slot/tag/correlation still appears plausible
  -> arrival path still looks broadly correct
  -> runtime asks a narrower question: does this still belong to the current live owner?
  -> timeout, cancel, reconnect, wrap, phase change, or object replacement says no
  -> stale-drop / ignore / no-wakeup wins despite the outer match
```

Useful branch-memory reminders to preserve:
- queue arrival is weaker than current-owner proof
- callback-path success is weaker than waiter-liveness proof
- stable slot/index visibility is weaker than phase/owner proof
- replay fixtures that preserve bytes but not lifecycle timing or reuse boundaries are often too weak

## KB maintenance conclusion from this batch
This batch justified strengthening the existing pending-request generation / epoch / slot-reuse continuation and syncing the branch memory into parent routing surfaces.

The practical gain is not another family label.
It is a clearer stop rule for when analysts should stop blaming parser or correlation mismatch and instead freeze one retire/reuse/phase-owned lifetime contract.
