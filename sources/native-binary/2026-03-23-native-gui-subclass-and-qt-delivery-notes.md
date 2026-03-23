# 2026-03-23 Native GUI subclass and Qt delivery notes

Focus:
- sharpen the native GUI practical continuation page with source-backed operator rules
- avoid generic GUI framework explanation
- improve proof tactics for Win32 subclass ownership and Qt direct-vs-queued delivery

## Why this source pass was chosen
Recent autosync work had already invested heavily in internal branch maintenance and other native leaves. To satisfy the anti-stagnation rule, this run prioritized a real external-research-driven pass on a still-practical but thinner native GUI branch rather than another internal canonical-sync-only sweep.

## Search intent
The target question was not “what is a window procedure?” or “what are Qt signals and slots?”
It was:
- how to avoid false ownership claims in Win32 subclass chains
- how to distinguish framework visibility from the first behavior-changing consumer
- how to classify Qt signal delivery as immediate vs queued before chasing downstream effects

## Search-layer attempt
Executed through:
- `skills/search-layer/scripts/search.py`
- explicit sources: `exa,tavily,grok`

Queries used:
1. `Win32 subclass CallWindowProc per-window original procedure reversing`
2. `Qt direct connection queued connection signal slot event loop reverse engineering`
3. `Win32 subclassing Raymond Chen per-window original wndproc SetWindowSubclass`

Raw log:
- `sources/native-binary/2026-03-23-native-gui-subclass-signal-slot-search-layer.txt`

## High-signal sources and findings

### 1. Microsoft Learn — Using Window Procedures
URL:
- https://learn.microsoft.com/en-us/windows/win32/winmsg/using-window-procedures

High-signal finding:
- subclassing is an instance-level operation that saves the original procedure and forwards through `CallWindowProc`
- this is enough to anchor a practical rule: `WndProc` discovery is only framework entry, not behavior proof

Operator consequence:
- when reversing GUI-heavy Win32 code, treat `DispatchMessage` and `WndProc` as routing landmarks only until one concrete `WM_*` branch is tied to a state write, action selection, or downstream work enqueue

### 2. Microsoft Learn — Subclassing Controls
URL:
- https://learn.microsoft.com/en-us/windows/win32/controls/subclassing-overview

High-signal finding:
- the older `SetWindowLongPtr` style has real chain-management pitfalls
- `SetWindowSubclass` / `DefSubclassProc` provide per-subclass identity and per-instance reference data

Operator consequence:
- if pseudocode shows several similar subclass wrappers, do not collapse them into one shared owner
- prefer recovering the exact `(window handle, subclass proc, subclass id/refdata)` ownership story before widening into sibling controls

### 3. Raymond Chen — original proc is per window, not globally shared
URL:
- https://devblogs.microsoft.com/oldnewthing/20090507-00/?p=18333

High-signal finding:
- the original procedure that must be called is the one for the specific window that was subclassed
- global/shared `oldWndProc` assumptions are wrong and can crash

Operator consequence:
- in reversing, do not trust a symmetric-looking wrapper until you have proved which exact control instance owns the saved original-proc chain
- this is especially important when several controls share one wrapper or helper but differ in prior subclass history

### 4. Microsoft Learn — SetWindowSubclass / DefSubclassProc
URLs:
- https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-setwindowsubclass
- https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-defsubclassproc

High-signal finding:
- `SetWindowSubclass` identifies subclasses by callback+ID and stores per-instance reference data
- `DefSubclassProc` forwards to the next handler in the subclass chain and eventually the original window procedure
- helper-based subclassing cannot cross threads

Operator consequence:
- for live proof, a breakpoint/log on `SetWindowSubclass` or `DefSubclassProc` can recover which instance-specific hop really owns a decisive `WM_COMMAND` / `WM_NOTIFY` family
- cross-thread assumptions should be treated skeptically when analyzing helper-based subclassing wrappers

### 5. Qt documentation — Signals & Slots
URL:
- https://doc.qt.io/qt-6/signalsandslots.html

High-signal finding:
- connected slots are usually executed immediately when the signal is emitted
- queued connections are the important exception and defer execution

Operator consequence:
- do not infer a queue boundary merely from `emit`
- first classify whether the signal/slot edge is direct/immediate or queued/deferred, then choose the proof boundary accordingly

### 6. Qt documentation — Threads and QObjects
URL:
- https://doc.qt.io/qt-6/threads-qobject.html

High-signal finding:
- `DirectConnection` executes in the emitter's thread immediately
- `QueuedConnection` runs when control returns to the receiver thread's event loop
- `AutoConnection` chooses based on thread affinity

Operator consequence:
- for Qt reversing, delivery classification should be part of the workflow note, not an afterthought
- if the receiver lives in another thread or the slot runs only after loop return, the GUI consumer may only be the first proof boundary before a later worker/request continuation

### 7. USENIX Security 2023 — QtRE
URL:
- https://www.usenix.org/conference/usenixsecurity23/presentation/wen

High-signal finding:
- callback and semantic recovery for Qt binaries is highly valuable and can expose many hidden callback instances

Operator consequence:
- callback recovery improves the map, but the practical question remains: which recovered slot/callback first changes state, policy, or downstream action in the current case?

## Resulting KB direction
This source pass supports strengthening the native GUI continuation around three practical distinctions:
- `WndProc` / subclass visibility vs instance-specific ownership truth
- visible signal emission vs actual delivery mode
- callback recovery vs first consequence-bearing consumer proof

The page should stay case-driven and should not expand into full Win32/Qt tutorial territory.
