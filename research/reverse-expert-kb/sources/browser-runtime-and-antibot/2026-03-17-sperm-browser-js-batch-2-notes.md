# Source Notes — 2026-03-17 — `sperm/md` Browser / JS anti-bot batch 2

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-Js Ast 一部曲：高完整度还原某 V5 的加密.md`
- `simpread-Js Ast 二部曲：某 V5 “绝对不可逆加密” 一探究竟.md`
- `simpread-ast 自动扣 webpack 脚本实战_渔滒的博客 - CSDN 博客.md`
- `simpread-JS 逆向系列 22 - 彻底解决前端无限 debugger.md`
- `simpread-所有无限 debugger 的原理与绕过.md`
- `simpread-监控、定位 JavaScript 操作 cookie - 『脱壳破解区』  - 吾爱破解 - LCG - LSG _ 安卓破解 _ 病毒分析 _ www.52pojie.cn.md`

## Why these articles were grouped together
This batch coheres around the **code-plane** of browser anti-bot work:
- **before you can emulate or replay a hostile web client, you often need to make the delivered code legible, executable, and observable enough to recover where cookies/signatures/guards actually originate**

The shared themes are:
- AST-guided deobfuscation and structural restoration
- webpack extraction / module recovery
- infinite-debugger neutralization
- cookie-write localization and monitoring
- turning hostile code blobs into smaller debuggable artifacts

## Strong recurring ideas

### 1. AST work is most valuable as structure recovery, not just pretty-printing
The AST articles are strongest when read as a workflow for recovering **analysis structure**:
- decrypt string tables
- inline object indirections
- normalize member access
- recover flattened control flow
- collapse no-argument IIFEs into sequential code
- restore a debuggable, step-through-capable artifact

That is more important than cosmetic beautification.
The goal is a surrogate program whose control and data flow are once again inspectable.

### 2. Browser deobfuscation often works by removing orchestration noise, not re-deriving every primitive
The AST/V5 articles repeatedly show the same move:
- keep the core decryption/decode primitive around if it is already understood or callable
- remove the surrounding layers of indirection, object wrappers, flow flattening, and encoding noise
- turn the code into a smaller legible artifact

This is similar to earlier Android batches: not every primitive needs full symbolic understanding if it can be safely reduced into a stable callable component.

### 3. Webpack extraction is a dependency-recovery problem
The webpack article is useful because it frames “扣 webpack” as:
- identify loader/runtime bundle
- identify target module bundles/chunks
- mix them into a standalone artifact
- then patch the missing browser environment or missing dependencies only as needed

This is strong KB material because many modern browser targets are not monolithic JS files but dependency graphs hidden behind bundler/runtime structure.

### 4. Infinite debugger defense is really execution-hostility management
The debugger articles are not just about deleting `debugger;`.
They map several distinct hostility forms:
- explicit `debugger` statements in visible code
- `setTimeout` / `setInterval` loops
- `eval`-constructed debugger payloads
- `Function` and `Function.prototype.constructor` generated VM scripts
- anti-hook checks using `toString` / native-code appearance

This is valuable because it reframes the issue as a family of **execution-hostility channels** rather than one keyword problem.

### 5. Some anti-debug channels are best neutralized by changing the debugging topology, not by patching one sink
The debugger material also produces a useful selection rule:
- sometimes patching or replacing the source file is fine
- sometimes hooking `eval` / `Function` / `constructor` is enough
- sometimes ignoring anonymous eval/VM scripts in the debugger is operationally cleaner
- sometimes local overrides / source replacement win over broad hooks because broad hooks cause scope or fidelity problems

That matches the broader cross-branch theme already emerging in the KB: topology choice matters.

### 6. Cookie generation is best localized by observing writes, not by reading the whole codebase linearly
The cookie-monitor article is strong because it encourages a better workflow than “search the entire obfuscated bundle manually”:
- hook `document.cookie` writes early
- classify add/update/delete events
- filter by cookie name or regex
- break only when the interesting cookie changes
- climb the call stack from the actual write site

This is a very high-leverage browser workflow and should likely become canonical.

### 7. Browser code-plane work often aims to expose one consequence-bearing write or one export-bearing module
Across the AST, webpack, debugger, and cookie-monitoring material, a repeated expert objective appears:
- expose the first meaningful write (cookie/signature/token)
- or recover the smallest module/export set that produces it
- instead of statically “understanding the whole site”

That is exactly the kind of reduction-first framing the KB wants.

## Concrete operator takeaways worth preserving

### A. Analysis-artifact restoration workflow for obfuscated web JS
Reusable sequence:
1. identify the smallest necessary decode/decrypt primitive(s)
2. inline or replace their call sites where safe
3. eliminate object-indirection shells and string-table noise
4. restore flattened control flow and sequentialize trivial IIFEs
5. stop when the artifact becomes debuggable and semantically navigable

### B. Webpack dependency-recovery workflow
Reusable sequence:
1. identify runtime/loader bundle
2. identify target module chunk(s)
3. identify any vendor/shared chunk dependencies
4. mix into a standalone execution artifact
5. patch missing browser globals or environment only after dependency closure is good enough

### C. Execution-hostility triage workflow for infinite debugger
Reusable sequence:
1. classify the channel:
   - explicit source `debugger`
   - timer-based loops
   - `eval`
   - `Function`
   - `Function.prototype.constructor`
   - anti-hook `toString` checks
2. choose the least damaging neutralization:
   - conditional breakpoint / ignore
   - local source replacement
   - `eval`/`Function` hook
   - toString/native-appearance protection
   - debugger setting/topology change
3. beware scope or fidelity loss from over-broad hooks

### D. Consequence-bearing cookie-write localization workflow
Reusable sequence:
1. hook `document.cookie` as early as possible
2. log add/update/delete events
3. filter for the target cookie by name or regex
4. break on the interesting event type only
5. climb the stack from the actual write instead of manually reading the entire obfuscated codebase first

### E. Export- or write-oriented browser reduction rule
Reusable rule:
- when browser code is bundled/obfuscated/hostile, aim first to recover the smallest export set or write site that owns the target artifact
- do not over-invest in total-program readability before you have the consequence-bearing edge

## Candidate KB implications
This batch strongly supports or suggests improvements to:
- browser-runtime and anti-bot subtree notes
- `topics/runtime-behavior-recovery.md`
- protected-runtime/deobfuscation branches, now with clear browser analogues

Potential future child-note opportunities:
- analysis-artifact restoration for obfuscated browser JS
- webpack dependency-recovery workflow note
- execution-hostility / infinite-debugger triage note
- cookie-write localization via hook-and-stack-climb workflow note

## Confidence / quality note
This is a very strong browser batch.
Its best contribution is that it makes browser-side reversing look less like “beautify and stare” and more like:
- recover a smaller artifact
- neutralize hostile execution channels
- hook the first consequence-bearing write
- extract only the dependency slice you actually need

That is excellent canonical-KB material later.
