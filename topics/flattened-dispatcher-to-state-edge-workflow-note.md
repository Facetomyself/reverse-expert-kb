# Flattened Dispatcher to State-Edge Workflow Note

Topic class: concrete workflow note
Ontology layers: deobfuscation practice branch, protected-runtime overlap, consequence-localization workflow
Maturity: structured-practical
Related pages:
- topics/obfuscation-deobfuscation-and-packed-binaries.md
- topics/anti-tamper-and-protected-runtime-analysis.md
- topics/vm-trace-to-semantic-anchor-workflow-note.md
- topics/trace-slice-to-handler-reconstruction-workflow-note.md
- topics/jsvmp-and-ast-based-devirtualization.md
- topics/native-interface-to-state-proof-workflow-note.md

## 1. Why this page exists
This page exists because the KB still had a practical gap inside the deobfuscation branch.

The KB already had:
- a mature synthesis page for obfuscation / deobfuscation / packed targets
- a practical note for VM trace -> semantic-anchor reduction
- a practical note for trace-slice -> handler reconstruction
- a browser-side page for JSVMP and AST-based devirtualization

What it still lacked was a smaller operator playbook for a recurring middle-state problem:

```text
flattened or dispatcher-heavy logic is already visible
  + the analyst already has some static foothold or narrow trace
  + full handler/opcode reconstruction is still too expensive
  -> identify the first durable state edge that predicts later behavior
```

This is not the same as:
- finding the dispatcher
- making the decompiler output prettier
- building a full handler catalog first
- fully reconstructing the VM model first

It is the practical task of turning dispatcher recognition into one consequence-bearing state transition that can guide the next move.

## 2. Target pattern / scenario
### Representative target shape
Use this note when most of the following are true:
- control-flow flattening, switch-dispatch churn, or VM-like handler routing is already visible
- static structure is partially readable but still too repetitive or distorted to trust directly
- a trace slice, compare-run, or runtime-guided foothold already exists, but it still feels too noisy
- the analyst now needs to know which state update, helper output, or dispatcher-exit family actually predicts the later effect
- the practical bottleneck is no longer “where is the dispatcher?” but “which state edge matters first?”

Representative cases include:
- OLLVM-style flattened regions where the dispatcher is obvious but the decisive state update is not
- native or mobile VMP-like loops where several handler families are visible but only one state object predicts later behavior
- browser JSVMP cases where dispatcher and handlers are known in outline, but the first durable policy/object update is still hidden behind helper churn
- protected native loops where the decompiler shows many synthetic blocks yet the first meaningful scheduler/mode/state transition remains unclear

### Analyst goal
The goal is **not** to understand the entire flattened machine at once.
It is to:
- isolate one durable state object, state slot, reduction helper, or dispatcher-exit family
- localize the first consequence-bearing state edge downstream from dispatcher churn
- prove one later effect depends on that edge
- hand back one smaller static target for careful reconstruction

## 3. The first five questions to answer
Before broadening the analysis, answer these:

1. **What late effect do I actually care about?**
2. **Which dispatcher window is the narrowest one that still precedes that effect?**
3. **What could count as the first durable state object here: slot, enum, object, table selector, or scheduler flag?**
4. **Is there a helper that reduces many transient handler effects into that smaller state?**
5. **What static target do I want back from this pass: one helper, one state slot, one dispatcher-exit bucket, or one state-write site?**

If these remain vague, the workflow usually collapses into repeated dispatcher reading without payoff.

## 4. Core claim
In flattened or dispatcher-heavy targets, the first useful milestone is often **not** full handler recovery.
It is the first durable state edge.

A practical sequence is:

```text
dispatcher churn
  -> role-labeled helper/handler regions
  -> durable state object or reduction helper
  -> first consequence-bearing state edge
  -> one proved downstream effect
  -> smaller next static target
```

The state edge matters because it reconnects transformed control flow back to ordinary reasoning about mode, policy, scheduler, ownership, or request shaping.

## 5. What counts as a durable state object
A durable state object is the smallest repeated thing that predicts later behavior better than raw dispatcher churn does.

Good candidates include:
- one state slot/register/field reused across several dispatcher iterations
- one local object or struct populated in pieces and then consumed later
- one enum or mode bucket selected by a reduction helper
- one scheduler flag / queue token / phase marker
- one dispatcher-exit family that consistently feeds ordinary business logic

Bad candidates are usually:
- the entire flattened region as one blob
- a giant handler list with no downstream consequence label
- guessed opcode semantics that are not tied to later effects
- a beautified CFG that still does not predict behavior

## 6. Practical workflow

### Step 1: anchor one late effect first
Start from a visible effect such as:
- allow / degrade / block behavior
- request family emitted or suppressed
- scheduler branch present or absent
- one follow-up callback or state machine phase starting
- one normalized object or policy bucket becoming visible

Good scratch note:

```text
late effect:
  retry phase never starts in failed run

working question:
  which dispatcher-side state edge first predicts that absence?
```

### Step 2: cut one narrow dispatcher window
Choose the smallest window that still contains:
- one relevant entry into the dispatcher / flattened region
- one likely reduction helper or repeated handler subset
- one later consequence boundary

Typical window boundaries:
- first dispatcher entry after a user/request trigger
- one loop interval immediately before a policy/state object is consumed
- one compare-run window immediately before a scheduler or request-family split
- one replay/trace segment ending at the first ordinary branch outside the flattened region

If the window contains many retries, unrelated loops, or many side paths, it is probably too broad.

### Step 3: label regions by role before exact meaning
Before naming detailed semantics, reduce the window into role labels such as:
- dispatcher churn
- transient handler bucket A / B / C
- reduction helper
- state accumulation object
- first durable state write
- consequence consumer

Example reduction:

```text
region A = repetitive switch dispatcher and state-index updates
region B = small helper family repacking handler outputs into a local object
region C = first durable write to phase/mode field
region D = outer consumer branch that decides request/scheduler path
```

That is already more useful than another raw flattened CFG.

### Step 4: force one state-object choice
Choose the smallest repeated thing that now looks predictive.
Typical choices:
- one slot/field whose value family differs only when behavior changes
- one helper output object that is consumed outside the dispatcher
- one dispatcher-exit family that always precedes the later effect
- one mode enum or flag that compresses many handler-level operations into one operational state

Practical rule:
- prefer objects that reconnect well to static cleanup, watchpoints, xrefs, or compare-runs later

### Step 5: localize the first consequence-bearing state edge
Ask:

```text
what is the first write / reduction / branch downstream from this state object
that actually changes later behavior?
```

Typical answers:
- first durable flag write
- first enum selection
- first scheduler enqueue/suppress decision
- first request-family selector
- first ownership/phase transition
- first reduction from many transient handler values into one operational mode

Do not stop at “this helper seems important.”
Push to the first state edge that predicts a later effect.

### Step 6: prove one downstream effect
Use one narrow proof move such as:
- compare-run alignment at the same state-object boundary
- watchpoint on the chosen field or object write
- one hook on the first outer consumer of that state
- reverse-causality from the visible late effect back to that state edge
- one controlled input variation that changes only the anchored path

The goal is not complete system validation.
It is one proof that:
- the chosen state object is real
- the chosen state edge matters
- one later effect depends on it

### Step 7: hand back one smaller static target
The workflow should end with one or more of:
- one helper worth careful pseudocode cleanup
- one state object / field worth renaming
- one dispatcher-exit bucket worth deeper reconstruction
- one outer consumer branch worth precise decompilation
- one justified quieter watchpoint / hook candidate

If the result is only a better-looking dispatcher map, the reduction is incomplete.

## 7. Common state-edge families

### A. Reduction-helper -> mode/enum edge
Use when:
- many handlers feed one smaller mode/enum/object
- later behavior depends on that smaller output, not on every handler separately

Why it helps:
- it collapses a broad flattened region into one interpretable operational bucket

### B. State-slot -> scheduler edge
Use when:
- the first meaningful change is whether a timer, retry, queue, or phase transition happens

Why it helps:
- scheduler decisions often predict later behavior better than dispatcher internals do

### C. Dispatcher-exit -> consumer edge
Use when:
- the flattened region ends by returning into ordinary code
- the real leverage point is the first outer consumer branch

Why it helps:
- it provides a clean bridge back into ordinary static analysis

### D. Compare-run state-edge divergence
Use when:
- accepted and failed runs share most dispatcher churn
- one smaller difference appears in object shape, mode, or field value

Why it helps:
- it turns a broad flattened trace into one inspectable state question

## 8. Representative scratch schemas

### Minimal dispatcher-to-state-edge note
```text
effect of interest:
  ...

window boundary:
  start = ...
  stop = ...

role-labeled regions:
  A = ...
  B = ...
  C = ...

chosen state object / helper:
  ...

first consequence-bearing state edge:
  ...

next static target:
  ...
```

### Compare-run state-edge note
```text
baseline state object:
  ...
failed-run state object:
  ...

first stable divergence:
  ...

first downstream effect difference:
  ...
```

### Tiny thought model
```python
class DispatcherStateEdgeReduction:
    effect = None
    window = None
    regions = None
    state_object = None
    consequence_edge = None
    next_static_target = None
```

## 9. Failure modes

### Failure mode 1: dispatcher understood better, but nothing becomes easier
Likely cause:
- too much energy spent on handler cataloging before forcing a state object / state edge choice

Next move:
- choose one field/object/exit-family and force a downstream effect question

### Failure mode 2: helper identified, but consequence still vague
Likely cause:
- the helper was named but not connected to the first durable write or outer consumer

Next move:
- push one step further to the first write / branch / scheduler edge after the helper

### Failure mode 3: compare-runs differ almost everywhere
Likely cause:
- window begins too early
- observation distortion or environment drift dominates

Next move:
- move the window closer to the late effect
- use quieter observation
- revisit observation-distortion or environment-differential notes when needed

### Failure mode 4: state object chosen, but static follow-up still sprawls
Likely cause:
- the result was not forced into one target class

Next move:
- rewrite the output as exactly one of:
  - helper
  - state field/object
  - dispatcher-exit bucket
  - outer consumer branch
  - watchpoint candidate

## 10. How this page connects to the rest of the KB
Use this page when the bottleneck is:
- **turning flattened/dispatcher-heavy logic into one consequence-bearing state edge and one smaller static target**

Then route outward based on what remains hard:
- if the target is still better framed as a broader deobfuscation/protected-runtime problem:
  - `topics/obfuscation-deobfuscation-and-packed-binaries.md`
  - `topics/anti-tamper-and-protected-runtime-analysis.md`
- if trace reduction itself is still the main issue:
  - `topics/trace-slice-to-handler-reconstruction-workflow-note.md`
- if the main problem is still finding a semantic anchor in VM churn:
  - `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- if the target is browser-side JSVMP or AST-hostile code:
  - `topics/jsvmp-and-ast-based-devirtualization.md`
- if the flattened region has already reduced into an ordinary interface/state question:
  - `topics/native-interface-to-state-proof-workflow-note.md`

## 11. What this page adds to the KB
This page adds a missing practical bridge in the deobfuscation branch:
- not full devirtualization first
- not giant handler catalogs first
- not prettier CFGs first

Instead it emphasizes:
- dispatcher-window reduction
- durable state-object selection
- first consequence-bearing state edge
- one downstream proof
- one smaller static target

That strengthens a relatively thin deobfuscation practical branch without drifting back into the already-dense browser/mobile branches.

## 12. Source footprint / evidence note
Grounding for this page comes from:
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- `topics/trace-slice-to-handler-reconstruction-workflow-note.md`
- `topics/jsvmp-and-ast-based-devirtualization.md`
- `sources/datasets-benchmarks/2026-03-14-obfuscation-benchmarks-source-notes.md`
- `sources/protected-runtime/2026-03-16-vm-trace-to-semantic-anchor-notes.md`
- `sources/protected-runtime/2026-03-16-flattened-dispatcher-to-state-edge-notes.md`
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`

The page intentionally stays conservative:
- it does not claim full handler recovery is usually the right first target
- it does not assume every flattened target has one clean VM model
- it treats dispatcher -> state-edge reduction as an analyst workflow for finding the next trustworthy object

## 13. Topic summary
Flattened dispatcher to state-edge reduction is a practical workflow for targets where the dispatcher is already visible but the first behavior-predicting state transition is still hidden behind handler churn.

It matters because analysts often do not need a full handler map first.
They need one durable state object, one consequence-bearing edge, and one proved downstream effect that turns flattened control flow into a smaller, more trustworthy static target.
