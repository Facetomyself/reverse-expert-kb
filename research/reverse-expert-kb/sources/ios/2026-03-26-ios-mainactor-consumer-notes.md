# iOS Swift async -> MainActor durable-consumer notes

Date: 2026-03-26
Mode: external-research-driven
Scope: iOS practical continuation seam; MainActor/view-model/coordinator-side first durable consumer

## Why this note exists
Recent iOS practical pages already preserved an important distinction between callback truth, continuation creation/storage, actual resume/delivery, and the first resumed consumer. This pass tightened one still-thin but operator-useful continuation:

- some Swift-heavy cases should **not** stop at `resume(...)`, `yield(...)`, or even the first resumed reducer
- the first durable consequence can live one hop later at a `@MainActor`-isolated view-model, coordinator, route selector, or UI-state write
- therefore `resume happened` and `the same behavior-bearing consumer woke` are separate proof objects

## Source-backed takeaways

### 1. Continuation bridge truth is only the handoff, not the durable effect
Donny Wals' continuation walkthrough is useful here because it preserves two practical facts:
- callback-based APIs can be wrapped into `async` APIs with checked continuations
- the continuation must actually be resumed, and exact-once discipline matters

For reverse work, that means:
- callback visibility and continuation resumption are strong handoff proof
- but they are still weaker than the later reducer / coordinator / state owner that changes app behavior

Source:
- https://www.donnywals.com/migrating-callback-based-code-to-swift-concurrency-with-continuations/

### 2. MainActor isolation is a separate runtime truth boundary
Antoine van der Lee's MainActor explanation is useful not for app architecture theory, but for one practical separation:
- `@MainActor` marks actor isolation, usually associated with main-thread UI ownership
- `MainActor.run { ... }` is an explicit hop boundary worth treating as an observable handoff
- non-isolated synchronous contexts and async contexts are not interchangeable; actor expectations can diverge from naive thread assumptions

For reverse work, this supports a more careful chain:
- callback / completion truth
- continuation resume or stream delivery truth
- resumed task-side reducer truth
- explicit `MainActor.run` or `@MainActor` consumer truth
- later visible effect

Source:
- https://www.avanderlee.com/swift/mainactor-dispatch-main-thread/

### 3. Debugging modern Swift async flows should ask “which actor owns the consumer?”
The SwiftyPlace debugging note usefully reframes the practical question from threads to actor isolation:
- in Swift 6-style debugging, the question is less “am I on the main thread?” and more “am I on the actor I expect?”
- `MainActor.assertIsolated()` is a development-time way to prove that a UI-facing consumer really lives on the MainActor side
- queue/runtime context can help distinguish background task execution from MainActor-owned consumption

For reverse work, the useful portable lesson is:
- if result material resumes correctly but the same durable effect does not happen, ask whether the first behavior-bearing consumer is a later MainActor-isolated object rather than the raw resumed task frame

Source:
- https://www.swiftyplace.com/blog/debugging-swift-concurrency

### 4. AsyncSequence / AsyncStream delivery should not be flattened into UI-state consequence
The MainActor + AsyncSequence gist/snippets and AsyncStream materials are imperfect as formal references, but they still reinforce one operator-useful rule:
- stream construction / continuation storage
- first `yield(...)` or iterator delivery
- later `for await` consumption
- MainActor-side state mutation

should be kept distinct when comparing runs.

In practice, a stream can visibly deliver values while the same MainActor-side consumer never commits the same route/state change.

Supporting sources surfaced by search:
- https://gist.github.com/mattmassicotte/e8d5b4f73d2545222decd61ccdc348bd
- https://matteomanferdini.com/swift-asyncstream/
- https://developer.apple.com/la/videos/play/wwdc2021/10194/

## Practical KB consequence
A more useful stop rule for Swift-heavy iOS cases is:

```text
Do not stop at callback truth or continuation resume by default.
If the case is UI/view-model/coordinator shaped, freeze one later MainActor-side
consumer and one later visible effect before claiming you proved the consequence.
```

## Operator checklist
When a modern iOS case already has truthful callback/delegate or imported-async proof, preserve these boundaries separately:
1. callback/delegate/completion truth
2. continuation creation/storage or stream construction
3. actual resume / yield / iterator-delivery truth
4. first resumed task-side reducer truth
5. actor-hop / `MainActor.run` / executor-handoff truth when relevant
6. first `@MainActor`-isolated view-model / coordinator / UI-state consumer truth
7. one later effect that proves that consumer mattered

## Search audit inputs
Requested source set: exa,tavily,grok
Observed outcome:
- Exa: returned usable results
- Tavily: returned usable results
- Grok: invoked but failed with HTTP 502 Bad Gateway

Endpoints in this run:
- Exa: http://158.178.236.241:7860
- Tavily: http://proxy.zhangxuemin.work:9874/api
- Grok: http://proxy.zhangxuemin.work:8000/v1
