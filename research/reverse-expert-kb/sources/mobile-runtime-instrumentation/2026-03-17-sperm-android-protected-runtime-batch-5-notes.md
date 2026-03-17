# Source Notes — 2026-03-17 — `sperm/md` Android / protected-runtime batch 5

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-App 逆向百例 _ 18 _ 某 A 系防护 SO 跳转修复.md`
- `simpread-初探 android crc 检测及绕过.md`
- `simpread-控制流平坦化反混淆（春节红包活动 Android 高级题） - 『移动安全区』  - 吾爱破解 - LCG - LSG _ 安卓破解 _ 病毒分析 _ www.52pojie.cn.md`
- `simpread-某风控 SDK 逆向分析 _ AshenOne.md`
- `simpread-【Fireyer】一款 Android 平台环境检测应用 _ iofomo _ Open-source organization.md`
- `simpread-【安卓逆向】安居客反调试与参数分析.md`

## Why these articles were grouped together
This batch clusters around one practical branch:
- **when protected Android targets aggressively hide or verify execution state, the analyst often wins by restoring a usable analysis image, shadowing integrity views, and modeling environment-collection surfaces instead of fighting every symptom locally**

The shared themes are:
- initialized-image-aware repair
- dynamic control-flow restoration
- integrity-shadowing against CRC / memory-view checks
- environment-detection surface inventory
- risk-SDK dual-surface collection modeling (Java + native)
- anti-debug thread neutralization before parameter recovery

## Strong recurring ideas

### 1. Static repair often fails because the binary on disk is not the binary that actually executes
The protective-SO jump-repair article makes this point clearly:
- some branch targets depend on initialized runtime state rather than pristine file bytes
- naïve emulation over the raw on-disk image can resolve the wrong target
- initialized-state-aware repair (for example via unidbg after constructor/runtime setup) can recover the real branch destinations

This is a very important KB lesson:
- **when branch-target computation depends on post-load state, treat the initialized image as the authoritative analysis object**.

### 2. Dynamic branch repair and control-flow deobfuscation are really “analysis-image restoration” moves
The jump-repair article and the control-flow-flattening exploration article both point toward the same high-level move:
- do enough execution to restore legible control flow
- patch the analysis artifact into a form that conventional static tooling can digest
- then continue ordinary reverse work on the repaired image/graph

This is more powerful than treating patching as ad hoc cleanup.
It is a reusable workflow:
- **restore an analysis-friendly surrogate of the protected artifact**.

### 3. Integrity checks can often be bypassed by shadowing the victim’s view, not by deleting every check
The CRC article is one of the strongest practical pieces in the whole repository.
Its durable lesson is that integrity checks often compare:
- file view vs `/proc/self/maps` executable view
- file view vs linker/soinfo-derived memory view
- file view vs section-pointer-derived memory view

The bypass pattern is elegant:
- create a clean shadow memory view
- redirect maps/linker/section-derived metadata to the shadow
- keep the live hooked/modified memory separate

This is a classic **view-shadowing** strategy, and it is extremely KB-worthy.

### 4. Environment detection is best handled as a structured surface inventory
The Fireyer article and the risk-SDK analysis both reinforce the same analyst move:
- enumerate environment-collection surfaces systematically rather than guessing detector trivia.

The recurring surfaces include:
- hidden API access and reflection reachability
- Binder / service proxying and Java proxy classes
- calling stacks and thread lists
- `/proc/self/maps`, `/proc/self/task`, `/proc/self/status`
- package, signature, manifest, and component integrity
- file/directory/process/network-interface collection
- virtualization / multi-open / emulator markers
- injected dex/lib or in-memory-loaded artifacts

This is very useful because it gives the KB a way to model hostile app/runtime inspection as a **surface matrix**, not as an endless list of named checks.

### 5. Large risk SDKs are best approached by collection-graph modeling
The risk-SDK article is unusually valuable because it reconstructs not just one bypass, but the shape of the SDK:
- config fetch
- Java-side and native-side collectors
- field renaming / serialization
- encrypted upload
- hook lists and collection specs embedded or encrypted in native land

That suggests a very reusable workflow:
- treat large anti-fraud / risk SDKs as **collection graphs** with configuration, collectors, transformations, and upload sinks.

This is a better operator model than reading one giant decompiler blob linearly.

### 6. Anti-debug neutralization often belongs before signing or parameter work
The Anjuke article reinforces a pattern already visible in earlier batches:
- identify the detector thread / loop first
- neutralize or unload the detection component at the right boundary
- only then proceed to request-sign analysis

This article is not conceptually new compared with earlier anti-Frida pieces, but it adds one useful practical framing:
- transport/SSL stabilization and anti-debug neutralization are often prerequisites for signature recovery, not separate tasks.

## Concrete operator takeaways worth preserving

### A. Initialized-image-first repair workflow
Reusable sequence:
1. identify branch/dispatch restoration that depends on computed runtime state
2. test whether raw-file emulation produces wrong targets
3. reconstruct or emulate enough initialization to obtain the executed image state
4. record true branch targets dynamically
5. patch a repaired analysis artifact for later static work

### B. Analysis-image restoration workflow
Reusable sequence:
1. treat control-flow deobfuscation and branch repair as artifact restoration
2. build a legible surrogate image or graph
3. move back into conventional static analysis only after edges/blocks become trustworthy
4. preserve the restored artifact as a durable intermediate, not just a temporary notebook trick

### C. Integrity-view shadowing workflow
Reusable sequence:
1. classify which memory/file views are being compared
2. build a clean shadow view from the expected file or segment contents
3. redirect the detector’s metadata path (maps, soinfo, section pointers, link-map) toward the shadow
4. keep the live modified region separate
5. prefer shadowing the detector’s observation path over patching every checksum call site

### D. Environment-surface inventory workflow
Reusable sequence:
1. enumerate detection surfaces before bypass attempts:
   - files/dirs
   - maps/status/task
   - signatures/manifest/components
   - hidden APIs / reflection
   - Binder/service proxies
   - thread/call-stack collection
   - network interfaces / proxy / VPN / virtio
   - package/process/app lists
2. group observations by collection surface and consequence
3. pick the earliest consequence-bearing surface for intervention

### E. Risk-SDK collection-graph workflow
Reusable sequence:
1. recover config or decrypt collector specifications if possible
2. separate Java collectors, native collectors, and upload/serialization stages
3. map field renaming/packing rules independently from raw collection logic
4. isolate the smallest collector subset that explains one server-facing field or risk outcome
5. avoid linear whole-SDK reading unless absolutely necessary

## Candidate KB implications
This batch strongly supports or suggests improvements to:
- `topics/runtime-behavior-recovery.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md`
- `topics/trace-guided-and-dbi-assisted-re.md`
- protected-runtime/deobfuscation and hostile-runtime-observation branches under the KB

Potential future child-note opportunities:
- initialized-image-first branch-repair workflow note
- integrity-view shadowing against maps/linker/section checks
- environment-detection surface matrix for Android hostile runtimes
- risk-SDK collection-graph reconstruction workflow note

## Confidence / quality note
This is another strong Android batch.
Its best contribution is not any one bypass trick.
It is the repeated expert move of **changing the analyst’s object of work**:
- from raw file to initialized image
- from live modified memory to a shadow integrity view
- from giant SDK blob to collection graph
- from scattered checks to environment-surface inventory

That is durable KB material.
