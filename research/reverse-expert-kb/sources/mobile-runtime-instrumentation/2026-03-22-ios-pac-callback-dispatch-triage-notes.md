# 2026-03-22 iOS PAC-shaped callback / dispatch triage notes

## Scope
External-research support note for the autosync run that adds a narrower practical continuation under the iOS PAC/arm64e branch for callback / dispatch failure triage.

Goal of this note:
- preserve the real multi-source search attempt required by the autosync policy
- separate genuinely usable operator signals from noisy or weakly grounded search returns
- support a conservative workflow note on PAC-shaped callback / dispatch failures rather than a hardware-theory page

## Search shape
Search was run through `search-layer` with explicit multi-source selection:
- `--source exa,tavily,grok`

Queries:
1. `iOS arm64e PAC callback block invoke reverse engineering workflow`
2. `iOS pointer authentication callback function pointer dispatch reverse engineering`
3. `arm64e PAC block invoke callback crash reverse engineering dyld shared cache`

Why these queries:
- bias toward callback / dispatch / invoke failures rather than generic PAC theory
- force overlap between arm64e/PAC terminology and operator-facing runtime symptoms
- keep dyld shared cache in scope because callback targets often become ambiguous at cache-backed boundaries

## Search audit snapshot
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- exa
- tavily
- grok

Failed sources:
- none at search invocation time

Endpoints used on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Ephemeral search capture:
- `/tmp/reverse_kb_search_20260322.txt`

## High-signal supporting sources actually used

### 1. Apple pointer-authentication documentation
- URL: <https://developer.apple.com/documentation/security/preparing-your-app-to-work-with-pointer-authentication>

Why it mattered:
- provides the conservative baseline that pointer authentication is normal arm64e behavior on Apple platforms
- explicitly supports the operator reminder that authentication failure is surfaced like memory corruption, which explains why callback/dispatch failures are easy to misclassify too broadly

Operator takeaway extracted:
- when callback or function-pointer invocation fails sharply on arm64e, do not jump straight from "crash" to "wrong owner"; first preserve the possibility that the family is right but the authenticated pointer/context pairing is not

Limitation:
- does not provide reverse-engineering workflow detail by itself
- used as baseline context only

### 2. Binary Ninja arm64e PAC cleanup plugin
- URL: <https://github.com/bdash/bn-arm64e-pac>

Why it mattered:
- directly shows a practical failure mode in analysis: explicit PAC/auth-check sequences before tail calls can dominate the decompiler output and obscure the meaningful target edge
- supports a callback/dispatch-specific workflow because analysts can otherwise treat auth scaffolding as the semantic dispatch site

Operator takeaway extracted:
- when triaging one crashing callback/dispatch boundary, preserve both views:
  - the decluttered view for quick routing
  - the raw auth-bearing sequence for failure classification
- do not let decompiler clutter turn mitigation scaffolding into the presumed owner

Limitation:
- tool/version specific
- supports a heuristic, not a universal rule

### 3. NowSecure dyld shared cache reversing series, part 1
- URL: <https://www.nowsecure.com/blog/2024/09/11/reversing-ios-system-libraries-using-radare2-a-deep-dive-into-dyld-cache-part-1/>

Why it mattered:
- reinforces that modern iOS system-library truth often lives in the dyld shared cache rather than in standalone extracted dylibs
- directly matters to callback/dispatch failure triage because static call targets and runtime landings become misleading if the code view is not cache-truthful

Operator takeaway extracted:
- if the failing callback/dispatch path crosses system/private framework code, freeze the exact cache/build/image view before making stronger claims about wrong targets or wrong callback families

Limitation:
- not callback-specific by itself
- used to support the code-view truthfulness step in the workflow

### 4. Practical iOS Reverse Engineering training overview
- URL: <https://ringzer0.training/countermeasure25-practical-ios-reverse-engineering/>

Why it mattered:
- while not a deep PAC source, it usefully reinforces the practical importance of asynchronous programming, tracing control flow with Frida, and moving between static and dynamic views on iOS
- this supports a workflow note centered on callback/dispatch boundaries rather than purely static PAC theory

Operator takeaway extracted:
- callback/dispatch triage should stay runtime-anchored: freeze one representative async path, then compare one no-failure and one failure boundary instead of widening into many possible callbacks

Limitation:
- training overview, not a proof-heavy technical source
- used only as weak supporting context for workflow emphasis

## Search results considered but treated cautiously

### 1. Search-layer returns naming specific PAC callback crash anecdotes and blogs
Examples returned by search included:
- Apple forum / crash-discussion style results
- generic blog posts describing PAC callback failures
- GitHub issues around dyld shared cache PAC handling

Why they were treated cautiously:
- search snippets alone are not enough to anchor durable KB claims
- many appear anecdotal, environment-specific, or not directly retrievable in a trustworthy way during this run

Conservative use:
- they support only the weak claim that callback / function-pointer failures around PAC are a recurring practical confusion surface
- they were not used as primary evidence for prescriptive crash semantics

### 2. Project Zero, Black Hat, and USENIX PAC research
Why they were not central:
- useful for background on PAC internals and Apple-specific implementation details
- but the current KB gap is operator triage, not a hardware-research survey

Conservative use:
- supports only the claim that PAC behavior is nontrivial enough that simplistic callback-crash diagnosis is risky
- not used as the main source of step-by-step workflow claims here

## Practical synthesis preserved for the KB page
The narrower callback/dispatch note should keep only these conservative claims:

1. once a modern iOS case has already narrowed into one authenticated callback / dispatch boundary, the first task is to classify the boundary, not to widen tracing
2. useful classification buckets are:
   - wrong family / wrong owner
   - right family, wrong authenticated pointer/context pair
   - right family, but code view is lying
   - replay-close path missing one init/table/image obligation
3. decompiler PAC scaffolding and cache-extraction distortions can make analysts overstate the meaning of one visible dispatch site
4. the best proof pattern is one boundary, one compare pair, one runtime landing, and one downstream effect
5. once the callback/dispatch boundary is reduced, route quickly back into owner proof, replay repair, runtime-table/init-obligation recovery, or result-to-policy consequence work

## What this run deliberately did not claim
- that every callback crash on arm64e is PAC-auth failure
- that authenticated-pointer failure can be diagnosed reliably from search snippets alone
- that the note should prescribe bypass techniques or offensive PAC manipulation
- that asynchronous or block-based code is itself PAC-specific

## Best next follow-on if future case pressure appears
If later runs produce more concrete case pressure, the next still-practical additions would be:
- one narrower note on PAC-shaped replay-close vs missing-init obligation repair
- one case-driven dyld-cache-to-runtime-anchor note for private-framework callback families
- one small cookbook section on block / closure / callback landing confirmation under arm64e-aware runtime conditions
