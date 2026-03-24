# Exception-owned control transfer: landing truth vs resume truth

Date: 2026-03-24
Branch: protected-runtime practical subtree
Chosen seam: exception-handler-owned control transfer
Mode: external-research-driven

## Why this source note exists
This source note captures the external-research pass behind a narrower practical refinement to the existing exception-handler workflow note.

The practical gap was no longer whether dispatcher-side landing matters.
That was already in the KB.

The thinner but still useful gap was:
- when should the analyst stop treating dispatcher/signal landing as the main proof object,
- and when should they instead preserve one resumed target, one context/register mutation, or one trap-specific resume delta as the first behavior-bearing truth?

## Practical takeaways preserved into the KB
### 1. Dispatcher landing is a strong anchor, but still only infrastructure until a later consequence is frozen
Microsoft Learn plus practitioner writeups reinforce that:
- VEH is a real first-class exception-routing surface
- `KiUserExceptionDispatcher` / `RtlDispatchException` are highly re-findable user-mode landing points
- `RtlLookupFunctionEntry` and dynamic function tables explain why ownership can stay invisible statically

But that still does **not** mean dispatcher landing is already the behavior-bearing consumer.
The more useful practical split is:
- landing truth -> where exception/signal ownership becomes re-findable
- lookup/range truth -> which owning region or callback-owned range is actually in play
- resume truth -> which resumed target or context mutation actually predicts later behavior

### 2. Recent Windows material strengthens the need to preserve stack/layout realism before reasoning about resume truth
Recent practitioner material around `KiUserExceptionDispatcher` is useful because it shows:
- guessed prototypes can be misleading
- stack/context layout realism can decide whether unwind ownership looks truthful at all
- once landing realism is restored, the next operator question is usually no longer “what is the dispatcher?” but “which later resume target or unwind-owned continuation actually matters?”

That makes landing truth a prerequisite, not the final stop rule.

### 3. Linux signal-handler cases benefit from the exact same split
Linux-side practitioner material plus `sigaction` references support the same operator rule:
- `SA_SIGINFO` and `ucontext_t` access are useful because they expose interrupted state
- but registration or landing alone is still infrastructure
- the practical proof object is one changed RIP/PC-like value, one register edit, one skip length, or one resumed target that predicts later behavior

This keeps Windows and Linux under the same practical stop rule.

## Best-fit source clusters
### Official / primary
- Microsoft Learn: vectored exception handling
- Microsoft Learn: `RtlLookupFunctionEntry`

### Practitioner / explanatory
- Maurice's Blog: `KiUserExceptionDispatcher`
- Elmo blog: modern x64 SEH / unwind deep dive
- Linux signal / `ucontext_t` practitioner material
- self-single-step / trap-resume writeup using signal-context manipulation

## Conservative synthesis boundaries
This pass does **not** claim:
- that every dispatcher landing implies meaningful hidden control transfer
- that every signal-context mutation is anti-debug or protection-related
- that landing truth is unimportant

It only claims a tighter practical routing rule:
- landing truth is necessary but still infrastructure
- resume truth is often the first behavior-bearing proof object worth freezing before handing the case back to ordinary route/state, integrity consequence, or anti-debug continuation work

## Direct URLs retained for synthesis
- `https://learn.microsoft.com/en-us/windows/win32/debug/vectored-exception-handling`
- `https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-rtllookupfunctionentry`
- `https://blog.elmo.sg/posts/structured-exception-handler-x64/`
- `https://momo5502.com/posts/2024-09-07-a-journey-through-kiuserexceptiondispatcher/`
- `https://stackoverflow.com/questions/2663456/how-to-write-a-signal-handler-to-catch-sigsegv`
- `https://ayrtonm.com/posts/2023/Self-single-stepping-code.html`

Excluded / degraded direct fetches:
- `https://momo5502.com/posts/2024-09-07-a-journey-through-kiuserexceptiondispatcher/` via `web_fetch` returned `403 Just a moment...` in one attempt, but the source remained usable from search-layer results and another successful fetch path was available

## Search audit
Requested sources: exa, tavily, grok
Succeeded sources: exa, tavily, grok
Failed sources:
- none during this search-layer run
Endpoints used:
- Exa: http://158.178.236.241:7860
- Tavily: http://proxy.zhangxuemin.work:9874/api
- Grok: http://proxy.zhangxuemin.work:8000/v1

## Practical operator reminder to preserve
When a protected target is already clearly exception/signal-owned, do not stop at:
- “VEH/SEH exists”
- “`KiUserExceptionDispatcher` keeps recurring”
- “`sigaction` with `SA_SIGINFO` exists”

Freeze one smaller proof object instead:
- one resumed target
- one context/register mutation
- one trap-family-specific resume delta
- one small state write that reliably accompanies the resumed path

That is usually the first moment the case becomes ordinary enough to hand back to narrower consequence proof.
