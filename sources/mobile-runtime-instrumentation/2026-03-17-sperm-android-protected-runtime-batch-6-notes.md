# Source Notes — 2026-03-17 — `sperm/md` Android / protected-runtime batch 6

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-09 - How to use frida on a non-rooted device — LIEF Documentation.md`
- `simpread-frida 免 root hook.md`
- `simpread-注入 frida-gadget 绕过 Frida 检测.md`
- `simpread-分析 okhttp3-retrofit2 - 截流某音通信数据.md`
- `simpread-安卓上基于透明代理对特定 APP 抓包 - SeeFlowerX.md`
- `simpread-iptables 在 Android 抓包中的妙用.md`

## Why these articles were grouped together
This batch works well as the closing cluster for the Android lane because it centers on one practical branch:
- **when ordinary spawn/attach instrumentation or ordinary proxy capture is too visible, move the intervention point into packaging-time gadget injection or network-path redirection that the target cannot trivially classify as “proxy mode”**

The shared themes are:
- non-root instrumentation forms
- embedded gadget injection instead of ptrace-style attach
- zygote/frida-server detection avoidance by changing injection topology
- framework-side traffic interception in OkHttp/Retrofit layers
- UID-scoped transparent-proxy redirection with iptables/redsocks
- selecting among app-layer response hooks, socket/SSL visibility, and transport-path hijack

## Strong recurring ideas

### 1. Injection topology matters as much as the hook logic
The non-root gadget articles are useful because they do not just say “use gadget.”
They change the entire instrumentation topology:
- instead of ptrace/spawn attach,
- embed the instrumentation library into the target’s own loading path,
- optionally rename and configure it to reduce obvious signatures,
- let the app or its native dependency graph load the gadget naturally.

This is an important KB lesson:
- **sometimes the best anti-detection move is to change how instrumentation arrives, not just what it does after arrival**.

### 2. Packaging-time gadget embedding is a boundary move, not just a tooling trick
The LIEF/patchelf-based articles show a repeatable pattern:
- modify ELF dependencies of an already-loaded native library
- place gadget and config alongside packaged native libs
- resign the APK
- execute scripts through gadget without root or frida-server

The durable value here is not the specific tool (`LIEF`, `patchelf`).
It is the workflow of **turning instrumentation into a dependency-resolution event**.

### 3. Some anti-Frida checks are really anti-zygote / anti-server checks
The zygisk-gadget piece adds useful nuance:
- some commercial protections do not merely detect Frida artifacts in the app process
- they detect that zygote/frida-server style process ancestry or modification occurred

That means a meaningful branch in the KB should distinguish:
- app-local Frida artifact detection
- Java/native hook side-effect detection
- zygote/frida-server topology detection

### 4. Traffic recovery has multiple semantically different cut-points
The OkHttp/Retrofit interception article complements earlier Android traffic batches nicely.
It reinforces that “capture” can mean at least three different things:
- recover request/response semantics at framework layer
- recover transport flow at proxy/transparent-proxy layer
- recover encrypted/plaintext buffers at SSL/native layer

These are not interchangeable.
The right cut-point depends on whether the analyst wants:
- business payload semantics
- network-path coverage
- protocol downgrade leverage
- invisibility to proxy/VPN detection

### 5. Transparent proxy redirection is a strong answer to proxy/VPN classification
The iptables/redsocks articles are especially KB-worthy because they show a clean alternative when apps classify or block ordinary proxy settings:
- redirect a specific UID’s TCP flows with iptables DNAT
- send them through a local transparent-proxy bind point
- relay onward to a normal analysis proxy via redsocks
- avoid exposing ordinary HTTP proxy or VPN configuration to the target app

This is a great example of **network-path intervention without app-visible proxy state**.

### 6. Framework-layer interception and network-path redirection serve different analysis goals
The OkHttp/Retrofit article and the iptables/redsocks articles together make a useful contrast:
- framework hooks are great for semantic payloads and app-specific request/response material
- transparent proxy redirection is better for broad protocol visibility and lower app awareness

That supports a reusable selection rule:
- use framework hooks when business semantics are the goal and framework classes are stable enough
- use transparent redirection when the goal is broad capture without app-visible proxy indicators

## Concrete operator takeaways worth preserving

### A. Injection-topology selection workflow
Reusable sequence:
1. classify why ordinary Frida attach/spawn is failing:
   - root unavailable
   - ptrace blocked
   - zygote/frida-server detection
   - app-local Frida artifact checks
2. if ordinary attach is the wrong topology, switch to embedded gadget injection or similar dependency-based loading
3. treat renaming, config mode, and load timing as first-class operational variables

### B. Dependency-based gadget embedding workflow
Reusable sequence:
1. identify a native library loaded early enough and reliably enough
2. add gadget as a dependency of that native library
3. place gadget and config in the packaged native-lib directory
4. resign and redeploy
5. use script/direct-execution mode when interactive listing/server mode is too visible or permission-heavy

### C. Zygote/frida-server-topology avoidance workflow
Reusable sequence:
1. distinguish app-local detection from zygote/server-side detection
2. if zygote ancestry or frida-server artifacts are the problem, avoid that injection path entirely
3. move instrumentation arrival into gadget/embedded/module-based loading paths instead

### D. Traffic cut-point selection workflow
Reusable sequence:
1. decide whether the objective is:
   - semantic request/response recovery
   - full transport capture
   - invisible proxying
   - downgrade/path-forcing support
2. choose among:
   - OkHttp/Retrofit/framework hook
   - Java/native SSL plaintext boundary
   - transparent iptables/redsocks redirection
3. only move lower or sideways when the current cut-point is too visible, too incomplete, or too app-specific

### E. UID-scoped transparent-proxy workflow
Reusable sequence:
1. identify the target app UID
2. redirect only that UID’s TCP flows with iptables DNAT
3. send to a local transparent-proxy bind address
4. relay to analysis tooling through redsocks or equivalent
5. preserve the ability to restore rules quickly
6. use this when ordinary proxy/VPN configuration is too visible or gets classified by the app

## Candidate KB implications
This batch strongly supports or suggests improvements to:
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/android-observation-surface-selection-workflow-note.md`
- `topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md`
- `topics/runtime-behavior-recovery.md`

Potential future child-note opportunities:
- injection-topology selection for Android instrumentation
- dependency-based gadget embedding vs attach/spawn workflows
- UID-scoped transparent-proxy traffic recovery note
- framework-hook vs transparent-redirection cut-point note

## Confidence / quality note
This is a strong closing batch for the Android lane.
Its best contribution is not new anti-Frida tricks in isolation.
It is the broader idea that both instrumentation and capture have **topologies**, and changing topology is often the decisive move when ordinary approaches are too visible.
