# Reverse Expert KB Autosync Run Report

- Time: 2026-03-21 20:16 Asia/Shanghai / 2026-03-21 12:16 UTC
- Mode: external-research-driven
- Focus branch: protected-runtime practical branch
- Focus gap: exception/signal-handler-owned control transfer as a thinner protected-runtime continuation

## Why this run
Recent same-day protected-runtime work already added anti-instrumentation gate triage and related branch synchronization. Under the anti-stagnation rule, this run should not fall back into another internal wording/index/family-count-only pass.

This run therefore prioritized a real external-research attempt and a thinner, still-practical seam:
- cases where ordinary direct control flow stays incomplete or misleading
- traps, faults, breakpoints, unwind lookup, or signal delivery may own the meaningful branch
- the missing KB help is not another anti-debug taxonomy page, but one compact workflow for recovering the first handler-owned transfer boundary and one consequence-bearing resume/state action

That is operator-useful because many real cases stall after broad anti-debug suspicion:
- analysts see `int3`, VEH/SEH, signal registration, or odd crash/resume behavior
- but the next useful object is still unclear
- the case then drifts either into platform-mechanism reading or into premature topology changes

The missing middle move is to prove one handler-owned transfer path and hand back one quieter post-handler target.

## Direction review
This run deliberately kept the KB practical and case-driven:
- it did not spend the slot on another top-level protected-runtime rewrite
- it did not overfeed browser/mobile branches
- it did not stop at branch-balance wording or index-only maintenance

The addition preserves the KB’s preferred direction:
- concrete workflow note rather than broad family inflation
- recovery of one ownership boundary, one context/state consequence, and one ordinary continuation target
- conservative, source-backed synthesis without overclaiming prevalence

## Branch-balance review
Current branch-balance picture:
- browser/mobile remain easier to overfeed with dense-source polishing
- protocol/malware already received substantive same-day work
- protected-runtime still benefits from selective growth when the new page is a real operator rung rather than another broad category page

Why this branch was chosen now:
- handler-owned transfer is thinner than the already stronger observation-topology and broad anti-instrumentation surfaces
- it has clear practical value for protected targets whose real branch hides in exception/signal ownership
- it satisfies the anti-stagnation rule by producing a real source-backed continuation page rather than more canonical-sync-only maintenance

## External research performed
This run attempted explicit multi-source search through `search-layer` with:
- `--source exa,tavily,grok`

Queries used:
1. `reverse engineering exception based anti debug SEH signal handler workflow`
2. `anti debug signal handler ptrace seccomp exception based reverse engineering`
3. `protected runtime exception handler anti tamper reverse engineering practical`
4. `Windows SEH VEH anti debugging reverse engineering exception handler`
5. `Linux signal handler anti debugging reverse engineering SIGTRAP SIGSEGV`
6. `exception based anti debugging reverse engineering SEH VEH signal handler`

Supporting direct fetches then focused on:
- Microsoft VEH documentation
- Microsoft SEH documentation
- focused practitioner writeups on exception internals and x64 unwind metadata
- a practical trap-triggered VEH/SEH hook demo
- one Linux ptrace anti-RE writeup plus one RE.SE discussion as light cross-check material

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
- none recorded at search-layer level for this run

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Audit artifacts:
- `sources/protected-runtime/2026-03-21-exception-handler-owned-control-transfer-notes.md`
- `/tmp/reverse-kb-search-20260321-2016.json` (ephemeral local search output)
- `/tmp/reverse-kb-search-20260321-2016b.json` (ephemeral local search output)

## KB changes made
### New page
Added:
- `topics/exception-handler-owned-control-transfer-workflow-note.md`

What it contributes:
- a practical workflow for cases where visible direct control flow stays incomplete because exception/signal ownership may own the real branch
- explicit separation among:
  - VEH-first global dispatch
  - SEH/unwind-local transfer
  - dynamic function-table/generated-code exception ownership
  - Linux signal-handler-owned transfer
  - trap-triggered hook / anti-debug dispatch
- a disciplined workflow centered on:
  - smallest trap/fault symptom
  - one ownership boundary
  - one consequence-bearing context/state action
  - one quieter post-handler target

### New source note
Added:
- `sources/protected-runtime/2026-03-21-exception-handler-owned-control-transfer-notes.md`

What it preserves:
- search framing and explicit multi-source accounting
- retained signals from official docs and practitioner writeups
- conservative synthesis boundaries
- rationale for choosing this thinner practical continuation

### Canonical synchronization updates
Updated:
- `topics/protected-runtime-practical-subtree-guide.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `index.md`

What was synchronized:
- protected-runtime practical subtree now includes handler-owned control transfer as an explicit recurring bottleneck
- branch ladder expanded from eight to nine recurring bottlenecks
- anti-tamper/protected-runtime synthesis now lists both anti-instrumentation gate triage and the new exception/signal-handler-owned transfer continuation
- top-level index now preserves the new protected-runtime practical rung canonically

## Practical outcome
The KB now has a better answer for a recurring protected-runtime stall point:
- the target appears anti-debug or structurally odd
- ordinary direct call flow does not explain later execution
- the real next task is to prove whether handlers/signals actually own the branch and, if so, where execution resumes or diverts afterward

That is more useful than another generic SEH/VEH explainer because it tells the analyst what evidence object to recover next:
- one registration or lookup boundary
- one context/state consequence
- one post-handler target

## Files changed this run
- `topics/exception-handler-owned-control-transfer-workflow-note.md`
- `sources/protected-runtime/2026-03-21-exception-handler-owned-control-transfer-notes.md`
- `topics/protected-runtime-practical-subtree-guide.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `index.md`
- `runs/2026-03-21-2016-exception-handler-owned-control-transfer-autosync.md`

## Commit / archival sync
If the diff remains KB-local:
1. commit KB changes in `research/reverse-expert-kb/`
2. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

This run should stage only the KB-local files above.

## Best-effort error logging
No `.learnings/ERRORS.md` update was required for the success path of this run.
Any source-quality limitations were recorded inside the source note and run report, which is sufficient for this run.

## Bottom line
This run satisfied the external-research-driven requirement and used that slot to improve a thinner protected-runtime branch with real operator value.

The KB is now better balanced in one specific way:
- it no longer has to jump directly from broad anti-debug suspicion to broader topology or integrity continuations
- there is now a concrete middle rung for proving that handlers/signals own the real branch and for handing the case back to an ordinary target with less guesswork.