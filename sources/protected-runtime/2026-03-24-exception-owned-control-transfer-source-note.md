# Exception-owned control transfer: dynamic unwind ownership and signal-context resume

Date: 2026-03-24
Branch: protected-runtime practical subtree
Chosen seam: exception-handler-owned control transfer
Mode: external-research-driven

## Why this source note exists
This source note captures the external-research pass behind the current refinement of the protected-runtime exception-handler workflow note.

The practical gap was not broad exception theory.
It was a smaller operator question:
- when should the analyst stop broadening around VEH/SEH/signal APIs,
- and what concrete proof object is enough to hand the case back to ordinary route/state work?

## Practical takeaways preserved into the KB
### 1. Windows dynamic function-table ownership is a real stop rule, not just API trivia
Microsoft documentation plus recent practitioner writeups strengthen a practical continuation:
- `RtlLookupFunctionEntry` searches active function tables for a PC, not only original static PE unwind ownership
- `RtlInstallFunctionTableCallback` installs callback-owned unwind metadata for a region
- when dispatcher-side arrival keeps recurring but static ownership stays incomplete, the practical object is often:
  - one callback-owned or runtime-added range
  - plus one later resume/consequence edge

That is enough to stop widening broad unwind theory.

### 2. `KiUserExceptionDispatcher` / `RtlDispatchException` are useful because they are re-findable landings, not because naming them is progress by itself
Recent practitioner material reinforces the existing KB direction:
- registration names alone are often too broad
- dispatcher-side landing gives a stable compare / trace boundary
- but landing alone is still infrastructure
- the useful next proof object is one concrete lookup-owned region, handler action, or later resume/state consequence

### 3. Linux signal-handler cases need the same infrastructure-vs-consequence split
Official `sigaction(2)` documentation and practitioner references support a conservative rule:
- `SA_SIGINFO` gives a three-argument handler with context access
- the third argument can be treated as `ucontext_t`-like interrupted state
- in practical RE cases, the useful boundary is not "signal registration exists"
- it is one resume-target or register/state mutation that predicts later behavior

This makes the Linux side align nicely with the Windows stop rule:
- registration/landing alone = infrastructure
- one concrete context/resume mutation = practical progress

## Best-fit source clusters
### Official / primary
- Microsoft Learn: `RtlInstallFunctionTableCallback`
- Microsoft Learn: `RtlLookupFunctionEntry`
- man7: `sigaction(2)`

### Practitioner / explanatory
- Maurice's Blog: `KiUserExceptionDispatcher`
- Elmo blog: modern x64 SEH / unwind deep dive
- generated-code / unwind ownership writeups surfaced by search-layer
- Linux practitioner Q&A around `ucontext_t` resume / signal-context edits

## Conservative synthesis boundaries
This pass does **not** claim:
- that dynamic function tables are common in all protected targets
- that signal-context mutation always implies anti-debug logic
- that dispatcher landing alone proves a malicious/protective intent

It only claims a stronger practical routing rule:
- stop calling the case “exception-owned” once there is one concrete runtime-owned lookup range or one concrete context/resume mutation that already predicts later behavior;
- then hand the case back to narrower consequence proof.

## Search audit
Requested sources: exa, tavily, grok
Succeeded sources: exa, tavily, grok
Failed sources: none observed in this run
Endpoints used:
- Exa: http://158.178.236.241:7860
- Tavily: http://proxy.zhangxuemin.work:9874/api
- Grok: http://proxy.zhangxuemin.work:8000/v1
