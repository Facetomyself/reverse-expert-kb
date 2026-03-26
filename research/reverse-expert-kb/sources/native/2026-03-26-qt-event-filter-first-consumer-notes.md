# Qt event-filter vs signal/slot first-consumer notes

Date: 2026-03-26 11:16 Asia/Shanghai / 2026-03-26 03:16 UTC
Branch: native practical workflows
Seam: GUI / event-loop continuation -> Qt event-filter interception vs signal/slot delivery truth

## Why this note exists
The native GUI branch already preserved useful stop rules for:
- Win32 message pumps vs per-window subclass ownership
- Qt direct vs queued signal/slot delivery
- Cocoa/XPC/dispatch visibility vs first truthful consumer ownership

What was still under-preserved was a thinner Qt-specific rule:
- `installEventFilter(...)` / `eventFilter(...)` visibility is not the same thing as proving the first consequence-bearing consumer
- an event filter can be the truthful consumer when it actually suppresses, rewrites, or retargets an event
- but when the filter returns `false` and later ordinary object handling or later signal/slot delivery still decides behavior, the filter is only an interception boundary, not the answer

## Conservative source-backed reminders
### 1. Event filters run before the target object and can stop later handling
Qt’s official event-system documentation states that an installed event filter receives events before the target object, and that returning `true` stops further processing so the target and later event filters do not see the event.

Practical operator consequence:
- `eventFilter(...)` is a real first-consumer candidate when it swallows, rewrites, or policy-gates the event
- but if it returns `false`, the truthful first behavior-changing consumer may still live later in `QObject::event(...)`, a type-specific handler, or later signal/slot routing

### 2. Global application filters are even earlier reduction boundaries, not automatic behavioral ownership
Qt also documents that application-wide filters on `QApplication` / `QCoreApplication` run before object-specific filters.

Practical operator consequence:
- global filters are strong interception points
- but they should not be overread as the real owner unless they actually change the event’s fate
- otherwise they are just earlier reduction boundaries and the analyst should continue into the object-specific or later consumer boundary

### 3. Direct vs queued signal/slot delivery is a separate truth boundary from event-filter interception
Qt documentation distinguishes immediate handling (`sendEvent`) from queued delivery (`postEvent`), and the Woboq implementation write-up explains that queued signal/slot delivery posts a `QMetaCallEvent` into the receiver thread’s event queue rather than executing the slot immediately.

Practical operator consequence:
- do not collapse event-filter visibility into later queued slot delivery
- first decide whether the event filter itself changes behavior
- if not, keep the existing branch split: direct slot delivery may still be immediate at emit time, while queued delivery is a later receiver-loop boundary

### 4. Qt meta-object recovery helps mapping, but still does not answer ownership by itself
Qt reversing notes around `staticMetaObject`, class names, and slot/signal tables remain useful for navigation and callback recovery.

Practical operator consequence:
- recovered meta-object names, signals, and slots improve the map
- but the practical question remains: which filter / handler / slot first changes behavior for this case?

## Practical stop rule worth preserving canonically
Use this narrower rule in Qt GUI reversing:

```text
Do not stop at “event filter installed” or “eventFilter(...) hit.”
Freeze one smaller boundary:
filter suppresses/rewrites/retargets event
or
filter passes through and one later object handler / direct slot / queued slot owns the first durable consequence.
```

## Suggested canonical wording to preserve
- Event-filter installation is weaker than filter-consequence truth.
- Filter execution is weaker than filter-owned behavior change if the filter returns `false`.
- Global filter visibility is weaker than object-specific or later slot-owned consequence unless the global filter actually suppresses, rewrites, or retargets the event.
- Direct-vs-queued signal/slot classification remains a separate truth split after the filter boundary.

## Source anchors consulted conservatively
- Qt documentation: `The Event System` (`eventsandfilters.html`)
- Woboq: `How Qt Signals and Slots Work - Part 3` (queued connections / `QMetaCallEvent`)
- Scott Knight: `Qt Reversing` (meta-object / slot-signal recovery as mapping aid)

## Search-source status for this note
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- exa
- tavily

Failed sources:
- grok (`502 Bad Gateway` during search-layer invocation)

Endpoints used on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`
