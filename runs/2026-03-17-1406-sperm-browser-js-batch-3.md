# Run Report — 2026-03-17 14:06 Asia/Shanghai — `sperm/md` Browser / JS anti-bot batch 3

## Summary
This run continued the browser / JS lane with a third cluster focused on:
- family-specific browser protection analysis (especially 瑞数/Botgate 4.x and 5.x)
- artifact pipelines for cookies and URL suffixes
- fingerprint-dependent artifact construction
- detector-aware canvas spoofing
- slider/captcha recovery as a data-path problem
- broader layered risk-control framing

This remained a source-first extraction pass with no canonical topic edits yet.

## Scope this run
- move from generic browser anti-bot concepts into protection-family-specific case structure
- preserve reusable workflows rather than site/vendor trivia
- add another source note and run report for later synthesis

## Sources consulted
From `Facetomyself/sperm/tree/main/md`:
- `simpread-人均瑞数系列，瑞数 4 代 JS 逆向分析.md`
- `simpread-人均瑞数系列，瑞数 5 代 JS 逆向分析.md`
- `simpread-某瑞数 5 代 cookie 和 url 后缀补环境代码.md`
- `simpread-Canvas 指纹隐藏实战.md`
- `simpread-【网页逆向】chan 妈妈滑块 ast 反混淆.md`
- `simpread-JS 逆向 _ 某行业大佬对坑风控的一些经验总结.md`

## New findings
### 1. Browser protection families can be modeled by artifact pipelines
The 瑞数 material is especially useful when reduced to challenge bootstrap -> VM/state acquisition -> cookie/suffix generation -> request rewriting.

### 2. `$_ts`-style state needs indirection recovery
These families often cannot be replayed reliably until their remapped state slots and method indirections are understood.

### 3. Some fingerprint surfaces participate in artifact construction, not just validation
This is a crucial distinction for deciding what can be stubbed and what must be faithfully reproduced.

### 4. Canvas spoofing must be detector-aware
Prototype fidelity, readout stability, and known-pixel checks matter enough that naive random-noise plugins are often trivially detected.

### 5. Slider/captcha tasks often collapse into data-path recovery
Scaling, timing, path serialization, and final encryption are the decisive layers much more often than “pretend to be human” UI theatrics.

### 6. The layered risk-control rule is a useful guardrail
Proxy/network reputation, then client environment, then behavior remains a practical triage order.

## Reflections / synthesis
After three browser batches, the branch now has a clearer structure:
- batch 1: runtime shape / transport identity / client topology
- batch 2: code-plane restoration / execution hostility / cookie/module localization
- batch 3: protection-family artifact pipelines / detector-aware spoofing / layered risk-control framing

That is a very healthy progression.
The browser branch is starting to feel as coherent as the Android branch did after several batches.

## Candidate topic pages to create or improve
No canonical topic pages were edited this run.

Likely future canonical targets after more browser accumulation:
- family-specific browser protection notes
- runtime reconstruction / detector-aware spoofing notes
- a note on browser artifact pipelines (cookie, suffix, sign)
- a note on layered risk-control triage

## Next-step research directions
Continue the browser / JS lane with likely next families including:
- more captcha / recognition articles
- browser automation / webdriver / CDP signal handling
- cookie/signature generation under packed browser-runtime constraints
- any remaining browser-side protection-family notes in the source set

## Concrete scenario notes or actionable tactics added this run
This run preserved several reusable tactics in the new source note, including:
- modeling protection families by emitted artifact pipelines
- recovering state-object indirection before replay
- separating fingerprint validation from artifact construction
- detector-aware, session-stable canvas spoofing
- treating slider/captcha flows as data-path recovery problems

## Files changed this run
- `research/reverse-expert-kb/sources/browser-runtime-and-antibot/2026-03-17-sperm-browser-js-batch-3-notes.md`
- `research/reverse-expert-kb/runs/2026-03-17-1406-sperm-browser-js-batch-3.md`

## Outcome
The reverse KB now has a third Browser / JS anti-bot extraction note from the `sperm/md` repository, centered on protection-family artifact pipelines, detector-aware fingerprint spoofing, and browser-side risk-control layering.
