# Reverse KB Autosync Run Report

Date: 2026-03-24 05:16 Asia/Shanghai
Mode: external-research-driven
Scope: `research/reverse-expert-kb/`
Primary branch worked: iOS practical subtree
Chosen seam: Swift-concurrency continuation seam -> delivery-shape classification (`CheckedContinuation` vs `AsyncStream` vs `AsyncSequence` / async-bytes)

## Summary
This run intentionally avoided another internal-only branch-memory / wording / index sync pass.

Recent iOS maintenance had already established a useful continuation page for cases where callback/delegate truth is already good enough but the first Swift-owned consequence boundary is still unclear.
What still looked slightly underfed was one thinner, very practical stop rule inside that page:
- analysts can still over-collapse three different async-looking seams into one generic “Swift async callback” bucket
- that flattening makes the chosen proof boundary too high and can send the case back into vague wrapper hunting

This run therefore did a real external search pass and sharpened the iOS practical branch around one narrower operator rule:
- classify whether the seam is **single-shot continuation**, **multi-value `AsyncStream`**, or **`AsyncSequence` / async-bytes consumption** shaped before choosing the next truthful consequence boundary

That is a KB improvement, not just source collection:
- the canonical workflow note now preserves the split explicitly
- the iOS subtree guide now remembers the classification stop rule
- the mobile parent page now preserves the same branch memory at the synthesis layer

## Direction review
This run stayed aligned with the reverse KB’s intended direction:
- maintain and improve the KB itself, not just collect links
- keep work practical and case-driven
- prefer a thinner operator seam over dense-branch polishing
- improve branch memory and stop rules only where they materially change how a real case would be worked

Why this branch was the right choice now:
- the iOS practical branch is now established enough that small continuation-quality refinements have real operator value
- recent runs had already fed other branches, so this was a branch-balance-safe way to keep iOS practical guidance improving without slipping into pure wording cleanup
- the chosen seam was still thin, practical, and source-backed rather than merely editorial

## Branch-balance awareness
Current balance judgment after this run:
- **Still easy to overfeed:** browser anti-bot / already-dense protected-runtime continuations
- **Recently established and worth keeping coherent:** iOS practical branch, especially the callback -> continuation -> policy handoff region
- **Good target for this run:** a thin iOS continuation seam that materially improves operator stop rules without spawning another broad leaf

Why this seam mattered:
- the continuation page already preserved callback truth vs post-resume consequence proof
- but it still risked treating continuation resume, `AsyncStream` delivery, and `AsyncSequence` / async-bytes consumption as one generic async family
- that is operationally too coarse because the decisive proof boundary differs:
  - exact-once resume in single-shot continuation cases
  - first yield/dequeue + iterator wakeup in `AsyncStream` cases
  - first parser/framer/classifier in async-bytes / sequence-consumption cases

This made it a good anti-stagnation run:
- real multi-source external search was attempted
- the run materially sharpened a practical workflow page
- the work did not collapse into index-only or family-count-only maintenance

## External research performed
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries used:
1. `Swift CheckedContinuation AsyncStream reverse engineering iOS async callback resume practical`
2. `URLSession async await delegate continuation AsyncStream practical behavior Apple docs`
3. `Swift concurrency Task MainActor AsyncStream continuation scheduling reverse engineering practical`

Saved raw search artifact:
- `sources/ios-runtime-and-sign-recovery/2026-03-24-ios-swift-concurrency-search-layer.txt`

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

Degraded-mode note:
- This run explicitly attempted all three requested sources.
- Returned retained hits were materially usable from Tavily + Grok.
- Exa did not appear in the returned source sets for the retained hits, so this run proceeded conservatively under a degraded source set and records that clearly here.

## Sources used conservatively
Primary retained sources:
- Apple Developer Documentation — `CheckedContinuation`
- Apple Developer Documentation — `AsyncStream`
- Apple Developer Documentation — `URLSession.AsyncBytes`
- Swift Forums — `AsyncStream and Actors`
- Donny Wals — migrating callback-based code to Swift concurrency with continuations

Retained source-backed cues:
- checked continuations preserve exact-once-resume discipline and make single-shot resume a meaningful proof boundary
- `AsyncStream` is a callback/delegate-to-async-sequence bridge, so stream creation is not yet the same thing as proving the first consequence-bearing consumer
- `URLSession.AsyncBytes` preserves a sequence-consumption shape where sequence availability and iterator-side parsing/classification should not be collapsed together
- stream delivery and actor/task-side consumption are often operationally distinct enough to preserve separately in workflow guidance

## KB changes made
### New source note
Added:
- `sources/ios-runtime-and-sign-recovery/2026-03-24-ios-swift-concurrency-delivery-shape-notes.md`

Purpose:
- preserve the delivery-shape classification rule and supporting source cues
- record the degraded search-source set explicitly

### Canonical workflow note materially refined
Updated:
- `topics/ios-swift-concurrency-continuation-to-policy-workflow-note.md`

Material improvements:
- added an explicit warning not to flatten single-shot continuation, `AsyncStream`, and `AsyncSequence`/async-bytes cases into one generic async bucket
- strengthened the resume/delivery section so iterator-side consumption is preserved as its own truthful boundary where needed
- added a concrete scenario for async-bytes / sequence-consumption cases where the first parser or classifier, not sequence existence, is the real consequence boundary
- updated hook-placement and failure-pattern guidance to preserve delivery-shape-aware stop rules

### iOS subtree guide updated
Updated:
- `topics/ios-practical-subtree-guide.md`

Change:
- sharpened the iOS routing checklist so the Swift-concurrency handoff explicitly remembers iterator-consumption-shaped cases
- added a stop rule requiring delivery-shape classification before choosing the next truthful async boundary too high

### Mobile parent page updated
Updated:
- `topics/mobile-reversing-and-runtime-instrumentation.md`

Change:
- preserved the same delivery-shape reminder at the parent-page layer so this logic does not live only in one leaf note

## Practical operator value added
This run improved a real stop rule that changes how an analyst works a modern iOS case.

Before this refinement, the branch could still nudge readers toward a slightly too-flat interpretation:
- “I found the Swift async layer, so now I just need some generic post-resume consumer.”

After the refinement, the branch more honestly supports:
- **single-shot continuation cases** -> prove exact-once resume and the first resumed task-side reducer/consumer
- **`AsyncStream` cases** -> prove first yield/dequeue and which iterator-side consumer actually wakes and matters
- **`AsyncSequence` / async-bytes cases** -> prove the first parser/framer/classifier that turns sequence delivery into app-local meaning

That is practical operator value:
- small enough to apply in real runtime work
- source-backed enough to keep conservatively
- thin enough to fit branch-balance goals
- clearly better than another wording-only sync run

## Files changed
Added:
- `sources/ios-runtime-and-sign-recovery/2026-03-24-ios-swift-concurrency-delivery-shape-notes.md`
- `runs/2026-03-24-0516-reverse-kb-autosync.md`

Updated:
- `topics/ios-swift-concurrency-continuation-to-policy-workflow-note.md`
- `topics/ios-practical-subtree-guide.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`

## Commit / sync plan
If KB-only changes are present after review:
1. commit the KB changes
2. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
3. leave this run report as the archival record

## Bottom line
This was a real external-research-driven maintenance run on a thinner but still practical iOS seam.

The KB now preserves a sharper rule:
- do not treat all Swift-concurrency-looking flows as one bucket
- classify continuation vs `AsyncStream` vs sequence-consumption first
- then prove the first delivery-shape-appropriate consumer that actually predicts later behavior
