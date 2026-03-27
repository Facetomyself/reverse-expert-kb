# iOS Swift AsyncStream termination / cancellation / consumer-truth notes

Date: 2026-03-27
Mode: external-research-driven
Branch target: iOS practical workflows / Swift-concurrency continuation-owned consequence seam
Purpose: preserve a narrower operator rule for `AsyncStream` / `AsyncThrowingStream` cases where visible `yield(...)` traffic, cancellation, and stream termination can be mistaken for the same proof object.

## Why this note exists
The KB already preserved an important stream-shaped reminder:
- `AsyncStream` / `AsyncThrowingStream` construction, buffering policy, first `yield(...)`, termination/cancellation, and first iterator-side or later MainActor-side consumer should stay separate.

This pass tightens that reminder with one more practical distinction:
- **producer-side activity after cancellation or after the consumer you care about disappeared is weaker than durable consumer truth**
- therefore `yield happened`, `finish happened`, `termination callback reported`, and `the same iterator-side or MainActor-side consumer still owned behavior` are separate proof objects

This is useful in real reverse work because Swift-heavy iOS cases often look “alive” at the producer edge even when the behavior-bearing consumer no longer wakes the same way.

## Search artifact
Raw multi-source search artifact:
- `sources/ios/2026-03-27-1016-asyncstream-termination-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Tavily returned usable result surfaces, including Apple documentation snippets and the Swift evolution proposal
- Exa was explicitly invoked but the backend reported `402 Payment Required`; merged output still surfaced some Exa-carried items, so Exa should be treated as attempted but degraded/unhealthy
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway`

## Retained sources
1. Swift evolution proposal SE-0314 — `AsyncStream` / `AsyncThrowingStream`
   - <https://github.com/swiftlang/swift-evolution/blob/main/proposals/0314-async-stream.md>
2. Apple Developer Documentation — `AsyncStream.Continuation`
   - <https://developer.apple.com/documentation/swift/asyncstream/continuation>
3. Apple Developer Documentation — `AsyncStream.Continuation.Termination`
   - <https://developer.apple.com/documentation/swift/asyncstream/continuation/termination>
4. Apple Developer Documentation — `AsyncThrowingStream.Continuation.onTermination`
   - <https://developer.apple.com/documentation/swift/asyncthrowingstream/continuation/ontermination>
5. Conservative practitioner discussion retained only as supporting field signal
   - <https://github.com/pointfreeco/swift-composable-architecture/discussions/1906>

## High-signal retained findings

### 1. Stream finish and cancellation are explicit termination states, not vague “async drift”
The retained Apple documentation snippets and search result surfaces are enough to preserve a narrow practical point:
- `AsyncStream.Continuation.Termination` explicitly models at least `finished` and `cancelled`
- Apple documents `finished` as the stream having ended because `finish()` was called
- the continuation APIs expose `onTermination`, making termination a first-class observable boundary rather than an implied side effect

Practical consequence:
- do not collapse `finish()`-, cancellation-, and later-consumer disappearance into one generic “the stream ended” story
- keep explicit track of whether the run ended because the producer finished, because cancellation occurred, or because the consumer-side behavior you cared about stopped being the same

### 2. `finish()` is required to end ordinary `AsyncStream` iteration cleanly
SE-0314 states that a call to `finish()` is required to end iteration for the consumer of an `AsyncStream`.

Practical consequence:
- repeated `yield(...)` visibility is weaker than proving the same consumer reached its expected terminal or later-effect boundary
- if the producer still emits or appears capable of emitting, that does not prove the same iterator-side or MainActor-side consumer still owns behavior
- in reverse work, this means “I still saw producer traffic” is weaker than “the same consumer finished or advanced to the same durable consequence”

### 3. Buffering policy and enqueue/drop behavior belong to delivery truth, not just API trivia
SE-0314 and Apple result surfaces both preserve that `AsyncStream` construction includes a buffering policy and that yielding has a `YieldResult` describing whether material was enqueued, dropped, or the continuation was already terminated.

Practical consequence:
- stream delivery is not a single proof object
- preserve at least these separations when they matter to a compare pair:
  - producer-side `yield(...)` attempt
  - enqueue vs drop vs already-terminated result
  - iterator-side wake/consumption
  - later MainActor-side consumer or coordinator effect
- this is especially important when a run seems to have “the same stream traffic” but not the same later behavior

### 4. `onTermination` is a cleanup/lifetime boundary, not automatic durable-consumer proof
Apple’s API surface explicitly exposes `onTermination`, and SE-0314’s examples use termination handlers for cleanup such as stopping monitoring.

Practical consequence:
- `onTermination` should be treated as a lifecycle boundary for the stream producer/bridge
- it is stronger than mere producer silence, but weaker than proving that the same iterator-side or MainActor-side consumer reached the same consequence
- a visible termination callback often tells you that the bridge lifetime changed; it does not by itself prove the same policy-bearing consumer ran or the same route/state changed

### 5. Field reports reinforce that producer work can outlive the consumer you care about
The retained practitioner discussion is not a normative source, but it is still useful as conservative field signal:
- `AsyncStream` producers may run inside nested/detached task structures
- cancellation handling may be easy to misread
- a producer loop can appear alive or continue briefly while the expected consumer-side behavior is already gone or different

Practical consequence:
- in reverse work, treat post-cancellation or late producer traffic as weaker than proof that the same iterator-side consumer, task-side reducer, or MainActor-side state owner still woke and committed the same behavior

## Practical synthesis worth preserving canonically
A compact stop rule for stream-shaped iOS cases is:

```text
yielded != enqueued != consumed != terminated != durable-effect
```

Where:
1. **yielded**
   - producer attempted `yield(...)`
   - weakest producer-side signal

2. **enqueued**
   - stream buffering policy and continuation state allowed the element to be accepted rather than dropped/terminated
   - stronger than raw producer intent, still weaker than consumer truth

3. **consumed**
   - iterator-side or resumed task-side consumer actually received and used the element
   - this is often the first behaviorally relevant stream-side proof object

4. **terminated**
   - `finish()` or cancellation produced explicit stream-lifetime end-state
   - lifecycle truth, not automatic durable-effect truth

5. **durable-effect**
   - MainActor-side view-model/coordinator/UI-state consumer or later policy-bearing reducer changed later behavior
   - this is the workflow stop boundary that matters most

## Best KB use of this material
This material is best used to sharpen the existing iOS Swift-concurrency workflow note and subtree guide, not to create a broad standalone Swift-concurrency taxonomy page.

The practical operator value is:
- do not overclaim from visible `yield(...)`
- do not overclaim from `finish()` alone
- do not overclaim from `onTermination` alone
- do not overclaim from producer activity after cancellation
- freeze the smallest truth object that actually predicts later behavior

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source run.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and the failing sources were recorded clearly.
