# Run Report — 2026-03-17 13:54 Asia/Shanghai — `sperm/md` Android / protected-runtime batch 5

## Summary
This run continued the Android / protected-runtime deep pass with a fifth cluster focused on:
- initialized-image-aware repair of protected native artifacts
- CRC and integrity-view bypass by shadowing detector-visible memory views
- control-flow-flattening restoration through dynamic exploration and patching
- risk-SDK collection-graph reconstruction
- environment-detection surface inventories for hostile Android runtimes
- anti-debug neutralization as a precursor to sign analysis

This was another source-first batch with no canonical topic edits yet.

## Scope this run
- review a coherent Android/protected-runtime subset around integrity and environment modeling
- extract durable workflows rather than product-specific notes
- preserve the results as a KB source note

## Sources consulted
From `Facetomyself/sperm/tree/main/md`:
- `simpread-App 逆向百例 _ 18 _ 某 A 系防护 SO 跳转修复.md`
- `simpread-初探 android crc 检测及绕过.md`
- `simpread-控制流平坦化反混淆（春节红包活动 Android 高级题） - 『移动安全区』  - 吾爱破解 - LCG - LSG _ 安卓破解 _ 病毒分析 _ www.52pojie.cn.md`
- `simpread-某风控 SDK 逆向分析 _ AshenOne.md`
- `simpread-【Fireyer】一款 Android 平台环境检测应用 _ iofomo _ Open-source organization.md`
- `simpread-【安卓逆向】安居客反调试与参数分析.md`

## New findings
### 1. Initialized-image analysis is a recurring necessity, not an edge case
The branch-repair article shows that raw-file restoration can simply be wrong when runtime initialization mutates the data needed for branch-target computation.

### 2. Integrity bypass by view shadowing is one of the clearest reusable patterns in the repo
The CRC article demonstrates a very strong operator tactic: build a detector-visible clean shadow rather than trying to silence every integrity function.

### 3. Hostile-environment collection is best treated as a surface inventory
The Fireyer and risk-SDK articles give enough breadth to support a more systematic Android hostile-runtime observation matrix in the KB.

### 4. Risk SDKs are often collection graphs more than single algorithms
Modeling config, collectors, field mapping, serialization, and upload paths separately is much more effective than reading everything linearly.

### 5. Sign analysis and environment stabilization remain tightly coupled
The Anjuke case reinforces the pattern that anti-debug neutralization and SSL/visibility stabilization often precede meaningful parameter recovery.

## Reflections / synthesis
After five Android/protected-runtime batches, the branch now has very strong thematic cohesion.

The recurring expert move is no longer just “find the right hook.”
It is:
- **pick the right object, boundary, and evidence surface so that the protected system becomes reducible.**

Batch 5 is important because it extends that principle from sign and anti-Frida work into:
- initialized images
- integrity-view shadowing
- hostile-runtime surface matrices
- large risk-SDK collection graphs

## Candidate topic pages to create or improve
No canonical topic pages were edited this run.

Likely later canonical targets after synthesis:
- `topics/runtime-behavior-recovery.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md`
- a possible new note on integrity-view shadowing
- a possible new note on initialized-image-first branch repair
- a possible new note on Android hostile-runtime surface inventories

## Next-step research directions
The Android lane is now rich enough that the next work can proceed in either of two ways:
- mine one or two more Android clusters for completeness,
- or start limited canonical synthesis before switching to browser/JS.

Given the standing instruction to keep going without stopping, continuing to mine remaining Android high-signal material is still appropriate.

## Concrete scenario notes or actionable tactics added this run
This run preserved several reusable tactics in the new source note, including:
- initialized-image-first branch repair
- analysis-image restoration by dynamic branch/control-flow recovery
- integrity-view shadowing via maps/linker/section metadata redirection
- environment-surface inventory modeling
- risk-SDK collection-graph reconstruction

## Files changed this run
- `research/reverse-expert-kb/sources/mobile-runtime-instrumentation/2026-03-17-sperm-android-protected-runtime-batch-5-notes.md`
- `research/reverse-expert-kb/runs/2026-03-17-1354-sperm-android-protected-runtime-batch-5.md`

## Outcome
The reverse KB now has a fifth Android/protected-runtime extraction note from the `sperm/md` repository, focused on initialized-image repair, integrity-view shadowing, hostile-runtime surface modeling, and risk-SDK collection-graph recovery.
