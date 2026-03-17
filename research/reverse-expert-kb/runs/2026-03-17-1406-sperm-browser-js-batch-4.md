# Run Report — 2026-03-17 14:06 Asia/Shanghai — `sperm/md` Browser / JS anti-bot batch 4

## Summary
This run continued the browser / JS lane with a fourth cluster focused on:
- observability-first browser-environment patching
- reusable environment frameworks rather than one-off stubs
- staged browser challenge pipelines like JSL / 加速乐
- compact signature generation paths like `__ac_signature`
- transport-stack selection for JA3/HTTP2-sensitive targets

This remained a source-first extraction pass with no canonical topic edits yet.

## Scope this run
- move the browser branch from family analysis toward concrete engineering workflow
- preserve stack-selection and escalation lessons rather than one-off library trivia
- add another source note and run report for later synthesis

## Sources consulted
From `Facetomyself/sperm/tree/main/md`:
- `simpread-js 破解之补浏览器环境的两种监控方式.md`
- `simpread-js 逆向之模拟浏览器环境 _ 范昌锐的博客.md`
- `simpread-js 逆向 --jsl mfw.md`
- `simpread-js 逆向) 某音 cookie 中的__ac_signature.md`
- `simpread-好库推荐 _ 两个解决 ja3 检测的 Python 库，强烈推荐.md`
- `simpread-深度剖析 ja3 指纹及突破.md`

## New findings
### 1. Environment reconstruction should usually start with observation
Proxy-based access monitoring is a compact but powerful workflow precursor to serious补环境 work.

### 2. Environment frameworks are cumulative infrastructure
Prototype fidelity, safe/native-looking functions, and proxy tooling are reusable investments, not target-specific hacks.

### 3. Some browser challenges are better approached as staged artifact pipelines
The JSL material is especially useful here.

### 4. Manual execution success is not the same as server-verification success
The `__ac_signature` material strongly supports escalating to a stronger harness when manual stubs execute but still fail verification.

### 5. JA3-sensitive targets often force stack selection, not just parameter tuning
This is a practical engineering lesson that should transfer beyond the specific libraries mentioned in the source set.

## Reflections / synthesis
After four browser batches, the branch is now showing the same kind of maturity the Android branch reached earlier.

The browser line now covers:
- identity layers (runtime/transport/topology)
- code-plane restoration and consequence-bearing writes
- protection-family artifact pipelines
- engineering escalation from observation to stronger harnesses and transport stacks

That is a healthy, workflow-centered structure for later canonical synthesis.

## Candidate topic pages to create or improve
No canonical topic pages were edited this run.

Likely future canonical targets after more browser accumulation:
- runtime reconstruction / environment observation notes
- family-artifact-pipeline notes
- verification-failure escalation note
- transport-stack selection note for JA3/HTTP2-sensitive targets

## Next-step research directions
The browser branch is now rich enough that the next work can proceed in either of two ways:
- mine one more browser/captcha cluster for completeness,
- or switch to the planned protocol/network branch and later synthesize browser material canonically.

Given the standing instruction to keep going without interruption, continuing to process the remaining major branches is appropriate.

## Concrete scenario notes or actionable tactics added this run
This run preserved several reusable tactics in the new source note, including:
- observability-first environment reconstruction
- treating environment frameworks as reusable infrastructure
- staged browser challenge pipeline modeling
- verification-failure escalation to stronger sandboxes/harnesses
- transport-stack selection for JA3/HTTP2-sensitive targets

## Files changed this run
- `research/reverse-expert-kb/sources/browser-runtime-and-antibot/2026-03-17-sperm-browser-js-batch-4-notes.md`
- `research/reverse-expert-kb/runs/2026-03-17-1406-sperm-browser-js-batch-4.md`

## Outcome
The reverse KB now has a fourth Browser / JS anti-bot extraction note from the `sperm/md` repository, focused on observability-first environment reconstruction, staged browser challenge pipelines, and transport-stack selection under verification pressure.
