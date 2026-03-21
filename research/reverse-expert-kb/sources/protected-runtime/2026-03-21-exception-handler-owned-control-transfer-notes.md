# 2026-03-21 Exception-Handler-Owned Control-Transfer Notes

Purpose:
- support a practical workflow note for cases where exception or signal delivery owns the meaningful branch
- keep the protected-runtime branch practical and case-driven rather than drifting into generic SEH/VEH theory

## Search framing
Requested search mode:
- external-research-driven
- explicit multi-source search via `search-layer --source exa,tavily,grok`

Queries used:
1. `reverse engineering exception based anti debug SEH signal handler workflow`
2. `anti debug signal handler ptrace seccomp exception based reverse engineering`
3. `protected runtime exception handler anti tamper reverse engineering practical`
4. `Windows SEH VEH anti debugging reverse engineering exception handler`
5. `Linux signal handler anti debugging reverse engineering SIGTRAP SIGSEGV`
6. `exception based anti debugging reverse engineering SEH VEH signal handler`

High-value question:
- what practical KB rung is still missing for cases where ordinary direct control flow stays incomplete because handlers, traps, or signal delivery own the real transfer?

## Search results summary
Observed result quality:
- Exa, Tavily, and Grok all returned result sets through search-layer for this run
- result quality was mixed, but sufficient for a conservative practical note
- direct fetch quality was better for official Windows docs and focused practitioner writeups than for broad anti-debug compilations

Useful retained signals:
- Microsoft VEH and SEH documentation confirms the basic ownership split between vectored handlers, structured exception handling, and handler-side access to exception/context data
- the Elmo x64 SEH writeup is useful because it turns hidden exception ownership into a concrete reverse-engineering object: `RUNTIME_FUNCTION`, `UNWIND_INFO`, `KiUserExceptionDispatcher`, `RtlDispatchException`, `RtlLookupFunctionEntry`, and dynamic-function-table installation paths
- the revers.engineering exceptions article reinforces the analyst value of treating exceptions and interrupts as real RE surfaces, not just language-level error handling
- the BenteVE debug-register / VEH-SEH hook demo is useful not as a bypass recipe, but as evidence that trap-triggered control transfer can be intentionally owned by handler logic plus resume/trampoline behavior
- the Linux/anti-debug cluster usefully reinforces that signal/trap delivery can be the real divergence boundary and should not always be collapsed into generic ptrace stories

## Conservative synthesis
What the evidence supports clearly:
- some protected or anti-debug cases really do hide meaningful branch ownership inside exception/signal registration, lookup, and resume logic
- analysts benefit from distinguishing at least:
  - VEH-first global dispatch
  - SEH/unwind-local transfer
  - dynamic function-table/generated-code exception ownership
  - Linux signal-handler-owned transfer
  - trap-triggered hook / anti-debug dispatch
- a useful practical rung is to recover one handler-ownership boundary plus one first consequence-bearing context/state action before trying to continue as ordinary control-flow analysis

What the evidence does **not** justify claiming strongly:
- that exception-owned transfer is a dominant protected-runtime family overall
- that all signal/trap usage is anti-debug rather than ordinary crash or hook infrastructure
- that one implementation pattern should be generalized into platform-agnostic recipe advice

## Practical KB contribution chosen
Chosen output:
- `topics/exception-handler-owned-control-transfer-workflow-note.md`

Why this output was chosen:
- the protected-runtime branch already had broad anti-instrumentation and broader topology notes
- this run should avoid another wording-only or family-count sync pass
- exception/signal-handler-owned transfer is a thinner protected-runtime seam with real operator value
- the new note produces a practical continuation page rather than another top-level conceptual rewrite

## Search audit
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- exa
- tavily
- grok

Failed or degraded sources:
- none recorded at search-layer level for this run

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

## External URLs consulted directly
- `https://learn.microsoft.com/en-us/windows/win32/debug/vectored-exception-handling`
- `https://learn.microsoft.com/en-us/windows/win32/debug/structured-exception-handling`
- `https://revers.engineering/applied-re-exceptions/`
- `https://blog.elmo.sg/posts/structured-exception-handler-x64/`
- `https://github.com/BenteVE/SEH-VEH-hook-Debug-Registers-Breakpoint`
- `http://hkopp.github.io/2023/08/the-ptrace-anti-re-trick`
- `https://reverseengineering.stackexchange.com/questions/21367/debug-program-using-peculiar-anti-debugging-technique`

## Notes for future continuation
Good next continuations only if a real source-backed need appears:
- a narrower page-guard / single-step / debug-register continuation only if multiple case-backed sources justify it
- a mobile-specific signal/exception continuation only if it becomes materially distinct from the current protected-runtime note
- a later anti-cheat / privileged-debugger continuation, but only with concrete case-driven evidence rather than family inflation