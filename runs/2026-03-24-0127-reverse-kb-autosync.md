# Reverse KB Autosync Run Report

Date: 2026-03-24 01:27 Asia/Shanghai
Mode: external-research-driven

## Summary
This run deliberately avoided another internal-only canonical sync pass.
Recent autosync work had already spent several consecutive runs on internal branch-shape / wording / index synchronization, so this run prioritized a thinner but still practical protected-runtime seam that could benefit from a real external pass.

The chosen target was the packed-startup / protected-runtime branch, specifically the operator gap around:
- a plausible post-unpack jump already existing
- but Windows startup reality still making it easy to stop too early
- because TLS callbacks, CRT/runtime startup, constructor/init-table work, or a secondary loader stage can separate:
  - raw PE entry
  - raw post-unpack transfer
  - first payload-bearing post-startup handoff

The result was a source-backed practical refinement to the packed-startup workflow note, plus small branch-memory updates in the protected-runtime subtree guide, protected-runtime parent page, and top-level index.

## Direction review
This run stayed aligned with the KB’s intended direction:
- practical and case-driven rather than taxonomic
- focused on a recurring operator stop-rule mistake
- improved the KB itself rather than only collecting loose notes
- added a source-backed continuation inside an already-real branch instead of polishing a dense browser/mobile area again

This is the kind of addition the branch needed:
- not another broad packer overview
- not another family-count / wording-only sync
- but one sharper workflow distinction analysts can actually apply during unpacking and early post-unpack validation

## Branch-balance review
Protected-runtime remains one of the KB’s stronger practical branches, but this particular seam was thinner than the broader VM / dispatcher / integrity surfaces.

Why this branch choice was justified:
- recent runs already improved index memory and several existing branch summaries
- protected-runtime had an actionable underfed continuation available
- the new work deepens a practical handoff rule instead of adding another dense top-level taxonomy paragraph
- the addition improves a cross-domain reusable pattern for Windows/native packed targets without reopening a huge new branch

Anti-stagnation assessment:
- external multi-source search was actually attempted this run
- this was a real source-backed pass, not a KB-only fallback disguised as research
- the output materially extended a practical workflow note rather than just touching top-level wording

## Work completed
### New source note
- `sources/protected-runtime/2026-03-24-packed-oep-vs-tls-crt-notes.md`

This note captured the practical distinction between:
- raw entry point
- raw post-unpack transfer
- first payload-bearing post-startup handoff

It used Windows/TLS/CRT startup behavior to sharpen the packed-startup workflow’s stop rules.

### KB pages updated
- `topics/packed-stub-to-oep-and-first-real-module-workflow-note.md`
- `topics/protected-runtime-practical-subtree-guide.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `index.md`

### Material KB improvement made
The main KB improvement was a new startup-normalization-aware rule for packed Windows/native targets:
- do not overclaim the first dramatic post-unpack transfer as the final useful handoff
- explicitly distinguish:
  - raw PE entry point
  - raw post-unpack transfer
  - first payload-bearing post-startup handoff
- when TLS callbacks / CRT startup / constructor-init scaffolding are still active, keep pushing until one import/module/object/consumer anchor survives after those stages quiet down

### Why this matters operationally
This reduces a very common unpacking failure mode:
- “I found the jump, therefore I found the real handoff”

The KB now more clearly supports the better operator question:
- “Did I only leave the stub, or did I actually reach the first reusable payload target?”

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
- none at the search-layer invocation level

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Search command shape:
- explicit `search-layer` run with `--source exa,tavily,grok`

Search artifact:
- `sources/protected-runtime/2026-03-24-packed-oep-vs-tls-crt-search-layer.txt`

Fetch-level degradation notes:
- `web_fetch` on the Black Hat Yason PDF returned a 403/interstitial and was not usable directly in this run
- that fetch failure did not invalidate the run’s multi-source search attempt because the search-layer invocation itself successfully exercised `exa`, `tavily`, and `grok`
- the run proceeded conservatively, using direct fetched pages where available and search/snippet support where not

## Sources used in synthesis
Primary directly used pages:
- Raymond Chen on WinMain / real PE entry reality
- Ring Zero Labs on TLS callbacks and early anti-analysis behavior
- StrelaStealer unpacking casework showing practical traversal past TLS-owned startup to a useful payload boundary
- Kaimi’s PE packer TLS implementation notes showing why TLS handling can still be part of runtime-correct staged startup
- ReverseEngineering Stack Exchange discussion on the PE entry point vs user-facing entry distinction

Supporting search/snippet evidence:
- Black Hat unpacking references surfaced by search-layer when direct fetch was degraded

## Changes by file
### `topics/packed-stub-to-oep-and-first-real-module-workflow-note.md`
Added:
- explicit distinction between raw PE entry, raw post-unpack transfer, and first payload-bearing post-startup handoff
- stronger candidate-selection rule for Windows/native packed targets
- a Windows-specific reminder that TLS / CRT / constructor/init scaffolding is usually still startup proof, not yet payload proof
- a new anchor family for raw-transfer -> payload-bearing post-startup handoff
- stronger failure modes and stop rules

### `topics/protected-runtime-practical-subtree-guide.md`
Added a routing reminder that Windows/native packed cases should not collapse raw entry, raw post-unpack transfer, and the first payload-bearing post-startup handoff into one event when startup machinery clearly separates them.

### `topics/anti-tamper-and-protected-runtime-analysis.md`
Updated the parent-page ladder memory so staged-bootstrap handoff now explicitly preserves Windows/native startup-normalization reality.

### `index.md`
Updated branch-balance memory so the protected-runtime ladder now records this sharper packed-startup stop rule as part of the branch’s established practical shape.

## Commit / sync
If KB changes existed, they were committed and then synced with:
- `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

## Best-effort errors logging note
No separate `.learnings/ERRORS.md` entry was required for this run.
The only noteworthy degradation was a direct PDF fetch failure / 403 on one Black Hat source, which was handled conservatively inside the run report rather than treated as a blocking workflow failure.

## Next recommended direction
Prefer not to spend the next run on another tiny wording/index-only repair unless something is actually inconsistent.
Good next external-research-driven candidates include:
- another thin protected-runtime continuation only if it produces equally concrete operator value
- a thinner firmware/protocol practical seam if recent work there has gone quiet
- a practicality-starved branch that can yield one more source-backed workflow note or case note rather than parent-page polish
