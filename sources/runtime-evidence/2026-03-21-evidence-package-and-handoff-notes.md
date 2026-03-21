# Evidence-package and handoff notes for runtime-evidence workflows

Date: 2026-03-21
Topic: runtime evidence / evidence packaging / analytic provenance / handoff discipline
Purpose: source-backed practical notes for turning one already-good runtime result into a reusable evidence package instead of leaving it trapped in replay UIs, screenshots, or analyst memory

## Why this note exists
The runtime-evidence branch already had practical notes for:
- choosing a truthful runtime surface
- deciding when replay or execution history is worth the cost
- choosing one representative execution and one first trace anchor
- designing a useful compare pair and isolating one first meaningful divergence
- walking backward from one late effect toward one causal boundary

What remained thinner was the next recurring operator problem:
- one runtime result is already technically good enough
- but it is still scattered across replay files, screenshots, query history, scratch notes, and remembered context
- another analyst, or future-you after a delay, would have to partially rediscover the proof

This note therefore focuses on a narrower question than broad provenance theory:
- how to package one runtime result so it survives delay, scrutiny, and branch-specific reuse

## Sources consulted

### SensorRE dissertation page
URL:
- https://scholar.afit.edu/etd/3882

Useful signals:
- SensorRE is framed as an analytic provenance tool for software reverse engineers.
- It automatically captures sensemaking actions and provides graph and storyboard views.
- The stated value is not merely logging activity, but helping users keep context inside a broad reverse-engineering task.

Practical extraction:
- packaging should preserve analyst context around the proof path, not just raw artifacts
- graph/storyboard style thinking suggests an evidence package should remember sequence and relation, not only isolated screenshots

### Provenance Ninja thesis page
URL:
- https://scholar.afit.edu/etd/7028

Useful signals:
- Provenance Ninja moved provenance capture directly into Binary Ninja, improving runtime and memory behavior over a more server/browser-heavy setup.
- The thesis frames accessibility and efficiency as major constraints for provenance support in reverse engineering.

Practical extraction:
- a usable package must be cheap enough to produce during real analysis, not only in idealized provenance systems
- packaging discipline should fit analyst workflow inside the reversing environment instead of assuming a separate heavy reporting pass

### reAnalyst paper (arXiv HTML)
URL:
- https://arxiv.org/html/2406.04427v2

Useful signals:
- reAnalyst is explicitly tool-agnostic and combines screenshots, keystrokes, active processes, active windows, and other machine-level observations.
- The paper argues that one-off interviews and reports are incomplete and imprecise compared with time-stamped activity evidence.
- It also highlights that manual annotation does not scale and that useful reuse depends on semiautomated structure.

Practical extraction:
- a strong runtime package should preserve more than one modality when needed: not only image slices, but also process/window/query/run context
- observation timestamps and event ordering matter because they preserve why the claim was trusted
- packaging should minimize manual rediscovery by imposing structure at the moment the claim is fresh

### reAnalyst repository README
URL:
- https://github.com/csl-ugent/reAnalyst

Useful signals:
- the framework explicitly separates image data, non-image data, OCR, function matching, and basic-block matching.
- the repository description treats screenshot analysis and non-visual logs as complementary, not interchangeable.

Practical extraction:
- runtime packages should not pretend that one artifact type is enough for every handoff
- the minimum useful package often combines one image-like slice with one non-image anchor such as run label, event family, address, query, or consumer path

### Binary Ninja workflows documentation
URL:
- https://docs.binary.ninja/dev/workflows.html

Useful signals:
- workflows are treated as DAGs of activities with explicit dependencies, execution order, and roles.
- the docs repeatedly emphasize bounded activities, dependencies, and composition rather than undifferentiated pipelines.

Practical extraction:
- evidence packaging should be treated as a bounded workflow stage after proof, not as an endless reporting tail
- a good package should preserve dependency order: observed event -> inferred consequence -> downstream consumer

## Lower-confidence / partial-use signals

### DTIC PDF fetch for the SensorRE dissertation
URL:
- https://apps.dtic.mil/sti/trecms/pdf/AD1108805.pdf

Status:
- direct fetch degraded to raw PDF bytes in this environment

Usefulness:
- metadata only; not used as a quote-bearing source

## Working synthesis
A strong runtime-evidence package preserves six things explicitly:

1. **claim boundary**
   - what exactly is proved, and no more
2. **run boundary**
   - which exact run, compare pair, replay artifact, or execution label produced the proof
3. **anchor boundary**
   - which timestamp, event family, watchpoint, address range, callback, or query returns the analyst to the decisive moment
4. **evidence slices**
   - the minimum before/after, upstream/downstream, or observed/consequence artifacts that justify the claim
5. **observation vs inference split**
   - what was directly seen versus what is being inferred from it
6. **next consumer**
   - which narrower task, page, analyst, or branch-specific proof this package is supposed to support

The package is weak if it preserves only artifacts.
It is strong when it preserves the recovery path to those artifacts.

## Operator implications

### 1. Preserve sequence, not just evidence blobs
The SensorRE graph/storyboard framing suggests that analysts often lose value not because data vanished, but because the ordering and relationship among events became implicit.

Practical implication:
- store one minimal sequence such as:
  - trigger or setup anchor
  - decisive write / divergence / callback / state edge
  - downstream consequence slice

### 2. Prefer multimodal minimums over single-modality dumps
reAnalyst’s structure suggests that screenshots alone and raw logs alone each underdescribe the proof.

Practical implication:
- prefer a small mixed package such as:
  - one screenshot or decompiler slice
  - one run label / replay id / query
  - one address or function anchor
  - one short explanation of why this slice matters

### 3. Package at the moment the claim becomes trustworthy
Both provenance-oriented systems and reAnalyst-style annotation pressure point to the same rule:
- late packaging causes rediscovery and overclaim

Practical implication:
- package immediately after the first trustworthy divergence or causal edge is found, before the analyst starts widening the story

### 4. Treat package creation as a workflow stage with a stop rule
The workflow/DAG framing is useful because packaging should be bounded.

Practical implication:
- stop packaging when the package can answer:
  - what is proved?
  - where is it proved?
  - how do I revisit it?
  - what remains open?
  - what next task is it for?

### 5. Make branch-specific reuse explicit
A runtime package is highest value when it is prepared for one next consumer.

Examples:
- native route-to-state continuation
- protocol parser-to-state continuation
- malware reporting/handoff package
- protected-runtime integrity or handler-owned-transfer continuation
- notebook/provenance system update

## Package template worth preserving in the KB
A minimal package template emerging from these sources is:

```text
Claim:
- one exact statement of what the runtime result proves

Run / compare context:
- run labels, replay artifact, environment fact, trace id

Anchors:
- timestamp / event id / address / callback / query / watchpoint

Observed:
- the direct evidence slices

Inferred:
- the bounded explanation supported by those slices

Still open:
- what remains plausible but unproved

Next consumer:
- which narrower task or page this package supports next
```

## KB implication
The runtime-evidence branch should preserve a distinct practical continuation note for:
- turning one already-good runtime result into a reusable package
- separating observation from inference
- recording the exact anchors that make the claim re-findable
- handing the package to one next consumer rather than widening into archive growth

That is the practical gap this source pass supports.
