# Reverse Expert KB Run Report — 2026-03-14 12:00 Asia/Shanghai

## 1. Scope this run
This run focused on a structural gap in the workflow/evidence branch of the KB:

- separating **analytic provenance and evidence management** into its own topic
- avoiding repetition of the prior two runs on record/replay and protected-runtime analysis
- looking for RE-specific source lines rather than generic note-taking or generic HCI literature
- checking whether there is enough distinct evidence to justify a standalone topic page now, rather than leaving the material buried inside broader workflow and notebook pages

I also updated the top-level `index.md` so this branch becomes part of the KB’s visible structure rather than an implied subtheme only.

## 2. New findings

### A. RE-specific analytic provenance is a real, source-backed subtopic
The strongest new structural finding is that analytic provenance in reverse engineering has enough dedicated literature to stand as its own topic page, instead of remaining folded into:
- `topics/analyst-workflows-and-human-llm-teaming.md`
- `topics/notebook-and-memory-augmented-re.md`

This is not just “take better notes.”
It is specifically about preserving:
- analyst activity history
- evidence linkage
- hypothesis context
- rationale trails
- resumption / handoff support

### B. SensorRE is the clearest foundational anchor for provenance-aware RE
From the AFIT dissertation and associated SensorsRE paper metadata/abstract material, the strongest usable claims are:
- reverse engineering is treated as an open-ended exploration problem with many possible explanations active at once
- one major bottleneck is maintaining the context of findings within the larger task
- **SensorRE** is framed as the first analytic provenance tool specifically for software reverse engineers
- it captures sensemaking actions and exposes them via **graph** and **storyboard** views
- expert interviews informed the design
- study evidence reported improved exploration support and good usability

This makes SensorRE the canonical origin point for the KB’s provenance branch.

### C. Provenance Ninja adds an important adoption/integration lesson
The 2023 AFIT thesis on **Provenance Ninja** adds a nontrivial new angle:
- provenance support was reimplemented to run directly within **Binary Ninja**
- the thesis frames SensorRE’s external-server/browser-heavy setup as a practical limitation
- it reports functionality parity plus statistically significant efficiency gains in runtime and memory utilization

This matters because it turns provenance from a purely conceptual support layer into an interface/integration question:
- provenance support likely matters more when embedded in the analyst’s main environment
- workflow friction is not a side issue; it is central to whether this support layer is viable

### D. reAnalyst broadens the topic from analyst support to research instrumentation
The reAnalyst line adds a different but closely related branch:
- activity capture across tools using screenshots, keystrokes, active processes, and other tool-agnostic signals
- semi-automated annotation of RE activities
- a research framing around what annotations matter, what data can be collected, what users will accept, and how reliable automatic extraction can be

The strongest synthesis point here is:
- **analytic provenance is not only a workflow aid**
- it is also **infrastructure for scalable empirical study of reverse-engineering practice**

That gives the KB a better bridge between workflow theory and evaluation methodology.

### E. A sharper conceptual distinction emerged: analyst-history preservation vs execution-history preservation
This run made a cleaner distinction than the KB had before:
- **record/replay / omniscient debugging** preserves the target program’s execution history
- **analytic provenance / evidence management** preserves the analyst’s investigative history

They are related because both preserve temporal structure and reduce evidence fragility.
But they operate at different layers.

This is a useful organizing distinction for future cross-linking and for avoiding conceptual blur.

### F. Provenance appears to be a natural bridge into future trust-calibration work
A new synthesis insight from this run:
- provenance-aware systems give a more RE-specific way to discuss trust calibration and verification burden in human–LLM workflows
- instead of only saying “LLMs hallucinate,” the KB can ask:
  - what evidence trail was visible?
  - which claims were grounded?
  - which names or inferences were speculative?
  - what re-verification cost was imposed?

That suggests `topics/trust-calibration-and-verification-burden.md` should probably grow partly out of this branch, not only out of general human–LLM discussions.

## 3. Sources consulted

### Existing KB files read
- `README.md`
- `index.md`
- `runs/2026-03-14-1000-record-replay.md`
- `runs/2026-03-14-1100-protected-runtime-eval.md`
- `topics/record-replay-and-omniscient-debugging.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/native-binary-reversing-baseline.md`
- `topics/notebook-and-memory-augmented-re.md`
- `topics/analyst-workflows-and-human-llm-teaming.md`
- `topics/expert-re-overall-framework.md`
- `topics/global-map-and-ontology.md`

### External sources with usable signal
- Wayne C. Henry, *Analytic Provenance for Software Reverse Engineers* (AFIT dissertation, 2020)
  - source used: AFIT Scholar page / abstract metadata
  - URL: `https://scholar.afit.edu/etd/3882/`
- *SensorRE: Provenance Support for Software Reverse Engineers* (Computers & Security, 2020)
  - accessible via search results / metadata confirmation
  - URL consulted: `https://www.sciencedirect.com/science/article/pii/S0167404820301371`
- Caleb W. Richardson, *Improving Accessibility and Efficiency of Analytic Provenance Tools for Reverse Engineering* (AFIT thesis, 2023)
  - source used: AFIT Scholar page / abstract metadata
  - URL: `https://scholar.afit.edu/etd/7028/`
- *reAnalyst: Scalable Annotation of Reverse Engineering Activities* (arXiv 2024 / JSS 2025)
  - URLs:
    - `https://arxiv.org/abs/2406.04427`
    - `https://arxiv.org/html/2406.04427v2`
    - matching metadata hits for the JSS publication
- Votipka et al., *An Observational Investigation of Reverse Engineers’ Processes* (USENIX Security 2020)
  - used primarily as workflow context anchor already present in the KB

### Search/tooling notes
- The local search-layer script returned strong hits for SensorRE, Provenance Ninja, reAnalyst, and related workflow literature.
- Brave-backed `web_search` was unavailable because the Brave API key is not configured in this environment.
- ScienceDirect direct fetches were largely blocked, but abstract-level metadata and alternative source pages were sufficient for this run’s synthesis purpose.

## 4. Reflections / synthesis
The most important outcome is structural, not merely bibliographic.

The KB now has a cleaner split among three related but distinct workflow-support ideas:

1. **Notebook and memory-augmented RE**
   - broad durable externalization and long-horizon analysis memory
2. **Analytic provenance and evidence management**
   - explicit linkage among analyst actions, evidence, hypotheses, and conclusions
3. **Record/replay and omniscient debugging**
   - preservation of target execution history for runtime understanding

This split feels right.

Before this run, provenance ideas were present but slightly submerged inside workflow and notebook discussions. That made the KB’s workflow spine flatter than it should be.

After this run, the KB can more clearly say:
- notebook/memory support preserves analysis state
- provenance preserves analysis lineage
- record/replay preserves execution lineage

That is a more useful ontology.

A second synthesis point is that provenance work is valuable for two different reasons:
- direct analyst support
- scalable study of analyst behavior

That dual role is unusual and important. It means provenance is not only a productivity aid; it is also part of how the field can build better evidence about RE expertise itself.

A third synthesis point is that provenance provides a concrete on-ramp to future trust-calibration work. It offers a more operational vocabulary for verification burden than generic AI discourse does.

## 5. Candidate topic pages to create or improve

### Created this run
- `topics/analytic-provenance-and-evidence-management.md`

### Improve next
- `topics/analyst-workflows-and-human-llm-teaming.md`
  - add a stronger explicit cross-link to provenance support as its own branch
- `topics/notebook-and-memory-augmented-re.md`
  - clarify the boundary between broad memory support and provenance-aware evidence systems
- `topics/record-replay-and-omniscient-debugging.md`
  - add the contrast between execution-history preservation and analyst-history preservation
- `topics/global-map-and-ontology.md`
  - likely worth a small future update so provenance becomes more explicit in the support-mechanism / evidence-management layers

### Candidate new pages
- `topics/trust-calibration-and-verification-burden.md`
- `topics/scalable-study-of-re-activities.md`
- `topics/provenance-interfaces-for-reverse-engineers.md`
- `topics/malware-analysis-overlaps-and-analyst-goals.md`

## 6. Next-step research directions

### Highest-value immediate follow-up
1. Do a focused run on **trust calibration and verification burden** in RE-specific human–LLM workflows.
   - Goal: connect NDSS 2026 human–LLM findings to provenance and evidence-management concerns.

2. Do a focused run on **malware-analysis overlaps and analyst goals**.
   - The KB still lacks a clean page explaining how malware-analysis objectives modify otherwise general RE workflow models.

3. Revisit `global-map-and-ontology.md` after one or two more runs.
   - The support-mechanism / evidence branch is getting rich enough to merit a tighter map.

### Secondary research directions
- find more concrete practitioner evidence on whether provenance-style systems are actually adopted in day-to-day RE work
- look for additional RE/HCI work on uncertainty representation and evidence-link interfaces
- examine whether anti-analysis / anti-tamper domains create stronger or different provenance requirements

## Files changed
- created `topics/analytic-provenance-and-evidence-management.md`
- updated `index.md`
- created this run report
- logged the missing Brave API key issue in `.learnings/ERRORS.md`
