# Reverse KB Autosync Run Report — 2026-03-24 13:16 Asia/Shanghai

Mode: external-research-driven

## Summary
This run deliberately avoided another KB-internal sync-only pass and performed an explicit multi-source search attempt on a thinner protected-runtime practical seam.

Chosen seam:
- existing `exception-handler-owned-control-transfer` branch
- narrower operator gap: **dispatcher-side landing is only useful if the stack/context model is truthful enough to make unwind lookup and resume behavior comparable**

This was not a leaf-creation run.
That was intentional branch-balance discipline: this branch already has a good leaf, so the better maintenance move was to sharpen one stop rule inside the canonical page rather than inflate topic count.

## Direction review
Recent autosync history does **not** show stagnation into pure internal canonical-sync work.
There were already several external-research-driven runs across malware, protocol/firmware, and protected-runtime within the recent window.

The branch-balance risk here was different:
- protected-runtime already has enough density that it is easy to overfeed with near-duplicate micro-leaves
- browser/mobile remain easy branches to over-polish
- the highest-value move on this run was a **tight, source-backed canonical refinement** that materially improves operator stopping rules without multiplying pages

Why this seam still earned an external run:
- recent exception-handler work already covered dispatcher landing, dynamic function tables, and Linux signal-context mutation
- but the page still benefited from one more practical correction: **do not treat an IDA-style guessed dispatcher prototype or shallow API label as truth when the stack/context landing layout itself determines whether later unwind ownership even makes sense**
- this is concrete, re-findable, and useful in real Windows exception-owned-control-transfer cases

## Work completed
### Canonical KB refinement
Updated:
- `topics/exception-handler-owned-control-transfer-workflow-note.md`
- `topics/protected-runtime-practical-subtree-guide.md`

What changed in the canonical page:
- strengthened the Windows dispatcher-side landing section with a practical caution that guessed signatures / API labels can be misleading
- made the stop rule more concrete: the landing is useful when it explains one `RtlLookupFunctionEntry` / unwind decision or one later resume edge well enough to predict behavior
- added concrete compare-pair ideas around guessed-register-argument models vs observed dispatcher-side stack/layout realism
- emphasized that the useful analyst object may be the landing layout plus one later lookup/resume consequence, not the dispatcher name alone

What changed in the subtree guide:
- the start condition for the exception-handler branch now explicitly includes cases where the dispatcher-side stack/context layout itself determines whether unwind ownership looks truthful

### Source-note hygiene / drift repair
Updated:
- `sources/protected-runtime/2026-03-24-exception-owned-control-transfer-source-note.md`

Reason:
- an existing same-day source note incorrectly recorded Grok as successful
- this run corrected that audit trail so the KB does not later mistake a degraded-source run for a full three-source-success run

### Search artifact
Created / refreshed:
- `sources/protected-runtime/2026-03-24-exception-owned-control-transfer-search-layer.txt`

## Why this was a worthwhile KB improvement
This run improved the KB itself rather than just accumulating notes because it tightened a recurring practical failure mode:
- analysts can already suspect VEH/SEH or dispatcher ownership
- but still lose time because their mental model of `KiUserExceptionDispatcher` arrival is too shallow or signature-shaped
- that makes unwind lookup, runtime ownership, or resume behavior look incoherent when the real issue is the landing model itself

The KB now preserves a stronger operator rule:
- dispatcher landing is infrastructure unless it yields one truthful lookup/resume consequence
- if unwind behavior still looks nonsense, verify landing-layout realism before widening into more exception-family theory

That is practical and case-driven, not just wording polish.

## External research used
Primary retained anchors for this refinement:
- Microsoft Learn — Structured Exception Handling Functions
- Microsoft Learn — `RtlInstallFunctionTableCallback`
- man7 — `sigaction(2)`
- Maurice’s Blog — `KiUserExceptionDispatcher`
- search-layer multi-source results around VEH / unwind / signal-context handling

Conservative synthesis retained in the KB:
- official Windows docs justify treating dynamic function tables and unwind lookup as first-class runtime ownership surfaces
- practitioner material justifies using `KiUserExceptionDispatcher` / dispatcher landing as a re-findable anchor
- but the analyst should not over-trust guessed prototypes when the stack/context landing shape is what makes later unwind behavior intelligible

## Search audit
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- exa
- tavily

Failed sources:
- grok
  - actual failure observed during explicit invocation: `502 Server Error: Bad Gateway for url: http://proxy.zhangxuemin.work:8000/v1/chat/completions`

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Degraded-source-set note:
- this run **did** perform a real explicit multi-source search attempt with `--source exa,tavily,grok`
- execution was degraded in practice to **Exa + Tavily** because Grok returned repeated 502 errors
- because Exa and Tavily returned enough practical signal, the run continued conservatively and recorded the degradation here

## Files changed
- `topics/exception-handler-owned-control-transfer-workflow-note.md`
- `topics/protected-runtime-practical-subtree-guide.md`
- `sources/protected-runtime/2026-03-24-exception-owned-control-transfer-source-note.md`
- `sources/protected-runtime/2026-03-24-exception-owned-control-transfer-search-layer.txt`
- `runs/2026-03-24-1316-reverse-kb-autosync.md`

## Commit / sync status
Planned after report write:
- commit KB changes if diff is non-empty
- run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

## Bottom line
This was a real external-research-driven run.
It did not create a new leaf because branch-balance discipline made canonical refinement the better move.
The practical gain is a sharper stop rule for Windows exception-owned-control-transfer cases: do not stop at dispatcher naming or guessed signatures; stop when the landing model explains one real unwind or resume consequence.
