# Source Notes — 2026-03-17 — `sperm/md` Android / protected-runtime batch 3

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-如何实现 Android App 的抓包防护？又该如何绕过？一文看懂攻防博弈 __ CYRUS STUDIO.md`
- `simpread-[原创]android 抓包学习的整理和归纳.md`
- `simpread-字节系, ali 系, ks,pdd 最新抓包方案.md`
- `simpread-某查线路 app 设备检测逆向分析.md`
- `simpread-过某加固 Frida 检测.md`
- `simpread-绕过 libxxxxsec.so 对 Frida hook Java 层的检测.md`

## Why these articles were grouped together
This batch centers on one practical branch:
- **when app transport is intentionally hardened or hidden, the analyst must choose the right network boundary and the right anti-detection boundary before deeper request analysis is even possible**

This includes:
- anti-proxy / anti-VPN / SSL / QUIC / SPDY transport hardening
- system-layer and native-layer packet visibility
- app-specific protocol downgrade or path rerouting
- shell/security-so anti-Frida and Java-hook detection countermeasures
- initialization-boundary interception for security components

## Strong recurring ideas

### 1. Packet capture is really a boundary-selection problem
The larger packet-capture articles are valuable because they frame capture methods by boundary:
- business-layer hook
- framework-layer hook
- MITM tooling
- NIC/router capture
- Java socket / SSL layer
- native send/recv layer
- SSL plaintext layer before record sealing

The durable lesson is not “use tool X.”
It is:
- choose the boundary that still exposes the evidence you need while surviving the target’s anti-capture measures.

### 2. HTTPS/SSL analysis benefits from separating plaintext and ciphertext boundaries
The long packet-capture article is especially valuable because it explicitly maps:
- Java `SocketOutputStream` / `SocketInputStream`
- Java `NativeCrypto.SSL_write` / `SSL_read`
- native `SSL_write` / `SSL_read`
- lower `read` / `write` or `sendto` / `recvfrom`

That gives the KB a strong reusable distinction:
- **plaintext boundary**: where request/response semantics remain visible
- **ciphertext boundary**: where transport framing remains visible but application semantics are already sealed

This is exactly the sort of operator distinction the KB should preserve.

### 3. Modern mobile packet capture often means protocol downgrade or alternate-route forcing
The app-family article on Byte/Ali/KS/PDD is useful because it reinforces a recurring tactic family:
- disable QUIC
- disable SPDY / proprietary SSL switch paths
- null out or rewrite config on native update calls
- intercept library load and patch transport-choice return values after `dlopen`

This is not just “capture trickery.”
It is **transport-path forcing**:
- if the app insists on a less observable channel, redirect it onto a more observable one.

### 4. Anti-capture is often environment classification, not just SSL pinning
The route app case is strong because the first blocker was not request encryption itself, but environment restriction:
- Frida detection changed app behavior
- VPN/tun detection blocked proxy-assisted traffic
- Wi-Fi/vpn state classification altered reachable behavior

That means anti-capture workflows should not be reduced to “unpin SSL.”
Very often the analyst must first solve:
- environment classification
- proxy/VPN detection
- runtime tooling detection
- transport selection
before request signatures matter at all.

### 5. Shell/security-so bypasses often belong at the constructor / initialization boundary
The two shell-so Frida-detection articles are especially useful together.
They reinforce several reusable moves:
- memory-dump + section repair to recover a hardened so for analysis
- string-led or protocol-led detection localization (`AUTH`, `REJECT`, `LIBFRIDA`, port scans)
- broad `recv` result tampering as a surgical bypass for a specific detector family
- bypassing security-so behavior by killing `.init_proc` / `JNI_OnLoad` execution at loader time
- even crude delete-the-security-so approaches can work when the app does not hard-depend on that component

The key workflow lesson is:
- if a security component’s main job is detection, the most leverage often sits at the **loader/constructor boundary**, before its runtime surface spreads through the app.

### 6. Java-hook detection deserves to be modeled as a distinct anti-instrumentation branch
The `libxxxxsec.so` article adds an important nuance:
- native anti-Frida bypasses may still leave Java-hook detection intact
- a target can detect prettyMethod/inline-hook side effects caused by `Java.perform` or `Java.use`

This is KB-worthy because it separates:
- generic Frida presence detection
- Java-hook side-effect detection
- security-so initialization bypass

Those are related, but not identical, analyst problems.

## Concrete operator takeaways worth preserving

### A. Transport-boundary selection workflow
Reusable sequence:
1. ask whether the goal is plaintext semantics, encrypted framing, or traffic provenance
2. choose the lowest boundary that still preserves the needed evidence:
   - business layer
   - framework layer
   - Java socket/SSL layer
   - native SSL plaintext layer
   - native socket layer
   - MITM/VPN/router capture
3. only go lower when the higher boundary is blocked, too noisy, or semantically late

### B. Transport-path forcing workflow
Reusable sequence:
1. identify whether the app prefers QUIC/SPDY/proprietary channel/proxy bypass path
2. locate the feature gate, config setter, or native transport selector
3. downgrade or reroute onto an observable path
4. re-run capture at the now-stable boundary

### C. Environment-classification-first anti-capture workflow
Reusable sequence:
1. distinguish among Frida detection, VPN/tun detection, Wi-Fi classification, SSL pinning, and request signing
2. neutralize the earliest gate that changes app behavior
3. only after behavior stabilizes, proceed to packet visibility or parameter reconstruction

### D. Security-so constructor-boundary bypass workflow
Reusable sequence:
1. identify the shell/security so responsible for detection
2. if necessary, dump memory image and repair sections for static analysis
3. localize detector family by strings, port protocol, or suspicious loops
4. choose one of:
   - detector-function return tampering
   - constructor / `.init_proc` / `JNI_OnLoad` neutralization
   - loader-time interception
   - dependency removal if app stability permits
5. only then attempt higher-level Java/native instrumentation

### E. Java-hook-side-effect detection workflow
Reusable sequence:
1. do not assume “Frida bypass” also covers Java-perform/use side effects
2. test separately for Java-layer hook stability
3. if prettyMethod or similar code-integrity checks are involved, prefer earlier security-so neutralization or constructor bypass over patching every later symptom

## Candidate KB implications
This batch strongly supports or suggests improvements to:
- `topics/android-observation-surface-selection-workflow-note.md`
- `topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/runtime-behavior-recovery.md`
- `topics/android-linker-binder-ebpf-observation-surfaces.md`

Potential future child-note opportunities:
- transport-boundary selection for mobile traffic recovery
- transport-path forcing via QUIC/SPDY downgrade or config rerouting
- security-so constructor-boundary bypass workflow note
- Java-hook side-effect detection and mitigation workflow note

## Confidence / quality note
This batch is heterogeneous but high-yield.
Its strongest value is not app-specific packet-capture recipes.
It is the recurring workflow pattern that hard mobile traffic analysis is usually solved in this order:
- stabilize execution environment
- choose or force the right transport path
- choose the right plaintext/ciphertext observation boundary
- only then solve signatures, payload crypto, or business semantics
