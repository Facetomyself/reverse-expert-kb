# Benchmarks and Datasets for Reverse Engineering Research

## Why this topic matters
A reverse-engineering expert knowledge base should track not just tools and workflows, but also the public corpora and benchmarks that shape evaluation. Recent work is making RE knowledge more measurable across decompilation, symbol recovery, binary understanding, malware analysis, firmware, and protocol reverse engineering.

## High-signal items collected so far

### 1. DecompileBench (evaluation framework for decompilers in realistic workflows)
- Paper: *DecompileBench: A Comprehensive Benchmark for Evaluating Decompilers in Real-World Scenarios* (ACL Findings 2025).
- Core contribution:
  - 23,400 functions from 130 real-world programs.
  - Runtime-aware validation.
  - LLM-as-judge assessment for human-centric code quality.
  - Comparison across six traditional decompilers and six LLM-based approaches.
- Important framing for this KB:
  - It treats decompiler evaluation as a workflow problem, not just a syntax problem.
  - It explicitly separates semantic correctness from analyst readability/usefulness.
- Emerging implication:
  - "Best decompiler" is task-dependent. Traditional tools still lead on correctness, but LLM-assisted outputs may score better on understandability.

### 2. Decompile-Bench (million-scale binary-source pairs)
- Distinct from DecompileBench above.
- Search results indicate a 2025 dataset effort focused on million-scale binary-source function pairs for real-world binary decompilation.
- This appears more training-data oriented than workflow-evaluation oriented.
- Research value for KB organization:
  - separate "evaluation benchmarks" from "training corpora"
  - track lineage between function-pair datasets and downstream evaluation papers

### 3. BinMetric (binary-analysis benchmark for LLMs)
- Paper: *BinMetric: A Comprehensive Binary Analysis Benchmark for Large Language Models* (2025 / IJCAI 2025).
- Reported structure:
  - 1,000 questions
  - 20 real open-source projects
  - 6 task categories
  - tasks include decompilation, summarization, assembly generation, call-site reconstruction, signature recovery, and algorithm classification
- Why it matters:
  - This is broader than decompilation-only evaluation.
  - It captures a more analyst-like task surface for binary understanding.
- Useful synthesis:
  - DecompileBench measures decompiler outputs.
  - BinMetric measures LLM capability on binary-analysis tasks.
  - Together they suggest a future taxonomy of RE evaluation: tool-centric, analyst-centric, and task-centric.

### 4. R3-Bench (symbol recovery)
- Search results surfaced: *R3-Bench: Reproducible Real-world Reverse Engineering Dataset for Symbol Recovery* (ASE 2025 listing / later mirrors).
- Even without full paper extraction yet, this looks important because symbol recovery is central to expert workflow quality and downstream readability.
- Candidate subtopic:
  - function naming / variable naming / type recovery / signature recovery as a dedicated track, not a side note under decompilation.

### 5. Type inference benchmarking in decompilers
- Search results surfaced a 2025 ACM paper on benchmarking binary type inference across Hex-Rays, Binary Ninja, Ghidra, angr, and Retypd.
- Why it matters:
  - Type recovery deserves its own evaluation layer.
  - Experts often care less about pretty pseudocode in the abstract and more about whether types/structures/prototypes are trustworthy enough to guide the next move.

### 6. Firmware corpora and firmware-oriented RE evaluation
- Search results surfaced:
  - `fkie-cad/linux-firmware-corpus`
  - *Mens Sana In Corpore Sano: Sound Firmware Corpora for Vulnerability Research*
  - *Recovering Peripheral Maps and Protocols to Expedite Firmware Reverse Engineering*
- Synthesis:
  - firmware RE benchmarks are not only about lifting/disassembly quality
  - they also hinge on environment reconstruction, peripheral understanding, and protocol recovery
- This suggests the KB should treat firmware RE as more than “embedded binaries + Ghidra” — it is an ecosystem problem involving corpora quality, emulation assumptions, and hardware-interface inference.

### 7. Malware-oriented corpora relevant to RE
- Search results surfaced:
  - EMBER2024
  - AU-PEMal-2025
  - CIC-DGG-2025
  - Binary-30K (2025/2026)
- Caution:
  - many malware datasets are primarily ML/detection datasets, not expert-analyst RE datasets
- Still useful because:
  - they can provide binary corpora, CFGs, metadata, and classification labels
  - they help identify where RE-oriented datasets differ from classifier-oriented datasets

### 8. Protocol reverse engineering benchmarks/surveys
- Search surfaced:
  - *An improved hierarchical protocol reverse engineering approach* (2025)
  - *ChatPRE* (LLM-oriented protocol analysis)
  - industrial control protocol RE survey (2025)
- Emerging structure:
  - protocol RE evaluation has its own pipeline: trace collection, clustering, field segmentation, semantic inference, state-machine recovery, and reverse application.
  - This differs substantially from binary decompilation benchmarks and should likely become its own topic family.

## Cross-cutting synthesis

### A. RE evaluation is fragmenting into specialized tracks
A useful knowledge-base structure is emerging:
- decompilation correctness and readability
- type/signature/symbol recovery
- binary-understanding tasks for LLMs
- firmware corpus realism and peripheral/protocol recovery
- malware corpora used for RE-adjacent research
- protocol message/state-machine reconstruction

### B. "Real-world" now has multiple meanings
Recent work uses "real-world" in at least four different senses:
- binaries sourced from real projects
- functions covered by actual execution/fuzzing traces
- tasks aligned with analyst decisions
- corpora that preserve deployment context (firmware/peripherals/protocol traces)

### C. Human-centric evaluation is becoming first-class
One especially important trend is the move away from purely syntactic metrics. DecompileBench explicitly introduces runtime-aware and human-centric evaluation. That is a strong signal for this KB: expert-level RE knowledge should privilege semantic usefulness, analyst workflow fit, and recoverability of intent.

## Open questions
- How should this KB distinguish training corpora from evaluation benchmarks?
- Which benchmarks are actually reproducible on a modest research machine versus only on specialized infrastructure?
- Which datasets are legally and operationally reusable for long-term personal study?
- What are the best benchmark families per subdomain: desktop binaries, malware, firmware, mobile, protocol traces?
