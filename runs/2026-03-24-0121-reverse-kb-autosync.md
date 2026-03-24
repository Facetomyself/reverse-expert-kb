# Reverse Expert KB Autosync Run Report

Date: 2026-03-24 09:16 Asia/Shanghai / 2026-03-24 01:16 UTC
Mode: external-research-driven
Scope: `research/reverse-expert-kb/`
Primary branch worked: protected-runtime practical subtree
Chosen seam: exception-handler-owned control transfer — dynamic unwind ownership and signal-context resume stop rule

## Why this seam
Recent runs were already doing real external passes, so this run avoided another internal-only index/family-count sync.
The protected-runtime subtree remains thinner and more operator-fragile than native/browser/mobile in one specific place:
- exception/signal-owned transfer had a good page already,
- but its practical stop rule was still softer than it should be.

This run therefore targeted a case-driven continuation instead of broad wording polish:
- when dispatcher landing is useful but still only infrastructure,
- when dynamic function-table ownership is the truthful Windows anchor,
- and when Linux `SA_SIGINFO` / `ucontext_t` resume mutation is the truthful signal-side proof object.

## External research pass
I ran explicit multi-source search through `search-layer` with:
- requested sources: `exa,tavily,grok`
- queries around:
  - `RtlInstallFunctionTableCallback` / `RtlLookupFunctionEntry` / generated-code unwind ownership
  - `KiUserExceptionDispatcher` / `RtlDispatchException` practical anchors
  - Linux `sigaction` / `SA_SIGINFO` / `ucontext_t` / resume-address control transfer

I then cross-checked the search output with direct fetches of:
- Microsoft Learn: `RtlInstallFunctionTableCallback`
- Microsoft Learn: `RtlLookupFunctionEntry`
- man7: `sigaction(2)`

## KB changes made
### 1. Tightened `topics/exception-handler-owned-control-transfer-workflow-note.md`
Materially improved the workflow note with a sharper practical routing rule:
- expanded the opening refinement from Windows-only to Windows/Linux
- added an explicit infrastructure-vs-proof stop rule
- clarified that dispatcher landing alone and `sigaction` registration alone are still infrastructure
- required one runtime-owned lookup range or one concrete context/resume mutation before treating the case as reduced enough to hand off
- strengthened the dynamic-function-table family with `RtlLookupFunctionEntry` recurrence and runtime-added-range language
- strengthened the Linux signal family with explicit `SA_SIGINFO` / `ucontext_t` framing and resume-target mutation language

### 2. Tightened `topics/protected-runtime-practical-subtree-guide.md`
Updated the branch guide so the exception-handler seam is easier to enter from real cases:
- added a concrete routing cue for recurring `KiUserExceptionDispatcher` / `RtlDispatchException` / `RtlLookupFunctionEntry` without stable static ownership
- added the Linux-side cue where `sigaction` / `SA_SIGINFO` is visible but the missing proof object is still the resume target or `ucontext_t` mutation

### 3. Archived the source-backed continuation
Added:
- `sources/protected-runtime/2026-03-24-exception-owned-control-transfer-source-note.md`

This source note preserves the practical research synthesis rather than leaving the rationale trapped in the run report.

## Direction review
This run stayed aligned with the anti-stagnation rule:
- not an internal canonical-sync-only pass
- not just wording/index/family-count repair
- real multi-source external research was attempted and succeeded across all requested sources
- the output was a practical continuation tightening a real operator stop rule in an underfed branch

This also stays aligned with the reverse-KB direction bias:
- concrete workflow note improvement
- code-adjacent seams (`RtlLookupFunctionEntry`, runtime function tables, `sigaction`, `SA_SIGINFO`, `ucontext_t`)
- emphasis on first truthful ownership / consequence object rather than taxonomy expansion

## Branch-balance review
Recent runs have been active across native desktop, iOS, malware, and protocol/firmware.
This run deliberately reinforced the protected-runtime subtree, which remains important but comparatively less fed.

Balance judgment for this run:
- good branch diversification relative to the last several runs
- practical value remained high because the edited seam is a recurrent analyst failure mode
- no need this run for top-level subtree reshaping; the best ROI was a thinner practical continuation

## Files changed
- `topics/exception-handler-owned-control-transfer-workflow-note.md`
- `topics/protected-runtime-practical-subtree-guide.md`
- `sources/protected-runtime/2026-03-24-exception-owned-control-transfer-source-note.md`

## Search audit
Requested sources: exa, tavily, grok
Succeeded sources: exa, tavily, grok
Failed sources: none observed in this run
Endpoints used:
- Exa: http://158.178.236.241:7860
- Tavily: http://proxy.zhangxuemin.work:9874/api
- Grok: http://proxy.zhangxuemin.work:8000/v1

## Outcome
This run materially improved the KB itself.
The protected-runtime exception-handler seam now has a cleaner practical stop rule:
- Windows: treat recurring dispatcher-side landing plus runtime function-table ownership as a concrete reduction target, not just API trivia
- Linux: treat `SA_SIGINFO` visibility plus `ucontext_t` resume/context mutation as the concrete proof object, not signal registration alone

That should reduce future drift into endless exception-theory reading and route analysts faster toward narrower consequence proof.
