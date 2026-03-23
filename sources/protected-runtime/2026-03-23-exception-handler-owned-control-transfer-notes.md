# 2026-03-23 Exception-Handler-Owned Control-Transfer Notes

Purpose:
- perform an external-research-driven refresh of the exception/signal-handler-owned control-transfer branch
- strengthen the existing workflow note with more operator-facing stop rules and case-shaping anchors
- avoid another protected-runtime run that only does internal wording/index sync

## Search framing
Requested search mode:
- external-research-driven
- explicit multi-source search via `search-layer --source exa,tavily,grok`

Queries used:
1. `Windows VEH SEH KiUserExceptionDispatcher RtlDispatchException RtlLookupFunctionEntry dynamic function table reverse engineering`
2. `Linux signal handler ucontext SIGTRAP SIGSEGV control flow anti debug reverse engineering`
3. `page guard hardware breakpoint exception handler resume address anti debug reverse engineering`

High-value question:
- what practical details make the existing exception-handler-owned transfer page more useful to an operator who already suspects handler-owned dispatch and now needs a smaller stop rule, compare pair, or downstream continuation target?

## Search results summary
Observed search-layer result quality:
- Exa succeeded
- Tavily succeeded
- Grok succeeded
- returned material was mixed, but good enough to support a conservative practical refinement

Most useful retained signals:
- Microsoft Learn usefully confirms the official API surface and, importantly, keeps dynamic function table APIs (`RtlAddFunctionTable`, `RtlAddGrowableFunctionTable`, `RtlInstallFunctionTableCallback`) on the same canonical SEH page as vectored handlers; that is enough to justify keeping dynamic-function-table ownership as a first-class family in the workflow note rather than a side remark
- Maurice Heumann’s `KiUserExceptionDispatcher` writeup is especially useful because it turns dispatcher-side landing into a concrete reverse-engineering anchor rather than folklore; the practical value is not just “exceptions exist” but that stack layout, unwind expectations, and `RtlLookupFunctionEntry` calls can explain why naive direct-call reading stays wrong
- Elmo’s x64 SEH internals writeup sharpens the operator model: `KiUserExceptionDispatcher -> RtlDispatchException -> RtlpCallVectoredHandlers -> RtlLookupFunctionEntry -> RtlpLookupDynamicFunctionEntry -> RtlVirtualUnwind / handler execution`; this supports a better stop rule in the KB: if registration is too abstract, the next honest object is often dispatcher landing plus one lookup/consequence pair
- Ling’s hardware-breakpoint article is valuable not because the KB should teach breakpoint tricks, but because it shows a very concrete family where the visible trigger (`#DB`, DRx, single-step) is not the main proof object; the practical proof object is handler-owned context/state change plus resumed target
- Check Point’s anti-debug exceptions page is useful as conservative evidence that exception chains can be used both for debugger-sensitive branching and for deliberate control-flow hiding, but it is too recipe-like to carry the whole page; it works best as corroboration for the existing “don’t stop at proving VEH/SEH exists” stance
- Linux-specific search results were weaker and noisier than Windows-specific ones, but still sufficient to preserve two conservative signals: `sigaction`/`ucontext_t` can be a real branch-owning surface, and debugger-vs-nondebugger divergence around `SIGTRAP`/`SIGSEGV` is a legitimate compare axis

## Direct fetch audit
Useful direct fetches:
- `https://learn.microsoft.com/en-us/windows/win32/debug/structured-exception-handling-functions`
- `https://momo5502.com/posts/2024-09-07-a-journey-through-kiuserexceptiondispatcher/`
- `https://blog.elmo.sg/posts/structured-exception-handler-x64/`
- `https://ling.re/hardware-breakpoints/`
- `https://anti-debug.checkpoint.com/techniques/exceptions.html`

Degraded or blocked direct fetches:
- `https://reverseengineering.stackexchange.com/questions/21597/can-i-trap-sigsegv-on-a-linux-and-what-are-are-the-conditions-to-make-it-works/21598`
  - `web_fetch` returned `403` / Cloudflare interstitial
  - this did **not** block the run because the search-layer pass had already succeeded with Exa/Tavily/Grok, and Linux claims were kept conservative

## Conservative synthesis
What the evidence supports clearly:
- the page should keep treating dispatcher-side landing as a first-class ownership boundary, not just a supporting detail after VEH/SEH naming
- dynamic-function-table ownership deserves explicit practical emphasis because it explains a common failure mode: static exception metadata looks incomplete, yet runtime-installed unwind ownership is the truthful explanation
- the page benefits from a more explicit compare-pair ladder for three recurring concrete families:
  - software or hardware trap consumed differently under debugger vs non-debugger conditions
  - page-guard or single-step sequences where the analyst must separate trigger from re-arm/resume behavior
  - Linux signal-delivery cases where the key question is whether `ucontext_t` mutation or signal interception is the real branch owner
- the most useful operator stop rule is still small: one ownership boundary plus one consequence-bearing resume/state action, then leave

What the evidence does **not** justify claiming strongly:
- that Linux signal-based protected-runtime control transfer is as well-supported in this source batch as the Windows side
- that every exception-heavy path is anti-debug rather than ordinary crash, hook infrastructure, or recovery logic
- that every dynamic function table is protection-related rather than runtime/JIT/runtime-support machinery

## Practical KB changes chosen
Chosen KB update:
- materially refine `topics/exception-handler-owned-control-transfer-workflow-note.md`

Intended improvements:
- make dispatcher-side landing a clearer practical stop point
- make dynamic-function-table ownership more operationally concrete
- add tighter compare pairs and stop rules around page-guard, hardware-breakpoint, and signal cases
- keep the note practical and case-driven instead of broadening into exception theory

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
- none at search-layer level

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

## Notes for future continuation
Good next continuations only if future runs have fresh evidence:
- a thinner page-guard / guard-page re-arm continuation if multiple practical case sources justify a dedicated leaf
- a Linux signal-owned control-transfer leaf only if a later run gets stronger source quality than this batch
- a cross-link from this exception-owned note into runtime-evidence compare-run guidance if repeated cases show analysts stalling at compare design rather than handler-family classification
