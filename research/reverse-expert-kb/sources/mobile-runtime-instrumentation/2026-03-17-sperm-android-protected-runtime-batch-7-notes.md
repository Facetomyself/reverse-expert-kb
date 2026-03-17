# Source Notes — 2026-03-17 — `sperm/md` Android / protected-runtime batch 7

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-Flutter Android APP 逆向系列 (一) _ Dawnnnnnn.md`
- `simpread-《安卓逆向这档事》番外实战篇 3 - 拨云见日之浅谈 Flutter 逆向.md`
- `simpread-x-zse-96 安卓端纯算, 魔改 AES.md`
- `simpread-x-zse-96,android 端, 伪 dex 加固, so 加固, 白盒 AES, 字符串加密.md`
- `simpread-[原创] 基于 trace 内存爆破标准算法 - Android 安全 - 看雪论坛 - 安全社区 _ 非营利性质技术交流社区.md`
- `simpread-unidbg 调用 sgmain 的 doCommandNative 函数生成某酷 encryptR_client 参数.md`

## Why these articles were grouped together
This batch coheres around one practical branch:
- **when protected Android targets span multiple runtimes or heavily obfuscated native crypto, the winning move is to recover a smaller owner path and then extract constants/tables/initialization obligations until the algorithm becomes externally reproducible**

The subthemes are:
- Flutter on Android as a cross-runtime owner-localization problem
- replacing repack/reflutter failure with live library replacement or runtime-oriented workflows
- trace-guided constant/table extraction from native crypto
- white-box / pseudo-AES / modified-AES reduction into pure external computation
- unidbg initialization sequencing for large SDK command routers
- memory-based algorithm recognition and table/key recovery without full IDA-centric workflow

## Strong recurring ideas

### 1. Flutter on Android is a cross-runtime ownership problem, not just a traffic or SSL problem
The two Flutter articles are useful because they force a broader view:
- requests may not obey ordinary proxy expectations
- trust handling lives in Flutter/Dart engine space
- business logic lives in `libapp.so`
- hook points may be in Dart runtime, engine patches, or dumped symbolized snapshots rather than Java

This is exactly the kind of cross-runtime owner-localization problem the KB should preserve.

### 2. Repack/reFlutter failure should trigger runtime-component substitution or runtime-owner localization, not endless packaging retries
One especially practical Flutter lesson in this batch:
- if a reFlutter-style repack crashes because of shell/protection constraints,
- it may be better to replace the live `libflutter.so` component or pivot to blutter/live-dump-based owner localization,
- instead of treating repack success as mandatory.

This parallels the iOS Flutter lesson nicely and feels like a cross-platform reusable rule.

### 3. White-box / modified-native crypto recovery often becomes a table-recovery problem
The `x-zse-96` pair is very strong because it makes the core reduction visible:
- identify the owning field/path first
- localize the native white-box-ish function
- recover or dump runtime tables rather than trusting damaged static output
- classify the true transform family from round structure, constants, schedule shape, IV/padding use, and table access patterns
- only then externalize into a pure implementation

This is extremely KB-worthy.

### 4. Runtime memory often contains truer crypto artifacts than the dumped or repaired static binary
A repeated lesson in the white-box / modified-AES material:
- dumped/repaired so files can still be insufficient or misleading
- runtime memory can contain the correct tables/arrays even when static views are damaged or partially unreadable
- therefore table extraction from the executing target or emulator may be more trustworthy than continuing to polish the static artifact

This aligns nicely with earlier Android findings on initialized images and integrity-view issues.

### 5. Standard-algorithm recovery can be driven by memory behavior and constants, not full decompilation
The trace-memory article is interesting because it proposes a different but compatible route:
- trace from a generic JNI entry edge (`artJniMethodStart`)
- monitor memory reads/writes around the active algorithm
- identify standard algorithm fingerprints via constants/tables in memory
- brute-force/align around the observed result

That yields a durable rule:
- **sometimes you do not need the function name, so name, or even a clean control-flow graph if the memory evidence already fingerprints the algorithm family**.

### 6. Large SDK command routers are best reduced by initialization sequencing plus target-command replay
The `sgmain` / `doCommandNative` article is highly practical because it shows a robust pattern:
- identify the target command id
- trace not only the final call but also required earlier initialization commands
- replay the minimal command sequence in unidbg
- satisfy missing IO/classes/threads incrementally
- then call the target command successfully

This is a very strong execution-assisted workflow note candidate.

### 7. “Close but wrong” results in unidbg often mean missing initialization or hidden side conditions, not wrong core logic
The `x-zse-96` and `sgmain` pieces reinforce the same operator rule from a different angle:
- if you almost have the algorithm but outputs drift,
- suspect missing initialization, runtime tables, file IO, process naming, plugin init, or side-condition commands,
- before assuming the transform family itself was misidentified.

### 8. A reusable reduction ladder emerges for protected Android crypto owners
This batch suggests a stable ladder:
1. localize the owner across Java/Dart/native/SDK router boundaries
2. if static output is unreliable, prefer runtime memory/table extraction
3. recover initialization obligations separately from core transform logic
4. identify standard-family anchors (AES/MD5/HMAC/sha256 etc.) even inside modified wrappers
5. externalize into a pure or minimally emulated reproduction

This is excellent canonical-KB material.

## Concrete operator takeaways worth preserving

### A. Cross-runtime owner-localization workflow for Android Flutter
Reusable sequence:
1. confirm Flutter footprint (`libflutter.so`, `libapp.so`, snapshot markers)
2. separate engine/trust/capture issues from business-owner localization
3. if repack fails, pivot to live component substitution or dump-based symbol recovery
4. localize the true sign/field owner in Dart/runtime space rather than overinvesting in Java absence

### B. Runtime-table-extraction workflow for protected native crypto
Reusable sequence:
1. identify likely table-driven or white-box-like transform behavior
2. distrust damaged static dumps when runtime evidence disagrees
3. hook or break on table access / round transitions / key-schedule use
4. dump tables/round material from live memory or emulator state
5. rebuild the transform externally from the extracted runtime artifacts

### C. Memory-fingerprint-first algorithm recognition workflow
Reusable sequence:
1. trace from a generic JNI/native boundary if owner localization is still rough
2. capture relevant memory reads/writes around the active crypto path
3. search for standard constant/table fingerprints
4. align plaintext/ciphertext/intermediate memory views against candidate standard families
5. only escalate to deeper control-flow recovery if memory evidence is insufficient

### D. Command-router initialization sequencing workflow for unidbg
Reusable sequence:
1. identify the target command or router entrypoint
2. trace the earlier initialization commands that must run first
3. replay the minimal init chain in unidbg
4. satisfy missing class/file/thread/process expectations incrementally
5. invoke the target command only after init state is coherent

### E. Near-correct-output troubleshooting rule
Reusable sequence:
1. when outputs are close but wrong, suspect missing init/tables/IO/process-state first
2. compare runtime artifacts between app and emulator
3. separate core transform reconstruction from environment obligations
4. only revisit the core math after side conditions are ruled out

## Candidate KB implications
This batch strongly supports or suggests improvements to:
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/runtime-behavior-recovery.md`
- `topics/trace-guided-and-dbi-assisted-re.md`
- future Flutter/cross-runtime notes under the KB
- future execution-assisted algorithm-recovery notes

Potential future child-note opportunities:
- Android Flutter cross-runtime owner-localization note
- runtime-table-extraction note for white-box/modified native crypto
- memory-fingerprint-first standard-algorithm recovery note
- command-router initialization sequencing note for unidbg/SDK routers

## Confidence / quality note
This is one of the strongest late Android batches because it adds several higher-order workflow ideas at once:
- cross-runtime ownership,
- runtime artifact trust over damaged static artifacts,
- initialization sequencing,
- and memory-led algorithm recognition.

Those ideas should transfer well beyond the specific case studies here.
