# Benchmarks and Datasets for Reverse Engineering Research

Topic class: topic synthesis
Ontology layers: evaluation frame, object-of-recovery, domain-constraint crosscut
Maturity: mature
Related pages:
- topics/expert-re-overall-framework.md
- topics/global-map-and-ontology.md
- topics/symbol-type-and-signature-recovery.md
- topics/obfuscation-deobfuscation-and-packed-binaries.md
- topics/firmware-and-protocol-context-recovery.md

## 1. Topic identity

### What this topic studies
This topic studies the benchmark, dataset, and corpus landscape relevant to reverse engineering.

It focuses on how reverse-engineering methods are evaluated across different recovery objects, including decompilation, symbol recovery, type inference, binary understanding, protocol inference, firmware context recovery, and adjacent RE-relevant corpora.

### Why this topic matters
A reverse-engineering expert KB should not only know what tools and methods exist. It also needs to know:
- what is actually being measured
- what kind of ground truth exists
- which benchmarks are analyst-relevant versus merely convenient
- which datasets are training corpora versus evaluation corpora
- which results are likely to transfer into real analyst work

Without this topic, the rest of the KB risks becoming a collection of claims without a stable way to compare them.

### Ontology role
This page mainly belongs to:
- **evaluation frame**
- **object-of-recovery**

It is also cross-cutting across domain families because different domains require different benchmark families.

### Page class
- topic synthesis page

### Maturity status
- mature

## 2. Core framing

### Core claim
Reverse-engineering evaluation is fragmenting into multiple benchmark families, and that fragmentation is a good thing.

A useful expert KB should not ask only “what is the best tool?”
It should ask:
- best for recovering what?
- under which constraints?
- measured how?
- with what analyst payoff?

### What this topic is not
This topic is **not**:
- just a paper list
- just a catalog of public corpora
- just a benchmark leaderboard
- just decompiler benchmarking

It exists to interpret evaluation work in terms of expert reverse-engineering needs.

### Key distinctions
Several distinctions must remain explicit.

#### 1. Training corpora vs evaluation benchmarks
A large function-pair corpus is not the same thing as a benchmark that measures analyst-relevant performance.

#### 2. Tool-centric vs task-centric evaluation
Some benchmarks evaluate decompiler outputs or tool pipelines.
Others evaluate analyst-like tasks such as summarization, signature recovery, or classification.

#### 3. Intrinsic metrics vs downstream utility
A benchmark may measure local correctness while ignoring whether the output helps rehosting, fuzzing, clustering, navigation, or hypothesis testing.

#### 4. Real-world source material vs real-world analyst conditions
“Real-world” may mean:
- binaries from real projects
- execution-trace-backed validation
- analyst-like tasks
- preservation of hardware/protocol context
These are related, but not identical.

#### 5. Benchmark breadth vs benchmark faithfulness
A large benchmark is not automatically better if the labels are noisy, the ground truth is weak, or the task does not reflect analyst reality.

## 3. What this topic depends on
This topic depends on several other KB ideas.

- A clear notion of **objects of recovery**
  - code reconstruction
  - names/types/signatures
  - runtime behavior
  - protocol fields and states
  - hardware/environment context

- A clear notion of **domain constraints**
  - mobile
  - firmware
  - obfuscation-heavy targets
  - malware-adjacent corpora

- A clear notion of **workflow payoff**
  - whether a benchmark measures something that helps an analyst take the next step

Without those frames, benchmark listings remain descriptive but not decision-useful.

## 4. What this topic enables
A good evaluation map enables the KB to do the following:

- compare methods more honestly
- identify under-benchmarked parts of reverse engineering
- distinguish reproducible work from one-off demos
- separate analyst-relevant evaluation from convenience evaluation
- decide which benchmark families are worth watching long term
- avoid overgeneralizing from one benchmark family to the entire RE problem

In practical analyst terms, this topic helps answer:
- should I trust the claim behind this paper or tool?
- is this benchmark measuring what I actually care about?
- which family of evaluation is relevant to my target and workflow?

## 5. High-signal sources and findings

### A. Decompilation evaluation is becoming more workflow-aware

#### DecompileBench
Paper:
- *DecompileBench: A Comprehensive Benchmark for Evaluating Decompilers in Real-World Scenarios* (ACL Findings 2025)

High-signal findings:
- evaluates decompilers in a more realistic workflow setting
- includes **23,400 functions** from **130 real-world programs**
- includes **runtime-aware validation**
- includes **LLM-as-judge assessment** for human-centric code quality
- compares both traditional decompilers and LLM-based approaches

Why it matters:
- this is a strong signal that decompiler evaluation is moving beyond syntax-level or toy-function comparison
- it explicitly separates semantic correctness from readability/usefulness
- it fits the KB’s broader claim that analyst-facing value is not reducible to textual output alone

#### Decompile-Bench (million-scale binary-source pairs)
High-signal findings:
- distinct from DecompileBench above
- appears to be a large-scale binary-source pair dataset for decompilation research
- more likely to be useful as **training / large-scale evaluation substrate** than as a directly workflow-faithful analyst benchmark

Why it matters:
- this is a good example of why the KB must separate **corpus scale** from **benchmark meaning**

### B. Binary-understanding task benchmarks broaden the surface beyond decompilation

#### BinMetric
Paper:
- *BinMetric: A Comprehensive Binary Analysis Benchmark for Large Language Models* (2025 / IJCAI 2025)

High-signal findings:
- includes **1,000 questions** over **20 real open-source projects**
- covers **6 task categories**
- tasks include:
  - decompilation
  - summarization
  - assembly generation
  - call-site reconstruction
  - signature recovery
  - algorithm classification

Why it matters:
- this benchmark family is more analyst-task-oriented than pure decompiler evaluation
- it supports the KB’s view that reverse engineering should be benchmarked at multiple task layers, not only code reconstruction

### C. Symbol/type/signature recovery is emerging as its own benchmark family

#### R3-Bench
Paper:
- *R3-Bench: Reproducible Real-world Reverse Engineering Dataset for Symbol Recovery* (ASE 2025)

High-signal findings:
- explicitly focuses on **symbol recovery**
- introduces **AST-Align** style alignment for richer semantic ground truth
- spans **x86 and ARM** and **C/C++/Rust**
- claims **4× more struct fields** than prior methods
- claims **over 10 million functions** and a reproducible processing pipeline

Why it matters:
- this strongly supports treating symbol recovery as a separate benchmark family rather than a footnote under decompilation
- it helps formalize analyst-relevant metadata recovery as its own evaluation object

#### Type inference benchmarking in decompilers
Signals:
- 2025 benchmark work comparing multiple decompilers / type inference systems
- public benchmark repository and evaluation scripts surfaced

Why it matters:
- type inference quality is becoming benchmarkable in a direct way
- this reinforces the split between:
  - decompilation quality
  - type recovery quality
  - symbol/signature recovery quality

### D. Firmware RE benchmarks are becoming more context-centered

#### Firmware corpora and context-recovery work
Signals surfaced:
- `fkie-cad/linux-firmware-corpus`
- *Mens Sana In Corpore Sano: Sound Firmware Corpora for Vulnerability Research*
- *Recovering Peripheral Maps and Protocols to Expedite Firmware Reverse Engineering*

Why it matters:
- firmware RE cannot be evaluated only by code recovery quality
- environment realism, peripheral context, and protocol recovery increasingly matter
- this supports the KB idea that firmware reversing is a context-recovery problem, not just an architecture problem

### E. Protocol reverse engineering has its own benchmark pipeline

#### Protocol RE survey and benchmark signals
Signals surfaced:
- hierarchical protocol reverse engineering work
- LLM-oriented protocol analysis work
- industrial-control protocol RE survey material
- binary-analysis-based protocol inference work such as BinPRE
- state-machine inference work in mixed protocol environments

Why it matters:
- protocol RE is best understood as a staged pipeline:
  - trace/session collection
  - clustering / separation
  - field boundary inference
  - field semantics inference
  - state-machine recovery
  - downstream validation
- this differs substantially from decompilation benchmarks and deserves its own benchmark family

### F. Malware-oriented corpora are relevant but not always RE-native

#### Malware corpora signals
Signals surfaced:
- EMBER2024
- AU-PEMal-2025
- CIC-DGG-2025
- Binary-30K (2025/2026)

Why it matters:
- many malware datasets are detection-oriented rather than reverse-engineering-oriented
- they may still be useful for corpus diversity, metadata, CFG availability, or binary coverage
- the KB should treat them as **RE-adjacent** unless they genuinely support analyst-style reverse-engineering tasks

## 6. Emerging benchmark family structure
A stable benchmark taxonomy is starting to emerge.

### 1. Decompilation evaluation
Measures:
- semantic correctness
- readability
- recompilability
- execution-backed validity

### 2. Symbol / type / signature recovery
Measures:
- naming quality
- type/layout recovery
- prototype reconstruction
- semantic anchor quality for navigation

### 3. Task-level binary understanding
Measures:
- analyst-like tasks such as summarization, classification, call-site reconstruction, and signature reasoning

### 4. Obfuscation / resilience evaluation
Measures:
- performance under semantics-preserving transformations
- diffing and similarity robustness
- deobfuscation effectiveness
- unpacking/packer handling readiness

### 5. Firmware / environment / context recovery
Measures:
- peripheral-map realism
- MMIO or register inference
- protocol recovery from firmware behavior
- rehosting-enabling value

### 6. Protocol reverse engineering
Measures:
- field boundary inference
- field semantic inference
- protocol classification
- state-machine recovery
- downstream fuzzing/traffic-analysis payoff

### 7. RE-adjacent corpora
Measures less directly:
- detection, classification, or generalized binary coverage rather than explicit expert-analyst RE utility

## 7. Analyst workflow implications
This topic matters most when the analyst, researcher, or tool-builder is deciding:
- what claims to trust
- what tool or method class is worth investing in
- what counts as success for a given task
- whether a reported result likely transfers to practical reversing

It is especially important in these workflow moments:

### During orientation
It helps frame the problem correctly:
- am I dealing with a decompilation problem?
- a naming/type problem?
- a dynamic-behavior problem?
- a protocol/state problem?
- an environment reconstruction problem?

### During method selection
It helps avoid misapplying the wrong benchmark family to the wrong task.

### During result interpretation
It helps analysts avoid being misled by:
- attractive metrics on unrealistic tasks
- large datasets with weak ground truth
- benchmark wins that do not improve next-step decision quality

### During research planning
It helps identify gaps where benchmark coverage is still weak, especially for:
- mobile runtime workflows
- anti-instrumentation resilience
- environment reconstruction
- long-horizon analyst assistance

## 8. Evaluation dimensions
This page itself is about evaluation, so the most important dimensions here are:

### Correctness of the benchmark target
Does the benchmark actually measure the thing it claims to measure?

### Ground-truth quality
How strong, reproducible, and interpretable is the labeling or alignment process?

### Analyst relevance
Does the benchmark reflect something that matters to expert reverse engineering?

### Downstream utility
Does the benchmark connect to clustering, navigation, fuzzing, patch diffing, triage, or hypothesis testing?

### Robustness relevance
Does the benchmark reflect realistic transformations or constraints such as optimization, obfuscation, platform shifts, or access limitations?

### Reproducibility
Can others realistically rerun, inspect, and extend the benchmark?

### Transferability
Do results on this benchmark say something meaningful outside the benchmark itself?

Among these, the most important for this topic are:
- analyst relevance
- ground-truth quality
- downstream utility
- transferability

## 9. Cross-links to related topics

### Closely related pages
- `topics/symbol-type-and-signature-recovery.md`
  - because symbol/type/signature recovery now appears to be its own benchmark family
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
  - because robustness and resilience benchmarks are increasingly central
- `topics/firmware-and-protocol-context-recovery.md`
  - because firmware/protocol work forces context-heavy evaluation rather than code-only evaluation
- `topics/analyst-workflows-and-human-llm-teaming.md`
  - because analyst workflow studies help judge whether a benchmark is truly analyst-relevant

### Depends on framework pages
- `topics/expert-re-overall-framework.md`
- `topics/global-map-and-ontology.md`

### Often confused with
- general paper collection pages
- tool comparison pages
- corpus directories without evaluation interpretation

## 10. Open questions
- How should the KB distinguish **training corpora**, **benchmark corpora**, and **workflow-faithful evaluation sets** in a formally consistent way?
- Which benchmark families are strong enough to support longitudinal tracking over time?
- Which public benchmarks best reflect analyst usefulness rather than only ML-model convenience?
- How should mobile runtime instrumentation and anti-instrumentation resistance be benchmarked, if at all?
- Which firmware benchmarks preserve enough peripheral/protocol/environment context to matter for rehosting-oriented analysis?
- Which protocol RE benchmarks best connect intrinsic field/state accuracy with downstream analyst payoff?
- What benchmark families are still missing for long-horizon human–LLM reverse-engineering workflows?

## 11. Suggested next expansions
This topic may later split into several child pages:
- `topics/decompilation-evaluation.md`
- `topics/symbol-type-and-signature-benchmarks.md`
- `topics/protocol-re-benchmark-taxonomy.md`
- `topics/firmware-corpora-and-context-evaluation.md`
- `topics/re-adjacent-malware-corpora.md`

## 12. Source footprint / evidence quality note
Current evidence quality is mixed but coherent.

Strengths:
- multiple strong benchmark signals across decompilation, symbol recovery, firmware, and protocol RE
- enough material to justify a stable taxonomy direction
- good alignment with the broader KB framework

Limitations:
- some items are currently supported by abstracts, search metadata, or repository structure more than full-paper deep reading
- some benchmark families are clearer conceptually than they are operationally reproducible on modest local infrastructure

Overall assessment:
- the benchmark landscape is now well enough defined to support a mature topic page, even though several subfamilies still need deeper source passes

## 13. Topic summary
Benchmarks and datasets are the evaluation spine of the reverse-engineering expert KB.

They matter not because they produce leaderboards, but because they reveal what different parts of the field are actually trying to recover, which kinds of ground truth are available, which claims are analyst-relevant, and where current evaluation still fails to capture real reverse-engineering work.