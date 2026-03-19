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

### Native desktop/server practical branch
- `topics/native-practical-subtree-guide.md`
- `topics/native-binary-reversing-baseline.md`
- `topics/native-semantic-anchor-stabilization-workflow-note.md`
- `topics/native-interface-to-state-proof-workflow-note.md`
- `topics/native-plugin-loader-to-first-real-module-consumer-workflow-note.md`
- `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md`

### Runtime-evidence practical branch
- `topics/runtime-evidence-practical-subtree-guide.md`
- `topics/runtime-behavior-recovery.md`
- `topics/hook-placement-and-observability-workflow-note.md`
- `topics/record-replay-and-omniscient-debugging.md`
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`

This branch should now be read as a practical bridge from runtime-evidence synthesis into four recurring operator bottlenecks:
- subtree navigation and bottleneck selection (`runtime-evidence-practical-subtree-guide`), which acts as the branch entry surface when the analyst first needs to decide whether the current runtime-evidence bottleneck is broad observation/layer-selection uncertainty, smaller hook-placement / truth-boundary uncertainty, capture-stability/replay-worthiness uncertainty, or late-effect-to-causal-boundary localization
- broad runtime answerability and observability framing (`runtime-behavior-recovery`)
- hook-placement / observation-surface selection (`hook-placement-and-observability-workflow-note`), which acts as the practical entry note when runtime work is clearly needed and the broad layer is already plausible, but the analyst still needs one smaller truthful observation surface plus one minimal hook family before replay, reverse-causality, or branch-specific proof work becomes trustworthy
- execution-history and replay tradeoffs (`record-replay-and-omniscient-debugging`), which acts as the practical entry note when the truthful surface is already known but live reruns are too fragile or expensive and one representative execution needs to be stabilized before narrower causal work becomes trustworthy; the branch should explicitly leave broad replay/tooling discussion here once one representative execution is already good enough and the real bottleneck becomes causal-boundary proof, branch-specific follow-up, or evidence packaging
- causal-write / reverse-causality localization (`causal-write-and-reverse-causality-localization-workflow-note`), which acts as the practical entry note when one suspicious late effect is already visible and the analyst needs the first causal write, branch, or state edge that predicts it before broadening into more static reconstruction, provenance cleanup, or wider trace review; the branch should explicitly leave broad reverse-causality work here once one causal boundary is already good enough and the real bottleneck becomes branch-specific proof or evidence packaging

This branch should now be read as a practical bridge from baseline native synthesis into an ordered operator ladder:
- subtree navigation and bottleneck selection (`native-practical-subtree-guide`), which acts as the branch entry surface when the analyst first needs to decide whether the current native bottleneck is semantic instability, route overabundance, module-owner uncertainty, or async ownership break
- static-first orientation and semantic navigation (`native-binary-reversing-baseline`)
- semantic-anchor stabilization (`native-semantic-anchor-stabilization-workflow-note`), which acts as the first practical entry note when pseudocode, names, types, and signatures are readable enough to navigate but the first trustworthy semantic anchor still has to be stabilized before wider relabeling or deeper proof work becomes reliable; the branch should explicitly leave broad semantic-anchor work here once one anchor is already good enough and the real bottleneck becomes representative route proof
- representative interface-path proof (`native-interface-to-state-proof-workflow-note`), which acts as the usual second native step when one semantic anchor is stable enough and imports/strings/xrefs/callbacks expose several plausible routes, but the first consequence-bearing state edge and one downstream effect still need to be proved before the subsystem map becomes trustworthy; the branch should explicitly leave broad route-proof work here once the real bottleneck becomes loader/provider ownership, async delivery, or another narrower continuation rather than representative route choice
- plugin-loader / first-real-module-consumer proof (`native-plugin-loader-to-first-real-module-consumer-workflow-note`), which acts as the usual third native step when one route is already plausible but plugin/module loaders, export-resolution helpers, or provider-installation code still hide the first loaded component that actually becomes behaviorally trustworthy; the branch should explicitly leave broad loader/provider work here once one retained owner is already good enough and the real bottleneck becomes async delivery rather than ownership
- async callback/consumer proof (`native-callback-registration-to-event-loop-consumer-workflow-note`), which acts as the usual fourth native step when one route or loaded-module owner is already plausible but registrations, message pumps, completions, or reactor-loop helpers still hide the first consequence-bearing callback delivery or event-loop consumer that makes the subsystem map behaviorally trustworthy; the branch should explicitly leave broad async callback/event-loop work here once one consequence-bearing consumer is already good enough and the real bottleneck becomes reverse-causality, broader runtime-evidence strategy, or one narrower output-side continuation

### Malware practical branch
- `topics/malware-practical-subtree-guide.md`
- `topics/malware-analysis-overlaps-and-analyst-goals.md`
- `topics/collaborative-malware-analysis-and-role-differentiation.md`
- `topics/staged-malware-execution-to-consequence-proof-workflow-note.md`
- `topics/malware-config-to-capability-bucket-workflow-note.md`
- `topics/malware-sleep-jitter-and-environment-gate-workflow-note.md`
- `topics/malware-reporting-and-handoff-evidence-packaging-workflow-note.md`

This branch should now be read as a practical bridge from malware-overlap synthesis into four recurring operator bottlenecks:
- subtree navigation and laddering (`malware-practical-subtree-guide`), which acts as the branch entry surface when the analyst needs to decide whether the current malware bottleneck is first-consequence proof, config-driven capability reduction, gated progression, or evidence packaging/handoff
- malware goal and triage framing (`malware-analysis-overlaps-and-analyst-goals`)
- collaboration / handoff burden (`collaborative-malware-analysis-and-role-differentiation`)
- staged execution to first proved consequence (`staged-malware-execution-to-consequence-proof-workflow-note`), which acts as the practical entry note when unpack/decrypt/inject/config stages are already visible but the first local handoff that actually predicts payload entry, persistence, comms, or sleep/degrade behavior still needs to be proved before deeper static work, reporting, or detection handoff becomes trustworthy; the branch should explicitly leave broad staged-handoff work here once that first consequence-bearing handoff is already good enough and the real bottleneck becomes config-driven behavior selection, gated progression, or handoff packaging
- config-to-capability reduction (`malware-config-to-capability-bucket-workflow-note`), which acts as the practical entry note when decoded or normalized config material is already visible enough to inspect but the first local reducer or consumer that turns raw config richness into one smaller request family, capability bucket, scheduler policy, plugin path, or persistence mode is still unproved; the branch should explicitly leave broad config-reduction work here once one reduced behavior bucket is already good enough and the real bottleneck becomes continue-vs-stall gating or handoff packaging
- sleep / jitter / environment-gate localization (`malware-sleep-jitter-and-environment-gate-workflow-note`), which acts as the practical entry note when staged or environment-sensitive malware is already visible enough to study and the analyst now needs to prove the first local continue vs sleep / jitter / degrade / suppress gate that actually predicts whether payload, persistence, or first-request behavior happens under the current conditions; the branch should explicitly leave broad gate discussion here once one decisive gate is already proved and the real bottleneck becomes downstream proof or handoff packaging
- reporting / handoff evidence packaging (`malware-reporting-and-handoff-evidence-packaging-workflow-note`), which acts as the practical entry note when a useful malware finding already exists but the result is still too trace-heavy, assumption-heavy, or analyst-private to survive handoff cleanly to another reverser, CTI, detection engineering, incident response, or reporting consumer; the branch should explicitly leave broad packaging discussion here once the package is already small and re-findable enough and the real bottleneck becomes evidence-linkage discipline, trust calibration, or one narrower downstream technical task

### Deobfuscation / protected-runtime practical branch
- `topics/protected-runtime-practical-subtree-guide.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/protected-runtime-observation-topology-selection-workflow-note.md`
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- `topics/flattened-dispatcher-to-state-edge-workflow-note.md`
- `topics/packed-stub-to-oep-and-first-real-module-workflow-note.md`
- `topics/decrypted-artifact-to-first-consumer-workflow-note.md`
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`
- `topics/integrity-check-to-tamper-consequence-workflow-note.md`

This branch should now be read as a practical bridge from mature protected/deobfuscation synthesis into a subtree guide plus seven recurring operator bottlenecks:
- subtree navigation and bottleneck selection (`protected-runtime-practical-subtree-guide`), which acts as the branch entry surface when the case is clearly protected-runtime shaped but the analyst first needs to classify whether the current bottleneck is observation-topology failure, trace/dispatcher churn, packed/bootstrap handoff, artifact-consumer proof, runtime-artifact / initialization-obligation recovery, or integrity/tamper consequence proof
- broad protected/deobfuscation framing and evaluation (`obfuscation-deobfuscation-and-packed-binaries`)
- observation-topology selection (`protected-runtime-observation-topology-selection-workflow-note`), which acts as the practical entry note when direct attach, spawn, app-local hooks, or ordinary instrumentation are themselves unstable, detected, semantically late, or misleading and the analyst first needs one more truthful boundary before narrower protected-runtime work becomes trustworthy
- trace-to-semantic-anchor reduction (`vm-trace-to-semantic-anchor-workflow-note`), which acts as the practical entry note when virtualization, flattening, or handler churn is already visible but the analyst still needs one stable semantic anchor plus one consequence-bearing handler/state edge before deeper static reconstruction becomes trustworthy
- dispatcher-to-state-edge reduction (`flattened-dispatcher-to-state-edge-workflow-note`), which acts as the practical entry note when the dispatcher or flattened region is already recognizable and the next bottleneck is identifying the first durable state object, reduction helper, or dispatcher-exit family that predicts later behavior and yields a trustworthy smaller static target; the branch should explicitly leave broad trace/dispatcher work here once one durable state object and one consequence-bearing state edge are already good enough and the real bottleneck becomes post-unpack handoff, ordinary route proof, or another narrower post-protection continuation
- packed-stub-to-OEP handoff reduction (`packed-stub-to-oep-and-first-real-module-workflow-note`), which acts as the practical entry note when shelling, packing, or staged bootstrap is already visible but the next bottleneck is proving one trustworthy OEP-like boundary plus one downstream ordinary-code anchor that yields a reusable post-unpack dump or smaller static target; the branch should explicitly leave broad packed-startup work here once that handoff is already good enough and the real bottleneck becomes post-unpack semantic-anchor work, artifact-consumer proof, or runtime-artifact / initialization-obligation recovery
- decrypted-artifact-to-first-consumer reduction (`decrypted-artifact-to-first-consumer-workflow-note`), which acts as the practical entry note when strings, config, code blobs, bytecode, tables, or normalized buffers are already visible enough to study and the next bottleneck is proving the first ordinary consumer that turns that recovered artifact into request, parser, policy, scheduler, or payload behavior; the branch should explicitly leave broad artifact-to-consumer work here once one first ordinary consumer and one downstream consequence-bearing handoff are already good enough and the real bottleneck becomes ordinary route-to-state proof, domain-specific consumer follow-up, or runtime-obligation recovery
- runtime-artifact / initialization-obligation recovery (`runtime-table-and-initialization-obligation-recovery-workflow-note`), which acts as the practical entry note when repaired dumps, static tables, or offline reconstructions still look damaged or under-initialized, live/runtime state looks truer, and the next bottleneck is isolating one minimal init chain, runtime table family, initialized image, or side-condition obligation that explains why replay is close-but-wrong; the branch should explicitly leave broad runtime-artifact / initialization-obligation work here once one truthful runtime artifact family and one smallest missing obligation are already good enough and the real bottleneck becomes first-consumer proof, ordinary route proof, or narrower mobile signing follow-up
- integrity-check-to-consequence reduction (`integrity-check-to-tamper-consequence-workflow-note`), which acts as the practical entry note when CRC, checksum, self-hash, signature, or anti-hook verification logic is already visible but the analyst still needs to prove the first reduced result, consequence-bearing tripwire, and one downstream effect that makes the next static or runtime target trustworthy; the branch should explicitly leave broad integrity/tamper work here once one reduced result and one first consequence-bearing tripwire are already good enough and the real bottleneck becomes downstream consumer proof, environment-differential trust work, or platform-specific verdict-to-policy follow-up

### Browser runtime subtree
- `topics/browser-runtime-subtree-guide.md`
- `topics/js-browser-runtime-reversing.md`
- `topics/jsvmp-and-ast-based-devirtualization.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/browser-fingerprint-and-state-dependent-token-generation.md`

A practical routing rule now reinforced across the browser subtree:
- prefer concrete boundary chains over family labels alone
- anchor concrete notes around:
  - bootstrap anchor
  - state write or state exposure boundary
  - validation / refresh / solve boundary
  - first accepted consumer request
- use this especially for Akamai, PerimeterX / HUMAN, Reese84 / `___utmvc`, Turnstile / Arkose / hCaptcha / reCAPTCHA, and request-signature-family notes like TikTok / Xiaohongshu
- `topics/reese84-and-utmvc-workflow-note.md`
- `topics/datadome-geetest-kasada-workflow-note.md`
- `topics/slider-captcha-state-capture-and-trace-comparison-workflow-note.md`
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
- `topics/cloudflare-clearance-cookie-and-js-challenge-workflow-note.md`
- `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md`
- `topics/browser-parameter-path-localization-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
  - now explicitly positioned as the bridge note for cases where callback/hidden-field/message token visibility and token-carrying submit/verify are both visible, but the first downstream accepted consumer request is still the decisive compare-run boundary
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
- request-path and request-boundary recovery (`browser-parameter-path-localization-workflow-note` and `browser-request-finalization-backtrace-workflow-note`), now also read as the browser-side continuation for hybrid cases where the decisive request-finalization edge only becomes visible after native→page reinjection succeeds
- instrumentation and contested observability (`browser-cdp-and-debugger-assisted-re` and `browser-debugger-detection-and-countermeasures`)
- environment and mixed-runtime execution (`browser-environment-reconstruction` and `js-wasm-mixed-runtime-re`)
- concrete mixed-runtime practice (`js-wasm-boundary-tracing`)
- concrete widget/session/iframe lifecycle practice (`cloudflare-turnstile-widget-lifecycle-workflow-note`, `arkose-funcaptcha-session-and-iframe-workflow-note`, `hcaptcha-callback-submit-and-siteverify-workflow-note`, and `recaptcha-v3-and-invisible-workflow-note`), now read with an explicit emphasis on the first accepted consumer request rather than token visibility alone; the Arkose note now also distinguishes callback/message token visibility from verify/update submission and the first downstream accepted consumer
- concrete clearance-cookie / HTML-seeding / first-consumer practice (`cloudflare-clearance-cookie-and-js-challenge-workflow-note`)
- concrete cookie-bootstrap / consumer-path practice (`acw-sc-v2-cookie-bootstrap-and-consumer-path-note`)
- concrete Imperva-family bootstrap / `_Incapsula_Resource` / first-consumer practice (`reese84-and-utmvc-workflow-note`)
- concrete request-signature-family practice (`bytedance-web-request-signature-workflow-note`, `tiktok-web-signature-workflow-note`)
- concrete served-player / transform-chain / throttling-diagnosis practice (`youtube-player-signature-and-nsig-workflow-note`)
- concrete sensor-submission / cookie-validation practice (`akamai-sensor-submission-and-cookie-validation-workflow-note`)
- concrete request-role / `X-KPSDK-*` attachment / invisible-challenge practice (`kasada-x-kpsdk-request-attachment-workflow-note`)
- concrete bootstrap-script / collector-or-solve / cookie-refresh / first-consumer practice (`perimeterx-human-cookie-collector-workflow-note`)
- hybrid WebView/mobile loop-closure practice is now explicitly strengthened around a recurring concrete diagnosis chain: page-seeded cookie/header/bootstrap state may enter native code correctly, yet the decisive browser/page request-finalization edge only appears after lifecycle-correct native→page reinjection and a ready page-side consumer. Read this chain in order when applicable:
  - `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`
  - `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
  - `topics/browser-request-finalization-backtrace-workflow-note.md`

### Mobile / protected-runtime practice subtree
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/ios-practical-subtree-guide.md`
- `topics/ios-traffic-topology-relocation-workflow-note.md`
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`
- `topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md`
- `topics/ios-chomper-owner-recovery-and-black-box-invocation-workflow-note.md`
- `topics/ios-result-callback-to-policy-state-workflow-note.md`
- `topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md`
- `topics/android-linker-binder-ebpf-observation-surfaces.md`
- `topics/android-observation-surface-selection-workflow-note.md`
- `topics/trace-guided-and-dbi-assisted-re.md`
- `topics/unity-il2cpp-state-ownership-and-persistence-workflow-note.md`
- `topics/trace-slice-to-handler-reconstruction-workflow-note.md`
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- `topics/mobile-risk-control-and-device-fingerprint-analysis.md`
- `topics/environment-state-checks-in-protected-runtimes.md`
- `topics/environment-differential-diagnosis-workflow-note.md`
- `topics/observation-distortion-and-misleading-evidence.md`
- `topics/mobile-signing-and-parameter-generation-workflows.md`
- `topics/mobile-signature-location-and-preimage-recovery-workflow-note.md`
- `topics/mobile-challenge-and-verification-loop-analysis.md`
- `topics/mobile-challenge-trigger-and-loop-slice-workflow-note.md`
- `topics/mobile-response-consumer-localization-workflow-note.md`
- `topics/result-code-and-enum-to-policy-mapping-workflow-note.md`
- `topics/attestation-verdict-to-policy-state-workflow-note.md`
- `topics/post-validation-state-refresh-and-delayed-consequence-workflow-note.md`
- `topics/android-network-trust-and-pinning-localization-workflow-note.md`
- `topics/cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note.md`
- `topics/webview-native-mixed-request-ownership-workflow-note.md`
- `topics/webview-custom-scheme-and-navigation-handoff-workflow-note.md`
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
  - now explicitly warns that a correct page→native payload does not prove the case is solved if the later native→page return still misses listener registration, route mount, or stable page-state timing
- `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`

### Firmware / protocol practical branch
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md`
- `topics/protocol-socket-boundary-and-private-overlay-recovery-workflow-note.md`
- `topics/protocol-layer-peeling-and-contract-recovery-workflow-note.md`
- `topics/protocol-content-pipeline-recovery-workflow-note.md`
- `topics/protocol-ingress-ownership-and-receive-path-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`

This branch should now be read as a practical bridge from firmware/protocol synthesis into a subtree guide plus ten recurring operator bottlenecks:
- subtree entry and routing (`protocol-firmware-practical-subtree-guide`), which acts as the compact branch entry note for choosing whether the current bottleneck is still broad context/object-of-recovery framing, boundary selection, socket-boundary/private-overlay object recovery, layer peeling / smaller-contract recovery, content-pipeline continuation, ingress ownership, parser/state consequence, acceptance gating, output handoff, or hardware-side effect proof
- environment/context recovery (`firmware-and-protocol-context-recovery`)
- message/state recovery (`protocol-state-and-message-recovery`)
- capture-failure diagnosis and boundary relocation (`protocol-capture-failure-and-boundary-relocation-workflow-note`), which acts as the practical entry note when the important traffic or protocol object is still not meaningfully visible from the current surface and the analyst must first prove whether the case is dominated by proxy bypass, trust-path mismatch, non-HTTP/private-overlay boundaries, environment-conditioned visibility, or a deeper manifest/key/content pipeline
- socket-boundary / private-overlay recovery (`protocol-socket-boundary-and-private-overlay-recovery-workflow-note`), which acts as the practical entry note when broad visibility has improved enough that the next bottleneck is surfacing the first truthful socket write/read, serializer, or framing-adjacent object before deeper layer peeling, ownership, or parser/state work
- layer-peeling / smaller-contract recovery (`protocol-layer-peeling-and-contract-recovery-workflow-note`), which acts as the practical entry note when traffic, buffers, wrapper objects, or artifact-bearing responses are already visible enough to inspect but still mix framing, compression, serialization, crypto wrapping, RPC shell, or downstream content continuation, and the next bottleneck is isolating one smaller trustworthy contract before ownership, parser/state, or replay work becomes trustworthy; the branch should explicitly leave broad layer-peeling work here once one smaller contract is already good enough and the real bottleneck becomes artifact continuation, receive ownership, parser/state consequence, or replay acceptance
- content-pipeline continuation (`protocol-content-pipeline-recovery-workflow-note`), which acts as the practical entry note when the top-level authenticated request already works well enough to expose a manifest, handle, key path, chunk map, playlist, or signed child-URL bundle, but the real analyst object still lives downstream in one representative artifact ladder that must be reduced before automation, replay, or extraction becomes trustworthy; the branch should explicitly leave broad content-pipeline work here once one representative artifact ladder is already good enough and the real bottleneck becomes automation, key/crypto recovery, or one narrower replay/acceptance gate
- ingress/receive-path ownership localization (`protocol-ingress-ownership-and-receive-path-workflow-note`), which acts as the practical entry note when inbound traffic, receive callbacks, queue/ring activity, framing/reassembly, or deferred receive work are already visible, but the first local receive owner that actually feeds the parser-relevant object or handler family is still unclear; the branch should explicitly leave broad ingress/ownership work here once one receive owner is already good enough and the real bottleneck becomes parser/state consequence, replay acceptance, or later output-side proof
- parser-to-state consequence localization (`protocol-parser-to-state-edge-localization-workflow-note`), which acts as the practical entry note when message families and candidate parsers are already visible but the first state write, reply-family selector, queue/timer insertion, or peripheral action that actually predicts later behavior is still unclear; the branch should explicitly leave broad parser/state work here once one consequence-bearing edge is already good enough and the real bottleneck becomes replay acceptance, reply/output handoff, or hardware-side effect proof
- replay-precondition / state-gate localization (`protocol-replay-precondition-and-state-gate-workflow-note`), which acts as the practical entry note when parser visibility and some field roles already exist, but structurally plausible replay, mutation, or stateful experimentation still fails because the decisive local acceptance gate still hides behind session phase, freshness, pending-request ownership, capability reduction, or another narrow protocol-state precondition; the branch should explicitly leave broad replay/acceptance work here once one gate is already good enough and the real bottleneck becomes emitted output, hardware-side effect proof, or later interrupt/deferred consequence
- reply-emission / transport-handoff localization (`protocol-reply-emission-and-transport-handoff-workflow-note`), which acts as the practical entry note when parser/state work and even local acceptance are already partly visible, but the analyst still needs to prove where an accepted path becomes one concrete emitted reply, serializer/framing path, queue/descriptor commit, or transport/peripheral send handoff before broadening into hardware-side consequence work
- peripheral/MMIO effect proof (`peripheral-mmio-effect-proof-workflow-note`), which acts as the practical entry note when the first outbound handoff is already good enough, candidate peripheral ranges, register families, or hardware-facing handlers are visible, and the first effect-bearing write, queue/DMA/interrupt arm, or status-latch edge still has to be proved before rehosting, modeling, or deeper static work becomes trustworthy
- ISR/deferred-worker consequence proof (`isr-and-deferred-worker-consequence-proof-workflow-note`), which acts as the practical entry note when trigger visibility and even some peripheral-effect visibility already exist, but the decisive boundary is later: the first interrupt/completion/deferred-worker handoff that turns an already-visible hardware-facing activity into durable state, reply, scheduler, or policy behavior

This subtree is now best read as coordinated mobile analyst entry surfaces:
- iOS subtree routing (`ios-practical-subtree-guide`), which acts as the branch entry note when a case is clearly iOS-shaped but the analyst first needs to decide whether the current bottleneck is traffic-topology uncertainty, broad setup/gate uncertainty, post-gate owner uncertainty, specialized Flutter/Dart cross-runtime owner uncertainty, controlled-replay/init-obligation uncertainty, or callback/result-to-policy consequence uncertainty
- iOS practical ladder: traffic-topology relocation (`ios-traffic-topology-relocation-workflow-note`) first when proxy-only visibility is still untrustworthy, then environment-gate diagnosis (`ios-packaging-jailbreak-and-runtime-gate-workflow-note`), then broad post-gate owner localization (`ios-objc-swift-native-owner-localization-workflow-note`), then specialized Flutter/cross-runtime owner recovery (`ios-flutter-cross-runtime-owner-localization-workflow-note`) when the true owner search spans iOS shell, Flutter bridge, Dart runtime, and native workers, then execution-assisted owner replay (`ios-chomper-owner-recovery-and-black-box-invocation-workflow-note`) when the owner path is already plausible enough, broad owner-localization work should stop, and the real bottleneck is now minimal truthful replay, then runtime-table / initialization-obligation recovery (`runtime-table-and-initialization-obligation-recovery-workflow-note`) when replay is already close-but-wrong and the remaining gap has narrowed into one runtime table family, initialized-image boundary, or minimal init/context obligation, then callback/result-to-policy localization (`ios-result-callback-to-policy-state-workflow-note`) once visible result material already exists; together these notes separate traffic-observation topology uncertainty, broad setup/gate uncertainty, consequence ownership across ObjC / Swift / native boundaries, specialized cross-runtime owner proof, execution-assisted owner replay once live truth is good enough, the narrower recovery of one missing runtime-table/init obligation when replay is almost right, and the proof of the first behavior-changing local policy state
- observability under resistance (`anti-frida-and-anti-instrumentation-practice-taxonomy`, `protected-runtime-observation-topology-selection-workflow-note`, `android-linker-binder-ebpf-observation-surfaces`, `android-observation-surface-selection-workflow-note`, and `trace-guided-and-dbi-assisted-re`)
- Unity / IL2Cpp state-ownership and persistence proof (`unity-il2cpp-state-ownership-and-persistence-workflow-note`), which acts as the practical entry note when metadata-visible classes, wrappers, or setters already exist but the real object owner, overwrite/refresh boundary, or persistence consequence is still unclear
- trace-slice reduction and handler reconstruction (`trace-slice-to-handler-reconstruction-workflow-note`), which acts as the practical entry note when execution can be captured but the analyst still needs to reduce one narrow slice into the first consequence-bearing handler, state write, or scheduler edge instead of collecting more trace churn
- VM/flattened-trace semantic-anchor reduction (`vm-trace-to-semantic-anchor-workflow-note`), which acts as the practical entry note when virtualization, flattening, or handler churn is already visible and the analyst must reduce repetitive execution into one stable semantic anchor plus one consequence-bearing handler/state edge before deeper static reconstruction becomes trustworthy
- environment and evidence trust (`environment-state-checks-in-protected-runtimes`, `environment-differential-diagnosis-workflow-note`, and `observation-distortion-and-misleading-evidence`)
- request-shaping and signature recovery (`mobile-signing-and-parameter-generation-workflows` and `mobile-signature-location-and-preimage-recovery-workflow-note`)
- distributed risk / challenge workflows (`mobile-risk-control-and-device-fingerprint-analysis`, `mobile-challenge-and-verification-loop-analysis`, `mobile-challenge-trigger-and-loop-slice-workflow-note`, `mobile-response-consumer-localization-workflow-note`, `result-code-and-enum-to-policy-mapping-workflow-note`, and `post-validation-state-refresh-and-delayed-consequence-workflow-note` as the practical chain from trigger visibility through first consequence-driving policy state into real loop closure or delayed re-entry)
- response-side native consumer localization (`mobile-response-consumer-localization-workflow-note`), which acts as the practical entry note when the relevant request/response family is already known but the first native branch, state write, or follow-up scheduler that changes behavior is still hidden behind parsing, normalization, and callback fan-out
- attestation-verdict-to-policy-state localization (`attestation-verdict-to-policy-state-workflow-note`), which acts as the practical entry note when an integrity / attestation / device-verdict family is already visible but the first local branch that turns verdict material into allow, degrade, retry, block, or challenge behavior is still unclear
- result-code / enum-to-policy mapping localization (`result-code-and-enum-to-policy-mapping-workflow-note`), which acts as the practical entry note when parsed objects or callbacks already expose result codes or enums but the app’s reduction from those values into a smaller local policy bucket is still hidden behind normalization helpers, switch lowering, or later state/scheduler logic
- network trust-path localization (`android-network-trust-and-pinning-localization-workflow-note`), which acts as the practical entry note when the first bottleneck is routing-vs-trust-vs-native-validation diagnosis rather than parameter recovery or challenge-loop analysis
- request-ownership and mixed-stack diagnosis (`cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note`), which acts as the practical entry note when Java-visible request assembly no longer matches the true transport owner and the analyst must separate plain OkHttp, OkHttp-plus-Cronet, direct Cronet/native, and mixed-family ownership before going deeper
- Android Flutter cross-runtime owner recovery (`android-flutter-cross-runtime-owner-localization-workflow-note`), which acts as the practical entry note when Java-visible triggers, Flutter bridge/plugin routing, `libapp.so` business logic, and native helpers all look relevant, but the analyst still needs to prove the first Dart/object owner that actually predicts one target field or consequence before deepening signature, transport, or runtime-table work
- hybrid WebView/native ownership diagnosis (`webview-native-mixed-request-ownership-workflow-note`), which acts as the practical entry note when both page logic and native code appear to participate in the same backend behavior and the analyst must separate intent owner, bridge boundary, transport owner, and response consumer before deepening hooks; it now also explicitly warns that native ownership can be solved while the remaining divergence is still page lifecycle timing, reload/reinit, or native→page consequence
- hybrid navigation/custom-scheme handoff localization (`webview-custom-scheme-and-navigation-handoff-workflow-note`), which acts as the practical entry note when no useful object bridge is visible and the analyst must test whether custom schemes, deep links, route changes, or URL-carried command state are the real page→native handoff boundary
- hybrid bridge payload recovery (`webview-native-bridge-payload-recovery-workflow-note`), which acts as the practical entry note when ownership is already suspected and the next bottleneck is recovering object-bridge, message-channel, or custom-URL handoff payloads before native normalization destroys structure
- hybrid cookie/header/bootstrap state handoff localization (`webview-cookie-header-bootstrap-handoff-workflow-note`), which acts as the practical entry note when page-side state clearly influences native behavior but no explicit object bridge is visible and the analyst must localize the first native consumer through cookie reads, header merges, or bootstrap-store pulls before deeper signing or ownership work; it now also explicitly treats stale bootstrap snapshots and later native→page re-consumption as common reasons a seemingly correct handoff still fails behaviorally
- hybrid native→page return-path and page-consumer diagnosis (`webview-native-response-handoff-and-page-consumption-workflow-note`), which acts as the practical entry note when native code already obtains a meaningful result but the decisive next behavior still happens inside the page and the analyst must separate outbound native emission from the first meaningful page consumer, while also checking whether bridge visibility is being mistaken for consumer readiness, whether coarse page-load anchors are masking SPA/remount timing, and whether lifecycle timing, document-start-vs-late observer placement, listener/port registration order, or callback-wrapper normalization explains why a seemingly correct payload still does not advance behavior

## Notes
This index should evolve to reflect the KB’s actual ontology and maturity state, not merely list files.
The more stable the KB becomes, the more this page should behave like a guide rather than a dump of links.
an a dump of links.
