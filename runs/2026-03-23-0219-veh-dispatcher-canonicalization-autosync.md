# Reverse KB Autosync Run Report — 2026-03-23 02:19 Asia/Shanghai

Mode: external-research-driven

## Scope this run
This run focused on a thinner protected-runtime practical continuation rather than another broad browser/mobile or index-only maintenance pass.

Chosen scope:
- strengthen the existing `exception-handler-owned-control-transfer` branch with a more practical Windows refinement
- preserve dispatcher-side landing and unwind-lookup thinking as a concrete analyst object
- improve the KB itself rather than producing only detached notes
- keep the change branch-balanced by extending a thinner protected-runtime continuation instead of feeding the already-dense browser/mobile micro-branches

Files improved this run:
- `topics/exception-handler-owned-control-transfer-workflow-note.md`
- `topics/protected-runtime-practical-subtree-guide.md`
- `sources/protected-runtime/2026-03-23-veh-dispatcher-search-layer.txt`

## New findings
Retained external signals from this run reinforced a practical Windows refinement:
- official VEH documentation remains useful for grounding the idea that exception routing and context-based resume are real first-class control surfaces rather than just background runtime machinery
- dispatcher-side landing around `KiUserExceptionDispatcher` / `RtlDispatchException` is often a better analyst object than generic “VEH/SEH exists” wording
- unwind lookup and dynamic function-table ownership give a more truthful next boundary when registration is already known but branch ownership is still diffuse
- practitioner material still supports a conservative operator rule: once one landing/lookup boundary plus one consequence-bearing resume or state action is good enough, leave broad exception theory

## Sources consulted
Primary retained sources:
- Microsoft Learn — Vectored Exception Handling
  - `https://learn.microsoft.com/en-us/windows/win32/debug/vectored-exception-handling`
- Maurice’s Blog — A journey through KiUserExceptionDispatcher
  - `https://momo5502.com/posts/2024-09-07-a-journey-through-kiuserexceptiondispatcher/`
- practitioner/community search hits around dispatcher-side landing, unwind lookup, and exception-owned control transfer
  - including `RtlDispatchException`, `RtlLookupFunctionEntry`, Reverse Engineering Stack Exchange discussions, and x64 SEH/unwind writeups surfaced by search-layer

Search artifact captured:
- `sources/protected-runtime/2026-03-23-veh-dispatcher-search-layer.txt`

## Reflections / synthesis
The important KB improvement here was not “create yet another Windows exceptions page.”

The real gap was narrower:
- the branch already had the right leaf
- the leaf and subtree guide needed a more re-findable practical refinement
- the KB needed a stop rule that discourages getting stuck at API presence or broad exception folklore

The most useful preserved rule from this run is:
- when a protected Windows case already smells exception-owned, do not stop at “VEH/SEH exists”
- prefer the smallest truthful boundary:
  - vectored registration if it already predicts the branch
  - otherwise dispatcher-side landing
  - otherwise one concrete unwind lookup / `RtlLookupFunctionEntry` region
  - otherwise runtime-installed function-table ownership for generated code
- then stop broad exception theory once one ownership boundary and one consequence-bearing resume/state action are good enough

That is practical operator value, not just terminology cleanup.

## Candidate topic pages to create or improve
Improved this run:
- `topics/exception-handler-owned-control-transfer-workflow-note.md`
- `topics/protected-runtime-practical-subtree-guide.md`

Candidate follow-ups, but not urgent enough to force this run into more leaf creation:
- a protected-runtime continuation specifically for runtime-installed function-table / generated-code unwind ownership if multiple future runs produce enough case-driven evidence
- a later cross-branch comparison note connecting protected-runtime dispatcher-side landing with runtime-evidence first-anchor selection

## Next-step research directions
Best next directions after this run:
- keep biasing toward thinner practical continuations, not easy browser/mobile branch feeding
- look for other underfed but still operator-useful bridges such as:
  - firmware/protocol continuation pages that connect parser/state proof to one narrower hardware-side effect or deferred completion edge
  - malware practical bridges that sharpen first-consumer proof without drifting into generic malware taxonomy
  - native/runtime-evidence cross-branch continuation where one runtime anchor cleanly hands back into ordinary route/state proof
- avoid spending several consecutive runs on wording/index/family-count-only maintenance unless navigation drift is actually blocking practical additions

## Concrete scenario notes or actionable tactics added this run
Added or materially reinforced in canonical KB pages:
- dispatcher-side landing in `KiUserExceptionDispatcher` / `RtlDispatchException` as a practical Windows anchor
- the rule that registration alone may be too abstract, and one landing/lookup boundary is often the better ownership proof object
- explicit use of `RtlLookupFunctionEntry` / unwind-region selection as a stop-short-of-theory next move
- branch routing language in the protected-runtime subtree guide now explicitly includes dispatcher-side landing, not only registration/unwind/signal wording
- cleanup of a previously corrupted duplicated tail in the exception-handler page, improving canonical stability rather than leaving broken drift in place

## Branch-balance review
Current branch picture from recent runs still looks healthy in frequency but needs steering discipline in topic choice.

Recent concentration pattern:
- strong recent activity exists across protected-runtime, iOS, malware, native, protocol, and runtime-evidence
- browser/mobile are still structurally among the easiest branches to overfeed, even when the last several runs were not exclusively browser/mobile
- protected-runtime is also becoming easier to overfeed if every follow-up stays inside anti-instrumentation / exception / VM micro-variants without cross-branch handoff discipline

What this run did well:
- chose a thinner protected-runtime refinement rather than browser/mobile easy-mode growth
- improved a canonical page and subtree guide instead of only adding another detached leaf
- turned external research into practical operator language

What still needs watching:
- protected-runtime now has enough density that future runs should avoid endless internal micro-variant accumulation
- protocol/firmware, runtime-evidence, and malware should continue receiving practical continuation work when they present a thinner but high-value bottleneck
- branch maintenance should keep preferring one smaller trustworthy proof boundary over more family naming or taxonomy spread

## Search audit
Search sources requested: exa,tavily,grok
Search sources succeeded: exa,tavily,grok
Search sources failed: none
Exa endpoint: `http://158.178.236.241:7860`
Tavily endpoint: `http://proxy.zhangxuemin.work:9874/api`
Grok endpoint: `http://proxy.zhangxuemin.work:8000/v1`

Queries used:
- `vectored exception handler control transfer reverse engineering anti debugging`
- `windows exception dispatcher KiUserExceptionDispatcher RtlDispatchException reverse engineering`
- `malware VEH anti-debug exception handler control flow analysis`

Notes on source quality:
- all three requested sources were actually invoked and returned results for this run
- some surfaced results were too offense-oriented or too generic; they were not promoted into the KB unless they supported a conservative analyst-workflow claim
- SonicWall/other practitioner material was useful as search signal but not necessary as a canonical anchor once Microsoft + dispatcher/unwind-oriented sources covered the core practical rule

## Commit / sync
Planned after report write:
- commit reverse-KB changes if diff remains non-empty
- run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
- if sync fails, preserve local progress and leave the failure recorded here
