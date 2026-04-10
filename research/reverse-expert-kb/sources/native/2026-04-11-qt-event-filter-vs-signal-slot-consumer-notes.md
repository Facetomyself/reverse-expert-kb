# Qt event-filter vs signal-slot consumer notes

Date: 2026-04-11
Branch: native practical workflows
Seam: Qt cases where `installEventFilter(...)`, `eventFilter(...)`, object handlers, signal emission, and slot fan-out are all visible, but the first behavior-changing consumer is still ambiguous
Related canonical pages:
- `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md`
- `topics/native-qt-event-filter-vs-signal-slot-first-consumer-workflow-note.md`
- `topics/native-practical-subtree-guide.md`
- `topics/native-binary-reversing-baseline.md`

## Research intent
Tighten the native GUI branch around a thinner Qt-only liar:
- filter installation truth
- filter-hit truth
- filter-owned fate truth
- later receiver-side handler truth
- signal emission truth
- connection-mode truth
- slot-delivery truth
- first consequence-bearing consumer truth

The goal is not a broad Qt GUI taxonomy page.
The goal is a reusable stop rule for native desktop reversing when recovered event-filter plumbing is being overread as if it already proved the real behavior-changing consumer.

## Search artifact
Raw multi-source search artifact:
- `sources/native/2026-04-11-0450-qt-event-filter-signal-slot-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Exa returned usable Qt documentation surfaces
- Tavily returned usable Qt documentation surfaces and useful snippets around filter-stop and thread-affinity behavior
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` errors through the configured proxy path

## Retained sources
1. Qt Documentation — `The Event System`
   - <https://doc.qt.io/qt-6/eventsandfilters.html>
2. Qt Documentation — `Signals & Slots`
   - <https://doc.qt.io/qt-6/signalsandslots.html>
3. Qt Documentation — `Threads and QObjects`
   - <https://doc.qt.io/qt-6/threads-qobject.html>

## High-signal retained findings

### 1. Filter visibility is earlier than target-object truth
Qt’s event-system documentation preserves the first critical split:
- `installEventFilter(...)` makes the filter object receive the target object’s events first
- if every filter returns `false`, the event is still sent to the target object
- if one filter returns `true`, the target object and any later event filters do not see the event at all

Practical consequence:
- `eventFilter(...)` visibility is not automatically filter-owned behavior truth
- a filter becomes the first truthful consumer only when it actually stops, rewrites, or retargets the event in a way that predicts the later behavior
- if it returns `false`, the first truthful consumer may still live later in the target object’s `event(...)`, a type-specific handler, a signal emission site, or a slot

### 2. Application-global filters are reduction boundaries first
Qt’s event-system documentation also preserves that application-wide filters on `QApplication` or `QCoreApplication` run before object-specific filters.
Qt explicitly warns that this power slows down every event in the application.

Practical consequence:
- global filter visibility often makes the event family easy to recover
- but global filters are still reduction boundaries first, not automatic first-consumer proof
- unless the global filter itself suppresses, rewrites, or policy-gates the event, keep reducing toward the later object handler or slot that first changes behavior

### 3. Signals are usually immediate; queued delivery is the exception that must be frozen explicitly
Qt’s signals-and-slots documentation preserves that connected slots are usually executed immediately, like a normal function call, and that this is independent of any GUI event loop.
The same source also preserves that queued connections are the special case where execution continues after `emit` and slots run later.

Practical consequence:
- signal visibility does not automatically imply queue-delivery truth
- if the connection is direct, the first truthful consumer may still be emission-time or one immediately entered slot
- if the connection is queued, the truthful next boundary is later delivery rather than the emit site itself

### 4. `Qt::AutoConnection` is receiver-affinity truth, not vibe-based “cross-thread shaped” truth
Qt’s thread documentation preserves the rule:
- `AutoConnection` behaves like `DirectConnection` when the signal is emitted in the thread that the receiver object has affinity to
- otherwise it behaves like `QueuedConnection`
- queued connections invoke the slot when control returns to the event loop of the receiver’s thread

Practical consequence:
- do not flatten recovered `AutoConnection` edges into generic queued-delivery proof
- first freeze the receiver object’s thread affinity
- then ask whether the real boundary is still direct immediate delivery or later queued delivery

### 5. Event-loop liveness is part of slot-delivery truth
Qt’s thread documentation preserves that if no event loop is running, events are not delivered to the object.
That same page also makes clear that queued connections rely on the receiver thread’s event loop.

Practical consequence:
- even after proving a queued edge, `connected != delivered`
- receiver-loop liveness is part of the truth object, not just an implementation detail
- a recovered queued edge with no live receiver loop is still weaker than one delivered slot or later consumer

### 6. Event-filter topology is thread-constrained
Qt’s thread documentation preserves a smaller but important rule:
- event filters are supported in all threads only if the monitoring object lives in the same thread as the monitored object

Practical consequence:
- “this filter class exists” is weaker than “this filter can truthfully own this event path in the current thread topology”
- when thread movement or worker-object patterns are present, recover the live object affinities before narrating filter ownership

## Practical synthesis worth preserving canonically
A compact stop-rule ladder for this seam is:

```text
filter installed
  != filter hit
  != filter returned true and owned event fate
  != receiver-side event()/handler truth
  != signal emitted
  != connection-mode truth
  != slot delivered
  != first consequence-bearing consumer
```

The smaller Qt-shaped memory worth preserving is:

```text
filter visible
  != filter-owned fate
  != signal found
  != direct/queued truth
  != delivered
  != consumed
```

This keeps six different wins separate:
1. **filter topology truth**
   - one specific target object and filter relationship is real
2. **filter-owned fate truth**
   - the filter actually stops, rewrites, or retargets the event
3. **receiver-handler truth**
   - the target object’s own `event(...)` or type-specific handler really handles the event
4. **signal-edge truth**
   - one concrete emitted signal or smaller follow-on edge is the next meaningful reduction
5. **delivery-mode truth**
   - the path is really direct or queued under the current receiver affinity and event-loop reality
6. **consumer truth**
   - one delivered slot or later reducer first predicts the downstream behavior

## Best KB use of this material
This material is best used as a dedicated thinner continuation page under the native GUI workflow note.
It should not become a broad Qt event-system overview page.

The operator-facing value is:
- do not stop at `installEventFilter(...)` or `eventFilter(...)` visibility by default
- do not overread application-global filters as automatic behavioral owners
- do not assume every recovered signal edge implies queued delivery
- do not flatten `Qt::AutoConnection` into “cross-thread, so later” without freezing receiver affinity
- do not stop at a queued edge without proving receiver-loop liveness and actual slot delivery

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source result set.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked; its failure is recorded clearly.
