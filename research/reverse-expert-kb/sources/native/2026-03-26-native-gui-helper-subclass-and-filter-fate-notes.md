# Native GUI helper-subclass identity and filter-fate notes

Date: 2026-03-26
Branch: native desktop/server practical workflows
Focus: Win32 helper-based subclass identity and Qt event-filter / direct-vs-queued delivery fate
Related pages:
- `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md`
- `topics/native-practical-subtree-guide.md`

## Why this note exists
The native GUI continuation already preserved the broad practical rule that framework hooks are often only reduction boundaries.
This run adds a narrower, more source-backed refinement for two places where analysts still overclaim first-consumer truth:
- Win32 helper-based subclass chains that look globally symmetric in pseudocode
- Qt event-filter / signal-slot cases where visible interception is weaker than actual event fate or actual delivery mode

## Source-backed reminders retained
### 1. Win32 helper-based subclass identity is not just "this callback exists"
Microsoft's `SetWindowSubclass` documentation makes the identity rule explicit:
- a helper subclass is identified by **callback address + subclass ID**
- reference data is associated with each **window handle + callback + subclass ID** combination
- helper subclassing is window-scoped and not valid across threads

Microsoft's `DefSubclassProc` documentation also keeps the chain semantics explicit:
- it calls the **next handler in a window's subclass chain**
- the last handler in that chain calls the original window procedure for the window

Practical reversing consequence:
- seeing one helper callback body is weaker than recovering the live per-window chain for the exact `HWND`
- one reused helper callback across several controls/windows is still weaker than one recovered tuple of **`HWND` + callback + subclass ID + instance-local reference data**
- `DefSubclassProc(...)` or forwarding visibility is chain-presence evidence, not automatic proof that the current helper owns the first behavior-changing consumer

Compact rule:
- **helper subclass presence != per-window owner truth**

### 2. Qt event-filter visibility is weaker than event-fate truth
Qt's event-system documentation keeps the filter boundary explicit:
- event filters run before the target object
- if all filters return `false`, the event continues to the target object
- if one filter returns `true`, the target object and later filters do not see that event
- application-global filters run before object-specific filters

Practical reversing consequence:
- `installEventFilter(...)` / `eventFilter(...)` visibility is reduction evidence, not automatic first-consumer proof
- the filter becomes the truthful first consumer only when it actually suppresses, rewrites, or retargets the event in a way that predicts later behavior
- if the filter returns `false`, the analyst should usually continue into the later object handler, event override, or slot path
- application-global filters are especially easy to overread because they see everything early, but they still may only be broad routing surfaces

Compact rule:
- **filter visibility != filter-owned fate**

### 3. Qt delivery mode must stay separate from generic signal discovery
Qt documentation also preserves a crucial immediate-vs-later split:
- normal event delivery through `event()` is immediate for the current dispatch
- `QCoreApplication::sendEvent(...)` processes immediately
- `QCoreApplication::postEvent(...)` queues work for later dispatch
- signal/slot connections may also be direct or queued depending on connection type / runtime context, so visible signal discovery is weaker than actual delivery-mode truth

Practical reversing consequence:
- do not flatten `AutoConnection` or visible signal emission into generic "queued" or generic "delivered" truth
- first decide whether the meaningful consumer runs in the current dispatch or only after later queued delivery
- if the first visible slot is immediate but behavior really changes only after a later posted event or queued slot, the later boundary may still be the first truthful consumer

Compact rule:
- **signal found != queued truth != first behavior-changing consumer**

## Operator-facing synthesis
For GUI-heavy native cases, the smallest trustworthy proof object is often one of these, not the framework hook itself:
- one exact `HWND`-scoped subclass tuple
- one filter decision that actually changes event fate
- one direct-vs-queued delivery boundary that predicts when the real consumer runs

That keeps the workflow practical:
- prefer one per-window live subclass identity over one shared helper callback body
- prefer one filter-owned fate decision over broad filter inventory
- prefer one proved immediate-vs-later delivery boundary over vague signal-slot narration

## Conservative evidence quality note
This run's search attempt was degraded:
- Tavily succeeded
- Exa returned backend `402 Payment Required`
- Grok returned `502 Bad Gateway`

The retained claims above were kept conservative and grounded mainly in official Microsoft and Qt documentation plus existing KB branch memory, not in community discussion alone.
