# Dynamic unwind range ownership: registration vs PC coverage vs lookup hit vs resumed consequence

Date: 2026-03-27
Branch: protected-runtime practical subtree
Chosen seam: exception-handler-owned control transfer
Mode: external-research-driven

## Why this source note exists
The protected-runtime exception-owned branch already preserved:
- dispatcher-side landing matters
- dynamic function-table ownership matters
- landing truth should be separated from resume truth
- range ownership truth is often the missing middle object

What was still slightly too compressible was the practical operator stop rule around dynamic unwind ownership.
The branch could still be overread as if:
- seeing `RtlInstallFunctionTableCallback` / `RtlAddFunctionTable` / `RtlAddGrowableFunctionTable`
- plus a general belief that dynamic unwind tables exist

already meant that the current protected branch was really owned by that runtime-installed region.

This pass tightens that seam into a sharper four-way split:
- `registered != covering this PC != lookup hit != resumed consequence`

That rule is narrower, more case-driven, and better matched to real operator failure modes.

## Practical takeaways preserved into the KB
### 1. Registration truth is only the first and weakest proof object
Microsoft’s API surfaces are explicit that the dynamic unwind registration objects are range-shaped:
- `RtlInstallFunctionTableCallback` takes a `BaseAddress` and `Length`, and the callback manages that region
- `RtlAddFunctionTable` uses a supplied table plus a base address for relative entries
- `RtlAddGrowableFunctionTable` likewise registers a runtime-owned unwind region for generated code

So a visible API call proves only:
- some dynamic unwind ownership was installed

It does **not** yet prove:
- that the current instruction pointer falls inside the relevant owned region
- that unwind lookup for the current PC actually resolves into that registration
- that the later behavior-bearing resumed branch is owned by that range

### 2. PC coverage truth is stronger than registration truth
The next truthful object is often not the API site itself, but whether the branch-defining PC actually falls inside the installed region.

That matters because practical cases often overclaim from one of these weaker observations:
- callback registration exists somewhere in startup code
- growable-table registration exists for one helper/JIT region
- generated-code support is generally present in the process

Yet the branch being analyzed may still be:
- outside that range
- owned by a different unwind region
- or still lacking any successful unwind ownership for the current PC

A better practical question is therefore:
- does the current faulting / resumed / branch-defining PC actually sit inside the callback-managed or runtime-added region?

### 3. Lookup-hit truth is stronger than mere range plausibility
Microsoft’s `RtlLookupFunctionEntry` documentation is especially useful here because it states that it searches the **active function tables** for an entry corresponding to the specified PC value.

That gives the branch a stronger stop rule:
- range plausibility is still weaker than one real lookup hit for the PC that matters

So in dynamic-unwind exception-owned cases, a strong operator sequence is:
1. freeze one registration site
2. freeze one owned range that actually covers the PC of interest
3. freeze one `RtlLookupFunctionEntry`-style hit that resolves the PC into a concrete runtime-owned entry/range
4. only then widen into resumed-target or consequence proof

This avoids stopping too early at documentation-shaped API inventory.

### 4. Resumed consequence is still a separate proof object
Even a successful lookup hit is still not the same as proving the behavior that matters.

The branch still needs one of:
- a resumed RIP/PC
- an instruction skip or trap-specific resume delta
- a handler-owned state write
- a downstream consequence edge that predicts the later branch

So the practical four-way split is:
- **registered** -> the dynamic unwind surface exists
- **covering this PC** -> the current PC falls into the candidate owned region
- **lookup hit** -> unwind lookup really resolves that PC into the runtime-owned region/entry
- **resumed consequence** -> one later branch/state/resume effect actually predicts behavior

That keeps the exception-owned branch from stopping at infrastructure proof.

### 5. Unwind-aware lookup is stronger than convenience backtrace surfaces when the two disagree
Recent practitioner material on generated-code stack walking is useful because it preserves a conservative but practical caution:
- if dynamic unwind registration is correct and `RtlLookupFunctionEntry` can find the current entry, debugger/ETW-visible unwinding may still look healthier than convenience stack-capture surfaces such as `RtlCaptureStackBackTrace`

For RE workflow that means:
- one convenience backtrace failing to show the generated-code frame is weaker than one direct unwind-aware lookup hit
- do not demote a dynamic range to “probably irrelevant” just because one stack-capture helper is not dynamic-table-aware enough

## Best-fit source clusters
### Official / primary
- Microsoft Learn: `RtlLookupFunctionEntry`
- Microsoft Learn: `RtlInstallFunctionTableCallback`
- Microsoft Learn: `RtlAddFunctionTable`
- Microsoft Learn: `RtlAddGrowableFunctionTable`
- Microsoft Learn: `RtlDeleteGrowableFunctionTable`

### Practitioner / explanatory
- Sebastian Schöner: generated-code unwind registration and stack-walking caveats
- Elmo: x64 SEH / unwind context and function-table lookup surroundings
- OSR NTDEV discussion: practical distinction around growable function tables / unwind visibility

## Conservative synthesis boundaries
This pass does **not** claim:
- that every dynamic function-table registration is protection-related
- that every current PC inside a registered range is necessarily behavior-bearing
- that every failing backtrace helper is evidence of malicious concealment

It only preserves a stronger operator rule:
- do not stop at API presence alone
- prove registration, then current-PC coverage, then lookup hit, then resumed consequence as separate proof objects when possible

## Direct URLs retained for synthesis
- `https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-rtllookupfunctionentry`
- `https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-rtlinstallfunctiontablecallback`
- `https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-rtladdfunctiontable`
- `https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-rtladdgrowablefunctiontable`
- `https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-rtldeletegrowablefunctiontable`
- `https://blog.s-schoener.com/2025-01-24-stack-walking-generated-code/`
- `https://blog.elmo.sg/posts/structured-exception-handler-x64/`
- `https://community.osr.com/t/rtladdfunctiontable-vs-rtladdgrowablefunctiontable/51512`

## Search audit
Requested sources: exa, tavily, grok
Succeeded sources:
- tavily
Failed sources:
- exa (`402 Payment Required` during direct backend invocation)
- grok (`502 Bad Gateway` during chat/completions invocation)
Degraded / partial observations:
- merged search output still included some Exa-carried result items despite the backend error; these were treated as degraded/partial presence rather than as a healthy Exa success
Endpoints used:
- Exa: `http://158.178.236.241:7860/search`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

## Practical operator reminder to preserve
In Windows dynamic-unwind exception-owned cases, keep this exact shorthand alive:
- `registered != covering this PC != lookup hit != resumed consequence`

That is the practical guardrail that prevents broad handler/unwind theory from being mistaken for one real behavior-bearing ownership proof.
