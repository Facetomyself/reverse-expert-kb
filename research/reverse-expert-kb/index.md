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

## Open structural questions
- How should a future native desktop baseline page be defined?
- When should the firmware/context page split protocol state/message recovery into its own child page?
- When should mature pages be promoted from `mature` to `canonical`?
- Which V2 pages are most valuable without destabilizing the V1 structure?

## Candidate next topic pages
Priority 2 candidates include:
- `topics/malware-analysis-overlaps-and-analyst-goals.md`

### Newly added Priority 2 pages
- `topics/analytic-provenance-and-evidence-management.md`
- `topics/native-binary-reversing-baseline.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/trust-calibration-and-verification-burden.md`

### Newly materialized child pages
- `topics/js-browser-runtime-reversing.md`
- `topics/jsvmp-and-ast-based-devirtualization.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`

## Notes
This index should evolve to reflect the KB’s actual ontology and maturity state, not merely list files.
The more stable the KB becomes, the more this page should behave like a guide rather than a dump of links.