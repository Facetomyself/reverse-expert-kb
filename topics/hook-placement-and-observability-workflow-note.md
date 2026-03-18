# Hook Placement and Observability Workflow Note

Topic class: concrete workflow note
Ontology layers: runtime-evidence practice branch, observation-topology selection, hook-placement workflow
Maturity: structured-practical
Related pages:
- topics/runtime-evidence-practical-subtree-guide.md
- topics/runtime-behavior-recovery.md
- topics/record-replay-and-omniscient-debugging.md
- topics/causal-write-and-reverse-causality-localization-workflow-note.md
- topics/analytic-provenance-and-evidence-management.md
- topics/mobile-protected-runtime-subtree-guide.md
- topics/browser-runtime-subtree-guide.md
- topics/native-practical-subtree-guide.md
- topics/protocol-firmware-practical-subtree-guide.md
- topics/protected-runtime-practical-subtree-guide.md

## 1. Why this page exists
This page exists because the runtime-evidence branch already had:
- a broad synthesis page for runtime answerability and observability
- a replay/execution-history page for capture-stability decisions
- a reverse-causality workflow note for late-effect-to-cause reduction

What it still lacked was a compact practical note for the earlier recurring bottleneck:

```text
many places could be instrumented
  + several layers look plausible
  + the current hooks are noisy, semantically late, too broad, or misleading
  -> choose one more truthful observation surface
  -> place one smaller hook family there
  -> prove that the new surface collapses uncertainty faster
```

This is not the same problem as:
- broad runtime-behavior theory
- replay tooling selection
- late-effect reverse watchpoint work
- full protected-runtime observation-topology relocation under resistance

It is the narrower practical problem of turning vague “let’s hook something” energy into one smaller, more decision-relevant observation plan.

## 2. When to use this note
Use this note when most of the following are true:
- the case is clearly runtime-evidence shaped
- several candidate observation layers or hook points exist
- the current uncertainty is still **what to observe next** rather than **what caused one already-stable late effect**
- current hooks/logs are too noisy, semantically late, too early to interpret, or attached to the wrong ownership boundary
- one better observation surface would make the next branch-specific task much smaller

Representative cases:
- many functions mention the target field, but only one owner or reducer would actually collapse the question
- network traffic is visible, but wire visibility does not show the nearest plaintext or structure owner
- a browser/mobile/native workflow exposes many callbacks, but only one callback family is close enough to the consequence-bearing state write
- dynamic traces exist, but they are broad and expensive, and the analyst still lacks one trustworthy compare-run anchor
- hooks at a UI, wrapper, or helper layer show symptoms, but not the first state, queue, reducer, serializer, or policy boundary that matters

Do **not** use this note when the real bottleneck is already narrower, such as:
- one suspicious late effect is already visible and stable enough to walk backward from
- replay/execution-history stabilization is now the main decision
- strong anti-instrumentation, attach failure, or topology relocation dominates the case
- the target is already better framed by a branch-specific note such as parser-to-state proof, interface-to-state proof, VM-trace reduction, or malware staging proof

In those cases, use the more downstream or more target-specific note first.

## 3. Core claim
Good hook placement is not “find an interesting function and log it.”
It is:
- choosing the **smallest truthful observation surface**
- attaching one hook family there
- proving that the new surface reduces uncertainty better than the previous one

The practical sequence is:

```text
question of interest
  -> candidate observation surfaces
  -> one chosen truth boundary
  -> one smaller hook family
  -> one compare-ready observation result
  -> one narrower next task
```

The milestone is not:
- “added hooks”
- “collected more logs”
- “found many related functions”

The milestone is:
- **placed one hook family at the most decision-relevant boundary available and used it to shrink the next question**

## 4. The five boundaries to mark explicitly

### A. Question boundary
State the concrete question first.
Examples:
- where does this request field become final?
- which callback family turns this result code into a policy bucket?
- where does the decrypted or normalized object first become behaviorally meaningful?
- which ownership boundary is closer to truth: UI helper, wrapper, serializer, queue, or consumer?

If the question is still “understand this subsystem,” the hook plan is still too vague.

### B. Surface menu boundary
List the plausible observation surfaces before choosing one.
Common surfaces:
- caller-visible wrappers
- serializers/parsers
- state reducers / enum mappers
- queue or scheduler boundaries
- request finalizers / emitters
- callback registration and callback consumers
- ownership handoffs
- lower socket / syscall / transport boundaries
- framework vs native vs runtime-specific edges

This prevents the common mistake of treating the first visible function as the default hook target.

### C. Truth boundary
Choose the earliest or smallest surface that would still answer the question truthfully.
Useful criteria:
- closer to the first meaning-bearing object
- less vulnerable to wrapper churn
- more comparable across good/bad runs
- near enough to later consequence to predict it
- narrow enough that a positive result changes the next decision

### D. Hook family boundary
Decide what minimal hook set is needed.
Examples:
- one producer + one consumer
- one parser + one state write
- one callback registration + one callback consumer
- one serializer + one request emitter
- one reducer + one downstream scheduler edge

Do not start with a maximal fan-out unless the case already proved that a smaller pair is insufficient.

### E. Compare boundary
Define how success will be judged.
Good compare shapes:
- good run vs failing run
- accepted vs rejected request
- challenge-triggering vs non-triggering path
- one earlier quiet run vs one instrumented run
- one hook surface vs another nearby surface

If there is no compare boundary, logs often decay into anecdotes.

## 5. Practical workflow

### Step 1: freeze one decision question
Write the question in a form that predicts what a better hook would reveal.

Good:

```text
where does visible result_code become the smaller local retry policy bucket?
```

Weak:

```text
find all functions related to retries
```

### Step 2: enumerate surfaces by ownership, not by tool convenience
Before placing hooks, sort candidates into one of a few role families:
- intent / input layer
- normalization / reduction layer
- state / ownership layer
- emission / serialization layer
- callback / consumer layer
- transport / system boundary

This is important because the easiest surface to hook is often:
- semantically too late
- semantically too early
- too wrapped to compare cleanly
- too noisy to support a stable next move

### Step 3: pick the smallest truthful boundary
Ask:

```text
if I could observe only one layer cleanly,
which layer would collapse the uncertainty fastest?
```

Typical choices:
- first reducer from rich object to policy bucket
- first serializer that finalizes a request-bearing object
- first callback consumer that changes durable state
- first queue insertion that predicts delayed behavior
- first owner-visible plaintext / normalized object before lower transport noise begins

Avoid choosing a surface only because:
- it already has friendly symbols
- it is easy to hook from the current tool
- it prints interesting strings
- it sees the data eventually

### Step 4: place one hook family, not a hook cloud
Start with the smallest pair or trio that can establish direction.
Useful starter shapes:
- producer + consumer
- parser + reducer + state write
- callback registration + callback consumer
- serializer + emitter
- queue arm + downstream fire point

A small family is better because it supports cleaner compare runs and clearer failure diagnosis.

### Step 5: read the output for leverage, not for volume
A hook result is useful when it tells you one of these:
- this surface is too late; move upstream
- this surface is too early or too raw; move downstream
- this surface is the right truth boundary; narrow deeper here
- this owner is now plausible enough to hand off to a branch-specific note
- this compare pair diverges here first; freeze this boundary

The desired output is not a bigger trace.
It is a better next decision.

### Step 6: leave this note as soon as the bottleneck changes
This note should end when one of the following becomes true:
- the main problem is now replay/capture stability rather than surface choice
- one suspicious late effect is already stable enough that reverse-causality localization is the better next move
- the right surface is now clear and the remaining work is branch-specific (native, protocol, browser, mobile, malware, protected-runtime)
- strong resistance/anti-instrumentation means the real problem is topology relocation, not ordinary hook placement

If you keep adding hook families after the truthful surface is already known, you are probably staying too long in this note.

## 6. Representative scenario patterns

### Pattern 1: wrapper-visible data, but owner unclear
Pattern:

```text
many wrapper/helper functions see the right object
  -> ownership is still unclear
  -> hooks keep confirming only that the object exists somewhere
```

Best move:
- stop widening wrapper hooks
- move to the first reducer, retained owner, or first consumer that changes durable state

### Pattern 2: wire visibility exists, but plaintext truth is elsewhere
Pattern:

```text
requests or packets are visible
  -> transport logs show symptoms
  -> field ownership or normalized structure still unclear
```

Best move:
- stop treating the wire as the primary truth surface
- move to the nearest serializer, parser, plaintext owner, or state reducer that explains the wire object

### Pattern 3: callback storm, but only one consumer matters
Pattern:

```text
many callbacks fire
  -> multiple listeners appear relevant
  -> only one consumer actually changes the later policy/state
```

Best move:
- stop cataloging every callback
- hook registration plus the first consequence-bearing consumer
- freeze the first durable state edge that follows

### Pattern 4: traces are broad, but branch choice is still unresolved
Pattern:

```text
DBI/trace output exists
  -> lots of events are visible
  -> no one truth boundary has been selected yet
```

Best move:
- reduce the question to one ownership, reducer, serializer, queue, or consumer boundary
- then use the trace only to place a smaller hook family there

### Pattern 5: current hook point is real but semantically late
Pattern:

```text
a hook confirms the visible effect
  -> but it cannot distinguish cause families
  -> compare runs still look almost identical there
```

Best move:
- move upstream to the earliest boundary that still predicts the same effect
- do not keep enriching the semantically late hook with more fields and logs

## 7. Failure modes this note helps prevent
- choosing hooks by convenience rather than by truth boundary
- logging every visible helper instead of choosing one smaller hook family
- staying on wrappers, UI handlers, or broad transport logs after they stop shrinking the question
- confusing “this function sees the data” with “this is the best observation surface”
- collecting traces without defining how a better surface would be recognized
- failing to leave ordinary hook-placement work once the case has become replay, reverse-causality, or topology-relocation shaped

## 8. Minimal operator checklist
- What exact question should the next hook answer?
- What are the plausible observation surfaces?
- Which one is the smallest truthful boundary?
- What minimal hook family is enough there?
- What compare boundary will tell me whether this was the right surface?
- If this surface works, which narrower next note does it hand off to?

If those answers are still vague, the case probably needs a broader runtime-behavior pass first.

## 9. Relationship to nearby pages
Use this page when the bottleneck is:
- **which observation surface and hook family should be chosen next**

Then route outward based on what becomes true:
- if the question is still broad runtime answerability or observability framing:
  - `topics/runtime-behavior-recovery.md`
- if the behavior is now too fragile and the real decision is capture stability:
  - `topics/record-replay-and-omniscient-debugging.md`
- if one suspicious late effect is already stable enough to walk backward from:
  - `topics/causal-write-and-reverse-causality-localization-workflow-note.md`
- if the case is actually target-specific now:
  - `topics/mobile-protected-runtime-subtree-guide.md`
  - `topics/browser-runtime-subtree-guide.md`
  - `topics/native-practical-subtree-guide.md`
  - `topics/protocol-firmware-practical-subtree-guide.md`
  - `topics/protected-runtime-practical-subtree-guide.md`
- if the remaining work is evidence packaging and durable comparison:
  - `topics/analytic-provenance-and-evidence-management.md`

## 10. What this page adds to the KB
This page repairs a practical gap in the runtime-evidence branch.

Before this note, the branch could already explain:
- why runtime evidence matters
- why replay matters when behavior is fragile
- how to localize one causal boundary once a late effect is already visible

What it lacked was the earlier practical bridge for cases where:
- runtime work is clearly needed
- but the right observation surface is still unclear
- and the analyst must choose one smaller hook family before replay or reverse-causality work becomes meaningful

That gap now has a dedicated workflow note.

## 11. Source footprint / evidence note
Grounding for this page comes from:
- `topics/runtime-behavior-recovery.md`
- `topics/runtime-evidence-practical-subtree-guide.md`
- `topics/record-replay-and-omniscient-debugging.md`
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`
- `topics/analytic-provenance-and-evidence-management.md`
- `topics/notebook-and-memory-augmented-re.md`
- `sources/runtime-evidence/2026-03-14-record-replay-notes.md`
- `sources/runtime-evidence/2026-03-16-causal-write-and-reverse-causality-workflow-notes.md`

The page stays conservative:
- it does not assume one tracing or hook framework is universally best
- it does not collapse target-specific topology-relocation problems into ordinary hook placement
- it treats hook placement as a workflow decision about truth boundaries, not as a tool-feature catalog

## 12. Bottom line
When runtime work is clearly necessary but the next hook point is still unclear, the high-value move is not “instrument more things.”

It is to choose the smallest truthful observation surface, place one minimal hook family there, and use that result to hand the case to a narrower next task.