# Run Report — 2026-03-17 14:00 Asia/Shanghai — `sperm/md` Browser / JS anti-bot batch 2

## Summary
This run continued the browser / JS lane with a second cluster focused on the **code plane** of hostile web targets:
- AST-guided structural deobfuscation
- webpack dependency and module recovery
- infinite-debugger / anti-debug neutralization
- cookie-write monitoring and localization

This was another source-first extraction pass with no canonical topic edits yet.

## Scope this run
- examine the browser branch from the perspective of code legibility and observability
- extract workflow patterns rather than tool-brand recipes
- preserve them as a source note and run report

## Sources consulted
From `Facetomyself/sperm/tree/main/md`:
- `simpread-Js Ast 一部曲：高完整度还原某 V5 的加密.md`
- `simpread-Js Ast 二部曲：某 V5 “绝对不可逆加密” 一探究竟.md`
- `simpread-ast 自动扣 webpack 脚本实战_渔滒的博客 - CSDN 博客.md`
- `simpread-JS 逆向系列 22 - 彻底解决前端无限 debugger.md`
- `simpread-所有无限 debugger 的原理与绕过.md`
- `simpread-监控、定位 JavaScript 操作 cookie - 『脱壳破解区』  - 吾爱破解 - LCG - LSG _ 安卓破解 _ 病毒分析 _ www.52pojie.cn.md`

## New findings
### 1. AST work is best framed as analysis-artifact restoration
The point is not pretty-printing; it is restoring a tractable surrogate artifact whose control flow, call sites, and writes can be meaningfully inspected.

### 2. Webpack extraction is essentially dependency closure recovery
Runtime bundle + target chunk + vendor chunk + minimal environment patching is a reusable pattern.

### 3. Infinite debugger belongs in a broader execution-hostility taxonomy
`debugger`, timers, `eval`, `Function`, constructor tricks, and anti-hook `toString` checks form a coherent family of hostile execution channels.

### 4. Cookie generation is often best localized from the write site outward
This is much more efficient than reading the whole codebase linearly from the top.

### 5. Browser code-plane work repeatedly targets one meaningful write or export slice
This is highly compatible with the KB’s broader reduction-first philosophy.

## Reflections / synthesis
After two browser batches, the branch is already showing a nice internal structure.

Batch 1 focused on:
- runtime shape
- transport identity
- client topology

Batch 2 now adds:
- code-plane restoration
- execution-hostility management
- export/write localization

Together these make browser anti-bot work feel much more operator-centered and less like a grab-bag of tricks.

## Candidate topic pages to create or improve
No canonical topic pages were edited this run.

Likely future canonical targets after more browser batches accumulate:
- browser-runtime subtree notes
- a note on analysis-artifact restoration for obfuscated browser JS
- a note on execution-hostility / infinite-debugger triage
- a note on cookie-write localization
- a note on webpack dependency recovery

## Next-step research directions
Continue the browser / JS lane with likely next families including:
- protection-family-specific browser defenses (for example 瑞数 generations)
- captcha/slider practical workflows
- canvas/fingerprint masking
- browser automation / CDP / webdriver signal handling

## Concrete scenario notes or actionable tactics added this run
This run preserved several reusable tactics in the new source note, including:
- restoring a debuggable surrogate artifact via AST transforms
- treating webpack extraction as dependency recovery
- classifying infinite-debugger as execution hostility channels
- localizing cookie generation from write hooks and call stacks

## Files changed this run
- `research/reverse-expert-kb/sources/browser-runtime-and-antibot/2026-03-17-sperm-browser-js-batch-2-notes.md`
- `research/reverse-expert-kb/runs/2026-03-17-1400-sperm-browser-js-batch-2.md`

## Outcome
The reverse KB now has a second Browser / JS anti-bot extraction note from the `sperm/md` repository, focused on code-plane restoration, execution-hostility management, and consequence-bearing cookie/module localization.
