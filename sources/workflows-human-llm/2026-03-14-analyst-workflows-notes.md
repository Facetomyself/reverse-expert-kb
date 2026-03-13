# Analyst workflows and human–LLM teaming — source notes

Date: 2026-03-14
Purpose: compact source notes for workflow/sensemaking/human–LLM-teaming research relevant to reverse-engineering expertise.

## Sources
- USENIX Security 2020 — An Observational Investigation of Reverse Engineers’ Processes
  - https://www.usenix.org/conference/usenixsecurity20/presentation/votipka-observational
- NDSS 2026 — Decompiling the Synergy: An Empirical Study of Human–LLM Teaming in Software Reverse Engineering
  - https://www.ndss-symposium.org/ndss-paper/decompiling-the-synergy-an-empirical-study-of-human-llm-teaming-in-software-reverse-engineering/
- Cisco Talos 2025 — Using LLMs as a reverse engineering sidekick
  - https://blog.talosintelligence.com/using-llm-as-a-reverse-engineering-sidekick/
- Frontiers 2026 — Immersive sensemaking for binary reverse engineering: a survey and synthesis
  - https://www.frontiersin.org/journals/virtual-reality/articles/10.3389/frvir.2026.1613269/full
- Additional workflow-taxonomy lead (malware analyst workflow study; PDF extraction messy but TOC useful)
  - https://blough.ece.gatech.edu/research/papers/ccs21.pdf

## Notes by source

### Votipka et al. 2020
- Observational interview study of 16 reverse engineers.
- Three-phase model: overview → sub-component scanning → focused experimentation.
- Static methods dominate early; dynamic methods more central later.
- Strong anchor for staged RE workflow / sensemaking modeling.

### Decompiling the Synergy 2026
- Survey of 153 practitioners + human study of 48 participants (24 novices, 24 experts).
- 109+ hours of instrumented SRE.
- Novices benefit much more than experts; comprehension gains reported around 98%.
- Algorithm-like function triage up to 2.4x faster.
- Artifact recovery (symbols/comments/types) up at least 66%.
- Also reports harms: hallucinations, unhelpful suggestions, ineffective results.

### Talos 2025
- Useful practical layer: MCP-mediated LLM + disassembler workflows.
- Good notes on context-window pressure, tool-use cost, privacy, local-vs-cloud tradeoffs.
- Suggests that automation-interface quality is a major determinant of LLM usefulness in RE.

### Frontiers 2026
- Frames binary RE as abductive sensemaking under uncertainty.
- Synthesizes RE cognition + cognitive systems engineering + immersive analytics.
- Three high-level support themes: abductive iteration, working-memory augmentation, information organization.
- Useful conceptual vocabulary even if no direct benchmark/dataset contribution.

### Malware analyst workflow taxonomy lead
- Need cleaner access later.
- TOC indicates useful sections on objectives, tiers, workflows, prioritization, environment setup, evasion, usability recommendations.
- Likely good bridge between “pure RE workflow” and real-world malware-analysis practice.

## Emerging synthesis
- Expert RE should be modeled as workflow/sensemaking, not only output recovery.
- LLM value appears asymmetric across experience levels.
- Trust calibration and correction burden remain central.
- Externalization of hypotheses/notes/artifacts looks increasingly important.
