# Reverse KB Autosync Run Report — 2026-03-22 21:18 Asia/Shanghai

Mode: external-research-driven

## Scope this run
This autosync run deliberately avoided another internal-only wording/index sync and instead used the required explicit multi-source search pass to deepen a still-practical but thinner continuation inside the iOS branch.

Chosen scope:
- review recent run concentration and branch-balance pressure
- perform a real external-research attempt through `search-layer --source exa,tavily,grok`
- target the specific underfed seam that recent iOS runs had already hinted at: **mitigation-aware replay repair** for PAC-shaped replay-close failures
- add a concrete workflow note, not just another branch-shape comment
- update nearby canonical routing pages so the new note is navigable and remembered by the branch
- write the run report, then commit and sync the reverse KB if KB files changed

## Summary
The main output of this run is a new practical iOS continuation page:
- `topics/ios-mitigation-aware-replay-repair-workflow-note.md`

This page fills the exact gap that earlier recent iOS runs had left open:
- the branch already had a broad mitigation-aware PAC/arm64e page
- it already had a narrower callback/dispatch triage page
- it still lacked the next continuation for cases where the path is already **replay-close** and the real remaining question is no longer broad family choice, but one smaller authenticated-context, object-materialization, or init/runtime repair target

Supporting source note added:
- `sources/mobile-runtime-instrumentation/2026-03-22-ios-pac-replay-repair-notes.md`

## Direction review
### Why this branch won this slot
Recent iOS practical runs had already done useful work on:
- broad mitigation-aware continuation
- callback/block landing proof
- callback/dispatch failure classification

That branch work repeatedly hinted at one next operator gap:
- a second narrow continuation for **replay-close missing-obligation repair** once callback family or owner path is already plausible enough

This run therefore did **not** spend itself on:
- top-level wording/index polishing
- another generic branch-shape sync
- a denser browser/mobile subtree that already has many practical leaves

Instead it used the anti-stagnation rule correctly:
- do a real multi-source external-research attempt
- pick a thinner but practical branch seam
- convert it into a source-backed workflow note with clear routing value

### Branch-balance awareness
Balance judgment this run:
- this run was correctly spent on iOS practical deepening rather than internal canonical-sync-only upkeep
- it produced a concrete operator page in a thinner seam rather than just tweaking wording or family counts
- it kept the iOS branch practical and case-driven instead of drifting into abstract PAC internals

## External research performed
Search was run explicitly through `search-layer --source exa,tavily,grok`.

Queries used:
1. `iOS arm64e PAC callback replay authenticated pointer dyld shared cache reversing`
2. `arm64e pointer authentication callback block invoke reverse engineering iOS`
3. `dyld shared cache arm64e PAC reverse engineering callback dispatch runtime landing`

High-signal source-backed takeaways used in synthesis:
- Apple pointer-authentication documentation supports the conservative operator reminder that sharp failure at an indirect/callback boundary can look like corruption even when the remaining gap is still context/provenance shaped rather than broad wrong-family proof
- `ipsw` dyld shared cache documentation supports a strong workflow rule that replay-repair claims on cache-backed code need cache/build/slide truth, not just pretty extracted pseudocode
- Binary Ninja PAC cleanup material supports keeping both a decluttered route view and the raw auth-bearing edge, because replay-repair classification can fail if the raw edge disappears from view
- recent dyld shared cache reversing material supports treating runtime/cached truth surfaces as primary when deciding whether a replay-close claim is actually trustworthy
- broader PAC background from Project Zero / USENIX was used only conservatively, as justification for not flattening replay-close arm64e failures into one simplistic story

## New practical additions made
### New workflow note
Added:
- `topics/ios-mitigation-aware-replay-repair-workflow-note.md`

What it contributes:
- a narrow operator workflow for cases where a modern iOS path is already reduced enough that broad owner search should probably stop
- an explicit four-way replay-close classification surface:
  - not actually replay-close / wrong-family
  - right family, wrong authenticated context
  - lying code-view still contaminating replay claims
  - missing narrower runtime obligation
- a practical bias toward one smaller object/context/materialization/init proof instead of reopening the whole case
- fast handoff rules back into runtime-table/init-obligation recovery or forward into result-to-policy work once the replay-close classification is done

### New source note
Added:
- `sources/mobile-runtime-instrumentation/2026-03-22-ios-pac-replay-repair-notes.md`

What it preserves:
- the exact search shape used this run
- the requested/succeeded/failed source audit required by policy
- the small supporting source set actually used
- the limits of what this run does and does not claim

### Canonical synchronization updates
Updated:
- `topics/ios-practical-subtree-guide.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `index.md`

What was synchronized:
- the iOS subtree guide now records the missing mitigation-aware replay-repair continuation as a first-class leaf instead of a future possibility
- the broad mobile reversing page now lists the new continuation explicitly
- the reverse-KB index now folds the page into the canonical iOS ladder and branch summary

## Practical value added
This run stayed practical rather than taxonomic.

The new page preserves a very specific operator lesson:
- once a modern iOS case is already replay-close, the best next move is usually not another broad theory pass
- first freeze one representative replay boundary
- preserve one truthful runtime landing and one compare pair
- classify the remaining gap conservatively
- isolate one smaller context/materialization/init repair target

That is more valuable to the KB than another broad PAC explanation because it prevents a recurring failure mode:
- replay-close confusion swallowing the rest of the case

## Search audit
Requested sources:
- Exa
- Tavily
- Grok

Succeeded sources:
- Exa
- Tavily
- Grok

Failed sources:
- none during this run’s explicit search-layer attempt

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Notes:
- This run explicitly attempted all three requested sources via `search-layer --source exa,tavily,grok`.
- No degraded-mode fallback was needed for this run.
- Search results included noisier PAC/exploitation background material, but canonical synthesis stayed conservative and workflow-first.

## Files changed
KB files changed this run:
- `research/reverse-expert-kb/topics/ios-mitigation-aware-replay-repair-workflow-note.md` (new)
- `research/reverse-expert-kb/sources/mobile-runtime-instrumentation/2026-03-22-ios-pac-replay-repair-notes.md` (new)
- `research/reverse-expert-kb/topics/ios-practical-subtree-guide.md`
- `research/reverse-expert-kb/topics/mobile-reversing-and-runtime-instrumentation.md`
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/runs/2026-03-22-2118-ios-mitigation-aware-replay-repair-autosync.md`

## Next directions
Good future follow-ons if case pressure supports them:
- a small compare-pair cookbook for replay-close callback/context failures
- a dyld-cache-to-runtime-anchor case note for private-framework callback families
- a narrower object-provenance / callback-materialization note if multiple future runs keep landing there

## Commit / sync status
Pending at report write time:
- commit KB changes if the working tree remains limited to the intended reverse-KB files
- run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

Best-effort note:
- `.learnings/ERRORS.md` logging remains best-effort only and was not required for the main success path in this run
