# Topic Template and Normalization Guide

## Purpose
This page defines the canonical structure for topic pages in the reverse-engineering expert KB.

The goal is to stop topic pages from drifting into incompatible styles.
A mature KB needs topic pages that are:
- comparable
- linkable
- incrementally improvable
- evaluable under a shared framework
- readable both by humans and future retrieval/agent systems

This template should be used for all major topic pages going forward.
Older pages should be gradually normalized toward it.

## Why normalization matters
Without a stable topic template, the KB will drift toward:
- uneven page quality
- repeated insights in different wording
- incompatible evaluation language
- missing cross-links
- unclear page maturity
- difficulty distinguishing framework pages from synthesis pages

Normalization makes the KB more usable as:
- a research map
- a study reference
- a future handbook draft
- an AI-ready knowledge substrate

## Page classes in this KB
Before applying a template, each page should be identified as one of four classes.

### 1. Framework page
Purpose:
- define the structure of the KB
- introduce global concepts
- establish canonical vocabulary

Examples:
- `topics/expert-re-overall-framework.md`
- `topics/global-map-and-ontology.md`

These should not be written like ordinary topic pages.
They are meta-pages.

### 2. Topic synthesis page
Purpose:
- synthesize a topic family
- explain why it matters
- summarize high-signal sources and distinctions
- define open questions

Examples:
- `topics/benchmarks-datasets.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/symbol-type-and-signature-recovery.md`

This template is mainly for these pages.

### 3. Source note page
Purpose:
- capture compact notes from a source cluster, search pass, or paper family
- preserve traceability without forcing full synthesis yet

Examples:
- notes under `sources/`

These should remain compact and traceable, not over-structured.

### 4. Run report
Purpose:
- record what a single cron run discovered or changed
- distinguish genuinely new findings from repeated known material

Examples:
- files under `runs/`

These should be incremental and operational, not canonical.

## Canonical template for topic synthesis pages
Each mature topic page should converge toward the following structure.

---

# [Topic Title]

## 1. Topic identity

### What this topic studies
State the topic in one or two sentences.

### Why this topic matters
Explain why the topic deserves to exist as its own node in the KB.

### Ontology role
Declare which ontology layers this page belongs to.
Possible roles include:
- analyst goal
- object of recovery
- workflow/sensemaking
- domain constraint family
- support mechanism
- evaluation frame

### Page class
Usually:
- topic synthesis page

### Maturity status
Use one of:
- seed
- emerging
- structured
- mature
- canonical

---

## 2. Core framing

### Core claim
What is the strongest current claim of this page?

### What this topic is not
Prevent scope drift by naming adjacent areas that should not be conflated with this one.

### Key distinctions
List the distinctions that should be used consistently.
Examples:
- readability vs trustworthiness
- static recoverability vs runtime answerability
- protocol inference vs firmware context recovery
- decompilation quality vs symbol recovery quality

---

## 3. What this topic depends on
List the prerequisites or adjacent concepts needed to interpret this topic correctly.

Examples:
- benchmark quality
- workflow models
- domain constraints
- decompilation context
- dynamic instrumentation access

---

## 4. What this topic enables
Explain what this topic helps an analyst do.
Focus on practical next-step value.

Examples:
- better orientation in large binaries
- stronger triage
- faster hypothesis rejection
- rehosting readiness
- protocol fuzzing
- patch diff interpretation

---

## 5. High-signal sources and findings
This is the main synthesis body.
Group sources by subtheme where possible.

Recommended pattern:
- source name / paper / repo
- high-confidence findings
- why it matters to the KB

This section should favor synthesis over long paraphrase.

---

## 6. Analyst workflow implications
Explicitly answer:
- when in the workflow this topic matters most
- what analyst decisions it affects
- what kinds of mistakes it helps prevent
- how it changes the next trustworthy object

This section is mandatory for mature pages.

---

## 7. Evaluation dimensions
Every mature topic page should state how work in this area ought to be judged.

Use the shared evaluation vocabulary when possible:
- correctness
- coverage
- trustworthiness
- false-positive burden
- robustness
- operational cost
- workflow payoff
- downstream utility
- transferability

Also note if certain dimensions matter more than others for this topic.

---

## 8. Cross-links to related topics
Each topic page should explicitly link to at least two related pages.

Use patterns such as:
- closely related pages
- contrasts with
- depends on
- often confused with
- extends into

This is important for navigation and later agent retrieval.

---

## 9. Open questions
List unresolved questions that define the next research frontier for this topic.
These should be concrete enough to guide future runs.

---

## 10. Suggested next expansions
If the topic is likely to split later, note the likely child pages.

Examples:
- split Android vs iOS
- split symbol vs type recovery
- add anti-instrumentation subpage
- add state-machine recovery subpage

---

## 11. Source footprint / evidence quality note
Briefly characterize the current evidence base.
Examples:
- mostly abstract-level evidence so far
- good paper coverage but weak practitioner coverage
- strong practitioner sources, weak benchmark formalization
- early but coherent signals

This helps keep confidence calibrated.

---

## 12. Topic summary
End with a compact summary paragraph that states why this topic matters in the final KB.

## Minimal front-matter block (optional but recommended)
Pages may also begin with a compact metadata block like:

```markdown
Topic class: topic synthesis
Ontology layers: object-of-recovery, evaluation-frame
Maturity: structured
Related pages:
- topics/benchmarks-datasets.md
- topics/obfuscation-deobfuscation-and-packed-binaries.md
```

This is optional for now, but recommended if the KB later becomes machine-indexed.

## Maturity model
Use this shared maturity ladder.

### Seed
- page exists
- topic identified
- minimal framing only
- sources sparse or noisy

### Emerging
- high-signal sources collected
- some distinctions visible
- enough material to justify the page

### Structured
- page has clear internal organization
- topic is placed in the ontology
- workflow implications are becoming visible
- open questions are meaningful

### Mature
- page uses the canonical structure fairly well
- evaluation language is explicit
- cross-links are good
- synthesis is stronger than collection

### Canonical
- page is stable enough to serve as a reference hub for the topic
- terminology is unlikely to change much
- later updates mostly refine, not redefine, the topic

## Normalization rules for existing pages
When updating older topic pages, normalize in this order.

### Rule 1. Preserve the best existing synthesis
Do not rewrite a page just to satisfy structure.
Keep what is already strong.

### Rule 2. Add missing ontology identity first
Before expanding content, make sure the page states:
- what it studies
- why it matters
- what role it plays in the KB

### Rule 3. Add workflow implications before adding more source bullets
This KB is about expert RE, not source accumulation for its own sake.

### Rule 4. Add evaluation framing before adding more examples
Without evaluation framing, topic pages become descriptive but not decision-useful.

### Rule 5. Add cross-links early
Pages should not remain isolated.

### Rule 6. Leave source notes and run reports alone unless needed
Do not over-normalize non-canonical page classes.

## Priority normalization order for current pages
Suggested order:
1. `topics/benchmarks-datasets.md`
2. `topics/symbol-type-and-signature-recovery.md`
3. `topics/analyst-workflows-and-human-llm-teaming.md`
4. `topics/firmware-and-protocol-context-recovery.md`
5. `topics/mobile-reversing-and-runtime-instrumentation.md`
6. `topics/obfuscation-deobfuscation-and-packed-binaries.md`

Rationale:
- benchmarks and symbol/type recovery are central structural pages
- workflow is the main cross-cutting human layer
- firmware/mobile/obfuscation are important domain modifiers

## V1 normalization standard
A topic page should count as V1-ready if it has:
- clear topic identity
- ontology role declared
- maturity status declared
- at least one explicit core claim
- at least one workflow-implication section
- at least one evaluation-dimensions section
- at least two related-page links
- meaningful open questions

## Bottom line
A strong KB is not just a pile of insightful pages.
It is a set of pages that can be read together under a shared model.

This template is the mechanism for making that happen.