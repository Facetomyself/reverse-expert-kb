# Guard-page / fault-owned transfer practical notes

Date: 2026-03-27 09:19 Asia/Shanghai / 2026-03-27 01:19 UTC
Scope: protected-runtime exception-owned continuation, with a thinner practical seam around guard-page / single-step re-arm realism and Linux fault-handler resume realism
Related pages:
- `topics/exception-handler-owned-control-transfer-workflow-note.md`
- `topics/protected-runtime-practical-subtree-guide.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`

## Why this note exists
The protected-runtime branch already knew that exception/signal ownership can hide the real branch. What it did not preserve sharply enough was a narrower practical stop rule for guard-page and fault-owned cases:
- the first fault/guard hit is usually only a one-shot trigger or landing boundary
- the useful analyst object is often the handler-side resume edit plus the re-arm realism that keeps the mechanism alive for later hits
- this is one of the thinner seams where analysts can overread the trigger primitive itself and underread the handler-owned continuation

This matters because PAGE_GUARD and similar fault-owned dispatch patterns often look deceptively solved too early:
- seeing `VirtualProtect(..., PAGE_GUARD)` or `NtProtectVirtualMemory(..., PAGE_GUARD)` is not yet behavior proof
- seeing one `STATUS_GUARD_PAGE_VIOLATION` is not yet ongoing ownership proof
- seeing one Linux `sigaction(..., SA_SIGINFO, ...)` fault handler is not yet the same thing as proving one resumed target or one stable fault-owned continuation

## Conservative retained takeaways
### Windows guard-page realism
Official Microsoft documentation preserves the key one-shot fact:
- a guard page raises `STATUS_GUARD_PAGE_VIOLATION` on access
- the system then clears the guard attribute
- the next access will not fault the same way unless the page is reestablished as guarded again

That is the practical anchor for this seam:
- **guard configured** != **first fault observed** != **re-armed for later reuse** != **meaningful resumed consequence**

Practical consequence for analysts:
- if a case appears to rely on guard-page-owned dispatch, do not stop at one first-hit violation
- freeze whether the handler or immediate follow-on path reestablishes the guard bit, often via a `STATUS_SINGLE_STEP`-driven reapply pattern or equivalent protection rewrite
- if later hits keep happening but no re-arm evidence exists, assume your current story is incomplete

### VEH / guard-page practitioner pattern
Practitioner material repeatedly shows the same operational shape:
- mark the containing page with `PAGE_GUARD`
- catch `STATUS_GUARD_PAGE_VIOLATION`
- inspect whether the exception address is the target of interest
- rewrite resume state or simulate an early return when it is
- set trap/single-step state so one immediate `STATUS_SINGLE_STEP` can be used to reapply `PAGE_GUARD`

For KB purposes, the durable lesson is not the bypass recipe itself. The durable lesson is the workflow stop rule:
- the trigger primitive is often infrastructure
- the handler-side resume edit is the first behavior-bearing proof object
- the single-step re-arm path is often the reality check that distinguishes a one-off fault from a sustained control-transfer mechanism

### Linux signal/fault-handler realism
Linux fault/signal material is noisier in public sources, but the conservative cross-source point is still stable enough:
- `SA_SIGINFO` handlers get a context object
- handler-side edits to machine context can change the resumed IP/PC or related state
- a visible fault alone is weaker than one resumed target or one state mutation that predicts later behavior
- non-reentrant or broad crash-style behavior should not be overread as deliberate handler-owned continuation without one concrete resumed consequence

Practical consequence for analysts:
- keep **handler registered** separate from **fault delivered** and separate again from **resume target edited**
- if the same signal family can lead to different later PCs or state writes, the resumed edge is usually the first useful consumer-level truth

## Useful branch shorthand added by this note
For this specific seam, preserve:
- **guard configured != first fault != re-armed mechanism != resumed consequence**

That shorthand complements the broader exception-owned branch memory:
- **landing truth**
- **range/lookup truth** when relevant
- **resume truth**

## Suggested case-facing workflow consequences
When a protected-runtime case looks guard-page or fault-owned:
1. freeze the first truthful landing:
   - `STATUS_GUARD_PAGE_VIOLATION`, `STATUS_SINGLE_STEP`, `SIGSEGV`, or similar
2. freeze one handler-side action that actually changes meaning:
   - resume IP rewrite
   - stack/return rewrite
   - skip-length change
   - small verdict/state write
3. freeze one mechanism-sustainment fact if the pattern is meant to repeat:
   - reapply `PAGE_GUARD`
   - set/clear trap state deliberately
   - restore page protection or similar fault precondition
4. only then hand off to the later ordinary consumer or consequence path

## Sources used conservatively
- Microsoft Learn: `Creating Guard Pages - Win32 apps`
- ShigShag: `Patchless AMSI Bypass via Page Guard Exceptions`
- search-layer results from Tavily-backed retrieval for Stack Overflow / ReverseEngineering StackExchange / Linux signal-handler references

## Search / fetch reality this note depended on
- explicit search attempted through `search-layer --source exa,tavily,grok`
- Tavily returned usable material
- Exa degraded with a payment error on this run
- Grok degraded with repeated 502 errors on this run
- direct `web_fetch` worked for Microsoft Learn and the ShigShag page
- direct `web_fetch` on some Stack Overflow / RE StackExchange pages hit Cloudflare/403 interstitials, so those pages were used only through returned search snippets and not treated as stronger than the Microsoft Learn confirmation
