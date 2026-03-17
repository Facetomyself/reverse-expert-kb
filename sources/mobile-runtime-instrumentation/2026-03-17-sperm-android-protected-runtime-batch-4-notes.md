# Source Notes — 2026-03-17 — `sperm/md` Android / protected-runtime batch 4

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-App 逆向百例 _ 19 _ 某 App Sign 完整分析.md`
- `simpread-大猿搜题 sign so 加密参数分析｜unidbg.md`
- `simpread-[原创] 记一次 unicorn 半自动化逆向——还原某东 sign 算法.md`
- `simpread-使用 Unidbg 模拟执行去除 OLLVM-BR 混淆.md`
- `simpread-逆向某物 App 登录接口：抓包分析 + Frida Hook 还原加密算法.md`
- `simpread-逆向某物 App 登录接口：还原 newSign 算法全流程.md`

## Why these articles were grouped together
This batch is a strong cluster around one practical branch:
- **mobile sign / parameter recovery is usually solved by first localizing the true path, then using controlled execution to extract transformation structure, and only then writing a minimal external reproduction**

The key shared ingredients are:
- request/sign path localization
- native or protected sign-entry tracing
- unidbg / unicorn / controlled execution assistance
- extracting permutation/mapping tables instead of reading every branch by hand
- deobfuscating OLLVM-BR or VM-ish control flow enough to recover semantics
- reducing full app logic to a smaller reproducible sign pipeline

## Strong recurring ideas

### 1. Sign recovery starts with path localization, not with cryptography
The app-login/sign articles are valuable because they repeatedly begin with:
- packet capture and request parameter identification
- Java hook at interceptor / request-builder / map-assembly points
- narrowing the candidate set to one or two suspicious params (`newSign`, `password`, `userName`, etc.)
- determining whether the decisive work is plain Java crypto, JNI/native crypto, or protected-wrapper dispatch

This is a durable workflow lesson:
- **do not begin by assuming “the algorithm is in native.”**
- first prove which path owns the final parameter.

### 2. Execution-assisted analysis is strongest when used to extract structure, not merely to invoke the target
The unidbg and unicorn articles are especially strong because they use controlled execution for more than one-shot invocation.
They use it to:
- recover bit-permutation tables
- compare all-zero vs single-bit inputs
- derive per-case mapping relationships
- inspect intermediate state around one decisive breakpoint
- extract small constant tables or state arrays that static reading cannot cheaply reveal

That is much more reusable than “call the sign function with unidbg and print the result.”

### 3. Many sign algorithms reduce to tractable transform families once you stop reading them literally
Several articles show the same reduction move:
- a huge ugly function is really a bit permutation, nibble/byte rearrangement, xor/add layer, case-based tail transform, AES+base64+MD5 pipeline, or similar compact family
- the analyst wins by discovering the compact family and its tables
- not by hand-copying every branch from decompiler sludge

This is core KB material because it strongly supports **family reduction over literal control-flow worship**.

### 4. Controlled differential inputs are a high-leverage deobfuscation tool
The JD/unicorn and sign-complete-analysis articles repeatedly use the same high-yield trick:
- feed one-hot / one-bit / sparse controlled inputs
- observe output-position change or bit flips
- infer permutation or transformation rule from differential behavior

This is a portable technique for:
- protected sign functions
- odd remainder-case handlers
- S-box-ish/permutation-ish native helpers
- VM-ish or table-driven transform blocks

### 5. OLLVM/BR deobfuscation often does not need full static cleanup before progress
The OLLVM-BR article is valuable because it operationalizes a practical idea:
- if indirect branch dispatch depends on runtime-known register values, emulate just enough to resolve the true edges
- then patch indirect branches back into direct branches
- let normal static tooling recover afterwards

That is exactly the kind of workflow note the KB should prefer over vague “去混淆” descriptions.

### 6. The real endpoint of sign recovery is a minimal reproducible pipeline
The strongest end-state in this batch is not merely “we know what happens.”
It is:
- captured param assembly rules
- localized sign path
- extracted keys/constants/transform tables
- minimal Python/Java reproduction that reproduces the app output

The app-login/newSign materials are especially good examples because they reduce a protected/native-looking path into a compact formula like:
- value assembly / sorting / concatenation
- AES-ECB + Base64 + MD5
- AES(plaintext,key)+suffix
- md5(password + constant)

That kind of collapse is the actual operator objective.

## Concrete operator takeaways worth preserving

### A. Sign/parameter recovery workflow
Reusable sequence:
1. identify unstable or secret-bearing request parameters from live traffic
2. hook request assembly points (map/interceptor/builder) before assuming native ownership
3. classify each target param into:
   - plain Java crypto
   - JNI/native helper
   - protected-wrapper dispatch
   - mixed pipeline
4. localize the narrowest entry that deterministically emits the target value

### B. Execution-assisted structure extraction workflow
Reusable sequence:
1. make the function callable or partially emulatable
2. design differential inputs (single-bit, sparse, all-zero baseline, one-field-at-a-time)
3. capture intermediate state at one decisive internal breakpoint
4. derive tables/mappings/constants from differences
5. rebuild the compact transformation in external code

### C. Tail-case or case-split transform recovery workflow
Reusable sequence:
1. identify the main block path and the leftover/remainder path separately
2. do not assume the tail handler is “just padding”
3. derive each remainder case by controlled-input mapping rather than literal pseudocode translation
4. preserve the case tables as first-class artifacts

### D. OLLVM-BR branch recovery workflow
Reusable sequence:
1. identify indirect-branch regions whose targets are runtime-computable
2. emulate enough state to resolve branch targets under each path condition
3. patch indirect branches back to direct edges when stable
4. return to static analysis only after dispatch becomes legible

### E. Minimal reproducible pipeline discipline
Reusable sequence:
1. stop when you can reproduce the target output from minimal inputs
2. preserve the smallest faithful formula, not the full app’s control flow
3. record where the constants/keys/tables came from
4. keep app-specific wrappers out of canonical notes unless they illustrate a reusable workflow move

## Candidate KB implications
This batch strongly supports or suggests improvements to:
- `topics/runtime-behavior-recovery.md`
- `topics/trace-guided-and-dbi-assisted-re.md`
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- protected-runtime/deobfuscation workflow branches under the KB

Potential future child-note opportunities:
- execution-assisted sign/parameter recovery workflow note
- differential-input mapping extraction workflow note
- OLLVM-BR indirect-branch recovery note
- minimal reproducible crypto/sign pipeline note

## Confidence / quality note
This is one of the strongest Android/protected-runtime batches so far.
The articles are varied in polish, but many converge on the same deep lesson:
- **if you can extract the transform family and its small artifacts, you do not need to understand every control-flow ornament around it**.

That is high-value canonical material for the KB.
