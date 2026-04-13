# Copied-Code Branch Inflation to Trustworthy Successor-Split Workflow Note

Topic class: workflow note
Ontology layers: workflow/sensemaking, protected-runtime practical branch, deobfuscation/flattening continuation, successor-split normalization
Maturity: emerging
Related pages:
- topics/protected-runtime-practical-subtree-guide.md
- topics/opaque-predicate-and-computed-next-state-recovery-workflow-note.md
- topics/flattened-dispatcher-to-state-edge-workflow-note.md
- topics/input-invariant-opaque-predicate-to-valid-input-constraint-recovery-workflow-note.md
Related source notes:
- sources/protected-runtime/2026-04-14-copied-code-branch-successor-split-notes.md

## 1. What this workflow note is for
This note covers a narrower protected-runtime / deobfuscation case than the broad opaque-predicate page.

Use it when the analyst already has something stronger than “there is a dispatcher somewhere.”
Typically, one normalized next-carrier already exists:
- one state variable
- one helper-reduced next value
- one compare-normalized carrier
- one table index family
- or one cmov/phi-reduced `next` family

But the practical blocker is now narrower:
- copied-code branches
- question-opaque splits
- bogus branch wrappers
- or other branch-inflation structure

still make it unclear which successor split is real enough to trust.

The workflow goal is to move from:

```text
one normalized next-carrier
+ several noisy copied / inflated / wrapper branches
```

to:

```text
one trustworthy successor split
or one proved "this branch family is only inflation noise" answer
```

## 2. When to use this note
Use this note when most of the following are true:
- the target is already clearly flattening- or protected-next-state-shaped
- the dispatcher or flattened region is already recognizable enough
- one normalized next-carrier is already good enough to name
- raw branch structure still looks wider or more dramatic than the real split probably is
- copied-code, bogus-branch, or question-opaque inflation is plausible
- patching or CFG repair feels tempting, but the branch family that actually owns the split is still not trustworthy

Do **not** use this as the primary note when:
- the main blocker is still broad next-carrier recovery
- the first stable semantic anchor is still missing entirely
- a trustworthy successor relation already exists and the real bottleneck is now durable state-edge or outer-consumer proof
- the narrower question is really accepted-input / valid-input invariance rather than copied-code split realism

## 3. Core claim
Once one next-carrier is already stable enough, the next discriminant is often **branch ownership**, not more broad carrier recovery.

A practical split worth preserving is:

```text
normalized next-carrier recovered
  != visible copied-code / question-opaque branch family understood
  != branch actually depends on the carrier or its dependency family
  != trustworthy true/false successor split recovered
  != safe CFG repair
```

This keeps analysts from overreading:
- big copied arms
- noisy conditional wrappers
- one patched never-branch
- or one recovered next value in isolation

as if any of those alone already explained the real successor split.

## 4. Boundary objects to keep separate
### A. Carrier truth
Freeze one last stable carrier before dispatcher re-entry or target-family mapping.
Examples:
- one `next` variable
- one helper output later written into `next`
- one table index family
- one SSA/phi/cmov-reduced conditional next value

### B. Copied-code / branch-inflation truth
Freeze which branch family is merely widening the picture.
Typical cases:
- a copied arm created by question-opaque insertion
- a bogus constant branch wrapper
- a duplicated statement with one lightly obfuscated copy
- a helper wrapper that looks branch-heavy but preserves the same carrier result

### C. Dependency truth
Ask which branch actually depends on:
- the carrier itself
- the carrier’s dependency family
- or the same reduction helper that materially changes the carrier

If a branch does **not** depend on the carrier family, it is a weak candidate for owning the real successor split.

### D. Successor-split truth
This is the main target of the note.
Recover one of:
- one real `true_next` / `false_next` pair
- one one-vs-many target-family split
- one proof that both visible arms normalize to the same successor family and are therefore only inflation noise

### E. Dispatcher-contract truth
Before patching, ask whether the dispatcher still contributes:
- one lookup step
- one side-effecting write
- one arg-struct update
- one normalization step that must survive

A correct successor family plus a wrong dispatcher contract is still not a safe repair.

## 5. Default workflow
### Step 1: freeze one last stable carrier, not the prettiest branch
Write the carrier explicitly:

```text
stable carrier for this pass:
  state var S before dispatcher compare
```

or

```text
stable carrier for this pass:
  phi/cmov-reduced next family N just before backbone mapping
```

If the chosen object still requires interpreting the whole block to stay meaningful, it is too large.

### Step 2: label branch families by role before exact semantics
Reduce visible branches into roles such as:
- copied-code arm
- bogus / constant wrapper
- carrier-producing branch
- backbone compare branch
- outer consumer branch

Good scratch reduction:

```text
branch A = copied-code inflation around statement family
branch B = real carrier-producing conditional
branch C = backbone compare that maps carrier values to targets
```

This prevents the broadest-looking branch from automatically becoming the trusted split.

### Step 3: ask which branch is eligible to own the split
Use the smallest discriminant first:
- which branch reads the carrier or its dependencies?
- which branch only wraps already-computed carrier writes?
- which branch is constant or patchable noise at the IL level?
- which branch changes the normalized carrier output, not just the raw pseudocode shape?

Practical rule:
- if a branch family does not materially change the carrier output or the mapped target family, treat it as inflation noise until proven otherwise

### Step 4: compare normalized arm outputs, not raw copied code
This is the key move.
For each visible arm, reduce the answer to one of:
- resulting carrier value family
- resulting `true_next` / `false_next`
- resulting table-index family
- resulting mapped backbone destination

Useful compare question:

```text
do the two visible arms actually produce different carrier outputs,
or only different-looking copied code?
```

If both arms normalize to the same carrier value or the same mapped destination, collapse the split as branch inflation noise.

### Step 5: recover one trustworthy split with the smallest truthful method
Useful methods include:
- IL/SSA reduction of a cmov/phi-style conditional carrier
- narrow symbolic execution from one relevant block to dispatcher re-entry
- narrow emulation of the carrier-producing window only
- dependency checks showing which branch family really changes the carrier
- backbone mapping from carrier values to real destinations

Good outputs:
- `OBB Y -> true_next A / false_next B`
- `both visible copied arms normalize to the same next value N`
- `branch family C is noise; branch family D owns the real split`

### Step 6: patch only after successor truth and dispatcher contract are frozen
Safe repair needs both:
- one trustworthy split
- one minimal dispatcher contract that still has to survive

Do **not** jump from “I found a stable next-carrier” directly to “delete the noisy branches” if one lookup/write/normalization step still belongs to the truthful path.

## 6. Source-backed practical reminders
### 1. Tigress keeps carrier obfuscation and branch inflation separate on purpose
The Tigress flattening docs keep these separate:
- dispatch form
- next-variable obfuscation (`--FlattenObfuscateNext`)
- branch encoding (`--FlattenConditionalKinds=branch|compute|flag`)

The AddOpaque docs make copied-code branch inflation explicit:
- `question` predicates can split an original statement from an obfuscated copy
- `--AddOpaqueObfuscate=true` can make the copied arm noisier without changing the real operator goal

Operator reminder:
- copied arm visibility is weaker than proving different normalized successor outputs

### 2. Binary Ninja’s opaque-predicate workflow is best read here as noise reduction
Binary Ninja’s MLIL/data-flow patching is useful when a branch is already constant enough to prove.
Its own limitations note matters just as much:
- loops
- writable segments
- unmodeled data sources

Operator reminder:
- constant-wrapper cleanup is real, but it is not the same proof object as a still-conditional successor split

### 3. State-carrier recovery and split ownership are separate steps
The Binary Ninja unflattening material from d0minik is useful because it:
- identifies a state variable / dependency family
- maps states to OBBs
- checks whether retained control-flow really depends on that family

Operator reminder:
- once a normalized carrier already exists, ask which branch truly depends on it before trusting the split

### 4. Miasm/SSA material sharpens the target into `true_next` / `false_next`
MODeflattener is useful because it reduces conditional relevant blocks into:
- one conditional reducer
- one `true_next`
- one `false_next`
- later backbone mapping

Operator reminder:
- if the visible arms do not survive normalization into distinct next values or mapped destinations, the branch family is weaker than it looked

### 5. Symbolic execution is a narrow bridge here, not the full job
angr’s symbolic-execution docs support using constraints to answer one bounded A-to-B question.

Operator reminder:
- use symbex here to recover one split or one carrier-to-target relation
- do not widen immediately into whole-function deobfuscation unless the narrower split still stays ambiguous

## 7. Practical stop rules this note preserves
- `copied-code branch visible != real successor-splitting branch`
- `stable next-carrier != true/false successor pair recovered`
- `constant wrapper patched != still-conditional split understood`
- `raw arms differ != normalized carrier outputs differ`
- `distinct successor pair recovered != later durable state edge proved`

## 8. Sources
See:
- `sources/protected-runtime/2026-04-14-copied-code-branch-successor-split-notes.md`
- `sources/protected-runtime/2026-04-14-0450-copied-code-successor-split-search-layer.txt`

Primary retained references for this continuation:
- https://tigress.cs.arizona.edu/transformPage/docs/flatten/index.html
- https://tigress.cs.arizona.edu/transformPage/docs/addOpaque/index.html
- https://binary.ninja/2017/10/01/automated-opaque-predicate-removal.html
- https://d0minik.me/posts/cff/
- https://mrt4ntr4.github.io/MODeflattener/
- https://docs.angr.io/en/latest/core-concepts/symbolic.html
