# Source notes — symbol / type / signature recovery sweep

Generated: 2026-03-14 05:00 Asia/Shanghai

## Primary sources captured this run

### R3-Bench / AST-Align
- URL: https://conf.researchr.org/details/ase-2025/ase-2025-papers/7/R3-Bench-Reproducible-Real-world-Reverse-Engineering-Dataset-for-Symbol-Recovery
- Key extracted claims from the abstract:
  - symbol recovery is framed around restoring variable and data-structure information in binaries
  - introduces **AST-Align** for aligning variables and struct-access expressions between binaries and source
  - spans **x86 and ARM** and **C/C++/Rust**
  - claims **4× more struct fields** captured than prior methods
  - introduces **R3-Bench** as a metadata-rich, extensible dataset with explicit inclusion criteria and reproducible processing pipeline
  - scale claim: **over 10 million functions** across multiple architectures
  - baseline evaluation spans **n-gram models to LLMs**
  - notable result: general LLMs perform poorly at first but improve sharply with proper demonstrations
- Usefulness:
  - strongest current anchor for treating symbol recovery as a dedicated benchmark family rather than a sub-bullet under decompilation

### Benchmarking Binary Type Inference Techniques in Decompilers
- URLs:
  - https://github.com/sefcom/decompiler-types-benchmark
  - https://raw.githubusercontent.com/sefcom/decompiler-types-benchmark/master/README.md
  - https://sure-workshop.org/accepted-papers/2025/sure25-8.pdf
- Key extracted claims / confidence notes:
  - repository explicitly states it contains binaries, extraction/evaluation scripts, extracted type data, and results for the SURE'25 paper
  - search-layer metadata links the paper to evaluation across **Hex-Rays, Binary Ninja, Ghidra, angr, and Retypd**
  - direct PDF extraction via web_fetch was poor/raw, so detailed metric claims remain provisional until a better extraction path is used
- Usefulness:
  - concrete evidence that decompiler type inference is being benchmarked directly as its own object of study
  - repository availability suggests unusually good reproducibility prospects compared with paper-only claims

### BTIGhidra / Trail of Bits practical framing
- URL: https://blog.trailofbits.com/2024/02/07/binary-type-inference-in-ghidra/
- Key extracted claims:
  - BTIGhidra performs inter-procedural type inference
  - consumes user-provided type information and propagates it conservatively
  - improves decompilation readability by turning pointer arithmetic into field accesses / array indexing and reducing `void*` clutter
  - synthesizes composite types and operates on stripped binaries
  - uses subtyping constraints, SCC summaries, and data-flow analyses via `cwe_checker`
- Usefulness:
  - bridges benchmark abstraction to analyst pain: type inference quality directly changes navigation and trust in decompiled output

### XTRIDE
- URL: https://arxiv.org/html/2603.08225v1
- Key extracted claims from the abstract/introduction:
  - focuses on practical, high-throughput type recovery grounded in real-world types
  - reports **90.15%** overall type inference accuracy on DIRT
  - claims to be **2300× to 7070× faster** than some prior state-of-the-art struct-recovery approaches
  - adds confidence scores for threshold-based filtering in automated pipelines
  - extends n-gram matching to **function signature recovery** with an embedded-firmware case study
- Usefulness:
  - strong signal that this research seam is splitting further into:
    - struct/type recovery accuracy
    - deployment/runtime practicality
    - confidence-calibrated abstention
    - function-signature recovery for analyst triage

## Practical retention decision
- Saved only this compact source-note file.
- Did not mirror PDFs or repositories.
- Rationale: enough structured signal for KB synthesis; avoid unnecessary disk use.
