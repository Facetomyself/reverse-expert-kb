# Reverse KB Autosync Run Report — 2026-03-23 16:16 Asia/Shanghai

Mode: external-research-driven

## Summary
This autosync run deliberately avoided another internal-only wording/index/family-count pass.

Recent runs had already spent meaningful attention on:
- protocol minimal replay / pending-request seams
- malware scheduled-task / scheduled-job consumer proof
- native completion-port / thread-pool consumer proof
- protected-runtime watchdog and callback pages in broad form

So this run targeted a thinner still-practicality-starved protected-runtime seam:
- **kernel callback telemetry -> first enforcement consumer**, with a narrower distinction between:
  - a **local rights-bearing consumer** inside callback context, and
  - an **emitted-record / queue / IOCTL / service handoff consumer** outside callback context

That produced a concrete workflow improvement rather than another top-level wording refresh.

## Direction review
Branch-balance / anti-stagnation review:
- This was **not** treated as a canonical-sync-only maintenance run.
- A real external-research pass was attempted with explicit `exa,tavily,grok` sources.
- Work selection biased toward a thinner protected-runtime practical leaf instead of dense-branch polishing.
- The resulting KB change was case-driven and operator-facing, not just taxonomic.

Why this branch won:
- protocol had already received multiple recent practical passes
- malware and native had also received several fresh consumer-proof refinements
- protected-runtime still had room for a sharper callback-specific operator split that recent runs had not yet articulated clearly enough

## Work completed
### 1. Performed explicit multi-source external research
Used `search-layer` with explicit sources:
- `exa`
- `tavily`
- `grok`

Query set:
1. `Windows kernel callback object callbacks telemetry enforcement consumer anti-cheat rights filter queue handoff`
2. `ObRegisterCallbacks access mask downgrade telemetry queue service handoff reverse engineering`
3. `process image thread notify callbacks anti-cheat telemetry reducer enforcement consumer reverse engineering`

### 2. Pulled stronger source material
Fetched and used:
- Microsoft Learn — `ObRegisterCallbacks`
- XPN — `OpenProcess` filtering / callback-based rights filtering discussion
- *Fast and Furious* paper on notification timing and handle-filter setup windows
- modern kernel anti-cheat architecture overview emphasizing driver -> IOCTL/shared-memory/service layering

### 3. Materially improved the KB itself
Extended:
- `topics/kernel-callback-telemetry-to-enforcement-consumer-workflow-note.md`

Improvement made:
- added explicit **Subcase A** for local rights-bearing consumers
- added explicit **Subcase B** for emitted-record / handoff consumers
- tightened proof guidance for:
  - requested access vs resulting granted access
  - callback firing vs settled-state rights outcome
  - callback emission vs downstream queue / IOCTL / shared-buffer consumption

Why this matters:
- prevents analysts from over-hunting a larger service narrative when the reduced access mask already explains behavior
- prevents analysts from overreading callback-local helpers when the callback is only a telemetry producer and the real consumer is downstream

### 4. Added archival/source note
Created:
- `sources/protected-runtime/2026-03-23-kernel-callback-local-vs-handoff-consumer-notes.md`

This note captures the source-backed distinction and preserves the search audit for future branch maintenance.

## Files changed
Modified:
- `topics/kernel-callback-telemetry-to-enforcement-consumer-workflow-note.md`

Created:
- `sources/protected-runtime/2026-03-23-kernel-callback-local-vs-handoff-consumer-notes.md`
- `runs/2026-03-23-1616-kernel-callback-local-vs-handoff-consumer-autosync.md`

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
- none during the search-layer pass itself

Endpoints used / configured on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Trace:
- `/tmp/reverse-kb-2026-03-23-1616-search.txt`

## Practical outcome
The protected-runtime branch now says something more operationally useful than before:
- if the callback directly rewrites the consequence-bearing rights object, treat that as the first enforcement consumer unless evidence forces a later story
- if the callback stays short and telemetry-heavy, stop overreading callback-local helpers once one emitted record or reducer write is isolated and move to the first downstream consumer

That is a better field rule than merely repeating “registration is not enough.”

## Commit / sync status
Planned after report write:
- commit KB changes if any
- run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

## Conservative limits
- did not claim vendor-specific callback pipelines beyond what the sources could support conservatively
- did not treat search-result snippets alone as sufficient evidence
- did not convert the page into bypass instructions
- kept this as workflow-centered practical maintenance of the KB itself
