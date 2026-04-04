# 2026-04-04 native wait object / threadpool wait first-consumer notes

Date: 2026-04-04 15:21 Asia/Shanghai / 2026-04-04 07:21 UTC
Theme: keep wait registration, signal-or-timeout truth, callback delivery truth, and first consequence-bearing consumer truth separate.

## Why this note was retained
The native practical branch already had:
- broad callback/event-loop reduction
- IOCP/thread-pool completion reduction
- APC alertable-wait reduction
- timer queue/threadpool timer reduction

What it still lacked was the thinner wait-object / threadpool-wait continuation for cases where one registered wait is visible but the main ambiguity is whether one signaled-or-timeout callback actually becomes the first behavior-changing consumer.

## Primary doc-backed anchors
### 1. CreateThreadpoolWait
Source:
- Microsoft Learn — CreateThreadpoolWait
  - https://learn.microsoft.com/en-us/windows/win32/api/threadpoolapiset/nf-threadpoolapiset-createthreadpoolwait

Retained points:
- creates a wait object
- callback environment can affect how the callback executes
- the object is only a wait object until a handle is actually set on it

Operator consequence:
- wait-object creation alone is weaker than active wait truth

### 2. SetThreadpoolWait
Source:
- Microsoft Learn — SetThreadpoolWait
  - https://learn.microsoft.com/en-us/windows/win32/api/threadpoolapiset/nf-threadpoolapiset-setthreadpoolwait

Retained points:
- sets the wait object, replacing the previous wait object if any
- a worker thread calls the callback after the handle becomes signaled or the timeout expires
- if `h` is NULL, the wait ceases to queue new callbacks, but callbacks already queued will still occur
- you must re-register the event with the wait object before signaling it each time to trigger the wait callback

Operator consequence:
- active registration is weaker than one actual signaled/timeout-driven callback
- unsetting/cancelling is weaker than proving no callback was already queued
- repeated-callback claims need re-registration truth, not just repeated signaling folklore

### 3. RegisterWaitForSingleObject
Source:
- Microsoft Learn — RegisterWaitForSingleObject
  - https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-registerwaitforsingleobject

Retained points:
- a wait thread in the thread pool waits on the object and queues the callback when the object is signaled or timeout elapses
- some flags materially change semantics (`WT_EXECUTEONLYONCE`, `WT_EXECUTEINWAITTHREAD`, etc.)
- objects that remain signaled can produce misleading callback repetition if flags are not handled honestly
- unregister/cancel semantics must be treated carefully; do not make blocking unregister calls from the callback itself

Operator consequence:
- flag posture and object type matter for compare-honest wait behavior
- object-signal visibility alone is weaker than first callback-owned consumer truth

## Search-layer trace
See:
- `sources/native/2026-04-04-1521-native-wait-search-layer.txt`

Observed degraded mode:
- Exa: returned results
- Tavily: returned results
- Grok: invoked but returned empty set
