# Pending-request generation / slot-reuse deepening notes
Date: 2026-03-25
Branch: protocol / firmware practical continuation
Status: retained synthesis notes for external-research-driven maintenance

## Why this batch exists
The protocol branch already had:
- broad replay-precondition work
- pending-request correlation / async-reply ownership
- a thinner generation / epoch / slot-reuse continuation page

What still looked worth deepening was the practical cross-family memory around one recurring failure shape:
- the visible identifier still looks right
- the arrival path still looks right
- but the target trusts one narrower owner-lifetime contract than the analyst has yet frozen

This batch was chosen specifically to avoid another KB-internal wording/index-only run and to feed an under-emphasized practical seam with real external search pressure.

## Search posture for this run
Search was attempted via the search-layer skill with explicit requested sources:
- Exa
- Tavily
- Grok

Result quality this run:
- Exa: succeeded
- Tavily: succeeded
- Grok: invoked but returned repeated `502 Bad Gateway` errors

This means the run is still external-research-driven and multi-source-attempted, but the retained source set is degraded relative to the requested three-source ideal.

Saved search trace:
- `sources/protocol-and-network-recovery/2026-03-25-pending-request-generation-slot-reuse-search-layer.txt`

## Retained practical support

### 1. gRPC async C++ tutorial
URL: https://grpc.io/docs/languages/cpp/async/

Retained points:
- completion-queue work is keyed by tags supplied by the implementation
- the tutorial’s server-side `CallData` object uses the object address as the unique tag for the request lifecycle
- the useful unit is therefore not merely queue arrival, but which per-call state object the queue event names and whether that object is still the one the runtime treats as live

Operator value:
- strong reminder that broad “event arrived on the right completion queue” claims are weaker than proving current call-object ownership and liveness
- useful analogy for any async framework where the visible tag can survive longer than the analyst’s mental model of the request owner

### 2. RabbitMQ RPC tutorial
URL: https://www.rabbitmq.com/tutorials/tutorial-six-go

Retained points:
- the client uses a callback queue and a unique `CorrelationId`
- replies on the callback path are only accepted when the correlation matches the still-awaited request
- the tutorial explicitly frames the client as waiting on the reply path for the right outstanding request, not simply any message on the queue

Operator value:
- strong minimal reminder that correct reply-path arrival is only the outer condition
- useful for preserving the split between callback-path truth and pending-waiter truth

### 3. RabbitMQ Direct Reply-To docs
URL: https://www.rabbitmq.com/docs/direct-reply-to

Retained points:
- the reply can be routed over a pseudo-queue path that looks especially “direct” or “obviously correct”
- the requester still pairs request publication material with response-side correlation properties

Operator value:
- helpful reminder that even the most streamlined reply path does not collapse the need for per-request ownership matching
- useful source-backed analogy for cases where analysts overread correct transport return as sufficient proof of current ownership

### 4. NVMe queue / completion explanations
URLs consulted:
- https://forum.osdev.org/viewtopic.php?t=38736
- http://datongfirmware.blogspot.com/2021/11/nvm-express-nvme-overview.html

Retained points:
- queue indexes can wrap while remaining superficially stable
- completion consumption is bounded by phase/ownership style logic rather than the naked index alone
- practical operator discussion explicitly treats wrap and stale-vs-new entry distinction as normal queue semantics rather than an exotic corner case

Operator value:
- good firmware-shaped reminder that the same visible slot index can name different ownership generations across wraps
- useful bridge between protocol pending-owner realism and descriptor/ring ownership realism already present elsewhere in the KB

## Practical synthesis carried into the KB
A stronger operator phrasing from this batch is:

```text
same visible slot/tag/correlation still appears plausible
  -> arrival path still looks broadly correct
  -> runtime asks a narrower question: does this still belong to the current live owner?
  -> timeout, cancel, reconnect, wrap, phase change, or object replacement says no
  -> stale-drop / ignore / no-wakeup wins despite the outer match
```

Useful cross-family reminders to preserve:
- queue correctness is weaker than waiter-liveness proof
- slot equality is weaker than phase/owner proof
- tag familiarity is weaker than current object-liveness proof
- replay fixtures that preserve bytes but not lifecycle timing or reuse boundaries are often too weak

## KB maintenance conclusion from this batch
This batch justified improving the existing thinner protocol note rather than creating another new leaf.

The practical gain was to keep this branch grounded in operator reminders that are:
- case-driven
- cross-family but conservative
- directly useful for breakpoint placement and compare-pair design
- less likely to drift back into abstract “freshness” or generic replay wording
