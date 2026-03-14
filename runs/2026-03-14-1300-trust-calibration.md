# Reverse Expert KB Run Report — 2026-03-14 13:00 Asia/Shanghai

## 1. Scope this run
This run focused on a gap that had become more obvious after the prior workflow-support runs:

- **trust calibration and verification burden** in human–LLM reverse-engineering workflows
- checking whether this should remain a subsection inside the workflow page or become its own topic page
- preferring RE-specific human-study and workflow-integration evidence over generic AI trust literature
- connecting the topic to the newly created provenance/evidence-management branch rather than treating it as generic “LLM caution”

The goal was to add genuinely new structure and synthesis, not to restate that “LLMs hallucinate.”

## 2. New findings

### A. Trust calibration is mature enough to stand as its own KB topic
The strongest structural conclusion from this run is that **trust calibration and verification burden deserve a standalone page**.

Why:
- the NDSS 2026 human–LLM RE study makes verification burden central rather than incidental
- the topic has clear ties to workflow evaluation, notebook/memory support, provenance, and benchmark interpretation
- there is now enough RE-specific evidence to say more than generic AI-safety platitudes

This page should still be `structured`, not `mature`, because direct RE-specific source density is meaningful but still limited.

### B. The key RE question is total trustworthy-progress cost, not output plausibility
A sharper synthesis point emerged this run:
- the relevant unit is not whether an answer looks intelligent
- it is whether the analyst reaches a trustworthy conclusion with **lower total checking cost**

That creates a better evaluation lens for assistant use in RE:
- plausible semantic output can still be net-negative
- local artifact recovery can improve while end-to-end workflow value stays mixed
- verification burden is not overhead outside the task; it is part of the task

### C. The NDSS 2026 human-study result is the core anchor
The NDSS paper remains the strongest single source for this topic because it combines:
- practitioner survey evidence
- human study evidence
- novice/expert comparison
- concrete harms, not only gains

The most useful synthesis from it is not merely “novices gain more.”
It is that **artifact recovery improvements do not eliminate trust-calibration problems**.

That means the KB should not let better task outputs stand in for better analyst outcomes.

### D. Workflow integration failures are themselves calibration failures
The Cisco Talos sidekick article was useful not as a rigorous user study, but because it makes several practical calibration pressures explicit:
- structured tool-use support matters
- context-window limitations matter
- prompt truncation and lost tool context matter
- cost/latency/privacy constraints affect realistic usage patterns

This run clarified a useful conceptual point:
**trust calibration problems are not only model-quality problems; they are often orchestration and interface problems.**

A strong model with bad context handling can still increase verification burden.

### E. The field currently measures output quality better than it measures checking cost
The 2025 RE/LLM papers on binary understanding, ReCopilot, and the SoK collectively suggest a field-level asymmetry:
- function name recovery, summarization, and type inference are being benchmarked aggressively
- evaluation/reproducibility issues are already being noticed
- but there is still much less direct measurement of analyst checking burden, miscalibration cost, or error recoverability

This is important for the KB because it gives a cleaner criticism than “benchmarks are bad.”
The better claim is:
- **current RE/LLM evaluation is stronger on output measurement than on reliance-cost measurement**

### F. Provenance is now the most concrete mitigation branch for this topic
A new cross-topic synthesis became much clearer in this run:
- trust calibration is not only about better prompting or better models
- it is deeply affected by whether claims are tied to visible evidence and rationale

That means the newly created provenance page is not just adjacent background.
It is one of the clearest RE-specific mitigation layers for verification burden.

This suggests the KB now has a cleaner logic:
- notebook/memory support preserves context
- provenance preserves evidence lineage
- trust-calibration analysis asks how those structures reduce assistant-checking cost

### G. Expertise asymmetry should remain central, not incidental
This run also sharpened a likely long-term principle:
- novice benefit and expert benefit should be modeled separately
- experts may be more sensitive to interruption, low-value suggestions, and semantic anchoring costs
- some assistant roles may be net-positive mostly for novices or for narrow task classes

So the KB should resist a global “LLMs help RE” or “LLMs hurt RE” framing.
Task class and expertise level matter too much.

## 3. Sources consulted

### Existing KB files read
- `README.md`
- `index.md`
- `runs/2026-03-14-1000-record-replay.md`
- `runs/2026-03-14-1100-protected-runtime-eval.md`
- `runs/2026-03-14-1200-analytic-provenance.md`
- `topics/analyst-workflows-and-human-llm-teaming.md`
- `topics/notebook-and-memory-augmented-re.md`
- `topics/analytic-provenance-and-evidence-management.md`

### External sources with usable signal
- NDSS 2026 paper page:
  - `https://www.ndss-symposium.org/ndss-paper/decompiling-the-synergy-an-empirical-study-of-human-llm-teaming-in-software-reverse-engineering/`
- NDSS 2026 PDF URL discovered via search:
  - `https://www.ndss-symposium.org/wp-content/uploads/2026-f380-paper.pdf`
  - note: direct PDF text extraction was poor in this environment
- Cisco Talos:
  - `https://blog.talosintelligence.com/using-llm-as-a-reverse-engineering-sidekick/`
- ReCopilot:
  - `https://arxiv.org/abs/2505.16366`
- Binary code understanding empirical study:
  - `https://arxiv.org/abs/2504.21803`
- SoK on LLMs for RE:
  - `https://arxiv.org/abs/2509.21821`
- reAnalyst context source revisited:
  - `https://arxiv.org/abs/2406.04427`

### Source material saved
- `sources/llm-re/2026-03-14-trust-calibration-notes.md`

## 4. Reflections / synthesis
The most important outcome is a cleaner evaluation vocabulary for the KB.

Before this run, the workflow page already mentioned:
- verification burden
- trust calibration
- hallucination risk

But those ideas were still somewhat compressed into one broad workflow page.

After this run, the KB can say more clearly:
- workflow pages describe how analysts and assistants interact over time
- provenance pages describe how evidence and rationale stay linked
- trust-calibration pages describe whether assistance reduces or increases the cost of justified reliance

That feels like a meaningful ontology improvement.

A second synthesis point is that RE-specific calibration differs from generic LLM trust discourse because reverse engineering has a particularly high cost for:
- semantic anchoring on wrong names
- adopting unsupported type claims
- carrying false summaries forward into later analysis
- wasting focused-analysis time on plausible but irrelevant assistant output

So this topic should stay grounded in RE artifacts and workflows, not drift into generic AI governance language.

A third useful synthesis point is that provenance now looks like the natural practical bridge between workflow theory and calibrated assistant use. That is probably the most important cross-link added by this run.

## 5. Candidate topic pages to create or improve

### Created this run
- `topics/trust-calibration-and-verification-burden.md`

### Improve next
- `topics/analyst-workflows-and-human-llm-teaming.md`
  - may later benefit from a shorter high-level summary now that trust calibration has its own child page
- `topics/notebook-and-memory-augmented-re.md`
  - could add a more explicit note that memory structure affects assistant verification cost
- `topics/analytic-provenance-and-evidence-management.md`
  - could add a direct cross-link section on calibration / re-verification burden
- `topics/benchmarks-datasets.md`
  - likely deserves future language about verification-aware evaluation dimensions

### Candidate new pages
- `topics/verification-aware-benchmarks-for-re.md`
- `topics/grounding-visibility-for-re-assistants.md`
- `topics/novice-vs-expert-llm-benefit-in-re.md`
- `topics/interface-patterns-for-calibrated-re-assistance.md`

## 6. Next-step research directions

### Highest-value immediate follow-up
1. Do a focused run on **malware-analysis overlaps and analyst goals**.
   - This remains one of the clearest open structural gaps in the KB.

2. Do a focused run on **verification-aware benchmark design for RE assistants**.
   - Goal: connect benchmark pages to trust-calibration concerns instead of treating them separately.

3. Strengthen the provenance ↔ trust-calibration bridge.
   - Look for sources or design ideas that explicitly tie visible grounding, evidence traces, or rationale capture to reliance decisions.

### Secondary directions
- collect more practitioner evidence on which assistant tasks are considered worth verifying in day-to-day reversing
- look for interface/UI work on uncertainty presentation in analyst tools
- separate task classes where expert benefit seems robust from classes where checking cost dominates

## Files changed
- created `topics/trust-calibration-and-verification-burden.md`
- created `sources/llm-re/2026-03-14-trust-calibration-notes.md`
- updated `index.md`
- created this run report

## Operational notes
- search-layer results were useful, but required manual filtering because several generic trust/calibration papers ranked highly without being RE-specific
- one direct NDSS PDF fetch route produced unusable raw PDF bytes in this environment, so the NDSS webpage plus search-layer metadata was the better source path
- this run remained fully within research/collection/synthesis and did not pivot into implementation work