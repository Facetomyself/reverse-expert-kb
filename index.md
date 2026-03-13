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
The KB now seems likely to need at least two orthogonal organization schemes:

### 1. By domain
- desktop / native binaries
- malware analysis overlaps
- mobile reversing
- firmware / embedded
- protocol reverse engineering
- anti-tamper / anti-cheat / obfuscation-heavy targets

### 2. By evaluation object
- decompiler output quality
- symbol / type / signature recovery
- task-level binary understanding
- firmware corpus realism and environment reconstruction
- protocol message/state reconstruction
- malware corpora used for RE-adjacent analysis

This second axis is important because recent papers increasingly evaluate not just tools, but specific analyst-relevant outputs and tasks.

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

## Notes
This file should be updated over time as higher-confidence structure emerges.
