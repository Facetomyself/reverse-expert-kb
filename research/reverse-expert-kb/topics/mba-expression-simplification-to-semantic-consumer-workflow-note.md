# MBA Expression Simplification to Semantic Consumer Workflow Note

Topic class: concrete workflow note
Ontology layers: deobfuscation practice branch, protected-runtime overlap, expression-recovery workflow
Maturity: structured-practical
Related pages:
- topics/obfuscation-deobfuscation-and-packed-binaries.md
- topics/anti-tamper-and-protected-runtime-analysis.md
- topics/protected-runtime-practical-subtree-guide.md
- topics/vm-trace-to-semantic-anchor-workflow-note.md
- topics/opaque-predicate-and-computed-next-state-recovery-workflow-note.md
- topics/input-invariant-opaque-predicate-to-valid-input-constraint-recovery-workflow-note.md
- topics/flattened-dispatcher-to-state-edge-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md

## 1. Why this page exists

This page preserves a narrower deobfuscation seam that was still underfed in the KB.

The protected-runtime branch already had practical notes for:
- trace slices to handler reconstruction
- VM trace to semantic anchor recovery
- opaque-predicate / computed-next-state recovery
- input-invariant predicates
- copied-code branch inflation
- flattened dispatcher to state-edge reduction

What was missing was the smaller expression-level case where the analyst has already isolated an obfuscated value expression, often a Mixed Boolean-Arithmetic (MBA) or bit-vector expression, but still has not proved that simplifying it explains the original program behavior.

The weak conclusion is:

```text
MBA expression simplified == behavior understood
```

The stronger reverse-engineering question is:

```text
which exact expression was extracted,
under which bit-vector width / flags / casts / memory-read domain,
which simplified candidate is equivalent there,
where can it safely replace the original reasoning,
and which first semantic consumer proves it matters?
```

## 2. Target pattern / scenario

Use this note when most of the following are true:
- a value, branch predicate, array index, key component, dispatcher update, handler result, or policy field is hidden behind MBA / bit-vector expression noise
- decompiler output or lifted IR is readable enough to isolate one candidate expression, but not simple enough to trust semantically
- symbolic execution, AST extraction, trace-window learning, algebraic rewriting, oracle lookup, or synthesis can produce a simpler candidate expression
- the current bottleneck is narrower than broad VM / dispatcher recovery, but earlier than ordinary consumer proof
- progress depends on proving that one simplified expression preserves the original program point’s behavior and is consumed by a later branch, state update, request field, key path, or dispatcher edge

Representative cases include:
- OLLVM / Tigress-style arithmetic encoding around branch predicates
- VMProtect / Themida-style arithmetic handler expressions or state updates
- malware or protector code that uses nonlinear MBA to diversify data flow or opaque predicates
- request-signature or token code where a masked bit-vector expression feeds one field, key, or checksum
- flattened dispatcher loops where one computed next-state expression is the remaining blocker

## 3. Core claim

MBA / bit-vector simplification is a candidate-expression workflow, not a final proof object.

A practical proof ladder is:

```text
expression extracted
  != bit-vector domain / side effects frozen
  != candidate simplification produced
  != equivalence validated for the original domain
  != replacement safe at this program point
  != first semantic consumer / effect proved
```

Compact branch memory:

```text
extracted != domain-frozen != simplified != equivalent != replaced != consumed/effected
```

This split prevents six common overreads:
1. **extraction overread** — a pretty AST / IR expression may omit flags, truncations, memory reads, undefined behavior, or surrounding side effects
2. **width overread** — equivalence at 8, 16, 32, or 64 bits may not transfer automatically across casts, sign/zero extension, or masked subexpressions
3. **tool-output overread** — a simplifier result is a candidate until its verification mode and residual handling are known
4. **sampling overread** — input/output agreement from finite samples is useful evidence, not universal proof unless the domain is small enough or solver proof covers it
5. **replacement overread** — a simplified expression may be safe for reasoning but not safe as a patch if flags, timing, faulting loads, or aliasing matter
6. **consumer overread** — knowing `x + y` does not prove which later predicate, index, key, state edge, or request field consumed it

## 4. First questions to answer

Before broadening the analysis, answer:

1. **What semantic question does this expression answer?** Branch predicate, next-state value, key component, index, checksum, handler return, or policy field.
2. **Where exactly did the expression come from?** Decompiled expression, lifted IR, trace window, symbolic slice, emulator sample, or manually reconstructed AST.
3. **What is the exact domain?** Bitwidth, signedness interpretation, truncation, extension, flags, carries, masks, and allowed input ranges.
4. **What side effects are outside the pure expression?** Memory reads, faulting operations, volatile loads, helper calls, flag writes, timing, or exception behavior.
5. **How was simplification produced?** Algebraic rewriting, MBA-Blast-style reduction, oracle lookup, SMT, synthesis, trace-window learning, or tool-specific pass.
6. **How was equivalence checked?** Solver proof, exhaustive small-domain check, randomized spot check, compare-run validation, or only visual plausibility.
7. **Who first consumes the simplified value?** Dispatcher update, branch condition, table index, request field, crypto/key path, state reducer, or ordinary effect.

## 5. Practical workflow

### Step 1: isolate one expression and one consumer hypothesis

Do not start by simplifying every noisy expression.

Pick one expression because it plausibly feeds a concrete later object:
- branch that gates accepted vs failed runs
- computed next-state assignment
- table index into handler / opcode / policy material
- key, checksum, token, or request-field component
- masked flag or enum consumed by a later reducer

Record:

```text
expression site: function/block/instruction or trace-window id
raw expression source: decompiler / IR / symbolic slice / trace samples
consumer hypothesis: <one later branch, index, field, state edge, or effect>
late behavior sought: <one visible consequence>
```

If there is no consumer hypothesis, the expression is only cleanup material.

### Step 2: freeze the exact bit-vector domain

Before trusting any simplification, freeze:
- bitwidth at every node that matters
- truncation and extension points
- signedness only where comparison, division, shift, or decompiler presentation requires it
- shift-count masking / target-ISA behavior
- carry/overflow/flag dependencies if the original instruction sequence exposes them
- input invariants such as parser ranges, accepted-domain constraints, or impossible malformed values

Good note:

```text
candidate predicate is 32-bit modulo arithmetic;
upper bits are truncated before the compare;
input byte range is already restricted by parser guard at block X.
```

Bad note:

```text
looks like x + y in Python, so replace it with integer addition everywhere.
```

### Step 3: separate pure expression from surrounding side effects

MBA simplification usually assumes a pure expression. Real binaries may not.

Check whether the expression extraction skipped:
- memory reads whose value or fault behavior matters
- helper calls folded into decompiler expressions
- flag writes consumed later
- volatile or device-backed reads
- self-modifying or generation-dependent code
- exception/fault behavior used as control flow

Stop rule:

```text
same value expression != same program-point behavior
```

If a memory read or flag write matters, package it as a precondition or split the workflow into side-effect proof first, expression simplification second.

### Step 4: produce one candidate simplification

Use the lightest method that matches the expression family:
- algebraic rewriting for obvious identities and linear MBAs
- MBA-Blast / 1-bit reduction style when the expression fits known MBA assumptions
- oracle / lookup / subtree simplification for extracted ASTs
- SMT equivalence for bounded bit-vector formulas where solver cost is acceptable
- synthesis or trace-window learning when direct symbolic handling is too brittle but input/output sampling is reliable
- decomposition or lifting when one hard subexpression blocks a simpler outer skeleton

Record the method and failure mode, not only the pretty output.

```text
candidate: ((x ^ y) + 2*(x & y)) -> x + y
method: oracle simplification + Z3 check at 32 bits
remaining residual: none
```

### Step 5: validate equivalence at the original program boundary

Prefer the strongest cheap validation available:
- solver proof over the exact bit-vector formula
- exhaustive check for small domains or reduced Boolean signatures
- randomized spot checks plus targeted edge cases for large domains
- compare-run validation at the same program boundary
- trace-window replay where the same inputs produce the same consumer-side value

Edge cases to include when sampling:
- zero, all-ones, sign bit, carry boundaries
- mask boundaries and shift-count extremes
- accepted-domain minima/maxima
- malformed-domain values if they can reach the site

Stop rule:

```text
simplified-looking != equivalent-for-this-boundary
```

### Step 6: decide whether the simplification is for reasoning or patching

A simplification may be good enough to label the program but unsafe to patch.

Separate:
- **reasoning replacement** — use the simpler expression to understand the value and guide the next hook / watchpoint / rename
- **static rewrite** — edit lifted IR / decompiler presentation or local notes, preserving original binary behavior
- **runtime patch** — change code in the target, only after flags, side effects, timing, fault behavior, and anti-tamper consequences are checked

Do not patch just because the value expression is equivalent. In protected runtimes, the original expression may also serve as a timing, anti-symbolic, checksum, or self-check surface.

### Step 7: prove the first semantic consumer

Finish by tying the simplified value to one behavior-bearing object:
- branch condition that selects accepted / rejected behavior
- dispatcher next-state write or state-edge reduction
- table index that selects one handler family
- key/checksum/token component used by a request field
- policy enum or flag consumed by an outer reducer
- unpacking or decoder parameter that changes the generated artifact

Good stop condition:

```text
32-bit candidate expression at block B is equivalent to x + y;
the value is written to state.slot_14;
first consumer is dispatcher compare at block D;
accepted and failed runs diverge there.
```

Weak stop condition:

```text
MBA simplified to x + y; done.
```

## 6. Where this note routes next

Route to `topics/opaque-predicate-and-computed-next-state-recovery-workflow-note.md` when the simplified expression is only one piece of a broader successor-recovery problem.

Route to `topics/input-invariant-opaque-predicate-to-valid-input-constraint-recovery-workflow-note.md` when equivalence depends on accepted-input constraints rather than the full bit-vector domain.

Route to `topics/flattened-dispatcher-to-state-edge-workflow-note.md` when one simplified next-state expression is already good enough and the real blocker is now the durable state edge or outer consumer.

Route to `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md` when the expression indexes runtime-built tables whose live initialization state is more truthful than static reconstruction.

Route to `topics/decrypted-artifact-to-first-consumer-workflow-note.md` when the simplified expression only yields readable artifact material and the remaining question is ordinary consumer proof.

## 7. Evidence packaging template

Use this compact shape in notes:

```text
site:
  <function/block/instruction/trace-window>
raw expression:
  <IR/AST/decompiler expression and extraction caveats>
domain:
  <bitwidth, casts, flags, ranges, side effects>
candidate simplification:
  <short expression>
validation:
  <solver/exhaustive/sampling/compare-run evidence and limits>
consumer:
  <branch/index/state/request/key/policy consumer>
status:
  reasoning-only | static-label-safe | patch-candidate | rejected
next missing proof:
  <one boundary, not broad future work>
```

This keeps expression recovery useful to the next reverser without pretending one simplifier output explains the whole protected region.
