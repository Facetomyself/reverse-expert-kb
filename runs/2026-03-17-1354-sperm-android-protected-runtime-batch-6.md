# Run Report — 2026-03-17 13:54 Asia/Shanghai — `sperm/md` Android / protected-runtime batch 6

## Summary
This run continued and effectively closed the first Android / protected-runtime lane with a sixth cluster focused on:
- non-root and embedded instrumentation topologies
- gadget-based loading instead of ordinary ptrace/spawn flows
- zygote/frida-server-topology avoidance
- framework-layer traffic interception in OkHttp/Retrofit
- UID-scoped transparent-proxy redirection using iptables and redsocks

This remains a source-first pass with no canonical topic edits yet.

## Scope this run
- review the remaining high-signal Android material around injection and network-path intervention
- extract durable workflow choices rather than tool-specific recipes
- preserve the results as a KB source note

## Sources consulted
From `Facetomyself/sperm/tree/main/md`:
- `simpread-09 - How to use frida on a non-rooted device — LIEF Documentation.md`
- `simpread-frida 免 root hook.md`
- `simpread-注入 frida-gadget 绕过 Frida 检测.md`
- `simpread-分析 okhttp3-retrofit2 - 截流某音通信数据.md`
- `simpread-安卓上基于透明代理对特定 APP 抓包 - SeeFlowerX.md`
- `simpread-iptables 在 Android 抓包中的妙用.md`

## New findings
### 1. Injection topology deserves to be a first-class analytical category
Changing from attach/spawn to embedded gadget loading can be more important than any later hook logic.

### 2. Some anti-Frida regimes are really anti-zygote or anti-server regimes
The zygisk-gadget material adds useful nuance beyond generic in-process artifact detection.

### 3. Android traffic recovery is now well supported across several cut-points in this source set
Earlier batches covered SSL/plaintext boundaries, downgrade, and anti-capture gates.
This batch adds a cleaner contrast between framework interception and transparent redirection.

### 4. UID-scoped transparent proxying is a strong stealthier alternative to ordinary proxy configuration
The iptables/redsocks approach is especially useful when the app inspects system proxy or VPN state.

## Reflections / synthesis
The Android lane now feels mature enough for later canonical synthesis.

Across six batches, the recurring practical identity is clear:
- **effective Android protected-runtime work is mostly about choosing the right topology, cut-point, and evidence surface so the target becomes reducible without overcommitting to one noisy method.**

The final batch helps close the loop by showing that this principle also applies to:
- how instrumentation arrives
- how traffic is redirected
- how much proxy visibility the app receives

## Candidate topic pages to create or improve
No canonical topic pages were edited this run.

Likely future canonical targets after synthesis:
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/android-observation-surface-selection-workflow-note.md`
- `topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md`
- a possible new note on injection-topology selection
- a possible new note on UID-scoped transparent-proxy capture

## Next-step research directions
With the Android lane now substantially mined, the next natural branch is the planned second major lane:
- **browser / JS anti-bot**

This matches the previously chosen overall sequence and can now begin cleanly.

## Concrete scenario notes or actionable tactics added this run
This run preserved several reusable tactics in the new source note, including:
- selecting instrumentation topology before hook tactics
- dependency-based gadget embedding for non-root or anti-server contexts
- separating zygote/frida-server detection from app-local artifact detection
- choosing between framework interception and transparent redirection for traffic recovery
- UID-scoped transparent-proxy redirection with fast restore paths

## Files changed this run
- `research/reverse-expert-kb/sources/mobile-runtime-instrumentation/2026-03-17-sperm-android-protected-runtime-batch-6-notes.md`
- `research/reverse-expert-kb/runs/2026-03-17-1354-sperm-android-protected-runtime-batch-6.md`

## Outcome
The reverse KB now has a sixth Android/protected-runtime extraction note from the `sperm/md` repository, closing the initial Android lane with material on instrumentation topology, gadget embedding, and transparent traffic redirection.
