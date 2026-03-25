# iOS Swift-concurrency AsyncStream / termination / consumer notes

Date: 2026-03-25
Branch: iOS practical workflow
Purpose: preserve source-backed practical reminders for modern Swift-heavy iOS cases where callback or continuation truth is already good enough, but a stream-shaped path still risks overclaiming consequence from `yield(...)` visibility alone.

## Sources retained
- Swift Evolution SE-0314 — AsyncStream and AsyncThrowingStream
  - https://github.com/swiftlang/swift-evolution/blob/main/proposals/0314-async-stream.md
- Swift Forums — How do you completely cancel an AsyncStream?
  - https://forums.swift.org/t/how-do-you-completely-cancel-an-asyncstream/53733
- Swift Forums — What to expect from `AsyncSequence` cancellation?
  - https://forums.swift.org/t/what-to-expect-from-asyncsequence-cancellation/62541
- SwiftLee — AsyncThrowingStream and AsyncStream explained with code examples
  - https://www.avanderlee.com/swift/asyncthrowingstream-asyncstream/
- Hacking with Swift — How to create and use AsyncStreams to return buffered data
  - https://www.hackingwithswift.com/quick-start/concurrency/how-to-create-and-use-asyncstreams-to-return-buffered-data

## High-signal findings retained conservatively
1. `yield(...)` visibility is weaker than durable consumer truth.
   - a producer can keep yielding values that look live and truthful
   - yet the first iterator-side consumer, task-owned reducer, or MainActor-side state owner may already be gone, cancelled, or no longer the same proof object

2. `finish()` / throwing-finish / termination status are separate proof objects from `yield(...)`.
   - SwiftLee’s practical guidance makes stream lifetime explicit: forgetting `finish()` can keep the stream alive and keep downstream code from ever concluding
   - `onTermination` gives a narrower lifetime signal than generic callback visibility
   - practical RE implication: preserve stream delivery truth and stream conclusion truth separately instead of flattening them into one generic async-consumer story

3. Cancellation can leave producer-side activity looking alive after the meaningful consumer already ended.
   - forum discussion around AsyncStream cancellation shows a recurring failure shape where nested or detached producer work continues even though the outer task/consumer has cancelled
   - practical RE implication: do not overread continued producer-side `yield(...)` attempts or upstream callback traffic as proof that the same consumer still owns behavior

4. Buffering policy affects whether visible stream activity corresponds to the consumer you care about.
   - buffering can drop old values, keep only newer values, or discard zero-buffer values when no consumer is actively waiting
   - practical RE implication: separate stream construction/buffering policy truth from first iterator-side consumption truth before making policy claims

5. `AsyncSequence` cancellation/termination expectations are weaker than a simple “cancel means no more interesting values” folklore.
   - cancellation semantics can still permit edge cases where an element is observed around termination boundaries depending on sequence behavior
   - practical RE implication: one emitted or observed element near cancellation is not automatically the durable policy boundary; prefer the first consumer/effect that remains stable across a compare pair

## Practical workflow reminder for the KB
Preserve seven distinct objects in stream-shaped iOS cases when they matter:
1. callback/delegate or imported-async owner family
2. stream construction / continuation storage
3. buffering policy / delivery posture
4. first `yield(...)` or delivery event
5. `finish()` / thrown-finish / termination / cancellation truth
6. first iterator-side or resumed task-side reducer/consumer that still predicts later behavior
7. first MainActor-side state consumer or later effect when that is where behavior becomes durable

## Why this matters for branch balance
This is a thinner, still-practical iOS continuation rather than another broad mobile or browser expansion.
It sharpens one concrete stop rule:
- do not stop at callback truth alone
- do not stop at `yield(...)` visibility alone
- do not stop at stream-lifetime folklore alone
- stop at the first iterator-side reducer / consumer or later MainActor-side consumer whose effect stays truthful after buffering, termination, and cancellation are accounted for
