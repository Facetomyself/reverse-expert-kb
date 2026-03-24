# Native GUI First-Consumer Notes — 2026-03-25

Focus: thin native practical seam where broad callback/event-loop truth is already good enough, but the KB still benefits from a sharper reminder that GUI/event-framework visibility is not yet first-consumer proof.

## Search intent
This pass intentionally targeted a thinner native-desktop practical seam rather than revisiting denser protocol/runtime/malware branches.

Queries were executed through `search-layer` with explicit multi-source request:
- `--source exa,tavily,grok`

Saved raw search trace:
- `sources/native/2026-03-25-native-gui-first-consumer-search-layer.txt`

## Retained practical reminders

### 1. Win32 subclass truth is per-window and helper-ID scoped, not just “subclassing exists”
Microsoft Learn for `SetWindowSubclass` preserves several practical constraints worth carrying into the KB:
- subclass callbacks are identified by the pair `(callback address, subclass ID)`
- reference data is associated with the combination of `HWND`, callback, and subclass ID
- helper-based subclassing cannot cross threads

Operationally this supports a more specific reverse-engineering stop rule:
- do not flatten a shared subclass wrapper into one global owner
- reduce to the exact `HWND` / subclass hop / callback+ID combination that first changes behavior
- if pseudocode shows one common wrapper, still prove which instance-local reference data and which live forwarding chain owns the decisive message family

This reinforces older Raymond Chen-style per-window subclassing cautions, but the Microsoft Learn API contract is enough on its own to preserve the operator rule conservatively.

### 2. Qt signal visibility is weaker than delivery-mode and receiver-thread truth
Qt connection-type documentation preserves the key distinction:
- `AutoConnection` is resolved at emit time based on whether receiver lives in the same thread as the caller
- same-thread delivery becomes direct
- cross-thread delivery becomes queued
- queued delivery requires argument types known to the meta-object system and is delivered later through the event loop

Operationally this supports a tighter native-GUI stop rule:
- do not flatten “signal found” into “later queued consumer proved”
- do not flatten `AutoConnection` into one static delivery meaning
- first classify receiver affinity and actual delivery mode before claiming the first consumer
- in Qt-heavy reversing, a better proof object is often one receiver instance + one delivery mode + one slot that writes durable state or schedules the next narrower task

### 3. Cocoa `NSApplication sendEvent:` is an early routing hook, not automatic consumer proof
Apple’s Event Architecture material preserves the event path:
- event enters the main event loop
- `NSApplication` fetches the next event
- `NSApp sendEvent:` performs an early dispatch stage
- `NSWindow` and then `NSView` / first responder / target-action style consumers often become the actual narrower owners
- some event families are filtered and handled by `NSApp` itself, but many continue downward

Operationally this supports a narrower stop rule:
- do not stop at `NSApplication sendEvent:` merely because it is the first app-global hook
- treat it as the real consumer only when it itself suppresses, rewrites, retargets, or policy-gates the later path
- otherwise reduce further into one `NSWindow`, responder-chain receiver, target/action consumer, or service-side exported-object method

## Practical synthesis for the KB
The useful branch-memory refinement is:

```text
visible GUI/event framework entry
  -> ask whether ownership is still only framework/global
  -> reduce to one per-window, per-receiver-thread, or per-responder owner
  -> prove one first consumer that writes state, gates forwarding, or schedules the next narrower task
  -> only then hand off to reverse-causality / runtime-evidence work
```

This is valuable because GUI/event-framework cases repeatedly invite three mistakes:
- stopping at global framework hooks (`WndProc`, `sendEvent:`, signal emission)
- treating wrapper symmetry as instance symmetry
- treating Qt `AutoConnection` as a static “queued” or “not queued” label without proving receiver/thread ownership

## Sources retained conservatively
- Microsoft Learn — `SetWindowSubclass`
  - https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-setwindowsubclass
- Qt 6 docs — `Qt::ConnectionType`
  - https://doc.qt.io/qt-6/qt.html#ConnectionType-enum
- Apple Event Architecture
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/EventOverview/EventArchitecture/EventArchitecture.html

## Intended KB impact
Use this source note to justify:
- a stronger per-instance/per-responder/per-receiver stop rule in `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md`
- corresponding branch-memory updates in `topics/native-practical-subtree-guide.md`
- a top-level native-branch reminder in `index.md`
