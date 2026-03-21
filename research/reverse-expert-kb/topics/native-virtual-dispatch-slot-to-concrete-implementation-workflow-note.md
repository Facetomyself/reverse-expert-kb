# Native Virtual-Dispatch Slot to Concrete Implementation Workflow Note

Topic class: workflow note
Ontology layers: workflow/sensemaking, runtime-evidence bridge, native baseline practical branch
Maturity: emerging-practical
Related pages:
- topics/native-binary-reversing-baseline.md
- topics/native-practical-subtree-guide.md
- topics/native-interface-to-state-proof-workflow-note.md
- topics/native-plugin-loader-to-first-real-module-consumer-workflow-note.md
- topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/runtime-behavior-recovery.md

## 1. What this workflow note is for
This note covers a recurring native desktop/server reversing case:

- the code is readable enough to navigate
- one object or interface family is already plausible
- one visible indirect call already looks like virtual dispatch or COM-style method invocation
- but the investigation still stalls because the analyst has not yet proved which concrete slot implementation or runtime object family actually carries the effect

This is not mainly the earlier native problem of choosing a broad route from many unrelated handlers.
It is not mainly the later async-native problem of proving which delivered callback matters after ownership is already known.
It is the narrower middle problem of turning:

```text
visible virtual / interface dispatch
```

into:

```text
one concrete implementation family
-> one slot
-> one downstream effect-bearing consequence
```

## 2. When to use this note
Use this note when most of the following are true:
- the target still behaves like an ordinary native binary rather than a primarily protected-runtime or protocol-shaped case
- one semantic anchor is already stable enough to read surrounding structure
- one route or subsystem is already plausible enough that the next uncertainty is no longer broad route choice
- a call site clearly uses a vptr/vtable, interface method table, COM-style pointer, or equivalent indirect slot dispatch
- multiple runtime types, subobjects, interface families, or sibling implementations still compete
- the useful next output is not broad class reconstruction, but one proof of which concrete implementation matters first

Typical triggers:
- `call [reg+offset]` after loading a vptr or interface table
- constructor-side vtable writes are visible, but several candidate tables still compete
- COM-like object creation / `QueryInterface` / factory output is visible, but one retained interface pointer has not yet been tied to one effect-bearing slot
- a decompiler shows `obj->vtable->MethodX(obj, ...)`, but the analyst still cannot say which concrete `MethodX` implementation changes behavior

Do **not** use this as the primary guide when:
- the main problem is still stabilizing the first trustworthy semantic anchor
- many unrelated entry families still compete and `topics/native-interface-to-state-proof-workflow-note.md` is the better earlier step
- the main uncertainty is still plugin/module ownership rather than concrete slot implementation
- the concrete implementation is already known and the remaining ambiguity now lives in callback/event delivery

## 3. Core claim
In virtual-dispatch-heavy native work, the next best move is often not:
- cataloging every class
- naming every vtable
- fully devirtualizing every call site
- or stopping at “this is a COM / C++ virtual call”

The useful practical move is to reduce one visible dispatch site into:
- one supplying object base or interface pointer
- one slot index / offset
- one smallest realistic set of candidate tables or runtime types
- one concrete implementation proved by one downstream state/effect edge

The key practical question is usually:

```text
Which concrete implementation behind this visible slot call
first changes behavior in a way that makes the subsystem trustworthy?
```

## 4. The five boundaries to mark explicitly

### A. Dispatch-site recognition boundary
This is where the analyst proves the call is really table-mediated dispatch.
Typical anchors include:
- vptr load followed by slot-offset indirect call
- COM/interface-pointer dereference followed by indexed call
- decompiler output that already exposes `obj->vtable->slot(...)`
- CFG or thunk wrappers that still preserve one slot-bearing indirect call pattern

What to capture here:
- the exact call site worth proving
- the object register / pointer used
- the slot offset or slot index

### B. Supplying object-base / subobject boundary
This is where the analyst proves which object base actually supplies the table pointer.
Typical anchors include:
- constructor writes to `this` plus subobject offsets
- multiple-inheritance layout showing several vptr-bearing regions
- pointer adjustments before the call
- retained interface pointers stored at different offsets or fields

What to capture here:
- whether the slot comes from the primary object base, a secondary subobject, or an adjusted interface pointer
- which offset matters at the call site

### C. Candidate-table narrowing boundary
This is where the analyst reduces the set of plausible runtime tables.
Typical anchors include:
- constructor/initializer overwrites
- factory return types or provider families
- `QueryInterface` identity checks and interface UUID comparisons
- pure-virtual placeholders and impossible abstract candidates
- compare-run evidence showing one family cannot be live under the current conditions

What to capture here:
- the smallest realistic set of candidate tables / runtime types
- why nearby alternatives are only structural siblings or impossible under current conditions

### D. Concrete slot-implementation boundary
This is where the analyst binds the slot to one concrete implementation worth following.
Typical anchors include:
- one function pointer entry in a candidate table
- one derived-class override at the relevant slot index
- one interface-specific method body reached from the retained pointer family
- one reused implementation shared by several candidates but still effect-bearing enough to matter

What to capture here:
- one implementation body worth trusting first
- whether the proof is “this exact type,” “this smaller type family,” or “this shared implementation used by the remaining candidates”

### E. Proof-of-effect boundary
This is where the analyst proves that the chosen implementation matters.
Typical anchors include:
- one state write or mode toggle
- one later request/reply/file/UI/storage effect
- one worker launch, callback registration, or provider installation seeded by the implementation
- one compare-run difference when table family, feature path, or interface negotiation changes
- one watchpoint / breakpoint proving that this implementation, not a sibling slot, precedes the target consequence

What to capture here:
- one concrete effect linked back to the chosen implementation

## 5. Default workflow

### Step 1: pick one dispatch site, not the whole class hierarchy
Do not begin by reconstructing every class in the binary.
Choose one dispatch site with:
- a clear target behavior
- one plausible downstream effect
- a manageable number of candidate runtime types or interface families

Good first questions are usually:
- which concrete implementation owns this one behavior-changing slot?
- which retained interface pointer is actually being invoked here?
- which slot behind this visible dispatch first causes the target effect?

### Step 2: separate call-site recognition, object-base recovery, candidate narrowing, and effect proof
A common native mistake is collapsing all of this into “virtual function analysis.”
Label the chain as:
- dispatch-site recognition
- supplying object base / subobject proof
- candidate-table narrowing
- concrete implementation selection
- effect proof

This usually reveals that seeing a vtable call is only the beginning.

### Step 3: prefer one retained pointer family over broad class inventory
Look for the first place where several structural possibilities reduce to:
- one object family returned by a factory
- one retained interface pointer
- one constructor pattern that makes one table live at the relevant offset
- one `QueryInterface` result used later
- one provider object reused downstream

If you still have many equally plausible runtime families after this pass, you are probably still doing structural inventory rather than behavioral reduction.

### Step 4: use compiler and ABI clues conservatively
Helpful clues include:
- constructor order and vtable overwrites
- pure-virtual placeholders
- secondary subobject offsets
- COM `IUnknown` / `QueryInterface` / factory patterns
- pointer adjustments before slot use

But treat them as narrowing evidence, not as the final proof.
The real stopping point is one implementation-to-effect chain.

### Step 5: prove one slot-to-effect chain with a narrow runtime move
Typical minimal proofs include:
- watchpoint on the retained object or interface pointer plus breakpoint on one candidate implementation
- breakpoint on constructor/factory output and one later slot invocation through the retained pointer
- compare run that changes one feature gate, object family, or interface negotiation path and checks one later effect difference
- reverse-causality from a visible state/file/network/UI effect back to the slot-bearing implementation
- record/replay around one stable invocation to show one implementation precedes one target consequence

The aim is not full class recovery.
It is one proof that:
- this is the relevant dispatch site
- this is the relevant object/interface family
- this slot implementation changes later behavior

### Step 6: rewrite the subsystem map after proof
Once proved, rewrite the working model as:

```text
retained object or interface family
-> slot index / method position
-> concrete implementation body
-> one downstream effect
```

Only after that should you widen into neighboring slots, sibling implementations, deeper class reconstruction, or later async continuations.

## 6. Common scenario patterns

### Pattern 1: Ordinary C++ hierarchy with one behavior-changing override
Symptoms:
- one base-type pointer is visible
- several derived types share nearby structure
- one vtable call is easy to spot, but dynamic type is unclear

Best move:
- use constructor-side table writes and impossible abstract candidates to narrow the runtime family
- prove one override body through one downstream effect
- ignore sibling classes until one implementation is grounded

### Pattern 2: COM-style interface pointer with sparse names
Symptoms:
- object creation or acquisition is visible
- `QueryInterface` or factory logic exists
- method calls happen through interface pointers, but names are weak or absent

Best move:
- treat interface identity and returned pointer retention as the main narrowing surface
- prove one slot index and one later consequence rather than trying to name every method up front
- use UUID / IID / factory anchors if present, but do not wait for perfect naming

### Pattern 3: Multiple inheritance or subobject confusion
Symptoms:
- several vptr-bearing offsets exist in the same object
- decompiler output looks plausible but the wrong base may be selected
- one pointer adjustment changes the apparent dispatch family

Best move:
- prove which subobject offset supplies the slot at the call site
- then narrow candidate implementations only inside that subobject family
- avoid broad hierarchy claims until the base-offset question is settled

### Pattern 4: CFG / thunk-heavy indirect calls
Symptoms:
- indirect-call wrappers or thunks make many slot calls look similar
- the call graph keeps terminating at a guard/helper layer
- analysts over-credit the thunk rather than the real implementation-bearing slot

Best move:
- treat the thunk as the dispatch-site wrapper, not the ownership proof
- recover the actual table slot and one downstream implementation body
- prove one effect after the thunk layer, not just successful thunk traversal

## 7. How this fits into the native branch
This note fills a practical native gap between broad route proof and later ownership/delivery continuations.

A useful native reading order is now:
- `topics/native-practical-subtree-guide.md` when the case is clearly native-shaped but the branch entry still needs routing
- `topics/native-semantic-anchor-stabilization-workflow-note.md` when readable structure still lacks one trustworthy local meaning
- `topics/native-interface-to-state-proof-workflow-note.md` when one anchor is stable enough but several broad entry families still compete
- `topics/native-virtual-dispatch-slot-to-concrete-implementation-workflow-note.md` when one route is plausible and the next bottleneck is reducing visible virtual/interface dispatch into one concrete implementation proof
- `topics/native-plugin-loader-to-first-real-module-consumer-workflow-note.md` when the remaining ambiguity is no longer the slot implementation itself but a loaded-module/provider owner
- `topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md` when a service/worker owner is already plausible but later worker ownership still needs narrowing
- `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md` when ownership is good enough and the remaining uncertainty lives in callback/event delivery

This note is therefore best read as the native branch’s **virtual-dispatch-to-concrete-implementation reduction step**.

## 8. Practical handoff rule
Leave this note and continue into a later native continuation as soon as the main uncertainty stops being “which concrete implementation sits behind this slot?” and becomes one of these instead:
- which loaded module or provider owns the now-proved implementation family
- which service-owned worker continues the proved implementation path
- which callback/event-loop consumer turns the proved implementation into later behavior

A compact rule is:
- stay in this note while the main uncertainty is still reducing visible slot dispatch into one concrete implementation proof
- leave this note once one implementation-to-effect chain is already good enough and the real bottleneck becomes module ownership, service/worker ownership, or async delivery

## 9. Failure modes this note helps prevent
- stopping at “this is a vtable call” without proving one implementation
- over-investing in whole-hierarchy reconstruction before one slot matters operationally
- confusing a base/interface abstraction with the concrete runtime family
- misreading the supplying object base or subobject offset in multiple-inheritance cases
- over-crediting CFG/thunk wrappers instead of the real slot-bearing implementation
- treating COM/interface naming as sufficient without one slot-to-effect proof
- widening into sibling implementations before one behavior-changing implementation is grounded

## 10. Compact operator checklist
- Pick one visible dispatch site, not the whole hierarchy.
- Prove which object base or subobject supplies the table.
- Narrow the candidate runtime families aggressively.
- Prefer one retained pointer family over broad class inventory.
- Use one narrow slot-to-effect proof before expanding sideways.

## 11. Sources and confidence
Primary source note for this page:
- `sources/native-binary/2026-03-21-native-virtual-dispatch-slot-to-concrete-implementation-notes.md`

This workflow is grounded in:
- practical virtual-call and vtable narrowing from ALSchwalm’s C++ virtual-function reversing write-up
- MSVC object-layout, constructor-overwrite, and COM-like vftable realities from Dennis Babkin’s write-up
- interface-negotiation and retained-contract framing from Microsoft’s `QueryInterface` documentation

Confidence note:
- strong for the workflow seam and stop rules
- moderate for compiler-specific details, which vary by ABI and implementation
- intentionally conservative about claiming universal static devirtualization; the page is about proving one concrete implementation first
