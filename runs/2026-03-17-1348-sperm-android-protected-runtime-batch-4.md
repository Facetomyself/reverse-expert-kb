# Run Report — 2026-03-17 13:48 Asia/Shanghai — `sperm/md` Android / protected-runtime batch 4

## Summary
This run continued the Android / protected-runtime deep pass with a fourth cluster centered on:
- sign / parameter recovery
- execution-assisted transform extraction with unidbg and unicorn
- OLLVM/indirect-branch reduction
- compact external reproduction of protected request-sign pipelines

This was another source-first batch with no canonical topic edits yet.

## Scope this run
- review a high-value sign/parameter-recovery subset
- extract reusable workflows rather than app/vendor-specific trivia
- preserve the results as a KB source note

## Sources consulted
From `Facetomyself/sperm/tree/main/md`:
- `simpread-App 逆向百例 _ 19 _ 某 App Sign 完整分析.md`
- `simpread-大猿搜题 sign so 加密参数分析｜unidbg.md`
- `simpread-[原创] 记一次 unicorn 半自动化逆向——还原某东 sign 算法.md`
- `simpread-使用 Unidbg 模拟执行去除 OLLVM-BR 混淆.md`
- `simpread-逆向某物 App 登录接口：抓包分析 + Frida Hook 还原加密算法.md`
- `simpread-逆向某物 App 登录接口：还原 newSign 算法全流程.md`

## New findings
### 1. Sign recovery is best understood as a staged reduction pipeline
The best articles do not begin by brute-forcing native code. They localize path ownership, then recover transform structure, then write a minimal reproduction.

### 2. Differential-input execution is one of the highest-leverage techniques in this source set
The use of one-hot / single-bit / all-zero baseline inputs to infer permutation and transform rules is repeatedly effective and highly reusable.

### 3. unidbg/unicorn matter most when extracting structure, not just invoking functions
The strongest use of controlled execution in this batch is table extraction, branch resolution, case separation, and intermediate-state capture.

### 4. OLLVM-BR style control-flow obstruction can often be reduced without full static cleanup
Resolve edges dynamically, patch back into direct flow, and only then return to static tooling. This is a very practical pattern worth preserving.

### 5. The true terminal artifact is a minimal faithful reimplementation
The best end-state is not “we understand the app.” It is “we can reproduce the output from compact external code and document where the constants/tables came from.”

## Reflections / synthesis
After four Android/protected-runtime batches, the branch now has a clear practical identity.

It is not just about Android reversing in general.
It is about this recurring expert move:
- **reduce protected execution into one smaller trustworthy object by choosing the right cut-point, the right evidence surface, and the right differential experiment.**

Batch 4 is especially strong because it demonstrates that principle on sign/parameter recovery, where people often get trapped in literal decompiler reading.

## Candidate topic pages to create or improve
No canonical topic pages were edited this run.

Likely future canonical targets after more accumulation:
- `topics/runtime-behavior-recovery.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- a new note on execution-assisted sign/parameter recovery
- a new note on differential-input transform extraction
- a new note on indirect-branch recovery under OLLVM-BR-like obfuscation

## Next-step research directions
Android lane is now mature enough that the next pass can either:
- continue mining remaining Android sign/protection cases,
- or begin synthesizing cross-batch canonical notes before switching to browser/JS.

Given the user's instruction to keep going without interruption, continuing Android mining first is still reasonable.

## Concrete scenario notes or actionable tactics added this run
This run preserved several reusable tactics in the new source note, including:
- sign-path localization before cryptographic assumptions
- execution-assisted structure extraction with differential inputs
- tail-case / remainder-path transform recovery
- OLLVM-BR indirect-branch reduction via controlled emulation
- minimal faithful sign-pipeline reproduction as the actual recovery endpoint

## Files changed this run
- `research/reverse-expert-kb/sources/mobile-runtime-instrumentation/2026-03-17-sperm-android-protected-runtime-batch-4-notes.md`
- `research/reverse-expert-kb/runs/2026-03-17-1348-sperm-android-protected-runtime-batch-4.md`

## Outcome
The reverse KB now has a fourth Android/protected-runtime extraction note from the `sperm/md` repository, focused on execution-assisted sign recovery, differential transform extraction, and deobfuscation by structure recovery rather than literal control-flow reading.
