# Qt AutoConnection thread-affinity and event-loop truth notes

Date: 2026-03-27 03:16 Asia/Shanghai / 2026-03-26 19:16 UTC
Branch: native practical workflows
Seam: Qt signal-slot / event-filter ownership after visible connection recovery

## Why this note exists
A recurring native-GUI reversing failure mode is to overread a recovered Qt connection edge as if it already proved:
- queued delivery
- cross-thread execution
- or the first behavior-changing consumer

The practical source-backed rule is narrower.
Under `Qt::AutoConnection`, the deciding fact is not “this is a signal/slot edge” by itself.
It is the receiver object's thread affinity at emission time.

A second recurring failure mode is to overread `eventFilter(...)` visibility as if the filter already owned later behavior.
That is only true when the filter actually changes event fate.

## Source-backed retained points
Primary official anchors used this run:
- Qt docs, `Threads and QObjects`: <https://doc.qt.io/qt-6/threads-qobject.html>
- Qt docs, `QObject`: <https://doc.qt.io/qt-6/qobject.html>

Conservative retained points:
1. `Qt::AutoConnection` is affinity-dependent.
   - if the signal is emitted in the thread that the receiver object has affinity to, behavior matches `DirectConnection`
   - otherwise behavior matches `QueuedConnection`

2. `QueuedConnection` truth is still weaker than consumer truth.
   - queued delivery runs when control returns to the event loop of the receiver thread
   - if no event loop is running, event-driven delivery does not happen
   - therefore “receiver is in another thread” is weaker than “the slot actually became a delivered consumer in that receiver-thread loop`

3. Explicit queued delivery and AutoConnection are different proof objects.
   - explicit `Qt::QueuedConnection` in the same thread is still delayed/event-loop-mediated
   - same-thread visibility therefore does not imply immediate slot execution unless the connection mode and affinity situation actually make it direct

4. Event filters require same-thread monitoring and are not automatic ownership.
   - Qt documents that the monitoring object must live in the same thread as the monitored object
   - `installEventFilter(...)` visibility is therefore a routing and reduction fact, not automatic first-consumer proof
   - the filter becomes the truthful first consumer only when it suppresses, rewrites, or retargets the event in a way that predicts later behavior
   - if it returns `false`, later object handlers, direct slots, or queued slots may still own the first durable consequence

## Practical operator synthesis
Useful branch shorthand for Qt-heavy native cases:

```text
connected != direct != queued != delivered != consumed
```

And for filter-shaped cases:

```text
filter-installed != filter-hit != filter-fate != later-consumer
```

What this changes in practice:
- do not narrate recovered signal/slot graphs as if every edge were a queued consumer path
- first freeze receiver thread affinity and the actual connection-mode consequence for the edge that matters
- if the edge is effectively queued, still ask whether the receiver-thread event loop is live enough for delivery to occur
- if the edge is direct, do not widen into thread/queue folklore; prove the slot-immediate consumer or one later narrower consequence
- do not stop at event-filter visibility when the filter returns `false` and one later handler or slot still owns the behavioral truth

## Where this should land in the KB
This note should tighten:
- `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md`
- `topics/native-practical-subtree-guide.md`
- top-level native branch memory in `index.md`

## Search/source audit context
Requested sources this run:
- exa
- tavily
- grok

Observed source condition:
- Tavily produced usable results
- Grok failed with `502 Bad Gateway`
- Exa showed `402 Payment Required` errors during execution, although the saved artifact still included some Exa-tagged results; treat Exa as degraded/ambiguous for this run rather than as a clean success

Endpoints on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Saved raw artifact:
- `sources/native/2026-03-27-0316-qt-autoconnection-thread-affinity-search-layer.txt`
