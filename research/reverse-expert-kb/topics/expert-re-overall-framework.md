# Overall Framework for a Reverse Engineering Expert Knowledge Base

## Purpose
This page defines the intended final shape of the reverse-engineering expert knowledge base.

The KB is **not** meant to be only:
- a tool list
- a paper digest collection
- a benchmark directory
- a malware-analysis note dump
- a decompiler comparison sheet

Instead, it should become a structured knowledge system for answering a harder question:

> What does expert reverse engineering actually consist of, and how should that knowledge be organized, evaluated, and extended over time?

## Core claim
Expert reverse engineering is not one task.
It is a **sensemaking discipline** built around recovering the right next trustworthy object under uncertainty.

That object might be:
- readable code structure
- function boundaries and signatures
- symbols, names, and types
- runtime behavior
- protocol fields or state transitions
- peripheral / MMIO / hardware context
- evidence that a hypothesis is wrong

This is why a useful KB should not be organized only by tools or only by binary format.
It should be organized around:
- **what is being recovered**
- **what the analyst needs next**
- **how the workflow progresses**
- **what constraints shape the domain**
- **how usefulness should be evaluated**

## What "expert" means here
For this KB, "expert reverse engineering" does not simply mean:
- using expensive tools
- knowing many shortcuts
- reading assembly quickly
- solving CTF-style toy problems

It means being able to:
- form useful hypotheses early
- choose the right layer of inspection
- recover the next decision-relevant object efficiently
- manage uncertainty without collapsing into false confidence
- externalize findings so analysis remains stable over long time horizons
- use static and dynamic methods in the right sequence
- understand when environment reconstruction matters more than code readability
- detect when a recovered artifact is helpful, misleading, incomplete, or not yet trustworthy

## Top-level model
A reverse-engineering expert KB should be built around five top-level questions.

### 1. What is the analyst trying to recover?
This is the **object-of-recovery** axis.

Examples:
- code structure
- semantics / intent
- names and symbols
- types and struct layouts
- function signatures and call shapes
- runtime behavior and trace evidence
- protocol fields and message semantics
- state machines
- peripheral maps / MMIO usage
- environment assumptions needed for rehosting or experimentation

### 2. What does the analyst need to trust next?
This is the **decision-support** axis.

Expert reverse engineering often progresses by restoring the next thing that is trustworthy enough to guide the next move.

Examples:
- a decompilation that is semantically good enough to orient
- a function name that is good enough to cluster behavior
- a type/layout that is good enough to navigate cross-references
- a dynamic trace that is good enough to reject a wrong hypothesis
- a protocol-field inference that is good enough to fuzz or classify traffic
- a peripheral map that is good enough to rehost or emulate firmware

This axis is more faithful to real analyst work than a flat “static vs dynamic” split.

### 3. How does expert workflow progress?
This is the **workflow / sensemaking** axis.

A recurring model now emerging from the collected material is:
- overview / orientation
- subcomponent scanning
- hypothesis formation
- focused experimentation
- evidence capture and externalization
- model revision
- repetition until the target is stable enough to answer the analyst’s real question

This means the KB should treat reverse engineering as a staged process rather than a bag of tactics.

A practical extension now worth preserving is that domain families also tend to stabilize into their own recurring **operator ladders** once a reader has chosen the right branch. In other words, the KB should not stop at broad phase language such as orientation, hypothesis formation, and focused experimentation. It should also preserve the smaller branch-local question:
- what is the next narrower trustworthy boundary for this kind of target?
- what proof should come before branch expansion?
- when should the analyst leave broad reading and continue into the next specific bottleneck family?

### 4. What constraints define the domain?
This is the **domain-constraint** axis.

Different subdomains are not just different file types. They impose different analysis constraints.

Examples:
- obfuscation changes what remains matchable or trustworthy
- mobile targets shift value toward runtime instrumentation and access strategy
- firmware targets shift value toward environment and hardware-context recovery
- protocol RE depends on message/session/state structure, not just binary lifting
- anti-tamper targets force stealth, resilience, and partial observability concerns

### 5. How should usefulness be evaluated?
This is the **evaluation** axis.

A method is not good merely because it produces output.
The output must support real analysis.

Useful evaluation dimensions across topics include:
- correctness
- coverage
- trustworthiness
- false-positive burden
- robustness under optimization / obfuscation / change
- operational cost
- time-to-answer
- downstream workflow payoff
- transferability across domains

## Stable top-level KB modules
The final KB should likely converge on the following module structure.

### Module A. Foundations
Purpose:
- define what expert reverse engineering is
- define the core framework of this KB
- establish shared vocabulary
- explain how different topic families relate

This page belongs to that module.

### Module B. Objects of recovery
This module should answer:
- what kinds of artifacts analysts try to reconstruct
- how these recovery objects differ
- which ones are local vs global in effect
- which ones are usually prerequisites for others

Likely subtopics:
- decompilation and code reconstruction
- symbol recovery
- type recovery
- signature recovery
- runtime behavior recovery
- protocol and state recovery
- firmware context recovery

### Module C. Workflow and sensemaking
This module should answer:
- how expert analysts move from uncertainty to confidence
- when they switch between static and dynamic modes
- how they externalize hypotheses and evidence
- where tools help or harm cognitive stability

Likely subtopics:
- observational studies of reverse engineers
- workflow/sensemaking models
- notebook / memory-augmented RE
- visualization / immersive support
- human-LLM teaming

### Module D. Domain families
This module should answer:
- what changes across subdomains
- which constraints dominate in each domain
- which forms of evidence matter most per domain

Likely subtopics:
- native binaries
- obfuscated / packed / protected binaries
- mobile reversing
- firmware / embedded reversing
- protocol reverse engineering
- malware-analysis overlaps
- anti-tamper / anti-cheat style targets

A practical reading that now deserves to be preserved more explicitly at the framework layer is:
- **native baseline** is the ordinary readable-code comparison case where analysts often reduce uncertainty by stabilizing one semantic anchor, proving one representative interface-to-state route, reducing one loader/provider ownership chain, and then localizing one async callback or event-loop consumer
- **protected-runtime** is the resistance-heavy case where observation topology, trace reduction, packed/bootstrap handoff, artifact-consumer proof, runtime-obligation recovery, and integrity/tamper consequence become the defining bottlenecks
- **mobile** is the environment- and ownership-distributed case where observation topology, trust path, mixed-runtime ownership, response-side consequence, and challenge-loop closure often dominate earlier than broad static reading
- **protocol / firmware** is the boundary- and state-recovery case where capture relocation, smaller-contract recovery, parser/state consequence, replay acceptance, reply/output, and hardware-side effect proof often dominate before broad semantic narration becomes useful
- **malware overlaps** are the consequence-first and handoff-heavy cases where first staged consequence, config-to-capability reduction, first outbound-family proof, gate localization, and evidence packaging often matter more than broad taxonomy

### Module E. Evaluation framework
This module should answer:
- how to compare tools, benchmarks, datasets, and workflows
- which metrics reflect analyst value
- which benchmarks are intrinsic vs downstream
- how to distinguish training corpora from evaluation benchmarks

Likely subtopics:
- benchmark families
- reproducibility and ground truth quality
- robustness-oriented evaluation
- analyst-centric evaluation
- downstream-utility evaluation

### Module F. Human-tool-LLM collaboration
This module should answer:
- where LLMs actually help in RE
- where they create workflow hazards
- how tool integration changes usefulness
- how trust calibration and evidence preservation should work

Likely subtopics:
- MCP/disassembler integration patterns
- context management and retrieval
- human verification burden
- novice vs expert benefit differences
- artifact drafting vs semantic overclaim risk

## Proposed canonical cross-topic distinctions
To keep the KB coherent, several distinctions should be used consistently.

### 1. Readability vs trustworthiness
Something can look readable while being unsafe to trust.
This matters for decompilation, naming, summarization, and LLM assistance.

### 2. Static recoverability vs runtime answerability
Some questions are cheaper to answer dynamically than statically.
This is especially important in mobile, firmware, and protected targets.

### 3. Intrinsic accuracy vs downstream utility
A method may score well intrinsically yet fail to reduce analyst time or error.
Conversely, a partial method may be very useful if it helps the next decision.

### 4. Recovery quality vs false-positive burden
A noisy method can be worse than a lower-coverage method if it creates misleading anchors.
This matters strongly in symbol recovery, protocol inference, and firmware context modeling.

### 5. Nominal benchmark score vs robustness
A method may perform well on static datasets but collapse under obfuscation, optimization, version drift, or anti-analysis conditions.

### 6. Local artifact improvement vs global workflow impact
A result that improves one function locally may or may not improve program-level navigation and understanding.

## A unifying evaluation schema
Across topics, the KB should prefer evaluating work using the following common dimensions.

### Correctness
Is the recovered artifact actually right?

### Coverage
How much of the relevant target can be recovered usefully?

### Trustworthiness
How often does the method produce analyst-misleading output?
How well calibrated is uncertainty?

### False-positive burden
How expensive are wrong guesses in analyst time and cognitive disruption?

### Robustness
Does the method continue to work under optimization, obfuscation, platform drift, version changes, or adversarial transformations?

### Operational cost
What are the runtime, hardware, environment, setup, and tooling requirements?

### Workflow payoff
Does the method help the analyst reach a better next question or faster next decision?

### Downstream utility
Does the method improve rehosting, fuzzing, clustering, triage, vulnerability discovery, patch diffing, or long-horizon understanding?

### Transferability
Do the ideas and metrics generalize across desktop, mobile, firmware, protocol, and protected-target settings?

## Current topic pages and where they fit
### Foundations / overall shape
- `topics/expert-re-overall-framework.md`

### Evaluation-oriented topics
- `topics/benchmarks-datasets.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/symbol-type-and-signature-recovery.md`

### Domain / context topics
- `topics/native-binary-reversing-baseline.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`

### Workflow / human-support topics
- `topics/analyst-workflows-and-human-llm-teaming.md`

## What a V1 should look like
A reasonable V1 of this KB should include:
- one stable foundations page
- one explicit global map of topic relationships
- one shared evaluation schema used across topic pages
- 8–12 mature topic pages
- clear distinction between:
  - raw source notes
  - run reports
  - topic syntheses
  - canonical framework pages
- enough cross-linking that readers can move from one topic family to its dependencies and contrasts

## What could go wrong if structure is not enforced
Without deliberate structure, this KB risks becoming:
- a growing pile of good notes with no canonical synthesis
- repetitive hourly reports that restate similar insights
- topic pages with incompatible vocabularies
- a benchmark directory without workflow relevance
- a workflow discussion disconnected from concrete recovery objects

That is why canonical framework pages are necessary.

## Immediate next steps
1. Add a global map / ontology page linking all current topic families.
2. Normalize current topic pages to a shared template.
3. Add explicit cross-links among topic pages.
4. Separate source-note conventions from topic-synthesis conventions.
5. Define V1 maturity criteria per topic.
6. Continue hourly runs, but shift them toward filling structural gaps rather than only broadening coverage.

## Bottom line
The final form of this project should be:

> a structured knowledge system for understanding how expert reverse engineering works, what it tries to recover, how progress is made under uncertainty, how tools and LLMs help or hurt, and how analyst-relevant value should actually be measured.

That is more ambitious than a paper summary archive, but it is also far more useful.