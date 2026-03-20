# Global Map and Ontology for the Reverse Engineering Expert Knowledge Base

## Purpose
This page defines how the major topic families in the reverse-engineering expert KB relate to one another.

The goal is to prevent the KB from becoming a flat list of unrelated notes.
Instead, it should behave like a navigable system where each topic can be understood in terms of:
- what it studies
- what it depends on
- what it enables
- what it is often confused with
- which analyst questions it helps answer

## Core ontology
The KB can be understood through six linked layers.

### Layer 1. Analyst goal
This is the real user-level reason reverse engineering is happening.

Examples:
- understand what this binary/app/firmware does
- triage a suspicious target
- recover an algorithm or protocol
- patch diff a security fix
- locate a vulnerability or attack surface
- rehost firmware for fuzzing
- classify protected/obfuscated behavior
- build a long-horizon mental model of a large target

This layer is important because reverse engineering is never done “for decompilation” alone.
The analyst always wants an answer to some larger question.

### Layer 2. Object of recovery
This is the thing the analyst is trying to reconstruct next.

Examples:
- code structure
- control/data flow
- names and symbols
- types and layouts
- function signatures
- runtime behavior
- traces
- protocol fields
- protocol states
- peripheral maps / MMIO context
- platform/environment assumptions

This layer is the best bridge between analyst goals and tool choices.

### Layer 3. Workflow phase
This is where the analyst is in the sensemaking cycle.

Typical phases:
- overview / orientation
- subcomponent scanning
- hypothesis formation
- focused experimentation
- externalization of evidence
- model revision
- convergence on a stable explanation

Different topic families matter more in different phases.

### Layer 4. Domain constraint family
This is the class of environment or target constraints shaping the work.

Examples:
- native desktop binaries
- obfuscated / packed / protected binaries
- mobile platforms
- firmware / embedded targets
- binary protocols
- malware-analysis overlaps
- anti-tamper / anti-cheat contexts

This layer matters because the same recovery object can be easier or harder depending on domain constraints.

### Layer 5. Support mechanism
This is the mechanism that helps the analyst progress.

Examples:
- static analysis
- decompilation
- dynamic instrumentation
- tracing
- type inference
- symbol recovery
- similarity search / diffing
- protocol inference
- context recovery / rehosting support
- notebook / memory support
- LLM assistance

A single analyst question may require multiple support mechanisms.

### Layer 6. Evaluation frame
This is how usefulness should be judged.

Examples:
- correctness
- coverage
- trustworthiness
- false-positive burden
- robustness
- operational cost
- time-to-answer
- downstream utility
- transferability

This layer exists to keep the KB tied to analyst reality instead of output aesthetics.

## Main topic families and their role

### 1. Foundations
Canonical page:
- `topics/expert-re-overall-framework.md`

Role in the ontology:
- defines the shared model for the whole KB
- explains what expert reverse engineering is trying to do
- defines the main axes of organization
- provides the language for comparing other topic families

Dependencies:
- draws on all topic families as they mature

Enables:
- coherent indexing
- shared vocabulary
- stable growth of the KB

### 2. Benchmarks and datasets
Canonical page:
- `topics/benchmarks-datasets.md`

Role in the ontology:
- maps the public evaluation and corpus landscape
- distinguishes benchmark families from training corpora
- clarifies what different papers actually measure

Depends on:
- understanding of recovery objects
- understanding of domain-specific constraints

Enables:
- principled comparison of methods
- reproducibility judgment
- identification of under-benchmarked subdomains

Often confused with:
- a generic “paper list”

Should actually be treated as:
- the evaluation backbone of the KB

### 3. Symbol, type, and signature recovery
Canonical page:
- `topics/symbol-type-and-signature-recovery.md`

Role in the ontology:
- covers semantic metadata recovery that stabilizes analyst navigation
- sits between raw code reconstruction and higher-level understanding

Depends on:
- binary lifting/decompilation context
- benchmark/evaluation structure

Enables:
- better navigation across large targets
- more reliable call-site interpretation
- stronger clustering and semantic anchoring
- more stable human or LLM-assisted reasoning

Strong relationships:
- linked to decompilation quality, but not reducible to it
- affected by obfuscation
- especially important for large targets and long-horizon analysis

### 4. Obfuscation, deobfuscation, and packed binaries
Canonical page:
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`

Role in the ontology:
- models what happens when the target actively resists readability, similarity, or faithful recovery
- forces the KB to care about robustness rather than just nominal performance

Depends on:
- benchmark quality
- similarity/diffing concepts
- semantic recovery concepts

Enables:
- analyst realism under protected targets
- evaluation of resilience under transformation
- packer-aware and anti-analysis-aware reasoning

Strong relationships:
- degrades symbol/type/signature recovery
- degrades decompilation trustworthiness
- changes similarity-search assumptions
- pushes analysts toward dynamic and partial-evidence workflows

### 5. Firmware and protocol context recovery
Canonical page:
- `topics/firmware-and-protocol-context-recovery.md`

Role in the ontology:
- models targets where environment reconstruction is part of the core reverse-engineering problem
- extends RE beyond code into MMIO/peripheral/protocol context

Depends on:
- domain-specific corpora and benchmarks
- protocol inference ideas
- downstream utility framing (rehosting, fuzzing, emulation)

Enables:
- firmware rehosting
- protocol identification
- used-vs-unused hardware discrimination
- more faithful embedded analysis

Strong relationships:
- overlaps with protocol reverse engineering but is not identical to it
- shows why environment/context recovery is a first-class recovery object
- useful counterexample to overly code-centric RE models

### 6. Mobile reversing and runtime instrumentation
Canonical page:
- `topics/mobile-reversing-and-runtime-instrumentation.md`

Role in the ontology:
- models a domain where runtime foothold and instrumentation often matter more than pure static readability
- foregrounds layer selection and access constraints

Depends on:
- workflow models
- dynamic instrumentation concepts
- environment/access strategy concepts

Enables:
- behavior-focused analysis
- managed/native/platform-layer interrogation
- mitigation-aware and hookability-aware reasoning

Strong relationships:
- especially tied to workflow phase and runtime answerability
- useful for understanding the difference between static recoverability and practical observability
- interacts strongly with anti-instrumentation and platform constraints

### 7. Analyst workflows and human–LLM teaming
Canonical page:
- `topics/analyst-workflows-and-human-llm-teaming.md`

Role in the ontology:
- explains how reverse engineering proceeds cognitively and organizationally
- keeps the KB centered on human reasoning, not just tool outputs

Depends on:
- observational and workflow studies
- practical integration patterns
- trust and context management concerns

Enables:
- phase-aware interpretation of tools and benchmarks
- notebook/memory-oriented analysis design
- clearer modeling of where LLMs help and where they hurt

Strong relationships:
- touches every other topic family
- determines whether recovered artifacts are actually usable in practice
- provides the best bridge between benchmarks and lived analyst experience

## Cross-topic dependency map
Below is the intended conceptual dependency structure.

### A. Foundations sits above everything
- Foundations gives language and structure to all topic families.
- Every mature topic should eventually align with the framework defined there.

### B. Benchmarks cut across all technical families
- Benchmarks do not sit beside the other topics as an equal silo.
- They evaluate the other topic families.
- They should be treated as a cross-cutting layer.

### C. Workflow cuts across all technical families
- Workflow is also cross-cutting.
- Every technical capability should ultimately be interpreted in terms of workflow payoff.

### D. Domain families modify technical assumptions
- Mobile, firmware, and obfuscation-heavy targets are not just “examples.”
- They alter what recovery objects matter and how reliable methods are.

### E. Recovery-object topics sit between tools and goals
- Symbol/type/signature recovery is the clearest current example.
- Additional recovery-object pages may later include:
  - decompilation/code reconstruction
  - runtime behavior recovery
  - protocol/state recovery
  - environment reconstruction

## Practical graph view
A useful simplified graph is:

- **Foundations**
  - governs terminology and structure for all pages
- **Workflow / Human-LLM**
  - interprets analyst phases, trust, and cognitive payoff
- **Benchmarks / Datasets**
  - evaluates methods and benchmark families across the KB
- **Recovery-object families**
  - decompilation / code reconstruction
  - symbol / type / signature recovery
  - runtime behavior recovery
  - protocol / state recovery
  - evidence / provenance support
- **Domain-constraint families**
  - native baseline
  - browser runtime
  - mobile runtime instrumentation
  - firmware / protocol context recovery
  - malware-analysis overlaps
  - obfuscation / packed / protected-runtime targets

In dependency terms:
- domain constraints shape which recovery objects matter most
- workflow determines when those recovery objects matter
- benchmarks determine how claims about those recovery objects should be judged
- foundations gives the vocabulary for the entire graph

A practical extension now worth preserving explicitly is that mature domain branches increasingly behave as **operator ladders**, not just topic labels. In other words, once the reader has identified the right branch, the KB should also tell them:
- which recurring bottleneck families define that branch in practice
- what smaller trustworthy boundary should usually be reduced next
- when broad framing should stop and narrower proof work should begin

That practical-branch reading is now part of the KB’s ontology rather than a temporary navigation aid.

## Matrix view
A mature KB should support matrix-like navigation.

### Matrix 1: Topic family × workflow phase
Example questions:
- which topics matter most during orientation?
- which ones matter most during focused experimentation?
- which ones help when hypotheses need to be falsified?

### Matrix 2: Topic family × recovery object
Example questions:
- where do symbol recovery and protocol recovery diverge?
- which domains depend most on environment reconstruction?
- which domains emphasize behavior over structure?

### Matrix 3: Topic family × evaluation dimension
Example questions:
- where is false-positive burden the biggest issue?
- where is robustness under obfuscation the main challenge?
- where does downstream utility matter more than intrinsic score?

### Matrix 4: Topic family × domain constraint
Example questions:
- how does mobile reversing change the value of dynamic instrumentation?
- how does firmware context recovery change the role of static decompilation?
- how do protected binaries change the meaning of similarity and naming recovery?

## Canonical navigation rules for the KB
To keep the KB coherent, readers should be able to move through it in predictable ways.

### Rule 1. Start from analyst question, not tool name
Bad entry:
- “I need Frida/Ghidra/IDA notes.”

Better entry:
- “I need runtime behavior evidence on a mobile target.”
- “I need trustworthy naming/type anchors in a large stripped binary.”
- “I need enough firmware context to rehost and fuzz.”

### Rule 2. Prefer recovery-object framing over tool framing
Tools change. Recovery objects are more stable.

### Rule 3. Always interpret technical pages through workflow payoff
A technique matters because it helps the next analyst move, not because it exists.

### Rule 4. Keep domain constraints explicit
A conclusion that is true for desktop ELF reversing may fail in mobile, firmware, or obfuscated settings.

### Rule 5. Keep evaluation language consistent across topics
Pages should increasingly converge on the same evaluation schema.

## Gaps in the current ontology
The current KB has already filled several earlier missing nodes, so the remaining gaps are now more about canonical alignment and selective depth than about obvious absent top-level pages.

### Earlier missing nodes now present
These are no longer gaps:
- decompilation and code reconstruction as a standalone page
- runtime behavior recovery / trace-based understanding
- protocol state and message recovery as a standalone page
- malware-analysis overlaps as a dedicated page
- anti-tamper / protected-runtime analysis as a dedicated page
- native desktop/server reversing baseline as a dedicated page
- notebook / memory-augmented reverse engineering
- trust calibration / evidence-management support pages

### Current ontology-pressure gaps
The more realistic remaining gaps now are:
- keeping framework, ontology, index, and subtree guides synchronized as branches mature
- deciding when a mature practical branch deserves a denser parent-page summary instead of another leaf note
- deciding when a cross-cutting recovery-object page should explicitly preserve the practical continuations it now feeds
- deciding which mature pages should eventually be treated as canonical rather than merely mature/structured

### Still-thin areas worth watching
Potential future gaps still worth monitoring:
- deeper browser-specific evaluation / benchmark framing
- stronger native-baseline direct source support beyond synthesis-by-contrast
- richer runtime-evidence packaging examples and compare-run preservation patterns
- more explicit anti-cheat / trusted-runtime operator routing if those cases become a sustained branch rather than an edge of protected-runtime work
- clearer separation of browser-only vs hybrid WebView cases at the ontology layer if branch pressure keeps growing there

## V1 ontology milestone
A practical V1 should achieve the following:
- every topic page declares which ontology layer(s) it belongs to
- every topic page links to at least two related pages
- every topic page states:
  - what it studies
  - what it depends on
  - what it enables
  - how it should be evaluated
- the KB contains both:
  - recovery-object pages
  - domain-constraint pages
- at least one global framework page and one global map page are stable

## Bottom line
The ontology of this KB should make one idea unavoidable:

> reverse engineering expertise is not best modeled as tool mastery, but as phase-aware, domain-sensitive recovery of the next trustworthy object under uncertainty.

That is the organizing principle tying the entire KB together.