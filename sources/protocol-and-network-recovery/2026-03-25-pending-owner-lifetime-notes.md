# Pending-owner lifetime deepening notes
Date: 2026-03-25 23:16 Asia/Shanghai / 2026-03-25 15:16 UTC
Branch: protocol / firmware practical continuation
Status: retained synthesis notes for external-research-driven maintenance

## Why this batch exists
This batch intentionally continued the protocol / firmware pending-owner lifecycle seam instead of doing another internal wording-only sync pass.

The practical question remained narrow and operator-shaped:
- a reply/completion can still arrive on the expected broad path
- a visible slot/tag/correlation can still look right
- but the runtime may still reject it because the current live waiter/owner contract has already changed

The point of this batch was not to invent a new family label.
It was to preserve a stronger practical stop rule for the existing generation/epoch/slot-reuse continuation.

## Search posture for this run
Search was attempted via the search-layer skill with explicit requested sources:
- Exa
- Tavily
- Grok

Saved search trace:
- `sources/protocol-and-network-recovery/2026-03-25-pending-owner-lifetime-search-layer.txt`

Observed source outcome:
- Exa: succeeded
- Tavily: succeeded
- Grok: invoked but returned repeated `502 Bad Gateway`

This run therefore counts as external-research-driven and multi-source-attempted, but with a degraded retained source set.

## Retained practical support

### 1. gRPC async C++ tutorial and completion-queue overview
URLs:
- https://grpc.io/docs/languages/cpp/async/
- https://grpc.github.io/grpc/core/md_doc_core_grpc-cq.html

Retained points:
- completion-queue delivery is tag-driven, not proof by itself that the currently trusted per-call owner is still live
- a per-call object or tag can remain the analyst-visible identity while the more important fact is whether that object is still the one the runtime treats as current
- queue arrival truth is therefore weaker than per-request liveness truth

Operator value:
- strong reminder not to stop at “the completion arrived on the right queue”
- useful analogy for any async runtime where broad event delivery and current owner-liveness are adjacent but different proof objects

### 2. RabbitMQ direct reply-to and Spring request/reply material
URLs:
- https://www.rabbitmq.com/docs/3.13/direct-reply-to
- https://docs.spring.io/spring-amqp/reference/amqp/request-reply.html

Retained points:
- direct reply-path correctness does not collapse the need for current waiter/correlation truth
- Spring request/reply documentation is explicit that late replies and replies without usable correlation should be handled as distinct reply-side failures
- reply-path success is therefore weaker than proving that the current trusted waiter map / future / pending marker still owns the reply

Operator value:
- strong practical reminder that callback-path success, queue success, or pseudo-queue success can still be only the outer shell of a stricter owner-lifetime contract
- useful bridge from generic async-reply reasoning into one concrete stale-drop or reply-error branch

### 3. NVMe-style completion discussions
URL consulted:
- search-layer and partial fetch evidence around NVMe completion-queue / phase-tag behavior

Retained points:
- stable index visibility can survive wrap while ownership still changes
- the useful reduction is phase/owner truth, not naked index equality
- partial source access here is good enough for conservative queue-ownership analogy, not for stronger target-specific claims

Operator value:
- keeps ring/queue ownership realism tied to the same pending-owner family without overclaiming protocol identity

## Practical synthesis carried into the KB
A stronger operator phrasing from this batch is:

```text
same broad path succeeds
  -> same visible slot/tag/correlation still looks plausible
  -> runtime asks whether the currently trusted waiter/owner is still the same live one
  -> timeout, cancel, object replacement, reconnect, wrap, or reuse says no
  -> stale-drop / late-reply / no-wakeup wins even though the outer path still looked right
```

Useful reminders preserved from this batch:
- queue arrival is weaker than current-owner proof
- callback-path success is weaker than waiter-liveness proof
- stable slot/index visibility is weaker than phase/owner proof
- replay fixtures that preserve bytes but not lifetime boundaries are often too weak

## KB maintenance conclusion from this batch
This batch justified refining the existing pending-request generation / epoch / slot-reuse note and keeping parent/index branch memory synchronized.

The practical gain is a clearer stop rule:
- do not stop at broad path correctness
- prove current owner-liveness against one retire/reuse/phase boundary
- then decide whether the target is rejecting bad syntax, or correctly discarding stale ownership
