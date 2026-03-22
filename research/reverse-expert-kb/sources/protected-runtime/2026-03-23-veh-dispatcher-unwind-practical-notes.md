# 2026-03-23 VEH / dispatcher / unwind practical notes

Purpose:
- strengthen the existing exception-handler-owned control-transfer branch with a more concrete Windows practical continuation
- preserve a case-driven operator rule for when handler registration alone is too abstract and the real truthful ownership boundary is dispatcher-side landing or unwind lookup

## Why this follow-up run happened
The protected-runtime branch already had a useful exception-handler-owned control-transfer note, but the new external-research pass suggested a narrower practical reinforcement was worthwhile:
- official VEH documentation confirms vectored handlers and context-based resume as a real control-transfer surface
- practitioner material around `KiUserExceptionDispatcher`, `RtlDispatchException`, and unwind lookup gives a more re-findable analyst object than broad “SEH/VEH exists” wording
- this improves operator value without inflating the branch into another separate family page

## Search framing
Requested search mode:
- external-research-driven
- explicit multi-source search via `search-layer --source exa,tavily,grok`

Queries used:
1. `vectored exception handler control transfer reverse engineering anti debugging`
2. `windows exception dispatcher KiUserExceptionDispatcher RtlDispatchException reverse engineering`
3. `malware VEH anti-debug exception handler control flow analysis`

## Retained external signals
### Microsoft Learn — vectored exception handling
Retained value:
- confirms VEH as a deliberate first-class user-mode exception routing surface
- supports the KB’s focus on `ContextRecord` / resume decisions rather than only API presence

URL:
- `https://learn.microsoft.com/en-us/windows/win32/debug/vectored-exception-handling`

### Momo5502 — journey through KiUserExceptionDispatcher
Retained value:
- useful for making dispatcher-side landing a concrete analyst object
- reinforces that `KiUserExceptionDispatcher` is often the first stable place to correlate exception arrival with later user-mode dispatch logic
- supports a practical stop rule: once dispatcher-side landing plus one consequence-bearing lookup/handler action are good enough, leave broad exception theory

URL:
- `https://momo5502.com/posts/2024-09-07-a-journey-through-kiuserexceptiondispatcher/`

### 0xpat — malware development anti-debug examples
Retained value:
- not used as a bypass recipe
- useful as practitioner evidence that exceptions and VEH are often used as behaviorally meaningful anti-debug/control surfaces, not just language/runtime infrastructure

URL:
- `https://0xpat.github.io/Malware_development_part_3/`

## Conservative synthesis
What this run supports adding to the KB:
- for Windows cases, the first ownership boundary is often better framed as one of:
  - vectored registration
  - dispatcher-side landing (`KiUserExceptionDispatcher`)
  - `RtlDispatchException` / `RtlLookupFunctionEntry` / unwind lookup into a concrete region
  - runtime-installed function-table callback ownership
- this is a practical improvement because it gives the analyst one re-findable landing and one stop rule rather than more generic handler theory

What this run does not justify:
- a separate standalone page just for `KiUserExceptionDispatcher`
- promoting one Windows dispatcher family into a universal exception-analysis recipe
- broad claims about prevalence across all protected targets

## KB contribution chosen
Updated rather than created:
- `topics/exception-handler-owned-control-transfer-workflow-note.md`
- `topics/protected-runtime-practical-subtree-guide.md`

Reason:
- the branch already had the right leaf
- the real gap was practical specificity inside that leaf and its subtree routing language

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
- no search-layer source failure recorded
- later direct fetch degradation observed for one SonicWall page and excluded from synthesis

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

## Direct URLs consulted
- `https://learn.microsoft.com/en-us/windows/win32/debug/vectored-exception-handling`
- `https://momo5502.com/posts/2024-09-07-a-journey-through-kiuserexceptiondispatcher/`
- `https://0xpat.github.io/Malware_development_part_3/`

Excluded due to fetch failure:
- `https://www.sonicwall.com/blog/guloader-demystified-unraveling-its-vectored-exception-handler-approach`

## Practical operator reminder to preserve
When a protected Windows case already smells exception-owned, do not stop at “VEH/SEH exists.” Prefer the smallest re-findable truthful boundary:
- registration if it already predicts the later branch
- otherwise dispatcher-side landing
- otherwise unwind lookup into one concrete region
- otherwise runtime-installed function-table ownership for generated code

Then stop broad handler theory as soon as one ownership boundary and one consequence-bearing resume/state action are good enough to hand the case back to ordinary route/state proof, integrity consequence proof, or observation-topology repair.
