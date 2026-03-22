# Reverse KB Autosync Run Report — 2026-03-23 00:16 Asia/Shanghai

Mode: external-research-driven

## Summary
This autosync run performed the required explicit multi-source external search and used it to strengthen a thinner protected-runtime branch with more concrete operator guidance.

The branch itself already existed:
- `topics/exception-handler-owned-control-transfer-workflow-note.md`

So the point of this run was **not** to invent another nearby leaf.
Instead, it improved the KB where the operator value was actually missing:
- making the exception-handler branch more concrete about Windows dispatcher-side ownership boundaries
- clarifying that the first truthful boundary may be `KiUserExceptionDispatcher`, `RtlDispatchException`, unwind lookup, or runtime-installed function-table ownership
- preserving this practical routing inside the protected-runtime subtree guide as well

## Mode rationale
This run counts as external-research-driven because it performed a real explicit multi-source search attempt through `search-layer --source exa,tavily,grok`.

All three requested search sources were actually invoked and succeeded.
A later fetch failure on one downstream page did not invalidate the run; it was recorded conservatively and excluded from synthesis.

## Direction review
This run followed the anti-stagnation rule and the branch-balance rule:
- it did not fall back to another purely internal wording/index/family-count sync
- it chose a thinner practical protected-runtime continuation instead of dense browser/mobile polishing
- it preserved practical operator value rather than inflating taxonomy

Why this direction was selected:
- recent runs were already broadly external-research-driven across multiple branches
- the protected-runtime exception-control-transfer branch was useful but still slightly too abstract at the Windows dispatcher/unwind boundary
- the freshest external evidence supported improving that practical seam more honestly than creating a redundant new page

## Branch balance review
Current balance remains roughly:
- strongest / easiest to overfeed:
  - browser anti-bot / captcha / request-signature workflows
  - mobile protected-runtime / WebView / challenge-loop workflows
- established and worth maintaining with branch awareness:
  - native practical workflows
  - protocol / firmware practical workflows
  - malware practical workflows
  - runtime-evidence practical workflows
  - iOS practical workflows
  - protected-runtime / deobfuscation ladders

This run intentionally fed a thinner protected-runtime seam:
- exception/signal-handler-owned control transfer
- specifically the Windows dispatcher / unwind lookup continuation inside that seam

That choice avoided both branch inflation and internal-only maintenance drift.

## External research performed
Explicit search-layer invocation used the required source selection:
- `exa`
- `tavily`
- `grok`

Queries used:
1. `vectored exception handler control transfer reverse engineering anti debugging`
2. `windows exception dispatcher KiUserExceptionDispatcher RtlDispatchException reverse engineering`
3. `malware VEH anti-debug exception handler control flow analysis`

## Sources used in synthesis
### Successfully used directly
- Microsoft Learn — vectored exception handling
  - <https://learn.microsoft.com/en-us/windows/win32/debug/vectored-exception-handling>
- Momo5502 — A journey through KiUserExceptionDispatcher
  - <https://momo5502.com/posts/2024-09-07-a-journey-through-kiuserexceptiondispatcher/>
- 0xpat — Malware development part 3
  - <https://0xpat.github.io/Malware_development_part_3/>

### Search-surfaced but fetch-degraded / excluded from synthesis
- SonicWall — GuLoader VEH article
  - fetch failed in this environment and was not relied on for KB claims

## KB work performed
### 1. Reviewed branch state and nearby pages
Confirmed that the KB already had:
- a practical exception-handler-owned control-transfer note
- protected-runtime subtree routing for that note

This prevented accidental duplicate-leaf growth.

### 2. Strengthened the existing exception-control-transfer note
Updated `topics/exception-handler-owned-control-transfer-workflow-note.md` to say more concretely that on Windows the first truthful ownership boundary may be:
- vectored registration
- dispatcher-side landing (`KiUserExceptionDispatcher`)
- `RtlDispatchException` / `RtlLookupFunctionEntry` / unwind lookup
- runtime-installed function-table ownership for generated code

The update also added a practical rule:
- if registration exists but still does not explain the hidden branch, move one hop deeper into dispatcher-side landing or unwind lookup rather than broadening into generic anti-debug folklore

### 3. Strengthened subtree routing language
Updated `topics/protected-runtime-practical-subtree-guide.md` so the branch now explicitly remembers that the missing object can be dispatcher-side landing or unwind lookup, not only “handler APIs” in the abstract.

### 4. Added a source note
Added:
- `sources/protected-runtime/2026-03-23-veh-dispatcher-unwind-practical-notes.md`

This preserves the practical external evidence and the conservative stop rule for future continuation.

## Practical value added
The useful improvement is not a new family label.
It is a better stop-and-target rule for real cases:
- do not stop at “the binary uses VEH/SEH”
- pick the smallest re-findable truthful boundary
- registration if it predicts the branch
- otherwise dispatcher-side landing
- otherwise unwind lookup into a concrete region
- otherwise runtime-installed function-table ownership

That makes the branch more actionable and less likely to regress into generic exception theory.

## Files changed
- `research/reverse-expert-kb/topics/exception-handler-owned-control-transfer-workflow-note.md`
- `research/reverse-expert-kb/topics/protected-runtime-practical-subtree-guide.md`
- `research/reverse-expert-kb/sources/protected-runtime/2026-03-23-veh-dispatcher-unwind-practical-notes.md`
- `research/reverse-expert-kb/runs/2026-03-23-0016-exception-dispatcher-boundary-autosync.md`

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
- none at the search-layer stage

### Endpoints used
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

### Fetch-level degradations observed after search
- SonicWall VEH article fetch returned no extractable content in this environment

### Degraded mode assessment
Not degraded at the search-layer level.
The required multi-source search attempt succeeded on all three requested sources.
One later direct-fetch failure was recorded and excluded from synthesis.

## Commit / sync status
- KB changes made: yes
- Commit created: pending at report-write time
- Reverse KB sync script: pending at report-write time

## Best-effort error logging
Per workflow policy, `.learnings/ERRORS.md` logging remained best-effort only and was not required for run completion.

## Next useful follow-up candidates
Good future follow-ups if stronger source pressure appears:
- a narrower page-guard / debug-register / single-step continuation only if multiple case-backed sources justify it
- a later privileged anti-cheat / callback-heavy dispatcher continuation if it stays practical and case-driven
- additional protected-runtime branch review only when it helps route to a quieter post-handler target, not to inflate exception taxonomy
