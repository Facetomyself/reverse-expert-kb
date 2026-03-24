# Protected Runtime Next-State / Dispatcher-Contract Research Notes

Date: 2026-03-25 00:20 Asia/Shanghai / 2026-03-24 16:20 UTC
Focus: practical continuation for protected-runtime deobfuscation where the flattened region is recognizable, but the truthful successor relation is still blocked by computed indices, helper-mediated writes, or dispatcher-local mechanics
Related pages:
- `topics/opaque-predicate-and-computed-next-state-recovery-workflow-note.md`
- `topics/flattened-dispatcher-to-state-edge-workflow-note.md`
- `topics/protected-runtime-practical-subtree-guide.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`

## Source set retained
- Tigress `Flatten` documentation
  - `https://tigress.cs.arizona.edu/transformPage/docs/flatten/index.html`
- Tigress opaque initialization / update documentation
  - `https://tigress.wtf/opaque.html`
- Quarkslab OLLVM deobfuscation write-up
  - `https://blog.quarkslab.com/deobfuscation-recovering-an-ollvm-protected-program.html`
- eShard D-810 control-flow unflattening write-up
  - `https://eshard.com/posts/D810-a-journey-into-control-flow-unflattening`
- MODeflattener write-up
  - `https://mrt4ntr4.github.io/MODeflattener/`
- raw multi-source search artifact
  - `sources/protected-runtime/2026-03-25-protected-next-state-search-layer.txt`

## High-signal findings

### 1. Dispatch family is not just description; it changes the right proof object
Tigress explicitly preserves multiple flattening forms:
- `switch`
- `goto`
- `indirect`
- `call`

Operational implication:
- `switch` often lets the analyst stop at state-to-case / OBB mapping
- `indirect` often makes the truthful object a **table index / target family relation** rather than a direct constant
- `call` often makes the truthful object an **arg-struct field / shared-state contract** rather than a classic local state variable alone

This supports a KB rule that asks for the smallest stable recovery object *inside the chosen dispatch family*, not just “find the state variable.”

### 2. Flattening can intentionally separate visible dispatcher structure from successor recovery
Tigress explicitly documents:
- `--FlattenObfuscateNext`
- `--FlattenConditionalKinds=compute`
- `--FlattenConditionalKinds=flag`
- optional indirect/call dispatch and optional block splitting/randomization

That matters because it validates a recurring practical bottleneck:
- dispatcher recognition is already solved
- but the next-state relation is still hidden behind helper reduction, computed index arithmetic, or flag-derived target selection

This is exactly the justification for keeping a dedicated bridge page between “semantic anchor exists” and “durable state edge exists.”

### 3. Dispatcher-local mechanics can be part of the truthful path
The retained operator write-ups reinforce that unflattening is not only about identifying the next target.
Two recurring realities show up:
- the dispatcher may perform table lookup, state normalization, or other mechanics that still matter to a truthful repair
- control-flow patching often requires deciding **what must be copied forward** before replacing a dispatcher return with a direct edge

This is especially visible in indirect/call-dispatch families and in microcode-patching workflows.

Practical lesson:
- separate `successor truth` from `dispatcher contract truth`
- do not assume that correctly recovering the target family means the dispatcher is now semantically disposable

### 4. Narrow backward tracking plus emulation is often enough
Quarkslab, eShard, and MODeflattener all point in the same practical direction:
- use narrow symbolic execution, backward variable tracking, SSA/def-use style recovery, or microcode emulation
- recover one successor relation or one state/target map first
- resist the urge to solve the whole function before the first useful edge exists

The KB should preserve the operator-level version of this lesson:
- one helper output, one computed index family, or one arg-struct `next` field can be enough to leave broad flattening work

### 5. Side-effect-aware patch boundaries are a real stop-rule issue
The D-810 write-up explicitly calls out that dispatcher blocks can have side effects and therefore cannot always be naively removed.
That is a practical stop-rule improvement for the KB:
- before CFG repair, write one small contract note naming
  - the stable state/index family
  - the selected target family
  - any dispatcher-local side effect that must survive
  - the safe patch boundary

This is more truthful and reusable than “we found the right successor, so delete the dispatcher.”

## Practical continuation rules worth preserving

### A. In indirect/call forms, freeze the dispatch contract early
Useful contract elements:
- admissible state/index domain
- table or call-family mapping
- arg-struct/shared-state field that actually carries `next`
- dispatcher-local side effects or normalization writes
- safe direct-edge patch boundary

### B. Treat helper output as a valid state carrier
If repeated slicing keeps converging on the same reducer helper or updater, promote that helper output to the main proof object for the pass.
That is often cheaper and more truthful than explaining every wrapper block.

### C. Separate successor proof from dispatcher-deletion proof
Good question split:
- `Which successor family is reached?`
- `What dispatcher-local semantics must survive for that edge to remain valid?`

### D. Leave broad flattening work once one successor family + one contract note exist
Especially in indirect/call-dispatch cases, that is often enough to hand off into:
- calmer CFG repair
- outer-consumer proof
- helper cleanup
- narrower durable-state-edge work

## What changed in my view after this run
Before this run, the KB already knew that table/index normalization and helper-mediated writes mattered.
After this run, the more durable source-backed refinement is:
- **dispatch-contract anchoring** deserves to be explicit, not only implicit inside table/index discussion
- the practical stop rule is often `successor family + dispatcher contract`, not `full predicate cleanup`
- indirect/call-dispatch families need stronger warnings against premature dispatcher deletion

## Conservative limits
- These sources support workflow improvements and stop rules, not a claim of universal generic unflattening.
- The retained value is practical and operator-centered: what to freeze, what to separate, and when to stop.
- Grok search quality was partially degraded during the search-layer run, so the KB edits lean mainly on retained, directly fetched source material plus cross-source consistency from Exa/Tavily surfaced results.
