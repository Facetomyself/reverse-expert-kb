# Trust Calibration and Verification Burden in Human–LLM Reverse Engineering

Topic class: topic synthesis
Ontology layers: workflow/sensemaking, evaluation frame, evidence management
Maturity: structured
Related pages:
- topics/analyst-workflows-and-human-llm-teaming.md
- topics/notebook-and-memory-augmented-re.md
- topics/analytic-provenance-and-evidence-management.md
- topics/decompilation-and-code-reconstruction.md
- topics/symbol-type-and-signature-recovery.md
- topics/benchmarks-datasets.md

## 1. Topic identity

### What this topic studies
This topic studies how reverse engineers should decide when to rely on LLM outputs, how much checking those outputs require, and which workflow designs make assistance net-positive rather than confidence-distorting.

It covers:
- trust calibration in human–LLM reverse-engineering workflows
- verification burden imposed by assistant outputs
- overtrust, undertrust, and selective reliance
- assistant failure modes that are especially costly in reverse engineering
- interface and workflow patterns that keep uncertainty visible
- the relationship between provenance, evidence trails, and assistant-checking cost

### Why this topic matters
In reverse engineering, an assistant can look useful while still making the analyst’s job worse.

That happens when the model produces:
- plausible but wrong semantics
- overconfident names or type guesses
- irrelevant suggestions that interrupt expert flow
- partially correct summaries that hide crucial caveats
- outputs whose checking cost exceeds their value

This topic matters because reverse engineering is highly verification-sensitive.
A fluent wrong answer is not merely noisy; it can redirect attention, contaminate naming, and increase downstream checking burden.

### Ontology role
This page mainly belongs to:
- **workflow/sensemaking**
- **evaluation frame**
- **evidence management**

It is a workflow page because trust decisions happen inside active analysis.
It is an evaluation page because assistance quality must be judged partly by verification cost, not just raw output quality.
It is also an evidence-management page because traceable evidence and provenance directly affect how expensive verification becomes.

### Page class
- topic synthesis page

### Maturity status
- structured

## 2. Core framing

### Core claim
Trust calibration and verification burden should be treated as a first-class reverse-engineering topic, not as a generic AI safety footnote.

The key analyst question is not:
- did the model produce a plausible answer?

It is:
- did the model reduce the total cost of reaching a trustworthy conclusion?

### What this topic is not
This topic is **not**:
- generic LLM trustworthiness discussion detached from RE
- only benchmark accuracy reporting
- only hallucination anecdotes
- a claim that analysts should never trust assistants

It is about analyst-centered reliance decisions under reverse-engineering evidence constraints.

### Key distinctions
Several distinctions should remain explicit.

#### 1. Output plausibility vs verification cost
An output may look strong while requiring expensive checking.
In RE, the verification burden can dominate any nominal time savings.

#### 2. Local correctness vs workflow harm
A suggestion may be locally useful but globally harmful if it causes naming drift, false anchoring, or distraction.

#### 3. Novice uplift vs expert uplift
A system that helps novices substantially may offer smaller average benefit to experts, and may even impose extra interruption cost on them.

#### 4. Missing evidence vs hidden evidence
An answer without visible grounding is harder to calibrate than one tied to specific code, traces, or prior notes.

#### 5. Assistant confidence vs analyst confidence
The model sounding certain is not evidence that the analyst should rely on it.
The relevant confidence is the analyst’s justified confidence after checking.

## 3. What this topic depends on
This topic depends on several other KB concepts.

- **Analyst workflows and human–LLM teaming**
  - because trust decisions happen inside staged sensemaking, not in isolation
- **Notebook and memory-augmented RE**
  - because explicit external memory reduces context loss and makes checking easier
- **Analytic provenance and evidence management**
  - because provenance can lower the cost of deciding what an assistant answer is actually grounded in
- **Decompilation and code reconstruction**
  - because many high-visibility LLM use cases operate on pseudo-code and semantic reconstruction
- **Benchmarks and datasets**
  - because output-centric evaluation often misses verification burden and miscalibration cost

Without these dependencies, trust calibration can collapse into generic “be careful with AI” advice.

## 4. What this topic enables
Strong understanding of this topic enables:
- better decisions about when assistant use is worthwhile
- more realistic evaluation of LLM support in RE workflows
- clearer separation between suggestion value and checking cost
- workflow designs that keep uncertainty visible
- better use of provenance and notebook structures to support verification
- more disciplined comparison of novice and expert benefit

In analyst terms, this topic helps answer:
- should I rely on this suggestion at all?
- what evidence do I need to check before adopting it?
- is this answer accelerating me or just giving me extra work?
- what interface features would make this safer to use?

## 5. High-signal sources and findings

### A. The NDSS 2026 human study makes verification burden a central RE issue
Source:
- *Decompiling the Synergy: An Empirical Study of Human–LLM Teaming in Software Reverse Engineering* (NDSS 2026)

High-signal findings:
- reports a survey of **153 practitioners** and a human study with **48 participants**
- finds substantial novice gains in comprehension and triage
- finds much smaller average gains for experts
- reports that hallucinations, unhelpful suggestions, and ineffective outputs remain significant harms
- shows that artifact recovery can improve while overall workflow value remains mixed

Why it matters:
- this is the clearest RE-specific anchor that assistance value must be judged together with analyst checking burden
- it supports the idea that trust calibration is not a side concern but a core outcome variable

### B. Practical RE sidekick workflows show that context and tool-integration failures directly affect calibration
Source:
- Cisco Talos, *Using LLMs as a reverse engineering sidekick* (2025)

High-signal findings:
- treats LLMs as workflow complements rather than replacements
- emphasizes MCP/tool integration with IDA Pro and Ghidra
- highlights input-context limits, cost growth from tool use, privacy constraints, and model suitability for structured tool calling
- notes that models not tuned for structured tool use may hallucinate during code analysis

Why it matters:
- calibration problems are not only model-internal; they are produced by interface, context truncation, and tool orchestration failures
- a poorly integrated assistant can raise verification burden even when the base model is strong

### C. RE-specific LLM evaluation is growing faster than human-verification evaluation
Sources:
- *An Empirical Study on the Effectiveness of Large Language Models for Binary Code Understanding* (2025)
- *Reverse Engineering Copilot in Binary Analysis* (ReCopilot, 2025)
- *Potentials and Challenges of Large Language Models for Reverse Engineering* (SoK, 2025)

High-signal findings:
- binary-analysis papers increasingly benchmark function-name recovery, summarization, type inference, and other semantic tasks
- systems like ReCopilot report strong task-level gains through domain-specific training and richer context
- the SoK explicitly identifies evaluation and reproducibility gaps across LLM-for-RE work

Why it matters:
- the field is getting better at measuring output quality than at measuring checking cost and reliance safety
- this creates a structural gap: benchmark improvement does not automatically imply reduced verification burden for analysts

### D. Provenance-aware support offers a concrete route to lower verification burden
Sources:
- `topics/analytic-provenance-and-evidence-management.md`
- SensorRE / Provenance Ninja / reAnalyst source line summarized there

High-signal synthesis:
- provenance systems preserve links among observations, hypotheses, and conclusions
- that structure makes it easier to ask what an assistant answer is grounded in
- visible rationale trails can reduce the re-verification cost of revisiting old claims or assistant-suggested names

Why it matters:
- trust calibration in RE should not be framed only as “better prompts” or “better models”
- evidence linkage and provenance are part of the solution space

### E. Trust calibration in RE is asymmetric across expertise levels and task classes
Synthesis across current sources suggests:
- novices may gain more from explanatory assistance and triage hints
- experts may gain less on average because they already possess efficient workflows and can be more sensitive to interruption or low-value suggestions
- known-algorithm recognition and artifact drafting may be relatively favorable assistant roles
- high-uncertainty semantic inference can impose larger checking costs than it appears to from surface fluency

Why it matters:
- this topic should remain tied to task class and expertise level rather than seeking one global verdict about LLM usefulness in RE

## 6. Emerging internal structure of the topic
A stable internal decomposition is emerging.

### 1. Verification burden as an evaluation dimension
Includes:
- checking cost
- correction cost
- interruption cost
- downstream rework cost

### 2. Trust calibration failures
Includes:
- overtrust in fluent answers
- undertrust in useful drafts
- anchoring on premature names or summaries
- acceptance of unsupported semantic claims

### 3. Interface and orchestration factors
Includes:
- context truncation
- grounding visibility
- tool-call design
- provenance display
- uncertainty presentation

### 4. Expertise-sensitive reliance patterns
Includes:
- novice vs expert benefit differences
- task-dependent reliance
- when assistance narrows or widens the effective expertise gap

### 5. Evidence-linked mitigation strategies
Includes:
- provenance-aware workflows
- notebook support
- explicit uncertainty marking
- retrieval of prior validated context
- structured comparison between assistant claim and target evidence

## 7. Analyst workflow implications
This topic matters especially during:

### Orientation
Assistants can help with rough explanation and triage, but early-stage trust should remain light because context is still incomplete.

### Naming and semantic reconstruction
This is a high-risk stage for miscalibration.
Plausible names, types, and summaries can stabilize understanding or poison it.

### Focused experimentation
Trust should increase only when assistant claims are connected to dynamic evidence, trace results, or analyst-confirmed structure.

### Long-horizon analysis
Verification burden compounds over time if unsupported names and claims enter the notebook as if they were facts.
This is where provenance and uncertainty tracking matter most.

### Mistakes this topic helps prevent
A strong model of this topic helps avoid:
- adopting fluent but unsupported semantic labels
- mistaking benchmark gains for end-to-end workflow gains
- assuming expert analysts benefit the same way novices do
- using assistants without enough evidence visibility to calibrate reliance
- letting hidden context loss or truncation masquerade as reasoning failure only

## 8. Evaluation dimensions
The most important evaluation dimensions for this topic are:

### Verification burden
How much checking and correction work does the assistant impose?

### Trust calibration quality
Does the workflow help the analyst rely appropriately rather than too much or too little?

### Grounding visibility
Can the analyst see what code, traces, or prior notes support the answer?

### Expertise sensitivity
How do costs and benefits differ across novice and expert analysts?

### Workflow payoff
After accounting for checking cost, is the analyst actually better off?

### Error recoverability
When the assistant is wrong, how easy is it to detect and repair the damage?

Among these, the especially central dimensions are:
- verification burden
- trust calibration quality
- grounding visibility
- workflow payoff

## 9. Cross-links to related topics

### Closely related pages
- `topics/analyst-workflows-and-human-llm-teaming.md`
  - because this page sharpens one of that topic’s central evaluation concerns
- `topics/notebook-and-memory-augmented-re.md`
  - because durable context and uncertainty management affect checking cost
- `topics/analytic-provenance-and-evidence-management.md`
  - because provenance is one of the clearest RE-specific mitigation layers for calibration problems
- `topics/decompilation-and-code-reconstruction.md`
  - because many assistant claims operate over pseudo-code semantics and reconstructed structure
- `topics/benchmarks-datasets.md`
  - because benchmark design should eventually include trust and verification-aware measures

### Depends on framework pages
- `topics/expert-re-overall-framework.md`
- `topics/global-map-and-ontology.md`

### Often confused with
- generic hallucination discussion
- raw model accuracy evaluation
- broad human–AI trust literature without RE grounding

## 10. Open questions
- Which RE task classes consistently have acceptable verification burden under LLM assistance?
- What interface patterns best expose uncertainty and grounding without slowing analysts too much?
- How should future RE benchmarks measure verification cost and not just output quality?
- Can provenance-aware assistants reduce miscalibration enough to change expert adoption patterns?
- Which errors are most damaging in practice: wrong names, wrong summaries, wrong type claims, or omitted caveats?
- How should assistants communicate tentative semantic guesses so they do not harden into false facts?

## 11. Suggested next expansions
This topic may later split into several child pages:
- `topics/novice-vs-expert-llm-benefit-in-re.md`
- `topics/grounding-visibility-for-re-assistants.md`
- `topics/verification-aware-benchmarks-for-re.md`
- `topics/interface-patterns-for-calibrated-re-assistance.md`

## 12. Source footprint / evidence quality note
Current evidence quality is good enough for a standalone structured page, but not yet for mature status.

Strengths:
- strong RE-specific anchor from the NDSS 2026 human–LLM study
- practical workflow integration evidence from the Talos sidekick article
- adjacent support from RE-specific benchmark, copilot, and SoK papers
- strong conceptual linkage to provenance and notebook topics already present in the KB

Limitations:
- direct RE-specific trust-calibration studies are still sparse
- many papers measure task performance more directly than checking burden
- some available evidence is practitioner/integration-oriented rather than controlled user-study evidence

Overall assessment:
- this topic is real, important, and sufficiently source-backed to stand alone as `structured`

## 13. Topic summary
Trust calibration and verification burden matter in reverse engineering because assistant value is determined not just by what the model says, but by how much justified confidence the analyst can extract from it without paying too much checking cost.

This topic gives the KB a sharper way to evaluate human–LLM workflows: not by fluency or benchmark gain alone, but by whether trustworthy reverse-engineering progress becomes cheaper or more expensive.