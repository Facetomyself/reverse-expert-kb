# Run Report — 2026-03-17 13:35 Asia/Shanghai — `sperm/md` Android / protected-runtime batch 1

## Summary
This run continued the manual staged ingest of `Facetomyself/sperm` and started the first deep pass in the planned sequence:
- **Android / protected-runtime** first
- then browser / JS
- then protocol / network
- then iOS

This batch reviewed six high-value articles centered on:
- VM reduction workflows
- trace / DBI as structural reduction tools
- seccomp / SVC trapping as an Android observation surface
- eBPF as a lower-boundary observation surface for anti-analysis cases

The run intentionally stayed conservative:
- it produced a strong source note
- it did **not** yet force canonical topic edits
- it treated this as the first accumulation pass before larger canonical synthesis

## Scope this run
- review a small high-value Android/protected-runtime subset from `sperm/md`
- extract recurring workflow patterns instead of article-by-article trivia
- preserve the results as a reusable source note
- avoid premature canonical edits until a few related batches accumulate

## Sources consulted
From `Facetomyself/sperm/tree/main/md`:
- `simpread-2024 腾讯游戏安全大赛 - 安卓赛道决赛 VM 分析与还原.md`
- `simpread-VM 逆向，一篇就够了.md`
- `simpread-VM 逆向，一篇就够了（下）.md`
- `simpread-从 trace 到二进制插桩到 Frida.md`
- `simpread-分享一个 Android 通用 svc 跟踪以及 hook 方案——Frida-Seccomp.md`
- `simpread-当 Xiaomi 12 遇到 eBPF.md`

Existing KB pages reviewed for fit:
- `research/reverse-expert-kb/topics/android-observation-surface-selection-workflow-note.md`
- `research/reverse-expert-kb/topics/android-linker-binder-ebpf-observation-surfaces.md`
- `research/reverse-expert-kb/topics/vm-trace-to-semantic-anchor-workflow-note.md`
- `research/reverse-expert-kb/topics/trace-guided-and-dbi-assisted-re.md`

## New findings
### 1. This batch strongly reinforces the KB’s existing shift toward observation-surface selection
The seccomp and eBPF articles are especially good evidence that Android practical reversing is often a question of **which boundary to observe next**, not which same-layer hook to retry.

### 2. VM articles repeatedly converge on semantic-anchor-first reduction
The useful repeated pattern is not “reverse every handler before doing anything useful.”
It is:
- recover dispatch shape
- recover enough handler semantics to isolate one meaningful family
- reduce the VM path into one smaller static or algorithmic target

### 3. Lower-boundary anti-analysis work is often best understood as consequence-bearing boundary behavior
This batch gives good examples of anti-Frida / anti-analysis logic expressed as:
- seccomp install
- `/proc` / filesystem scans
- thread-name or maps checks
- later kill/crash consequence

That is exactly the kind of material the KB wants when moving from “detection exists” to “which first boundary edge actually predicts the later failure.”

### 4. DBI/trace material is useful here mainly as a reduction discipline, not as tool fandom
The Frida/DBI overview article is broad, but it still reinforces a durable workflow rule:
- collect runtime evidence only when it will reduce the next static target or choose the next observation surface more intelligently.

## Reflections / synthesis
The first Android/protected-runtime batch turned out to be more coherent than it looked from titles alone.

The unifying theme is:
- **protected targets are often solved by choosing the right evidence surface and reducing execution churn into one smaller trustworthy object**.

That theme now has support from several angles:
- VM handler reduction
- trace/DBI-assisted simplification
- seccomp/SVC boundary trapping
- eBPF lower-boundary observation

This makes the batch genuinely useful to the KB rather than just another collection of practical reverse articles.

## Candidate topic pages to create or improve
No canonical topic pages were edited this run.

Likely future targets after one or two more related Android batches:
- strengthen `topics/android-linker-binder-ebpf-observation-surfaces.md`
- strengthen `topics/android-observation-surface-selection-workflow-note.md`
- strengthen `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- possibly add a child workflow note for seccomp/SVC trap-driven observation if later source batches keep reinforcing it

## Next-step research directions
Continue the Android/protected-runtime lane before switching branches.
Good next article families from `sperm/md` include:
- anti-debug / anti-Frida / anti-hook cases
- Android sign / parameter recovery under protection
- unidbg / Chomper / hybrid execution-assisted recovery
- linker / SO / load-path cases
- app-side environment detection / pinning / trust-path cases

## Concrete scenario notes or actionable tactics added this run
This run preserved several reusable tactics in the new source note, including:
- VM-entry -> dispatch-shape -> handler-subset -> smaller-static-target reduction
- seccomp trap -> reconstruct syscall args -> replay syscall on unconstrained thread -> restore return value
- lower-boundary anti-analysis localization via `/proc`, `access`, `readlinkat`, maps, task-name, or seccomp-adjacent events
- trace/DBI only when it shrinks the next static target

## Files changed this run
- `research/reverse-expert-kb/sources/mobile-runtime-instrumentation/2026-03-17-sperm-android-protected-runtime-batch-1-notes.md`
- `research/reverse-expert-kb/runs/2026-03-17-1335-sperm-android-protected-runtime-batch-1.md`

## Outcome
The reverse KB now has its first deep Android/protected-runtime extraction note from the `sperm/md` repository, with practical emphasis on VM reduction, observation-surface choice, and lower-boundary anti-analysis localization.
