# Reverse KB Autosync Run Report

Date: 2026-03-25 01:16 Asia/Shanghai / 2026-03-24 17:16 UTC
Mode: external-research-driven
Scope: `research/reverse-expert-kb/`
Primary branch worked: iOS practical subtree
Chosen seam: Swift-concurrency continuation cases where callback/delegate truth is already good enough, but the first usable consequence still hides one hop later at a MainActor-isolated view-model / coordinator / UI-state consumer

## Summary
This run intentionally avoided another internal-only sync pass.

Recent reverse-KB activity had already improved several non-iOS branches, while the iOS practical subtree had also received substantial callback, replay-repair, and continuation work over the last few days. That made another broad iOS wording cleanup or another new sibling leaf the wrong move.

The thinner practical gap was narrower:
- callback/delegate landing can already be truthful enough
- continuation resume / task wakeup can already be plausible enough
- yet the first behavior-bearing proof object still lives later at a MainActor-bound state consumer

Without that reminder, the branch still risks two operator mistakes:
- stopping too early at raw callback or continuation truth
- reopening broad callback hunting when the real remaining gap is one MainActor-side state mutation, route selector, or coordinator handoff

This run therefore did a real explicit multi-source search attempt and then made a **canonical refinement** rather than creating another leaf:
- extended the existing Swift-concurrency continuation workflow note with a sharper MainActor/UI-state stop rule
- synchronized the iOS subtree guide, mobile parent page, and top-level index so the refinement survives at branch-memory level
- preserved a source note and raw search artifact for future continuation

## Direction review
This run stayed aligned with the KB’s intended direction:
- maintain and improve the KB itself, not just collect notes
- keep work practical and case-driven
- preserve a real operator stop rule rather than generic Swift-concurrency theory
- avoid dense-branch churn when a narrower canonical refinement yields more value

Why this seam was worth working:
- it is small, practical, and modern
- it changes real workflow behavior in Swift-heavy iOS cases
- it avoids turning `@MainActor` into taxonomy by tying it to one later effect
- it improves a canonical note already used in the iOS ladder rather than fragmenting the branch further

## Branch-balance awareness
Current balance judgment after this run:
- **still easy to overfeed:** browser anti-bot / captcha, broad mobile protected-runtime, and generic iOS callback-family polishing
- **recently improved enough to preserve canonically:** runtime-evidence, protocol/firmware, malware, protected-runtime exception-owned control transfer
- **good target for this run:** iOS practical continuation work, specifically the thin seam between continuation truth and the first MainActor/UI-state consumer

Why this was the right maintenance move instead of a new leaf:
- the iOS subtree already has callback landing, result-to-policy, replay-repair, and continuation pages
- what it still needed was a clearer stop rule *inside* that continuation branch
- a parent/subtree/index sync around that stop rule is more valuable than one more micro-topic page

## External research performed
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries used:
1. `Swift MainActor callback continuation UI state consumer iOS reverse engineering`
2. `Swift concurrency MainActor task UI update after await first consumer`
3. `iOS reverse engineering callback result MainActor state reducer`

Saved raw search artifact:
- `sources/mobile-runtime-instrumentation/2026-03-25-ios-mainactor-ui-state-search-layer.txt`

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
- none

Endpoints used on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Degraded-mode note:
- none for this run
- this was a full explicit multi-source external-research attempt, not Grok-only degraded execution

## Sources used conservatively
Readable retained anchors:
- Swift Forums — `Effect of @MainActor inference on Obj-C completion callbacks`
- Swift Forums — `How to correctly update the UI from an asynchronous context`
- Augmented Code — `Wrapping delegates for @MainActor consumers in Swift`
- SwiftLee — `MainActor usage in Swift explained to dispatch to the main thread`

Conservative source-backed cues retained:
- callback/delegate delivery and MainActor-owned consumption are adjacent but not identical proof objects
- delegate-to-MainActor wrapper shapes are real enough to preserve as a workflow pattern
- MainActor-isolated methods, closures, and state writes are plausible first consumers when UI-bound or view-model-bound state actually changes behavior
- imported async surfaces and completion callbacks can remain the same broad ownership family while still differing at the first MainActor-side consequence boundary
- `@MainActor` labels are only useful when tied to one later effect; they are not meaningful by themselves

## KB changes made
### New source note
Added:
- `sources/mobile-runtime-instrumentation/2026-03-25-ios-mainactor-ui-state-notes.md`

Purpose:
- preserve the narrower operator rule around callback truth, continuation truth, and MainActor/UI-state consumer truth
- keep the retained source-backed basis for this refinement close to the iOS continuation branch

### Canonical continuation page materially refined
Updated:
- `topics/ios-swift-concurrency-continuation-to-policy-workflow-note.md`

Material improvements:
- strengthened the continuation note so raw resume truth is not overread as final consequence truth
- added an explicit reminder that the first useful consumer may be a MainActor-isolated state owner, route selector, or coordinator handoff
- added a dedicated practical scenario for cases where callback and continuation are already truthful but the first usable consequence still lives at the MainActor/UI-state boundary

### iOS subtree guide updated
Updated:
- `topics/ios-practical-subtree-guide.md`

Change:
- added branch-memory that some Swift-heavy iOS cases should stop at a MainActor-side state consumer rather than reopening broad callback hunting once callback/resume truth is already good enough

### Mobile parent page updated
Updated:
- `topics/mobile-reversing-and-runtime-instrumentation.md`

Change:
- preserved the same branch-memory at the mobile parent layer so this rule does not live only in one leaf page

### Top-level branch memory updated
Updated:
- `index.md`

Change:
- top-level branch-balance memory for the iOS practical subtree now includes the MainActor/UI-state continuation reminder

## Practical operator value added
This run improved a real operator stop rule.

Before this refinement, the branch already helped analysts separate:
- callback truth
- continuation/stream truth
- later result-to-policy reduction

But it still left an avoidable ambiguity:
- if callback landing looks right and continuation resume looks right, is the job done?

After this refinement, the branch more honestly supports a narrower split:
- callback/delegate truth
- continuation/task wakeup truth
- first MainActor/view-model/UI-state consumer truth
- later effect

That changes real case handling:
- analysts are less likely to overread raw resume or a neat Swift wrapper as the decisive answer
- Swift-heavy UI/view-model apps are less likely to trigger a wasteful return to broad callback hunting
- the branch now better supports proving one later effect from one MainActor-side state consumer

This is practical operator value because it is:
- small enough to apply in live iOS reversing work
- source-backed enough to preserve conservatively
- strong enough to improve canonical branch routing rather than just polishing wording

## Files changed
Added:
- `sources/mobile-runtime-instrumentation/2026-03-25-ios-mainactor-ui-state-search-layer.txt`
- `sources/mobile-runtime-instrumentation/2026-03-25-ios-mainactor-ui-state-notes.md`
- `runs/2026-03-25-0116-reverse-kb-autosync.md`

Updated:
- `topics/ios-swift-concurrency-continuation-to-policy-workflow-note.md`
- `topics/ios-practical-subtree-guide.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `index.md`

## Best-effort errors logging note
No `.learnings/ERRORS.md` update was necessary for the main workflow.
Search/runtime degradation would have been recorded here if present, but all requested search sources were successfully attempted in this run.

## Commit / sync status
Plan for this run:
1. commit the reverse-KB files changed by this workflow
2. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
3. leave this run report as the archival record

## Bottom line
This was a real external-research-driven maintenance run on a thinner but practical iOS seam.

The KB now preserves a sharper Swift-heavy iOS stop rule:
- callback truth is not yet continuation truth
- continuation truth is not yet MainActor/UI-state consumer truth
- and in some cases the first behavior-bearing proof object is the MainActor-side handoff that selects state, route, or visible app behavior
