# iOS Swift-concurrency MainActor / actor-hop notes

Date: 2026-03-25
Branch: iOS practical workflow
Purpose: preserve source-backed practical reminders for modern Swift-heavy iOS cases where callback truth and continuation resume truth are already good enough, but the first behavior-bearing consumer may still sit behind one actor-hop / executor-handoff boundary before a MainActor-owned state mutation or coordinator effect.

## Sources retained
- Swift Evolution SE-0338 — Clarify the Execution of Non-Actor-Isolated Async Functions
  - https://github.com/apple/swift-evolution/blob/main/proposals/0338-clarify-execution-non-actor-async.md
- Swift Forums — Guarantee of resume function on MainActor
  - https://forums.swift.org/t/guarantee-of-resume-function-on-mainactor/58754
- Swift Forums — How to correctly update the UI from an asynchronous context
  - https://forums.swift.org/t/how-to-correctly-update-the-ui-from-an-asynchronous-context/71155
- SwiftLee — MainActor usage in Swift explained to dispatch to the main thread
  - https://www.avanderlee.com/swift/mainactor-dispatch-main-thread/

## High-signal findings retained conservatively
1. Continuation resume is not the same proof object as MainActor-owned consequence.
   - a callback may resume a continuation correctly
   - yet the first behavior-bearing state mutation may still happen one hop later at a MainActor-isolated view-model, coordinator, or UI-state owner

2. Non-actor-isolated `async` execution should not be flattened into implicit MainActor truth.
   - SE-0338 clarifies that non-actor-isolated async functions do not automatically run on an actor executor
   - practical RE implication: preserve one explicit actor-hop / executor-handoff question when the first consumer appears UI-owned

3. `@MainActor` annotation visibility is weaker than a proved consumer.
   - annotation or type isolation alone is not enough
   - prefer one concrete state mutation, route selection, coordinator handoff, or later effect that shows the MainActor-side consumer actually mattered

4. Resume-thread folklore is weaker than actor/executor truth.
   - practical discourse around resumed execution repeatedly warns that "resume happened" is not identical to "resumed here on main/UI"
   - practical RE implication: separate callback truth, continuation creation/storage, actual resume, first resumed reducer truth, actor-hop truth, and MainActor-side consumer truth

## Practical workflow reminder for the KB
Preserve six distinct objects when the case is Swift-heavy and UI-state shaped:
1. callback/delegate family
2. continuation creation/storage or imported async wrapper
3. exact resume/delivery boundary
4. first resumed task-side reducer / mapper
5. actor-hop / executor-handoff truth when relevant
6. first MainActor-side state consumer or later coordinator/UI effect

## Why this matters for branch balance
This is a thinner iOS practical refinement, not another broad mobile or browser expansion.
It improves a still-practical iOS seam with a more conservative stop rule:
- do not stop at "async function found"
- do not stop at "resume happened"
- do not stop at `@MainActor` annotation alone
- stop at the first resumed reducer or MainActor-side consumer that predicts one later effect, preserving actor-hop truth when it is what actually separates those two boundaries
