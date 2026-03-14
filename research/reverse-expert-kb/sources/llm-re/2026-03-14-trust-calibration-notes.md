# Source Notes — Trust Calibration and Verification Burden in Human–LLM RE

Date: 2026-03-14
Topic: trust calibration / verification burden / human–LLM reverse engineering

## Core source anchors

### 1. NDSS 2026 — Decompiling the Synergy
URL:
- https://www.ndss-symposium.org/ndss-paper/decompiling-the-synergy-an-empirical-study-of-human-llm-teaming-in-software-reverse-engineering/
- search-discovered PDF URL: https://www.ndss-symposium.org/wp-content/uploads/2026-f380-paper.pdf

Usable signals:
- first systematic investigation claim for human–LLM teaming in software reverse engineering
- survey of 153 practitioners
- human study with 48 participants
- 109+ hours of instrumented SRE activity
- strong novice gains, smaller expert gains
- hallucinations / unhelpful suggestions remain significant harms
- artifact recovery improves, but workflow value remains mixed

Why it matters:
- strongest RE-specific justification for modeling verification burden and trust calibration as central workflow concerns

### 2. Cisco Talos — Using LLMs as a reverse engineering sidekick
URL:
- https://blog.talosintelligence.com/using-llm-as-a-reverse-engineering-sidekick/

Usable signals:
- frames LLMs as sidekicks, not replacements
- emphasizes MCP integration with IDA/Ghidra-like tooling
- details practical constraints: context window limits, tool-use cost, privacy/confidentiality, local-model latency
- notes models not suited for structured tool use may hallucinate during code analysis

Why it matters:
- shows that trust problems are partly workflow/integration failures rather than only base-model failures

### 3. 2025 RE-specific LLM evaluation papers
URLs:
- https://arxiv.org/abs/2504.21803
- https://arxiv.org/abs/2505.16366
- https://arxiv.org/abs/2509.21821

Usable signals:
- output-centric binary-analysis evaluation is accelerating quickly
- function-name recovery, summarization, and type inference are becoming common targets
- SoK explicitly says evaluation and reproducibility remain uneven

Why it matters:
- suggests a gap between task-performance measurement and verification-burden measurement

## Synthesis notes
- The field has stronger evidence for "LLMs can sometimes produce useful RE artifacts" than for "LLMs reduce analyst verification cost."
- Trust calibration in RE is tightly coupled to grounding visibility.
- Provenance/evidence-management pages now look like the natural mitigation branch for this topic.
- This topic should stay distinct from generic hallucination discussion because RE has unusually high costs for semantic drift and overconfident naming.

## Operational note
- Direct PDF text extraction via `web_fetch` on the NDSS PDF returned mostly raw PDF bytes in this environment, so the NDSS webpage plus search-layer metadata was the more reliable source path for this run.