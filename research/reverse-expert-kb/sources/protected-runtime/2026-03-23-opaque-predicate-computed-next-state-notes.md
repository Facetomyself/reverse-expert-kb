# Opaque-Predicate / Computed-Next-State Research Notes

Date: 2026-03-23 10:18 Asia/Shanghai / 2026-03-23 02:18 UTC
Focus: practical continuation for flattened protected runtimes where the dispatcher is recognizable but the next-state relation is still obscured
Related pages:
- `topics/opaque-predicate-and-computed-next-state-recovery-workflow-note.md`
- `topics/protected-runtime-practical-subtree-guide.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`

## Source set retained
- eShard / D-810 control-flow unflattening write-up
  - `https://eshard.com/posts/D810-a-journey-into-control-flow-unflattening`
- synthesis.to flattening-detection write-up
  - `https://synthesis.to/2021/03/03/flattening_detection.html`
- Tigress `Flatten` documentation
  - `https://tigress.cs.arizona.edu/transformPage/docs/flatten/index.html`
- Tigress `AddOpaque` documentation
  - `https://tigress.wtf/addOpaque.html`
- raw multi-source search artifact
  - `sources/protected-runtime/2026-03-23-opaque-predicate-computed-next-state-search-layer.txt`

## High-signal findings

### 1. There is a real middle stage between “dispatcher found” and “state edge reduced”
The strongest cross-source confirmation from Tigress docs + eShard’s D-810 write-up is that practical unflattening often stalls after the easy win:
- the dispatcher is already obvious
- one state carrier is already visible
- but the next-state relation is still not directly readable because the state write is hidden behind helper reduction, opaque compare structure, flag-derived branching, copied-code inflation, or computed target selection

This validates keeping a dedicated workflow note for this middle stage instead of collapsing it directly into broad dispatcher/state-edge reduction.

### 2. Dispatch form changes the right recovery object
Tigress explicitly preserves several dispatch families:
- `switch`
- `goto`
- `indirect`
- `call`

Operational implication:
- `switch` often favors state-to-case / OBB mapping first
- `indirect` often favors table-index or target-family recovery first
- `call` often favors arg-struct / shared-state field recovery first

So the practical question is not merely “what is the state variable?” but “what is the smallest stable next-state carrier in this dispatch family?”

### 3. Opaque-next-state obfuscation is a first-class transformation, not incidental noise
Tigress explicitly documents:
- `--FlattenObfuscateNext`
- `--FlattenConditionalKinds=compute`
- `--FlattenConditionalKinds=flag`

That matters because it means common real-world flattening cases can deliberately separate:
- visible dispatcher structure
- from straightforward successor-state recovery

This supports a KB workflow that tells the analyst to normalize one next-state relation first, rather than trying to beautify the whole flattened CFG immediately.

### 4. AddOpaque-style copied-code inflation creates false branch importance
Tigress `AddOpaque` examples reinforce a recurring field reality:
- many visible branches are intentionally duplicated, copied, or bogus
- the practical recovery object is often one reduced helper output, one normalized compare family, or one actual state write bucket
- not every visible branch is equally important to the business-relevant successor relation

This is exactly the situation where branch normalization should come before full predicate simplification.

### 5. D-810’s workflow strongly supports helper-output / backward-tracking recovery
The eShard D-810 write-up highlights three repeatedly useful ingredients:
- backward variable tracking
- microcode emulation
- microcode control-flow patching

The practical lesson for the KB is narrower than “use microcode APIs”:
- when state writes are obscured, the stable recovery object is often the helper output or dependency slice feeding the dispatcher input
- backward dependency recovery plus narrow emulation can be enough to recover one trustworthy successor relation without fully solving the whole function

### 6. Flattening detection and flattening recovery are different tasks
The synthesis.to article is helpful mostly as a control point:
- it cleanly reinforces that a flattened region behaves like a state machine centered on a dispatcher
- but practical recovery still requires following state transitions and connecting them to real blocks or later effects

That distinction matters for the KB because analysts can otherwise mistake “I can detect flattening” for “I can already recover the next useful state edge.”

## Practical continuation rules worth preserving

### A. Ask the blocked successor question explicitly
Good practical forms:
- “from this OBB, which successor states are genuinely possible before dispatcher re-entry?”
- “is the computed index itself the state carrier, or only a later dispatch artifact?”
- “which helper output determines the next-state write?”

### B. Normalize by role before solving exact semantics
Useful labels:
- copied-code / branch inflation
- helper reduction
- state write candidate
- table-index computation
- dispatcher re-entry

This reduces the risk of spending the whole pass naming opaque branches that are not actually state-driving.

### C. Prefer one trustworthy successor relation over whole-function cleanup
The sources support a narrower operator target:
- one OBB/state mapping
- one two-way successor split
- one normalized condition family
- one table-index -> target-family relation
- one patch-worthy dispatcher-return edge

### D. Stop broad flattening work once one calmer downstream target exists
Once one successor relation is trustworthy, the next best step is often outside the flattened core:
- outer consumer proof
- narrower state-edge reduction
- patch/IL repair
- calmer static helper cleanup

## What changed in my view after this run
Before the run, the workflow note already captured the middle-stage idea.
After the run, the stronger source-backed refinements are:
- dispatch family should be treated as a routing choice for the recovery object, not just descriptive taxonomy
- copied-code / bogus-branch inflation should be treated as a normalization problem before full predicate solving
- helper-output anchoring deserves stronger emphasis because it matches real unflattening workflows better than “understand the whole block”
- the bridge note is justified not just conceptually, but by concrete Tigress options and D-810-style recovery practice

## Conservative limits
- This source set was strong enough for workflow improvement, not for claiming a universal deobfuscation algorithm.
- The practical guidance should remain case-driven and operator-focused, not drift into grand claims about full generic unflattening.
- Search hits beyond the retained source set included lower-signal or repetitive flattening references, so only the strongest practical distinctions were kept.