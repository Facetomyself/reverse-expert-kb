# 2026-03-22 iOS mitigation-aware replay-repair notes

## Scope
External-research support note for adding a narrower iOS practical continuation for **PAC-shaped replay-close failures**.

Goal of this note:
- preserve the required explicit multi-source search attempt
- support a practical workflow note for cases where callback family / broad owner choice are already plausible enough
- keep claims conservative and operator-facing rather than turning PAC into a hardware-survey branch

## Search shape
Search was run through `search-layer` with explicit multi-source selection:
- `--source exa,tavily,grok`

Queries:
1. `iOS arm64e PAC callback replay authenticated pointer dyld shared cache reversing`
2. `arm64e pointer authentication callback block invoke reverse engineering iOS`
3. `dyld shared cache arm64e PAC reverse engineering callback dispatch runtime landing`

Why these queries:
- bias toward replay-close / callback-context / runtime-landing repair rather than generic PAC theory
- keep dyld shared cache truth in scope because replay-repair claims are weak if the code view itself is untruthful
- force overlap between pointer-authentication vocabulary and operator symptoms like callback invoke drift, landing mismatch, and replay-close failure

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
- none at invocation time

Endpoints used on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Artifacts:
- `sources/mobile-runtime-instrumentation/2026-03-22-ios-pac-replay-repair-search-layer.txt`

## High-signal sources actually used

### 1. Apple pointer-authentication documentation
- URL: <https://developer.apple.com/documentation/security/preparing-your-app-to-work-with-pointer-authentication>

Why it mattered:
- supports the conservative baseline that pointer-auth failure is surfaced like memory corruption
- justifies a workflow rule that sharp replay failure at a callback / indirect boundary does **not** automatically mean wrong owner or wrong callback family

Operator takeaway extracted:
- if replay is already structurally close, treat pointer/context/materialization mismatch as a live possibility before rewriting the whole owner story

Limitation:
- baseline context only, not a reverse-engineering workflow source by itself

### 2. `ipsw` dyld shared cache guide
- URL: <https://blacktop.github.io/ipsw/docs/guides/dyld>

Why it mattered:
- directly reinforces that arm64e / PAC-bearing pointer views in dyld shared cache analysis need cache-truthful tooling and slide-aware interpretation
- useful for the workflow step that freezes cache/build/image/slide assumptions before stronger replay-repair claims

Operator takeaway extracted:
- if replay repair depends on one callback or dispatch target inside cache-backed code, preserve the exact cache/build/slide view and do not mix extracted-image guesses with runtime anchors casually

Limitation:
- tool-guidance, not a replay methodology by itself

### 3. Binary Ninja arm64e PAC cleanup plugin
- URL: <https://github.com/bdash/bn-arm64e-pac>

Why it mattered:
- supports a practical distinction between decluttered route views and raw auth-bearing sequences
- useful when a replay-close case is blocked by not knowing whether the remaining drift is really in the authenticated boundary or in one missing object/context/setup obligation nearby

Operator takeaway extracted:
- use decluttered views for routing, but preserve the raw auth-bearing edge for replay-repair classification

Limitation:
- tool/version specific; supports a heuristic rather than a universal truth claim

### 4. NowSecure dyld shared cache reversing material
- URL: <https://www.nowsecure.com/blog/2024/09/13/reversing-ios-system-libraries-using-radare2-a-deep-dive-into-dyld-cache-part-3/>
- supporting context: <https://www.nowsecure.com/blog/2024/09/11/reversing-ios-system-libraries-using-radare2-a-deep-dive-into-dyld-cache-part-1/>

Why it mattered:
- reinforces that modern iOS system/private-framework truth often lives in the dyld shared cache and not in stale standalone images
- helps justify a replay-repair workflow that freezes one runtime landing and one cache-truthful code view before making stronger missing-obligation claims

Operator takeaway extracted:
- replay-repair should begin from one truthful runtime landing plus one cache-truthful code view, not from the prettiest extracted-image pseudocode

Limitation:
- not specifically about callback replay; used as workflow support for truth-surface discipline

### 5. PAC background used cautiously
- Project Zero PAC background: <https://projectzero.google/2019/02/examining-pointer-authentication-on.html>
- USENIX Apple PAC paper: <https://www.usenix.org/system/files/usenixsecurity23-cai-zechao.pdf>

Why they mattered:
- they support only the weak claim that PAC behavior and modifier/context handling are nontrivial enough that simplistic replay diagnosis is risky

Conservative takeaway extracted:
- do not collapse replay-close arm64e failures into a single generic story; preserve family-vs-context-vs-code-view-vs-missing-obligation distinctions

Limitation:
- background only; not used as the main source of step-by-step operator claims here

## Search results considered but treated cautiously

### 1. RPAC / exploit-chain / anecdotal PAC posts
Examples returned included:
- exploitation-oriented PAC/RPAC analysis
- issue trackers or anecdotal crash discussions
- general PAC explanation posts

Why they were treated cautiously:
- useful for background pressure, but not tightly aligned with the specific operator task of truthful replay repair in an already narrowed iOS reversing case
- many are exploit- or internals-focused rather than workflow-focused

Conservative use:
- supports only the idea that modifier/context assumptions matter and that replay-like substitution can fail for reasons not visible in pretty pseudocode

### 2. Generic reversing / training pages
Why they were not central:
- too broad to anchor concrete replay-repair claims
- retained only as weak context for runtime-first discipline

## Practical synthesis preserved for the KB page
The new workflow note should keep only these conservative claims:

1. once a modern iOS case is already **replay-close**, the next best move is often to classify the remaining gap as one of:
   - wrong-family after all
   - wrong authenticated context / pointer-context mismatch
   - lying code view
   - missing narrower runtime obligation
2. the strongest evidence pattern is one truthful runtime landing plus one compare pair, not broader tracing
3. when the family is already plausible, bias toward proving one missing object/materialization/init obligation before rewriting broad owner logic again
4. preserve both:
   - a cache-truthful / runtime-truthful route view
   - the raw auth-bearing edge needed for classification
5. stop once the case can be rewritten as one smaller replay-repair task with one downstream proof target

## What this run deliberately did not claim
- that every replay-close arm64e failure is caused by PAC itself
- that search results alone can diagnose a precise pointer-auth modifier problem
- that exploitation-focused PAC research should drive the KB’s operator workflow language
- that replay repair always beats owner re-checking

## Best next follow-on if future case pressure appears
If later runs produce concrete case pressure, the best next additions would be:
- one small cookbook section around compare-pair design for replay-close callback/context failures
- one dyld-cache-to-runtime-anchor case note for private-framework callback families
- one narrower note on object provenance / callback materialization under arm64e-aware runtime conditions
