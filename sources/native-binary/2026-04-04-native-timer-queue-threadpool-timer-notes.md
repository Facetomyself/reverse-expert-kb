# 2026-04-04 native timer-queue / threadpool-timer first-consumer notes

Date: 2026-04-04 11:21 Asia/Shanghai / 2026-04-04 03:21 UTC
Theme: keep timer-object truth separate from callback-queued truth, callback-running truth, and first-consumer truth.

## Why this note was retained
The native practical branch already had broad callback/event-loop notes plus thinner IOCP/APC/GUI continuations.
What it did not yet have was a timer-shaped continuation for cases where a Windows timer object is already visible and the remaining problem is proving whether one timer callback actually becomes the first behavior-changing consumer.

## Primary doc-backed anchors
### 1. CreateTimerQueue / CreateTimerQueueTimer
Sources:
- Microsoft Learn — CreateTimerQueue
  - https://learn.microsoft.com/en-us/windows/win32/api/threadpoollegacyapiset/nf-threadpoollegacyapiset-createtimerqueue
- Microsoft Learn — CreateTimerQueueTimer
  - https://learn.microsoft.com/en-us/windows/win32/api/threadpoollegacyapiset/nf-threadpoollegacyapiset-createtimerqueuetimer

Retained points:
- a timer queue is a queue for lightweight timer objects with callbacks
- `CreateTimerQueueTimer` creates a timer-queue timer and calls the callback when the timer expires
- if due time and period are both nonzero, the callback is called first at due time, then periodically
- periodic callbacks can be queued whether or not the previous callback has finished executing
- callbacks are queued to the thread pool by default, with flag-dependent behavior and timer-thread special cases

Operator consequence:
- timer registration alone is weaker than callback queue/delivery truth
- periodic timers need per-instance honesty; do not flatten them into one linear callback chain

### 2. SetThreadpoolTimer
Source:
- Microsoft Learn — SetThreadpoolTimer
  - https://learn.microsoft.com/en-us/windows/win32/api/threadpoolapiset/nf-threadpoolapiset-setthreadpooltimer

Retained points:
- sets the timer object, replacing the previous timer if any
- if due time is NULL, the timer stops queueing new callbacks, but already queued callbacks can still occur
- some callbacks may still run after the application closes the timer unless the documented close/wait pattern is followed

Operator consequence:
- replacement/cancellation is weaker than proof that no queued callback remains in flight

### 3. Raymond Chen on cancelling timers/waits
Source:
- The Old New Thing — On the finer points of cancelling timers and wait objects in Windows thread pool
  - https://devblogs.microsoft.com/oldnewthing/20230428-00/?p=108110

Retained points:
- cancelling prevents future callbacks from being created but cannot necessarily recall one already scheduled
- `Set...Ex` FALSE can mean the callback is already in progress or past the recall point
- waiting for outstanding callbacks is the correct completion barrier

Operator consequence:
- cancel-path visibility must not be overread as “callback impossible now”

## Search-layer trace
See:
- `sources/native-binary/2026-04-04-1121-native-timer-search-layer.txt`

Observed degraded mode:
- Exa: returned results
- Tavily: returned results
- Grok: invoked but returned empty set
