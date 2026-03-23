# Reverse KB Autosync Run Report

- Time: 2026-03-23 21:20 Asia/Shanghai / 2026-03-23 13:20 UTC
- Mode: external-research-driven
- Branch worked: protected-runtime practical branch
- Focus: exception/signal-handler-owned control transfer

## Why this branch / direction review
Recent same-day runs had already spent meaningful effort on internal branch synchronization and on nearby protected-runtime practical leaves. To avoid drift into endless canonical-sync-only maintenance, this run intentionally chose a thinner but still practical protected-runtime seam that could support a real external-research pass.

Chosen direction:
- strengthen the KB itself, not just source stash accumulation
- keep work practical and case-driven
- improve a thin practical continuation page rather than only polishing top-level wording

Why this branch was a good fit:
- the protected-runtime practical subtree already had the broad leaf for exception/signal-handler-owned transfer, but the page still risked stalling at “prove VEH/SEH/signal usage exists” instead of helping an operator freeze one ownership boundary and one consequence-bearing resume action
- this made it a good anti-stagnation target: thin enough to benefit from fresh external research, practical enough to improve operator value, and not just another dense browser/mobile increment

## Branch-balance review
Current balance signal after this run:
- browser/mobile remain easy-to-overfeed and did not get this slot
- protected-runtime received a thinner practical refinement rather than another broad family-count or wording pass
- this run improved branch quality without adding a whole new leaf, which is appropriate because the branch already had the right leaf but needed stronger operational memory

Maintenance takeaway:
- this was not just index grooming
- it was a source-backed practical refinement on an underfed-enough seam inside an already-important branch

## External research performed
A real explicit multi-source search was attempted through `search-layer --source exa,tavily,grok`.

Queries:
1. `Windows VEH SEH KiUserExceptionDispatcher RtlDispatchException RtlLookupFunctionEntry dynamic function table reverse engineering`
2. `Linux signal handler ucontext SIGTRAP SIGSEGV control flow anti debug reverse engineering`
3. `page guard hardware breakpoint exception handler resume address anti debug reverse engineering`

High-value question:
- what practical details would make the exception-handler-owned control-transfer page more useful to an operator who already suspects handler-owned dispatch and now needs a smaller stop rule, compare pair, or truthful continuation target?

## Search findings used
Most useful retained signals:
- Microsoft’s SEH function surface keeps dynamic function table APIs on the same canonical page as vectored handlers, which supports treating dynamic-function-table ownership as a first-class workflow family
- the `KiUserExceptionDispatcher` practitioner writeup makes dispatcher-side landing a concrete RE anchor rather than folklore, especially around unwind expectations and why naive direct-call reading stays wrong
- the x64 SEH deep dive reinforces the practical chain `KiUserExceptionDispatcher -> RtlDispatchException -> RtlLookupFunctionEntry / dynamic lookup / unwind`, which supports a better stop rule for analysts
- hardware-breakpoint / guard-page material reinforces that the visible trigger is often not the real proof object; the real object is handler-owned context rewrite plus resumed target or downstream state consequence
- Linux-specific material was weaker than the Windows side, so Linux-related page refinement stayed conservative

## KB changes made
### 1. New source note
Added:
- `sources/protected-runtime/2026-03-23-exception-handler-owned-control-transfer-notes.md`

What it captures:
- explicit search framing
- retained multi-source findings
- direct-fetch degradation note
- conservative synthesis and next-step guidance

### 2. Practical workflow note refined
Updated:
- `topics/exception-handler-owned-control-transfer-workflow-note.md`

Material refinements:
- strengthened Step 3 so dynamic function table ownership is treated as a first-class ownership explanation rather than a side remark
- strengthened Step 5 with more useful compare pairs around page-guard re-arm behavior and hardware-breakpoint-driven resume-context mutation
- sharpened Failure mode 3 so the analyst freezes one runtime-owned code range or lookup result instead of stopping at API-name collection
- updated source-footprint wording so the official dynamic-function-table API surface is explicitly remembered

Net effect:
- the page is now more practical for cases where the analyst already knows exceptions matter but still needs a smaller honest proof object
- the page is less likely to drift into generic SEH/VEH theory or cookbook anti-debug narration

### 3. Top-level branch-balance memory updated
Updated:
- `index.md`

Change:
- added a short balance note that the protected-runtime exception-owned control-transfer branch is now sharpened around dispatcher landing, dynamic-function-table ownership, and trap-family compare pairs

## Practical operator value added
This run materially improved the KB’s usefulness for a recurring real bottleneck:
- cases where direct control flow still looks wrong
- handler registration is visible but still too broad
- unwind lookup or generated-code ownership is the truthful next object
- the analyst needs a better compare pair than just “with debugger / without debugger”

The key practical improvement is a better stop rule:
- freeze one ownership boundary
- freeze one consequence-bearing resume/state action
- leave broad exception theory there

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

Direct-fetch degradation encountered:
- one Linux-oriented direct fetch hit `403` / Cloudflare:
  - `https://reverseengineering.stackexchange.com/questions/21597/can-i-trap-sigsegv-on-a-linux-and-what-are-are-the-conditions-to-make-it-works/21598`
- this did not block the run because the search-layer pass itself succeeded and Linux claims were kept conservative

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

## Files changed
- `index.md`
- `topics/exception-handler-owned-control-transfer-workflow-note.md`
- `sources/protected-runtime/2026-03-23-exception-handler-owned-control-transfer-notes.md`
- `sources/protected-runtime/2026-03-23-exception-handler-owned-control-transfer-search-layer.txt`
- `runs/2026-03-23-2120-reverse-kb-autosync.md`

## Commit / sync intent
If git reports KB changes, commit them and run:
- `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

## Outcome
Completed an external-research-driven KB maintenance pass that improved a thin protected-runtime practical branch with source-backed operator guidance, while also preserving branch-balance discipline and explicit search-audit reporting.
