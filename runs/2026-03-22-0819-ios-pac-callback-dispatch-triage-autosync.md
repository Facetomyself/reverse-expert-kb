# Reverse KB Autosync Run — 2026-03-22 08:19 Asia/Shanghai

Mode: external-research-driven

## Scope this run
This run deliberately avoided another internal-only wording/index sync and instead used the required explicit multi-source search pass to deepen a thinner but still practical iOS branch.

Chosen scope:
- review branch balance and recent run concentration
- perform a real external-research attempt through `search-layer --source exa,tavily,grok`
- extend the iOS practical branch with a narrower continuation page for PAC-shaped callback / dispatch failure handling
- update nearby branch-routing pages so the new note is navigable and canonically placed
- write the run report, then commit and sync the reverse KB if KB files changed

## New findings
The strongest useful finding from this run was not a new hardware-level PAC claim; it was a branch-shape finding:
- the KB already had a broad mitigation-aware iOS continuation (`arm64e-pac-and-mitigation-aware-ios-reversing.md`)
- recent branch text and source notes had already identified a likely next gap around **PAC-shaped callback/dispatch failure families**
- that narrower gap was now concrete enough to justify a real workflow note rather than another broad branch-shape comment

Practical additions made this run:
- added `topics/ios-pac-shaped-callback-and-dispatch-failure-triage.md`
- added supporting source note `sources/mobile-runtime-instrumentation/2026-03-22-ios-pac-callback-dispatch-triage-notes.md`
- updated nearby iOS/mobile routing pages to point at the narrower continuation

The new note keeps the problem small and operator-oriented:
- freeze one callback / dispatch boundary
- classify it conservatively as:
  - wrong-family
  - wrong-context / authenticated-pointer-context mismatch
  - lying-code-view
  - replay-close / missing-obligation
- prove one runtime landing and one compare pair
- route quickly back out into owner proof, replay repair, runtime-table/init-obligation work, or result-to-policy consequence work

## Sources consulted
Primary external/useful sources:
- Apple pointer-authentication documentation
  - <https://developer.apple.com/documentation/security/preparing-your-app-to-work-with-pointer-authentication>
- Binary Ninja arm64e PAC cleanup plugin
  - <https://github.com/bdash/bn-arm64e-pac>
- NowSecure dyld shared cache reversing article
  - <https://www.nowsecure.com/blog/2024/09/11/reversing-ios-system-libraries-using-radare2-a-deep-dive-into-dyld-cache-part-1/>
- Practical iOS Reverse Engineering training overview
  - <https://ringzer0.training/countermeasure25-practical-ios-reverse-engineering/>
- background-only / not central to workflow claims:
  - USENIX pointer-authentication presentation page
  - search returns for anecdotal PAC callback crash discussions and dyld/PAC issue threads

Internal/canonical sources consulted:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent `research/reverse-expert-kb/runs/*.md`
- `topics/ios-practical-subtree-guide.md`
- `topics/arm64e-pac-and-mitigation-aware-ios-reversing.md`
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`
- `topics/ios-chomper-owner-recovery-and-black-box-invocation-workflow-note.md`
- `topics/ios-result-callback-to-policy-state-workflow-note.md`
- `sources/mobile-runtime-instrumentation/2026-03-21-arm64e-pac-mitigation-aware-ios-notes.md`

## Reflections / synthesis
This was a good example of the anti-stagnation rule doing useful work.

Without that rule, it would have been easy to spend this run on another internal branch-shape cleanup or top-level wording pass. But recent runs had already been strong on internal KB maintenance and native practical growth, so the better move was to do a real external-research-driven pass on a thinner iOS practical seam.

The resulting synthesis is intentionally conservative:
- PAC-shaped callback/dispatch failures are a **classification** problem before they are a theory problem
- the most important discipline is keeping the code view and runtime landing truthful
- the note does not pretend every callback crash on arm64e is PAC-auth failure
- it also does not let analysts flatten these failures into generic corruption or generic wrong-owner stories too early

That is practical operator value: one smaller decision surface, not a wider theory survey.

## Candidate topic pages to create or improve
Created this run:
- `topics/ios-pac-shaped-callback-and-dispatch-failure-triage.md`

Improved this run:
- `topics/ios-practical-subtree-guide.md`
- `topics/arm64e-pac-and-mitigation-aware-ios-reversing.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`

Still-plausible future additions:
- a narrower mitigation-aware replay-repair note for PAC-shaped replay-close failures that are clearly not wrong-family cases
- a dyld-cache-to-runtime-anchor cookbook note for private-framework callback families
- a small operator cookbook section for block / closure / callback landing confirmation under arm64e-aware runtime conditions

## Next-step research directions
Near-term good directions:
- watch whether future iOS case pressure clusters more around callback/dispatch classification or around replay-close missing-obligation repair
- if multiple future runs confirm the latter, add the second narrow mitigation-aware replay-repair continuation hinted by the subtree guide
- keep iOS practical growth case-driven and avoid turning PAC/arm64e into an abstract hardware-research branch detached from operator workflows

Broader branch-balance direction:
- continue resisting over-concentration in already-dense browser anti-bot and mobile protected-runtime subtrees
- keep using external-research-driven runs to deepen thinner but practical branches when the last few runs have tilted too far toward internal upkeep

## Concrete scenario notes or actionable tactics added this run
The new practical note adds these concrete tactics:
- freeze one callback / dispatch boundary rather than many neighboring PAC-looking sites
- separate four failure classes explicitly:
  - wrong-family
  - right-family/wrong-context
  - lying-code-view
  - replay-close/missing-obligation
- prefer one runtime landing and one compare pair over prettier pseudocode
- treat cache-truthful system-code views as primary when the path crosses dyld shared cache backed code
- preserve both decluttered and raw auth-bearing views when decompiler PAC cleanup changes readability
- route out quickly once the boundary is classified instead of letting mitigation-aware callback confusion consume the whole case

## Search audit
Search sources requested: `exa,tavily,grok`

Search sources succeeded: `exa,tavily,grok`

Search sources failed: `none`

Exa endpoint: `http://158.178.236.241:7860`

Tavily endpoint: `http://proxy.zhangxuemin.work:9874/api`

Grok endpoint: `http://proxy.zhangxuemin.work:8000/v1`

Queries used:
- `iOS arm64e PAC callback block invoke reverse engineering workflow`
- `iOS pointer authentication callback function pointer dispatch reverse engineering`
- `arm64e PAC block invoke callback crash reverse engineering dyld shared cache`

Notes on search quality:
- the multi-source search attempt was real and all three requested sources returned results
- Grok supplied several plausible-looking PAC/callback references, but many were anecdotal or snippet-only and were therefore treated conservatively
- Exa and Tavily were more useful for stable retrieval of GitHub/tooling, dyld-cache workflow material, and higher-signal operator-facing pages
- one direct `web_fetch` attempt for a Project Zero Blogger URL returned a 404/blog-not-found path during this run, so that source was not promoted into the canonical workflow claims

## Branch-balance review
Recent branch pattern:
- multiple very recent autosync runs have been active in native practical areas and runtime-evidence/operator-proof style topics
- historically the KB has also been dense in browser anti-bot / request-signature and mobile protected-runtime / WebView challenge-loop work
- iOS practical reversing is stronger than it was a week ago, but still thinner than the densest branches and still benefits from narrow, operator-first continuations

Balance judgment this run:
- this run was correctly spent on iOS practical branch deepening rather than more browser/mobile canonical sync
- choosing a PAC-shaped callback/dispatch triage seam met the anti-stagnation rule well because it produced a concrete continuation page rather than only index/wording repairs
- the new page keeps iOS practical growth case-driven instead of broadening into abstract PAC taxonomy

Current branch-strength impression:
- strong: browser anti-bot/request-signature; mobile protected-runtime/WebView; growing native practical workflows
- medium and improving: iOS practical reversing
- still relatively weaker overall: protocol/firmware practical workflows, desktop native workflows at the same level of case density, and malware/deobfuscation practical continuations

## Files changed
KB files changed this run:
- `research/reverse-expert-kb/topics/ios-pac-shaped-callback-and-dispatch-failure-triage.md` (new)
- `research/reverse-expert-kb/sources/mobile-runtime-instrumentation/2026-03-22-ios-pac-callback-dispatch-triage-notes.md` (new)
- `research/reverse-expert-kb/topics/ios-practical-subtree-guide.md`
- `research/reverse-expert-kb/topics/arm64e-pac-and-mitigation-aware-ios-reversing.md`
- `research/reverse-expert-kb/topics/mobile-reversing-and-runtime-instrumentation.md`

## Commit / sync status
Pending at report write time:
- commit KB changes if the working tree remains limited to the intended reverse-KB files
- run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

Best-effort note:
- `.learnings/ERRORS.md` handling was not required for this run; any such logging remains best-effort only
