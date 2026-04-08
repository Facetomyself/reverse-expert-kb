# AsyncStream yield vs consumer notes

Date: 2026-04-08
Branch target: iOS practical workflows / Swift-concurrency continuation seam
Purpose: preserve a source-backed operator refinement for Swift-heavy cases where `AsyncStream` / `AsyncThrowingStream` producer visibility is already good enough, but the first iterator-side or MainActor-side consequence boundary is still weaker than analysts assume.

## Research intent
Strengthen the existing iOS Swift-concurrency workflow note with a sharper stream-shaped separation between:
- `yield(...)` happened
- buffering/enqueue truth
- iterator-side consumption truth
- termination/finish/cancellation truth
- later MainActor/policy durable effect

## Search artifact
Raw multi-source search artifact:
- `sources/ios/2026-04-08-1256-asyncstream-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Exa returned usable Apple/Swift async-stream surfaces
- Tavily returned usable Apple/Swift async-stream surfaces
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` through the configured proxy path

## Retained sources
1. Apple documentation surfaces for `AsyncStream` / `AsyncThrowingStream`
2. Apple documentation for `AsyncStream.Continuation.YieldResult` and related continuation/termination surfaces
3. Conservative Swift async-stream design/evolution surfaces retained only as support for operator framing

## High-signal retained findings

### 1. Producer-side `yield(...)` is weaker than iterator-side consumption
Apple’s async-stream surfaces already separate:
- calling `yield(...)`
- what the stream/continuation reports about the yield attempt
- later iterator-side consumption

Practical consequence:
- seeing producer traffic is weaker than proving the app-side consumer actually used the value
- do not narrate `yield(...)` visibility as equivalent to first behavior-changing async ownership

### 2. Buffering/enqueue truth is its own practical proof object
Async-stream buffering policy and yield-result surfaces make accepted buffering distinct from both raw producer attempt and later iterator consumption.

Practical consequence:
- `yield(...)` and `enqueued` are not the same truth object
- when compare pairs drift, buffering/queue acceptance can be the liar even before later consumer logic matters

### 3. Termination/finish/cancellation is still weaker than later MainActor/policy effect
Apple’s async-stream end-state surfaces make stream termination a distinct event from later state/policy consequence.

Practical consequence:
- do not collapse finish/cancellation into later UI/policy behavior
- keep stream mechanics separate from MainActor-owned or policy-bearing effect

## Practical synthesis worth preserving canonically
A compact stop-rule ladder for this seam is:

```text
yielded
  != enqueued
  != consumed
  != terminated
  != durable-effect
```

This keeps five different successes separate:
1. **yielded**
   - producer attempted to supply a value
2. **enqueued**
   - the stream accepted/buffered the value according to policy
3. **consumed**
   - one iterator-side consumer actually observed/used it
4. **terminated**
   - finish/cancellation/end-state became true
5. **durable-effect**
   - one later MainActor/policy-owned consequence happened

## Best KB use of this material
This material is best used to sharpen the existing iOS Swift-concurrency workflow note.
It should not become a broad Swift async-stream page.

The operator-facing value is:
- do not overclaim from `yield(...)`
- keep buffering acceptance visible as its own proof object
- keep iterator-side truth separate from later MainActor/policy consequence
- stop only when one later durable effect is frozen

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source result set.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked; its failure is recorded clearly.
