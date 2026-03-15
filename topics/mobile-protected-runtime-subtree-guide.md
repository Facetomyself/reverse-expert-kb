# Mobile / Protected-Runtime Subtree Guide

Topic class: framework / guide page
Ontology layers: navigation, subtree map, practice guide
Maturity: structured
Related pages:
- topics/mobile-reversing-and-runtime-instrumentation.md
- topics/anti-tamper-and-protected-runtime-analysis.md
- topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md
- topics/android-linker-binder-ebpf-observation-surfaces.md
- topics/trace-guided-and-dbi-assisted-re.md
- topics/community-practice-signal-map.md

## Purpose
This page explains how to navigate the mobile / protected-runtime practice branch of the reverse-expert KB.

This subtree grew out of the manually curated practitioner source cluster, which repeatedly emphasized:
- anti-Frida and anti-instrumentation pressure
- Android-side alternative observation surfaces
- trace-guided and DBI-assisted workflows
- mobile reversing under environment, hook, and protection constraints

This page exists to keep those growth directions coherent.

## Core claim
The mobile / protected-runtime branch should be read as a coordinated subtree about how analysts preserve observability and recover trustworthy runtime evidence when direct app-level analysis becomes constrained, unstable, or detectable.

Its organizing logic is:
- the parent problem is mobile or protected-runtime analysis under observation pressure
- different child pages describe different practical analyst responses to that pressure
- those responses should be understood as complementary workflow choices rather than isolated tricks

## Parent pages
### 1. Mobile runtime parent
- `topics/mobile-reversing-and-runtime-instrumentation.md`

Use this page when the question is broad, such as:
- is this primarily a mobile runtime reversing problem?
- which layer should I observe first?
- what access or instrumentation strategy is the main bottleneck?

### 2. Protected-runtime parent
- `topics/anti-tamper-and-protected-runtime-analysis.md`

Use this page when the question is broad, such as:
- is this mainly a runtime-resistance problem rather than a code-readability problem?
- is observability being actively denied or distorted?
- which protected-runtime branch should I read next?

## Main child branches

### 1. Anti-Frida and anti-instrumentation practice taxonomy
- `topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md`

Read this when the main problem is:
- direct hooks are failing, crashing, or being detected
- you need to classify what kind of instrumentation resistance is present
- you need to distinguish Frida detection, environment checks, integrity checks, and evidence distortion

### 2. Android Linker / Binder / eBPF observation surfaces
- `topics/android-linker-binder-ebpf-observation-surfaces.md`

Read this when the main problem is:
- direct app-layer hooks are not reliable enough
- you need an alternative observation surface
- loader activity, IPC, or lower-level execution traces may reveal the target behavior better

### 3. Trace-guided and DBI-assisted reverse engineering
- `topics/trace-guided-and-dbi-assisted-re.md`

Read this when the main problem is:
- transformed or protected execution paths are too ambiguous statically
- traces may help expose real control structure or hidden behavior
- DBI or execution-derived evidence may support deobfuscation or semantic recovery

## How the branches relate
These pages often form a workflow chain.

### Common path A: direct hooks fail under protection pressure
Typical path:
1. Start at `topics/mobile-reversing-and-runtime-instrumentation.md`
2. Move to `topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md`
3. Use `topics/android-linker-binder-ebpf-observation-surfaces.md` if a different observation layer is needed
4. Use `topics/trace-guided-and-dbi-assisted-re.md` if execution-derived simplification becomes more valuable than direct hooking

### Common path B: transformed / protected native path inside a mobile target
Typical path:
1. Start at `topics/anti-tamper-and-protected-runtime-analysis.md`
2. Move to `topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md`
3. Use `topics/trace-guided-and-dbi-assisted-re.md` for path or handler recovery
4. Use `topics/android-linker-binder-ebpf-observation-surfaces.md` if direct observation remains too unstable

### Common path C: alternative surface first
Typical path:
1. Start at `topics/android-linker-binder-ebpf-observation-surfaces.md`
2. Map system-layer findings back to `topics/mobile-reversing-and-runtime-instrumentation.md`
3. Use `topics/trace-guided-and-dbi-assisted-re.md` if lower-level traces reveal hidden structure worth lifting back into the analysis

## What this subtree is best at
The mobile / protected-runtime subtree is especially strong for:
- anti-instrumentation reasoning
- protected mobile runtime workflows
- alternative observation-surface selection
- trace-guided analysis under observation pressure
- connecting runtime evidence strategy back to higher-level analyst goals

## 4. Mobile risk-control and device-fingerprint analysis
- `topics/mobile-risk-control-and-device-fingerprint-analysis.md`

Read this when the main problem is:
- request behavior depends on device-state collection or app-side trust signals
- signature or parameter recovery is entangled with environment-sensitive logic
- captcha / slider / anti-bot workflows involve mobile-side runtime participation

## What this subtree is weaker at
This subtree is currently weaker on:
- dedicated iOS-only substructure
- formal comparative literature for anti-instrumentation families
- systematic mobile game / anti-cheat separation
- finer child-page separation inside mobile risk-control and environment-state reasoning

## 5. Environment-state checks in protected runtimes
- `topics/environment-state-checks-in-protected-runtimes.md`

Read this when the main problem is:
- root / jailbreak / emulator / resign / packaging / browser-state differences may be changing behavior
- you need to distinguish execution gating from trust-scoring effects
- environment-sensitive failure is currently being confused with anti-instrumentation failure

## 6. Observation distortion and misleading evidence
- `topics/observation-distortion-and-misleading-evidence.md`

Read this when the main problem is:
- the target still runs, but the evidence surface may no longer be trustworthy
- you need to distinguish missing evidence from misleading evidence
- traces, hooks, or environment changes may be altering semantics rather than simply exposing them

## 7. Mobile signing and parameter-generation workflows
- `topics/mobile-signing-and-parameter-generation-workflows.md`

Read this when the main problem is:
- app-side request validity depends on locally generated parameters or signatures
- you need to distinguish input collection, transform chain, and final field placement
- parameter changes across sessions or environments need to be explained rather than merely replayed

## 8. Mobile challenge and verification-loop analysis
- `topics/mobile-challenge-and-verification-loop-analysis.md`

Read this when the main problem is:
- a captcha / verification / anti-bot flow must be understood as a stateful loop rather than a single request
- app-side preprocessing and backend validation need to be separated
- retries, escalations, or challenge-state transitions are changing behavior over time

## Suggested next expansions from this subtree
The most natural next child pages include:
- `topics/ebpf-seccomp-and-svc-tracing-for-mobile-re.md`
- `topics/browser-fingerprint-and-state-dependent-token-generation.md`

### 9. Concrete mobile workflow notes
Current concrete notes:
- `topics/mobile-signature-location-and-preimage-recovery-workflow-note.md`
- `topics/mobile-challenge-trigger-and-loop-slice-workflow-note.md`
- `topics/android-observation-surface-selection-workflow-note.md`
- `topics/environment-differential-diagnosis-workflow-note.md`
- `topics/android-network-trust-and-pinning-localization-workflow-note.md`
- `topics/cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note.md`
- `topics/webview-native-mixed-request-ownership-workflow-note.md`
- `topics/webview-custom-scheme-and-navigation-handoff-workflow-note.md`
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`

Read `mobile-signature-location-and-preimage-recovery-workflow-note` when the main problem is:
- you have one app-side signature or anti-risk field and need a concrete first-pass workflow
- you need attachment-path-first reasoning instead of generic signing taxonomy
- you need preimage-recovery, Java↔JNI split, compare-run strategy, and failure diagnosis guidance

Read `mobile-challenge-trigger-and-loop-slice-workflow-note` when the main problem is:
- the app enters a challenge / captcha / verification branch and you need a concrete first-pass workflow
- you need trigger-boundary-first reasoning instead of focusing only on visible challenge content
- you need loop-slice selection, pre/post state capture, role-labeled protocol modeling, and failure diagnosis guidance

Read `mobile-response-consumer-localization-workflow-note` when the main problem is:
- the relevant request/response family is already known, but the first native branch or state transition that changes behavior is still hidden behind parsing and callback fan-out
- you need to separate raw response bytes, parser boundary, normalized object boundary, and first meaningful consumer
- you need to prove which callback, dispatcher, state write, or request scheduler actually matters before deepening challenge-loop or signing analysis

Read `android-observation-surface-selection-workflow-note` when the main problem is:
- direct app-layer hooks are weak, detected, or semantically unhelpful
- you need to choose among linker / Binder / eBPF / trace-oriented observation surfaces
- you need narrow-slice collection and explicit reconnection of lower-layer evidence back to app meaning

Read `environment-differential-diagnosis-workflow-note` when the main problem is:
- behavior drifts across device, packaging, session, or observation conditions
- you need to tell whether the drift is execution, trust, session, or observation drift
- you need a triage layer that routes you to the right deeper workflow note instead of patching blindly

Read `android-network-trust-and-pinning-localization-workflow-note` when the main problem is:
- the app’s decisive request path is blocked by routing, TLS trust, or certificate pinning uncertainty
- you need to distinguish OkHttp/Java trust paths from Cronet/Flutter/native validation paths
- you need stack-classification-first reasoning, trust-registration anchors, and failure diagnosis for partial/unreliable universal bypass coverage

Read `cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note` when the main problem is:
- Java-visible OkHttp/Retrofit request assembly no longer matches the real transport behavior of the target request
- you need to tell whether the case is plain OkHttp, OkHttp-plus-Cronet transport, direct Cronet/native, or mixed by request family
- you need owner-selection-boundary reasoning before committing to deeper trust hooks, native tracing, or signature-path recovery

Read `webview-native-mixed-request-ownership-workflow-note` when the main problem is:
- the app is hybrid and both WebView/page logic and native code appear to touch the same backend or request family
- you need to separate intent owner, bridge boundary, transport owner, and response consumer
- you need WebView/native ownership diagnosis before committing to page-only hooks, native-only hooks, trust-path localization, or signature recovery

Read `webview-custom-scheme-and-navigation-handoff-workflow-note` when the main problem is:
- no useful object bridge is visible, but page actions still clearly trigger native behavior
- you need to tell whether custom schemes, deep links, route changes, or URL-carried command state are the real page→native handoff
- you need raw navigation-target capture and first native parser localization before deeper payload, signing, or request-ownership work

Read `webview-native-bridge-payload-recovery-workflow-note` when the main problem is:
- hybrid ownership is already suspected and the next bottleneck is recovering what actually crosses the WebView/native bridge
- you need to distinguish object bridges, message-channel bridges, and custom-URL/navigation handoff
- you need payload-shape capture before native normalization, request ownership, signing, or trust-path analysis

Read `webview-cookie-header-bootstrap-handoff-workflow-note` when the main problem is:
- page-side cookies, hidden bootstrap state, or JS-produced header material clearly influence native behavior
- no explicit object bridge is visible, but native requests appear to consume page-seeded state
- you need to localize the first native consumer through `CookieManager`, header merge/interceptor paths, or bootstrap-store reads before deeper signing or ownership work

Read `webview-native-response-handoff-and-page-consumption-workflow-note` when the main problem is:
- native code already retrieves or computes a meaningful result, but the decisive next behavior still happens on the page side
- you need to distinguish `evaluateJavascript(...)`, message-channel posting, and reload/bootstrap refresh as native→page return families
- you need to separate outbound native emission from the first meaningful page callback, store, hidden-field, or request-helper consumer

## Source anchor
The subtree is strongly justified by the practitioner cluster documented in:
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`
- `topics/community-practice-signal-map.md`

## Bottom line
The mobile / protected-runtime subtree is the KB’s main practice branch for preserving observability under active runtime resistance.

Its pages should be read as a coordinated set of analyst entry surfaces into a hard practical problem:
- classify the resistance
- choose a better observation layer
- use traces when direct structure is still too ambiguous