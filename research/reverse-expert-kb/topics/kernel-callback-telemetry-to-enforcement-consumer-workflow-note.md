# Kernel Callback Telemetry to Enforcement-Consumer Workflow Note

Topic class: concrete workflow note
Ontology layers: protected-runtime practice branch, anti-cheat-adjacent protected-runtime seam, kernel telemetry to policy bridge
Maturity: structured-practical
Related pages:
- topics/protected-runtime-practical-subtree-guide.md
- topics/anti-tamper-and-protected-runtime-analysis.md
- topics/watchdog-heartbeat-to-enforcement-consumer-workflow-note.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/integrity-check-to-tamper-consequence-workflow-note.md
- topics/protected-runtime-observation-topology-selection-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/environment-differential-diagnosis-workflow-note.md

## 1. Why this page exists
This page exists for a recurring protected-runtime stall pattern in anti-cheat-adjacent or privilege-heavy monitoring cases:
- callback registration surfaces are easy to find
- callback families are easy to label
- the analyst can already tell the target is gathering kernel telemetry
- but the investigation still stalls because registration is being mistaken for behavioral ownership

The KB already had two strong neighboring surfaces:
- a general native note for callback-registration to event-loop consumer proof
- a protected-runtime note for watchdog / heartbeat to enforcement-consumer reduction

What it still lacked was one narrower note for cases where:
- the analyst is dealing with kernel callback telemetry rather than ordinary native async delivery
- registrations such as process/thread/image/object callbacks are already visible
- yet the first reducer, queue, service handoff, or policy object that turns telemetry into protection behavior is still missing

A compact operator shape for this case is:

```text
one callback family is visible
  -> separate registration from actual trigger path
  -> isolate the first telemetry reducer or carrier
  -> prove one enforcement-relevant consumer
  -> route toward a quieter next target
```

This is not the same as:
- broad anti-cheat taxonomy
- a generic kernel-driver reversing guide
- a bypass cookbook
- a pure Windows callback reference page

It is the practical task of moving from visible callback registration to the first consumer that actually makes the telemetry matter.

## 2. Target pattern / scenario
### Representative target shape
Use this page when most of the following are true:
- a kernel driver or privileged monitor already appears to register one or more callback families such as process, thread, image, object-handle, registry, or related event surfaces
- reversing has already localised registration code, callback metadata, or trigger-side helper paths
- the analyst still cannot say which state object, rights filter, queue, IOCTL path, shared buffer, service handoff, or later reducer first predicts protected behavior
- the next useful output is not more callback inventory, but one telemetry-to-enforcement proof object
- the target is protected-runtime shaped enough that privilege, timing, and observation asymmetry matter materially

Representative cases include:
- anti-cheat or anti-tamper drivers that register object-handle callbacks and then later downgrade, correlate, or report suspicious access
- security-sensitive drivers that consume process/thread/image notifications but do not enforce directly inside the registration callback
- cases where a callback fires often, but the meaningful analyst object is a later reducer, message handoff, or policy bucket outside the callback itself
- cases where callback setup timing or race windows matter to later behavior, so registration alone does not explain the result

### Analyst goal
The goal is **not** to enumerate every callback API used by the driver.
It is to:
- pick one callback family that plausibly matters
- separate registration from real trigger delivery
- isolate the first telemetry reducer or enforcement-relevant consumer
- prove one later behavior depends on it
- return one justified next route

## 3. The first five questions to answer
Before widening the map, answer these:

1. **Which callback family is actually closest to the protected behavior I care about: process, thread, image, handle, registry, file, or another event family?**
2. **Is the useful object the callback itself, or a later telemetry carrier such as a flag, rights mask change, queue item, ring buffer, IOCTL payload, or service message?**
3. **Does the target appear to enforce immediately in callback context, or only after reduction into another worker, service, or policy bucket?**
4. **Does callback setup timing or lifecycle matter enough that registration-time and effect-time must be treated separately?**
5. **What smallest compare pair would prove the first enforcement-relevant consumer: callback firing vs callback suppressed, producer intact vs consumer changed, early-window vs settled-state, or low-noise environment vs normal run?**

## 4. Core claim
In callback-heavy protected-runtime cases, the right unit of progress is usually:
- one callback family
- plus one first reducer or enforcement-relevant consumer

A practical sequence is:

```text
name one callback family
  -> trace one real trigger path
  -> find the first telemetry reducer / carrier
  -> prove one enforcement-relevant consumer downstream
  -> stop once one quieter next target exists
```

The useful milestone is not:
- finding `PsSet*` registration once
- labeling one `ObRegisterCallbacks` call site
- cataloging all callback entries in one driver

The useful milestone is:
- one proved callback-telemetry-to-enforcement-consumer path

## 5. Common callback-to-enforcement shapes
### A. Callback -> local rights modification
Use when:
- the callback directly strips rights, rewrites access masks, or records granted-vs-requested state
- the practical question is whether that local modification already explains behavior

Why it helps:
- it distinguishes immediate protection-side filtering from later service-side policy

### B. Callback -> reducer helper -> policy/state bucket
Use when:
- raw callback events are noisy or high-volume
- one smaller suspicious/clean bucket, score, or mode object predicts later behavior

Why it helps:
- it prevents endless callback inventory without a smaller operational state

### C. Callback -> queue / shared buffer / IOCTL handoff
Use when:
- the driver gathers telemetry in kernel context
- but later service-owned or game-owned logic decides what matters

Why it helps:
- it keeps the analyst from overtrusting the callback body when the real consumer lives elsewhere

### D. Process-create callback -> object callback setup -> later protection result
Use when:
- process lifecycle timing or startup windows matter
- the callback family is part of a setup chain rather than the final behavior by itself

Why it helps:
- it forces separate treatment of registration timing, setup completion, and later effect

### E. Multi-callback aggregation -> one first decision point
Use when:
- several callback families exist together
- the meaningful analyst object is one common reducer, score, or action selector

Why it helps:
- it prevents overfitting the story to whichever callback was easiest to find first

## 6. Practical workflow

### Step 1: anchor the protected behavior first
Write one explicit sentence such as:

```text
enforcement symptom:
  a protected process survives startup, but suspicious handle requests lose rights and a later service path records or reacts to that reduction.
```

Good symptom shapes:
- access-right downgrade
- denied or degraded process interaction
- delayed kick / exit / refusal after kernel-observed events
- later service-owned decision after kernel telemetry accumulation
- startup-window race or early unprotected interval that later closes

### Step 2: choose one callback family
Prefer the family with:
- the clearest relation to the visible symptom
- the narrowest likely path to a later policy consumer
- the best official or structural grounding

Examples:
- object callbacks for handle-rights modification
- process callbacks for startup-window or protected-process lifecycle setup
- image/thread callbacks for telemetry accumulation rather than direct enforcement

### Step 3: separate registration from real delivery
Label the chain as:
- registration site
- trigger condition
- callback execution path
- first telemetry carrier or reducer
- first enforcement-relevant consumer
- later effect

Practical rule:
- if the current map ends at registration metadata, it is still too early

### Step 4: identify the first telemetry carrier that survives callback scope
Ask:

```text
what first object survives beyond callback execution and predicts later behavior better than the callback label itself?
```

Good candidates:
- access-mask rewrite or granted-rights result
- suspicious/clean flag or score bucket
- event queue node or ring-buffer entry
- IOCTL payload or shared-memory record
- service notification or policy-state update

Bad candidates:
- loop-local or callback-local temporary fields with no later dependency
- every helper the callback calls
- registration metadata alone

### Step 5: prove one enforcement-relevant consumer
Use one narrow proof move:
- show that the callback still fires, but changing the downstream carrier or consumer changes the later effect
- correlate one queue item, rights mask, or policy bucket with later deny/degrade/kick behavior
- compare early-window vs settled-state behavior when callback setup timing matters
- show that registration exists, but only one later reducer or service handoff predicts the behavior under study

The useful proof is not merely “kernel telemetry exists.”
It is “this consumer is the first thing that makes this telemetry matter.”

### Step 6: choose the next route deliberately
Once one callback-to-consumer path exists, route the case:
- **stay local** when one rights filter, reducer, or queue handoff is narrow enough to support direct continuation
- **move to observation-topology selection** when the current observation posture is still too visible or semantically late for trustworthy proof
- **move to integrity/tamper consequence reduction** when callback telemetry has already collapsed into one later verdict or tripwire object
- **move to environment-differential diagnosis** when callback behavior still depends more on privilege, lifecycle, or deployment realism than on the code path itself
- **move to native callback/event-loop continuation** when the kernel side is already reduced and the remaining ambiguity now lives in an ordinary userland async consumer

## 7. Representative scenario families
### A. Object-handle callback -> access-mask downgrade -> later protected-process stability
Use when:
- suspicious handle opens are the visible issue
- the callback likely modifies granted or desired rights
- the next task is proving whether the rights result itself is enough or whether a later consumer matters more

Why it helps:
- it centers the analyst on the smallest rights-bearing consequence object

### B. Process/thread/image callbacks -> telemetry queue -> service-owned policy action
Use when:
- kernel callbacks gather broad event streams
- yet the real protection behavior happens after aggregation or handoff

Why it helps:
- it shifts the effort from callback inventory to one service-facing reducer

### C. Process-create notification -> callback setup chain -> early-window race
Use when:
- the timing of registration or protection establishment matters
- the analyst needs to compare startup phases rather than assume a steady-state design

Why it helps:
- it turns timing ambiguity into one compare-run problem instead of vague speculation

### D. Multi-callback anti-cheat driver -> one suspicion score or verdict bucket
Use when:
- several callback families are present and all look relevant
- one score, verdict, or mode bucket predicts later user-visible action better than any single callback by itself

Why it helps:
- it reduces privilege-heavy telemetry sprawl into one smaller decision object

## 8. Representative scratch schemas
### Minimal callback-to-consumer note
```text
enforcement symptom:
  ...

callback family:
  ...

registration site:
  ...

first telemetry carrier / reducer:
  ...

first enforcement-relevant consumer:
  ...

later effect:
  ...

next route if confirmed:
  ...
```

### Timing-sensitive compare note
```text
baseline condition:
  ...

changed condition:
  ...

callback setup / trigger boundary:
  ...

first stable downstream divergence:
  ...

later effect difference:
  ...
```

### Tiny thought model
```python
class CallbackTelemetryReduction:
    symptom = None
    callback_family = None
    registration = None
    carrier = None
    consumer = None
    effect = None
    next_route = None
```

## 9. Failure modes
### Failure mode 1: the analyst keeps proving registrations but not behavior
Likely cause:
- registration metadata is being mistaken for the first meaningful consumer

Next move:
- force the map to include one telemetry carrier that survives callback scope

### Failure mode 2: the callback body is heavily read, but later behavior is still unexplained
Likely cause:
- the real first consumer is a queue, service handoff, or later reducer outside callback context

Next move:
- search for state or message objects produced by the callback rather than more trigger-side labeling

### Failure mode 3: the target behaves differently only at startup
Likely cause:
- registration timing or setup windows matter materially

Next move:
- turn the problem into an early-window vs settled-state compare pair

### Failure mode 4: several callback families all look important
Likely cause:
- the true next object is an aggregator or decision bucket rather than another callback family

Next move:
- search for the first common reducer or policy carrier

### Failure mode 5: userland and kernelland evidence are both partial
Likely cause:
- the observation posture is still too distorted or late

Next move:
- route to protected-runtime observation-topology selection before deepening the callback map

## 10. How this page connects to the rest of the KB
Use this page when the bottleneck is:
- **kernel callback telemetry is already visible, but the first reducer or consumer that turns that telemetry into protected behavior is still unclear**

Then route outward based on what becomes clearer:
- to `topics/protected-runtime-practical-subtree-guide.md` when the broader branch classification still needs recalibration
- to `topics/watchdog-heartbeat-to-enforcement-consumer-workflow-note.md` when the case is less callback-heavy kernel telemetry and more repeated monitor/liveness enforcement
- to `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md` when the kernel side is already reduced enough and the remaining ambiguity now lives in ordinary async userland delivery
- to `topics/integrity-check-to-tamper-consequence-workflow-note.md` when callback outputs have already collapsed into one later verdict/tripwire object
- to `topics/protected-runtime-observation-topology-selection-workflow-note.md` when the current posture still makes proof too noisy or too visible
- to `topics/environment-differential-diagnosis-workflow-note.md` when privilege level, startup timing, or deployment realism still dominate evidence trust

## 11. What this page adds to the KB
This page adds a missing practical rung between:
- broad protected-runtime / anti-cheat conceptual treatment, and
- broader callback or watchdog reduction patterns elsewhere in the KB

Instead it emphasizes:
- registration vs delivery separation
- callback telemetry as producer-side evidence
- one first carrier or reducer
- one first enforcement-relevant consumer
- one deliberate stop rule

That gives the protected-runtime branch a concrete answer to a common operator question:
**I found the kernel callback registration — what is the first thing that makes it matter?**

## 12. Source footprint / evidence note
Grounding for this page comes from:
- Microsoft Learn callback API references, especially `PsSetCreateThreadNotifyRoutine`
- SpecterOps work on Windows kernel callbacks and object-callback trigger paths
- public anti-cheat architecture analysis describing callback telemetry as one layer in a larger protection stack
- the timing paper `Fast and Furious: Outrunning Windows Kernel Notification Routines from User-Mode`
- `sources/protected-runtime/2026-03-22-kernel-callback-telemetry-enforcement-notes.md`

The page intentionally stays conservative:
- it does not assume one anti-cheat architecture stands for all others
- it does not assume kernel callbacks always enforce locally
- it does not claim undocumented internals without stronger support
- it treats callback-heavy protected-runtime analysis as a workflow problem of finding the first behavior-changing consumer

## 13. Topic summary
Kernel callback telemetry to enforcement-consumer reduction is a practical workflow for protected-runtime cases where callback registration is already visible, but the first behavior-changing consumer is still hidden.

It matters because many analysts can find the registration site, but still cannot prove which rights filter, queue, reducer, service path, or policy object actually turns that telemetry into a real protected behavior.
