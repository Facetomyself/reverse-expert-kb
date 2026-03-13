# Source notes — obfuscation / deobfuscation benchmark sweep

Generated: 2026-03-14 04:18 Asia/Shanghai

## Primary sources captured this run

### quarkslab/diffing_obfuscation_dataset
- URL: https://github.com/quarkslab/diffing_obfuscation_dataset
- Key extracted claims:
  - realistic amalgamated C projects: zlib, lz4, minilua, sqlite, freetype
  - OLLVM + Tigress
  - multiple obfuscation types/passes including CFF, opaque, encodearith, virtualize, copy, merge, split, mix1, mix2
  - >6,000 binaries and >8M functions
  - stripped binaries with JSON ground truth plus BinExport/Quokka exports
  - full dataset download about 92 GB
- Usefulness:
  - strong anchor for realistic obfuscation-resilience research
  - important caveat about compiler optimizations weakening/erasing applied obfuscation

### quarkslab/obfuscation_benchmark_code_artifacts
- URL: https://github.com/quarkslab/obfuscation_benchmark_code_artifacts
- Repository points to:
  - Identifying Obfuscated Code through Graph-Based Semantic Analysis of Binary Code (ComplexNetworks 2024)
  - Experimental Study of Binary Diffing Resilience on Obfuscated Programs (DIMVA 2025)
- Usefulness:
  - useful breadcrumb that this area spans both detection and diffing-resilience evaluation

### REFuSE-Bench
- URL: https://arxiv.org/abs/2410.22677
- Key extracted claims:
  - benchmark for binary function similarity detection
  - addresses duplication/labeling issues
  - includes real malware and Windows data
  - simple raw-byte baseline performs surprisingly well
- Usefulness:
  - good contrast to over-engineered preprocessing-heavy similarity pipelines

### BinSimDB
- URL: https://arxiv.org/abs/2410.10163
- Key extracted claims:
  - fine-grained binary code similarity benchmark
  - includes smaller code snippets such as basic blocks
  - proposes BMerge / BPair to align across optimization/platform differences
- Usefulness:
  - suggests value of sub-function-level matching in obfuscation-heavy settings

### MetamorphASM / MAD
- URL: https://arxiv.org/abs/2412.16135
- Key extracted claims:
  - 328,200 obfuscated assembly samples
  - dead code, register substitution, control-flow change
  - evaluates LLMs generating/analyzing obfuscated assembly
- Usefulness:
  - modern assembly-obfuscation corpus; intersects with LLM capability and threat-model questions

### JsDeObsBench
- URL: https://arxiv.org/abs/2506.20170
- Key extracted claims:
  - benchmark for LLM-based JavaScript deobfuscation
  - spans simple renaming through stronger structural transformations
  - evaluates syntax correctness and execution reliability in addition to simplification
  - includes JS malware cases
- Usefulness:
  - broadens deobfuscation benchmarking beyond native binaries

### asmFooler / BCSD robustness
- URL: https://arxiv.org/abs/2602.12681
- Key extracted claims:
  - 9,565 variants from 620 baseline samples
  - eight semantics-preserving transformations
  - evaluates six BCSD models
- Usefulness:
  - strong signal that robustness under transformation deserves separate tracking from nominal benchmark score

### DEBRA
- URLs:
  - https://dl.acm.org/doi/10.1145/3733822.3764674
  - https://sure-workshop.org/accepted-papers/2025/sure25-7.pdf
- Extractability this run:
  - metadata/abstract-level only; direct PDF extraction via `web_fetch` was poor
- Usefulness:
  - still important as a lead for real-world deobfuscation evaluation

## Practical retention decision
- Saved only this compact source-note file.
- Did not mirror PDFs or clone large datasets.
- Rationale: enough structured signal for future synthesis; avoid unnecessary disk growth.