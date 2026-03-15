# Reverse Expert Knowledge Base Index

## Purpose
Build a long-running, structured knowledge base about how to think like a reverse-engineering expert.

The KB is now best understood as a system for organizing reverse engineering around:
- recovery objects
- workflow and sensemaking
- domain constraints
- evaluation logic
- evidence and memory support

## Current status
The KB has now reached a **V1 structural milestone**:
- framework layer established
- core topic layer established
- domain-constraint layer established
- Priority 1 V1 topic set completed

See:
- `topics/v1-roadmap-and-maturity-criteria.md`
- `topics/v1-review-and-consistency-pass.md`

## How to navigate this KB
A useful reading order is:

1. **Start with the framework**
   - `topics/expert-re-overall-framework.md`
   - `topics/global-map-and-ontology.md`

2. **Understand the normalization and V1 boundary**
   - `topics/topic-template-and-normalization-guide.md`
   - `topics/v1-roadmap-and-maturity-criteria.md`
   - `topics/v1-review-and-consistency-pass.md`

3. **Read the core cross-cutting pages**
   - `topics/benchmarks-datasets.md`
   - `topics/decompilation-and-code-reconstruction.md`
   - `topics/symbol-type-and-signature-recovery.md`
   - `topics/runtime-behavior-recovery.md`
   - `topics/analyst-workflows-and-human-llm-teaming.md`
   - `topics/notebook-and-memory-augmented-re.md`
   - `topics/analytic-provenance-and-evidence-management.md`

4. **Read the domain-constraint pages**
   - `topics/mobile-reversing-and-runtime-instrumentation.md`
   - `topics/firmware-and-protocol-context-recovery.md`
   - `topics/obfuscation-deobfuscation-and-packed-binaries.md`
   - `topics/malware-analysis-overlaps-and-analyst-goals.md`

## Layered topic map

### 1. Framework pages
These pages define the KB’s structure and language.

- `topics/expert-re-overall-framework.md`
- `topics/global-map-and-ontology.md`
- `topics/topic-template-and-normalization-guide.md`
- `topics/v1-roadmap-and-maturity-criteria.md`
- `topics/v1-review-and-consistency-pass.md`

### 2. Core recovery / workflow / evaluation pages
These pages define the central recovery objects, evaluation logic, and analyst workflow support patterns.

- `topics/benchmarks-datasets.md`
- `topics/decompilation-and-code-reconstruction.md`
- `topics/symbol-type-and-signature-recovery.md`
- `topics/runtime-behavior-recovery.md`
- `topics/analyst-workflows-and-human-llm-teaming.md`
- `topics/notebook-and-memory-augmented-re.md`
- `topics/analytic-provenance-and-evidence-management.md`
- `topics/trust-calibration-and-verification-burden.md`
- `topics/community-practice-signal-map.md`

### 3. Domain-constraint pages
These pages show how different target classes change what matters in reverse engineering.

- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/malware-analysis-overlaps-and-analyst-goals.md`
- `topics/js-browser-runtime-reversing.md`

### 4. Source and run material
These directories contain incremental research artifacts rather than canonical synthesis pages.

- `runs/`
- `sources/`
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`

## Current active themes
- reverse-engineering methodology
- expert workflows and heuristics
- staged sensemaking under uncertainty
- code reconstruction and semantic recovery
- runtime evidence and observability
- notebook / memory-augmented analysis
- analytic provenance and evidence management
- trust calibration and verification burden in human–LLM RE
- domain-constrained reversing (mobile / firmware / protected targets)
- benchmarks, datasets, and analyst-relevant evaluation
- collaborative malware analysis, role differentiation, and reporting/handoff burden

## Open structural questions
- How should a future native desktop baseline page be defined?
- When should the firmware/context page split protocol state/message recovery into its own child page?
- When should mature pages be promoted from `mature` to `canonical`?
- Which V2 pages are most valuable without destabilizing the V1 structure?

## Candidate next topic pages
Priority 2 candidates include:
- none currently urgent enough to list as a single standout from this branch

### Newly added Priority 2 pages
- `topics/analytic-provenance-and-evidence-management.md`
- `topics/native-binary-reversing-baseline.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/trust-calibration-and-verification-burden.md`
- `topics/collaborative-malware-analysis-and-role-differentiation.md`

### Browser runtime subtree
- `topics/browser-runtime-subtree-guide.md`
- `topics/js-browser-runtime-reversing.md`
- `topics/jsvmp-and-ast-based-devirtualization.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/browser-fingerprint-and-state-dependent-token-generation.md`
- `topics/reese84-and-utmvc-workflow-note.md`
- `topics/datadome-geetest-kasada-workflow-note.md`
- `topics/slider-captcha-state-capture-and-trace-comparison-workflow-note.md`
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
- `topics/cloudflare-clearance-cookie-and-js-challenge-workflow-note.md`
- `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md`
- `topics/browser-parameter-path-localization-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/bytedance-web-request-signature-workflow-note.md`
- `topics/xiaohongshu-web-signature-workflow-note.md`
- `topics/youtube-player-signature-and-nsig-workflow-note.md`
- `topics/akamai-sensor-submission-and-cookie-validation-workflow-note.md`
- `topics/kasada-x-kpsdk-request-attachment-workflow-note.md`
- `topics/perimeterx-human-cookie-collector-workflow-note.md`
- `topics/cdp-guided-token-generation-analysis.md`
- `topics/browser-cdp-and-debugger-assisted-re.md`
- `topics/browser-debugger-detection-and-countermeasures.md`
- `topics/browser-environment-reconstruction.md`
- `topics/js-wasm-mixed-runtime-re.md`
- `topics/js-wasm-boundary-tracing.md`

This subtree is now best read as coordinated browser analyst entry surfaces:
- structural recovery (`jsvmp-and-ast-based-devirtualization`)
- workflow/state recovery (`browser-side-risk-control-and-captcha-workflows`, `browser-fingerprint-and-state-dependent-token-generation`, `reese84-and-utmvc-workflow-note`, `datadome-geetest-kasada-workflow-note`, `datadome-cookie-challenge-workflow-note`, `geetest-v4-w-parameter-and-validate-workflow-note`, `slider-captcha-state-capture-and-trace-comparison-workflow-note`, and `cloudflare-turnstile-widget-lifecycle-workflow-note`)
- request-path and request-boundary recovery (`browser-parameter-path-localization-workflow-note` and `browser-request-finalization-backtrace-workflow-note`)
- instrumentation and contested observability (`browser-cdp-and-debugger-assisted-re` and `browser-debugger-detection-and-countermeasures`)
- environment and mixed-runtime execution (`browser-environment-reconstruction` and `js-wasm-mixed-runtime-re`)
- concrete mixed-runtime practice (`js-wasm-boundary-tracing`)
- concrete widget/session/iframe lifecycle practice (`cloudflare-turnstile-widget-lifecycle-workflow-note`, `arkose-funcaptcha-session-and-iframe-workflow-note`, `hcaptcha-callback-submit-and-siteverify-workflow-note`, and `recaptcha-v3-and-invisible-workflow-note`)
- concrete clearance-cookie / HTML-seeding / first-consumer practice (`cloudflare-clearance-cookie-and-js-challenge-workflow-note`)
- concrete cookie-bootstrap / consumer-path practice (`acw-sc-v2-cookie-bootstrap-and-consumer-path-note`)
- concrete request-signature-family practice (`bytedance-web-request-signature-workflow-note`, `tiktok-web-signature-workflow-note`)
- concrete served-player / transform-chain / throttling-diagnosis practice (`youtube-player-signature-and-nsig-workflow-note`)
- concrete sensor-submission / cookie-validation practice (`akamai-sensor-submission-and-cookie-validation-workflow-note`)
- concrete request-role / `X-KPSDK-*` attachment / invisible-challenge practice (`kasada-x-kpsdk-request-attachment-workflow-note`)
- concrete collector / cookie-refresh / first-consumer practice (`perimeterx-human-cookie-collector-workflow-note`)

### Mobile / protected-runtime practice subtree
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md`
- `topics/android-linker-binder-ebpf-observation-surfaces.md`
- `topics/android-observation-surface-selection-workflow-note.md`
- `topics/trace-guided-and-dbi-assisted-re.md`
- `topics/mobile-risk-control-and-device-fingerprint-analysis.md`
- `topics/environment-state-checks-in-protected-runtimes.md`
- `topics/environment-differential-diagnosis-workflow-note.md`
- `topics/observation-distortion-and-misleading-evidence.md`
- `topics/mobile-signing-and-parameter-generation-workflows.md`
- `topics/mobile-signature-location-and-preimage-recovery-workflow-note.md`
- `topics/mobile-challenge-and-verification-loop-analysis.md`
- `topics/mobile-challenge-trigger-and-loop-slice-workflow-note.md`
- `topics/android-network-trust-and-pinning-localization-workflow-note.md`
- `topics/cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note.md`
- `topics/webview-native-mixed-request-ownership-workflow-note.md`
- `topics/webview-custom-scheme-and-navigation-handoff-workflow-note.md`
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`

This subtree is now best read as six coordinated mobile analyst entry surfaces:
- observability under resistance (`anti-frida-and-anti-instrumentation-practice-taxonomy`, `android-linker-binder-ebpf-observation-surfaces`, `android-observation-surface-selection-workflow-note`, and `trace-guided-and-dbi-assisted-re`)
- environment and evidence trust (`environment-state-checks-in-protected-runtimes`, `environment-differential-diagnosis-workflow-note`, and `observation-distortion-and-misleading-evidence`)
- request-shaping and signature recovery (`mobile-signing-and-parameter-generation-workflows` and `mobile-signature-location-and-preimage-recovery-workflow-note`)
- distributed risk / challenge workflows (`mobile-risk-control-and-device-fingerprint-analysis`, `mobile-challenge-and-verification-loop-analysis`, and `mobile-challenge-trigger-and-loop-slice-workflow-note`)
- response-side native consumer localization (`mobile-response-consumer-localization-workflow-note`), which acts as the practical entry note when the relevant request/response family is already known but the first native branch, state write, or follow-up scheduler that changes behavior is still hidden behind parsing, normalization, and callback fan-out
- network trust-path localization (`android-network-trust-and-pinning-localization-workflow-note`), which acts as the practical entry note when the first bottleneck is routing-vs-trust-vs-native-validation diagnosis rather than parameter recovery or challenge-loop analysis
- request-ownership and mixed-stack diagnosis (`cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note`), which acts as the practical entry note when Java-visible request assembly no longer matches the true transport owner and the analyst must separate plain OkHttp, OkHttp-plus-Cronet, direct Cronet/native, and mixed-family ownership before going deeper
- hybrid WebView/native ownership diagnosis (`webview-native-mixed-request-ownership-workflow-note`), which acts as the practical entry note when both page logic and native code appear to participate in the same backend behavior and the analyst must separate intent owner, bridge boundary, transport owner, and response consumer before deepening hooks
- hybrid navigation/custom-scheme handoff localization (`webview-custom-scheme-and-navigation-handoff-workflow-note`), which acts as the practical entry note when no useful object bridge is visible and the analyst must test whether custom schemes, deep links, route changes, or URL-carried command state are the real page→native handoff boundary
- hybrid bridge payload recovery (`webview-native-bridge-payload-recovery-workflow-note`), which acts as the practical entry note when ownership is already suspected and the next bottleneck is recovering object-bridge, message-channel, or custom-URL handoff payloads before native normalization destroys structure
- hybrid cookie/header/bootstrap state handoff localization (`webview-cookie-header-bootstrap-handoff-workflow-note`), which acts as the practical entry note when page-side state clearly influences native behavior but no explicit object bridge is visible and the analyst must localize the first native consumer through cookie reads, header merges, or bootstrap-store pulls before deeper signing or ownership work
- hybrid native→page return-path and page-consumer diagnosis (`webview-native-response-handoff-and-page-consumption-workflow-note`), which acts as the practical entry note when native code already obtains a meaningful result but the decisive next behavior still happens inside the page and the analyst must separate outbound native emission from the first meaningful page consumer

## Notes
This index should evolve to reflect the KB’s actual ontology and maturity state, not merely list files.
The more stable the KB becomes, the more this page should behave like a guide rather than a dump of links.p of links.