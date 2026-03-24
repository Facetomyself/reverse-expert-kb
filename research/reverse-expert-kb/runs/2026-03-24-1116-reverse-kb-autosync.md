# Reverse KB Autosync Run Report

Date: 2026-03-24 11:16 Asia/Shanghai
Mode: external-research-driven
Scope: `research/reverse-expert-kb/`
Primary branch worked: malware practical subtree
Chosen seam: PowerShell Scheduled Job persistence — separating definition truth, conditions truth, and history truth

## Summary
This run intentionally avoided another index-only / wording-only / family-count sync pass.

Recent runs already fed iOS and WMI practical continuations with real external work. To stay inside the anti-stagnation rule and branch-balance rule, this run targeted a thinner but still practical malware continuation that was already present in the KB:
- not broad Scheduled Task persistence
- not broad PowerShell Scheduled Job explanation
- but one narrower analyst mistake inside the existing PowerShell Scheduled Job note

The practical gap was this:
- once analysts localize `ScheduledJobDefinition.xml`, they can still flatten three different truths into one vague claim:
  - what the persisted definition says
  - whether current host conditions allow execution now
  - whether historical output proves earlier runs

That flattening is operationally bad because it can turn:
- a battery / idle / network / wake / demand-start / instance-policy gate
into
- the false conclusion that the persisted malware path is not real

This run therefore did a real external search pass and refined the malware PowerShell Scheduled Job continuation around a sharper stop rule:
- preserve **definition truth**, **conditions truth**, and **history truth** separately before deciding whether a present-day no-run weakens or does not weaken the persistence claim

This is a KB improvement, not just source collection:
- the canonical PowerShell Scheduled Job workflow note is materially sharper
- the malware subtree guide now preserves the same stop rule at branch-memory level
- the top-level index now preserves the same branch-balance memory so this logic does not live only in one leaf
- a prior duplication/corruption artifact at the tail of the Scheduled Job note was also cleaned while updating the page

## Direction review
This run stayed aligned with the reverse KB’s intended direction:
- maintain and improve the KB itself, not just collect notes
- keep work practical and case-driven
- improve a real operator stop rule
- prefer a thin continuation on an underfed-enough branch over easy dense-branch polishing

Why this branch was the right choice now:
- malware practical work is established enough that narrower persistence refinements now have operator value
- browser/mobile/protected-runtime remain easier to overfeed than this seam
- the existing Scheduled Job note already had enough structure to support a source-backed refinement instead of another detached leaf
- recent runs had already covered other branches, so this was branch-balance-safe and anti-stagnation-safe

## Branch-balance awareness
Current balance judgment after this run:
- **Still easy to overfeed:** browser anti-bot / challenge-loop continuations; already-dense mobile protected-runtime seams
- **Recently improved enough to keep coherent:** iOS Swift-concurrency continuation seam; malware WMI consumer-class proof seam
- **Good target for this run:** malware persistence, specifically PowerShell Scheduled Job proof quality when current no-run behavior risks being overread

Why this seam mattered:
- the Scheduled Job continuation was already practical, but still slightly too flat around options/history interpretation
- a small source-backed refinement here changes how a real analyst judges “definition found, but no run right now” cases
- that is better operator value than another top-level wording repair

## External research performed
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries used:
1. `PowerShell ScheduledJob ScheduledJobDefinition.xml Results.xml Status.xml conditions reverse engineering malware persistence`
2. `PowerShell about_Scheduled_Jobs about_Scheduled_Jobs_Advanced ScheduledJobOptions results history conditions`
3. `Register-ScheduledJob ScheduledJobOptions network idle battery wake run history practical analysis`

Saved raw search artifact:
- `sources/malware/2026-03-24-scheduled-job-conditions-history-search-layer.txt`

## Search audit
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- exa
- tavily

Failed sources:
- grok

Endpoints used on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Degraded-mode note:
- This run explicitly attempted all three requested sources.
- Grok returned explicit `502 Bad Gateway` failures during invocation.
- Exa and Tavily returned enough usable material to continue conservatively.
- This therefore counts as a real multi-source external-research attempt under a degraded source set, not as normal Grok-only mode.

## Sources used conservatively
Primary retained sources:
- Microsoft Learn — `about_Scheduled_Jobs`
- Microsoft Learn — `about_Scheduled_Jobs_Advanced`
- Microsoft Learn — `New-ScheduledJobOption`
- Microsoft Learn — `Set-ScheduledJobOption`
- Microsoft Learn — `Get-ScheduledJobOption`
- Splunk Research — `Detection: Windows PowerShell WMI Win32 ScheduledJob` (supporting only)

Retained source-backed cues:
- scheduled jobs are a hybrid of PowerShell jobs and Task Scheduler tasks, so task-only views are not the whole truth once PSScheduledJob machinery appears
- scheduled jobs persist under `$HOME\AppData\Local\Microsoft\Windows\PowerShell\ScheduledJobs`, with `ScheduledJobDefinition.xml` and timestamped `Output\<time>\Results.xml` / `Status.xml`
- scheduled jobs run only when all configured conditions are satisfied; practical conditions include network, idle, battery, wake, demand-start, and multiple-instance policy
- historical output and execution-history retention are their own proof surface and should not be conflated with present-day eligibility
- `Start-Job -DefinitionName` creates an ordinary background job instance, not a scheduled execution instance, and its output is not written into the scheduled job output directory

## KB changes made
### New source note
Added:
- `sources/malware/2026-03-24-scheduled-job-conditions-history-notes.md`

Purpose:
- preserve the narrower operator rule around definition vs conditions vs history
- explicitly record the degraded search-source set

### Canonical workflow note materially refined
Updated:
- `topics/malware-powershell-scheduled-job-consumer-proof-workflow-note.md`

Material improvements:
- replaced the too-flat “reduce the definition into one runnable object” framing with an explicit three-way split:
  - definition truth
  - conditions truth
  - history truth
- added a practical stop rule preventing analysts from collapsing these into one generic “scheduled job exists” claim
- strengthened acceptable proof forms so present-day no-run can be explained by options/conditions without invalidating the persisted definition
- added a concrete scenario for options/conditions-gated no-run behavior
- added a concrete scenario for thinned/cleared/rolled-over execution history
- preserved a stronger anti-mistake rule around `Start-Job -DefinitionName` not counting as equivalent historical scheduled-run proof
- cleaned duplicated/corrupted tail text left in the page from an earlier edit state

### Malware subtree guide updated
Updated:
- `topics/malware-practical-subtree-guide.md`

Change:
- added subtree-memory that when a Scheduled Task case narrows into PowerShell Scheduled Job persistence, analysts should keep definition truth, conditions truth, and history truth separate

### Top-level branch memory updated
Updated:
- `index.md`

Change:
- the branch-balance memory for malware practical workflows now preserves the same Scheduled Job distinction so it does not live only in one leaf note

## Practical operator value added
This run improved a real analyst stop rule.

Before this refinement, the branch could still nudge readers toward a slightly too-flat interpretation:
- “I found the scheduled job definition, so if it is not firing now, maybe this persistence path is weak or fake.”

After the refinement, the branch more honestly supports:
- **definition truth** -> what malware persisted
- **conditions truth** -> why it can or cannot execute now under current host state
- **history truth** -> whether it executed before under earlier conditions

That changes real case handling:
- battery / idle / network / wake conditions no longer automatically downgrade the persisted definition
- sparse `Output` history no longer automatically means “never mattered”
- manual `Start-Job -DefinitionName` testing is less likely to be mistaken for equivalent proof of historical scheduled execution

This is practical operator value:
- narrow enough to apply in a real Windows persistence investigation
- source-backed enough to retain conservatively
- materially improves a canonical workflow page instead of just polishing wording

## Files changed
Added:
- `sources/malware/2026-03-24-scheduled-job-conditions-history-notes.md`
- `runs/2026-03-24-1116-reverse-kb-autosync.md`

Updated:
- `topics/malware-powershell-scheduled-job-consumer-proof-workflow-note.md`
- `topics/malware-practical-subtree-guide.md`
- `index.md`

Saved raw search artifact:
- `sources/malware/2026-03-24-scheduled-job-conditions-history-search-layer.txt`

## Best-effort errors logging note
No `.learnings/ERRORS.md` entry was required for the main workflow.
Search degradation was captured directly in this run report’s Search audit section and was not treated as a blocking workflow error.

## Commit / sync status
Plan for this run:
1. commit the reverse-KB files changed by this workflow
2. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
3. leave this run report as the archival record

## Bottom line
This was a real external-research-driven maintenance run on a thinner but practical malware persistence seam.

The KB now preserves a sharper rule for PowerShell Scheduled Job cases:
- do not flatten persisted definition, current eligibility, and historical execution into one claim
- classify **definition truth**, **conditions truth**, and **history truth** separately
- then choose the next proof boundary based on which of those layers is actually missing
