# acw_sc__v2 Cookie Bootstrap / Consumer-Path Notes

Date: 2026-03-14
Topic: browser runtime anti-bot family, cookie bootstrap, request-path localization, environment-sensitive execution
Prepared from: search-layer results, limited web fetches, and KB cross-synthesis

## Scope
These notes support a practical KB page on `acw_sc__v2`-style browser protection flows.

The goal is not to describe every implementation detail of every site using the family.
The goal is to preserve the most reusable analyst observations for cases where:
- a challenge/bootstrap JS runs before the protected request can succeed
- a cookie such as `acw_sc__v2` is set or refreshed client-side
- the practical problem is to locate the bootstrap path, cookie write path, and first request that actually depends on the cookie

## Sources consulted

### Search-layer results
1. Sechub mirror / discussion:
   - https://sechub.in/view/2850259
   - Title signal: `【JS逆向】前程无忧cookie逆向，acw_sc__v2，阿里系算法分析大全`
   - Usefulness: confirms the family is actively discussed as a cookie-oriented JS reverse target.

2. Aliyun developer community article:
   - https://developer.aliyun.com/article/1597002
   - Title: `前程无忧搜索接口JS 逆向：阿里系acw_sc__v2和Sign加密`
   - Usefulness: confirms a concrete real-site pattern where `acw_sc__v2` and another signed request parameter coexist.
   - Fetch quality this run: low; readability extraction exposed only title/metadata.

3. Aliyun XZ article / known cluster result:
   - https://xz.aliyun.com/t/14872
   - Search-layer summary: notes important algorithm iterations and key function traits.
   - Fetch quality this run: failed to extract.
   - Usefulness: supports treating the family as evolving wrapper/algorithm practice rather than one frozen recipe.

4. Search-layer result on anti-analysis pressure:
   - BlackHatWorld discussion summary on `acw_sc__v2`
   - Usefulness: suggests recurring friction around hooked XHR/fetch, Proxy/global traps, and prototype integrity assumptions.
   - Reliability: lower than official docs; treat as practitioner orientation only.

## Practical target shape distilled from the source cluster
A recurring `acw_sc__v2` shape looks like this:

```text
initial page or protected endpoint response
  -> bootstrap / challenge JS executes
  -> browser computes or unlocks cookie state
  -> cookie write occurs (acw_sc__v2 or related state)
  -> subsequent request replays with cookie present
  -> server either accepts path or serves next-stage challenge/failure
```

What matters in practice is often not full algorithm prettification first.
It is recovering:
1. where the bootstrap JS is introduced
2. where the cookie is written
3. which first request actually depends on the cookie
4. whether the cookie alone is enough, or whether sibling request state also changes

## Reusable analyst observations

### 1. This family rewards cookie-bootstrap tracing before deep deobfuscation
Many analysts over-rotate into beautifying obfuscated JS too early.
For this family, a higher-yield first step is often:
- map the response that introduces the bootstrap logic
- map the first cookie write
- map the first consumer request that becomes accepted only after that write

### 2. The cookie write path is a stronger anchor than raw string search
Searching all bundles for `acw_sc__v2` can help, but the better anchor is usually:
- `document.cookie` write path
- the response handler that triggers it
- the request-finalization boundary where the now-present cookie changes server behavior

### 3. The first accepted request matters more than the first visible cookie
Analysts can stall after proving that the cookie exists.
The stronger artifact is:

```text
bootstrap response
  -> cookie write
  -> first request that now changes server response class
```

That request is the real consumer-path milestone.

### 4. Coexisting signed parameters are a practical warning sign
At least one concrete source title (`acw_sc__v2` + `Sign`) suggests that analysts should not assume:
- cookie solved = request solved

Instead, verify whether accepted behavior depends on:
- cookie only
- cookie plus signed query/body/header fields
- cookie plus timing/session order

### 5. Environment assumptions may be lighter than full browser-fingerprint families, but still matter
The source cluster suggests this family often sits between two extremes:
- not purely a static arithmetic porting problem
- not always as environment-heavy as the broadest browser fingerprint families

Practical implication:
- test whether the path fails due to missing JS runtime assumptions, request sequencing, or integrity-sensitive observation before committing to a large browser-clone effort

### 6. Anti-analysis pressure should be treated as workflow risk, not mythology
Search-layer results mention:
- hooked XHR/fetch detection
- Proxy/global traps
- prototype integrity checks

Whether or not every claim generalizes, the practical takeaway is solid:
- compare a minimal-observation run against a heavier hook run
- if the cookie path appears to change only under instrumentation, downgrade trust in the evidence channel

## Concrete workflow cues to preserve in the KB
- start at the first challenge/bootstrap response, not random bundle search
- hook or breakpoint `document.cookie` writes
- correlate the cookie write with the next protected request and next server response class
- compare cookie-only success hypothesis against cookie-plus-sibling-field hypothesis
- log whether retry / reload / new session changes the cookie path
- prefer a compact consumer-path artifact over a long static dump

## Suggested provenance use in KB pages
This source note is best used to support:
- a concrete workflow note on `acw_sc__v2` cookie bootstrap and consumer-path localization
- back-links from browser parameter-path localization and browser token-generation pages

## Evidence quality note
- Strongest evidence this run: repeated practitioner/topic-cluster signals that `acw_sc__v2` is a cookie-bootstrap-centric browser target family.
- Weaker evidence this run: exact algorithm details from pages with poor fetch extraction.
- Therefore the KB page should stay workflow-centered and evidence-conscious, avoiding overclaiming undocumented internals.
