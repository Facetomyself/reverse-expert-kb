# V1 Roadmap and Maturity Criteria

## Purpose
This page defines what should count as Version 1 of the reverse-engineering expert knowledge base.

The goal is to prevent the project from growing indefinitely without a stable completion boundary.
A KB like this can always be expanded, but it still needs a meaningful point at which it becomes:
- coherent
- navigable
- internally consistent
- useful as a reference system rather than only as a research scratchpad

This page therefore answers four questions:
- what V1 is supposed to be
- what is already complete enough for V1
- what is still missing for V1
- what should explicitly be deferred beyond V1

## What V1 is
V1 should be understood as:

> the first stable, structured, internally coherent version of the reverse-engineering expert KB, with enough framework, ontology, topic depth, and cross-topic consistency to function as a real knowledge system.

V1 is **not**:
- exhaustive coverage of all reverse-engineering subfields
- a finished book
- a complete benchmark census
- a fully mature ontology for every possible target class
- a frozen final theory of reverse engineering

It is the first version where the KB clearly demonstrates:
- a stable organizing framework
- a stable topic taxonomy
- consistent evaluation language
- real cross-topic navigation
- a meaningful distinction between framework pages, topic syntheses, source notes, and run reports

## What V1 must contain
A V1-complete KB should contain at least the following layers.

### Layer 1. Framework layer
Required pages:
- `topics/expert-re-overall-framework.md`
- `topics/global-map-and-ontology.md`
- `topics/topic-template-and-normalization-guide.md`

Purpose:
- define what the KB is trying to model
- define how topics relate
- define how pages should converge structurally

### Layer 2. Cross-cutting core topic layer
Required pages:
- `topics/benchmarks-datasets.md`
- `topics/symbol-type-and-signature-recovery.md`
- `topics/analyst-workflows-and-human-llm-teaming.md`

Purpose:
- define how methods are evaluated
- define one key family of recovery objects
- define the workflow/sensemaking model that interprets the rest of the KB

### Layer 3. Domain-constraint layer
Required pages:
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`

Purpose:
- show how domain constraints alter reverse-engineering practice
- demonstrate that the KB is not only about generic stripped native binaries

### Layer 4. Gap declaration layer
Required outcome:
- explicit listing of what remains missing or only partially developed

Purpose:
- avoid pretending the ontology is more complete than it is
- make future work legible

## Current V1 status
The KB now appears to have completed most of the V1 skeleton.

### Framework layer status
- `topics/expert-re-overall-framework.md` — present
- `topics/global-map-and-ontology.md` — present
- `topics/topic-template-and-normalization-guide.md` — present

Assessment:
- the framework layer is already strong enough for V1

### Cross-cutting core topic layer status
- `topics/benchmarks-datasets.md` — normalized and strong
- `topics/symbol-type-and-signature-recovery.md` — normalized and strong
- `topics/analyst-workflows-and-human-llm-teaming.md` — normalized and strong

Assessment:
- the core cross-cutting layer is already strong enough for V1

### Domain-constraint layer status
- `topics/mobile-reversing-and-runtime-instrumentation.md` — normalized and strong
- `topics/firmware-and-protocol-context-recovery.md` — normalized and strong
- `topics/obfuscation-deobfuscation-and-packed-binaries.md` — normalized and strong

Assessment:
- the main domain-constraint layer is already strong enough for V1

## What is still missing for a solid V1
Even though the skeleton is strong, V1 is not fully finished yet.
Several missing nodes should ideally be addressed before declaring the KB stable.

### Priority 1 pages
These are the most important pages for closing V1.

#### 1. Decompilation and code reconstruction
Page:
- `topics/decompilation-and-code-reconstruction.md`

Status:
- now added and mature enough for V1

Why it matters:
- decompilation remains one of the central recovery-object families
- this page now closes a major structural gap in the KB

#### 2. Runtime behavior recovery
Page:
- `topics/runtime-behavior-recovery.md`

Status:
- now added and mature enough for V1

Why it matters:
- the KB increasingly emphasizes runtime answerability, observability, traces, and focused experimentation
- this page now closes a major cross-cutting evidence and workflow gap

#### 3. Notebook and memory-augmented reverse engineering
Page:
- `topics/notebook-and-memory-augmented-re.md`

Status:
- now added and mature enough for V1

Why it matters:
- evidence externalization and long-horizon cognitive stability are already central to the KB’s theory
- this page now closes the final Priority 1 workflow-support gap for V1

### Priority 2 missing pages
These would strengthen V1, but are not strictly required before calling it stable.

#### 4. Native desktop reversing methodology baseline
Suggested page:
- `topics/native-binary-reversing-baseline.md`

Why it matters:
- would provide a “default case” against which mobile, firmware, and protected targets can be compared

#### 5. Protocol state/message recovery split
Suggested page:
- `topics/protocol-state-and-message-recovery.md`

Why it matters:
- would separate field-level and state-level protocol reasoning from the broader firmware/context page

#### 6. Anti-tamper / protected-runtime analysis
Suggested page:
- `topics/anti-tamper-and-protected-runtime-analysis.md`

Why it matters:
- would extend the obfuscation page toward protected runtimes and anti-analysis environments

## What can be deferred beyond V1
The following are valuable, but should not block V1.

### Possible V2+ expansions
- Android-specific page split
- iOS-specific page split
- PAC/arm64e dedicated page
- fine-grained protocol benchmarking page
- firmware corpora and metadata page
- unpacking-readiness benchmark page
- LLM failure-mode taxonomy in RE
- domain-specific workflow studies per malware/mobile/firmware
- visual/immersive RE interfaces as their own dedicated page

These are important but belong to later refinement once the KB’s first stable shape is in place.

## Shared maturity criteria
A page should be considered V1-ready if it satisfies all of the following.

### Structural criteria
- has a clear identity section
- declares ontology role
- declares maturity level
- follows the topic normalization structure reasonably well
- includes explicit cross-links to related pages

### Conceptual criteria
- makes at least one explicit core claim
- distinguishes itself clearly from adjacent topics
- explains what it enables for analysts
- includes workflow implications
- includes evaluation dimensions where relevant

### Evidence criteria
- grounded in more than one source or source family
- evidence quality is characterized honestly
- open questions are concrete and useful
- page is more synthesis than source accumulation

### KB-integration criteria
- page fits clearly into the ontology
- page is linkable from multiple other pages
- page helps clarify rather than duplicate neighboring topics

## Shared maturity ladder for the KB
The KB can use the following global maturity labels.

### 1. Seed
- topic identified
- page exists or is planned
- little synthesis yet

### 2. Emerging
- several strong sources gathered
- topic boundaries becoming visible
- some structural claims visible

### 3. Structured
- page has clear organization
- ontology placement is clear
- meaningful open questions exist

### 4. Mature
- page supports cross-topic navigation well
- synthesis outweighs collection
- workflow and evaluation framing are explicit
- likely stable enough for V1

### 5. Canonical
- page acts as a reference anchor for a topic family
- later edits are mostly refinement, not reconceptualization
- page is stable enough to guide the rest of the KB

## Current maturity snapshot
Approximate current status:

### Canonical or near-canonical framework pages
- `topics/expert-re-overall-framework.md`
- `topics/global-map-and-ontology.md`
- `topics/topic-template-and-normalization-guide.md`

### Mature topic pages
- `topics/benchmarks-datasets.md`
- `topics/symbol-type-and-signature-recovery.md`
- `topics/analyst-workflows-and-human-llm-teaming.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`

### Remaining high-priority pages
- none at Priority 1

## V1 completion rule
The KB should count as V1-complete when all of the following are true:

1. The framework layer is stable.
2. The cross-cutting core topic layer is stable.
3. The domain-constraint layer is stable.
4. The Priority 1 topic set is complete and normalized.
5. Cross-links between pages are sufficient that the KB can be navigated as a system.
6. Hourly runs are no longer primarily discovering structure, but mostly filling known gaps.

Current assessment:
- Conditions 1–4 are now satisfied.
- Condition 5 is substantially improved but still worth another dedicated sweep.
- Condition 6 appears to be the right operating target going forward.

That last condition matters.
V1 is not only about page count.
It is about whether the project has moved from structural exploration to structured extension.

## Operational guidance for the hourly cron after this point
The cron should gradually shift its emphasis.

### Earlier phase behavior
- broad exploration
- discovering topic families
- sketching structure

### V1-closing behavior
- fill explicit missing nodes
- deepen primary-source coverage for already recognized pages
- improve cross-links and evidence quality
- reduce repeated rediscovery of already-known structure

### Post-V1 behavior
- incrementally refine mature pages
- split mature pages where justified
- add specialized child topics
- maintain benchmark and literature freshness

## Recommended next build order
The next best order is now:

1. cross-link and metadata cleanup pass across all mature pages
2. `topics/native-binary-reversing-baseline.md`
3. `topics/protocol-state-and-message-recovery.md`
4. `topics/anti-tamper-and-protected-runtime-analysis.md`

This order preserves coherence:
- cleanup strengthens V1 before expanding it
- native baseline adds a useful default comparison case
- protocol split sharpens a page that is already structurally dense
- protected-runtime analysis extends the obfuscation branch without destabilizing the core

## What success looks like after V1
After V1, the KB should feel like:
- a navigable framework rather than a pile of notes
- a system with stable language
- a foundation for deeper topic splits
- a plausible substrate for future handbook writing, retrieval, or agent support

Users of the KB should be able to answer questions such as:
- what kind of reverse-engineering problem is this?
- what recovery object matters next?
- what benchmark family is relevant?
- what domain constraint is changing the workflow?
- what kind of analyst support is likely to help?

## Bottom line
The KB is already past the “interesting research pile” stage.

Its V1 task is now to become a stable system.
That means resisting infinite expansion long enough to close the most important missing nodes, stabilize navigation, and declare a first version that is coherent, useful, and extendable.