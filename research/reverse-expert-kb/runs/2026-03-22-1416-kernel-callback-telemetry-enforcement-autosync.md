# 2026-03-22 14:16 Asia/Shanghai — kernel callback telemetry -> enforcement consumer autosync

Mode: external-research-driven

## Summary
This run intentionally avoided another pure canonical-sync-only pass.
Recent autosync work had already covered several internal/practical seams, including watchdog enforcement, native async ownership, runtime evidence, and malware persistence continuations. To satisfy the anti-stagnation rule and branch-balance guidance, this run performed a real external-research pass on a thinner protected-runtime seam:
- callback-heavy kernel telemetry in anti-cheat-adjacent / privilege-heavy monitoring cases
- the analyst bottleneck of getting from visible callback registration to the first enforcement-relevant consumer

The run produced a new practical workflow note plus the usual canonical synchronization work so the addition does not remain stranded as an isolated leaf.

## Branch-balance / direction review
Why this branch was chosen:
- the protected-runtime branch was already materially established, but anti-cheat-adjacent operator guidance remained lighter than browser/mobile and even lighter than newer malware/runtime-evidence continuations
- recent runs had already added a watchdog / heartbeat continuation inside protected-runtime, but callback-heavy kernel telemetry still lacked a concrete workflow page
- the KB’s anti-cheat material was still mostly conceptual inside `anti-tamper-and-protected-runtime-analysis.md`, which risked keeping anti-cheat as “interesting context” instead of a source-backed practical operator seam

Direction decision for this run:
- do a real multi-source search pass
- bias toward a practical workflow note instead of another top-level wording/index repair
- improve the KB itself by adding one operator page and then syncing the protected-runtime parent/index around it

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
- none during the explicit `search-layer --source exa,tavily,grok` attempt

Endpoints used on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Queries used:
1. `kernel anti cheat callback telemetry enforcement consumer reverse engineering workflow`
2. `ObRegisterCallbacks PsSetCreateThreadNotifyRoutine anti cheat enforcement analysis`
3. `minifilter ETW anti cheat driver event pipeline enforcement reverse engineering`

## Sources used
Primary grounding used for the new page:
- Microsoft Learn — `PsSetCreateThreadNotifyRoutine`
- SpecterOps — `Understanding Telemetry: Kernel Callbacks`
- s4dbrd — `How Kernel Anti-Cheats Work`
- `Fast and Furious: Outrunning Windows Kernel Notification Routines from User-Mode`

Why these were enough:
- official API grounding for producer-side callback boundaries
- structural explanation of callback registration / trigger / object-callback paths
- practical anti-cheat architecture context showing why kernel telemetry is often only one layer in a broader protection stack
- timing-sensitive protected-process paper support for treating registration/setup and later protection effect as distinct analytical boundaries

## KB changes made
### New source note
Created:
- `sources/protected-runtime/2026-03-22-kernel-callback-telemetry-enforcement-notes.md`

Purpose:
- records the explicit multi-source search pass
- preserves the search audit and endpoint record required by policy
- distills callback-registration vs telemetry-carrier vs enforcement-consumer structure into reusable notes

### New practical workflow note
Created:
- `topics/kernel-callback-telemetry-to-enforcement-consumer-workflow-note.md`

What it adds:
- a protected-runtime-specific workflow note for cases where kernel callback registration is already visible but behavioral ownership is still unclear
- a practical ladder:
  - choose one callback family
  - separate registration from actual trigger path
  - isolate the first telemetry carrier or reducer
  - prove one enforcement-relevant consumer
  - route to the next quieter target

Why this is materially useful:
- it turns anti-cheat-adjacent callback-heavy targets into a workflow problem instead of a taxonomy-only topic
- it fills a gap between the existing watchdog note and the native callback/event-loop note

### Canonical synchronization
Updated:
- `topics/protected-runtime-practical-subtree-guide.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `index.md`

What changed canonically:
- protected-runtime branch now explicitly includes **kernel-callback telemetry to enforcement-consumer reduction** as a practical bottleneck family
- subtree guide now routes into the new note explicitly instead of leaving anti-cheat-like kernel telemetry implicit
- parent protected-runtime synthesis now reflects anti-cheat as not just a conceptual case, but also a callback-heavy telemetry-to-policy workflow seam
- top-level index now includes the new note in the protected-runtime branch ladder

## Practical synthesis from the run
The main reusable insight from the sources was:
- callback registration is easy to over-credit
- the real analyst milestone is the first object that survives callback scope and predicts protected behavior better than the callback label itself

For this seam, the useful recurring units are:
1. callback family
2. trigger/delivery path
3. telemetry carrier or reducer
4. enforcement-relevant consumer
5. later effect

That is a better operator ladder than:
- callback API cataloging
- generic anti-cheat summary
- broad “kernel monitoring exists” narration

## Why this was not just another internal maintenance run
This run qualifies as external-research-driven because it actually attempted and used explicit multi-source search via `search-layer --source exa,tavily,grok` and then converted those results into:
- a new source-backed practical workflow note
- branch-level canonical synchronization around that note

It did **not** merely do:
- family-count sync
- wording cleanup
- index-only repair
- another browser/mobile densification pass

## Files changed
Created:
- `sources/protected-runtime/2026-03-22-kernel-callback-telemetry-enforcement-notes.md`
- `topics/kernel-callback-telemetry-to-enforcement-consumer-workflow-note.md`
- `runs/2026-03-22-1416-kernel-callback-telemetry-enforcement-autosync.md`

Updated:
- `topics/protected-runtime-practical-subtree-guide.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `index.md`

## Next sensible directions
Prefer one of these in future protected-runtime maintenance passes:
- a concrete case-driven continuation for callback setup timing / early-window races when that seam accumulates enough source pressure
- a narrower anti-cheat/trusted-runtime comparison note only if it remains workflow-centered rather than taxonomy-heavy
- cross-branch cleanup comparing callback-heavy protected-runtime cases against ordinary native callback/event-loop ownership so the boundary between those branches stays sharp

Avoid for the next few runs unless clearly needed:
- multiple consecutive protected-runtime wording/index-only sync passes without another source-backed practical addition
- treating anti-cheat merely as broad conceptual context after this workflow seam has now been established

## Commit / sync expectation
If KB changes are present:
- commit them
- run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

This run produced KB changes, so commit + archival sync should follow.
