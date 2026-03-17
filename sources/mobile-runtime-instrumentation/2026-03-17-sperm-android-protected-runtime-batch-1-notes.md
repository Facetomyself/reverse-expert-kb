# Source Notes — 2026-03-17 — `sperm/md` Android / protected-runtime batch 1

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-2024 腾讯游戏安全大赛 - 安卓赛道决赛 VM 分析与还原.md`
- `simpread-VM 逆向，一篇就够了.md`
- `simpread-VM 逆向，一篇就够了（下）.md`
- `simpread-从 trace 到二进制插桩到 Frida.md`
- `simpread-分享一个 Android 通用 svc 跟踪以及 hook 方案——Frida-Seccomp.md`
- `simpread-当 Xiaomi 12 遇到 eBPF.md`

## Why these articles were grouped together
This batch hangs together around one practical branch:
- **when direct app/native hooks are weak, noisy, or resisted, analysts shift downward or sideways into trace / DBI / seccomp / eBPF / VM-execution reduction surfaces**

That makes this batch more valuable as a workflow cluster than as isolated article summaries.

## Strong recurring ideas

### 1. VM work is usually won by reduction, not by “understand the whole VM first”
Across the Tencent game VM article and the two general VM articles, the useful repeated pattern is:
- identify the VM entry and state layout
- determine the dispatch rule (`pc`, handler selection, operand extraction)
- reconstruct only enough handler semantics to expose the relevant transformation family
- dump / replay / translate bytecode into a smaller ordinary target
- only then return to algorithm recovery or consequence proof

This is very close to the KB’s existing **semantic-anchor-first** protected-runtime direction.

Useful reduction shapes seen in the batch:
- handler bucket reconstruction
- opcode-field extraction by bit slicing
- VM-bytecode-to-native-assembly translation (`vm_to_asm`)
- reduction from “full interpreter churn” into one later algorithm family (for example AES-like transform recovery)

### 2. The right observation surface is often below the function you first wanted to hook
The seccomp / Frida-Seccomp article and the eBPF article both reinforce the same operator lesson:
- if Java/native hooks are fragile, detected, or semantically late,
- observing **SVC/syscall-adjacent** behavior or **kernel-side lower-boundary effects** may expose the real boundary faster.

Useful concrete observation surfaces reinforced by this batch:
- seccomp-generated `SIGSYS` trapping of selected syscalls
- manual recovery of syscall args/return values from register context
- dedicated unconstrained worker thread to actually perform blocked syscalls after trap
- manual FP-chain stack unwinding when ordinary Frida helpers are unstable
- Android eBPF tracing of lower-boundary events like `readlinkat` to expose anti-Frida behavior from outside app-local defenses

### 3. Trace/DBI is most valuable when it shrinks the next static target
The Frida/DBI overview article is broad, but the durable lesson is still solid:
- trace and DBI are not valuable just because they collect runtime data
- they matter when they make the next static target smaller, cleaner, or better labeled

In this batch that principle appears in several forms:
- trace a protected VM path just enough to map handler families
- trap syscall/SVC boundaries to recover anti-analysis logic without staying inside the protected code body
- use lower-boundary observation to identify one decisive path (for example anti-Frida readlink/access/maps/task scanning) before attempting deeper static cleanup

### 4. Android protected-runtime work often becomes a compare-surface problem
The combined batch suggests a recurring decision chain:
- app-layer hook
- native hook
- trace / DBI slice
- SVC / seccomp trap
- eBPF / lower-boundary kernel observation

The expert move is not “always go lower.”
The expert move is:
- choose the lowest-cost surface that exposes the next trustworthy object.

### 5. Anti-Frida / anti-instrumentation logic is frequently recoverable as boundary behavior
The Tencent game article is especially strong here because the anti-analysis path is not framed only as strings or booleans. It is reconstructed as a boundary chain:
- seccomp rule installs a kill-on-syscall policy for specific syscall numbers
- environment checks inspect filesystem / maps / task names
- thread-name and maps scanning reveal Frida/gadget presence
- crash consequence is triggered through later kill/memclr behavior

That is exactly the kind of material that can strengthen the KB’s “first consequence-bearing edge” language.

## Concrete operator takeaways worth preserving

### A. Protected VM reduction workflow
A reusable pattern from the Tencent/game and generic VM articles:
1. localize VM entry and initial register/state layout
2. identify dispatch mechanism and opcode field extraction scheme
3. recover only the relevant handler subset first
4. translate/dump bytecode into a more ordinary form if possible
5. reconnect to one smaller algorithm/static target

### B. Seccomp/SVC observation workflow
A reusable pattern from Frida-Seccomp:
1. install seccomp filter that traps selected syscall numbers
2. catch `SIGSYS` in process exception handling
3. reconstruct syscall number and arguments from register context
4. execute the real syscall on a pre-created unconstrained worker thread
5. restore return value into the trapped thread context
6. log stack / args / result using low-friction paths

### C. Lower-boundary anti-analysis localization workflow
A reusable pattern from the eBPF and Tencent anti-Frida material:
1. identify likely anti-analysis family (`access`, `readlinkat`, `/proc/self/maps`, `/proc/self/task/*/status`, seccomp)
2. observe one narrow lower-boundary event class around the trigger
3. compare normal vs instrumented run if possible
4. localize the first detection-relevant boundary read or scan
5. only then decide whether to patch, redirect, emulate, or rename

### D. DBI/trace value discipline
A reusable rule from the Frida/DBI overview article:
- do not collect trace because trace is available
- collect trace when it will expose one handler family, state edge, or boundary event that reduces the next static target

## Candidate KB implications
This batch strengthens or supports the following existing KB areas:
- `topics/android-observation-surface-selection-workflow-note.md`
- `topics/android-linker-binder-ebpf-observation-surfaces.md`
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- `topics/trace-guided-and-dbi-assisted-re.md`
- `topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md`

Potential future child-note opportunities if later batches reinforce them:
- Android seccomp/SVC trap-to-syscall-replay workflow note
- anti-analysis boundary-read localization workflow note
- VM-entry-to-bytecode-translation workflow note

## Confidence / quality note
These articles are strongly practical and useful, but heterogeneous.
Best use in the KB:
- extract recurring workflow shapes and operator bottlenecks
- do **not** import article-specific exploit/game details wholesale
- treat individual bypasses as examples of boundary localization, not as canonical ends in themselves
