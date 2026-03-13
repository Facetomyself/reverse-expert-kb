# Reverse Expert Knowledge Base Index

## Purpose
Build a long-running, research-stage knowledge base about how to think like a reverse-engineering expert.

## Active themes
- reverse engineering methodology
- expert workflows and heuristics
- tooling ecosystems
- knowledge organization patterns
- specialized domains (malware/mobile/firmware/protocol/anti-tamper)
- benchmarks, datasets, and corpora for evaluating RE knowledge and tooling

## Emerging structural axes
The KB now seems likely to need at least three orthogonal organization schemes:

### 1. By domain
- desktop / native binaries
- malware analysis overlaps
- mobile reversing
- firmware / embedded
- protocol reverse engineering
- anti-tamper / anti-cheat / obfuscation-heavy targets

### 2. By evaluation object
- decompilation output quality
- symbol recovery
- type inference / struct-layout recovery
- function signature / prototype recovery
- task-level binary understanding
- firmware corpus realism and environment reconstruction
- protocol message/state reconstruction
- malware corpora used for RE-adjacent analysis

This second axis is important because recent papers increasingly evaluate not just tools, but specific analyst-relevant outputs and tasks. Recent runs also suggest that symbol/type/signature recovery should not be collapsed into one vague sub-bullet under decompilation, because those recovery layers affect analyst trust and navigation in different ways.

### 3. By analyst-support pattern
- observational studies of expert reverse engineers
- workflow and sensemaking models
- human-LLM teaming in reverse engineering
- notebook / memory-augmented analysis flows
- visualization and immersive-analysis support
- automation interfaces shaped by analyst interaction needs

This third axis matters because expert reverse engineering is not only about outputs and benchmarks; it is also about how analysts gather context, preserve hypotheses, navigate uncertainty, and decide what to inspect next.

## Open questions
- What makes a reverse engineer "expert-level" beyond tool familiarity?
- How should knowledge be segmented: by platform, task, tool, or mental model?
- What recurring expert heuristics show up across case studies?
- Which public sources are the best long-term feed for incremental learning?
- What source/download retention policy is useful without wasting disk?
- Which benchmarks are truly useful for studying expert RE, versus only useful for ML model benchmarking?
- How should the KB distinguish training corpora from evaluation benchmarks?

## Current promising topic pages
- `topics/benchmarks-datasets.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/symbol-type-and-signature-recovery.md`
- `topics/analyst-workflows-and-human-llm-teaming.md` (candidate)

## Emerging benchmark family split
Recent runs suggest the KB should represent obfuscation-heavy reverse engineering as a dedicated benchmark/evaluation family rather than as a sub-bullet under malware or generic decompilation.

A useful decomposition is:
- **obfuscation detection / characterization**
- **deobfuscation quality**
- **diffing and function-similarity resilience under transformation**
- **packer detection / unpacking readiness**
- **robustness against semantics-preserving adversarial transformations**

This matters because expert reversing often depends less on perfect pseudocode recovery and more on whether the analyst can still triage, match, unpack, and preserve trustworthy semantic anchors despite protective transformations.

## Structural updates from recent runs
Recent evidence suggests the KB should explicitly separate at least four benchmark/evaluation families instead of treating them as one bucket:
- **decompilation evaluation** — semantic correctness, recompilability, runtime-aware validation, human readability
- **symbol/type/signature recovery** — names, types, struct fields, prototypes, and related metadata recovery quality
- **task-level binary understanding** — analyst-like tasks such as summarization, call-site reconstruction, algorithm classification, assembly generation
- **firmware / protocol context recovery** — peripheral maps, protocol semantics, field inference, state-machine reconstruction, and environment realism

This is a better fit for expert RE knowledge than a flat tool-centric structure, because it tracks what analysts actually need to trust before making the next investigative move.

## Notes
This file should be updated over time as higher-confidence structure emerges.
