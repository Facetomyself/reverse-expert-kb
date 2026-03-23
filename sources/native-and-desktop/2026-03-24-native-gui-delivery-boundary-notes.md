# 2026-03-24 Native GUI delivery-boundary notes

Focus:
- tighten the native GUI practical continuation around one thinner operator stop rule
- prevent over-collapsing Win32 subclass visibility and Qt signal visibility into generic “framework found” proof
- preserve a stricter delivery-boundary split for per-window subclass ownership and `AutoConnection` / queued Qt delivery

## Why this source pass was chosen
Recent autosync work had already invested in the native GUI branch.
That made another broad GUI wording pass a poor use of this run.

This run instead used a real external multi-source search attempt and then targeted one thinner practical gap:
- analysts can still stop too early once they see `CallWindowProc`, `SetWindowLongPtr`, `emit`, or a recovered slot graph
- but those landmarks still do not tell them whether they have the right per-window owner or the right first consumer boundary

The goal was therefore not to restate Win32 or Qt basics.
It was to preserve a more honest stop rule for real cases.

## Search-layer attempt
Executed through:
- `skills/search-layer/scripts/search.py`
- explicit sources: `exa,tavily,grok`

Queries used:
1. `Win32 message pump subclass SetWindowLongPtr CallWindowProc reverse engineering workflow first consumer`
2. `Qt signal slot queued connection event loop reverse engineering first consumer practical`
3. `reverse engineering GUI message loop callback dispatch first meaningful consumer Windows Qt`

Raw log:
- `sources/native-and-desktop/2026-03-24-native-gui-consumer-search-layer.txt`

## Search-source outcome
Observed source outcome in the retained search artifact:
- Exa returned usable results
- Tavily returned usable results
- Grok emitted JSON-parse errors in this run artifact and did not contribute retained hits

This still counts as a real multi-source attempt because all three requested sources were explicitly invoked.
The KB update should therefore record Grok as attempted-but-failed for this run rather than silently omitting it.

## High-signal source-backed reminders

### 1. Microsoft Learn — Using Window Procedures
URL:
- https://learn.microsoft.com/en-us/windows/win32/winmsg/using-window-procedures

High-signal reminder:
- the message loop and broad `WndProc` structure are routing landmarks
- the real proof still lives in one concrete `WM_*` branch or follow-on handler that changes state or chooses later behavior

Operator consequence:
- do not stop at `DispatchMessage`, class `WndProc`, or `DefWindowProc`
- treat them as framework reduction boundaries only until one narrower consumer-to-effect chain is proved

### 2. Raymond Chen — original proc must belong to the window actually subclassed
URL:
- https://devblogs.microsoft.com/oldnewthing/20090507-00/?p=18333

High-signal reminder:
- the saved original procedure is specific to the window instance that was subclassed
- using some other window’s saved procedure is wrong

Operator consequence:
- `CallWindowProc` visibility is still not enough
- the analyst should preserve which exact window instance and which exact subclass hop owns the decisive message family before widening into sibling controls or shared wrappers

### 3. Qt documentation — Threads and QObjects
URL:
- https://doc.qt.io/qt-6/threads-qobject.html

High-signal reminder:
- each thread has its own event loop
- objects have thread affinity
- queued delivery depends on the receiver thread’s event loop, and without a running event loop events are not delivered

Operator consequence:
- queued-vs-direct classification is not just about the signal edge label
- it also depends on receiver thread affinity and whether the receiving loop is actually alive
- this means a visible `emit` or recovered connection list may still be earlier than the first truthful consumer boundary

### 4. Woboq — queued connection internals
URL:
- https://woboq.com/blog/how-qt-signals-slots-work-part3-queuedconnection.html

High-signal reminder:
- queued delivery goes through `QMetaObject::activate`, `queued_activate`, event posting, and later `QMetaCallEvent` processing
- direct delivery is a different boundary from queued-delivery processing

Operator consequence:
- when a case is truly queued, the first meaningful proof boundary is often not the emission site
- it is one layer later: the receiver-side event-loop processing or the first slot-side reducer that changes behavior after the `QMetaCallEvent` handoff

## Resulting KB direction
This run supports a thinner practical rule inside the native GUI branch:
- **Win32:** do not treat subclass presence or `CallWindowProc` visibility as consumer proof until per-window ownership is preserved
- **Qt direct/auto cases:** the slot may already be the right first consumer boundary
- **Qt queued/auto-cross-thread cases:** treat emission as earlier framework visibility and preserve the later event-loop / receiver-side consumer boundary separately

This is a small refinement, but it changes how a real analyst decides where to stop and where to hand off next.
