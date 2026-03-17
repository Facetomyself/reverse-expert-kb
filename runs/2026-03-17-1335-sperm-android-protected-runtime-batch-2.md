# Run Report — 2026-03-17 13:35 Asia/Shanghai — `sperm/md` Android / protected-runtime batch 2

## Summary
This run continued the Android / protected-runtime deep pass and reviewed a second cluster focused on:
- anti-debug / anti-Frida thread and surface selection
- execution-assisted algorithm reconstruction with unidbg
- dynamic classloader and fake-so/jar localization for signing paths

As with batch 1, the run remained conservative:
- source-note first
- no premature canonical-topic edits yet

## Scope this run
- review another small high-value Android/protected-runtime subset
- extract durable workflow patterns instead of app-specific trivia
- preserve the results as a source note for later canonical synthesis

## Sources consulted
From `Facetomyself/sperm/tree/main/md`:
- `simpread-APP 逆向工程技巧——反调试检测线程.md`
- `simpread-frida 检测.md`
- `simpread-unidbg 算法还原术 · 某民宿 app 篇 · 上卷.md`
- `simpread-unidbg 算法还原术 · 某民宿 app 篇 · 中卷.md`
- `simpread-unidbg 算法还原术 · 某民宿 app 篇 · 下卷.md`
- `simpread-某 A 系电商 App x-sign 签名分析.md`

## New findings
### 1. The “closest stable cut-point” idea keeps showing up
The thread anti-debug article gives a concrete example: do not stop at `pthread_create`; go to thread-start handoff and attribute by payload function.
This fits the KB’s broader observation-surface selection logic very well.

### 2. Anti-Frida should be treated as a bundle of detection surfaces
The short anti-Frida checklist article is still useful because it gathers many detector families into one compact map:
- threads
- maps/fd/readlink
- task names
- ports/D-Bus/process scanning
- hook opcode checks
- breakpoint checks
- `ptrace`
- checksum / integrity
- `libart` / `libc` verification

This is stronger than talking about “Frida detection” as if it were one trick.

### 3. unidbg contributes most when framed as execution-assisted reduction
The unidbg trilogy is not most valuable as a library tutorial.
It is valuable because it demonstrates a repeatable workflow:
- validate path in live target
- emulate enough environment to execute the native path
- hook internal transforms
- recover preimages, keys, IVs, and mode choices
- reduce the full algorithm into a reproducible implementation

### 4. True-path localization often precedes useful native reversing
The x-sign article reinforces the importance of localizing the real Java/native boundary first, including dynamic classloaders and fake-so jars, before spending effort on full native reconstruction.

## Reflections / synthesis
After two Android/protected-runtime batches, a more stable theme is emerging:
- **strong mobile reversing is often about choosing the right cut-point into the execution graph**.

Batch 1 emphasized lower-boundary observation surfaces.
Batch 2 emphasizes:
- thread bootstrap cut-points
- classloader/plugin cut-points
- intermediate-transform cut-points during execution-assisted algorithm recovery

That is a very healthy sign for the KB because it keeps the material workflow-centered instead of tool- or sample-centered.

## Candidate topic pages to create or improve
No canonical topic pages were edited this run.

Likely future canonical targets after another one or two Android batches:
- `topics/android-observation-surface-selection-workflow-note.md`
- `topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- a possible new workflow note for execution-assisted native algorithm reconstruction

## Next-step research directions
Continue Android/protected-runtime while momentum is still coherent.
Good next families from `sperm/md` likely include:
- app signing / parameter recovery variants
- environment/pinning/trust-path material
- linker / load-path notes
- hybrid Java/native or unidbg/chomper-style execution assistance

## Concrete scenario notes or actionable tactics added this run
This run preserved several reusable tactics in the new source note, including:
- thread-start handoff interception instead of obvious `pthread_create` hooking
- anti-Frida decomposition into detector surfaces
- execution-assisted algorithm reduction under partial environment reconstruction
- dynamic-classloader localization before deep plugin/native analysis

## Files changed this run
- `research/reverse-expert-kb/sources/mobile-runtime-instrumentation/2026-03-17-sperm-android-protected-runtime-batch-2-notes.md`
- `research/reverse-expert-kb/runs/2026-03-17-1335-sperm-android-protected-runtime-batch-2.md`

## Outcome
The reverse KB now has a second Android/protected-runtime extraction note from the `sperm/md` repository, focused on anti-Frida surface decomposition, thread-start cut-points, execution-assisted algorithm recovery, and dynamic-classloader path localization.
