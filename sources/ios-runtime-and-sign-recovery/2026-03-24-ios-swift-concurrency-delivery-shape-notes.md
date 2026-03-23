# 2026-03-24 iOS Swift concurrency delivery-shape notes

## Scope
External-research support note for an autosync run that intentionally deepens an already-established iOS Swift-concurrency continuation seam.

This pass does **not** try to reopen broad questions like:
- whether callback/delegate truth is already solved
- whether Swift async code exists at all
- whether result-to-policy reduction is valuable in general

Instead it preserves one narrower practical rule for modern iOS reversing:
- do not flatten **single-shot continuation**, **multi-value `AsyncStream`**, and **`AsyncSequence` / async-bytes consumption** into one generic “Swift async” bucket
- classify the delivery shape first, because the truthful consequence boundary is often different in each case

## Mode
external-research-driven

## Search shape
Search was run through `search-layer` with explicit multi-source selection:
- `--source exa,tavily,grok`

Queries:
1. `Swift CheckedContinuation AsyncStream reverse engineering iOS async callback resume practical`
2. `URLSession async await delegate continuation AsyncStream practical behavior Apple docs`
3. `Swift concurrency Task MainActor AsyncStream continuation scheduling reverse engineering practical`

## Search audit
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- tavily
- grok

Failed sources:
- exa

Endpoints used on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Search transcript:
- `sources/ios-runtime-and-sign-recovery/2026-03-24-ios-swift-concurrency-search-layer.txt`

Degraded-mode note:
- This run attempted all three requested sources explicitly.
- Returned search results were materially usable from Tavily + Grok.
- Exa did not appear in the returned result-source sets for the retained hits, so this run is recorded as an external-research-driven run under a degraded source set rather than a full three-source success.

## High-signal sources actually used

### 1. Apple Developer Documentation — `CheckedContinuation`
- URL: <https://developer.apple.com/documentation/swift/checkedcontinuation>

Why it mattered:
- even with thin extraction, the doc supports the exact-once-resume discipline
- this is enough to preserve the practical reminder that single-shot continuation cases should be analyzed around one truthful resume boundary, not around generic async wrapper accumulation

KB takeaway:
- in a single-shot continuation case, the main stop rule is often:
  - continuation created/stored
  - resumed exactly once
  - later resumed task-side reducer/consumer proves consequence

### 2. Apple Developer Documentation — `AsyncStream`
- URL: <https://developer.apple.com/documentation/swift/asyncstream>

Why it mattered:
- the doc explicitly positions `AsyncStream` as a way to adapt callback/delegate style delivery into an asynchronous sequence
- that supports preserving a different operator boundary from single-shot continuation: stream construction is not yet consequence ownership, and neither is just seeing that the stream object exists

KB takeaway:
- in an `AsyncStream` case, the practical boundary is often:
  - stream created
  - values yielded / buffered
  - one specific iterator-side consumer wakes and changes behavior

### 3. Apple Developer Documentation — `URLSession.AsyncBytes`
- URL: <https://developer.apple.com/documentation/foundation/urlsession/asyncbytes>

Why it mattered:
- this keeps alive a third delivery shape that is easy to flatten away in practical reversing notes: sequence-style byte delivery
- a bytes/sequence object being returned is not the same thing as proving the first parser, framer, classifier, or coordinator that turns delivery into app-local meaning

KB takeaway:
- in `AsyncSequence` / async-bytes cases, a useful stop rule is often:
  - sequence becomes available
  - iterator/`for await` consumption begins
  - parser/framer/classifier reduces bytes/events into app-local meaning
  - later consumer changes behavior

### 4. Swift Forums — `AsyncStream and Actors`
- URL: <https://forums.swift.org/t/asyncstream-and-actors/70545>

Why it mattered:
- the discussion reinforces that stream delivery and actor/executor context are operationally separate concerns in real code
- that supports a conservative workflow reminder: even when the callback/delegate family is already frozen, the real next question may be which actor/task-side consumer is actually woken and where delivery becomes behavior-bearing

KB takeaway:
- stream yield, actor handoff, and first consumer should often be separated instead of treated as one blob of “async handling”

### 5. Donny Wals — migrating callback-based code to Swift concurrency with continuations
- URL: <https://www.donnywals.com/migrating-callback-based-code-to-swift-concurrency-with-continuations/>

Why it mattered:
- although not an official reversing source, it cleanly reiterates the exact-once-resume and missing-resume hazards
- this is directly useful as a workflow reminder when one callback family fires but one compare run never reaches the same resumed reducer/consumer

KB takeaway:
- when the callback fires in both runs but only one run reaches the same post-resume path, a narrower next question may be resume discipline, cancellation/timeout handling, or stale-task handling rather than more callback hunting

## Practical synthesis for the KB
The durable claim supported by this run is modest but operationally useful:
- once an iOS case has already narrowed into Swift-concurrency-owned consequence proof, the analyst should first classify whether the case is:
  1. **single-shot continuation shaped**
  2. **multi-value `AsyncStream` shaped**
  3. **`AsyncSequence` / async-bytes consumption shaped**

That classification matters because the best next proof object differs:
- **single-shot continuation**
  - best next proof often centers on exact-once resume and the first resumed task-side reducer/consumer
- **`AsyncStream`**
  - best next proof often centers on first yield/dequeue and which iterator-side consumer is actually woken
- **`AsyncSequence` / bytes**
  - best next proof often centers on first iterator-side parser/framer/classifier rather than on sequence creation or header-time visibility alone

A compact operator rule now worth keeping canonically is:
- do not stop at the prettiest `async` surface
- do not stop at stream creation
- do not stop at sequence availability
- stop at the first delivery-shape-appropriate consumer that actually predicts later behavior

## What this run deliberately did not claim
- that every Swift async case can be cleanly classified from static surface alone
- that `AsyncStream` and `AsyncSequence` always imply different business logic
- that `URLSession.AsyncBytes` is common in all real-world iOS targets
- that exact-once-resume or actor handoff issues are always the reason one compare run diverges

## Best canonical landing spots
These notes best support:
- `topics/ios-swift-concurrency-continuation-to-policy-workflow-note.md`
- `topics/ios-practical-subtree-guide.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`

## Bottom line
A useful iOS practical stop rule is now sharper:
- first decide whether the async-looking seam is continuation-shaped, stream-shaped, or iterator-consumption-shaped
- then prove the first delivery-shape-appropriate consumer
- only after that widen into broader policy or replay explanations
