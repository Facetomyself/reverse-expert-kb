# Native Inotify/Fanotify First Event Consumer Workflow Note

Topic class: workflow note
Ontology layers: workflow/sensemaking, runtime-evidence bridge, native baseline practical branch
Maturity: emerging
Related pages:
- topics/native-practical-subtree-guide.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/runtime-behavior-recovery.md
Related source notes:
- sources/native/2026-04-04-native-inotify-fanotify-first-event-consumer-notes.md

## 1. What this workflow note is for
This note covers a recurring Linux-native async case where the analyst has already reduced the target into a filesystem-watch shape, but the remaining bottleneck is narrower than broad callback/event-loop routing.

Typical symptoms:
- `inotify_init*`, `inotify_add_watch`, `fanotify_init`, `fanotify_mark`, or equivalent watch-registration helpers are visible
- the analyst keeps stopping at registration sites or at one watched path instead of proving which first event record becomes behaviorally real
- one watcher appears to explain later behavior, but it is unclear whether the real owner is watch registration, one event record, one parser/dispatcher, or one immediate downstream consumer

The goal is to move from:

```text
one visible inotify/fanotify registration and one plausible watched object
```

to:

```text
one proved chain from watch registration
through one concrete event record
into one first event-owned consumer
and one downstream effect
```

## 2. When to use this note
Use this note when most of the following are true:
- the target is Linux-native enough that filesystem watch APIs are already a plausible pivot
- broad callback/event-loop ownership is no longer the main bottleneck
- the remaining uncertainty is about which first event record or watch callback actually matters
- one narrow runtime proof against one watched path or event family would collapse a lot of uncertainty

Common shapes include:
- inotify-based config reload, dropper, watchdog, or plugin discovery flows
- fanotify-based monitoring or filtering where file events appear to trigger later analysis/decision paths
- malware or protected tools that monitor one directory or path family and react asynchronously to changes
- service/control logic where a watched path is visible but the first event-owned consumer is not

Do **not** use this as the primary note when:
- the broad async path is still unclear and generic callback registration is the better first stop
- the case is really socket-, timer-, GUI-, or wait-shaped rather than filesystem-event-shaped
- the main uncertainty is later application semantics after one first event consumer is already known

## 3. Core claim
For filesystem-watch cases, **watch registration is weaker than one concrete event record**, and one event record is weaker than proving the first event-owned consumer that changes behavior.

The wrong stopping point is often:

```text
a watched path exists == later behavior is explained
```

The better question is:

```text
Which first inotify/fanotify event record actually becomes the first consequence-bearing consumer,
and what downstream effect does it own?
```

## 4. Boundary objects to keep separate
### A. Watch-registration truth
This is where the target creates the monitoring instance and registers one watch/mark.

Typical anchors:
- `inotify_init`, `inotify_init1`, `inotify_add_watch`
- `fanotify_init`, `fanotify_mark`

What to capture here:
- one monitor FD / instance identity
- one watched path or object family
- one mask / mark configuration

This is weaker than event-consumer truth.

### B. Event-record truth
From the Linux man pages:
- inotify events are read from the inotify file descriptor as `struct inotify_event` records
- fanotify returns event metadata records on the fanotify file descriptor
- inotify rename-related events are connected by a shared `cookie`
- successive identical unread inotify events may be coalesced into one returned record
- inotify queues can overflow and emit `IN_Q_OVERFLOW`

What to capture here:
- one concrete event record
- one mask / event-type family
- one path/object identity if recoverable
- whether the current record could be coalesced, paired, or overflow-adjacent rather than a one-to-one reflection of every underlying filesystem operation

### C. First event-owned consumer truth
This is the first parser/dispatcher/handler that turns the event record into meaningful application behavior.

Typical anchors:
- one first event-mask switch
- one path filter / allow-deny decision
- one reload/scan/launch branch
- one queue insertion or state change driven by the event
- for fanotify permission classes, one first allow/deny response path that actually decides whether later file access proceeds

### D. Effect truth
This is where the analyst proves the first event consumer actually matters.

## 5. Default workflow
### Step 1: freeze one monitor instance and one watched object family
Do not widen to every watched path.
Pick one instance with:
- a clear later effect
- one stable watched path or object class
- one event family with obvious leverage

### Step 2: separate registration from event delivery
Write the local chain explicitly:
- watch/mark registration
- event record arrival
- event parse/filter
- first event-owned consumer
- downstream effect

This prevents stopping at registration or mask inventory.

### Step 3: freeze one event family
From the docs:
- inotify events arrive as read records containing masks and names
- fanotify marks and event metadata have their own semantics and object scope
- inotify may coalesce identical unread events, preserves queue order, and uses rename cookies to pair `IN_MOVED_FROM` / `IN_MOVED_TO`
- inotify overflow (`IN_Q_OVERFLOW`) is a first-class condition, not background noise
- fanotify may identify objects by file descriptor or by FID-style records depending on report flags, so object identity may not always look like one simple path string

Practical stop rules:
- do not flatten “path is watched” into “relevant event occurred in the run that matters”
- do not overread one observed read from the monitoring FD as proof that the later behavior is owned by that event family
- do not assume one returned inotify record means a one-to-one underlying operation history when coalescing or rename pairing could already be shaping what the consumer sees
- do not treat overflow as mere observability noise if the consumer’s own behavior may already be shaped by missed events or by explicit overflow handling

### Step 4: preserve event-mask / object-scope truth
Prefer one event family with:
- stable mask bits
- a clear watched path/object interpretation
- obvious downstream leverage

If multiple masks co-occur, do not force broad taxonomy first.
One consequence-bearing event family is enough.

### Step 5: prove one first event consumer
Among candidate consumers, prefer the one that:
- predicts later behavior better than watch registration alone
- turns one event record into a state/dispatch decision
- survives compare-runs better than raw FD activity
- for fanotify permission cases, actually emits or gates the allow/deny response rather than merely logging metadata arrival

### Step 6: use one narrow runtime move
Typical minimal proofs include:
- breakpoint/log on the first event-mask/path dispatcher after `read()` from the monitor FD
- compare one run with the triggering file event against one quiet run while observing one later effect
- watch one state variable or queue that changes only after the first accepted event record
- for fanotify permission cases, freeze the first allow/deny response owner rather than stopping at metadata arrival alone

The aim is not full watcher reconstruction.
It is one proof that links registration to a first consequence-bearing event consumer.

A compact compare checklist for this seam is now worth keeping explicit:
- did the run only prove **watch registration**?
- did it prove only a **returned event record**?
- did it prove only a **coalesced/paired/overflow-shaped or permission-shaped watcher surface**?
- did it actually prove the first **event-owned consumer** that predicts later behavior?

That checklist helps keep watcher setup, returned-record truth, record-shaping semantics, and later event-owned consumer truth separate.

## 6. Practical stop rules this note preserves
- `watch registration exists != relevant event occurred`
- `one event record read != first event-owned consumer proved`
- `watched path visibility != downstream effect ownership`
- `one event family observed != full monitoring semantics recovered`
- `one returned inotify record != one complete underlying operation history`
- `coalesced/paired/overflow-shaped returned record != first event-owned consumer proved`
- `rename-related record seen != rename consumer truth unless cookie-paired handling is preserved`
- `overflow seen != harmless logging artifact`
- `fanotify metadata arrival != permission decision consumer proved`

## 7. Sources
See: `sources/native/2026-04-04-native-inotify-fanotify-first-event-consumer-notes.md`

Primary references:
- https://man7.org/linux/man-pages/man7/inotify.7.html
- https://man7.org/linux/man-pages/man7/fanotify.7.html
- https://man7.org/linux/man-pages/man2/fanotify_init.2.html
- https://man7.org/linux/man-pages/man2/fanotify_mark.2.html
- sources/native/2026-04-05-native-inotify-fanotify-delivery-and-overflow-notes.md
