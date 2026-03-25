# Reverse KB Autosync Run Report

Date: 2026-03-25 11:16 Asia/Shanghai
Mode: external-research-driven
Scope: `research/reverse-expert-kb/`
Primary branch worked: malware practical subtree
Chosen seam: Windows service recovery-action slot selection — separating recovery presence, failure-count/reset-window state, and exact selected action

## Summary
This run intentionally avoided another KB-internal wording/count/index-only maintenance pass.

Recent autosync history already fed several other branches. To stay anti-stagnation-safe and branch-balance-aware, this run performed a real external research pass on a thinner malware practical seam that already existed in the KB but still had one under-preserved analyst mistake:
- proving that service recovery exists
- or proving that a service failed
- but still flattening the later effect into vague wording like “SCM restarted it” or “recovery ran a command”
- without preserving which recovery slot actually fired under which reset-window semantics

The practical gap was this:
- failure-action cases were already treated as real persistence contracts
- but the branch still risked under-preserving the narrower distinction between:
  - recovery presence
  - failure-count truth
  - reset-window truth
  - action-selection truth
  - effect truth

That gap matters because a durable malware effect can depend on:
- only the first failure
- only later failures
- last-slot repetition after action-array overflow
- or whether `dwResetPeriod` kept the case inside one failure series versus resetting it

This run therefore did a real explicit `exa,tavily,grok` search pass and refined the malware service-failure continuation around a sharper stop rule:
- do not stop at “failure actions exist”
- do not stop at “the service failed”
- do not stop at generic “SCM restarted it” wording
- preserve recovery presence, failure-count/reset-window state, and exact recovery-slot selection separately before attributing later durable behavior to SCM-owned restart or run-command effects

This is a KB improvement, not just source collection:
- the canonical service-failure workflow note is materially sharper
- the malware subtree guide now preserves the same stop rule at branch-memory level
- the malware parent framing now preserves the same service-recovery caution so it does not live only in the leaf note
- the top-level index now preserves this branch-memory distinction as part of the practical malware route

## Direction review
This run stayed aligned with the reverse KB’s intended direction:
- maintain and improve the KB itself, not just collect notes
- keep work practical and case-driven
- improve a real operator stop rule
- bias toward a thinner practical seam on an underfed branch rather than easy dense-branch polishing

Why this branch was the right choice now:
- malware remains one of the KB’s stronger operator-value branches, but service failure-action semantics are still thinner than more frequently touched mobile/protected-runtime/browser seams
- the existing workflow note already had enough structure to support a source-backed refinement instead of spawning another detached note for the same family
- this refinement changes how a real analyst handles restart loops and `SC_ACTION_RUN_COMMAND` cases, rather than only polishing wording
- it also satisfies the anti-stagnation rule by being a real external-research-driven run inside the rolling window

## Branch-balance awareness
Current balance judgment after this run:
- **Still easy to overfeed:** browser challenge/anti-bot continuations; already-dense protected-runtime seams
- **Recently improved enough to keep coherent:** Scheduled Job conditions/history distinction; several non-malware continuity seams from prior runs
- **Good target for this run:** malware service persistence, specifically recovery-action slot selection and reset-window semantics

Why this seam mattered:
- the service-failure branch already preserved recovery as a first-class contract
- but it still risked flattening slot selection into generic restart/crash narration
- a small source-backed refinement here changes real operator judgment in restart-loop and run-command persistence cases
- that is better practical value than another internal canonical-sync-only pass

## External research performed
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries used:
1. `Windows service failure actions SC_ACTION_RUN_COMMAND recovery options dwResetPeriod malware persistence analysis`
2. `SERVICE_FAILURE_ACTIONS_FLAG non crash failures SERVICE_STOPPED dwWin32ExitCode service recovery`
3. `Windows service recovery actions restart run command analysis persistence SCM failure count reset period`

Saved raw search artifact:
- `sources/malware/2026-03-25-service-recovery-action-selection-search-layer.txt`

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

Degraded-source note:
- This run explicitly attempted all three requested sources.
- Grok returned explicit `502 Bad Gateway` failures during invocation.
- Exa and Tavily returned enough usable material to continue conservatively.
- This therefore counts as a real multi-source external-research attempt under a degraded source set, not as normal mode.

## Sources used conservatively
Primary retained sources:
- Microsoft Learn — `SERVICE_FAILURE_ACTIONSW`
- Microsoft Learn — `SERVICE_FAILURE_ACTIONS_FLAG`
- Microsoft Learn (archived) — `sc failure`
- Stephen Cleary — `Win32 Service Gotcha: Recovery Actions` (supporting practitioner cue only)

Retained source-backed cues:
- `SERVICE_FAILURE_ACTIONS` preserves a stored recovery contract with `dwResetPeriod`, `lpCommand`, `cActions`, and `lpsaActions`
- failure-action presence is not yet action-selection truth
- `dwResetPeriod` resets the failure count only after an error-free interval, so reset-window state is its own proof layer
- if failure count exceeds `cActions`, SCM repeats the last configured action
- `SERVICE_FAILURE_ACTIONS_FLAG` determines whether non-crash failures that report `SERVICE_STOPPED` with non-zero `dwWin32ExitCode` also queue recovery actions
- `SC_ACTION_RUN_COMMAND` should be treated as one selected recovery slot with one attributable later effect, not as vague service-recovery capability narration

## KB changes made
### New source note
Added:
- `sources/malware/2026-03-25-service-recovery-action-selection-notes.md`

Purpose:
- preserve the narrower operator rule around recovery presence vs failure-count/reset-window/action-selection truth
- explicitly record the degraded search-source set

### Canonical workflow note materially refined
Updated:
- `topics/malware-service-failure-action-and-timeout-abuse-workflow-note.md`

Material improvements:
- strengthened the recovery-analysis stop rule so **reset-window truth** is preserved alongside failure existence, failure count, action selection, and effect truth
- clarified that long restart loops may be **last-slot repetition** rather than repeated fresh action selection
- tightened the default proof recipe so analysts verify whether `dwResetPeriod` keeps the case inside the same sequence or should have reset the count
- strengthened source-backed practical cues so the branch remembers that slot selection is a real proof boundary, not just configuration trivia

### Malware subtree guide updated
Updated:
- `topics/malware-practical-subtree-guide.md`

Change:
- added subtree-memory that the service-failure / timeout-abuse leaf should preserve recovery presence, failure-count/reset-window state, exact selected recovery slot, and later effect separately
- added a compact ladder memory line so this does not live only in the leaf workflow note

### Malware parent framing updated
Updated:
- `topics/malware-analysis-overlaps-and-analyst-goals.md`

Change:
- added parent-page memory that service-recovery-shaped persistence cases should preserve recovery presence, failure-count/reset-window state, and exact selected recovery slot before attributing durable behavior to SCM-owned restart or run-command effects

### Top-level branch memory updated
Updated:
- `index.md`

Change:
- the malware practical branch entry for service failure-action / timeout-abuse continuation now preserves the same action-selection distinction so it does not live only in one leaf note

## Practical operator value added
This run improved a real analyst stop rule.

Before this refinement, the branch could still permit a slightly too-flat reading:
- “the service has recovery configured, it failed, so this later restart/run-command effect is probably just service recovery doing its thing.”

After the refinement, the branch more honestly supports:
- **recovery presence truth** -> what contract exists
- **failure-count truth** -> which failure attempt this is
- **reset-window truth** -> whether SCM is still in the same sequence
- **action-selection truth** -> which configured slot should fire now
- **effect truth** -> what later restart/command proves that exact slot mattered

That changes real case handling:
- repeated restart loops are less likely to be narrated as generic “keeps restarting” noise
- `SC_ACTION_RUN_COMMAND` paths are less likely to be described as generic service lore instead of one selected slot
- analysts are less likely to overattribute a late effect to the wrong failure number or wrong recovery action
- restart-loop timing can be judged against `dwResetPeriod` and last-slot repetition rather than vague crash folklore

This is practical operator value:
- narrow enough to apply in a real Windows persistence investigation
- source-backed enough to retain conservatively
- materially improves a canonical workflow page instead of only adding detached notes

## Files changed
Added:
- `sources/malware/2026-03-25-service-recovery-action-selection-notes.md`
- `runs/2026-03-25-1116-reverse-kb-autosync.md`

Updated:
- `topics/malware-service-failure-action-and-timeout-abuse-workflow-note.md`
- `topics/malware-practical-subtree-guide.md`
- `topics/malware-analysis-overlaps-and-analyst-goals.md`
- `index.md`

Saved raw search artifact:
- `sources/malware/2026-03-25-service-recovery-action-selection-search-layer.txt`

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

The KB now preserves a sharper rule for Windows service recovery-action cases:
- do not flatten recovery presence, current failure sequence, and exact selected recovery slot into one generic claim
- classify **recovery presence truth**, **failure-count truth**, **reset-window truth**, **action-selection truth**, and **effect truth** separately
- then choose the next proof boundary based on which of those layers is still actually missing
