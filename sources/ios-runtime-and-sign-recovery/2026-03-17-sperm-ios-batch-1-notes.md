# Source Notes — 2026-03-17 — `sperm/md` iOS batch 1

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-在非越狱 iOS 上实现全流量抓包.md`
- `simpread-【iOS 逆向】iOS 某大厂 vmp 参数还原.md`
- `simpread-【iOS 逆向】某音乐 sign 分析 - 过 ollvm 与花指令.md`
- `simpread-某手 sig3-ios 算法 Chomper 黑盒调用.md`
- `simpread-某红书 Shield 算法 Chomper 黑盒调用.md`

Existing KB page consulted for fit:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`

## Why these articles were grouped together
This first iOS batch coheres around one practical branch:
- **iOS reversing becomes much easier once the analyst separates transport topology, runtime gate selection, and algorithm-owner recovery; only then does it make sense to choose between trace-guided reduction and black-box execution assistance**

The subthemes are:
- non-jailbroken iOS full-traffic capture via VPN/WireGuard/transparent MITM topologies
- iOS VMP-style parameter recovery with trace-guided semantic reduction
- OLLVM / flower-instruction cleanup for sign recovery
- Chomper as iOS-side execution-assisted / black-box invocation framework
- initialization- and token-dependent black-box algorithm invocation

## Strong recurring ideas

### 1. On iOS, traffic visibility is often a network-topology choice before it is a pinning-bypass problem
The non-jailbroken iOS traffic-capture article is especially useful because it starts by refusing the obvious but wrong assumption:
- if proxy-config capture misses key traffic and there is no clear SSL alert,
- the real issue may be proxy bypass or capture topology mismatch rather than certificate trust itself.

The durable lesson is:
- **pick the right traffic topology first**:
  - ordinary system proxy
  - NE/VPN interception
  - WireGuard full-tunnel observation
  - transparent MITM in WireGuard mode

This parallels the Android transport-boundary lessons nicely.

### 2. iOS full-traffic capture can be achieved without jailbreak by moving capture below app-visible proxy settings
The WireGuard / mitmproxy-wireguard material gives a strong reusable operator move:
- when app-visible HTTP proxy settings are bypassed or classified,
- move to VPN/full-tunnel topology,
- capture on the analyst-controlled host at decrypted or reroutable boundaries.

This is strong KB material because it generalizes beyond the specific app.
It is an **observation-topology relocation** workflow.

### 3. iOS VMP/sign recovery still converges on semantic-anchor reduction, not full literal VM understanding
The iOS VMP article is valuable because, despite the platform difference, it reinforces a familiar expert move:
- locate the target field (`x6` etc.)
- freeze unstable/random factors
- run trace over the decisive region
- identify standard crypto constants or transform families from intermediate states
- recover the compact operator model (for example HMAC-SHA256 + MD5-derived parts + fixed decode side data)

This is exactly the same reduction-first philosophy seen in Android protected-runtime work.

### 4. Trace is most valuable when it localizes the transform family, not when it records everything
The iOS VMP article is long, but its most reusable lesson is not “trace more.”
It is:
- use trace to expose where a target byte/word family comes from,
- identify standard constants (`SHA256` IV/K table, MD5 constants, padding/layout markers),
- then collapse the protected routine into a smaller standard-family explanation.

This is strong canonical material because it keeps the workflow disciplined.

### 5. iOS OLLVM / 花指令 cleanup often exists to restore a callable sign pipeline, not to achieve perfect decompilation beauty
The music-sign article contributes a useful code-plane lesson:
- use trace/stalker/de-dup of indirect/control-flow calls to map the real subordinate routines
- identify standard helpers like base64 / digest / XOR-padding / HMAC-like ipad/opad structure
- recover the final sign pipeline even if the top-level function remains visually ugly under OLLVM/flower instructions

This is a very reusable iOS pattern.

### 6. Chomper should be framed as execution-assisted owner recovery and black-box reduction, not merely “iOS unidbg clone”
The Chomper articles are strongest when read as a workflow, not as a tool introduction:
- use frida-trace first to recover the real Objective-C call path and initialization path
- identify framework load, setup/token/init requirements
- emulate enough iOS runtime/framework support to satisfy the owner path
- patch or hook narrow checks/initialization returns if needed
- call the owning ObjC/native method directly and extract output bytes

That is a very powerful KB pattern: **owner recovery first, controlled invocation second**.

### 7. Black-box execution assistance is especially strong when initialization and side conditions are reconstructed from live traces
The `sig3-ios` and `Shield` articles show a repeated operator move:
- do not guess all initialization state from static code alone
- capture setup methods, tokens, SDK init sequences, request-object construction, and parameter-context builders from live frida traces
- replay those inside Chomper

That is highly transferable and should likely become a dedicated workflow note later.

### 8. iOS practical work keeps splitting into the same three decisions as the other branches
This batch suggests a stable iOS decision split:
- **topology**: how to observe traffic or reach the runtime (proxy, VPN, gadget/emulator, etc.)
- **gate**: what initialization / packaging / token / environment requirement must be satisfied first
- **owner**: which ObjC/native method truly owns the target artifact

Only after these are stable should the analyst choose:
- trace-guided semantic reduction
- or black-box execution assistance

This fits the existing KB direction extremely well.

## Concrete operator takeaways worth preserving

### A. iOS traffic-topology relocation workflow
Reusable sequence:
1. if ordinary proxy capture misses key traffic, do not assume cert pinning immediately
2. test whether the app is bypassing or classifying proxy settings
3. move capture topology to VPN/full-tunnel/WireGuard/transparent MITM
4. capture at the analyst-controlled host boundary
5. only then decide whether deeper app-side trust bypass is still necessary

### B. Trace-guided iOS VMP/sign reduction workflow
Reusable sequence:
1. localize the target parameter/field first
2. freeze random/time-based instability if needed
3. trace the decisive region only
4. identify standard-crypto constants, padding, and schedule structures
5. reduce the protected routine into a compact standard-family model
6. preserve fixed side tables/decoded constants separately from dynamic core transforms

### C. OLLVM/flower-instruction callable-pipeline recovery workflow
Reusable sequence:
1. use stalker/trace to map real subordinate calls under OLLVM noise
2. de-duplicate call graphs and classify helpers
3. identify known transform families (base64, digest, HMAC-like xor pads, etc.)
4. recover the minimal callable sign pipeline without demanding perfect source-like decompilation

### D. Chomper owner-recovery and black-box invocation workflow
Reusable sequence:
1. use live frida-trace to recover real init/setup/call chains
2. load the responsible framework/module in Chomper
3. reproduce initialization objects, context builders, tokens, and request wrappers
4. patch or hook only the narrow checks needed to keep the owner path alive
5. call the true ObjC/native owner and extract output bytes or NSString/NSData results

### E. iOS topology/gate/owner triage rule
Reusable sequence:
1. choose the right observation/execution topology
2. identify the first runtime gate (init, token, packaging, environment, or trust requirement)
3. localize the true owner of the target artifact
4. only then pick between semantic trace reduction and execution-assisted black-box replay

## Candidate KB implications
This batch strongly supports or suggests improvements to:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- iOS practical branches under the KB

Potential future child-note opportunities:
- iOS traffic-topology relocation note for non-jailbroken capture
- trace-guided iOS VMP/sign reduction note
- Chomper owner-recovery / black-box invocation note
- iOS topology-gate-owner triage workflow note

## Confidence / quality note
This is a strong first iOS batch.
Its best contribution is that it makes iOS practical reversing look structurally similar to the Android and browser branches:
- pick topology,
- satisfy or localize the gate,
- find the real owner,
- then either reduce semantically or replay in a controlled runtime.

That symmetry is excellent for later cross-branch canonical synthesis.
