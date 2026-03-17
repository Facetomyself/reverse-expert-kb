# Run Report — 2026-03-17 14:00 Asia/Shanghai — `sperm/md` Browser / JS anti-bot batch 1

## Summary
This run began the second major planned lane after Android/protected-runtime:
- **Browser / JS anti-bot**

The first browser batch focused on:
- environment patching / browser-runtime reconstruction
- Cloudflare challenge and turnstile style fingerprint surfaces
- TLS / JA3 transport identity
- the practical split between replay, impersonation, and native browser execution

As before, this was a source-first extraction pass with no canonical topic edits yet.

## Scope this run
- start the browser / JS branch with its densest cross-cutting themes
- extract durable workflows rather than one-off target recipes
- preserve the results as a source note and run report

## Sources consulted
From `Facetomyself/sperm/tree/main/md`:
- `simpread-Python 爬虫进阶必备 _ Js 逆向之补环境到底是在补什么？.md`
- `simpread-cloudflare 五秒盾 js 逆向分析.md`
- `simpread-curl_cffi 突破 Cloudflare 验证.md`
- `simpread-某某网站 JS 逆向及 tls 指纹绕过分析.md`
- `simpread-突破 tls_ja3 新轮子.md`

One intended browser-automation file name did not resolve cleanly during local file probe, but this did not block meaningful extraction from the rest of the batch.

## New findings
### 1. “补环境” should be reframed as runtime-shape reconstruction
The environment-patching material is much more valuable when interpreted this way than when treated as a bag of stubs.

### 2. Browser anti-bot checks often validate provenance and shape, not just field values
Descriptor, prototype, constructor, and function-identity checks matter enough that simple literals and hand-made objects are often structurally wrong even when their values look right.

### 3. Cloudflare-style systems are better modeled as broad environment-surface interrogators
The batch reinforces that cookies/tokens are downstream artifacts of a much larger runtime interrogation.

### 4. TLS/JA3 is an independent validation layer
Correct params and headers are not enough when the transport identity itself is judged.

### 5. A clean operator split emerges among replay, impersonated transport, and native browser execution
This is likely to be one of the most useful canonical lessons from the browser branch.

## Reflections / synthesis
The browser lane starts with a pleasing parallel to the Android lane.

Android protected-runtime work kept converging on:
- choosing the right cut-point, topology, and evidence surface.

Browser anti-bot work seems to converge on:
- choosing the right client topology and deciding which identity layers must be made coherent.

That symmetry is a good sign for later KB synthesis.

## Candidate topic pages to create or improve
No canonical topic pages were edited this run.

Likely future canonical targets after more browser batches accumulate:
- browser-runtime subtree topic notes
- anti-bot workflow notes around runtime reconstruction
- a possible note on transport identity as a separate validation layer
- a possible note on replay vs impersonation vs native-browser execution

## Next-step research directions
Continue the browser / JS lane while the clustering is still strong.
Good likely next families from `sperm/md` include:
- AST / deobfuscation and webpack module recovery
- slider / captcha / turnstile implementation cases
- browser automation / webdriver / CDP detection specifics
- cookie/sign generation under browser-runtime constraints

## Concrete scenario notes or actionable tactics added this run
This run preserved several reusable tactics in the new source note, including:
- runtime-shape reconstruction instead of simple global stubbing
- strict-surface-first anti-bot triage
- treating TLS/JA3 as a separate transport-identity layer
- selecting among replay, impersonation, and native-browser execution based on the failing layer

## Files changed this run
- `research/reverse-expert-kb/sources/browser-runtime-and-antibot/2026-03-17-sperm-browser-js-batch-1-notes.md`
- `research/reverse-expert-kb/runs/2026-03-17-1400-sperm-browser-js-batch-1.md`

## Outcome
The reverse KB now has its first Browser / JS anti-bot extraction note from the `sperm/md` repository, centered on runtime-shape reconstruction, Cloudflare-like environment probes, and transport identity as a separate validation layer.
