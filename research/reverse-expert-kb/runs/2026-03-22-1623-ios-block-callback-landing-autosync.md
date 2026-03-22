# Reverse KB Autosync Run Report — 2026-03-22 16:23 Asia/Shanghai

Mode: external-research-driven

## Summary
This autosync run intentionally avoided another pure internal branch-sync pass.
Recent maintenance had already strengthened broad iOS PAC/callback routing, so this run biased toward a still-practical but thinner continuation inside the iOS branch: **callback/block landing truth and runtime signature recovery**.

The main output is a new practical workflow note for cases where:
- one callback/block family is already plausible
- modern iOS PAC / dyld-cache truth affects confidence
- block signatures are still too vague for safe replay or policy claims
- the right next move is to prove one truthful landing boundary before widening back into owner or policy work

## Direction review
### Why this branch
The iOS branch is established, but this run did **not** spend itself on broad wording-only sync.
Instead it targeted a narrower operator gap between:
- mitigation-aware PAC/arm64e reasoning
- PAC-shaped callback/dispatch failure triage
- callback/result-to-policy reduction

That gap was practical and case-driven:
- analysts can often see a callback family before they can trust the landing
- `CDUnknownBlockType`-style ambiguity blocks progress in real cases
- dyld shared cache truthfulness matters directly when deciding whether a landing view is honest enough

### Branch-balance awareness
This run kept the anti-stagnation rule in mind:
- it was **not** another internal-only canonical sync pass
- it performed a real explicit multi-source search attempt with Exa, Tavily, and Grok
- it produced a concrete workflow note in a thinner practical seam rather than only editing top-level wording or family counts

## External research performed
Queries used through `search-layer --source exa,tavily,grok`:
- `iOS block invoke callback landing reverse engineering arm64e workflow`
- `Objective-C block invoke callback reverse engineering iOS pointer authentication dyld`
- `iOS arm64e callback block invoke dyld shared cache reverse engineering`

High-signal source-backed takeaways used in synthesis:
- Apple PAC documentation reinforced that authenticated-pointer pressure should be treated as a **confidence/truthfulness constraint** around callback views, not only a bypass topic
- the `ipsw` dyld guide reinforced that dyld shared cache / arm64e extraction truth is part of trustworthy callback-landing analysis
- LLDB/block-signature material reinforced that runtime-visible block signature recovery can be a better next proof object than broader hook growth when callback contracts remain vague
- older block-structure/debugging material still usefully supports the separation between block object presence, invoke landing, and later consequence

## KB changes made
### New source notes
- `sources/mobile-runtime-instrumentation/2026-03-22-ios-block-callback-landing-and-signature-recovery-notes.md`

### New practical page
- `topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md`

### Canonical synchronization updates
Updated routing/canonical pages so the new note is remembered by the branch rather than left as an orphan:
- `topics/ios-practical-subtree-guide.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `index.md`

## What the new note contributes
The new note preserves a narrower practical continuation with this core claim:
- once a modern iOS case has already narrowed into one plausible callback/block family, the next useful move is often to prove **one truthful landing boundary** and **one usable runtime contract** before making stronger owner, replay, or policy claims

It operationalizes four reminders:
1. block object presence is not the same as invoke-landing proof
2. static/decompiler view is not the same as dyld/cache-truthful runtime view
3. placeholder callback signatures are often not good enough for stronger conclusions
4. landing truth is still distinct from later ownership or policy consequence

## Practicality / case-driven value
This run stayed practical rather than taxonomic:
- it added a concrete iOS operator note
- it strengthened routing between existing iOS leaves
- it did not spend the run on abstract classification or family-count polishing
- it gives a clear handoff path from callback ambiguity into either:
  - PAC-shaped failure triage
  - owner localization
  - runtime-obligation recovery
  - result-to-policy consequence work

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

## Files changed
- `index.md`
- `topics/ios-practical-subtree-guide.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md`
- `sources/mobile-runtime-instrumentation/2026-03-22-ios-block-callback-landing-and-signature-recovery-notes.md`

## Next directions
Prefer one of these on a later run if branch pressure supports it:
- a practical iOS note on mitigation-aware replay repair when the callback landing is already trustworthy but replay still fails due to one PAC-adjacent context obligation
- a concrete case note that exercises the new callback-landing page against one representative real target pattern
- another external-research-driven pass on a different thinner branch if the rolling 6-hour window would otherwise become too iOS-internal
