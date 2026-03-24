# 2026-03-24 iOS Swift async shape refinement notes

## Scope
External-research support note for reverse-KB autosync maintenance on the iOS practical branch.

Target seam:
- callback/delegate truth is already good enough, or one imported-async owner path is already plausible
- analysts still risk flattening several different modern Swift delivery shapes into one generic “async callback” bucket
- the practical KB need is better routing and stop rules, not a generic Swift-concurrency internals survey

## Mode
external-research-driven

## Search shape
Search was run through `search-layer` with explicit multi-source selection:
- `--source exa,tavily,grok`

Queries:
1. `reverse engineering Swift AsyncStream AsyncSequence continuation resume iOS callback policy`
2. `URLSession AsyncBytes AsyncSequence reverse engineering iOS response consumer`
3. `Swift CheckedContinuation AsyncStream continuation resume task wakeup practical debugging`

## Search audit
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- exa
- tavily
- grok

Failed sources:
- none at invocation time

Endpoints used on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Search transcript:
- `sources/ios/2026-03-24-ios-swift-async-shape-search-layer.txt`

## High-signal sources actually used

### 1. Swift Evolution SE-0297: Concurrency Interoperability with Objective-C
- URL: <https://github.com/swiftlang/swift-evolution/blob/main/proposals/0297-concurrency-objc.md>

Why it mattered:
- it gives the most useful official bridge reminder that many Objective-C completion-handler APIs surface in Swift as `async` / `throws`
- it explicitly shows the compiler-import pseudo-shape using continuation-based wrapping
- this supports a durable reverse-workflow rule: a visible `async` entry is not automatically a different semantic family from the underlying completion/delegate path

KB takeaway:
- keep callback/delegate truth and imported-async visibility connected
- do not widen back into broad owner search just because the current code view now looks more Swift-native

### 2. Apple / search-backed CheckedContinuation semantics
- URLs surfaced in search:
  - <https://developer.apple.com/documentation/swift/checkedcontinuation>
  - <https://developer.apple.com/videos/play/wwdc2021/10132/>

Why it mattered:
- even though direct fetch extraction was sparse, the search-layer results consistently preserve the exact-once resume rule
- that gives a practical analyst distinction between:
  - missing resume
  - double resume / misuse
  - cancellation-owned conclusion
  - later consumer divergence after a truthful resume

KB takeaway:
- treat exact-once continuation semantics as an operator classification aid, not just language trivia
- “async weirdness” is often better reduced into one smaller continuation lifecycle failure shape

### 3. Apple / search-backed AsyncStream continuation and termination surfaces
- URLs surfaced in search:
  - <https://developer.apple.com/documentation/swift/asyncstream/continuation>
  - <https://developer.apple.com/documentation/swift/asyncstream/continuation/ontermination>
  - <https://developer.apple.com/documentation/swift/asyncstream/continuation/termination>

Why it mattered:
- these reinforce that stream-shaped cases are not just single-shot continuation cases with different syntax
- delivery, buffering, finish, and termination/cancellation all form separate proof objects in practical diagnosis

KB takeaway:
- preserve `AsyncStream` as its own delivery shape in the iOS branch
- when the analyst sees delegate/callback truth plus stream buffering/yield behavior, the next truthful boundary may be yield->iterator wakeup rather than callback->resume

### 4. Apple / search-backed URLSession.AsyncBytes surface
- URLs surfaced in search:
  - <https://developer.apple.com/documentation/foundation/urlsession/asyncbytes>
  - <https://developer.apple.com/videos/play/wwdc2021/10095/>

Why it mattered:
- these support a thinner but practical distinction between header-time success and later body-consumption truth
- in reverse work, analysts can otherwise stop too early at `bytes(...)` return instead of the parser / framer / classifier that actually turns the stream into policy-bearing meaning

KB takeaway:
- preserve `AsyncSequence` / async-bytes cases as iterator-consumption shaped, not just as “streaming async” generically
- separate stream creation from iterator-side parse/classify consumption when choosing the first meaningful consumer

### 5. Swift Forums / practitioner evidence on stream delivery and cancellation
- URLs:
  - <https://forums.swift.org/t/bridging-the-delegate-pattern-to-asyncstream-with-swift6-and-sendability-issues/75754>
  - <https://forums.swift.org/t/asyncsequence-stream-version-of-passthroughsubject-or-currentvaluesubject/60395>
  - <https://forums.swift.org/t/asyncstream-element-delivery/73454>
  - <https://stackoverflow.com/questions/75464142/cancelling-the-task-of-a-urlsession-asyncbytes-doesnt-seem-to-work>

Why it mattered:
- these are not canonical specifications, but they reinforce real operator-facing pitfalls:
  - buffering policy changes observability
  - cancellation does not always mean “nothing more will be iterated immediately”
  - stream setup can look similar while iterator-side consumption diverges meaningfully

KB takeaway:
- for practical routing, it is worth preserving compare-pair questions around buffering, wakeup, termination, and iterator-side consumption rather than only callback truth

## Practical synthesis for the KB
The durable branch refinement from this run is:
- do not flatten three distinct Swift delivery shapes into one generic async seam:
  1. **single-shot continuation** — one callback/delegate/completion resumes one suspended task once
  2. **multi-value `AsyncStream`** — one producer yields multiple values and wakeups/termination/buffering matter
  3. **`AsyncSequence` / `URLSession.AsyncBytes` consumption** — stream creation may already be truthful, but the first policy-bearing meaning appears later at iterator-side parse / framing / classification

That gives a better operator ladder:
- freeze callback/delegate truth first
- classify the Swift async shape second
- choose the right next boundary for that shape
- only then reduce normalization / mapping / first consumer

## Best canonical landing spots
These notes most directly support:
- `topics/ios-swift-concurrency-continuation-to-policy-workflow-note.md`
- `topics/ios-practical-subtree-guide.md`

## Bottom line
The iOS branch needed a sharper practical distinction, not more generic async vocabulary.

The useful durable rule is:
- once callback truth is already good enough, classify whether the case is single-shot continuation, `AsyncStream`, or iterator-consumption shaped before deciding what “the next truthful boundary” even means.
