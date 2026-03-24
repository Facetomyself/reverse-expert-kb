# iOS Swift-concurrency continuation / MainActor continuation notes

Date: 2026-03-25
Branch: iOS practical workflow
Purpose: preserve source-backed practical reminders for modern Swift-heavy iOS cases where callback truth already exists, but the first behavior-bearing consumer may sit one hop later in resumed task logic or a MainActor-isolated state owner.

## Sources retained
- Donny Wals — Migrating callback based code to Swift Concurrency with continuations
  - https://www.donnywals.com/migrating-callback-based-code-to-swift-concurrency-with-continuations/
- SwiftLee — MainActor usage in Swift explained to dispatch to the main thread
  - https://www.avanderlee.com/swift/mainactor-dispatch-main-thread/
- Hacking with Swift — How to use continuations to convert completion handlers into async functions
  - https://www.hackingwithswift.com/quick-start/concurrency/how-to-use-continuations-to-convert-completion-handlers-into-async-functions

## High-signal findings retained conservatively
1. Continuations are a bridge from callback/completion APIs into `async`/`await`, not proof that ownership changed.
   - imported `async` surfaces may still just wrap older completion handlers
   - therefore visible async entry points are handoff candidates, not automatic consequence owners

2. Checked continuations preserve an exact-once proof discipline.
   - resume exactly once
   - zero resumes leak/suspend the task
   - double resume is a misuse/crash shape
   - practical RE implication: compare pairs should separate “same callback family fired” from “same continuation actually resumed exactly once”

3. Resume truth is narrower than consumer truth.
   - the callback-based API is invoked immediately when building the bridge
   - later task progress after `resume(...)` is still scheduler/executor-mediated
   - practical RE implication: do not collapse continuation creation, resume event, and first resumed task-side reducer/consumer into one bucket

4. MainActor/UI-state truth can be one hop later than resume truth.
   - a MainActor-isolated property/method/class is the right practical consequence boundary when the meaningful state change is UI/view-model/coordinator owned
   - `MainActor.run { ... }` and `@MainActor` are useful proof surfaces, but they are not identical to generic callback or resume visibility

5. `@MainActor` is not a magical “main thread proof” stamp in every synchronous context.
   - SwiftLee’s practical warning is that synchronous methods in non-isolated contexts do not automatically guarantee the expected main-thread behavior simply because the annotation exists
   - practical RE implication: do not overclaim a state consumer solely from seeing an annotation; prefer one actual state write / route selection / coordinator handoff plus one later effect

## Practical workflow reminder for the KB
Preserve five distinct objects when the case is Swift-heavy:
1. callback/delegate family
2. continuation creation/storage or imported async wrapper
3. exact resume/delivery boundary
4. first resumed task-side reducer / mapper
5. first MainActor-isolated state consumer or later coordinator/UI effect, when that is where behavior actually changes

## Why this matters for branch balance
This is a thinner iOS practical refinement, not another browser/mobile-webview expansion.
It improves a weaker-but-valuable iOS seam with concrete operator stop rules:
- do not stop at “async function found”
- do not stop at “resume happened”
- do not stop at `@MainActor` annotation alone
- stop at the first resumed reducer or MainActor-side state consumer that predicts one later effect
