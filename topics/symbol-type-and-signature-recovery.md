# Symbol, Type, and Signature Recovery in Reverse Engineering

## Why this topic matters
For expert reverse engineering, readable pseudocode is not enough. Analysts need trustworthy **semantic anchors**:
- variable and function names
- struct fields and layouts
- prototypes and calling conventions
- argument and return types
- enough confidence to know what to trust and what to verify manually

This makes symbol/type/signature recovery a distinct knowledge area rather than just a side effect of decompilation.

## High-signal items collected so far

### 1. R3-Bench reframes symbol recovery as a benchmark family of its own
Primary paper page:
- **R3-Bench: Reproducible Real-world Reverse Engineering Dataset for Symbol Recovery** (ASE 2025)

Key reported properties from the accessible abstract:
- introduces **AST-Align** for aligning variables and struct-access expressions between binaries and source
- spans **x86 and ARM** and **C/C++/Rust**
- claims **4× more struct fields** captured than prior methods
- dataset is described as **metadata-rich**, **extensible**, and backed by an explicit **reproducible processing pipeline**
- scale claim: **over 10 million functions** across multiple architectures
- baseline evaluation includes approaches from **n-gram models to LLMs**
- notable result: general LLMs initially perform poorly, but improve strongly with proper demonstrations

Why it matters:
- this is unusually direct evidence that symbol recovery should be tracked separately from generic decompilation
- it also sharpens a useful distinction between:
  - **semantic recovery** (names, types)
  - **syntactic/shape recovery** (struct-access shapes, layouts)
- for expert RE, both matter, but they are not identical evaluation objects

### 2. Type inference in decompilers is becoming explicitly benchmarked
Repository and paper lead:
- `sefcom/decompiler-types-benchmark`
- **Benchmarking Binary Type Inference Techniques in Decompilers** (SURE 2025)

Current high-confidence signals:
- the public repository explicitly contains binaries, extraction/evaluation scripts, extracted type data, and results
- search-layer metadata ties the evaluation to **Hex-Rays, Binary Ninja, Ghidra, angr, and Retypd**
- detailed metrics still need a better PDF extraction path, but the benchmark itself appears concretely reproducible

Why it matters:
- this reinforces that type recovery quality is becoming benchmarkable as its own object, not merely anecdotal tool preference
- it also suggests the KB should separate at least three closely related evaluation surfaces:
  - pseudocode readability/correctness
  - type inference quality
  - symbol/signature recovery quality

### 3. BTIGhidra highlights why type recovery changes analyst workflow quality
Operational source:
- Trail of Bits — **Binary type inference in Ghidra**

Key practical points:
- inter-procedural type inference can propagate user-provided type information conservatively
- better inferred types turn opaque pointer arithmetic into named field accesses and array indexing
- recursive/composite types become navigable rather than remaining as `void*` noise
- user guidance matters, but the propagation machinery can carry that guidance far beyond a local function

Why it matters:
- benchmarks can feel abstract; this source shows the lived analyst effect
- experts often tolerate imperfect pseudocode longer than they tolerate misleading or missing types, because type information changes navigation across the whole program

### 4. XTRIDE adds a deployment-oriented perspective
Paper:
- **Practical Type Inference: High-Throughput Recovery of Real-World Structures and Function Signatures** (2026)

Key extracted claims:
- emphasizes practicality, high throughput, and confidence-calibrated filtering
- reports **90.15%** overall type inference accuracy on DIRT
- claims **2300×–7070×** speedups over some heavier prior methods
- extends the same style of recovery toward **function signature recovery** with an embedded-firmware case study

Why it matters:
- type/signature recovery is not only an accuracy problem; it is also a deployment problem
- expert-facing automation often needs:
  - fast enough inference for iterative use
  - confidence estimates for selective application
  - graceful abstention instead of low-confidence pollution of the decompiler database

## Cross-cutting synthesis

### A. This topic is adjacent to decompilation, but not reducible to it
A useful separation is:
- **decompilation evaluation**: Is the output semantically correct and readable?
- **type recovery evaluation**: Are variable/field/prototype types trustworthy?
- **symbol recovery evaluation**: Are names and semantic anchors restored usefully?
- **signature recovery evaluation**: Are function boundaries, parameters, and returns reconstructed well enough to steer analysis?

An analyst may survive mediocre pseudocode if semantic anchors are strong. The inverse is often less true.

### B. Recovery quality has both local and global effects
Bad type recovery is not just a local formatting issue. It changes:
- call-site interpretation
- struct-field navigation
- cross-reference usefulness
- confidence in inferred control/data flow
- whether the analyst can build a stable mental model of the target

This is why inter-procedural and confidence-aware recovery matter so much.

### C. Demonstration and analyst context may matter disproportionately for LLMs
R3-Bench’s abstract-level result that LLMs improve dramatically with proper demonstration is especially interesting.

That suggests a research direction the KB should keep watching:
- symbol recovery may be unusually sensitive to prompting, exemplars, and local project context
- the right comparison may not be “LLM vs classic method” in isolation, but “LLM with structured demonstrations and recovered context vs classic method”

### D. Runtime and abstention are first-class evaluation concerns
XTRIDE makes a useful point for this KB: a recovery system that is highly accurate but too slow or too eager to guess may be worse for expert workflows than a faster system with calibrated abstention.

That points toward a more analyst-faithful evaluation matrix:
- accuracy
- coverage
- throughput
- confidence calibration
- downstream impact on decompiler usability

## Open questions
- Which public datasets best separate **struct layout recovery** from **semantic naming recovery**?
- How should a KB compare systems that recover anonymous-but-correct layouts versus semantically named but partially wrong types?
- Which benchmarks evaluate downstream analyst benefit rather than only intrinsic field/type accuracy?
- How much do demonstrations, retrieval context, or notebook memory improve LLM-based symbol recovery?
- Which subdomains (firmware, malware, mobile, protocol handlers) are especially sensitive to signature recovery quality?
- Can type/signature recovery be benchmarked using analyst-time-saved or navigation-efficiency measures rather than only intrinsic metrics?
