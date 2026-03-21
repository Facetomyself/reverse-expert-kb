# 2026-03-21 arm64e / PAC mitigation-aware iOS reversing notes

## Scope
External-research support note for the autosync run that adds a practical iOS continuation page for PAC / arm64e-aware reversing.

Goal of this note:
- preserve the source set actually used
- separate high-signal operator takeaways from weaker/noisier search returns
- support conservative synthesis into a concrete workflow note rather than a theory-heavy PAC page

## Search shape
Search was run through `search-layer` with explicit multi-source selection:
- `--source exa,tavily,grok`

Queries:
1. `iOS arm64e PAC reverse engineering practical workflow pointer authentication branch target recovery`
2. `iOS pointer authentication PAC debugger reversing crash branch target workflow arm64e`
3. `arm64e PAC reverse engineering dyld shared cache practical tips iOS`

Why these queries:
- bias toward practical workflow rather than pure hardware-theory papers
- pull dyld-shared-cache/operator material alongside PAC terminology
- surface tool-facing materials that help distinguish mitigation scaffolding from business logic

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
- `/tmp/reverse-kb-search-20260321-2216.txt`

## High-signal supporting sources actually used

### 1. Apple pointer-authentication documentation
- URL: <https://developer.apple.com/documentation/security/preparing-your-app-to-work-with-pointer-authentication>

Why it mattered:
- confirms the arm64e / pointer-authentication baseline on Apple platforms
- supports conservative wording that authenticated pointers are a normal workflow reality on modern iOS rather than an exotic corner

Operator takeaway extracted:
- when a modern iOS case reaches indirect-branch / return / callback failure around arm64e-era paths, PAC-awareness is part of normal analysis hygiene

Limitation:
- weak for reverse-engineering workflow detail by itself
- used only as baseline context, not as a workflow source alone

### 2. `ipsw` dyld shared cache guide
- URL: <https://blacktop.github.io/ipsw/docs/guides/dyld/>

Why it mattered:
- strongly reinforces dyld shared cache as an operational truth surface for modern Apple-platform reversing
- exposes practical cache facts such as arm64e cache identity, image extraction, symbol/objc lookup, address translation helpers, and authenticated patch listings

Operator takeaway extracted:
- if the path runs through system libraries/private frameworks/cache-backed code, the dyld shared cache should be treated as a primary truth surface, not an afterthought
- cache/build provenance should be frozen in notes because address interpretation depends on it

Limitation:
- tool-specific examples should not be overgeneralized into a universal workflow
- still strong enough to support a cache-first practical note

### 3. NowSecure dyld shared cache reversing series, part 1
- URL: <https://www.nowsecure.com/blog/2024/09/11/reversing-ios-system-libraries-using-radare2-a-deep-dive-into-dyld-cache-part-1/>

Why it mattered:
- gives practitioner framing that iOS system libraries live meaningfully inside the dyld shared cache and that navigating the cache is core workflow, not niche trivia
- supports the KB’s emphasis on truth surfaces before stronger semantic claims

Operator takeaway extracted:
- if the analyst is arguing from system-library code on iOS, they should verify that the code view is cache-truthful before promoting owner/crash claims

Limitation:
- still not a PAC-specific page
- used here mainly to support the cache-truthfulness part of the workflow

### 4. Binary Ninja arm64e PAC cleanup plugin
- URL: <https://github.com/bdash/bn-arm64e-pac>

Why it mattered:
- directly illustrates a recurring practical issue: explicit PAC checks before tail calls can pollute higher-level IL/decompiler views
- useful for teaching the distinction between mitigation scaffolding and semantic owner logic

Operator takeaway extracted:
- cleanup may reduce clutter, but the analyst should preserve a path back to the raw auth-bearing sequence when crash classification or edge proof depends on it
- not every visible PAC-related instruction sequence is the analyst’s real target

Limitation:
- tool/version specific and narrow in scope
- should support a heuristic, not become the whole page

## Search results considered but treated cautiously

### Apple PAC / Four Years Later, Demystifying Pointer Authentication on Apple M1
Why they were not central:
- valuable background on deeper PAC internals
- but this run’s goal was a practical iOS workflow note, not a PAC research survey

Conservative use:
- they support the claim that mitigation-aware reasoning is real and nontrivial
- they were not used as primary anchors for specific operator workflow steps in the KB page

### Various GitHub issues / crash anecdotes / blog posts on pointer-auth failures
Why they were treated cautiously:
- useful for reminding that PAC-like failures are often operationally confusing
- but too anecdotal or environment-specific to anchor broad KB rules cleanly

Conservative use:
- support only the weak claim that analysts often misclassify these failures
- do not prove universal diagnosis rules

## Practical synthesis preserved for the KB page
The practical page intentionally keeps only a narrow set of claims:

1. modern iOS reversing can hit a point where PAC/arm64e awareness becomes part of the workflow
2. the first job is usually to keep the code view truthful, especially around dyld shared cache realities
3. the analyst must separate:
   - view problems
   - failure-classification problems
   - replay-is-close / missing-init-context problems
4. some explicit PAC-related decompiler clutter is not the business owner and should not be overpromoted semantically
5. once the mitigation-aware boundary is reduced, the case should route back into owner proof, black-box replay, or runtime-table/init-obligation recovery quickly

## What this run deliberately did not claim
- that PAC explains every arm64e-era crash
- that decompiler cleanup is always safe
- that the external sources above fully explain Apple’s hidden PAC implementation
- that a dedicated hardware-research page is the right next step for the KB

## Best next follow-on if future case pressure appears
If later runs produce more concrete case pressure, the next additions that would still be practical are:
- one narrower note on PAC-shaped callback/dispatch failure triage
- one narrower note on mitigation-aware replay failure versus missing-init obligation
- one case-driven dyld-cache-to-runtime-anchor continuation for iOS system/private-framework paths
