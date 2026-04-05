# Opaque-Predicate and Computed-Next-State Recovery Workflow Note

Topic class: concrete workflow note
Ontology layers: deobfuscation practice branch, protected-runtime overlap, flattened-control-flow continuation
Maturity: structured-practical
Related pages:
- topics/obfuscation-deobfuscation-and-packed-binaries.md
- topics/protected-runtime-practical-subtree-guide.md
- topics/vm-trace-to-semantic-anchor-workflow-note.md
- topics/flattened-dispatcher-to-state-edge-workflow-note.md
- topics/record-replay-and-omniscient-debugging.md
- topics/native-semantic-anchor-stabilization-workflow-note.md

## 1. Why this page exists
This page exists because the KB already had practical notes for:
- noisy VM / trace churn where the first stable semantic anchor is still missing
- flattened dispatchers where the remaining bottleneck is reducing one visible state machine into one durable state edge

What it still lacked was a thinner continuation for a recurring, annoying middle case:

```text
flattening is already recognizable
  + some dispatcher / state object is already visible
  + the next-state logic is still hidden behind opaque predicates,
    copied-code branches, computed branch targets, or helper-mediated state writes
  -> recover one trustworthy next-state relation anyway
```

This case is common in OLLVM- and Tigress-shaped work and in practical unflattening attempts where:
- finding the dispatcher was the easy part
- naming every handler is unnecessary
- the real blocker is that the next state is not assigned in one trivial `mov state, imm` pattern

Without a note for this case, the KB jumps too quickly from:
- “find a semantic anchor”
- to “reduce the dispatcher into a durable state edge”

while under-describing the stubborn bridge step where the state edge exists, but is still obscured by opaque branch logic or computed/indirect next-state selection.

## 2. Target pattern / scenario
### Representative target shape
Use this note when most of the following are true:
- control-flow flattening or dispatcher-driven churn is already clearly present
- one candidate state variable, state object, or dispatcher family is already visible enough to name
- the practical bottleneck is now recovering successor state(s), not proving that a dispatcher exists at all
- direct pattern matching for next-state writes is brittle, incomplete, or misleading
- opaque predicates, copied-code branches, helper-reduced values, or computed jump targets are making the “real” successor relation ambiguous
- the analyst needs one trustworthy OBB/state mapping or one successor-edge proof before broader cleanup or patching

Representative cases include:
- OLLVM-style flattened functions where the state update is hidden behind arithmetic, condition splitting, or helper-mediated writes
- Tigress flattening with `--FlattenObfuscateNext`, `--FlattenConditionalKinds=compute`, or `--FlattenConditionalKinds=flag`
- AddOpaque-shaped branch inflation where obvious branches are not the same as business-relevant control decisions
- Binary Ninja / Miasm / angr unflattening work where the dispatcher is obvious but the next-state extractor keeps producing incomplete or noisy results

### Analyst goal
The goal is **not** to solve every opaque predicate or fully decompile the whole flattened machine.
It is to:
- classify how next-state computation is being obscured
- recover one smaller trustworthy successor relation anyway
- prove one OBB/state or state/successor edge that predicts later behavior
- hand back one calmer target for static cleanup, CFG repair, or downstream consequence proof

## 3. The first five questions to answer
Before widening analysis, answer these:

1. **What exact successor question is blocked right now: OBB -> next state, state -> OBB, or branch condition -> successor split?**
2. **Which next-state shape am I actually seeing: direct constant, helper-reduced value, compare-dependent split, computed-target table index, or copied-code/opaque branch inflation?**
3. **What is the smallest trustworthy state object available now: one variable, one helper output, one branch-normalized compare result, or one dispatcher-exit bucket?**
4. **What proof would be enough for progress: one successor edge, one two-way split, one OBB/state mapping, or one patch-worthy dispatcher-return replacement?**
5. **What should remain out of scope for this pass: full opcode naming, full CFG prettification, or every bogus branch?**

If these stay vague, the workflow usually degenerates into reading more flattened pseudocode without actually recovering the next move.

## 4. Core claim
When flattening is already known, the next practical milestone is often **not** “remove all opaque predicates.”
It is **recover one trustworthy next-state relation despite opaque predicates or computed-next-state machinery**.

A useful practical sequence is:

```text
recognizable dispatcher / state object
  -> classify how next-state computation is obscured
  -> choose one smaller trustworthy state carrier
  -> normalize one successor relation
  -> prove one OBB/state or state/successor edge
  -> decide whether CFG repair or deeper static cleanup is now worth it
```

The point is to recover a next move, not to win a purity contest against every obfuscation gadget in the function.

## 5. Common obscuration shapes for next-state recovery
### A. Direct state write hidden by helper reduction
Shape:
- many instructions feed a helper or temporary
- helper output is eventually written into the state variable or dispatcher input

Why it matters:
- the stable recovery object is often the helper output, not every upstream arithmetic step

### B. Branch-dependent two-successor split
Shape:
- a block has two real successors, but the split is wrapped in copied-code structure, flag extraction, or opaque compare noise

Why it matters:
- the useful recovery target is often the pair of successor states plus the branch-normalized condition family, not perfect source-level condition reconstruction

### C. Computed-next-state / table-index recovery
Shape:
- the next state is selected indirectly through arithmetic, table indexing, indirect goto/call, or flag-derived address computation

Why it matters:
- the useful object is often a reduced table/index relation or target family, not immediate constants

### D. Opaque-branch inflation around a stable state core
Shape:
- bogus or duplicated branches make the block look wider, but only one smaller subexpression or assignment family actually drives the successor state

Why it matters:
- the practical move is branch normalization: label and strip the noise around the state-driving core

### E. Encoded-branch / obfuscated-next variants that still preserve one next-state carrier
Shape:
- branch structure is additionally obscured by encoded-branch schemes or by explicit next-variable obfuscation rather than by plain dispatcher repetition alone
- the visible compare or branch edge is not yet the real successor object because the next-state carrier is still being transformed

Why it matters:
- Tigress-style `FlattenObfuscateNext` and encoded-branch variants are a useful reminder that the first trustworthy object may be the normalized next-carrier or one reduced branch-family output, not the superficial branch instruction the decompiler currently emphasizes
- this is still a next-state recovery problem, not automatically a separate full deobfuscation campaign

## 6. Practical workflow

### Step 1: anchor the successor question, not the whole function
Write the smallest blocked question you actually need answered.

Good scratch notes:

```text
blocked question:
  from OBB 0x4016aa, which two states are actually possible on return to the dispatcher?
```

```text
blocked question:
  is the indirect target index itself the real next-state carrier, or only a later dispatch artifact?
```

Bad scratch note:

```text
figure out what this whole function does
```

### Step 2: classify the dispatch form first
Before solving the state relation, classify the local flattening shape.

Useful buckets:
- `switch` / explicit state compare dispatch
- `goto` / direct label churn
- `indirect` / jump-table or computed target dispatch
- `call` / outlined block-function dispatch
- mixed or nested flattening where one layer still reduces into another

Why this matters:
- `switch` and explicit compares often favor state-to-OBB mapping first
- `indirect` and computed-target forms often favor table/index reduction first
- `call` dispatch often favors arg-struct / shared-state object recovery first

### Step 3: choose one state carrier smaller than the whole block
Pick the smallest object that still seems trustworthy.

Typical choices:
- one state variable or register reused across dispatcher entries
- one helper return value consumed by the dispatcher
- one compare result or normalized condition flag that selects between two state families
- one table index used to enter a jump/call table
- one arg-struct field in call-dispatch flattening

Practical rule:
- if your chosen object still requires interpreting the whole flattened block, it is too large

### Step 4: label opaque structure by role before exact truth
Before proving exact semantics, label code regions as:
- state-preserving noise
- branch-inflation / copied-code noise
- helper reduction
- state write candidate
- table/index computation
- dispatcher return or outer consumer

This matters because many practical failures come from treating every branch as business logic.

Example reduction:

```text
region A = copied-code branch inflation
region B = helper reducing compare/output into eax-like next-state carrier
region C = dispatcher re-entry with computed target
```

That is already enough to choose the next proof move.

### Step 5: decide between direct solving and normalization
There are two main operator moves here.

#### Move A: direct solving
Use when:
- the next-state carrier is concrete enough to query symbolically or emulate directly
- a symbolic or emulated run can stop again at dispatcher re-entry
- you can evaluate one or a few solutions for the state carrier

Typical tools / styles:
- angr-style symbolic execution from dispatcher state to dispatcher return
- Miasm symbolic recovery of successor states
- narrow emulation from one candidate state value through one OBB window

Good output:
- `state X -> OBB Y -> successor states {A, B}`

#### Move B: branch normalization first
Use when:
- copied-code or opaque branching makes raw symbolic results too noisy
- the next-state carrier is stable, but the path condition is cluttered
- direct solving is possible only after reducing one compare/helper family

Typical techniques:
- isolate the most-written state variable and its dependencies
- classify which outgoing branch actually depends on that dependency family
- collapse repeated bogus branches into one branch-normalized split
- focus on the helper output or compare result rather than every branch wrapper

Good output:
- `OBB Y has a real two-way split controlled by normalized condition C, producing successor states A/B`

### Step 6: prove one trustworthy relation, not all of them
Useful proof targets include:
- one state value mapping to one original basic block
- one OBB producing exactly one successor state in the non-branching case
- one OBB producing two successor states under one normalized condition family
- one computed table index mapping cleanly to one dispatcher target family
- one patch-worthy replacement where a dispatcher return can be rewritten as a direct edge

Do not wait to recover the whole function if one trustworthy relation is already enough to unblock static work.

Practical reminder from recent Binary Ninja / Miasm / OLLVM unflattening material:
- many workable pipelines succeed by extracting one state mapping or one successor edge first, then rewriting or simplifying around that proof
- they do **not** require perfect decompilation or total opaque-predicate removal before progress starts
- if your workflow keeps demanding full CFG prettification before you trust any edge, you are probably solving the wrong step first

### Step 7: decide whether CFG repair is now worth it
Once one successor relation is trusted, decide what to do next.

Good next outputs:
- one repaired edge in IL or a patching script
- one smaller helper worth deeper static cleanup
- one calmer compare-run / watchpoint target
- one renamed state slot / table index family
- one outer consumer branch now reachable without dispatcher churn

If the answer is still “read more flattened code,” the pass probably failed to reduce the problem enough.

## 7. Practical recovery families

### A. State-to-OBB mapping first
Use when:
- explicit state compares or switch cases are still visible
- the missing piece is attaching each state to a real original block

Why it helps:
- once OBB/state mapping is stable, successor recovery becomes more local and less abstract

### B. OBB-to-successor-state solving first
Use when:
- one OBB is already visible enough
- the real blocker is which successor state(s) it computes before returning to the dispatcher

Why it helps:
- this is often the narrowest bridge from flattened reading back to ordinary CFG truth

### C. Table/index normalization first
Use when:
- indirect dispatch or computed-target arithmetic dominates
- the immediate state constant is less stable than the table/index relation
- Tigress-like `indirect` or `call` dispatch makes the real stable object look more like an index domain, jump-table family, or arg-struct `next` field than a direct constant write

Why it helps:
- a truthful target-family map can be enough before exact constant recovery
- in indirect/call forms, the practical proof object is often the **dispatch contract**:
  - which index or field values are admissible
  - which jump-table or call-table family they select
  - whether the dispatcher itself adds side effects that must be preserved when patching

Practical stop rule:
- if you can already say `index/field family X reaches target family Y under dispatcher contract Z`, you often have enough to leave broad flattening work even before every constant is explained

### D. Helper-output anchor first
Use when:
- many noisy instructions reduce into one helper output later written to the state carrier
- backward slicing keeps rediscovering the same reducer helper, compare-normalization helper, or arg-struct updater even though the surrounding block stays messy

Why it helps:
- reading the helper is often cheaper and more truthful than reading every opaque wrapper around it
- this matches real operator practice in Miasm / Hex-Rays-style workflows where narrow backward tracking plus emulation is enough to recover one trustworthy successor relation

Practical stop rule:
- if one helper output already predicts the later `next` write, table index, or arg-struct field family better than the raw block does, freeze that helper as the state carrier for this pass instead of widening back out to the whole OBB

### E. Dispatcher-contract anchoring first
Use when:
- call-dispatch or indirect-dispatch flattening keeps mixing real successor selection with dispatcher-local mechanics
- patching or CFG repair is tempting, but it is still unclear whether dispatcher blocks themselves contribute side effects, normalization writes, or table lookups that must be copied forward
- the immediate question is not full handler meaning, but what exact dispatcher assumptions must stay true for one recovered edge to remain valid

Why it helps:
- it separates `recover next target` from `preserve dispatcher-owned semantics`
- it prevents a common failure mode where analysts correctly recover a successor family but incorrectly delete dispatcher-side writes, lookup steps, or return-shape obligations that still matter

Minimum useful output:
- one small dispatcher contract note such as:
  - `state/index domain = {a,b}`
  - `table/dispatcher maps a->handler_A, b->handler_B`
  - `dispatcher side effect = writes arg->phase before tail call`
  - `safe patch boundary = after side-effect copy, before indirect jump`

## 8. Representative scratch schemas

### Minimal next-state note
```text
blocked relation:
  ...

dispatch form:
  switch | goto | indirect | call | mixed

state carrier chosen:
  ...

opaque / noise regions:
  A = ...
  B = ...

proof target:
  one OBB/state mapping | one successor edge | one two-way split | one patch-worthy edge

result:
  ...
```

### Branch-normalized split note
```text
OBB:
  ...

noise shape:
  copied-code | opaque compare | helper-mediated write | computed index

normalized condition family:
  ...

successor states:
  true-like -> ...
  false-like -> ...

later effect linked:
  ...
```

## 9. Typical mistakes
### Mistake 1: treating all opaque branches as equally important
Why it hurts:
- you spend time naming junk structure instead of the state-driving core

Better move:
- separate branch inflation from the actual state carrier and successor relation

### Mistake 2: demanding full predicate simplification before any progress
Why it hurts:
- many practical wins only require one normalized split or one solved successor pair
- real-world flatteners can deliberately obfuscate `next` or inflate copied-code branches, so full predicate cleanup is often a poor first milestone

Better move:
- recover one trustworthy next-state relation first, then decide if deeper predicate cleanup is worth it

### Mistake 3: solving state values without reconnecting them to OBBs or effects
Why it hurts:
- raw constants are not yet analyst leverage

Better move:
- tie the state to one original block, one dispatcher target family, or one downstream effect

### Mistake 4: patching too early
Why it hurts:
- premature CFG repair can lock in a wrong successor model
- in indirect/call-dispatch cases, it can also erase dispatcher-side lookup or side-effect obligations that were still part of the truthful path

Better move:
- patch only after at least one state/OBB or successor relation is independently trusted
- if dispatcher-local side effects still look plausible, write the patch boundary as a contract first instead of immediately deleting the dispatcher

### Mistake 5: staying inside the flattened region after one edge is already enough
Why it hurts:
- the next useful question may already live in the outer consumer branch, not in more dispatcher archaeology

Better move:
- once one edge is trustworthy, ask which calmer static target it unlocks

### Mistake 6: collapsing target recovery and dispatcher contract into the same question
Why it hurts:
- you may prove that an index maps to the right handler family, yet still miss that the dispatcher writes one phase field, normalizes one register, or contributes one arg-struct update before re-entry

Better move:
- keep two explicit proof objects when needed:
  - `successor truth`: which target family is reached
  - `dispatcher contract truth`: which dispatcher-local writes/lookups must survive for that edge to stay valid

## 10. Stop rule
You can stop this workflow when you have all of:
- one named dispatch form and one chosen state carrier
- one trustworthy OBB/state or state/successor relation
- one branch-normalized, helper-normalized, or dispatcher-contract explanation for why the relation was previously obscured
- one next static or runtime target that is now calmer than the original flattened window

Strong stop signal for indirect/call forms:
- if you can already name one small dispatcher contract plus one trustworthy successor family, that is usually enough to hand off into calmer CFG repair, helper cleanup, or outer-consumer proof work

If you still only have:
- “there are many opaque predicates here”
- “the dispatcher is complicated”
- or “symbolic execution produced a lot of expressions”

then you are not done yet.

## 11. Practical reminders from external tooling and transform docs
- Tigress flattening documentation is useful because it makes the transform knobs explicit: dispatch shape (`switch`, `goto`, `indirect`, `call`) and next-variable obfuscation are separate moving parts. That is a practical reminder not to confuse “dispatcher recognized” with “next-state carrier already recovered.”
- Binary Ninja-based unflattening writeups are useful because they often succeed by mapping one state variable or one block-to-state relation and only then patching or rewiring blocks. That supports the operator rule: recover one edge first, prettify later.
- Opaque-predicate-removal material is useful, but mainly as a **noise reduction** aid. If the real missing object is still one successor relation, do not over-promote generic opaque cleanup into the whole task.
- Miasm / OLLVM deflattening material is useful because it repeatedly treats symbolic execution or local emulation as a narrow successor extractor, not as a requirement to fully solve the whole function in one pass.

## 12. Relationship to neighboring pages
- Use `vm-trace-to-semantic-anchor-workflow-note` when the main problem is still finding the first stable semantic anchor inside noisy protected execution.
- Use `flattened-dispatcher-to-state-edge-workflow-note` when the anchor is already good enough and the remaining problem is a more ordinary state-edge / dispatcher-exit reduction.
- Use this page **between** them when the flattened region is already recognizable, but the next-state relation is still obscured by opaque predicates, helper-mediated writes, computed-next-state structure, or encoded-branch / obfuscated-next variants.
- Leave this page once one trustworthy successor relation already exists and the real next task becomes outer-consumer proof, CFG repair, or downstream consequence localization.

## 13. Sources
- `sources/protected-runtime/2026-04-05-opaque-next-state-recovery-notes.md`
