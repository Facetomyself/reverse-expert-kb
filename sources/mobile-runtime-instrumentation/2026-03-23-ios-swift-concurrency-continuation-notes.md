# 2026-03-23 iOS Swift concurrency continuation / async-result ownership notes

## Scope
External-research support note for a reverse-KB autosync run targeting a thinner iOS practical seam:
- callback/block landing is already plausible or already frozen strongly enough
- visible result material now appears inside Swift `async` / continuation / stream-shaped machinery
- the remaining analyst gap is often not “find more callbacks,” but proving where continuation-owned result material becomes one durable app-local policy state

The goal is not a broad Swift concurrency internals survey.
The goal is to support a practical workflow rule for modern iOS reversing when completion-handler or delegate-era reasoning has already narrowed into Swift-concurrency-owned result consumption.

## Mode
external-research-driven

## Search shape
Search was run through `search-layer` with explicit multi-source selection:
- `--source exa,tavily,grok`

Queries:
1. `Swift concurrency CheckedContinuation callback completion handler reverse engineering block async await iOS`
2. `withCheckedContinuation AsyncStream delegate callback completion handler state machine Swift iOS debugging`
3. `Swift async await generated state machine continuation resumption callback Objective-C bridge reverse engineering iOS`

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
- `sources/mobile-runtime-instrumentation/2026-03-23-ios-swift-concurrency-continuation-search-layer.txt`

## High-signal sources actually used

### 1. Swift Evolution SE-0297: Concurrency Interoperability with Objective-C
- URL: <https://github.com/swiftlang/swift-evolution/blob/main/proposals/0297-concurrency-objc.md>

Why it mattered:
- it gives the most useful source-backed reminder that many Objective-C completion-handler APIs are imported into Swift as `async` / `throws` entry points
- it explicitly frames the compiler bridge as continuation-based, with pseudo-code that wraps the completion handler and resumes a continuation
- this helps analysts avoid treating the imported async surface as an entirely separate semantic family from the underlying completion path

KB takeaway:
- when a visible Swift `async` path feels owner-relevant, the first practical question is often whether the remaining unknown is still the completion-side contract, or the first post-resume consumer in Swift task/continuation-owned logic
- that means some iOS cases should stop at callback landing, while others should continue into a narrower continuation-owned result-consumer workflow

Caution:
- this proposal explains the language/runtime bridge model, not a reverse-engineering recipe
- used here only to support conservative workflow framing

### 2. Apple documentation: Calling Objective-C APIs Asynchronously
- URL: <https://developer.apple.com/documentation/swift/calling-objective-c-apis-asynchronously>

Why it mattered:
- even though extraction here was thin, the source supports the same practical bridge: Apple officially presents Objective-C completion-handler APIs as Swift async APIs
- that is enough to reinforce the operator lesson that async-looking Swift call sites may still be fed by older completion/delegate machinery

KB takeaway:
- do not over-separate callback-landings truth from continuation-owned consequence proof
- modern iOS practical routing needs an explicit handoff point between those two stages

Caution:
- readable extraction was sparse, so this source is supporting context rather than the main retained evidence

### 3. Swift Forums discussion on adapting completion-block code via `withCheckedContinuation`
- URL: <https://forums.swift.org/t/considerations-when-adapting-completion-block-async-code-to-swift-concurrency-via-withtaskcancellationhandler-withcheckedcontinuation/68892>

Why it mattered:
- the concrete page extraction was weak, but the topic itself corroborates that real-world code commonly wraps completion-block APIs using continuation machinery and cancellation handling
- for analysts, that matters because a path may look “post-callback” while still being structurally dominated by continuation lifecycle and exact-once resume assumptions

KB takeaway:
- when replay or hook evidence says the callback family is right but the behavioral consequence is still elusive, continuation lifecycle ownership can be the thinner next branch

Caution:
- retained conservatively because extract quality was poor
- used as corroboration, not as the primary proof object

### 4. Swift Forums discussion on bridging delegate patterns to `AsyncStream`
- URL: <https://forums.swift.org/t/bridging-the-delegate-pattern-to-asyncstream-with-swift6-and-sendability-issues/75754>

Why it mattered:
- this source usefully reinforces that modern Swift code often converts delegate/callback delivery into stream/continuation-owned state and buffering
- from a reverse-engineering perspective, that means the first meaningful consumer may no longer be the delegate callback itself, but the first task/stream reducer, iterator wakeup, or buffering policy that turns delivery into later app behavior

KB takeaway:
- a practical iOS branch should explicitly preserve the handoff: callback/delegate truth first, then continuation/stream-owned consequence proof when the result material is already truthful enough

Caution:
- again, extraction quality was light, so this supports workflow shape more than detailed internals

### 5. SwiftRocks: How async/await works internally in Swift
- URL: <https://swiftrocks.com/how-async-await-works-internally-in-swift>

Why it mattered:
- although not an official specification, it provides operator-valuable framing around async/await lowering, cooperative execution, and the fact that async code is not magic but runtime/compiler machinery around resumable tasks
- it is especially useful as a reminder that the analyst should look for state-machine/resume boundaries and not assume the prettiest `async` call site owns the consequence

KB takeaway:
- a useful proof object in these cases is often:
  - one callback/delegate or completion bridge already frozen strongly enough
  - one continuation-resume or stream-delivery boundary
  - one first reducer / mapper / consumer in task-owned logic
  - one downstream policy effect

Caution:
- non-official and self-described as partly reverse-engineered
- used only for workflow intuition, not fine-grained ABI claims

## Practical synthesis for the KB
The narrow durable claim supported by this run is:
- once a modern iOS case already has a truthful callback/delegate family or a plausible async owner path, a recurring thinner next step is to prove the **first continuation-owned consequence boundary** rather than reopen broad owner search or overread the visible callback itself

That proof object often looks like:
- one already-frozen callback/delegate/completion family or imported-async owner path
- one continuation resume / stream delivery / task wakeup boundary
- one result normalization or policy-mapping reducer inside Swift-owned logic
- one first behavior-changing consumer or downstream effect

This helps classify ambiguity more honestly:
- callback truth still not solved
- callback truth solved, but resume/stream ownership still unclear
- resume ownership solved, but policy mapper/consumer still unclear
- replay-close path still missing one narrower init/context/materialization obligation

## What this run deliberately did not claim
- that every modern iOS callback case becomes a Swift-concurrency case
- that every async function visible in Swift code is compiler-imported from Objective-C
- that continuation internals alone explain replay or policy failures
- that generic async/await lowering details are enough to replace runtime proof of one concrete consumer

## Best canonical landing spots
These notes best support:
- a new thinner iOS practical continuation page for Swift-concurrency continuation / async-result consequence proof
- explicit routing updates in `topics/ios-practical-subtree-guide.md`
- a small parent-page update in `topics/mobile-reversing-and-runtime-instrumentation.md`

And they should hand off cleanly to:
- `topics/ios-result-callback-to-policy-state-workflow-note.md`
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`

## Bottom line
The practical iOS gap here is not just “find the callback.”
In some modern cases it is:
- freeze the callback or imported-async owner strongly enough
- find the continuation-owned or stream-owned delivery boundary
- prove the first Swift-side reducer / consumer that changes behavior
- only then widen into broader policy or replay explanations.
