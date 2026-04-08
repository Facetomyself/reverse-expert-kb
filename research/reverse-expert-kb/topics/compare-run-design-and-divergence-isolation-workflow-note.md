# Compare-Run Design and Divergence Isolation Workflow Note

Topic class: workflow note
Ontology layers: runtime-evidence practice branch, compare-run design, divergence isolation, operator workflow
Maturity: structured-practical
Related pages:
- topics/runtime-evidence-practical-subtree-guide.md
- topics/runtime-behavior-recovery.md
- topics/hook-placement-and-observability-workflow-note.md
- topics/record-replay-and-omniscient-debugging.md
- topics/representative-execution-selection-and-trace-anchor-workflow-note.md
- topics/causal-write-and-reverse-causality-localization-workflow-note.md
- topics/runtime-evidence-package-and-handoff-workflow-note.md
- topics/analytic-provenance-and-evidence-management.md

## 1. Why this note exists
The runtime-evidence branch already had practical pages for:
- choosing a truthful observation surface
- deciding when replay or execution-history capture is worth the cost
- choosing one representative execution and one first trace anchor
- walking backward from one visible late effect to one causal boundary
- packaging one already-good runtime result for reuse

What it still lacked was a concrete note for a common operator bottleneck in between:

```text
I can run the target in at least two nearby ways
  + I know the behavior differs somewhere meaningful
  + but I have not yet designed a useful compare pair
  + and I still do not know where the first meaningful divergence lives
  -> design one compare pair on purpose
  -> hold the invariants steady
  -> choose one compare boundary
  -> isolate the first divergence worth deeper causal work
```

Without this step, analysts often fall into one of two bad patterns:
- compare two runs that differ in too many dimensions, then drown in noise
- skip compare-run design entirely and jump straight into broad reverse-causality over an oversized trace

This note exists to preserve a smaller practical rule:
- design the compare pair before diffing it
- choose the smallest behavior-bearing difference you actually care about
- isolate the first meaningful divergence boundary
- only then widen into deeper reverse-causality or branch-specific proof

## 2. Core claim
Compare-run work becomes useful when the analyst treats the pair itself as a designed experimental object.

The usual ladder is:

```text
name one target behavior difference
  -> choose one near-neighbor compare pair
  -> hold all irrelevant conditions as fixed as possible
  -> choose one first compare boundary
  -> isolate the first meaningful divergence
  -> hand that divergence into reverse-causality or branch-specific proof
```

The practical milestone is not:
- “I have two traces”

The practical milestone is:
- **I have one compare pair whose first meaningful divergence is small enough to explain and useful enough to guide the next proof step**

## 3. When to use this note
Use this note when most of the following are true:
- two nearby executions can be produced or approximated
- one run is accepted / failing / gated / ungated / consequence-bearing and the other is not
- the broad observation surface is already good enough to support comparison
- the analyst still needs to design the pair so that the later diff is interpretable
- the key missing proof is the first meaningful divergence, not a full subsystem narrative

Representative triggers:
- “I have an accepted and rejected request path, but too many surrounding differences.”
- “I can capture crash and no-crash runs, but I need to know where they first separate.”
- “I have instrumented and uninstrumented outcomes, but I still need one narrower divergence boundary before deeper explanation.”
- “I know the late behavior differs, but I do not yet know which event family should act as the compare boundary.”

Do **not** use this note when:
- the truthful observation surface is still unclear
  - use `topics/runtime-behavior-recovery.md` or `topics/hook-placement-and-observability-workflow-note.md`
- replay worthiness is still the main question
  - use `topics/record-replay-and-omniscient-debugging.md`
- one stable compare pair already exists and the first meaningful divergence is already known
  - use `topics/causal-write-and-reverse-causality-localization-workflow-note.md` or a branch-specific continuation
- the real problem is preserving an already-good compare result for handoff
  - use `topics/runtime-evidence-package-and-handoff-workflow-note.md`

## 4. Core distinction: compare-pair design vs reverse-causality
### A. Compare-pair design
Question:
- what two executions should I compare so that the diff means something?

The goal is:
- one near-neighbor pair
- one intended behavior difference
- as few accidental differences as possible

### B. Reverse-causality
Question:
- now that I know the first meaningful divergence region, what earlier write, branch, queue edge, or reducer predicts it?

The goal is:
- one causal boundary behind a now-bounded divergence

Treating these as separate choices prevents a recurring failure mode:
- analysts compare noisy runs
- mistake volume for signal
- then do expensive backward reasoning over differences caused by setup drift rather than the target behavior

## 5. How to design a useful compare pair
A useful compare pair usually differs in one intended dimension while keeping neighboring conditions steady enough that early divergence is interpretable.

Prefer pairs that are:
- **near-neighbor**: accepted vs rejected, gated vs ungated, crash vs no-crash, challenge-passed vs challenge-failed, feature-on vs feature-off
- **bounded**: minimal setup difference needed to provoke the target contrast
- **stable enough**: repeated enough to trust that the key difference is not random noise
- **anchorable**: both runs still share at least one event family or boundary useful for alignment

Avoid pairs that differ in too many uncontrolled ways:
- different environment plus different input plus different timing plus different observer placement
- long runs with unrelated background tasks inserted in only one side
- “successful” vs “failed” runs where failure changed the whole setup before the target path even began

A compact rule:
- if you cannot say in one sentence what the pair is meant to isolate, the pair is not ready

## 6. What to hold invariant
Before collecting the pair, freeze as many non-target variables as practical:
- same build, image, or binary revision
- same observation surface and hook family
- same environment unless environment is the intended test dimension
- same setup steps and trigger timing where possible
- same starting state or reset procedure where possible
- same trace or logging granularity

If one of these must differ, record it explicitly as part of the pair design.

The compare pair should make it obvious which of these is:
- the intended difference
- tolerated noise
- still-open uncertainty

A practical refinement worth preserving is an **alignment truth** split:
- which early differences are merely real-but-non-explanatory variation that the pair can tolerate
- which early differences show the pair is misaligned and needs redesign
- which early differences are credible first semantic split candidates

That keeps the operator from collapsing every early mismatch into one vague "divergence" bucket.

## 7. How to choose the first compare boundary
Do not begin by diffing the entire trace blindly.
Choose one first boundary where alignment is still plausible and downstream divergence is likely to matter.

Good first compare boundaries are often:
- first request-finalization or send boundary
- first parser entry or validated input object
- first callback fire after shared registration/setup
- first child-process creation or first handoff to payload-side execution
- first module load or first artifact consumer after shared initialization
- first queue insertion, wakeup, or worker-owned consumer after shared trigger setup
- first state reduction or policy bucket assignment near the visible late effect

A useful heuristic:
- pick the earliest boundary that still preserves a believable “same path so far” story across both runs

## 8. Practical workflow
### Step 1: state the intended contrast
Write one line describing what the pair is meant to isolate.
Examples:
- accepted request vs rejected request with same pre-signing state except freshness token
- crash-triggering input vs no-crash input with one field family changed
- gated execution vs ungated execution under same setup except anti-instrumentation presence

### Step 2: list the intended difference and fixed invariants
Write two short lists:
- **Intended difference**
- **Held fixed**

If those lists are fuzzy, the pair will probably be noisy.

### Step 3: choose one first compare boundary
Pick one boundary where both runs should still be meaningfully alignable.
Examples:
- same serializer entry
- same handler family
- same callback registration followed by first callback fire
- same queue owner before later state or consequence diverges

### Step 4: test whether the pair is too wide
If the two runs diverge massively before the chosen boundary, redesign the pair.
Typical fixes:
- narrow the input difference
- shorten the capture window
- hold more setup constant
- move the first compare boundary later to a more stable shared region
- or, if the pair reveals a hidden earlier setup dependency, make that dependency the new intended question

### Step 5: isolate the first meaningful divergence
Once the pair is good enough, identify the first divergence that actually matters for the target question.
Good divergence candidates usually include:
- first missing/present callback consumer
- first different field/value reduction with downstream effect
- first different queue edge or worker wakeup
- first different request object or emitted request family
- first different artifact consumer or module-owner handoff
- first different branch or state write that predicts the later outcome

Meaningful divergence is not the same as earliest textual diff.
Ignore differences that are obviously incidental:
- addresses, handles, unrelated timestamps, allocator churn, trivial logging order, or known non-semantic noise

A practical refinement worth preserving explicitly is:
- the first mismatch is not automatically the first meaningful divergence
- early differences often need to be classified as either:
  - expected nondeterministic churn
  - setup drift that means the compare pair itself still needs repair
  - or true semantic split candidates worth deeper work

A stronger operator stop rule is:
- **alignment truth comes before causality truth**
- before asking "what caused this divergence?", first ask whether the observed early mismatch is:
  - tolerated alignment noise
  - evidence that the pair itself is not yet comparable at this level
  - or the first behavior-bearing split worth causal follow-up

This matters because an early mismatch can be perfectly real while still being non-explanatory for the analyst's actual question.

Representative noisy-early-diff families include:
- checksums, nonces, or freshness fields that are already known to vary but do not yet predict the behavior difference
- scheduler/context-switch churn, queue ordering drift, or background worker activity that perturbs the trace before the target path separates semantically
- late-bound handles, addresses, allocator layout, or bookkeeping fields whose variation is structurally normal

When those dominate, do not immediately widen into deeper reverse-causality.
Instead:
- move to a compare level or boundary that preserves semantic continuity better
- compare calls, validated objects, queue ownership, reducer outputs, or context-bearing fields before raw instruction churn
- if needed, increase observation density only around the suspected boundary so the first behavior-bearing divergence becomes easier to catch

A compact operator rule is:
- when the early diff is noisy, re-ask the comparison question at a better boundary before treating the first mismatch as explanatory

A narrower async-heavy refinement worth preserving explicitly is:
- if both runs already enter the same broad event loop, queue family, callback-registration region, or worker subsystem, do **not** treat broad async entry or raw mixed-thread event order as the compare boundary by default
- early queue pops, callback timestamps, worker wakeups, or cross-thread TTD positions can be perfectly real while still too weak to answer the operator's actual question
- in those cases, align instead on one **delivery class** or one **consumer-bearing boundary**, such as:
  - first delivered callback family with downstream effect
  - first dequeued work item carrying the target object/session/request identity
  - first queue-owner handoff that makes one later consumer inevitable
  - first reducer from many ready events into one specific handler/consumer family
- once that first behavior-bearing delivery is bounded, shrink it into one callback slot, queue node, reducer output, or object field before widening into watched-object, reverse-causality, or branch-specific proof

### Step 6: decide whether the divergence is already the watched object
Once the first meaningful divergence is bounded, ask one more question before widening into reverse-causality or branch-specific proof:
- is this divergence already the smallest durable object that a watchpoint, memory query, or reducer-localization workflow can answer well?

Often the answer is **no**.
The first meaningful divergence can still be:
- one callback family rather than the queue slot or registration bit that predicts it
- one request-object difference rather than the field or reduced mode bit inside it
- one policy/result family rather than the local enum or bucket slot that stores the reduced decision
- one consumer/consequence difference rather than the earlier state slot that makes the later difference inevitable

A practical bridge rule worth preserving is:
- **first meaningful divergence** and **best watched object** are often adjacent, but they are not automatically the same proof object
- if the divergence is still semantically rich, aggregate, or awkward to query directly, shrink it into the narrowest truthful watched object before continuing
- treat **query scope as part of correctness**, not just speed: oversized watched objects and broad memory/event searches mix unrelated semantic roles and can return upstream edges that are real but not explanatory for the consequence you care about
- debugger-supported watchpoints/data breakpoints reinforce the same operator rule: a real hit proves one access to the watched range or location, not automatically that the watched scope was already the causal object you should narrate

A second compact reminder now worth preserving explicitly is:
- **watchable != causally selected**
- a watchpoint or data-breakpoint hit can be perfectly real while still belonging to a range, wrapper object, or reused location whose semantic scope is too broad for the actual consequence question

A compact operator ladder is:

```text
first meaningful divergence isolated
  -> ask whether it is already a good watched object
  -> if not, shrink it into one field / slot / slice / reducer output
  -> only then hand off into first-bad-write / decisive-reducer localization or wider reverse-causality
```

A compact compare checklist for this seam is now worth keeping explicit:
- did the run only prove the object/range was **watchable**?
- did it prove only that one **real access/hit** occurred?
- did it prove the watched scope was actually the **causal object selection**?
- did it prove one narrower field/slot/reducer output that predicts the later consequence?

That checklist helps keep watchability, real hit truth, object-scope truth, and consequence-bearing causal selection separate.

### Step 7: decide the next handoff
After the first meaningful divergence is either accepted as the watched object or reduced into one smaller watched object, choose the next note by the remaining bottleneck:
- `topics/first-bad-write-and-decisive-reducer-localization-workflow-note.md` if the real next move is now one watched object, one first useful write/reducer boundary, and one downstream dependency proof
- reverse-causality if the first causal boundary behind the divergence is still missing at a broader level than one watched object
- native/protocol/malware/mobile/protected-runtime branch notes if the divergence now clearly belongs to one domain-specific operator question
- evidence packaging if the compare result is already good enough technically and now needs preservation

A practical stop rule is:
- once the compare pair is trustworthy and one first meaningful divergence is already small enough to shrink into a durable watched object, do **not** keep improving the diff by default
- leave broad compare-run work and let watched-object reduction carry the next proof step

## 9. Common mistakes this note prevents
This note is meant to prevent:
- comparing two runs that differ in many uncontrolled dimensions
- equating early textual differences with meaningful divergence
- starting with a giant trace diff instead of a designed compare boundary
- overcommitting to reverse-causality before the pair itself is trustworthy
- spending time explaining noise created by setup drift rather than the target behavior
- treating “accepted vs rejected” labels as sufficient compare design without checking what was really held constant

## 10. Relationship to sources
This note is supported by several practical source families:
- Tetrane’s trace-diffing write-up explicitly shows that compare value depends on choosing two nearby scenarios and selecting an appropriate comparison level, often starting from calls or coverage before instruction-level detail.
- rr/Pernosco style replay material reinforces that deterministic replay is most useful when the analyst can preserve and revisit one intended behavior difference rather than broad uncontrolled execution history.
- rr divergence-debugging material also reinforces that early visible divergence may need denser checking or narrower observation before the real causal split is caught close enough to explain.
- Binary Ninja’s TTD guidance highlights the need to scope queries and avoid broad, expensive searches without a well-chosen target boundary.

The practical convergence is:
- choose the pair on purpose
- choose the compare level on purpose
- classify noisy early differences before overexplaining them
- in async queue/callback-heavy cases, prefer one delivery-class or consumer-bearing boundary over raw mixed-thread event order
- use the earliest meaningful divergence, not the fullest possible diff and not the first raw mismatch, as the bridge to deeper analysis

Additional source-backed refinement for async-heavy compare work:
- Microsoft Learn and Binary Ninja TTD material reinforce that replay/query value comes from smaller bounded questions, not whole-trace narration or broad unscoped queries
- GDB/ROCGDB watchpoint documentation and WinDbg data-breakpoint material reinforce a related operator rule: hardware/software watch support helps answer a bounded access question, but it does not choose the right semantic object for you
- Raymond Chen's TTD position-order discussion reinforces that cross-thread chronology is weaker than many analysts want at fine granularity, so raw mixed-thread step order should not be overread as behavioral proof by itself
- rr divergence-debugging guidance reinforces that once one narrower delivery boundary is plausible, denser observation around that boundary is more useful than broad timeline storytelling

## 11. Topic summary
This note turns compare-run work into a designed workflow step rather than an ad hoc diff.

The compact rule is:
- design one near-neighbor compare pair
- hold the invariants steady
- choose one first compare boundary
- isolate one meaningful divergence
- only then widen into reverse-causality or branch-specific proof

That keeps runtime-evidence work practical, case-driven, and aligned with the KB’s preferred style: one smaller trustworthy proof boundary at a time.
