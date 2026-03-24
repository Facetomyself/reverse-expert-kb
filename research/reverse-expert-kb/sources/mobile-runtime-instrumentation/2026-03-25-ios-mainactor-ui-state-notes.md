# iOS MainActor / UI-State Consumer Notes

Date: 2026-03-25 01:19 Asia/Shanghai / 2026-03-24 17:19 UTC
Branch: iOS practical subtree
Focus: Swift-concurrency continuation cases where callback/delegate truth is already good enough, but the first behavior-bearing consumer actually sits at a MainActor/UI-state boundary rather than at callback landing or raw continuation resume.

## Search basis
Raw multi-source search artifact:
- `sources/mobile-runtime-instrumentation/2026-03-25-ios-mainactor-ui-state-search-layer.txt`

Explicit sources requested during search:
- Exa
- Tavily
- Grok

Readable sources retained conservatively:
- Swift Forums — `Effect of @MainActor inference on Obj-C completion callbacks`
- Swift Forums — `How to correctly update the UI from an asynchronous context`
- Augmented Code — `Wrapping delegates for @MainActor consumers in Swift`
- SwiftLee — `MainActor usage in Swift explained to dispatch to the main thread`

## Practical findings worth preserving

### 1. Callback/delegate delivery and MainActor-owned consumption are adjacent but not identical proof objects
A delegate or completion callback can be truthful enough to freeze while the first behavior-changing consumer still lives later at a MainActor-isolated state update, coordinator, or view-model boundary.

Practical implication for reversing:
- do not stop at "the callback fired"
- do not stop at "the continuation resumed"
- ask whether the result still crosses one actor-isolation or UI-state handoff before it becomes behavior-bearing

### 2. Delegate-to-MainActor wrappers are a real bridging shape, not a theoretical edge case
The retained delegate-wrapper example is useful because it preserves a common pattern:
- background-thread delegate callback
- wrapper object creates async context
- `@MainActor` closure or handler performs the stateful/UI-bound consequence

For RE workflow purposes, this means the first useful consumer may be:
- not the delegate method itself
- not the wrapper alone
- but the first MainActor-bound handler that mutates durable state or selects the next route

### 3. MainActor isolation is often the real boundary for UI-bound or view-model-bound state
The retained MainActor guidance supports a modest but useful claim:
- state that directly drives view redraws or user-visible route changes is commonly isolated to MainActor
- this makes MainActor-bound methods, closures, and state writes good candidate consumers when callback/continuation truth already exists

For RE workflow purposes, a good practical question is:
- where does resumed result material first become one MainActor-owned state mutation, route change, scheduler choice, or controller/view-model decision?

### 4. Imported async surfaces and completion callbacks can share ownership while still differing at the first MainActor consumer
The retained forum material reinforces that Obj-C completion-based APIs and Swift async-facing surfaces can be closely related rather than genuinely separate ownership families.

For RE workflow purposes:
- do not reopen broad owner search merely because both callback and `async` faces are visible
- instead, preserve the possibility that the true practical split is later:
  - callback/delegate truth
  - continuation/task wakeup truth
  - first MainActor-owned consumer truth

### 5. MainActor labels are only useful when tied to one later effect
This run should avoid turning MainActor into empty taxonomy.
The useful operator object is not "MainActor exists here" by itself.
It is one smaller proof chain such as:

```text
callback/delegate already frozen
  -> continuation resume or task wakeup
  -> MainActor-isolated reducer / state write / route selection
  -> one later visible effect
```

Examples of later effects worth preferring:
- challenge screen becomes reachable
- retry/backoff scheduling changes
- allow/degrade/block state flips
- next request family or route selection changes
- visible UI/model state changes in a reproducible compare pair

## Conservative synthesis to carry into the KB
This source set supports a practical workflow refinement, not a runtime-internals page.
The safe retained claim is:
- in modern iOS/Swift cases, callback truth and continuation truth may still be earlier than the first behavior-bearing MainActor/UI-state consumer
- therefore the iOS continuation note should preserve one narrower stop rule around MainActor/view-model/UI-state handoff instead of treating post-resume logic as a single undifferentiated bucket

## What not to overclaim
- Do not claim fine-grained Swift runtime internals from these sources.
- Do not claim every `@MainActor` annotation implies the decisive consumer.
- Do not equate UI-thread affinity with business-policy meaning automatically.
- Do not rely on synchronous non-isolated call behavior as a stable reversing heuristic beyond the conservative warning that actor annotations alone are not the whole proof object.
