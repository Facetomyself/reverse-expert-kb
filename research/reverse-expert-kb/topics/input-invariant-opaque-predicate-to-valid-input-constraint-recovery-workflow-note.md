# Input-Invariant Opaque Predicate to Valid-Input Constraint Recovery Workflow Note

Topic class: workflow note
Ontology layers: workflow/sensemaking, protected-runtime practical branch, deobfuscation/constraint recovery, opaque-predicate continuation
Maturity: emerging
Related pages:
- topics/protected-runtime-practical-subtree-guide.md
- topics/opaque-predicate-and-computed-next-state-recovery-workflow-note.md
- topics/native-semantic-anchor-stabilization-workflow-note.md
- topics/causal-write-and-reverse-causality-localization-workflow-note.md
Related source notes:
- sources/protected-runtime/2026-04-04-input-invariant-opaque-predicate-notes.md

## 1. What this workflow note is for
This note covers a narrower protected-runtime / deobfuscation case than the broad opaque-predicate page.

Use it when the analyst already knows the remaining ambiguity is not mainly:
- “what is the computed next state?”
- “which dispatcher successor is real?”

but instead:
- “what valid-input constraint keeps this branch family invariant?”

The practical problem is that some opaque-predicate families are only “opaque” if the analyst ignores the input domain the protected code actually expects.
Under the valid-input set, the branch can become effectively invariant or nearly invariant, while invalid-input exploration creates misleading extra structure.

The goal is to move from:

```text
one branch family that looks data-dependent and expensive to enumerate
```

to:

```text
one recovered valid-input constraint or invariant class
that explains why the branch behaves as fixed (or nearly fixed)
for the executions that actually matter
```

## 2. When to use this note
Use this note when most of the following are true:
- the target is already clearly protected-runtime / obfuscation shaped
- broad dispatcher / successor recovery is no longer the cheapest discriminant
- one suspicious branch or predicate looks input-dependent in the large but strangely stable in real executions
- compare runs suggest the branch truth depends less on arbitrary symbolic inputs than on a smaller “accepted/valid” input class
- the operator value is recovering one acceptance or validity constraint, not just proving one dead branch in the abstract

Do **not** use this as the primary note when:
- the main uncertainty is still broad computed-next-state recovery
- the case is better described as flattening/dispatcher ownership rather than valid-input restriction
- the analyst does not yet have enough stable traces or execution classes to distinguish valid-input behavior from arbitrary perturbation noise

## 3. Core claim
Some opaque predicates are most usefully understood not as “universally constant” but as **stable over the valid input domain the protected code expects**.

That means the right operator question is often not:

```text
Can I prove this predicate is globally constant?
```

but:

```text
What input/trace/domain constraint makes this predicate effectively fixed
for the real executions I care about?
```

## 4. Boundary objects to keep separate
### A. Predicate-structure truth
You already have one candidate branch family.
Freeze:
- one predicate site
- one controlling value family
- one compare pair or trace family

### B. Real-execution stability truth
Ask:
- across real executions, is the branch unusually stable?
- do perturbations that violate the target’s acceptance rules create branch diversity that the target normally never sees?

### C. Valid-input constraint truth
This is the real target of the note.
Recover one smaller constraint class such as:
- input length/domain restriction
- parser-normalized field relation
- checksum or modular relation
- range/format property
- earlier guard that eliminates the seeming branch diversity

### D. Consequence truth
Once the constraint is recovered, ask what it buys you:
- dead-branch elimination for real traces?
- cleaner state reduction?
- simpler patch point?
- easier accepted-input generation?

## 5. Default workflow
### Step 1: choose one predicate family, not all opaque branches
Do not start by classifying every suspicious branch.
Pick one family with:
- high recurrence in real traces
- obvious downstream leverage if simplified
- a compare set where “valid” versus “invalid” executions can be distinguished

### Step 2: stop asking for global constancy first
Write the narrower local question explicitly:

```text
Is this predicate globally opaque,
or only effectively fixed over the valid input class?
```

This prevents wasted effort on universal proofs when the operator need is domain-constrained.

### Step 3: build a valid-vs-invalid compare set
Prefer compare pairs like:
- accepted input vs nearby rejected input
- sanitized/normalized input vs raw malformed variant
- successful protected execution vs failing early-guard execution

Goal:
- separate branch diversity caused by invalid domains from behavior that survives accepted executions

### Step 4: recover one smallest explanatory constraint
Try to name one compact constraint that collapses the branch family, such as:
- equality modulo some mask or width
- checksum consistency
- length/header relationship
- parser-normalized canonical form
- one earlier acceptance guard that dominates later branch variation

Do not overfit to symbolic beauty.
One ugly but real accepted-input invariant is enough.

### Step 5: cash out the recovery
Once you have one valid-input constraint, decide the cheapest operator payoff:
- simplify the predicate as effectively fixed under valid inputs
- generate accepted inputs that bypass exploration noise
- move the breakpoint/watchpoint earlier to the acceptance guard
- patch or rewrite analysis assumptions around the invariant domain

## 6. Practical stop rules this note preserves
- `branch looks data-dependent != branch matters across valid executions`
- `can’t prove global constancy != no practical invariant exists`
- `symbolic diversity over malformed inputs != real branch diversity in accepted traces`
- `one recovered valid-input invariant != full semantic recovery of the subsystem`

## 7. Sources
See: `sources/protected-runtime/2026-04-04-input-invariant-opaque-predicate-notes.md`

Primary retained references for this continuation:
- https://www.usenix.org/conference/usenixsecurity21/presentation/yadegari
- https://www.usenix.org/system/files/sec21fall-yadegari.pdf
- https://www.ndss-symposium.org/wp-content/uploads/2020/04/bar2020-23004.pdf
- https://dl.acm.org/doi/pdf/10.1145/2810103.2813617
