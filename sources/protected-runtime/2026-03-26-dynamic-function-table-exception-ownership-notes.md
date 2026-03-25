# Exception-owned control transfer: dynamic function-table ownership as a practical continuation

Date: 2026-03-26
Branch: protected-runtime practical subtree
Chosen seam: exception-handler-owned control transfer
Mode: external-research-driven

## Why this source note exists
The protected-runtime exception-owned branch already preserved:
- dispatcher-side landing matters
- dynamic function-table ownership exists
- landing truth should be separated from resume truth

But the branch still risked staying slightly too slogan-like around dynamic unwind ownership.
It said the idea, but did not yet preserve enough concrete operator memory about **what to do when `RtlLookupFunctionEntry` keeps making sense only after runtime-installed tables exist**.

This pass tightens that seam into a more practical continuation:
- treat dynamic function-table ownership as a real operator branch, not as API trivia
- separate **range ownership truth** from **resume truth**
- preserve a small generated-code / stack-walking caution so analysts do not overread tools that ignore dynamic tables

## Practical takeaways preserved into the KB
### 1. Dynamic function-table registration is often the first truthful owner when static unwind ownership stays close-but-wrong
Microsoft documentation confirms:
- `RtlLookupFunctionEntry` searches the **active** function tables for the current PC
- `RtlInstallFunctionTableCallback` can make unwind ownership appear only after a callback-owned range is installed
- `RtlAddFunctionTable` and `RtlAddGrowableFunctionTable` do the same for prebuilt runtime function entries over generated-code ranges

The practical consequence for reverse work is:
- when dispatcher-side landing keeps recurring,
- and static PE exception data still does not convincingly own the PC,
- the next truthful object is often **one runtime-installed code range plus the registration site that owns it**.

That is usually a better stop rule than collecting more generic VEH/SEH names.

### 2. Range ownership truth and resume truth are related, but they are not the same thing
Recent Windows exception writeups plus Microsoft docs support a three-part split:
- landing truth -> where exceptional ownership becomes re-findable
- range ownership truth -> which runtime-added or callback-owned unwind range actually owns the current PC
- resume truth -> which resumed target, unwind consequence, or later handler-owned edge first predicts the behavior that matters

This matters because the branch can otherwise stall in two opposite ways:
- stopping too early at `KiUserExceptionDispatcher` / `RtlDispatchException`
- or stopping too early at `RtlInstallFunctionTableCallback` / growable-table registration without freezing one later consequence

A practical stop rule is therefore:
- first freeze one installed range or callback-owned lookup result
- then freeze one later resumed target / consequence edge
- then hand the case back to ordinary route, integrity, or anti-debug continuation work

### 3. Generated-code stack walking adds an important analyst caution: some tooling may under-report dynamic unwind ownership
Recent practitioner material around generated code and stack walking is useful because it preserves a small but practical warning:
- dynamically added unwind tables can be perfectly real for `RtlLookupFunctionEntry`, debugger unwinding, and ETW-style stack walking
- but some convenience stack-capture paths may fail to honor them consistently

For RE workflow, that means:
- do not treat one stack-capture helper failing to recover the generated-code frame as proof that the dynamic range is unowned or irrelevant
- prefer one direct `RtlLookupFunctionEntry` / unwind-aware observation over a weaker convenience backtrace when the two disagree

This is not a blanket tooling claim.
It is a conservative workflow reminder that **dynamic unwind ownership can be real even when one stack-view surface is misleading**.

### 4. Dispatcher-layout realism still matters because wrong landing assumptions can make dynamic ownership look broken
Recent `KiUserExceptionDispatcher` practitioner material still matters here.
If the analyst's landing model is wrong, later unwind lookup and resume behavior can look falsely nonsensical.

So a useful progression is:
1. make dispatcher-side landing truthful enough
2. freeze one dynamic range ownership object
3. freeze one resumed target or consequence edge
4. leave broad exception theory

That keeps the branch practical instead of drifting into platform-tourism.

## Best-fit source clusters
### Official / primary
- Microsoft Learn: `RtlInstallFunctionTableCallback`
- Microsoft Learn: `RtlAddFunctionTable`
- Microsoft Learn: `RtlLookupFunctionEntry`

### Practitioner / explanatory
- Elmo: x64 SEH / unwind / dynamic function-table lookup context
- Momo5502: dispatcher-side landing and stack-layout realism around `KiUserExceptionDispatcher`
- Sebastian Schöner: generated-code unwind registration and stack-walking caveats

## Conservative synthesis boundaries
This pass does **not** claim:
- that every protected target uses dynamic function tables
- that every generated-code range is protection-related
- that one failing stack-capture helper proves a Windows bug in all contexts

It only preserves a stronger operator rule:
- when unwind ownership keeps looking real only after runtime registration is considered, freeze one installed range first
- then freeze one later resume or consequence edge
- do not let the case stall at either pure dispatcher naming or pure registration naming

## Direct URLs retained for synthesis
- `https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-rtlinstallfunctiontablecallback`
- `https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-rtladdfunctiontable`
- `https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-rtllookupfunctionentry`
- `https://blog.elmo.sg/posts/structured-exception-handler-x64/`
- `https://momo5502.com/posts/2024-09-07-a-journey-through-kiuserexceptiondispatcher/`
- `https://blog.s-schoener.com/2025-01-24-stack-walking-generated-code/`

## Search audit
Requested sources: exa, tavily, grok
Succeeded sources: exa, tavily, grok
Failed sources:
- none during the search-layer attempt captured for this note
Endpoints used:
- Exa: http://158.178.236.241:7860
- Tavily: http://proxy.zhangxuemin.work:9874/api
- Grok: http://proxy.zhangxuemin.work:8000/v1

## Practical operator reminder to preserve
When `RtlLookupFunctionEntry` keeps recurring but static ownership remains thin, do not stop at:
- “the dispatcher is involved”
- “VEH/SEH exists”
- “a callback registration API exists somewhere”

Freeze these two smaller proof objects instead:
- one runtime-installed range that truthfully owns the current PC
- one resumed target, unwind consequence, or later handler-owned edge that makes that ownership behaviorally relevant

That is usually enough to leave the exception-owned branch without overexpanding unwind theory.
