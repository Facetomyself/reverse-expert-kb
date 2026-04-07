# Qt event-filter vs signal-slot handoff notes

Date: 2026-04-08 03:51 Asia/Shanghai / 2026-04-07 19:51 UTC
Mode: external-research-driven
Branch: native desktop/server practical workflows -> GUI event-filter vs signal-slot handoff realism

## Why this branch
This run used the external slot on a bounded thin native candidate already named in top-level steering:
- native GUI event-filter vs signal-slot handoff when both are visible but the first behavior-changing consumer is still ambiguous

The practical question was not broad Qt event taxonomy.
It was how to keep a narrower proof split when the analyst can already see:
- `installEventFilter(...)` / `eventFilter(...)`
- later object event handling
- later signal emission and slot graphs

## Search-layer observations
Explicit multi-source search was attempted with:
- `--source exa,tavily,grok`

Queries used:
1. `Qt eventFilter return true false queued connection receiver thread affinity documentation`
2. `Qt AutoConnection receiver thread affinity event loop queued slot delivery official docs`
3. `Qt event filter signal slot first consumer official docs`

Observed source behavior:
- Exa returned usable results
- Tavily returned usable results
- Grok was invoked on all queries but returned 502 errors through the configured proxy/completions endpoint

## Primary source anchors
### Qt event system docs
URL:
- https://doc.qt.io/qt-6/eventsandfilters.html

Useful operator implications:
- event filters run before the target object
- returning `true` stops later processing
- returning `false` allows later event processing to continue
- that fall-through is only delivery-continuation truth, not later consumer truth

### QObject/connect docs
URL:
- https://doc.qt.io/qt-6/qobject.html

Useful operator implications:
- a visible connection edge proves connect-time structure, not necessarily later delivery or first consequence-bearing ownership
- queued connections require argument copying / meta-type support and should remain distinct from direct delivery truth

### Threads and QObjects docs
URL:
- https://doc.qt.io/qt-6/threads-qobject.html

Useful operator implications:
- `Qt::AutoConnection` resolves by receiver thread affinity at emission time
- queued delivery depends on control returning to the receiver thread's event loop
- without a running event loop, queued delivery will not happen
- event filters require monitoring and monitored objects to live in the same thread

### Signals and slots docs
URL:
- https://doc.qt.io/qt-6/signalsandslots.html

Useful operator implications:
- slots are usually executed immediately when the signal is emitted
- queued connections are the important exception
- one emitted signal may still fan out to multiple slots in connection order, so visible emit-site truth is weaker than first consequence-bearing consumer truth

## Practical synthesis to preserve canonically
Useful ladder:

```text
filter returned false
  != receiver event handled
  != signal edge chosen
  != slot delivered
  != first consequence-bearing consumer
```

Smaller supporting reminders:
- `eventFilter(...)` visibility is weaker than filter-owned fate
- filter `false` return is weaker than proving the receiver object handler became the first truthful consumer
- receiver object handling is weaker than proving which emitted signal/connection edge actually mattered
- visible signal edge is weaker than proving slot delivery under `AutoConnection` or queued delivery conditions
- delivered slot is still weaker than proving it was the first behavior-changing consumer

## Why this mattered to the KB
The native GUI page already preserved event-filter and signal-slot realism separately.
This run tightened the handoff seam between them so analysts do not stop too early at visible filter fall-through or visible signal edges when the real missing proof object is still one later slot or one later consumer-side write/branch/enqueue.

## Candidate follow-ons
Possible later native continuations if needed:
- a smaller compare-heavy continuation when filter fate is already known but receiver-thread event-loop liveness is the main remaining liar for queued delivery
- a parent/subtree sync only if this new handoff seam still feels too leaf-local
