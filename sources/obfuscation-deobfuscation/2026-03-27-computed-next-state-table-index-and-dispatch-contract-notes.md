# Obfuscation / Deobfuscation Notes — Computed Next-State, Table/Index Recovery, and Dispatcher Contract

Date: 2026-03-27 13:16 Asia/Shanghai / 2026-03-27 05:16 UTC
Branch: protected-runtime / deobfuscation practical workflows
Seam: flattened dispatchers where the dispatcher is already recognizable but next-state recovery is still obscured by computed indices, indirect/call dispatch, opaque `next` encodings, or dispatcher-local mechanics that matter for later patching

## Why this note exists
The protected-runtime branch already preserved a useful bridge for:
- flattened regions where the dispatcher is visible
- next-state logic that is still obscured by opaque predicates, helper-mediated writes, or copied-code inflation

What still needed a thinner practical continuation was the specific subcase where the analyst can already tell the target is **indirect-dispatch** or **call-dispatch** shaped, but the real stable recovery object is not a direct `state = CONST` write.

Instead, practical cases often stall at a narrower boundary:
- the real recovery object looks more like a table index family, arg-struct `next` field, or admissible target-family relation
- dispatcher-local side effects or lookup rules still matter
- early patching risks deleting semantics the dispatcher still owns

This note preserves the narrower operator rule:

```text
dispatcher found != direct next-state truth != target-family truth != safe patch boundary
```

And, for indirect/call forms specifically:

```text
index/field value visible != target-family proved != dispatcher contract preserved
```

## Conservative source-backed takeaways
### 1. Dispatch form diversity matters operationally, not just descriptively
Tigress `Flatten` documentation preserves that flattening is not one single layout. It supports:
- `switch`
- `goto`
- `indirect`
- `call`
- `concurrent`

It also preserves that conditional branches can be rewritten as:
- ordinary branch form
- computed branch form
- flag-derived form

And it explicitly exposes `--FlattenObfuscateNext` plus optional implicit-flow machinery.

Conservative workflow consequence:
- once flattening is recognized, the next recovery object should depend on **dispatch family**
- indirect/call forms often make `table/index relation` or `dispatcher contract` stronger proof objects than a premature hunt for exact next-state constants

### 2. O-MVLL preserves that the state may be encoded rather than directly readable
O-MVLL’s control-flow flattening page explicitly preserves a pattern where the dispatcher switches on an **encoding** of the state variable rather than the raw state value.

Conservative workflow consequence:
- `case label seen` is weaker than `real next-state relation understood`
- a stable recovery object may be one normalized table/index or target-family relation before exact constant decoding is worth forcing

### 3. Practical unflattening writeups repeatedly use narrower successor recovery objects
The retained practitioner material preserves recurring operator moves such as:
- symbolic execution on one relevant block to compute its destination address (Quarkslab’s OLLVM recovery writeup)
- tracking a state variable and mapping possible values back to destinations (MODeflattener)
- for Tigress indirect dispatch, treating jump-table addresses and state-variable-to-target mapping as the core reduction object (D-810 writeup)

Conservative workflow consequence:
- practical progress often comes from recovering one smaller successor relation, index-domain map, or target-family map
- this is a bridge step, not a demand for total function simplification first

### 4. Dispatcher-local mechanics can still be part of the truth boundary
Tigress `call` / `indirect` forms and practitioner unflattening notes together support a narrower warning:
- the dispatcher may own lookup steps, arg-struct writes, normalization, or other local mechanics
- therefore `recovered target family` is not yet the same thing as `safe to patch out dispatcher`

Conservative workflow consequence:
- analysts should freeze one explicit **dispatcher contract** before claiming a recovered edge is patch-ready
- a safe patch boundary may need to preserve dispatcher-side writes or lookup obligations even after the target family is known

## Practical workflow rule preserved for the KB
When flattening is already recognizable, explicitly ask:
1. What dispatch family is this really: `switch`, `goto`, `indirect`, `call`, or mixed?
2. Is the strongest current recovery object a direct state constant, a helper output, an index family, a target family, or a dispatcher-local side effect?
3. Do I already know the target family, or only one encoded/indexed precursor?
4. If I patch now, what dispatcher-owned semantics might I silently erase?

If these split apart, do **not** force the case into a direct-constant next-state story by default.
Instead:
- freeze the smallest truthful recovery object
- preserve one dispatcher contract note when indirect/call mechanics still matter
- stop once one trustworthy successor family plus one safe patch boundary is already enough for the next calmer task

## Case-shaped reminders
### A. Tigress indirect-dispatch cases
Useful stable objects may be:
- admissible `next` index family
- jump-table target family
- one helper that normalizes branch output before index use

Often the right stop rule is:
- `index family -> target family under dispatcher contract`
not
- `every exact state constant fully decoded`

### B. Call-dispatch / outlined-block cases
The operational question may be:
- which arg-struct field or `next` slot selects the next outlined block
- and which dispatcher-side writes still happen before the tail call / indirect call

The first trustworthy proof object may therefore be:
- arg-field family -> callee family
plus
- one dispatcher-owned write that must survive patching

### C. Encoded-state switch cases
When the switch key is encoded or normalized, a useful intermediate answer is often:
- one normalized successor family
- one mapping between the encoded selector domain and a smaller target family

That can already unlock calmer static or IL repair work even before every encoding constant is explained.

## Operator shorthand worth preserving
```text
dispatcher found != direct next-state truth != target-family truth != safe patch boundary
```

```text
index/field value visible != target-family proved != dispatcher contract preserved
```

## Sources used conservatively
- Tigress Flatten docs: <https://tigress.wtf/flatten.html>
- Tigress options docs: <https://tigress.cs.arizona.edu/options.html>
- O-MVLL control-flow flattening docs: <https://obfuscator.re/omvll/passes/control-flow-flattening/>
- Quarkslab — recovering an OLLVM-protected program: <https://blog.quarkslab.com/deobfuscation-recovering-an-ollvm-protected-program.html>
- eShard D-810 unflattening writeup: <https://eshard.com/posts/D810-a-journey-into-control-flow-unflattening>
- MODeflattener writeup: <https://mrt4ntr4.github.io/MODeflattener/>

## Confidence and limits
Confidence: moderate for the workflow rule; conservative for tool-specific generalization.

What this note does **not** claim:
- that exact state constants are never worth recovering
- that dispatcher-local writes always matter
- that all flattened targets should be patched through the same contract model

What it does claim conservatively:
- dispatch-family differences change what the most truthful recovery object looks like
- indirect/call forms often justify `table/index/target-family + dispatcher contract` as a better bridge than premature exact-constant fixation
- the KB should preserve that thinner bridge explicitly so practical deobfuscation work stays case-driven and patch-safe
