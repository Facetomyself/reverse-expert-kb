# Run Report — 2026-03-17 13:48 Asia/Shanghai — `sperm/md` Android / protected-runtime batch 3

## Summary
This run continued the Android / protected-runtime deep pass with a third cluster focused on:
- anti-capture and transport hardening
- transport-boundary selection for traffic recovery
- protocol downgrade / path forcing (QUIC, SPDY, proprietary transport)
- shell/security-so anti-Frida bypass at constructor/loader boundaries
- Java-hook-side-effect detection as a distinct problem

The run stayed conservative and source-first.
No canonical topic pages were edited yet.

## Scope this run
- review another tightly related Android/protected-runtime subset
- extract durable workflow shapes rather than app-specific recipes
- preserve the results as a KB-ready source note

## Sources consulted
From `Facetomyself/sperm/tree/main/md`:
- `simpread-如何实现 Android App 的抓包防护？又该如何绕过？一文看懂攻防博弈 __ CYRUS STUDIO.md`
- `simpread-[原创]android 抓包学习的整理和归纳.md`
- `simpread-字节系, ali 系, ks,pdd 最新抓包方案.md`
- `simpread-某查线路 app 设备检测逆向分析.md`
- `simpread-过某加固 Frida 检测.md`
- `simpread-绕过 libxxxxsec.so 对 Frida hook Java 层的检测.md`

## New findings
### 1. Packet capture is better modeled as layered evidence recovery than as a single tool choice
These sources strongly reinforce the need to classify packet recovery by boundary: business-layer, framework, Java socket, SSL plaintext, native socket, MITM, or lower network capture.

### 2. Modern capture failure is often due to path choice, not just visibility failure
QUIC/SPDY/proprietary-channel forcing or downgrade repeatedly appears as the decisive move before ordinary analysis can continue.

### 3. Anti-capture frequently begins with environment classification
Frida detection, VPN/tun detection, Wi-Fi state classification, and other environment gates often determine whether traffic recovery is possible at all.

### 4. Security-shell bypass often belongs at constructor or loader time
The security-so articles make a strong case that `.init_proc` / `JNI_OnLoad` / constructor neutralization can be a higher-leverage move than symptom-by-symptom patching.

### 5. Java-hook-side-effect detection should be separated from generic Frida detection
The prettyMethod / Java.perform / Java.use side-effect problem deserves its own branch in the KB instead of being buried under generic “Frida detection.”

## Reflections / synthesis
After three Android/protected-runtime batches, the branch is cohering around a strong operator-centered theme:
- **pick the right cut-point and the right boundary before trying to understand the whole target**.

Batch 1 emphasized lower-boundary observation surfaces.
Batch 2 emphasized thread-start cut-points, dynamic classloader localization, and execution-assisted reduction.
Batch 3 now adds:
- transport-boundary selection
- transport-path forcing
- environment-classification-first anti-capture logic
- security-so constructor-boundary bypass

This is excellent KB material because it stays concrete and workflow-oriented.

## Candidate topic pages to create or improve
No canonical topic pages were edited this run.

Likely later targets after more Android batches accumulate:
- `topics/android-observation-surface-selection-workflow-note.md`
- `topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- a possible new note on transport-boundary selection for mobile traffic recovery
- a possible new note on security-so constructor-boundary bypass

## Next-step research directions
Continue the Android lane while the material is still clustering naturally.
Good next article families from `sperm/md` likely include:
- sign / parameter recovery cases
- hybrid execution (unidbg/unicorn/chomper) sign recovery
- linker / load-path / SO repair cases
- app-specific protected-sign practical workflows

## Concrete scenario notes or actionable tactics added this run
This run preserved several reusable tactics in the new source note, including:
- transport-boundary selection
- transport-path forcing through QUIC/SPDY downgrade or config rewrite
- environment-classification-first anti-capture debugging
- security-so constructor / loader-time bypass
- separating Java-hook-side-effect detection from generic Frida detection

## Files changed this run
- `research/reverse-expert-kb/sources/mobile-runtime-instrumentation/2026-03-17-sperm-android-protected-runtime-batch-3-notes.md`
- `research/reverse-expert-kb/runs/2026-03-17-1348-sperm-android-protected-runtime-batch-3.md`

## Outcome
The reverse KB now has a third Android/protected-runtime extraction note from the `sperm/md` repository, focused on anti-capture workflows, transport-boundary selection, transport-path forcing, and constructor-boundary bypass of security components.
