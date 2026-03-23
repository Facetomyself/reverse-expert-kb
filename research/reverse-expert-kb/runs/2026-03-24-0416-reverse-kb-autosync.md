# Reverse KB Autosync Run Report

Date: 2026-03-24 04:16 Asia/Shanghai
Mode: external-research-driven
Scope: `research/reverse-expert-kb/`
Primary branch worked: malware practical subtree
Chosen seam: WMI permanent event subscription consumer-proof — consumer-class-specific effect boundaries

## Summary
This run intentionally avoided another internal-only wording / index / branch-shape sync pass.

Recent autosync work had already produced several real external-research-driven runs across protected-runtime and protocol / firmware seams. To keep branch balance healthy and avoid overfeeding those same dense areas, this run targeted a thinner but still practical malware-persistence continuation:
- not whether WMI permanent subscriptions exist in general
- not whether filter / consumer / binding decomposition is already known
- but whether the KB was still too biased toward one downstream proof stereotype: `WmiPrvSe.exe` spawning a child process

The resulting KB improvement was practical and case-driven:
- preserve different downstream effect boundaries for `CommandLineEventConsumer` vs `ActiveScriptEventConsumer`
- prevent analysts from under-proving script-backed WMI persistence just because no obvious child process appears

## Direction review
This run stayed aligned with the reverse KB’s intended direction:
- maintain and improve the KB itself, not just stash links
- keep work practical and case-driven
- prefer a thin operator seam over broad taxonomy or parent-page polish
- add one sharper stop rule that changes analyst behavior in real cases

Why this branch was the right choice now:
- recent runs had already fed protected-runtime and protocol / firmware branches with real external work
- the malware persistence branch had an underfed but still practical continuation available
- the chosen seam could materially strengthen an existing canonical workflow page instead of only creating another source note

## Branch-balance awareness
Current balance judgment after this run:
- **Recently fed enough:** protected-runtime startup / exception-handler seams; protocol / firmware async ownership seams
- **Still easy to overfeed if not careful:** browser/runtime anti-bot or already-dense runtime-evidence branches
- **Good target for this run:** malware persistence, specifically WMI permanent subscription proof quality

Why this seam mattered:
- the WMI note already had the right broad shape: filter -> consumer -> binding -> later effect
- but it still risked implying that later effect should look child-process-centered in all cases
- that bias is operationally wrong for `ActiveScriptEventConsumer`-shaped cases, where script-bearing fields and script-side effects may be the more truthful proof boundary

This made it a good anti-stagnation run:
- real external multi-source search was attempted
- a practical workflow note was materially improved
- the work did not collapse into branch-memory grooming only

## External research performed
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries used:
1. `ActiveScriptEventConsumer WmiPrvSe in-process script execution persistence investigation reverse engineering`
2. `WMI permanent event subscription ActiveScriptEventConsumer ScriptText ScriptFileName WmiPrvSe practical analysis`
3. `CommandLineEventConsumer vs ActiveScriptEventConsumer WmiPrvSe child process reverse engineering proof`

Saved raw search artifact:
- `sources/malware/2026-03-24-wmi-consumer-effect-boundaries-search-layer.txt`

## Sources used conservatively
Primary directly used pages:
- Microsoft Learn — `ActiveScriptEventConsumer` class
- Microsoft Learn — `CommandLineEventConsumer` class
- Elastic — Persistence via WMI Event Subscription

Retained source-backed cues:
- `ActiveScriptEventConsumer` is script-bearing, centered on `ScriptText` / `ScriptFileName`, and associated with `Scrcons.exe`
- `CommandLineEventConsumer` is naturally process-launch-shaped and centered on `ExecutablePath` / `CommandLineTemplate`
- detection/investigation guidance in the ecosystem still preserves both families and, in some environments, `scrcons.exe`-adjacent signals instead of only `WmiPrvSe.exe` child-process evidence

## KB changes made
### New source note
Added:
- `sources/malware/2026-03-24-wmi-consumer-effect-boundaries-notes.md`

Purpose:
- preserve the consumer-class-specific effect-boundary rule
- document why `ActiveScriptEventConsumer` should not inherit the exact same downstream proof expectation as `CommandLineEventConsumer`

### Canonical workflow note materially refined
Updated:
- `topics/malware-wmi-permanent-event-subscription-consumer-proof-workflow-note.md`

Material improvements:
- refined the “right proof object” section so later consequence examples preserve the split between:
  - `CommandLineEventConsumer` -> process-launch-shaped effect proof
  - `ActiveScriptEventConsumer` -> script execution, script-side state change, or `scrcons.exe`-adjacent execution signal
- strengthened Step 5 so analysts pick the later-effect boundary by bound consumer class instead of forcing every case into one child-process model
- strengthened the stop rule around preserving both filter shape and consumer execution model
- widened the later-effect scenario language so the page covers script-consumer-side proof, not only visible `WmiPrvSe.exe` children
- updated hook-placement guidance so `scrcons.exe`-adjacent or script-side effect boundaries are remembered as legitimate anchors
- refreshed source-backed cues to preserve the execution-model split explicitly

### Subtree guide memory updated
Updated:
- `topics/malware-practical-subtree-guide.md`

Change:
- added a malware-branch memory note that the WMI permanent-subscription leaf should not force all proof into `WmiPrvSe.exe` child-process form
- preserved the narrower stop rule that consumer class should shape the chosen effect boundary

## Practical operator value added
This run improved a real analyst stop rule.

Before this refinement, the page still risked nudging readers toward a too-narrow proof expectation:
- “if I cannot show `WmiPrvSe.exe` spawning a child, my WMI proof is weak”

After the refinement, the workflow more honestly supports:
- `CommandLineEventConsumer` cases -> prove launched command path / child-process-shaped effect
- `ActiveScriptEventConsumer` cases -> prove script-bearing fields plus script-side effect or `scrcons.exe`-adjacent execution signal

That is exactly the kind of practical correction the KB should retain:
- small enough to be actionable
- source-backed
- clearly useful in real specimen work
- not just taxonomy growth

## Files changed
- Added: `sources/malware/2026-03-24-wmi-consumer-effect-boundaries-notes.md`
- Added: `sources/malware/2026-03-24-wmi-consumer-effect-boundaries-search-layer.txt`
- Updated: `topics/malware-wmi-permanent-event-subscription-consumer-proof-workflow-note.md`
- Updated: `topics/malware-practical-subtree-guide.md`
- Added: `runs/2026-03-24-0416-reverse-kb-autosync.md`

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

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Notes:
- this run was not Grok-only degraded mode
- the explicit multi-source `search-layer` invocation completed successfully
- direct source fetches succeeded for the Microsoft Learn and Elastic pages needed for the conservative KB update

## Best-effort errors logging note
No `.learnings/ERRORS.md` entry was required for the main workflow.
There was no concrete blocking search/runtime failure in this run.

## Commit / sync status
Plan for this run:
- commit only the reverse-KB files changed by this workflow
- then run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

## Recommended next direction
Do not spend the next run on another tiny wording-only WMI touch-up unless a contradiction appears.
Better next candidates remain:
- another thin malware or desktop/server practical continuation with a similarly concrete proof-object gap
- a source-backed continuation page or workflow note extension on an underfed branch
- avoid collapsing back into canonical-sync-only maintenance unless search/runtime failure forces a KB-only fallback
