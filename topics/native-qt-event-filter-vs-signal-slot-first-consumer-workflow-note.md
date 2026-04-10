# Native Qt Event-Filter vs Signal-Slot First-Consumer Workflow Note

Topic class: workflow note
Ontology layers: native baseline practical branch, GUI/event-dispatch practical continuation, runtime-evidence bridge
Maturity: emerging
Related pages:
- topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md
- topics/native-practical-subtree-guide.md
- topics/native-binary-reversing-baseline.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/causal-write-and-reverse-causality-localization-workflow-note.md

## 1. What this workflow note is for
This note covers a narrower Qt-heavy GUI case inside the native branch:
- `installEventFilter(...)` and `eventFilter(...)` are visible
- the target object’s `event(...)` or type-specific event handler is visible
- one or more signals are emitted near the same path
- one or more slots are visible or recoverable
- but the analyst still has not proved which layer is the **first behavior-changing consumer**

This is not a broad Qt architecture note.
It is the thinner practical continuation for cases where event-filter plumbing, handler logic, and signal-slot routing all look plausible enough, yet the real behavior-bearing boundary still lies one step later than the prettiest framework hook.

The question this note answers is:

```text
when both filter plumbing and signal-slot routing are visible,
which smaller proof object actually owns the first behavior-changing consequence?
```

## 2. When to use this note
Use this note when most of the following are true:
- the case is native desktop / rich-client / Qt-heavy rather than browser/mobile/protected-runtime first
- the broad async-ownership break has already narrowed into GUI/event dispatch
- one target object, one event family, or one visible UI-trigger family is already plausible enough
- `eventFilter(...)` visibility alone still feels too early
- signal discovery alone still feels too broad
- the real bottleneck is deciding whether ownership is at the filter, the target object’s own handler, the emit site, or one later delivered slot

Typical triggers:
- “I found `installEventFilter(...)`, but I still do not know whether the filter actually owns the behavior.”
- “I can see the target widget’s `event(...)` and an emitted signal, but I do not know whether the filter or one later slot first changes state.”
- “I found a signal and several slots, but I have not frozen whether delivery is direct or queued.”
- “The path looks cross-thread, so I suspect queued delivery, but I have not proved receiver affinity or event-loop liveness yet.”

Do **not** start here when:
- the case is still broad Win32/Cocoa GUI routing rather than specifically Qt-shaped
- no plausible target object or event family is narrowed yet
- the real problem is still route overabundance, service-owned worker ambiguity, or broader callback/event-loop mapping
- the case is really mobile/WebView/protected-runtime shaped rather than ordinary Qt/native GUI work

## 3. Core claim
In Qt-heavy GUI work, the decisive proof usually is not:
- “I found `installEventFilter(...)`”
- “I saw `eventFilter(...)` fire”
- “I found the signal emission site”
- “I recovered a `QObject::connect(...)` edge”

The decisive proof is usually one of these smaller truth objects:
- the filter **really owns event fate** because it returns `true` or rewrites/retargets the event in a way that predicts the later effect
- the target object’s own `event(...)` or type-specific handler is the first truthful reducer because the filter falls through
- the signal emission site is the last truthful synchronous reducer before the decisive consumer boundary
- one slot is the real first consumer, with delivery mode proved as direct or queued under the actual receiver affinity and receiver-loop reality

The practical ladder is:

```text
filter topology
 -> filter-owned fate or fall-through
 -> receiver-side handler truth
 -> signal-edge truth
 -> direct/queued delivery truth
 -> first consequence-bearing slot or later reducer
```

## 4. Why this thinner continuation matters
The broader native GUI workflow note already preserves a generic rule that Qt event-filter visibility is weaker than consumer truth.
This page exists because real Qt cases keep lying in a specific way:
- filters are easy to recover
- object handlers are easy to recover
- signals are easy to enumerate
- but the first behavior-changing consumer is still ambiguous because the analyst has not frozen fate, affinity, or delivery truth

This thinner continuation keeps four different stories apart:
- **filter story** — who sees the event first
- **fate story** — who actually stops, rewrites, or retargets it
- **delivery story** — whether a later slot is direct or queued
- **consumer story** — who first changes behavior in a way that predicts the downstream effect

## 5. Practical source-backed reminders
The retained Qt documentation supports several operator reminders.

### A. `eventFilter(...)` visibility is not automatic filter-owned behavior truth
Qt’s event-system documentation preserves that an event filter gets to process events before the target object does, but if all filters return `false`, the event is still sent to the target object itself.
If one filter returns `true`, the target and any later event filters do not get to see the event at all.

Practical rule:
- **filter hit != filter-owned fate**
- a filter becomes the truthful first consumer only when it actually stops, rewrites, or retargets the event in a way that predicts later behavior
- if it returns `false`, keep reducing into the later object handler, signal edge, or slot rather than freezing the map at filter visibility

### B. Application-global filters are usually reduction boundaries first
Qt also preserves that filters installed on `QApplication` or `QCoreApplication` run before object-specific filters.
They are powerful and expensive.

Practical rule:
- global filter visibility often proves the relevant event family early
- but unless that global filter itself changes fate, it is usually a reduction boundary rather than the first behavior-changing consumer
- do not flatten “the app-wide filter saw it” into ownership of the later state/policy/task change

### C. Signals are usually immediate; queued delivery must be proved, not assumed
Qt’s signals-and-slots documentation preserves that connected slots are usually executed immediately when the signal is emitted.
Queued connections are the special case where execution continues after `emit` and slots run later.

Practical rule:
- **signal found != queued truth**
- a visible emit site may still be the last synchronous reducer before one immediately entered slot
- only treat the path as later/queued once connection-mode truth is frozen

### D. `AutoConnection` is receiver-affinity truth
Qt’s thread documentation preserves that `AutoConnection` behaves like direct delivery when the signal is emitted in the thread the receiver object has affinity to, and behaves like queued delivery otherwise.

Practical rule:
- **connected != direct != queued**
- do not narrate `AutoConnection` as “cross-thread shaped, so queued” until receiver affinity is actually recovered
- when receiver affinity shows same-thread delivery, the first truthful consumer may still be immediate slot entry rather than later event-loop delivery

### E. Queued delivery needs receiver-loop liveness
Qt’s thread documentation preserves that queued connections run when control returns to the event loop of the receiver’s thread, and that if no event loop is running, events will not be delivered.

Practical rule:
- **queued != delivered**
- even after proving a queued edge, keep receiver-loop liveness separate from actual slot entry
- a plausible queued connection with no running receiver loop is weaker than one delivered slot or later consequence-bearing reducer

### F. Event-filter topology is thread-constrained
Qt’s thread documentation preserves that event filters are supported in all threads only if the monitoring object lives in the same thread as the monitored object.

Practical rule:
- **filter class exists != current filter topology is valid for this object pair**
- if `moveToThread(...)`, worker-object patterns, or thread-owned UI helpers are in play, freeze live object affinity before narrating filter ownership

## 6. The boundaries to mark explicitly

### A. Filter topology truth
Capture:
- which target object is being monitored
- which filter object is attached
- whether the filter relationship is object-local or app-global
- whether the monitoring and monitored objects live in the same thread

This is not yet ownership of behavior.
It is only the truthful starting topology.

### B. Filter-owned fate truth
Capture:
- whether the filter returns `true` or `false`
- whether it suppresses, rewrites, or retargets the event
- whether a global filter merely logs/classifies or actually blocks/redirects

If the filter returns `false` and leaves the event path intact, do not stop here.

### C. Receiver-side handler truth
Capture:
- which object-local `event(...)` or type-specific handler first meaningfully handles the event after filter fall-through
- whether that handler changes state directly, chooses one narrower branch, or emits one decisive signal

This is often the first truthful reducer when the filter does not own fate.

### D. Signal-edge and delivery-mode truth
Capture separately:
- which signal is emitted
- which receiver or receiver set is actually relevant
- whether the delivery mode is direct, queued, or `AutoConnection` that must still be resolved via receiver affinity
- whether the receiver thread has a live event loop when queued delivery is the model

Do not collapse these into one vague “signal/slot path exists” claim.

### E. First consequence-bearing consumer truth
Capture:
- one exact slot or later reducer
- one write, branch, enqueue, or state/policy/task decision that predicts the downstream effect better than framework labels do

This is the point where the map stops being Qt-framework narration and becomes behavior proof.

## 7. Default workflow

### Step 1: choose one event family and one downstream effect
Good candidates:
- one key/mouse/UI action
- one object-local event type
- one interaction that predictably gates a later mode/state/task/request change

Bad candidates:
- “all filters on this widget”
- “all signals from this object”
- “everything connected to this form/controller”

### Step 2: freeze filter topology before interpreting it
Recover:
- the exact target object
- the exact filter object
- whether the filter is object-specific or application-global
- whether thread affinity even permits this filter relationship to be truthful

### Step 3: prove filter-owned fate or explicit fall-through
Ask:
- does `eventFilter(...)` return `true` for the event family that matters?
- if not, what later object handler still sees the event?
- if yes, what exact rewrite, retarget, or suppression makes the filter behaviorally real?

### Step 4: localize the receiver-side handler that matters
If the filter falls through, recover one smaller receiver-side reducer:
- one `event(...)` branch
- one type-specific handler
- one state write or branch that decides which signal or downstream action family matters next

### Step 5: classify direct vs queued truth honestly
Freeze separately:
- the relevant receiver object
- that receiver’s thread affinity
- the effective connection mode
- receiver event-loop liveness when queued delivery is still the model

Keep this ladder visible:

```text
signal emitted
  != connection exists
  != AutoConnection resolved
  != queued delivery became possible
  != slot actually ran
```

### Step 6: prove the first consequence-bearing consumer
Prefer the slot or later reducer that:
- writes durable state
- selects a later action family
- queues or triggers the next meaningful worker/request/policy path
- suppresses or transforms the path in a way that explains the later compare-run effect

## 8. Minimal proof tactics that work well here
- breakpoint/log on one concrete `eventFilter(...)` branch for one event family, not the whole filter class
- compare whether the relevant path still reaches the receiver object when the filter returns `false` versus `true`
- breakpoint/log on one receiver-side `event(...)` or type-specific handler that still sees the event after filter fall-through
- log one specific signal emission site and one specific slot, then decide whether control stayed synchronous or resumed later through queued delivery
- recover receiver affinity and receiver-loop liveness before narrating queued-slot ownership
- when queued delivery remains ambiguous, prove one downstream state write or enqueue from the slot rather than cataloging sibling receivers

## 9. Common scenario patterns

### Pattern 1: Object-specific filter that only inspects, then falls through
Symptoms:
- `eventFilter(...)` visibly runs
- it returns `false` for the event family that matters
- a later object-local handler still emits the decisive signal

Best move:
- treat the filter as reduction only
- freeze the receiver-side handler or later signal edge instead of overclaiming filter ownership

### Pattern 2: Global application filter that makes the event easy to find, but not behaviorally real
Symptoms:
- app-wide filter sees the event before everything else
- the filter mainly logs, normalizes, or classifies
- later widget/controller logic still owns the actual state change

Best move:
- keep the app-global filter as earlier routing truth
- continue into the later object-local handler or slot that first changes behavior

### Pattern 3: `AutoConnection` edge that looks queued until affinity is checked
Symptoms:
- several signals and slots are visible
- the connection style looks async by inspection
- no one has frozen the receiver object’s thread affinity yet

Best move:
- classify `AutoConnection` using actual receiver affinity first
- only then decide whether the first truthful consumer is immediate slot entry or later event-loop delivery

### Pattern 4: Queued slot exists, but receiver-loop liveness is the real liar
Symptoms:
- the edge really is queued
- slot delivery is assumed from the existence of the connection alone
- receiver thread lifecycle or event-loop startup is shaky

Best move:
- separate queued-edge truth from delivered-slot truth
- prove one receiver-loop-liveness boundary before overreading the slot as behaviorally real

### Pattern 5: Filter owns fate, but analysts reopen the map too early
Symptoms:
- the filter returns `true` and the downstream effect disappears with it
- later object handlers and slots still look richer in pseudocode

Best move:
- stop at the filter when it is already the first truthful consumer
- only continue later if the actual analyst question has moved beyond filter-owned fate into the next smaller consequence-bearing reducer

## 10. Handoff rule
Leave this note once the main uncertainty is no longer “filter fate vs handler vs signal-slot delivery.”

Common next steps:
- move to `topics/causal-write-and-reverse-causality-localization-workflow-note.md` when one Qt consumer is already known and the remaining bottleneck is the first decisive write/reducer behind a later effect
- move to `topics/runtime-behavior-recovery.md` when broader observability, compare-run design, or event-loop timing strategy becomes the real need
- move back outward to `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md` when the case stops being specifically Qt event-filter-vs-slot shaped and needs the broader cross-framework GUI routing again

## 11. Failure modes this note helps prevent
- stopping at `installEventFilter(...)` or `eventFilter(...)` visibility as if that already proved behavioral ownership
- treating app-global filters as if they automatically own later object-local consequences
- assuming every visible signal implies queued delivery
- assuming `AutoConnection` means “probably later” without freezing receiver affinity
- assuming queued connection truth already proves slot delivery without checking receiver-loop liveness
- cataloging many signals/slots before grounding one first consequence-bearing consumer

## 12. Compact operator checklist
- Pick one event family and one downstream effect.
- Freeze one exact filter topology: target object, filter object, and thread validity.
- Ask whether the filter owns fate or merely falls through.
- If it falls through, recover one truthful receiver-side handler.
- Keep `signal emitted != connection exists != delivery-mode truth != slot delivered` visible.
- Resolve `AutoConnection` by receiver affinity, not by intuition.
- Treat queued delivery as weaker than delivered-slot truth until receiver-loop liveness is proved.
- Stop at the first consumer that actually changes behavior, not at the prettiest framework hook.

## 13. Topic summary
Qt-heavy GUI reversing often stalls because recovered filter plumbing and recovered signal-slot edges both look like the answer.

The practical cure is to separate filter topology, filter-owned fate, receiver-side handler truth, delivery-mode truth, and first consequence-bearing consumer truth. That keeps `eventFilter(...)`, `emit`, and `connect(...)` from impersonating the one smaller proof object that actually predicts behavior.
