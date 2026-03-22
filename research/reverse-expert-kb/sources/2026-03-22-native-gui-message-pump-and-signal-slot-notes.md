# 2026-03-22 Native GUI message-pump / signal-slot first-consumer notes

Focus:
- narrow native practical continuation for GUI-heavy cases
- Win32 message-pump / `WndProc` / subclass ownership
- Qt event delivery / signal-slot ownership
- first consequence-bearing consumer rather than framework labels

## Why this source pass was chosen
Recent autosync runs had already been productive on several other practical leaves. This run deliberately targeted a still-practical native leaf that was not yet broken out as a thinner GUI-specific continuation, in line with the anti-stagnation rule against endless internal wording-only maintenance.

## Search intent
We needed sources that support a practical operator rule, not just GUI framework tutorials:
- distinguish message-pump/framework structure from the first behavior-changing handler
- distinguish subclassing presence from per-window-instance ownership
- distinguish Qt signal presence from direct vs queued delivery and first policy-changing slot

## Search-layer attempt
Primary search was executed through:
- `skills/search-layer/scripts/search.py`
- explicit source selection: `exa,tavily,grok`

Queries used:
1. `reverse engineering windows message dispatch WndProc subclass callback workflow`
2. `reverse engineering event loop message pump callback ownership GUI native`
3. `reverse engineering Qt signal slot event loop callback consumer workflow`

Raw search-layer log:
- `sources/2026-03-22-native-gui-message-pump-search-layer.txt`

## High-signal fetched sources

### 1. Microsoft Learn — Using Window Procedures
URL:
- https://learn.microsoft.com/en-us/windows/win32/winmsg/using-window-procedures

Why it matters:
- separates message loop, class registration, and `lpfnWndProc` association from actual message handling
- confirms that `WndProc` / `DefWindowProc` are framework-level structure, so reversing still has to reduce to one meaningful `WM_*` branch

### 2. Microsoft Learn — Subclassing Controls
URL:
- https://learn.microsoft.com/en-us/windows/win32/controls/subclassing-overview

Why it matters:
- shows concrete subclass chain APIs (`SetWindowLongPtr`, `SetWindowSubclass`, `DefSubclassProc`)
- supports the operator rule that subclassing introduces an ownership chain rather than a single monolithic consumer label

### 3. Raymond Chen / The Old New Thing — original proc must be per-window
URL:
- https://devblogs.microsoft.com/oldnewthing/20090507-00/?p=18333

Why it matters:
- provides a crisp practical reminder that the original window procedure is specific to the subclassed window instance
- directly supports the reversing rule: do not assume a global/shared “old WndProc” truth when proving which control instance owns the decisive behavior

### 4. Qt documentation — Signals & Slots
URL:
- https://doc.qt.io/qt-6/signalsandslots.html

Why it matters:
- confirms that many slots execute immediately on signal emission, while queued connections defer delivery
- directly supports the reversing rule that signal visibility alone does not prove a queue boundary

### 5. Understanding Qt's Event Loop and Signals/Slots
URL:
- https://dekonvoluted.github.io/programming/2018/09/16/qt-event-loop.html

Why it matters:
- useful explanatory bridge for the practical interaction between event arrival, signal emission, and later event-loop return
- weaker than official docs, but still helpful as workflow-oriented operator intuition

### 6. USENIX Security 2023 — QtRE abstract page
URL:
- https://www.usenix.org/conference/usenixsecurity23/presentation/wen

Why it matters:
- supports the claim that callback recovery in Qt binaries is valuable and practically fruitful
- also helps justify why the KB should distinguish “callback recovery” from the narrower question of first consequence-bearing consumer proof

## Resulting KB direction
This source pass supports a thinner native continuation page centered on:
- message family / signal family selection
- framework-reduction boundary
- per-instance or per-connection ownership
- first consequence-bearing consumer
- proof-of-effect boundary

The resulting page should stay practical and case-driven rather than expanding into generic GUI framework explanation.