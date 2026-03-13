# Firmware and Protocol Context Recovery for Reverse Engineering

## Why this topic matters
Firmware reverse engineering often stalls long before classic decompilation questions are answered well.

The blocking issue is frequently **context recovery**:
- which peripherals actually exist and matter
- which MMIO/register ranges correspond to real hardware behavior
- which protocols the firmware is speaking through those peripherals
- which parts of the nominal hardware can be ignored because the target firmware never uses them
- which recovered context materially improves rehosting, emulation, or fuzzing

That makes firmware/protocol context recovery a distinct expert knowledge area, adjacent to but not reducible to decompilation or symbolic execution.

## High-signal items collected so far

### 1. ProtoReveal / ACSAC 2025: protocol identification from peripheral access chains
Source preview:
- Carter Yagemann, **Recovering Peripheral Maps and Protocols to Expedite Firmware Reverse Engineering** (ACSAC 2025 preview page)

Key reported properties from the preview abstract:
- frames the problem as **limited hardware knowledge** in off-the-shelf firmware analysis
- introduces **access chains** to identify which protocol is implemented for each set of in-use peripheral registers
- prototype: **ProtoReveal**
- evaluation scale:
  - **412 firmware samples**
  - **6 manufacturer websites**
  - **35 microcontrollers**
  - **82 protocols** (including SPI, UART, etc.)
  - **ARM and MIPS**
- reported protocol-identification result: **92% accuracy**
- reported downstream effect: integration with an existing framework lets analysts skip modeling peripherals/protocols that exist in hardware but are never used, reducing automatic rehosting time for fuzzing by **99%** without sacrificing effectiveness

Why it matters:
- this is unusually direct evidence that firmware RE should be evaluated partly by **rehosting utility** and **used-context recovery**, not only by code-understanding quality
- it suggests a benchmark family around:
  - peripheral/register discovery
  - protocol identification
  - used-vs-unused hardware discrimination
  - downstream rehosting/fuzzing acceleration

### 2. AutoMap / RAID 2022: hidden memory mappings for peripheral modeling
Operational artifact:
- `OSUSecLab/AutoMap`
- README points to **What You See is Not What You Get: Revealing Hidden Memory Mapping for Peripheral Modeling** (RAID 2022)

Key accessible signal:
- AutoMap is an emulator plugin for MCU firmware
- goal is to discover **hidden memory mappings between peripheral registers**

Why it matters:
- useful precursor to newer protocol/peripheral recovery work
- highlights that firmware context recovery starts below the protocol layer: analysts may first need to reconstruct the correct memory/peripheral model before higher-level protocol recognition becomes possible

### 3. BinPRE / CCS 2024: field inference with downstream fuzzing utility
Paper:
- **BinPRE: Enhancing Field Inference in Binary Analysis Based Protocol Reverse Engineering**

Key reported properties from the abstract:
- focuses on **field inference** for protocol reverse engineering without source code
- explicitly tackles two weaknesses of prior binary-analysis PRE methods:
  - format inference fragility across protocol implementations
  - inadequate/inaccurate semantic inference rules
- contributions include:
  - instruction-based semantic similarity for format extraction
  - atomic semantic detectors
  - cluster-and-refine semantic inference
- compared against **Polyglot, AutoFormat, Tupni, BinaryInferno, DynPRE**
- evaluation on **eight widely-used protocols**
- reported results:
  - **0.73 perfection** on format extraction
  - semantic-inference F1: **0.74** for types and **0.81** for functions
  - downstream fuzzing improvement: **5–29% higher branch coverage** than the best prior PRE tool
  - enabled discovery of **one new zero-day vulnerability**

Why it matters:
- strong signal that protocol RE benchmarks should include both **intrinsic inference quality** and **downstream analyst/security utility**
- also suggests that field inference should not be treated as a monolith; type/function semantics need separate attention from boundary extraction

### 4. Automatic State Machine Inference for Binary Protocol Reverse Engineering (2024)
Paper:
- **Automatic State Machine Inference for Binary Protocol Reverse Engineering**

Key reported properties from the abstract:
- argues that many PRE methods over-focus on field identification and neglect **protocol state machine (PSM)** analysis
- targets **mixed protocol environments**
- pipeline includes:
  - protocol-format clustering
  - session clustering using Needleman-Wunsch + K-Medoids
  - probabilistic PSM inference
- claims more precise protocol classification while inferring PSMs

Why it matters:
- reinforces that protocol RE is not finished once fields are inferred
- state/transition recovery is a separate stage with distinct analyst value, especially for abnormal behavior analysis and fuzzing guidance

### 5. BinaryInferno: semantic-driven field inference with low false positives
Paper page:
- **BinaryInferno: A Semantic-Driven Approach to Field Inference for Binary Message Formats**

Key reported properties from the NDSS page:
- fully automatic field/message-format inference from sets of messages sharing a format
- uses targeted semantic detectors for floats, timestamps, integer length fields, entropy boundaries, and serialization idioms
- evaluated on **10 binary protocols**
- reported top-level protocol metrics:
  - precision **0.69**
  - recall **0.73**
  - false positive rate **0.04**
- compared against AWRE, FieldHunter, Nemesys, NetPlier, and Netzob
- explicitly emphasizes semantically meaningful descriptions and fewer false positives as especially valuable to users

Why it matters:
- good complement to BinPRE because it highlights that lower false positives and semantically meaningful partial descriptions may fit expert workflows better than noisy broad extraction

## Cross-cutting synthesis

### A. Firmware RE and protocol RE intersect, but should not be collapsed
A useful distinction is:
- **firmware context recovery**
  - peripheral maps
  - hidden memory mappings
  - MMIO/register usage
  - protocol identification over hardware-facing access patterns
  - rehosting/emulation payoff
- **protocol reverse engineering**
  - message clustering
  - field boundary extraction
  - semantic field-function/type inference
  - state-machine recovery
  - downstream fuzzing/traffic-analysis payoff

They inform each other, but they are not the same benchmark family.

### B. Environment reconstruction is a first-class evaluation object
Recent sources suggest expert reversing is often bottlenecked by whether the analyst can reconstruct the right environment assumptions.

That means useful firmware RE evaluation may need to ask:
- were the right peripherals identified?
- were unused peripherals excluded?
- was the right protocol associated with observed access patterns?
- did this make emulation/rehosting materially faster or more faithful?

### C. Downstream utility matters more than isolated intrinsic scores
BinPRE and ProtoReveal are especially helpful because both connect recovery quality to practical outcomes:
- improved fuzzing coverage / bug discovery
- reduced rehosting time without losing effectiveness

This is closer to expert analyst reality than isolated accuracy numbers alone.

### D. False positives are a workflow tax
BinaryInferno’s emphasis on precision and low false-positive rates is worth preserving.

In protocol and firmware context recovery, a wrong guessed field or a wrongly modeled peripheral can waste substantial analyst time downstream. Expert-oriented benchmarks should therefore treat **false-positive burden** as a central metric, not a side note.

## Open questions
- What benchmark families exist specifically for **MMIO/register recovery** versus higher-level protocol identification?
- Which firmware corpora preserve enough peripheral/protocol metadata to support reproducible context-recovery evaluation?
- How should the KB represent the boundary between **hardware-model inference** and **protocol inference**?
- Which public datasets compare protocol RE tools on both field inference and state-machine recovery?
- What are the best downstream metrics for expert workflows: time-to-rehost, fuzzing coverage, bug yield, analyst correction burden, or emulation fidelity?
- Which sources cover mobile/IoT/industrial protocols in a way that transfers into practical firmware reversing rather than generic network analysis?
