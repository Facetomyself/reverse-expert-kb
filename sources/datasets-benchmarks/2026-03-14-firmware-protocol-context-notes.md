# Source notes — firmware/protocol context recovery

Date: 2026-03-14
Focus: firmware reverse engineering with peripheral-map/protocol recovery, plus protocol reverse engineering benchmarks that look analyst-relevant.

## Recovering Peripheral Maps and Protocols to Expedite Firmware Reverse Engineering (ACSAC 2025 preview)
Source:
- https://carteryagemann.com/protoreveal-to-appear-in-acsac-2025.html

High-signal extracted points:
- Frames firmware RE bottleneck as **limited hardware knowledge** rather than only poor code recovery.
- Key contribution: defining and using **access chains** inside firmware to identify which protocol is implemented for each set of in-use peripheral registers.
- Prototype: **ProtoReveal**.
- Evaluation scale (from preview abstract):
  - **412 firmware samples**
  - **6 manufacturer websites**
  - **35 microcontrollers**
  - **82 protocols** (e.g. SPI, UART)
  - **ARM and MIPS**
- Reported result: **92% protocol-identification accuracy**.
- Reported downstream impact: when integrated with an existing framework, can skip modeling peripherals/protocols that are present in hardware but unused by the firmware, reducing automatic rehosting time for fuzzing by **99%** without sacrificing effectiveness.

Why it matters:
- Strong evidence that firmware RE evaluation should include **environment/context recovery** and **rehosting utility**, not only decompiler quality.
- Suggests a useful benchmark decomposition:
  - MMIO/peripheral-register discovery
  - protocol identification
  - used-vs-unused hardware discrimination
  - downstream rehosting/fuzzing speed/effectiveness

## AutoMap / RAID 2022
Sources:
- https://github.com/OSUSecLab/AutoMap
- README points to: "What You See is Not What You Get: Revealing Hidden Memory Mapping for Peripheral Modeling" (RAID 2022)

High-signal extracted points from README:
- AutoMap is an **emulator plugin** for MCU-based firmware.
- Goal: discover **hidden memory mappings between peripheral registers**.
- Supports multiple MCU examples in the artifact/readme (NRF52832, STM32F103, STM32F429).

Why it matters:
- Useful antecedent to ProtoReveal-style work.
- Indicates firmware RE context recovery includes not only named protocol detection, but more basic **memory-mapping / peripheral-model reconstruction**.

## BinPRE (CCS 2024)
Source:
- https://arxiv.org/abs/2409.01994

High-signal extracted points:
- PRE = protocol reverse engineering without source code.
- Focuses on **field inference** in binary-analysis-based PRE.
- Two challenges called out:
  1. format inference is fragile across different implementations
  2. semantic inference is limited by inadequate/inaccurate inference rules
- Proposed components:
  - instruction-based semantic similarity analysis for format extraction
  - library of atomic semantic detectors
  - cluster-and-refine paradigm for semantic inference
- Compared against **Polyglot, AutoFormat, Tupni, BinaryInferno, DynPRE**.
- Evaluation on **eight widely-used protocols**.
- Reported results:
  - **0.73 perfection** on format extraction
  - semantic inference F1: **0.74** for types, **0.81** for functions
  - downstream fuzzing: **5–29% higher branch coverage** than best prior PRE tool
  - helped discover **one new zero-day vulnerability**

Why it matters:
- Strong anchor for protocol-RE evaluation that includes both intrinsic accuracy and downstream security utility.
- Suggests field inference should be split into:
  - format extraction
  - semantic type/function inference
  - downstream utility (e.g. fuzzing coverage, vuln discovery)

## Automatic State Machine Inference for Binary Protocol Reverse Engineering (2024)
Source:
- https://arxiv.org/abs/2412.02540

High-signal extracted points:
- Explicitly argues that many PRE methods focus on field identification within a single protocol and neglect **protocol state machine (PSM)** analysis.
- Also targets **mixed protocol environments**.
- Pipeline includes:
  - protocol format clustering via fuzzy-membership auto-converging DBSCAN
  - session clustering using Needleman-Wunsch + K-Medoids
  - probabilistic PSM inference
- Claimed benefit: infer PSMs while enabling more precise classification of protocols.

Why it matters:
- Strengthens the case that protocol RE should not be modeled as only message-format extraction.
- Suggests a separate evaluation stage for **state/transition recovery** after field inference.

## BinaryInferno (NDSS)
Source:
- https://www.ndss-symposium.org/ndss-paper/binaryinferno-a-semantic-driven-approach-to-field-inference-for-binary-message-formats/

High-signal extracted points:
- Fully automatic tool for reverse engineering binary message formats from sets of messages with the same format.
- Uses targeted semantic detectors (floats, timestamps, integer length fields, entropy-based field-boundary detection, serialization idioms).
- Evaluated on **10 binary protocols**.
- Reported metrics for top-level protocols:
  - precision **0.69**
  - recall **0.73**
  - false positive rate **0.04**
- Compared against AWRE, FieldHunter, Nemesys, NetPlier, and Netzob.
- Notable framing: lower false positive rates and semantically meaningful descriptions are emphasized as especially valuable to users.

Why it matters:
- Good complementary anchor to BinPRE.
- Reinforces that expert users may prefer lower false positives and semantically meaningful partial descriptions over noisier broad coverage.

## Structural synthesis from this source set
1. Firmware RE and protocol RE intersect around **context recovery**, but should not be collapsed.
2. Firmware RE context recovery seems to center on:
   - peripheral maps / hidden memory mappings
   - MMIO/register usage
   - protocol identification on top of peripheral access patterns
   - rehosting utility
3. Protocol RE seems to decompose into at least:
   - field boundary / format extraction
   - semantic field-function/type inference
   - state-machine inference
   - downstream utility such as fuzzing effectiveness
4. A promising expert-KB distinction is:
   - **artifact understanding**: what does this code/message mean?
   - **environment reconstruction**: what hardware/protocol context must exist for analysis to progress?
