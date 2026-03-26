# ISR / Deferred-Worker Consequence-Proof Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, firmware/protocol context recovery, runtime-evidence bridge
Maturity: practical
Related pages:
- topics/firmware-and-protocol-context-recovery.md
- topics/peripheral-mmio-effect-proof-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/causal-write-and-reverse-causality-localization-workflow-note.md
- topics/native-interface-to-state-proof-workflow-note.md

## 1. When to use this note
Use this note when the firmware case is already partly localized, but the analysis still stalls because the first behavior-changing boundary is later than the obvious MMIO write.

Typical entry conditions:
- one command family, parser path, or state trigger is already isolated
- one peripheral/MMIO path, register family, or effect-bearing write is already suspected
- some interrupt/ack/mask helpers, ISR entries, or deferred worker callbacks are already visible
- but the first trustworthy consequence-bearing edge is still unclear

Use it for cases like:
- firmware where a register write or DMA arm is visible, but the meaningful state change only appears in an interrupt/completion path
- embedded services where a parser path is known, yet the real reply-family or scheduler effect is chosen in a later deferred worker
- rehosting work where peripheral writes are modeled, but behavioral drift persists because completion/interrupt handling is still under-modeled
- ISR-heavy code where broad peripheral labeling exists, but the first durable state reduction still hides inside bottom-half or workqueue logic

Do **not** use this note when the real bottleneck is earlier, such as:
- no stable trigger or compare pair exists yet
- the parser/state consequence is still unclear before any peripheral path is visible
- MMIO/peripheral effect proof itself is still the main unknown
- the problem is mainly a generic protected-runtime or mobile/WebView observability issue

In those cases, start with:
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`

## 2. Core claim
A recurring interrupt-driven firmware RE bottleneck is that the first visible MMIO or peripheral effect is **not yet the most useful proof boundary**.

The useful analyst target is often:
- not the first register write you can name
- not the first interrupt line or vector table entry you can label
- not the broadest set of ISR/deferred callbacks you can enumerate

It is the first local handoff that turns a trigger or hardware-side condition into one durable consequence, such as:
- a completion-driven state write
- a reply-family or error-family selection
- a queued deferred worker that applies policy or mode reduction
- a scheduler edge that gates later retries or wakeups
- a status-latch or completion bucket that predicts downstream behavior

That handoff is usually more valuable than wider interrupt taxonomy.

## 3. Target pattern
The recurring target pattern is:

```text
trigger / parser / MMIO path visible
  -> interrupt enable, completion, or peripheral condition becomes possible
  -> ISR or deferred worker consumes that condition
  -> one state/reply/scheduler reduction actually changes behavior
  -> later visible effect proves it mattered
```

The key discipline is:
- separate **peripheral-effect visibility** from **interrupt/deferred consequence visibility**
- separate **IRQ arrival truth** from **deferred scheduling truth** from **first consumer/reduction truth**
- localize the first handoff that predicts later durable behavior

A useful operator shorthand for this branch is:
- `armed != observed_irq != scheduled_deferred != consumed`

That shorthand helps prevent a recurring overclaim:
- seeing an interrupt line fire or a worker get scheduled is often only arrival truth, not yet the first truthful behavior owner
- the stronger target is the first completion/status reduction, poll owner, worker-side state write, reply selector, or wakeup edge that actually predicts later durable behavior

It also guards the opposite mistake:
- sometimes the top-half or IRQ-side path really does perform the decisive reduction already
- in those cases, do not invent a later worker story just because deferred machinery exists nearby

## 4. What counts as a consequence-bearing handoff
Treat these as high-value targets:
- first interrupt enable/mask/ack path that differs across a representative compare pair
- first ISR entry that only occurs on the interesting side and leads to durable state reduction
- first deferred worker/tasklet/workqueue/bottom-half callback that performs a meaningful state write or reply/error selection
- first completion or status-latch edge that predicts later policy/state behavior better than the earlier MMIO write alone
- first queue insertion or scheduler wakeup that turns hardware completion into user-visible or protocol-visible behavior
- first reduction from a noisy completion/status value into a smaller local mode/policy bucket

Treat these as useful but often one layer too early:
- vector-table visibility alone
- broad ISR enumeration alone
- seeing the candidate MMIO write alone
- broad polling/status reads without a later durable consequence

## 5. Practical workflow

### Step 1: Freeze one narrow representative pair
Prefer one compare pair over broad interrupt logging.

Good pairs include:
- same command family where only one side reaches the later reply or completion behavior
- same trigger under two hardware/model states where only one side enters the interesting ISR or deferred callback
- same MMIO write pattern where only one side reaches the later state write or wakeup
- same request/command family where accepted vs degraded behavior differs only after completion handling

Record only what you need:
- trigger identity
- candidate MMIO/peripheral path
- candidate ISR/deferred-worker family
- later visible consequence difference

If you do not yet have a stable pair, you are still too early for this note.

### Step 2: Mark five boundaries explicitly
Before widening interrupt taxonomy, mark these five boundaries:

1. **trigger boundary**
   - first stable command, state, or route distinction
2. **peripheral-effect boundary**
   - where the path first becomes MMIO/peripheral-facing or completion-eligible
3. **interrupt/deferred handoff boundary**
   - where an interrupt, completion callback, tasklet, bottom-half, or worker becomes reachable
4. **consequence boundary candidate**
   - first state write, reply-family selection, scheduler wakeup, or policy reduction inside that handoff path
5. **proof-of-effect boundary**
   - later status, reply, retry, wakeup, or externally visible difference that depends on the candidate consequence edge

This prevents “we found the ISR” from being mistaken for “we found the cause.”

### Step 3: Prefer first durable reduction over widest callback map
When many ISR/deferred paths are visible, prioritize the earliest stable reduction that differs across the pair:
- completion/status bucket -> mode/policy bucket
- interrupt source -> one narrower handler family
- deferred callback -> one state/reply selector
- wakeup/queue edge -> one later visible consequence

This is usually a better anchor than enumerating every interrupt source first.

A practical refinement from current Linux-facing source material is:
- IRQ/top-half visibility may only prove arrival and scheduling
- NAPI poll ownership, softirq/tasklet execution, threaded IRQ follow-up, or workqueue/process-context handling may own the first durable behavior change instead
- therefore, prefer the first object that **survives** IRQ scope and predicts later behavior: one poll owner, worker argument package, reduced completion bucket, reply selector, or wakeup/state-write edge

### Step 4: Localize the first handoff that predicts behavior
After the peripheral-effect boundary, ask:
- where does the path first stop being a raw hardware event and become a stable local state or policy event?
- where is the first ISR or deferred path only reachable on the interesting side?
- where is the first completion/status value reduced into a smaller action bucket?
- where is the first wakeup/queued callback that actually changes later behavior?

Useful local role labels:
- `trigger`
- `mmio-entry`
- `interrupt-arm`
- `isr-entry`
- `completion-read`
- `status-reduction`
- `deferred-worker`
- `state-write`
- `reply-select`
- `scheduler/wakeup`
- `effect-proof`

If a region cannot be given one of these roles, it may still be churn rather than leverage.

### Step 5: Prove the handoff with one downstream consequence
Do not stop at “this looks like the right ISR.”

Prove the candidate handoff by tying it to one downstream effect such as:
- a durable state value changes only when the deferred callback runs
- one reply or error family appears only after one ISR/deferred path takes a specific reduction
- one retry/wakeup/scheduler edge occurs only after the candidate completion handler
- one rehosting failure disappears only when the interrupt/deferred consequence is modeled correctly
- one visible behavior difference correlates with the ISR/deferred consequence edge across a disciplined compare pair

A weaker but still useful proof is:
- the earlier MMIO write appears in both runs, but only the run reaching the candidate ISR/deferred consequence edge produces the later behavior

### Step 6: Hand the result back to one next concrete task
Once localized, route the result into one next task only:
- refine the minimal rehosting/interrupt model
- narrow the next static target around one completion or deferred-worker family
- refine one protocol-state or reply-selection note
- improve one fuzzing or replay model with the newly proved deferred consequence

Do not immediately widen into full interrupt-controller or driver taxonomy unless the next experiment truly needs it.

### Practical handoff rule
Stay on this note while the missing proof is still the first durable interrupt/completion/deferred consequence:
- the first ISR or deferred-worker reduction that turns an already-visible hardware-facing edge into one trustworthy state, reply, scheduler, or policy consequence
- the first completion/status bucket whose local reduction predicts later durable behavior better than the earlier MMIO/peripheral edge alone
- the first interrupt/deferred handoff that must be proved before rehosting, protocol-state reasoning, or replay realism becomes trustworthy

Leave broad ISR/deferred consequence work once one durable consequence edge is already good enough and the real bottleneck has shifted into one narrower continuation such as:
- rehosting or interrupt-model refinement when one proved ISR/deferred consequence is already enough and the next task is now representing that handoff correctly rather than proving more neighboring callback families
- narrower protocol-state, reply-selection, or scheduler follow-up when the durable consequence is already good enough and the remaining uncertainty is no longer interrupt/deferred proof itself
- provenance, runtime-evidence packaging, or another branch-specific continuation when the decisive consequence is already captured and the next need is preserving, reusing, or handing off that proof cleanly

A recurring failure mode is staying too long in broad interrupt/callback narration after one consequence-bearing handoff is already good enough:
- enumerating sibling ISR entries
- widening callback maps
- cataloging more completion helpers
when the real bottleneck has already become model realism, narrower downstream proof, or evidence packaging.

## 6. Breakpoint / hook placement guidance
Useful anchor classes:
- first trigger-family discriminator
- first interrupt enable/mask/ack helper differing across the pair
- first ISR entry only reached on the interesting side
- first completion/status read inside the ISR/deferred path
- first deferred worker/tasklet/workqueue callback reached after the candidate event
- first state write or reply-family selection inside that callback family
- first scheduler wakeup or queue insertion that predicts later visible behavior
- first downstream reply/status/output boundary after the deferred consequence

If traces are noisy, anchor on:
- compare-run divergence around first ISR/deferred entry
- completion/status reductions rather than every low-level register read
- first durable state write or reply selection rather than the full callback body
- later proof boundaries such as reply/status/retry/wakeup rather than every polling loop

## 7. Failure patterns this note helps prevent

### 1. Mistaking MMIO visibility for solved understanding
A visible register write is not yet leverage if the first durable consequence only appears after interrupt or deferred handling.

### 2. Overcollecting ISR traces after one good pair already exists
Once one good pair exists, more interrupt logs often add breadth without explaining the decisive handoff.

### 3. Treating callback enumeration as the end of the hunt
The stronger target is often the first reduction from completion/status material into:
- one state bucket
- one reply family
- one scheduler/wakeup decision
- one retry/degrade branch

### 4. Confusing generic interrupt plumbing with the interesting consequence
The meaningful edge is often later and more conditional than generic vectoring or ack boilerplate.

### 5. Chasing full hardware-model completeness too early
A partial but proven ISR/deferred consequence edge is often enough to unblock rehosting, replay, protocol, or state reasoning.

## 8. Concrete scenario patterns

### Scenario A: The visible write matters only because one ISR consumes it
Pattern:

```text
command handled
  -> MMIO write visible
  -> no immediate stable behavior change
  -> one ISR later reads completion/status and changes durable state
```

Best move:
- anchor on the first ISR-side state reduction, not the write alone

### Scenario B: Deferred worker is the real reply selector
Pattern:

```text
parser and peripheral path visible
  -> completion/interrupt occurs
  -> deferred worker runs later
  -> reply or error family is chosen there
```

Best move:
- treat the deferred worker's first reply-select or state-write edge as the real consequence boundary

### Scenario C: Rehosting drift comes from under-modeled completion logic
Pattern:

```text
register map partly modeled
  -> trigger path appears correct
  -> behavior still diverges
  -> only one missing completion/interrupt/deferred consequence explains the drift
```

Best move:
- use the later divergence as proof-of-effect and work backward to the missing ISR/deferred boundary

## 9. Relationship to nearby pages
- `topics/firmware-and-protocol-context-recovery.md`
  - explains why context and downstream utility dominate many firmware cases
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
  - use that when the missing proof is still where accepted local state becomes one real outbound serializer / queue / transport handoff rather than a later completion-driven consequence
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
  - use that when the main missing edge is still the first effect-bearing MMIO/peripheral write itself
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
  - use that when the missing edge is still parser/state-side before peripheral or interrupt consequences dominate
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`
  - this page is the firmware interrupt/deferred sibling for a similar effect-to-cause proof problem

## 10. Minimal operator checklist
Use this note best when you can answer these in writing:
- what is the one trigger family or compare pair?
- where is the first peripheral-effect boundary?
- what interrupt/deferred handoff becomes reachable after it?
- what is the first candidate consequence edge inside that handoff path?
- what later effect proves that edge mattered?
- what single next task becomes easier once that edge is known?

If you cannot answer those, the case likely needs a more upstream note first.

## 11. Source footprint / evidence quality note
This note is intentionally workflow-first.

It is grounded by:
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/runtime-behavior-recovery.md`
- `sources/datasets-benchmarks/2026-03-14-firmware-protocol-context-notes.md`
- `sources/firmware-protocol/2026-03-16-isr-deferred-worker-consequence-proof-notes.md`

The evidence base here is sufficient for a practical workflow note because the point is not to claim one universal interrupt architecture.
The point is to normalize a recurring operator move that the KB previously lacked.

## 12. Bottom line
When firmware analysis already has trigger visibility and even some MMIO/peripheral effect visibility, the next high-value move is sometimes not broader register labeling and not wider ISR logging.

It is to localize the first **ISR/deferred-worker consequence boundary** that turns an earlier hardware-facing edge into a durable state, reply, scheduler, or policy effect that can guide the next experiment confidently.
