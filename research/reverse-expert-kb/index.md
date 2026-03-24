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

- `topics/native-binary-reversing-baseline.md`
- `topics/js-browser-runtime-reversing.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/malware-analysis-overlaps-and-analyst-goals.md`

A practical reading now worth preserving at the top level is:
- the domain layer is no longer just a set of broad synthesis pages
- several branches now also have practical subtree guides that teach recurring operator bottlenecks and stop rules
- maintenance work should therefore keep the **domain parent pages**, **subtree guides**, and **top-level index** synchronized rather than letting branch logic live only in leaves

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

## Current branch-balance view
The KB should now be maintained with explicit branch-balance awareness rather than simple leaf-count growth.

Current practical branch picture:
- **very strong / easy-to-overfeed**:
  - browser runtime anti-bot / captcha / request-signature workflows
  - mobile protected-runtime / WebView / challenge-loop workflows
- **now materially established and worth preserving canonically**:
  - native practical workflows
  - protocol / firmware practical workflows
  - malware practical workflows, now including a sharper Run-key / StartupApproved continuation around startup-live truth vs artifact truth, a sharper Scheduled Task continuation around live-scheduler / reload truth, explicit handoff rules for `ComHandler` and PowerShell Scheduled Job cases, and a thinner dedicated continuation once the real proof object lives in one ScheduledJobs-store definition rather than in task inventory alone; that Scheduled Job continuation should now preserve the split between **definition truth**, **conditions truth**, and **history truth** so current no-run behavior is not overread
  - runtime-evidence practical workflows, now including a sharper compare-run continuation around noisy early mismatches where scheduler/timing/randomness churn can mask the first behavior-bearing divergence, plus a clearer alignment-truth stop rule so the branch keeps tolerated variation, pair-breaking misalignment, and the first explanatory split separate before widening into causality claims
  - iOS practical workflows, now including a clearer callback/block stop rule around freezing the first runtime-backed contract instead of reopening broad owner search too early, plus a dedicated Swift-concurrency continuation seam when callback truth is already good enough but the first continuation-owned consequence boundary still hides the real consumer, and now a sharper reminder that some Swift-heavy cases still hide the first behavior-bearing proof object one hop later at a MainActor-isolated view-model / coordinator / UI-state handoff rather than at raw callback or resume time; the branch should also preserve exact-once continuation discipline as practical branch memory, so callback visibility, continuation creation/storage, actual resume, missing-resume leak/suspend, double-resume misuse, resumed reducer truth, and MainActor-side consumer truth do not collapse into one vague async-drift story
  - protected-runtime deobfuscation ladders, now including a thinner opaque-predicate / computed-next-state bridge between broad VM anchoring and broader flattened state-edge reduction, with stronger dispatch-family-aware recovery memory around helper outputs, table indexes, and copied-code normalization, plus a sharper packed-startup stop rule for Windows/native cases where TLS callbacks or CRT/runtime startup mean the first raw post-unpack transfer is still earlier than the first payload-bearing post-startup handoff
- protected-runtime exception-owned control-transfer work, now sharpened around dispatcher-side landing, dynamic-function-table ownership, trap-family compare pairs, and a clearer landing-truth vs resume-truth split so the branch does not stall at merely proving VEH/SEH existence or at naming dispatcher infrastructure before one behavior-bearing resumed target is actually preserved
- **main maintenance risks**:
  - continuing to add convenient browser/mobile leaves while higher-level branch memory, parent-page routing, and cross-branch comparison drift out of sync
  - letting runtime-evidence stop too often at replay/watchpoint/write-localization language without clearly handing off into the KB’s already-strong consumer/consequence proof style

A top-level maintenance rule worth keeping visible here is:
- when a branch already has a coherent parent page, subtree guide, and several practical leaves, prefer **canonical synchronization**, **branch-balance repair**, or **cross-branch comparison cleanup** before adding another leaf by default
- when choosing new work, bias toward thinner-but-valuable practical continuations rather than the easiest dense micro-branch

## Open structural questions
- Which mature pages or branch summaries are now strong enough to be promoted from `mature` / `structured` to `canonical`?
- Which top-level pages still under-describe the real center of gravity of the KB’s practical branches?
- Where should the next maintenance pass prefer parent-page / index synchronization over adding another leaf note?
- Which thinner practical branches still need one more concrete bridge note before they can be considered locally stable?
- When should the firmware/context branch split further beyond the current protocol state/message and practical workflow surfaces?
- Which V2 pages are most valuable without destabilizing the V1 structure or overfeeding already-dense branches?

## Candidate next topic pages
Priority 2 candidates include:
- none currently urgent enough to list as a single standout from this branch

### Newly added / notable practical continuation pages
- `topics/analytic-provenance-and-evidence-management.md`
- `topics/native-binary-reversing-baseline.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/trust-calibration-and-verification-burden.md`
- `topics/collaborative-malware-analysis-and-role-differentiation.md`
- `topics/opaque-predicate-and-computed-next-state-recovery-workflow-note.md`

### Native desktop/server practical branch
- `topics/native-practical-subtree-guide.md`
- `topics/native-binary-reversing-baseline.md`
- `topics/native-semantic-anchor-stabilization-workflow-note.md`
- `topics/native-interface-to-state-proof-workflow-note.md`
- `topics/native-virtual-dispatch-slot-to-concrete-implementation-workflow-note.md`
- `topics/native-plugin-loader-to-first-real-module-consumer-workflow-note.md`
- `topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md`
- `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md`
- `topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md`
- `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md`
- `topics/decompilation-and-code-reconstruction.md`

A compact native reading now worth preserving at the top level is:
- decompilation is often the practical entry enabler for the native branch, but not the endpoint
- once code is readable enough to navigate, the branch usually reduces through six recurring bottlenecks:
  - semantic-anchor stabilization
  - representative interface-to-state proof
  - virtual-dispatch slot / concrete-implementation proof
  - plugin-loader / first-real-module-consumer reduction
  - service-dispatcher / worker-owned-consumer reduction
  - callback-registration / event-loop consumer proof, with a thinner GUI continuation when the bottleneck narrows specifically into Win32 message-pump / subclass, Qt signal-slot ownership, or Cocoa responder/target-action ownership
- inside that thinner GUI continuation, preserve one extra practical reminder: global framework hooks are often only reduction boundaries, so prefer one per-window, per-receiver-thread, or per-responder first consumer over stopping at shared subclass wrappers, signal emission, or `NSApplication sendEvent:` visibility
- the branch should therefore be remembered not only as “ordinary native binaries,” but as a practical ladder where readable pseudocode is converted into one smaller trustworthy proof boundary before broader subsystem expansion resumes

This branch should now also be read as the default comparison case for the rest of the KB’s domain families:
- less dominated by environment reconstruction than firmware/protocol
- less dominated by access/instrumentation topology than mobile
- less dominated by resistance churn than protected-runtime work
- but still dependent on choosing the next smaller trustworthy object instead of widening the map too early

This branch should now be read as a practical bridge from baseline native synthesis into six recurring operator families, followed by one parent-page routing surface that preserves the same ladder at the synthesis level:
- subtree navigation and bottleneck selection (`native-practical-subtree-guide`), which acts as the branch entry surface when the analyst first needs to decide whether the current native bottleneck is semantic instability, route overabundance, virtual-dispatch implementation uncertainty, module-owner uncertainty, service-owned worker uncertainty, or async ownership break
- broad baseline-native framing and comparison (`native-binary-reversing-baseline`), which now also acts as the parent-page routing surface that preserves the same native six-family ladder at the synthesis level rather than only by leaf-note accumulation
- semantic-anchor stabilization (`native-semantic-anchor-stabilization-workflow-note`), which acts as the first practical entry note when pseudocode, names, types, and signatures are readable enough to navigate but the first trustworthy semantic anchor still has to be stabilized before wider relabeling or deeper proof work becomes reliable; the branch should explicitly leave broad semantic-anchor work here once one anchor is already good enough and the real bottleneck becomes representative route proof
- representative interface-path proof (`native-interface-to-state-proof-workflow-note`), which acts as the usual second native step when one semantic anchor is stable enough and imports/strings/xrefs/callbacks expose several plausible routes, but the first consequence-bearing state edge and one downstream effect still need to be proved before the subsystem map becomes trustworthy; the branch should explicitly leave broad route-proof work here once one route is already good enough and the real bottleneck becomes concrete slot-implementation proof rather than continued route cataloging
- virtual-dispatch slot / concrete-implementation proof (`native-virtual-dispatch-slot-to-concrete-implementation-workflow-note`), which acts as the usual third native step when one route or object family is already plausible but a visible vtable / interface-slot call still has several candidate runtime types or concrete implementations and the first effect-bearing implementation is still unclear; the branch should explicitly leave broad virtual-dispatch work here once one implementation-to-effect chain is already good enough and the real bottleneck becomes loader/provider ownership, service/worker ownership, or async delivery rather than continued hierarchy cataloging
- plugin-loader / first-real-module-consumer proof (`native-plugin-loader-to-first-real-module-consumer-workflow-note`), which acts as the usual fourth native step when one route or concrete implementation family is already plausible but plugin/module loaders, export-resolution helpers, or provider-installation code still hide the first loaded component that actually becomes behaviorally trustworthy; this step now also preserves a thinner Windows-heavy stop rule for delay-load helpers, forwarded exports, API-set-style indirection, and repeated `GetProcAddress` cases: separate **resolution truth** from **consumer truth** and do not stop until one caller-side retained use or later dispatch edge first makes the resolved target behaviorally relevant; the branch should explicitly leave broad loader/provider work here once one retained owner is already good enough and the real bottleneck becomes service-owned worker proof or async delivery rather than ownership
- service-dispatcher / worker-owned-consumer proof (`native-service-dispatcher-to-worker-owned-consumer-workflow-note`), which acts as the usual fifth native step when service/daemon entry, control handlers, command dispatchers, or worker launchers are visible enough to read but the first worker-owned consumer that actually changes behavior is still unclear; the branch should explicitly leave broad service/daemon ownership work here once one worker-owned consumer is already good enough and the real bottleneck becomes narrower callback/event-loop delivery, reverse-causality, or broader runtime-evidence strategy
- async callback/consumer proof (`native-callback-registration-to-event-loop-consumer-workflow-note`), which acts as the usual sixth native step when one route, concrete implementation family, loaded-module owner, or service-owned worker path is already plausible but registrations, message pumps, completions, or reactor-loop helpers still hide the first consequence-bearing callback delivery or event-loop consumer that makes the subsystem map behaviorally trustworthy; the branch should explicitly leave broad async callback/event-loop work here once one consequence-bearing consumer is already good enough and the real bottleneck becomes reverse-causality, broader runtime-evidence strategy, or one narrower output-side continuation
- completion-port / thread-pool first-consumer continuation (`native-completion-port-and-thread-pool-first-consumer-workflow-note`), which acts as the thinner native continuation once the broad async bottleneck has already been reduced into posted work, completion packets, helper-owned thread-pool callbacks, or queue-dequeue ownership and the remaining question is specifically which delivered work item first changes behavior rather than which callback family exists at all

### Protocol / firmware practical branch
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md`
- `topics/protocol-socket-boundary-and-private-overlay-recovery-workflow-note.md`
- `topics/protocol-layer-peeling-and-contract-recovery-workflow-note.md`
- `topics/protocol-schema-externalization-and-replay-harness-workflow-note.md`
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- `topics/protocol-content-pipeline-recovery-workflow-note.md`
- `topics/protocol-ingress-ownership-and-receive-path-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`

This branch should now be read as a practical bridge from firmware/protocol synthesis into eleven recurring operator families:
- subtree navigation and bottleneck selection (`protocol-firmware-practical-subtree-guide`), which acts as the branch entry surface when the analyst first needs to decide whether the current bottleneck is context/object-of-recovery framing, capture-failure / boundary relocation, socket-boundary / private-overlay truth selection, layer peeling, contract externalization into a reusable schema or harness target, content-pipeline continuation, ingress ownership, parser/state consequence, replay acceptance, output handoff, or hardware-side effect / interrupt consequence proof
- broad firmware/protocol framing and comparison (`firmware-and-protocol-context-recovery`)
- message/state recovery framing (`protocol-state-and-message-recovery`)
- capture-failure / boundary relocation (`protocol-capture-failure-and-boundary-relocation-workflow-note`), which acts as the practical entry note when the important traffic or content-bearing object is still partial, misleading, or absent from the current surface and the analyst still needs to prove whether the right next boundary is transparent interception, socket plaintext, serializer/framer adjacency, or a downstream content-manifest boundary
- socket-boundary / private-overlay truth selection (`protocol-socket-boundary-and-private-overlay-recovery-workflow-note`), which acts as the practical entry note when broad visibility is no longer the main problem but the first truthful overlay object is still hiding at socket write/read, serializer, or framing-adjacent surfaces rather than the packet view
- layer peeling / smaller-contract recovery (`protocol-layer-peeling-and-contract-recovery-workflow-note`), which acts as the practical entry note when one visible object already exists but still mixes framing, compression, serialization, crypto wrapping, RPC shell, or continuation structure and the main need is reducing it into one smaller trustworthy contract
- schema externalization / replay-harness generation (`protocol-schema-externalization-and-replay-harness-workflow-note`), which acts as the practical entry note when one smaller trustworthy contract is already visible but still trapped in traces, notes, or target-local objects and the next useful output is one reusable schema, service-contract artifact, or representative replay/edit/fuzz surface before narrower replay-gate debugging begins
- method-contract -> minimal replay-fixture reduction (`protocol-method-contract-to-minimal-replay-fixture-workflow-note`), which acts as the practical thinner continuation when one representative method-bearing contract is already externalized but still not frozen into one truthful request/response, request/completion, or streaming-aware ordered fixture slice plus one smallest constructor path that makes later gate debugging and compare design honest
- content-pipeline continuation (`protocol-content-pipeline-recovery-workflow-note`), which acts as the practical entry note when the first authenticated API family is already visible but the real analyst object continues through manifest/handle, key/path, chunk/segment, or another downstream artifact ladder
- ingress ownership (`protocol-ingress-ownership-and-receive-path-workflow-note`), which acts as the practical entry note when inbound traffic is already visible enough but the first local receive owner that makes parser-relevant handling trustworthy is still unclear
- parser-to-state consequence localization (`protocol-parser-to-state-edge-localization-workflow-note`), which acts as the practical entry note when one parser or dispatch region is already visible and the next bottleneck is the first state/reply/peripheral consequence edge rather than more field cataloging
- replay-precondition / acceptance-gate localization (`protocol-replay-precondition-and-state-gate-workflow-note`), which acts as the practical entry note when replay is already structurally plausible but one narrow freshness/auth/session/state gate still decides whether the interaction really advances
- reply-emission / transport-handoff proof (`protocol-reply-emission-and-transport-handoff-workflow-note`), which acts as the practical entry note when local acceptance or reply-object creation is already partly visible but the first concrete emitted output path is still unproved
- peripheral/MMIO and ISR/deferred consequence proof (`peripheral-mmio-effect-proof-workflow-note`, `isr-and-deferred-worker-consequence-proof-workflow-note`), which act as the late practical entry notes when the decisive uncertainty has already crossed below transport/output proof into one effect-bearing hardware edge or one later durable completion/deferred handoff

A compact protocol/firmware reading worth preserving at the top level is:
- choose the right truth boundary before overcommitting to protocol semantics
- peel one visible object into one smaller trustworthy contract
- externalize that contract into one reusable schema or representative harness target when analyst-private understanding is now the real blocker
- if one method-bearing contract is already externalized, freeze one truthful representative replay fixture plus one smallest constructor path before broad replay-gate guesses
- then prove one ownership, consequence, acceptance, output, or hardware-side edge instead of widening protocol narration forever

### Runtime-evidence practical branch
- `topics/runtime-evidence-practical-subtree-guide.md`
- `topics/runtime-behavior-recovery.md`
- `topics/hook-placement-and-observability-workflow-note.md`
- `topics/record-replay-and-omniscient-debugging.md`
- `topics/representative-execution-selection-and-trace-anchor-workflow-note.md`
- `topics/compare-run-design-and-divergence-isolation-workflow-note.md`
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`
- `topics/first-bad-write-and-decisive-reducer-localization-workflow-note.md`
- `topics/runtime-evidence-package-and-handoff-workflow-note.md`
- `topics/analytic-provenance-and-evidence-management.md`

This branch should now be read as a practical bridge from runtime-evidence synthesis into eight recurring operator families:
- subtree navigation and bottleneck selection (`runtime-evidence-practical-subtree-guide`), which acts as the branch entry surface when the analyst first needs to decide whether the current runtime-evidence bottleneck is broad observation/layer-selection uncertainty, smaller hook-placement / truth-boundary uncertainty, capture-stability/replay-worthiness uncertainty, representative-execution / trace-anchor selection, compare-run design / first-divergence isolation, late-effect-to-causal-boundary localization, or evidence-package / handoff continuation
- broad runtime answerability and observability framing (`runtime-behavior-recovery`)
- hook-placement / observation-surface selection (`hook-placement-and-observability-workflow-note`), which acts as the practical entry note when runtime work is clearly needed and the broad layer is already plausible, but the analyst still needs one smaller truthful observation surface plus one minimal hook family before replay, reverse-causality, or branch-specific proof work becomes trustworthy
- execution-history and replay tradeoffs (`record-replay-and-omniscient-debugging`), which acts as the practical entry note when the truthful surface is already known but live reruns are too fragile or expensive and one representative execution needs to be stabilized before narrower causal work becomes trustworthy; the branch should explicitly leave broad replay/tooling discussion here once replay is already clearly worthwhile and the real bottleneck has narrowed into capture-window and first-anchor selection, compare-run design, causal-boundary proof, branch-specific follow-up, or evidence packaging
- representative-execution / trace-anchor selection (`representative-execution-selection-and-trace-anchor-workflow-note`), which acts as the practical entry note when replay already looks attractive, but the analyst still needs to choose which execution window is worth preserving and which first event family should partition the trace before broader backward search begins; the branch should explicitly leave this work once one bounded execution and one stable first anchor are already good enough and the real bottleneck becomes compare-run design, causal-boundary proof, branch-specific follow-up, or evidence packaging
- compare-run design / first-divergence isolation (`compare-run-design-and-divergence-isolation-workflow-note`), which acts as the practical entry note when one representative execution and one first anchor are already good enough to support comparison, but the analyst still needs to design one useful near-neighbor compare pair, hold the right invariants steady, choose one compare boundary, and isolate the first meaningful divergence before deeper causal work becomes trustworthy; the branch should explicitly leave broad compare-run design work here once one trustworthy pair and one first meaningful divergence are already good enough, and should often reduce that divergence into one durable watched object before proceeding when the diff is still too aggregate for efficient reverse watchpoint or memory-query work
- causal-write / reverse-causality localization (`causal-write-and-reverse-causality-localization-workflow-note`), which acts as the practical entry note when one suspicious late effect or one already-bounded compare-run divergence is already visible and the analyst needs the first causal write, branch, or state edge that predicts it before broadening into more static reconstruction, provenance cleanup, or wider trace review; the branch should explicitly leave broad reverse-causality work here once one causal boundary is already good enough and the real bottleneck becomes branch-specific proof or evidence packaging
- first-bad-write / decisive-reducer localization (`first-bad-write-and-decisive-reducer-localization-workflow-note`), which acts as the practical entry note when a bad late field, state slot, buffer, handle, policy bucket, or delayed consequence is already visible and revisitable enough, but the analyst still needs to choose the narrowest truthful watched object and localize the first bad write or first decisive reducer behind it before wider reverse-causality, branch-specific proof, or packaging work becomes efficient; the branch should explicitly leave broad watched-object / first-bad-write work here once one watched object, one useful write/reducer boundary, and one downstream dependency are already good enough and the real bottleneck becomes branch-specific proof, broader causal-window work, or evidence packaging
- evidence package / handoff continuation (`runtime-evidence-package-and-handoff-workflow-note`), which acts as the practical entry note when one representative execution, compare-run result, or causal claim is already technically good enough, but still too scattered, assumption-heavy, or analyst-private to survive delay, handoff, or narrower branch reuse cleanly; the branch should explicitly leave broad package-building work here once one claim is already re-findable, bounded, and attached to one next consumer, and the real bottleneck becomes either a narrower branch-specific proof step or a broader provenance/notebook-system problem
- provenance / evidence-linkage continuation (`analytic-provenance-and-evidence-management`), which acts as the practical continuation surface when one representative execution, compare-run result, or causal claim is already good enough and the remaining problem is preserving exactly how observations, assumptions, and inferences stay linked for later reuse rather than collecting more broad runtime material

### Malware practical branch
- `topics/malware-practical-subtree-guide.md`
- `topics/malware-analysis-overlaps-and-analyst-goals.md`
- `topics/collaborative-malware-analysis-and-role-differentiation.md`
- `topics/malware-packed-loader-to-first-payload-handoff-workflow-note.md`
- `topics/staged-malware-execution-to-consequence-proof-workflow-note.md`
- `topics/malware-config-to-capability-bucket-workflow-note.md`
- `topics/malware-first-request-family-and-comms-proof-workflow-note.md`
- `topics/malware-request-builder-to-send-boundary-workflow-note.md`
- `topics/malware-persistence-consumer-localization-workflow-note.md`
- `topics/malware-runkey-startup-consumer-proof-workflow-note.md`
- `topics/malware-scheduled-task-consumer-proof-workflow-note.md`
- `topics/malware-powershell-scheduled-job-consumer-proof-workflow-note.md`
- `topics/malware-service-servicemain-consumer-proof-workflow-note.md`
- `topics/malware-service-failure-action-and-timeout-abuse-workflow-note.md`
- `topics/malware-wmi-permanent-event-subscription-consumer-proof-workflow-note.md`
- `topics/malware-com-clsid-hijack-consumer-proof-workflow-note.md`

The persistence-consumer step now explicitly includes thinner startup-side families such as Run-key / StartupApproved autorun chains, Scheduled Task trigger/action chains, PowerShell Scheduled Job definition-owned chains, Windows service / ServiceMain-owned startup chains, WMI permanent event subscriptions, and COM/CLSID-resolution hijack paths, not only generic Run-key or service-install examples, and the malware branch now preserves dedicated narrower continuation leaves for Run-key autorun, Scheduled Task, PowerShell Scheduled Job, service, WMI, and COM/CLSID consumer-proof work.
- `topics/malware-sleep-jitter-and-environment-gate-workflow-note.md`
- `topics/malware-reporting-and-handoff-evidence-packaging-workflow-note.md`

This branch should now be read as a practical bridge from malware-overlap synthesis into eight recurring operator bottlenecks:
- subtree navigation and laddering (`malware-practical-subtree-guide`), which acts as the branch entry surface when the analyst needs to decide whether the current malware bottleneck is payload-entry localization out of a packed/wrapped loader chain, first-consequence proof, config-driven capability reduction, first outbound-family proof, committed send-boundary proof, gated progression, or evidence packaging/handoff
- malware goal and triage framing (`malware-analysis-overlaps-and-analyst-goals`)
- collaboration / handoff burden (`collaborative-malware-analysis-and-role-differentiation`)
- packed-loader to first-payload handoff (`malware-packed-loader-to-first-payload-handoff-workflow-note`), which acts as the practical entry note when packed, installer-wrapped, script-wrapped, or hollowing-heavy startup is already visible and the next bottleneck is turning that visible staging into one trustworthy payload-side handoff boundary plus one reusable next target; the branch should explicitly leave broad packed-loader handoff work here once one payload-side handoff is already good enough and the real bottleneck becomes first later consequence proof rather than payload-entry localization
- staged execution to first proved consequence (`staged-malware-execution-to-consequence-proof-workflow-note`), which acts as the practical entry note when one payload-side handoff is already plausible enough and the first local handoff that actually predicts payload-side consequence, persistence, comms, or sleep/degrade behavior still needs to be proved before deeper static work, reporting, or detection handoff becomes trustworthy; the branch should explicitly leave broad staged-handoff work here once that first consequence-bearing handoff is already good enough and the real bottleneck becomes config-driven behavior selection, first outbound-family proof, gated progression, or handoff packaging
- config-to-capability reduction (`malware-config-to-capability-bucket-workflow-note`), which acts as the practical entry note when decoded or normalized config material is already visible enough to inspect but the first local reducer or consumer that turns raw config richness into one smaller request family, capability bucket, scheduler policy, plugin path, or persistence mode is still unproved; the branch should explicitly leave broad config-reduction work here once one reduced behavior bucket is already good enough and the real bottleneck becomes first outbound-family proof, continue-vs-stall gating, or handoff packaging
- first request-family / communications proof (`malware-first-request-family-and-comms-proof-workflow-note`), which acts as the practical entry note when staged or config-driven setup is already visible enough that networking should be near, but the first local reducer, builder, queue edge, or send boundary that turns broad communications possibility into one smaller beacon/check-in/request family is still unproved; the branch should explicitly leave broad malware-side communications discussion here once one first request family is already good enough and the real bottleneck becomes committed send-boundary proof, persistence-consumer proof, continue-vs-stall gating, narrower protocol/transport recovery, or handoff packaging
- request-builder to committed send-boundary proof (`malware-request-builder-to-send-boundary-workflow-note`), which acts as the practical entry note when one first outbound family is already plausible enough to name, but the first builder, serializer/framing helper, queue edge, wrapper, or object-method call that commits that family to an outbound path is still unproved; the branch should explicitly leave broad malware-side communications discussion here once one first request family and one committed send boundary are already good enough and the real bottleneck becomes narrower protocol/transport truth selection, persistence-consumer proof, continue-vs-stall gating, or handoff packaging
- persistence-consumer localization (`malware-persistence-consumer-localization-workflow-note`), which acts as the practical entry note when persistence is already plausible or artifact-visible but the first startup-side reader, resolver, trigger/action consumer, or service-owned path that turns the durable artifact into one smaller trustworthy startup-side behavior is still unproved; the branch should explicitly leave broad persistence-family labeling and install-time setup discussion here once one persistence consumer is already good enough and the real bottleneck becomes family-specific continuation, upstream mode selection, narrower native/runtime continuation, or handoff packaging
- Run-key / Startup consumer proof (`malware-runkey-startup-consumer-proof-workflow-note`), which acts as the practical thinner-family continuation when the broad persistence step has already narrowed specifically to Windows Run / RunOnce / Startup-folder persistence and the analyst still needs to reduce one artifact/startup-live state/launcher/later-effect chain into one durable execution-relevant proof object; the branch should explicitly leave broad Run-key inventory, generic autorun naming, and install-time registry narration here once one startup-live autorun chain is already good enough and the real bottleneck becomes Scheduled Task/service/COM/WMI continuation, downstream malware-stage proof, evidence packaging, or another narrower continuation
- Scheduled Task consumer proof (`malware-scheduled-task-consumer-proof-workflow-note`), which acts as the practical thinner-family continuation when the broad persistence step has already narrowed specifically to Windows Scheduled Tasks and the analyst still needs to reduce one trigger/action/principal/live-scheduler/later-effect chain into one durable execution-relevant proof object; the branch should explicitly leave broad task inventory, task-name trust, and registration-only narration here once one reduced task chain is already good enough and the real bottleneck becomes PowerShell Scheduled Job continuation, service/COM/WMI continuation, downstream malware-stage proof, evidence packaging, or another narrower continuation
- PowerShell Scheduled Job consumer proof (`malware-powershell-scheduled-job-consumer-proof-workflow-note`), which acts as the practical thinner-family continuation when the Scheduled Task branch or setup path has already narrowed specifically to PSScheduledJob-owned persistence and the analyst still needs to reduce one ScheduledJobs-store definition plus one script-bearing field plus one trigger/options family plus one output/history/effect chain into one durable execution-relevant proof object; this leaf should now also preserve the narrower distinction between prior execution history and current liveness, plus condition-gated no-run cases, so the branch does not overclaim durability from stale output alone; the branch should explicitly leave broad task inventory, cmdlet syntax narration, and generic PowerShell-host evidence here once one reduced job-definition chain is already good enough and the real bottleneck becomes first-request proof, config-mode reduction, reporting, or another narrower continuation
- Windows service / ServiceMain consumer proof (`malware-service-servicemain-consumer-proof-workflow-note`), which acts as the practical thinner-family continuation when the broad persistence step has already narrowed specifically to Windows service persistence and the analyst still needs to reduce one registration / service-entry / worker-or-child / later-effect chain into a durable execution-relevant proof object; the branch should explicitly leave broad service-install inventory, host-process name trust, and registry-only narration here once one service-owned chain is already good enough and the real bottleneck becomes downstream malware-stage proof, evidence packaging, or another narrower continuation
- WMI permanent-subscription consumer proof (`malware-wmi-permanent-event-subscription-consumer-proof-workflow-note`), which acts as the practical thinner-family continuation when the broad persistence step has already narrowed specifically to WMI permanent event subscriptions and the analyst still needs to reduce one `__EventFilter` plus logical consumer plus `__FilterToConsumerBinding` chain into one durable execution-relevant proof object; the branch should explicitly leave broad WMI artifact inventory here once one bound trigger/action chain and one later `WmiPrvSe.exe`-side or timing-consistent effect are already good enough and the real bottleneck becomes downstream malware-stage proof, evidence packaging, or another narrower continuation
- COM / CLSID hijack consumer proof (`malware-com-clsid-hijack-consumer-proof-workflow-note`), which acts as the practical thinner-family continuation when the broad persistence step has already narrowed specifically to COM / CLSID hijacking and the analyst still needs to reduce one trigger process plus one class-resolution winner plus one later host-process load/launch effect into a durable execution-relevant proof object; the branch should explicitly leave broad CLSID inventory and registry-only narration here once one trigger-process / resolution / consequence chain is already good enough and the real bottleneck becomes downstream malware-stage proof, evidence packaging, or another narrower continuation
- sleep / jitter / environment-gate localization (`malware-sleep-jitter-and-environment-gate-workflow-note`), which acts as the practical entry note when staged or environment-sensitive malware is already visible enough to study and the analyst now needs to prove the first local continue vs sleep / jitter / degrade / suppress gate that actually predicts whether payload, persistence, first-request, or committed-send behavior happens under the current conditions; the branch should explicitly leave broad gate discussion here once one decisive gate is already proved and the real bottleneck becomes downstream proof or handoff packaging
- reporting / handoff evidence packaging (`malware-reporting-and-handoff-evidence-packaging-workflow-note`), which acts as the practical entry note when a useful malware finding already exists but the result is still too trace-heavy, assumption-heavy, or analyst-private to survive handoff cleanly to another reverser, CTI, detection engineering, incident response, or reporting consumer; the branch should explicitly leave broad packaging discussion here once the package is already small and re-findable enough and the real bottleneck becomes evidence-linkage discipline, trust calibration, or one narrower downstream technical task

### Deobfuscation / protected-runtime practical branch
- `topics/protected-runtime-practical-subtree-guide.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/anti-instrumentation-gate-triage-workflow-note.md`
- `topics/watchdog-heartbeat-to-enforcement-consumer-workflow-note.md`
- `topics/kernel-callback-telemetry-to-enforcement-consumer-workflow-note.md`
- `topics/protected-runtime-observation-topology-selection-workflow-note.md`
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- `topics/flattened-dispatcher-to-state-edge-workflow-note.md`
- `topics/packed-stub-to-oep-and-first-real-module-workflow-note.md`
- `topics/decrypted-artifact-to-first-consumer-workflow-note.md`
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`
- `topics/integrity-check-to-tamper-consequence-workflow-note.md`
- `topics/exception-handler-owned-control-transfer-workflow-note.md`

This branch should now be read as a practical bridge from mature protected/deobfuscation synthesis into a subtree guide plus eleven recurring protected-runtime operator bottlenecks:
- subtree navigation and bottleneck selection (`protected-runtime-practical-subtree-guide`), which acts as the branch entry surface when the case is clearly protected-runtime shaped but the analyst first needs to classify whether the current bottleneck is anti-instrumentation gate triage, watchdog/heartbeat enforcement reduction, kernel-callback telemetry to enforcement-consumer reduction, observation-topology failure, trace-to-semantic-anchor churn, flattened-dispatcher-to-state-edge reduction, packed/bootstrap handoff, artifact-consumer proof, runtime-artifact / initialization-obligation recovery, integrity/tamper consequence proof, or exception/signal-handler-owned control transfer
- broad protected/deobfuscation framing and evaluation (`obfuscation-deobfuscation-and-packed-binaries`)
- anti-instrumentation gate triage (`anti-instrumentation-gate-triage-workflow-note`), which acts as the practical entry note when some anti-instrumentation effect is already visible but the analyst still needs to prove whether the first decisive gate is artifact-presence, ptrace/tracer-state, watchdog/liveness, loader-time, or environment-coupled before choosing local handling, environment normalization, or broader observation-topology relocation
- watchdog / heartbeat enforcement reduction (`watchdog-heartbeat-to-enforcement-consumer-workflow-note`), which acts as the practical thinner continuation when the case is already clearly watchdog- or heartbeat-shaped and the analyst still needs to reduce one repeated monitor into the first reducer, queue handoff, or enforcement consumer that turns it into kill, stall, degrade, or decoy behavior
- kernel-callback telemetry to enforcement-consumer reduction (`kernel-callback-telemetry-to-enforcement-consumer-workflow-note`), which acts as the practical thinner continuation when callback-heavy kernel telemetry is already visible and the analyst still needs to reduce one registration/trigger-side path into the first rights filter, reducer, queue handoff, service path, or policy object that actually makes the telemetry behaviorally relevant
- observation-topology selection (`protected-runtime-observation-topology-selection-workflow-note`), which acts as the practical entry note when direct attach, spawn, app-local hooks, or ordinary instrumentation are themselves unstable, detected, semantically late, or misleading and the analyst first needs one more truthful boundary before narrower protected-runtime work becomes trustworthy
- trace-to-semantic-anchor reduction (`vm-trace-to-semantic-anchor-workflow-note`), which acts as the practical entry note when virtualization, flattening, or handler churn is already visible but the analyst still needs one stable semantic anchor plus one consequence-bearing handler/state edge before deeper static reconstruction becomes trustworthy; the branch should explicitly leave broad trace/semantic-anchor work here once one stable semantic anchor and one consequence-bearing handler/state edge are already good enough and the real bottleneck becomes dispatcher/state-edge reduction inside a still-recognizable flattened region, ordinary native follow-up in a quieter post-protection region, or a narrower packed/artifact continuation
- dispatcher-to-state-edge reduction (`flattened-dispatcher-to-state-edge-workflow-note`), which acts as the practical entry note when the dispatcher or flattened region is already recognizable and the next bottleneck is identifying the first durable state object, reduction helper, or dispatcher-exit family that predicts later behavior and yields a trustworthy smaller static target; the branch should explicitly leave broad trace/dispatcher work here once one durable state object and one consequence-bearing state edge are already good enough and the real bottleneck becomes post-unpack handoff, ordinary route proof, or another narrower post-protection continuation
- packed-stub-to-OEP handoff reduction (`packed-stub-to-oep-and-first-real-module-workflow-note`), which acts as the practical entry note when shelling, packing, or staged bootstrap is already visible but the next bottleneck is proving one trustworthy OEP-like boundary plus one downstream ordinary-code anchor that yields a reusable post-unpack dump or smaller static target; the branch should explicitly leave broad packed-startup work here once that handoff is already good enough and the real bottleneck becomes post-unpack semantic-anchor work, artifact-consumer proof, or runtime-artifact / initialization-obligation recovery
- decrypted-artifact-to-first-consumer reduction (`decrypted-artifact-to-first-consumer-workflow-note`), which acts as the practical entry note when strings, config, code blobs, bytecode, tables, or normalized buffers are already visible enough to study and the next bottleneck is proving the first ordinary consumer that turns that recovered artifact into request, parser, policy, scheduler, or payload behavior; the branch should explicitly leave broad artifact-to-consumer work here once one first ordinary consumer and one downstream consequence-bearing handoff are already good enough and the real bottleneck becomes ordinary route-to-state proof, domain-specific consumer follow-up, or runtime-obligation recovery
- runtime-artifact / initialization-obligation recovery (`runtime-table-and-initialization-obligation-recovery-workflow-note`), which acts as the practical entry note when repaired dumps, static tables, or offline reconstructions still look damaged or under-initialized, live/runtime state looks truer, and the next bottleneck is isolating one minimal init chain, runtime table family, initialized image, or side-condition obligation that explains why replay is close-but-wrong; the branch should explicitly leave broad runtime-artifact / initialization-obligation work here once one truthful runtime artifact family and one smallest missing obligation are already good enough and the real bottleneck becomes first-consumer proof, ordinary route proof, or narrower mobile signing follow-up
- integrity-check-to-consequence reduction (`integrity-check-to-tamper-consequence-workflow-note`), which acts as the practical entry note when CRC, checksum, self-hash, signature, or anti-hook verification logic is already visible but the analyst still needs to prove the first reduced result, consequence-bearing tripwire, and one downstream effect that makes the next static or runtime target trustworthy; the branch should explicitly leave broad integrity/tamper work here once one reduced result and one first consequence-bearing tripwire are already good enough and the real bottleneck becomes downstream consumer proof, environment-differential trust work, or platform-specific verdict-to-policy follow-up
- exception/signal-handler-owned control transfer (`exception-handler-owned-control-transfer-workflow-note`), which acts as the practical entry note when visible direct control flow still stays incomplete or misleading because traps, faults, breakpoints, unwind lookup, handler registration, or signal delivery may own the meaningful branch; the branch should explicitly leave broad exception-control-transfer work here once one handler-ownership boundary and one consequence-bearing resume/state action are already good enough and the real bottleneck becomes anti-debug continuation, integrity consequence proof, ordinary route/state proof, or broader observation-topology selection

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
- `topics/ios-environment-normalization-and-deployment-coherence-workflow-note.md`
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `topics/ios-trust-path-and-pinning-localization-workflow-note.md`
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`
- `topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md`
- `topics/ios-chomper-owner-recovery-and-black-box-invocation-workflow-note.md`
- `topics/ios-request-signing-finalization-and-preimage-routing-workflow-note.md`
- `topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md`
- `topics/ios-mitigation-aware-replay-repair-workflow-note.md`
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
- `topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- `topics/protocol-content-pipeline-recovery-workflow-note.md`
- `topics/protocol-ingress-ownership-and-receive-path-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md`
- `topics/protocol-pending-request-generation-epoch-and-slot-reuse-workflow-note.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- `topics/mailbox-doorbell-command-completion-workflow-note.md`
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`
- `topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`
- `topics/analytic-provenance-and-evidence-management.md`

This branch should now be read as a practical bridge from firmware/protocol synthesis into a subtree guide plus thirteen recurring operator families, followed by one evidence-linkage continuation surface once the technical proof is already good enough:
- subtree entry and routing (`protocol-firmware-practical-subtree-guide`), which acts as the compact branch entry note for choosing whether the current bottleneck is still broad context/object-of-recovery framing, boundary selection, socket-boundary/private-overlay object recovery, layer peeling / smaller-contract recovery, content-pipeline continuation, ingress ownership, parser/state consequence, acceptance gating, output handoff, mailbox/doorbell publish-completion proof, descriptor ownership-transfer / completion-visibility proof, or hardware-side effect proof
- environment/context recovery (`firmware-and-protocol-context-recovery`)
- message/state recovery (`protocol-state-and-message-recovery`)
- capture-failure diagnosis and boundary relocation (`protocol-capture-failure-and-boundary-relocation-workflow-note`), which acts as the practical entry note when the important traffic or protocol object is still not meaningfully visible from the current surface and the analyst must first prove whether the case is dominated by proxy bypass, trust-path mismatch, non-HTTP/private-overlay boundaries, environment-conditioned visibility, or a deeper manifest/key/content pipeline
- socket-boundary / private-overlay recovery (`protocol-socket-boundary-and-private-overlay-recovery-workflow-note`), which acts as the practical entry note when broad visibility has improved enough that the next bottleneck is surfacing the first truthful socket write/read, serializer, or framing-adjacent object before deeper layer peeling, ownership, or parser/state work
- layer-peeling / smaller-contract recovery (`protocol-layer-peeling-and-contract-recovery-workflow-note`), which acts as the practical entry note when traffic, buffers, wrapper objects, or artifact-bearing responses are already visible enough to inspect but still mix framing, compression, serialization, crypto wrapping, RPC shell, or downstream content continuation, and the next bottleneck is isolating one smaller trustworthy contract before ownership, parser/state, or replay work becomes trustworthy; the branch should explicitly leave broad layer-peeling work here once one smaller contract is already good enough and the real bottleneck becomes service-contract extraction, artifact continuation, receive ownership, parser/state consequence, or replay acceptance
- service-contract / method-dispatch extraction (`protocol-service-contract-extraction-and-method-dispatch-workflow-note`), which acts as the practical entry note when one smaller trustworthy contract already exists and the family already looks service-oriented or RPC-shaped, but the first reusable service shell, interface roster, dispatch table, or representative method contract is still implicit; the branch should explicitly leave broad service-shell cataloging work here once one representative method-bearing contract is already good enough and the real bottleneck becomes schema externalization, handler/state consequence, replay acceptance, or output proof
- content-pipeline continuation (`protocol-content-pipeline-recovery-workflow-note`), which acts as the practical entry note when the top-level authenticated request already works well enough to expose a manifest, handle, key path, chunk map, playlist, or signed child-URL bundle, but the real analyst object still lives downstream in one representative artifact ladder that must be reduced before automation, replay, or extraction becomes trustworthy; the branch should explicitly leave broad content-pipeline work here once one representative artifact ladder is already good enough and the real bottleneck becomes automation, key/crypto recovery, or one narrower replay/acceptance gate
- ingress/receive-path ownership localization (`protocol-ingress-ownership-and-receive-path-workflow-note`), which acts as the practical entry note when inbound traffic, receive callbacks, queue/ring activity, framing/reassembly, or deferred receive work are already visible, but the first local receive owner that actually feeds the parser-relevant object or handler family is still unclear; the branch should explicitly leave broad ingress/ownership work here once one receive owner is already good enough and the real bottleneck becomes parser/state consequence, replay acceptance, or later output-side proof
- parser-to-state consequence localization (`protocol-parser-to-state-edge-localization-workflow-note`), which acts as the practical entry note when message families and candidate parsers are already visible but the first state write, reply-family selector, queue/timer insertion, or peripheral action that actually predicts later behavior is still unclear; the branch should explicitly leave broad parser/state work here once one consequence-bearing edge is already good enough and the real bottleneck becomes replay acceptance, reply/output handoff, or hardware-side effect proof
- replay-precondition / state-gate localization (`protocol-replay-precondition-and-state-gate-workflow-note`), which acts as the practical entry note when parser visibility and some field roles already exist, but structurally plausible replay, mutation, or stateful experimentation still fails because the decisive local acceptance gate still hides behind session phase, freshness, pending-request ownership, capability reduction, or another narrow protocol-state precondition; the branch should explicitly leave broad replay/acceptance work here once one gate is already good enough and the real bottleneck becomes emitted output, hardware-side effect proof, or later interrupt/deferred consequence
- pending-request correlation / async-reply consumption (`protocol-pending-request-correlation-and-async-reply-workflow-note`), which acts as the practical continuation note when the broad replay gate has already collapsed to one outstanding-request owner, correlation-id match, async handle, pending slot, callback queue, or late-reply lifecycle boundary deciding whether a structurally plausible response-like artifact is consumed at all; the branch should explicitly leave broad replay-gate narration once the real unknown is the first owner-match, stale/unknown-reply discard, timeout cleanup, or matched-only wakeup/dequeue effect
- pending-request generation / epoch / slot-reuse realism (`protocol-pending-request-generation-epoch-and-slot-reuse-workflow-note`), which acts as the thinner practical continuation once broad owner-match is already good enough but late replies, timeout/cancel cleanup, reconnect, phase/wrap mismatch, or slot/tag reuse still decide whether the same visible identifier names the current live request or only a stale retired owner; the branch should explicitly leave broad pending-owner discussion once the real unknown is this narrower liveness contract rather than basic owner-match itself
- reply-emission / transport-handoff localization (`protocol-reply-emission-and-transport-handoff-workflow-note`), which acts as the practical entry note when parser/state work and even local acceptance are already partly visible, but the analyst still needs to prove where an accepted path becomes one concrete emitted reply, serializer/framing path, queue/descriptor commit, or transport/peripheral send handoff before broadening into hardware-side consequence work; the branch should explicitly leave broad reply-emission / transport-handoff work here once one committed outbound path is already good enough and the real bottleneck becomes mailbox/doorbell publish-completion proof, descriptor publish/completion-chain proof, hardware-side effect proof, later interrupt/deferred consequence proof, or one narrower output-side continuation
- mailbox/doorbell command publish-completion proof (`mailbox-doorbell-command-completion-workflow-note`), which acts as the practical entry note when one accepted command path or local output-side handler is already visible and one mailbox, command queue, slot, or tail/doorbell path is already plausible, but the analyst still needs the smaller chain from local command staging to peer-visible publish and then to request-linked completion/ack before widening into broader descriptor, MMIO, or interrupt-side reasoning; the branch should explicitly leave broad mailbox/doorbell continuation work here once one publish-to-completion chain is already good enough and the real bottleneck becomes descriptor generalization, narrower MMIO effect proof, later ISR/deferred consequence proof, or replay/model realism
- descriptor publish / completion-chain proof (`descriptor-tail-kick-and-completion-chain-workflow-note`), which acts as the practical entry note when local output-side preparation is already visible and descriptor/ring/mailbox objects are already plausible, but the analyst still needs the first publish/tail/doorbell/owner edge that commits hardware-visible ownership plus one later completion/ISR/deferred reduction that proves the earlier publish mattered; the branch should explicitly leave broad descriptor publish / completion-chain work here once one publish-to-consequence chain is already good enough and the real bottleneck becomes narrower ownership/visibility proof, MMIO effect proof, later ISR/deferred consequence proof, or model realism rather than continued ring taxonomy
- descriptor ownership-transfer / completion-visibility proof (`descriptor-ownership-transfer-and-completion-visibility-workflow-note`), which acts as the practical entry note when one descriptor, ring slot, or completion record is already visible enough to track and the remaining uncertainty is the narrower contract: when ownership changes, when the other side may trust the record, what cache/order boundary matters, and what reclaim or slot reuse proves durable completion; the branch should explicitly leave broad ownership/visibility continuation work here once one trust-and-reclaim contract is already good enough and the real bottleneck becomes narrower MMIO effect proof, later ISR/deferred consequence proof, or model realism rather than continued shared-ring narration
- peripheral/MMIO effect proof (`peripheral-mmio-effect-proof-workflow-note`), which acts as the practical entry note when the first outbound handoff, descriptor publish chain, or descriptor ownership/visibility contract is already good enough, candidate peripheral ranges, register families, or hardware-facing handlers are visible, and the first effect-bearing write, queue/DMA/interrupt arm, or status-latch edge still has to be proved before rehosting, modeling, or deeper static work becomes trustworthy; the branch should explicitly leave broad peripheral/MMIO effect work here once one effect-bearing edge is already good enough and the real bottleneck becomes interrupt/deferred consequence proof, model realism, or one narrower downstream continuation
- ISR/deferred-worker consequence proof (`isr-and-deferred-worker-consequence-proof-workflow-note`), which acts as the practical entry note when trigger visibility and even some peripheral-effect visibility already exist, but the decisive boundary is later: the first interrupt/completion/deferred-worker handoff that turns an already-visible hardware-facing activity into durable state, reply, scheduler, or policy behavior; the branch should explicitly leave broad ISR/deferred consequence work here once one durable consequence edge is already good enough and the real bottleneck becomes model realism, narrower downstream proof, or provenance/evidence packaging
- provenance / evidence-linkage continuation (`analytic-provenance-and-evidence-management`), which acts as the practical continuation surface when one parser/state edge, replay gate, emitted-output path, or hardware-side consequence is already good enough and the remaining problem is preserving the exact assumptions, compare points, and proof slices needed for later replay, handoff, or automation

This subtree is now best read as coordinated mobile analyst entry surfaces:
- iOS subtree routing (`ios-practical-subtree-guide`), which acts as the branch entry note when a case is clearly iOS-shaped but the analyst first needs to decide whether the current bottleneck is traffic-topology uncertainty, environment-normalization/deployment-coherence uncertainty, broad setup/gate uncertainty, trust-path/pinning uncertainty, post-gate owner uncertainty, specialized Flutter/Dart cross-runtime owner uncertainty, controlled-replay/init-obligation uncertainty, callback/block-landing uncertainty, Swift-concurrency continuation-owned consequence uncertainty, or callback/result-to-policy consequence uncertainty
- iOS practical ladder: traffic-topology relocation (`ios-traffic-topology-relocation-workflow-note`) first when proxy-only visibility is still untrustworthy, then environment normalization / deployment-coherence repair (`ios-environment-normalization-and-deployment-coherence-workflow-note`) when install/signing path, rootful-vs-rootless mode, Frida deployment recipe, or repack-vs-live-runtime choice still make runs operationally incomparable, then environment-gate diagnosis (`ios-packaging-jailbreak-and-runtime-gate-workflow-note`), then trust-path / pinning localization (`ios-trust-path-and-pinning-localization-workflow-note`) when one decisive request family is already visible enough and the remaining blocker is routing-vs-trust-vs-post-trust diagnosis on iOS, then broad post-gate owner localization (`ios-objc-swift-native-owner-localization-workflow-note`), then specialized Flutter/cross-runtime owner recovery (`ios-flutter-cross-runtime-owner-localization-workflow-note`) when the true owner search spans iOS shell, Flutter bridge, Dart runtime, and native workers, then execution-assisted owner replay (`ios-chomper-owner-recovery-and-black-box-invocation-workflow-note`) when the owner path is already plausible enough, broad owner-localization work should stop, and the real bottleneck is now minimal truthful replay; that branch should explicitly leave broad replay/harness work once one truthful callable path is already good enough and the real bottleneck has shifted, then use mitigation-aware PAC/arm64e continuation (`arm64e-pac-and-mitigation-aware-ios-reversing.md`) when a modern iOS case has already narrowed into authenticated-pointer, dyld-cache-truthfulness, or replay-close signed-pointer confusion rather than broad setup or owner uncertainty, then continue into iOS request-signing finalization / preimage routing (`ios-request-signing-finalization-and-preimage-routing-workflow-note`) when one owner path is already plausible or partly callable but the next question is still iOS-shaped: prove one last request-finalization boundary, move one hop earlier into preimage/state capture, or stop at one truthful black-box request path, then callback/block landing and signature recovery (`ios-block-callback-landing-and-signature-recovery-workflow-note`) when one callback family is already plausible but the invoke landing and runtime-visible contract still are not trustworthy enough under PAC/callback ambiguity, then Swift-concurrency continuation / async-result consequence routing (`ios-swift-concurrency-continuation-to-policy-workflow-note`) when callback/delegate truth is already good enough or one imported-async owner path is already plausible, but the remaining gap is the first continuation-owned or stream-owned consequence boundary inside Swift task logic, then mitigation-aware replay repair (`ios-mitigation-aware-replay-repair-workflow-note`) when the callback/owner path is already plausible enough and the remaining replay-close gap has narrowed into one authenticated-context, object-materialization, or smaller init/runtime repair target, then continue into runtime-table / initialization-obligation recovery (`runtime-table-and-initialization-obligation-recovery-workflow-note`) when the remaining gap is now clearly one runtime table family, initialized-image boundary, or minimal init/context obligation, then callback/result-to-policy localization (`ios-result-callback-to-policy-state-workflow-note`) once controlled replay, black-box invocation, callback/delegate proof, or narrower continuation-owned consequence proof is already good enough to expose truthful result material and the remaining gap is the first behavior-changing local policy state; together these notes separate thirteen primary recurring families — traffic-observation topology uncertainty, environment-normalization/deployment-coherence uncertainty, broad setup/gate uncertainty, iOS trust-path/pinning uncertainty, consequence ownership across ObjC / Swift / native boundaries, specialized cross-runtime owner proof, controlled-replay uncertainty, mitigation-aware PAC/arm64e continuation, iOS signing-finalization / preimage-routing uncertainty, callback/block-landing truth uncertainty, Swift-concurrency continuation-owned consequence uncertainty, mitigation-aware replay-repair uncertainty, and the proof of the first behavior-changing local policy state — plus one narrower runtime-table/init-obligation continuation that commonly appears once replay is already almost right
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
This index should evolve to reflect the KB’s actual ontology, maturity state, and practical branch shape, not merely list files.
The more stable the KB becomes, the more this page should behave like a guide rather than a dump of links.

A maintenance rule now worth preserving explicitly is:
- when a branch already has a coherent parent page, subtree guide, and several practical leaves, prefer **canonical synchronization** work before adding another leaf by default
- use new leaf pages when there is a real operator gap, not merely because one branch already has momentum
