# Source Notes — 2026-03-17 — `sperm/md` Android / protected-runtime batch 2

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-APP 逆向工程技巧——反调试检测线程.md`
- `simpread-frida 检测.md`
- `simpread-unidbg 算法还原术 · 某民宿 app 篇 · 上卷.md`
- `simpread-unidbg 算法还原术 · 某民宿 app 篇 · 中卷.md`
- `simpread-unidbg 算法还原术 · 某民宿 app 篇 · 下卷.md`
- `simpread-某 A 系电商 App x-sign 签名分析.md`

## Why these articles were grouped together
This batch coheres around another practical branch of Android protected-runtime work:
- **when you cannot or should not stay at the obvious surface, move to the closest stable execution boundary that still exposes the secret-bearing path**

The concrete subthemes here are:
- deeper thread-start interception instead of obvious `pthread_create` hooking
- anti-Frida detection as a collection of boundary checks, not one trick
- unidbg as execution-assisted algorithm reconstruction
- dynamic-classloader and native-string localization to identify the true Java/native boundary around a signing path

## Strong recurring ideas

### 1. Choose the closest stable cut-point, not the most famous cut-point
The thread anti-debug article is useful because it says something very transferable:
- do not necessarily hook the first symbol everyone thinks of (`pthread_create`)
- move one layer deeper toward the actual execution handoff (`__start_thread`, `__pthread_start`)
- recover the user-function entry from thread bootstrap state
- decide based on the real thread payload rather than the obvious creator API

This is a valuable general rule for protected-runtime work:
- when the common API hook is too visible, cut at the **handoff boundary** instead.

### 2. Anti-Frida is best modeled as a detection-surface set
The `frida 检测` note is terse but useful as a checklist reservoir.
It clusters common detection families into a compact operator map:
- fake or monitored `pthread_create`
- memfd / maps / fd / readlink / task-name scans
- inline-hook opcode checks
- breakpoint byte checks
- `ptrace` occupation or parent/child attach patterns
- process/port/D-Bus probing for frida-server
- `LIBFRIDA` string or module scanning
- `libart.so` / `libc.so` integrity checks
- `RWX/RWXP` permission anomalies
- text-section CRC checks

This is strong source material for viewing anti-Frida not as one signature but as a **surface bundle** with filesystem, memory, thread, IPC, and integrity branches.

### 3. unidbg matters less as a tool brand than as an execution-assisted reduction method
The three-part unidbg series is long, but the enduring value is not “how to use unidbg” in the abstract.
It is the workflow:
- confirm callable Java/native interface with Frida or live app observation
- get `JNI_OnLoad` and registration to run under emulation
- patch missing environment dependencies iteratively until the target path executes
- call the relevant JNI/native entry directly
- hook internal functions to recover plaintext, intermediate state, keys, IVs, or block transforms
- reconstruct the algorithm from observed intermediate semantics rather than heroic pure-static reading

That is a very high-value KB pattern: **execution-assisted algorithm reduction under partial environment reconstruction**.

### 4. Good signing analysis often localizes the true boundary before reconstructing the full math
The x-sign article is much shorter but still important because it reinforces a practical front-end workflow:
- use string anchors such as `x-sign`
- correlate Java stack and native backtrace
- identify which native library and which Java proxy/plugin layer actually carry the request
- account for dynamically loaded fake-so/jar packaging
- switch to the correct classloader before hooking the Java side

This is not the full algorithm workflow, but it is a crucial earlier stage:
- **true path localization before deep reconstruction**.

### 5. Many signing/encryption paths are mixed-surface problems, not pure-native problems
The unidbg series and x-sign localization article together support the same broader lesson:
- the decisive path may cross Java strings, JNI registration, dynamically loaded jars, native crypto helpers, and return-path encoders.

That means the analyst should preserve at least these boundaries separately:
- Java caller / proxy / plugin layer
- registration or native entry address
- internal crypto preimage / intermediate transform / final formatter
- classloader or packaging tricks that hide the accessible Java-facing interface

## Concrete operator takeaways worth preserving

### A. Thread-start cut-point workflow
Reusable pattern:
1. avoid hooking the obvious thread creation API if it is likely monitored
2. inspect actual thread bootstrap path (`__start_thread`, `__pthread_start`)
3. recover user function pointer from bootstrap structure
4. attribute the new thread by real payload address/module
5. selectively suppress, detour, or log suspicious detector threads

### B. Anti-Frida detection-surface decomposition
Reusable pattern:
1. classify the target’s detector into one or more surfaces:
   - memory/maps/fd
   - process/port/D-Bus
   - thread/task-name
   - hook/instruction integrity
   - `ptrace` / debugger occupation
   - module/text checksum
2. choose the first bypass or observation move surface-by-surface, not as a generic “anti-Frida bypass” blob
3. localize the first consequence-bearing detection edge on that surface

### C. Execution-assisted algorithm reconstruction workflow
Reusable pattern from the unidbg series:
1. validate the callable path under the real app first
2. reproduce the native path under emulation
3. patch environment holes incrementally until entry executes
4. hook intermediate transforms (`Update`, `Final`, key/iv init, encoded preimage builders)
5. infer standard vs modified crypto from constants, mode setup, and intermediate buffers
6. only then write an external reimplementation

### D. Dynamic classloader / fake-so localization workflow
Reusable pattern from the x-sign article:
1. anchor on a native or Java string feature
2. capture both Java stack and native backtrace around the feature
3. identify fake-so / jar packaged plugin layers if present
4. enumerate classloaders and bind the correct one
5. hook the nearest stable Java-facing API before diving into native internals

## Candidate KB implications
This batch strengthens or supports the following KB areas:
- `topics/android-observation-surface-selection-workflow-note.md`
- `topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md`
- `topics/trace-guided-and-dbi-assisted-re.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/runtime-behavior-recovery.md`

Potential future child-note opportunities if later batches reinforce them:
- thread-bootstrap cut-point workflow note for detector-thread interception
- dynamic-classloader localization workflow note for mobile protected plugins
- execution-assisted native algorithm reconstruction workflow note (unidbg/chomper/unicorn-adjacent, tool-agnostic framing)

## Confidence / quality note
This batch is very practical but uneven in depth:
- the anti-Frida note is shallow yet high-signal as a detector-surface checklist
- the unidbg series is much deeper and supplies the strongest workflow value
- the x-sign note is more about localization than full reconstruction, but that localization step is legitimately important

Best KB use:
- preserve workflow shapes
- preserve detector-surface decomposition
- avoid carrying over sample-specific brand/app details unless they illustrate a general boundary pattern
