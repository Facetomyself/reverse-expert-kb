# Obfuscation, Deobfuscation, and Packed-Binary Evaluation

## Why this topic matters
A reverse-engineering expert KB needs a dedicated treatment of obfuscation-heavy targets rather than folding them into generic decompilation or malware-analysis buckets.

Obfuscation changes what analysts must trust:
- whether similarity search still works after semantics-preserving transformations
- whether symbols, types, and control flow remain recoverable enough for navigation
- whether unpacking/deobfuscation methods are evaluated on realistic binaries rather than toy snippets
- whether a benchmark measures analyst-relevant resilience or only nominal task success

## High-signal items collected so far

### 1. Quarkslab diffing_obfuscation_dataset
GitHub repository:
- `quarkslab/diffing_obfuscation_dataset`

Key reported properties from the repository README:
- realistic C projects rather than toy algorithms: `zlib`, `lz4`, `minilua`, `sqlite`, `freetype`
- two obfuscators: **OLLVM** and **Tigress**
- multiple obfuscation families:
  - data obfuscation (`encodearith`, `encodeliteral`-style equivalents)
  - intra-procedural (`CFF`, `opaque`, `virtualize`)
  - inter-procedural (`copy`, `merge`, `split`)
  - combined schemas (`mix1`, `mix2`)
- obfuscation levels from 0% to 100% in 10% steps
- x64 binaries at multiple optimization levels
- stripped binaries with accompanying JSON ground truth for function names / addresses
- exported artifacts such as BinExport and Quokka
- reported scale: **more than 6,000 binaries** and **more than 8M functions**
- full download size is large: about **92 GB**

Why it matters:
- this is closer to a real obfuscation-resilience corpus than many older toy datasets
- the explicit combination of projects, obfuscators, passes, seeds, optimization levels, and obfuscation ratios makes it useful for studying robustness rather than one-off wins
- it also exposes a practical benchmark-design problem: compiler optimizations can partly erase applied obfuscation, so labels like “obfuscated” are not always semantically clean from an analyst’s point of view

### 2. Artifact repository linking obfuscation detection and diffing work
GitHub repository:
- `quarkslab/obfuscation_benchmark_code_artifacts`

Repository description points to two papers:
- **Identifying Obfuscated Code through Graph-Based Semantic Analysis of Binary Code** (ComplexNetworks 2024)
- **Experimental Study of Binary Diffing Resilience on Obfuscated Programs** (DIMVA 2025)

This is useful because it suggests the obfuscation benchmark story is splitting into at least two related but distinct evaluation objects:
- **obfuscation detection / characterization**
- **binary diffing resilience under obfuscation**

### 3. DEBRA: real-world deobfuscation benchmark
Paper lead:
- **DEBRA: A Real-World Benchmark For Evaluating Deobfuscation Methods** (SURE 2025 / ACM DOI listing)

Accessible metadata strongly suggests:
- emphasis on **real-world open-source programs** rather than tiny hand-crafted examples
- metric-driven selection of sensitive functions / targets
- use of state-of-the-art obfuscators
- goal is to reveal limitations in existing deobfuscation tools that toy datasets fail to expose

Why it matters:
- this looks like one of the clearest signs that deobfuscation is becoming its own benchmark family rather than a side experiment inside malware analysis or symbolic execution papers
- it may become a key bridge between classical obfuscation literature and analyst-oriented evaluation

### 4. REFuSE-Bench: function similarity under realistic binary conditions
Paper:
- **Is Function Similarity Over-Engineered? Building a Benchmark** (NeurIPS Datasets & Benchmarks 2024)

From the abstract:
- introduces **REFuSE-Bench** for binary function similarity detection
- explicitly tries to reflect real-world use cases better
- addresses data duplication and labeling quality
- includes experiments with **real malware**
- includes Windows data, not only the Linux-centric defaults common in many prior works
- notable result: a simple raw-byte baseline can achieve state-of-the-art performance in several settings

Why it matters for this topic:
- function similarity is one of the analyst’s key weapons against stripped/obfuscated binaries
- obfuscation-resilience should be treated not only as “can we decompile it” but also as “can we still match, cluster, diff, and triage it reliably?”

### 5. BinSimDB: fine-grained binary code similarity benchmark
Paper:
- **Benchmark Dataset Construction for Fine-Grained Binary Code Similarity Analysis** (SecureComm 2024)

From the abstract:
- introduces **BinSimDB**
- focuses on fine-grained equivalence pairs, including smaller snippets such as **basic blocks**
- proposes alignment/pairing algorithms to bridge differences caused by optimization levels or platforms

Why it matters:
- fine-grained matching is relevant when obfuscation breaks whole-function comparability but leaves reusable local structure
- this may become important for the KB’s eventual treatment of partial deobfuscation and resilient analyst navigation

### 6. MetamorphASM / MAD: assembly obfuscation dataset for LLM evaluation
Paper:
- **Can LLMs Obfuscate Code? A Systematic Analysis of Large Language Models into Assembly Code Obfuscation** (AAAI 2025)

From the abstract:
- introduces **MetamorphASM benchmark** and **MAD dataset**
- dataset scale: **328,200 obfuscated assembly code samples**
- three obfuscation techniques explicitly studied:
  - dead code
  - register substitution
  - control-flow change
- evaluates whether LLMs can generate and analyze obfuscated assembly
- uses both information-theoretic metrics and manual human review

Why it matters:
- this is not a direct deobfuscation benchmark, but it provides a modern assembly-level obfuscation corpus that could be useful for studying model robustness and remediation strategies
- it also shows that obfuscation research is now intersecting directly with LLM capability evaluation

### 7. JsDeObsBench: deobfuscation benchmark for obfuscated JavaScript
Paper:
- **Measuring and Benchmarking LLMs for JavaScript Deobfuscation** (CCS 2025)

From the abstract:
- introduces **JsDeObsBench**
- targets a range of obfuscation techniques from variable renaming to more structural transformations
- evaluates both code simplification quality and practical reliability issues like syntax correctness and execution reliability
- includes JS malware deobfuscation scenarios

Why it matters:
- it broadens this topic beyond native binaries
- expert reverse-engineering knowledge should track when the same conceptual problems reappear across ecosystems: readability recovery, semantics preservation, and trustworthiness of restored behavior

### 8. Robustness of BCSD models against semantics-preserving transformations
Paper:
- **Fool Me If You Can: On the Robustness of Binary Code Similarity Detection Models against Semantics-preserving Transformations** (FSE 2026)

From the abstract:
- introduces **asmFooler** for robustness evaluation
- dataset: **9,565 binary variants from 620 baseline samples**
- applies **eight semantics-preserving transformations**
- evaluates **six representative BCSD models**
- key result: small, carefully chosen transformations can strongly disrupt model decisions

Why it matters:
- this is a direct reminder that benchmark accuracy on a static dataset is not the same as resilience under analyst-relevant adversarial transformations
- the KB should preserve a distinction between:
  - nominal function-similarity accuracy
  - robustness to semantics-preserving obfuscation / perturbation

### 9. Packed-binary and packer-oriented resources
High-signal practical leads surfaced this run:
- `packing-box/docker-packing-box`
- `packing-box/awesome-executable-packing`
- `joyce8/MalDICT`

These are not all benchmark papers, but they matter because packers create a separate evaluation layer:
- before decompilation or semantic recovery, the analyst may need to detect, classify, unpack, or dump memory correctly
- packer-aware datasets can therefore be useful even when they are not framed as “reverse engineering benchmarks” in the academic sense

## Cross-cutting synthesis

### A. Obfuscation-heavy RE needs its own evaluation family
This topic is not just an edge case of decompilation. It spans at least five distinct evaluation objects:
- obfuscation detection / characterization
- deobfuscation effectiveness
- function similarity resilience
- diffing resilience
- unpacking / packer handling

### B. Robustness matters more than one-shot score
A recurring lesson from these sources is that a method may look strong on a static benchmark yet fail once semantics-preserving transformations are introduced.

That makes “robust under transformation” a more analyst-faithful criterion than simple average accuracy.

### C. Ground truth is tricky in obfuscation datasets
The Quarkslab dataset highlights an important caveat: compiler optimization can partially erase or distort applied obfuscations. So labels such as “obfuscated function” may not always correspond to the semantic analyst experience.

This means the KB should track not only dataset scale and diversity, but also:
- how labels are generated
- whether post-compilation validation is done
- whether the benchmark measures applied transformations or observable transformed behavior

### D. Obfuscation research is connecting with LLM evaluation
MetamorphASM and JsDeObsBench indicate a broader trend: LLMs are now part of both sides of the equation.
- they can be evaluated as deobfuscators
- they can also potentially generate obfuscation variants

That creates a new expert-knowledge question: how should reverse engineers evaluate assistance tools when the threat side may also be model-assisted?

## Open questions
- What are the best public benchmarks specifically for **unpacking** rather than general malware classification?
- Which datasets validate that obfuscation survived compilation rather than merely being requested at build time?
- How should deobfuscation quality be measured: semantics recovery, readability, recompilability, execution equivalence, or analyst time saved?
- Which function-similarity benchmarks explicitly test resilience to Tigress / OLLVM / virtualization-style transformations?
- How portable are lessons from JS deobfuscation to native binary deobfuscation?
- Which anti-tamper / anti-cheat sources provide analyst-relevant evaluation rather than vendor marketing or purely defensive guidance?
