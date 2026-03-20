# V1 Roadmap and Maturity Criteria

## Purpose
This page defines what should count as Version 1 of the reverse-engineering expert knowledge base.

The goal is to prevent the project from growing indefinitely without a stable completion boundary.
A KB like this can always be expanded, but it still needs a meaningful point at which it becomes:
- coherent
- navigable
- internally consistent
- useful as a reference system rather than only as a research scratchpad

This page therefore answers five questions:
- what V1 is supposed to be
- what is already complete enough for V1
- what still needs to be true before V1 should be treated as operationally complete
- what should explicitly be deferred beyond V1
- how recurring maintenance should behave once the KB is no longer in obvious missing-page discovery mode

## What V1 is
V1 should be understood as:

> the first stable, structured, internally coherent version of the reverse-engineering expert KB, with enough framework, ontology, topic depth, and cross-topic consistency to function as a real knowledge system.

V1 is **not**:
- exhaustive coverage of all reverse-engineering subfields
- a finished book
- a complete benchmark census
- a fully mature ontology for every possible target class
- a frozen final theory of reverse engineering

It is the first version where the KB clearly demonstrates:
- a stable organizing framework
- a stable topic taxonomy
- consistent evaluation language
- real cross-topic navigation
- a meaningful distinction between framework pages, topic syntheses, source notes, and run reports
- enough parent-page and subtree-guide coherence that dense practical branches read like deliberate operator ladders rather than accidental note piles

## What V1 must contain
A V1-complete KB should contain at least the following layers.

### Layer 1. Framework layer
Required pages:
- `topics/expert-re-overall-framework.md`
- `topics/global-map-and-ontology.md`
- `topics/topic-template-and-normalization-guide.md`

Purpose:
- define what the KB is trying to model
- define how topics relate
- define how pages should converge structurally

### Layer 2. Cross-cutting core topic layer
Required pages:
- `topics/benchmarks-datasets.md`
- `topics/symbol-type-and-signature-recovery.md`
- `topics/analyst-workflows-and-human-llm-teaming.md`

Purpose:
- define how methods are evaluated
- define one key family of recovery objects
- define the workflow/sensemaking model that interprets the rest of the KB

### Layer 3. Domain-constraint layer
Required pages:
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`

Purpose:
- show how domain constraints alter reverse-engineering practice
- demonstrate that the KB is not only about generic stripped native binaries

### Layer 4. Gap declaration layer
Required outcome:
- explicit listing of what remains missing, thin, or only partially canonical

Purpose:
- avoid pretending the ontology is more complete than it is
- make future work legible
- distinguish true remaining gaps from stale descriptions of earlier missing-page pressure

## Current V1 status
The KB now appears to have completed the basic V1 skeleton.
The main remaining work is no longer the old missing-page phase.
It is now mostly about canonical synchronization, branch-balance maintenance, and selective deepening where a real operator gap still exists.

### Framework layer status
- `topics/expert-re-overall-framework.md` — present and near-canonical
- `topics/global-map-and-ontology.md` — present and near-canonical
- `topics/topic-template-and-normalization-guide.md` — present and canonical enough for ongoing normalization

Assessment:
- the framework layer is already strong enough for V1
- the real maintenance pressure here is synchronization rather than creation

### Cross-cutting core topic layer status
- `topics/benchmarks-datasets.md` — normalized and strong
- `topics/symbol-type-and-signature-recovery.md` — normalized and strong
- `topics/analyst-workflows-and-human-llm-teaming.md` — normalized and strong
- `topics/decompilation-and-code-reconstruction.md` — added and mature enough for V1
- `topics/runtime-behavior-recovery.md` — added and mature enough for V1
- `topics/notebook-and-memory-augmented-re.md` — added and mature enough for V1

Assessment:
- the core cross-cutting layer is already strong enough for V1
- the practical issue is now preserving cross-links and keeping canonical summaries honest about what already exists

### Domain-constraint layer status
- `topics/native-binary-reversing-baseline.md` — present and useful as the ordinary comparison case
- `topics/js-browser-runtime-reversing.md` — present and now supported by a dense browser practical subtree
- `topics/mobile-reversing-and-runtime-instrumentation.md` — normalized and strong
- `topics/firmware-and-protocol-context-recovery.md` — normalized and strong
- `topics/anti-tamper-and-protected-runtime-analysis.md` — present and supported by a dedicated protected-runtime practical subtree
- `topics/malware-analysis-overlaps-and-analyst-goals.md` — present and supported by a practical malware ladder

Assessment:
- the domain-constraint layer is already strong enough for V1
- several branches have matured beyond parent-page existence and now need to be treated as stable routed subtrees

## Earlier missing nodes now closed
The pages that previously represented obvious V1-closing gaps are now present.
They should no longer be narrated as active missing-page pressure.

### Former Priority 1 gaps now closed
- `topics/decompilation-and-code-reconstruction.md`
- `topics/runtime-behavior-recovery.md`
- `topics/notebook-and-memory-augmented-re.md`

### Former Priority 2 gaps now closed
- `topics/native-binary-reversing-baseline.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`

This matters because stale roadmap language is a real maintenance bug.
If this page still talks as if those nodes are missing, it teaches the wrong model of the KB’s current phase.

## What is still missing for a solid V1
V1 is close enough that the realistic remaining work is no longer “find the obvious top-level pages.”
The more important remaining tasks are canonical and structural.

### Priority 1 remaining work
These are the most important remaining V1-closing tasks.

#### 1. Canonical synchronization across framework surfaces
Required outcome:
- framework pages, ontology pages, index surfaces, parent pages, and subtree guides should describe the same branch reality

Why it matters:
- the KB already has more mature branch structure than some canonical surfaces admit
- stale framework summaries create avoidable branch drift
- users should not have to infer current branch maturity only from recent run reports

#### 2. Cross-link and branch-routing coherence
Required outcome:
- mature pages should route readers into the right subtree guides, parent pages, and neighboring continuations without depending on recent autosync memory

Why it matters:
- V1 should be navigable as a system, not merely searchable as a note pile
- dense branches need explicit stop rules and continuation rules to avoid repeated rediscovery

#### 3. Branch-balance maintenance
Required outcome:
- recurring work should notice when one branch is getting much denser than others and should prefer canonical repair, subtree-guide strengthening, or thinner high-value continuations instead of momentum-driven leaf growth

Why it matters:
- browser and mobile/practical branches now grow faster than thinner but still important branches
- V1 quality depends on balance and navigability, not just local density

### Priority 2 remaining work
These would strengthen V1 further, but are not strict blockers.

#### 4. Canonical status review for mature pages
Required outcome:
- decide which mature pages should now be treated as canonical anchors instead of merely mature leaves

Why it matters:
- some pages already function as reference anchors in practice
- making that status explicit reduces ambiguity about where future edits should converge

#### 5. Selective deepening of still-thin practical continuations
Required outcome:
- add new leaves only where there is a real operator gap visible across runs, not merely because a dense branch is easy to continue

Why it matters:
- post-V1 quality depends more on disciplined continuation than on raw page count
- branch balance is harmed by low-friction expansion in already-dense areas

## What can be deferred beyond V1
The following are valuable, but should not block V1.

### Possible V2+ expansions
- Android-specific deeper branch splitting beyond current practical ladders
- iOS-specific narrower continuations beyond the current ladder
- PAC / arm64e dedicated page
- fine-grained protocol benchmarking page
- firmware corpora and metadata page
- unpacking-readiness benchmark page
- LLM failure-mode taxonomy in RE
- domain-specific workflow studies per malware/mobile/firmware/browser family
- visual / immersive RE interfaces as their own dedicated page
- denser anti-cheat / trusted-runtime operator routing if that edge becomes a sustained branch

These are important but belong to later refinement once the KB’s first stable shape is in place.

## Shared maturity criteria
A page should be considered V1-ready if it satisfies all of the following.

### Structural criteria
- has a clear identity section
- declares ontology role
- declares maturity level
- follows the topic normalization structure reasonably well
- includes explicit cross-links to related pages

### Conceptual criteria
- makes at least one explicit core claim
- distinguishes itself clearly from adjacent topics
- explains what it enables for analysts
- includes workflow implications
- includes evaluation dimensions where relevant

### Evidence criteria
- grounded in more than one source or source family
- evidence quality is characterized honestly
- open questions are concrete and useful
- page is more synthesis than source accumulation

### KB-integration criteria
- page fits clearly into the ontology
- page is linkable from multiple other pages
- page helps clarify rather than duplicate neighboring topics
- page’s practical continuation rules are consistent with the current branch shape when it belongs to a mature subtree

## Shared maturity ladder for the KB
The KB can use the following global maturity labels.

### 1. Seed
- topic identified
- page exists or is planned
- little synthesis yet

### 2. Emerging
- several strong sources gathered
- topic boundaries becoming visible
- some structural claims visible

### 3. Structured
- page has clear organization
- ontology placement is clear
- meaningful open questions exist

### 4. Mature
- page supports cross-topic navigation well
- synthesis outweighs collection
- workflow and evaluation framing are explicit
- likely stable enough for V1

### 5. Canonical
- page acts as a reference anchor for a topic family
- later edits are mostly refinement, not reconceptualization
- page is stable enough to guide the rest of the KB
- nearby parent pages, subtree guides, and framework surfaces increasingly converge on it

## Current maturity snapshot
Approximate current status:

### Canonical or near-canonical framework pages
- `topics/expert-re-overall-framework.md`
- `topics/global-map-and-ontology.md`
- `topics/topic-template-and-normalization-guide.md`

### Mature or branch-anchor pages
- `topics/benchmarks-datasets.md`
- `topics/symbol-type-and-signature-recovery.md`
- `topics/analyst-workflows-and-human-llm-teaming.md`
- `topics/decompilation-and-code-reconstruction.md`
- `topics/runtime-behavior-recovery.md`
- `topics/notebook-and-memory-augmented-re.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/native-binary-reversing-baseline.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/js-browser-runtime-reversing.md`
- `topics/malware-analysis-overlaps-and-analyst-goals.md`

### Remaining high-priority V1 work
- canonical synchronization
- cross-link and routing cleanup
- branch-balance review rather than branch-count expansion

## V1 completion rule
The KB should count as V1-complete when all of the following are true:

1. The framework layer is stable.
2. The cross-cutting core topic layer is stable.
3. The domain-constraint layer is stable.
4. The earlier Priority 1 topic set is complete and normalized.
5. Cross-links between pages are sufficient that the KB can be navigated as a system.
6. Canonical surfaces describe current branch reality rather than stale missing-page pressure.
7. Recurring runs are no longer primarily discovering structure, but mostly maintaining coherence, branch balance, freshness, and selective high-value continuations.

Current assessment:
- Conditions 1–4 are satisfied.
- Condition 5 is substantially improved but still worth ongoing maintenance.
- Condition 6 is now an active maintenance target and should be checked regularly.
- Condition 7 appears to be the right operating target going forward.

That last shift matters.
V1 is not only about page count.
It is about whether the project has moved from structural exploration to structured extension and canonical upkeep.

## Operational guidance for the recurring autosync after this point
The recurring maintenance workflow should now emphasize post-missing-page discipline.

### Earlier phase behavior
- broad exploration
- discovering topic families
- sketching structure

### V1-closing behavior
- fill obvious missing nodes
- deepen primary-source coverage for already recognized pages
- improve cross-links and evidence quality
- reduce repeated rediscovery of already-known structure

### Current post-V1 behavior
- keep framework, ontology, index, parent pages, and subtree guides synchronized
- preserve branch-balance memory when one branch becomes much denser than peers
- prefer canonical repair when the real gap is stale summary language rather than missing content
- add specialized child topics only when there is a real operator gap
- maintain benchmark, literature, and source freshness without letting freshness work erase structural discipline
- treat run reports as temporary execution memory, not as a substitute for canonical pages

## Recommended near-term build order
The next best order is now:

1. canonical sync passes across framework / ontology / index / subtree surfaces
2. cross-link and metadata cleanup across mature pages
3. selective strengthening of thinner but strategically important continuations
4. new leaf pages only when recurring operator pressure clearly justifies them

This order preserves coherence because:
- sync prevents stale canonical guidance
- cleanup improves system navigability
- selective strengthening protects branch balance
- delayed leaf growth reduces momentum-driven overexpansion in already-dense areas

## What success looks like after V1
After V1, the KB should feel like:
- a navigable framework rather than a pile of notes
- a system with stable language
- a foundation for deeper topic splits
- a plausible substrate for future handbook writing, retrieval, or agent support
- a set of practical branches whose ladders are explicit enough that users do not need recent cron memory to navigate them

Users of the KB should be able to answer questions such as:
- what kind of reverse-engineering problem is this?
- what recovery object matters next?
- what benchmark family is relevant?
- what domain constraint is changing the workflow?
- what practical branch should I enter?
- what narrower trustworthy boundary should usually be reduced next?
- what kind of analyst support is likely to help?

## Bottom line
The KB is already past the “interesting research pile” stage.

Its V1 task is no longer mainly to close a few obvious missing pages.
It is to behave like a stable system:
- keep canonical surfaces honest
- preserve branch balance
- keep navigation coherent
- extend selectively when real operator pressure appears

That is the point at which V1 becomes genuinely stable rather than merely large.