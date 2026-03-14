# Analyst Workflows and Human–LLM Teaming in Reverse Engineering

Topic class: topic synthesis
Ontology layers: workflow/sensemaking, support mechanism, evaluation frame
Maturity: mature
Related pages:
- topics/expert-re-overall-framework.md
- topics/global-map-and-ontology.md
- topics/topic-template-and-normalization-guide.md
- topics/benchmarks-datasets.md
- topics/symbol-type-and-signature-recovery.md
- topics/mobile-reversing-and-runtime-instrumentation.md

## 1. Topic identity

### What this topic studies
This topic studies how reverse engineers actually work, how they move through uncertainty, how they externalize evidence, and how human–LLM collaboration changes or fails to change that process.

It covers:
- observational models of reverse-engineering practice
- workflow and sensemaking structure
- hypothesis formation and revision
- cognitive support and externalization
- notebook / memory-oriented analysis patterns
- practical integration of LLMs into analyst workflows
- trust calibration, context management, and verification burden

### Why this topic matters
A reverse-engineering expert KB cannot be only about tools, outputs, or benchmark scores.
It also needs to describe how expert analysis actually progresses.

Without workflow understanding, the KB risks making several category errors:
- treating all reverse-engineering tasks as if they were static recovery problems
- assuming better local outputs automatically produce better global understanding
- evaluating assistance tools without modeling human verification cost
- overlooking evidence management, memory burden, and phase transitions in analysis

This topic matters because reverse engineering is not merely artifact recovery. It is a staged sensemaking process under uncertainty.

### Ontology role
This page mainly belongs to:
- **workflow/sensemaking**
- **support mechanism**
- **evaluation frame**

It is a workflow page because it models the analyst’s process.
It is a support-mechanism page because notebooks, interfaces, and LLM tools shape how work is carried out.
It also belongs to evaluation because many tools can only be judged meaningfully through their effect on analyst workflow.

### Page class
- topic synthesis page

### Maturity status
- mature

## 2. Core framing

### Core claim
Expert reverse engineering is best understood as a staged sensemaking discipline, and human–LLM teaming should be evaluated according to whether it improves that discipline rather than whether it merely produces plausible text.

The central question is not:
- can an assistant say something intelligent about a binary?

The central question is:
- does the workflow become more accurate, more stable, faster, or less cognitively fragile for the analyst?

### What this topic is not
This topic is **not**:
- generic AI coding assistance
- a broad “LLMs in security” summary
- a tool list for reverse engineering
- an argument that automation replaces analysts

It is about analyst-centered reverse-engineering practice.

### Key distinctions
Several distinctions are essential.

#### 1. Output quality vs workflow value
An assistant may produce plausible output while making the human workflow worse by increasing verification cost or false confidence.

#### 2. Novice benefit vs expert benefit
A tool that greatly helps novices may provide only modest benefit to experts, or may help them in different ways.

#### 3. Local suggestion quality vs long-horizon evidence stability
Useful reversing often depends on preserving hypotheses, evidence trails, and uncertainty boundaries across long sessions.

#### 4. Tool integration vs raw model capability
A strong model without good access to disassembler state, memory, notes, or context may be less useful than a weaker model integrated well into the workflow.

#### 5. Assistance vs replacement
The most realistic framing is often augmentation, orchestration, and externalization support rather than full analyst substitution.

## 3. What this topic depends on
This topic depends on several other KB concepts.

- **Recovery objects**
  - because workflow is about deciding which artifact needs to be trusted next
- **Evaluation framing**
  - because workflow benefit must be judged in more than intrinsic task terms
- **Domain constraints**
  - because workflows differ across malware, mobile, firmware, obfuscated binaries, and protocol analysis
- **Support mechanisms**
  - because tool integration, instrumentation access, and note systems strongly shape analyst behavior

Without those dependencies, workflow discussion becomes too abstract to guide real reverse engineering.

## 4. What this topic enables
Strong workflow understanding enables the KB to:
- explain why certain tools matter at specific phases of analysis
- model how experts transition from orientation to focused experimentation
- evaluate LLM assistance in terms of verification burden and trust calibration
- identify where note-taking, memory systems, and evidence management are critical
- connect benchmark claims back to actual analyst use
- distinguish local acceleration from genuine end-to-end workflow improvement

In analyst terms, this topic helps answer:
- what should I do next?
- what kind of evidence do I need now?
- when should I stop reading statically and test a hypothesis dynamically?
- what should I externalize instead of keeping in my head?
- where can an assistant help without corrupting the analysis?

## 5. High-signal sources and findings

### A. Reverse engineering already has observable process structure

#### Votipka et al.
Source:
- *An Observational Investigation of Reverse Engineers’ Processes* (USENIX Security 2020)

High-signal findings:
- observational/interview-based study of **16 reverse engineers**
- identifies a three-phase model:
  - overview
  - sub-component scanning
  - focused experimentation
- reports that analysts tend to rely more on static methods early and more on dynamic methods later
- experience matters across all phases, but in different ways
- proposes design guidance for reverse-engineering tools

Why it matters:
- this is one of the strongest anchors for treating RE as staged sensemaking rather than a flat set of tactics
- it justifies organizing the KB around workflow transitions, not only topic silos

### B. Workflow taxonomies exist beyond one narrow subdomain

#### Malware-analysis workflow taxonomy signals
Accessible signal from artifact and paper structure suggests coverage of:
- analyst goals and tiers
- workflow branching conditions
- prioritization logic
- dynamic-analysis setup choices
- evasion handling
- usability recommendations

Why it matters:
- this suggests workflow modeling is rich enough to stand beside benchmark taxonomy as a first-class topic family
- it also implies that differences in expertise level and analysis objective must remain visible in the KB

### C. Human–LLM teaming is now empirically visible in software reverse engineering

#### Decompiling the Synergy
Source:
- *Decompiling the Synergy: An Empirical Study of Human–LLM Teaming in Software Reverse Engineering* (NDSS 2026)

High-signal findings:
- claims to be the first systematic investigation of human–LLM teaming in software reverse engineering
- includes survey data from **153 practitioners**
- includes a human study with **48 participants** split across novices and experts
- instruments over **109 hours** of reverse-engineering activity
- reports notable gains for novices in comprehension and triage
- reports more limited average gains for experts
- reports improved artifact recovery but also significant harms from hallucinations and ineffective suggestions

Why it matters:
- this is a major anchor for the KB’s workflow layer
- it supports a nuanced view: LLMs may meaningfully narrow novice/expert gaps in some tasks, but do not simply make all analysts uniformly better
- it also reinforces that verification burden and overtrust risk are central evaluation dimensions

### D. Practical sidekick models emphasize interface and orchestration

#### Cisco Talos: Using LLMs as a reverse engineering sidekick
High-signal findings:
- frames LLMs as workflow complements rather than replacements
- emphasizes MCP-style integration with tools such as IDA Pro and Ghidra
- highlights practical constraints:
  - context-window pressure
  - tool-call overhead and cost
  - privacy and confidentiality limits
  - local-model latency and hardware limits
  - model-specific support for structured tool use

Why it matters:
- this is a practical confirmation that workflow value depends on integration and orchestration, not just model intelligence
- it supports treating disassembler integration and context management as first-class workflow design problems

### E. Cognitive support and externalization deserve a first-class place

#### Immersive sensemaking survey/synthesis
Source:
- *Immersive sensemaking for binary reverse engineering: a survey and synthesis* (Frontiers 2026)

High-signal findings:
- frames binary reverse engineering as cognitively demanding and unlikely to be fully automated away
- emphasizes:
  - abductive iteration
  - working-memory support
  - information organization
- treats representations and externalization as mechanisms for stabilizing reasoning

Why it matters:
- this broadens the workflow topic beyond LLMs alone
- it strongly supports the idea that notes, structure, memory systems, and representation design are central to expert RE

## 6. Emerging internal structure of the topic
A stable internal decomposition is emerging.

### 1. Process models of reverse engineering
Includes:
- staged workflow models
- transitions between static and dynamic methods
- expertise-dependent differences in behavior

### 2. Evidence externalization and memory support
Includes:
- note-taking and notebook systems
- hypothesis logs
- uncertainty tracking
- memory-augmented and representation-aware workflows

### 3. Tooling and interface mediation
Includes:
- disassembler integration
- MCP or tool-protocol layers
- structured tool use
- context retrieval and state preservation

### 4. Human–LLM collaboration
Includes:
- explanation support
- triage acceleration
- artifact drafting
- candidate hypothesis generation
- hallucination and overtrust risks

### 5. Workflow evaluation
Includes:
- comprehension gains
- time-to-triage
- correction burden
- trust calibration
- downstream quality of conclusions

## 7. Analyst workflow implications
This page is itself about workflow, so its implications are central.

### Orientation
Analysts often begin by trying to establish:
- what kind of target this is
- where to look next
- what evidence is cheap to obtain
- which hypotheses are worth keeping alive

Workflow-aware tooling should support broad orientation without forcing premature commitment.

### Sub-component scanning
At this stage, analysts need:
- rapid local inspection
- cross-reference support
- clustering and naming aids
- lightweight note externalization

This is where symbol/type recovery and search support can become disproportionately valuable.

### Focused experimentation
Later stages often need:
- dynamic validation
- runtime instrumentation
- trace comparison
- explicit evidence trails

This is where mobile instrumentation, firmware rehosting, or protocol inference may become essential, depending on domain.

### Long-horizon understanding
Large reverse-engineering tasks decay unless the analyst can preserve:
- hypotheses
- evidence
- uncertainty boundaries
- naming rationale
- links between observations and conclusions

This is one of the strongest arguments for notebook-style and memory-augmented workflows.

### Mistakes this topic helps prevent
A strong workflow model helps avoid:
- treating reverse engineering as pure linear reading
- trusting fluent assistant output too quickly
- losing track of what has actually been verified
- mixing tentative names with stable facts
- overvaluing local acceleration that harms end-to-end understanding

## 8. Evaluation dimensions
The most important evaluation dimensions for this topic are:

### Workflow payoff
Does the system improve actual analyst progress rather than isolated task output?

### Verification burden
How much extra checking does the analyst need to do because of the system’s suggestions?

### Trust calibration
Does the workflow help the analyst keep uncertainty visible and avoid false confidence?

### Memory and evidence stability
Does the system help preserve hypotheses, evidence, and rationale over time?

### Experience-level sensitivity
Who benefits most: novices, intermediates, experts?
Are the benefits and harms the same across groups?

### Integration quality
How well does the support mechanism connect to disassemblers, notes, traces, context retrieval, and other tools?

### Transferability across domains
Do workflow patterns generalize across mobile, firmware, malware, protocol, and protected-target reversing?

Among these, the especially central dimensions are:
- workflow payoff
- verification burden
- trust calibration
- memory/evidence stability

## 9. Cross-links to related topics

### Closely related pages
- `topics/benchmarks-datasets.md`
  - because workflow-aware evaluation should shape how benchmarks are interpreted
- `topics/symbol-type-and-signature-recovery.md`
  - because semantic anchors heavily influence navigation and note quality
- `topics/mobile-reversing-and-runtime-instrumentation.md`
  - because runtime-centered domains make workflow transitions especially visible
- `topics/firmware-and-protocol-context-recovery.md`
  - because context-heavy domains highlight why workflow cannot be modeled as code reading alone

### Depends on framework pages
- `topics/expert-re-overall-framework.md`
- `topics/global-map-and-ontology.md`

### Often confused with
- generic AI assistant discussions
- reverse-engineering tool lists
- broad HCI discussions without RE grounding

## 10. Open questions
- What exact tool-design guidelines from observational RE studies should be extracted into the KB as canonical workflow principles?
- Which workflow patterns generalize across malware, firmware, vulnerability research, mobile reversing, and protected binaries?
- What kinds of LLM assistance are consistently net-positive for experts rather than only for novices?
- How should notebook/memory-augmented RE be evaluated in a way that captures long-horizon cognitive benefit?
- Which failure modes are most dangerous in practice: hallucinated semantics, context loss, tool misuse, overconfident naming, or evidence drift?
- What interfaces best preserve uncertainty and evidence traceability while still accelerating analyst work?

## 11. Suggested next expansions
This topic may later split into several child pages:
- `topics/process-models-of-reverse-engineering.md`
- `topics/notebook-and-memory-augmented-re.md`
- `topics/llm-sidekicks-in-re-workflows.md`
- `topics/trust-calibration-and-verification-burden.md`
- `topics/interface-design-for-re-automation.md`

## 12. Source footprint / evidence quality note
Current evidence quality is strong enough for a mature synthesis page.

Strengths:
- direct observational/process-study anchor
- emerging empirical human–LLM teaming evidence in software reverse engineering
- practical workflow integration material from industry
- broader cognitive-support framing from sensemaking literature

Limitations:
- some practitioner workflow signals still need deeper direct-source extraction
- notebook/memory-augmented RE remains conceptually important but still under-collected as a dedicated subtopic
- more evidence is needed on domain-specific workflow variation

Overall assessment:
- this topic is mature enough to serve as the workflow spine of V1 of the KB

## 13. Topic summary
Analyst workflows and human–LLM teaming form the human-centered spine of the reverse-engineering expert KB.

This topic matters because expert reverse engineering is not just about producing artifacts; it is about moving through uncertainty, preserving evidence, choosing the right next action, and using assistance systems without sacrificing trust or cognitive stability.