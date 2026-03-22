# Reverse KB Autosync Run Report — 2026-03-22 20:16 Asia/Shanghai

Mode: external-research-driven

## Summary
This autosync run intentionally avoided another internal canonical-sync-only pass and instead performed a real explicit multi-source search on a thinner protected-runtime / deobfuscation branch.

The chosen gap was a practical middle-stage workflow that the KB was still under-modeling:
- flattening is already recognizable
- the dispatcher or state carrier is already partially visible
- but the **next-state relation** is still obscured by opaque predicates, copied-code branch inflation, helper-mediated writes, or computed-next-state machinery

The main KB outcome was a new practical continuation note:
- `topics/opaque-predicate-and-computed-next-state-recovery-workflow-note.md`

This fills the branch gap between:
- `vm-trace-to-semantic-anchor-workflow-note.md`
- `flattened-dispatcher-to-state-edge-workflow-note.md`

rather than letting the branch jump too abruptly from “find an anchor” to “reduce a durable state edge.”

## Why this direction was chosen
Recent runs in the same window already fed multiple branches, including some canonical-sync repair work and thinner practical leaves in native, malware, protocol, runtime, and mobile areas.

The anti-stagnation review for this run showed a real maintenance risk on the deobfuscation/protected-runtime side:
- the branch already had good pages for VM/trace anchoring and flattened dispatcher reduction
- but it still under-described the stubborn operator case where the analyst can already see flattening, yet still cannot recover a trustworthy successor relation because next-state computation is obscured
- that made the branch feel slightly too eager to skip from broad protected churn into later state-edge reduction without preserving the actual bridge analysts often fight through in OLLVM/Tigress-shaped work

This was a good target because:
- it is thinner than the heavily fed browser/mobile practical branches
- it is still strongly practical and case-driven
- it directly improves the KB itself, not just source notes
- it uses external research pressure to produce a concrete workflow continuation page, not only index wording

## Branch-balance review
### Before this run
The protected-runtime deobfuscation ladder already had:
- broad protected-runtime subtree routing
- VM / trace -> semantic-anchor reduction
- flattened dispatcher -> durable state-edge reduction
- packed/bootstrap handoff
- runtime-artifact/init-obligation and integrity consequence continuations

But it still had a practical bridge weakness:
- it did not preserve the middle case where one dispatcher/state carrier is already visible, but next-state recovery itself is still obstructed by opaque predicates, copied-code inflation, helper-mediated writes, or computed-target selection

### Balance decision
This run therefore chose to feed a thinner practical continuation on the protected-runtime ladder, rather than:
- adding another dense browser/mobile leaf
- doing another top-level wording/count sync
- or widening the broad deobfuscation synthesis page without preserving operator workflow

## External research performed
A real explicit search-layer run was executed with the required source selection:
- `exa`
- `tavily`
- `grok`

Queries used:
1. `control flow flattening deobfuscation opaque predicate symbolic execution practical workflow binary ninja angr miasm`
2. `OLLVM control flow flattening opaque predicate removal practical reverse engineering workflow`
3. `Tigress control flow flattening opaque predicates dynamic symbolic execution reverse engineering`

Raw search capture saved to:
- `sources/obfuscation-deobfuscation/2026-03-22-opaque-predicate-search-layer.txt`

A practical source note was also written:
- `sources/obfuscation-deobfuscation/2026-03-22-opaque-predicate-and-cff-practical-sources.md`

## Sources used in synthesis
### Successfully used in synthesis
- OpenAnalysis — angr control-flow deobfuscation notes
- Tigress docs — `Flatten`
- Tigress docs — `AddOpaque`
- d0minik — Binary Ninja control-flow unflattening write-up
- `cdong1012/ollvm-unflattener`

### Search-discovered / cited but fetch-degraded
- Quarkslab — `Deobfuscation: recovering an OLLVM-protected program`
  - direct `web_fetch` degraded in this environment (`429` / Vercel security checkpoint)
- Reverse Engineering Stack Exchange thread on OLLVM deobfuscation
  - direct `web_fetch` degraded in this environment (`403` / anti-bot interstitial)

These fetch degradations did not block the run because the required multi-source search attempt succeeded first and sufficient practical material remained available from the other sources.

## Work performed
### 1. Reviewed branch state and recent run mix
Checked recent autosync reports to avoid drifting into another internal-only maintenance pass and to ensure this run would still satisfy the anti-stagnation requirement with a real external-research-driven attempt.

### 2. Re-ran explicit multi-source search
Used `search-layer --source exa,tavily,grok` with deobfuscation / opaque-predicate / CFF workflow queries.

### 3. Collected practical source-backed deobfuscation signals
Preserved source-backed operator signals showing that:
- dispatch form diversity matters (`switch`, `goto`, `indirect`, `call`)
- opaque predicates and copied-code branches often block direct next-state extraction even after the dispatcher is recognizable
- practical unflattening commonly relies on one smaller trustworthy successor relation, not immediate perfect whole-function recovery
- symbolic execution and IL repair often serve as narrow bridge tools, not all-or-nothing solutions

### 4. Added a new practical continuation page
Created:
- `topics/opaque-predicate-and-computed-next-state-recovery-workflow-note.md`

The new note preserves a thinner operator ladder for this specific case:

```text
recognizable dispatcher / state carrier
  -> classify how next-state computation is obscured
  -> choose one smaller trustworthy state carrier
  -> normalize or solve one successor relation
  -> prove one OBB/state or state/successor edge
  -> decide whether CFG repair or deeper cleanup is now worth it
```

### 5. Synced nearby parent / routing pages
Updated:
- `topics/protected-runtime-practical-subtree-guide.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `index.md`

The practical effect was to make the branch remember that:
- there is now a distinct opaque-predicate / computed-next-state bridge page
- flattened-dispatcher reduction should start only after at least one trustworthy successor relation already exists
- the deobfuscation parent should explicitly preserve this middle-stage workflow instead of compressing it away

## KB changes
### Added
- `topics/opaque-predicate-and-computed-next-state-recovery-workflow-note.md`
- `sources/obfuscation-deobfuscation/2026-03-22-opaque-predicate-and-cff-practical-sources.md`
- `runs/2026-03-22-2016-opaque-predicate-next-state-recovery-autosync.md`

### Updated
- `topics/protected-runtime-practical-subtree-guide.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `index.md`

## Practical value added
The useful result is not just “more deobfuscation content.”
It is that the KB now preserves a more realistic practical ladder for protected / flattened targets:
- VM / trace anchoring when the first semantic anchor is still missing
- **opaque-predicate / computed-next-state recovery** when flattening is recognizable but successor recovery is still obscured
- flattened-dispatcher / durable-state-edge reduction once one trustworthy successor relation already exists

That is a more truthful operator progression than forcing all such cases into either broad trace churn or later state-edge reduction.

## Direction review
This run stayed aligned with the autosync policy:
- it did not rely on implicit/default search-source selection
- it used explicit `search-layer --source exa,tavily,grok`
- it did not treat Grok-only execution as normal mode
- it produced a concrete source-backed practical continuation page instead of only top-level wording/index repair
- it biased toward a thinner protected-runtime branch rather than another convenient dense browser/mobile slot

It also respected the anti-stagnation rule by making a real external-research-driven pass and turning it into a KB improvement with operator value.

## Search audit
### Requested sources
- Exa
- Tavily
- Grok

### Succeeded sources
- Exa
- Tavily
- Grok

### Failed sources
- none at the search-layer source-selection stage

### Endpoints used
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

### Fetch-level degradations observed after search
- Quarkslab article fetch: `429` / Vercel security checkpoint
- Reverse Engineering Stack Exchange fetch: `403` / anti-bot interstitial

### Degraded mode assessment
Not degraded at the search-layer level.
The required multi-source search was attempted explicitly and succeeded on all three requested sources.
Later fetch degradation affected only two downstream pages and was recorded conservatively.

## Commit / sync status
KB changes were made and should be committed.
After committing, run:
- `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

## Best-effort error logging
Per workflow policy, `.learnings/ERRORS.md` logging was treated as best-effort only and was not required for run completion.

## Next useful follow-up candidates
Good follow-ups if this branch gets revisited under fresh source pressure:
- a narrower call-dispatch / arg-struct state-carrier continuation for Tigress-like outlined-block flattening
- a table-index / indirect-dispatch recovery continuation focused on computed target families
- a compare-run note for validating one recovered successor relation before aggressive CFG repair

For this run, the highest-value move was preserving the missing middle step in the deobfuscation ladder itself.
