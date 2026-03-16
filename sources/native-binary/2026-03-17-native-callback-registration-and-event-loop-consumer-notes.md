# Source Notes — Native callback-registration and event-loop consumer workflow

Date: 2026-03-17
Purpose: practical support note for a native workflow page focused on the recurring desktop/server/native case where callback registration, message dispatch, completion posting, or reactor/event-loop plumbing is already visible, but the analyst still has not proved which callback family or loop-consumer boundary actually owns the first consequence-bearing behavior.

## Scope
This note does not try to survey all asynchronous native reversing.
It consolidates practical signals already present in the KB into one operator-facing frame for the native baseline case where:
- static structure is already reasonably legible
- imports, strings, xrefs, callback tables, vtables, window procedures, dispatch sources, completion handlers, or reactor registrations are visible
- the analyst can tell that asynchronous or event-driven execution matters
- but progress still stalls because the first meaningful callback owner, posted task, event-loop consumer, or completion reducer is still unclear

The recurring bottleneck is not lack of entry visibility.
It is **mistaking registration or dispatch surface visibility for proved behavioral ownership**.

## Supporting source signals

### 1. Native baseline synthesis already implies a callback-heavy practical gap
From:
- `topics/native-binary-reversing-baseline.md`
- `topics/native-interface-to-state-proof-workflow-note.md`
- `topics/runtime-behavior-recovery.md`

High-signal points reused here:
- native work often starts with a useful static map and multiple plausible interface paths
- imports, strings, callbacks, and registrations are often routing aids rather than proof
- runtime validation is especially useful when one narrow asynchronous handoff can collapse uncertainty
- proving one consequence-bearing edge is usually more valuable than broadly scanning more readable code

Why it matters:
- this supports a distinct native workflow note for the async/event-loop middle state where callback or registration visibility exists, but the first consequence-driving consumer is still unproved

### 2. Existing mobile/browser notes already encode a transferable ownership lesson
From:
- `topics/mobile-response-consumer-localization-workflow-note.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`

High-signal points reused here:
- visible payload or registration does not prove meaningful consumption
- the decisive boundary is often later than the most obvious callback surface
- useful progress comes from separating producer, handoff, reducer, and first behavior-changing consumer

Why it matters:
- although these are not native desktop/server pages, the same operator lesson transfers directly to callback-heavy native targets: registration is not ownership, and event visibility is not yet consequence proof

### 3. Runtime-evidence pages already justify narrow async proof moves
From:
- `topics/runtime-behavior-recovery.md`
- `topics/record-replay-and-omniscient-debugging.md`
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`

High-signal points reused here:
- runtime work pays off most when it targets one uncertainty rather than generating maximal traces
- late visible effects can be traced back to one earlier queue insertion, posted completion, wakeup, or callback dispatch boundary
- selective evidence beats broad event logging when the analyst’s question is ownership

Why it matters:
- this supports a callback/event-loop note centered on one narrow proof chain rather than generalized tracing advice

## Distilled practical pattern
A useful native async workflow pattern here is:

```text
registration, dispatch, or callback surface becomes visible
  -> separate registration from actual delivery/selection
  -> choose one candidate callback family or loop consumer
  -> localize the first queue/post/dispatch/ownership edge that predicts later behavior
  -> prove one downstream effect from that edge
  -> only then broaden to sibling handlers or adjacent event families
```

## Candidate callback / event-loop anchor families
Useful anchor families in this native baseline case include:
- callback registration tables or function-pointer families
- window procedures, message maps, event filters, or notifier chains
- queued work items, posted completions, timers, and delayed tasks
- reactor/select/epoll/kqueue/libuv/libevent dispatch reducers
- C++ signal/slot or observer-notification reducers
- async I/O completion callbacks or state-machine continuations

Bad anchors usually look like:
- the first registration site that happens to be easy to read
- a dispatch helper that only forwards events without choosing meaning
- a callback name that sounds important but predicts no downstream effect
- a message/event family label copied from strings without proving which consumer changes behavior

## Operator heuristics to preserve
- Registration visibility is not consequence ownership.
- Prefer the first callback family that predicts one later state write, mode change, queue insertion, or external effect.
- Separate event production, queueing, dispatch selection, callback delivery, and behavior-changing consumption explicitly.
- If many callbacks look similar, choose the family with the clearest later effect instead of the best-looking pseudocode.
- Use one narrow proof move: one queue watch, one posted-task hook, one dispatch breakpoint, one compare run, or one reverse-causality step from a visible late effect.
- Stop after one proved callback/consumer chain; do not catalog the entire event framework first.

## Candidate canonical KB mapping
This note most directly supports:
- `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md`

It also strengthens:
- `topics/native-binary-reversing-baseline.md`
- `topics/native-interface-to-state-proof-workflow-note.md`
- `topics/runtime-behavior-recovery.md`

## Bottom line
The native branch does not mainly need another broad “asynchronous native programming” page right now.
It needs a practical workflow note for the common case where callback or event-loop structure is already visible, but the analyst still must prove which queue/dispatch/consumer boundary actually owns the first consequence-bearing behavior.
