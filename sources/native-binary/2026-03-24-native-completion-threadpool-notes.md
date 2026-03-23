# 2026-03-24 Native completion / thread-pool first-consumer notes

## Scope
Source-backed practical notes for the native completion-port / thread-pool first-consumer branch, with emphasis on:
- Windows IOCP dequeue truth
- Windows thread-pool wrapper vs real callback ownership
- libuv worker-thread completion vs loop-thread consequence ownership

Companion search trace:
- `sources/native-binary/2026-03-24-native-completion-threadpool-search-layer.txt`

## Sources consulted
- Microsoft Learn: I/O Completion Ports
  - https://learn.microsoft.com/en-us/windows/win32/fileio/i-o-completion-ports
- Microsoft Learn: `GetQueuedCompletionStatus`
  - https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-getqueuedcompletionstatus
- Microsoft Learn: thread-pool overview page requested, but the specific URL used in this run returned 404 via `web_fetch`
- libuv guide: Threads / work queue
  - https://docs.libuv.org/en/v1.x/guide/threads.html
- libuv source: `src/threadpool.c`
  - https://github.com/libuv/libuv/raw/refs/heads/v1.x/src/threadpool.c

## High-signal findings

### 1. IOCP has two distinct ownership carriers at dequeue time
For practical reversing, the key point is not just that `GetQueuedCompletionStatus` yields a completion, but that it yields **two different ownership clues**:
- `lpCompletionKey` = the per-handle completion key associated by `CreateIoCompletionPort`
- `lpOverlapped` = the address of the `OVERLAPPED` used to start the completed operation

Practical implication:
- if the target embeds `OVERLAPPED` inside a request/session object, `lpOverlapped` is often the best route back to the real owner
- if the implementation multiplexes several handle families through one port, `lpCompletionKey` may provide the first dequeue-time family reduction before object recovery
- analysts should not stop at “this worker calls `GetQueuedCompletionStatus`”; the real proof object is often the first recovered request object or packet family selected immediately after dequeue

### 2. IOCP ordering is not the same thing as simple submit-order truth
The Microsoft docs explicitly distinguish:
- completion packets are queued FIFO
- waiting threads are released in LIFO order
- the port’s concurrency value controls how many associated threads may run

Practical implication:
- naive assumptions like “earliest issued request corresponds to first consumer I observed” are unsafe
- on multi-worker ports, the stable proof object is usually not chronological order but one `(completion key, OVERLAPPED pointer, recovered owner object)` chain tied to one later state edge or emission
- when compare-runs are noisy, hold queue family and recovered owner identity constant before inferring meaning from timing

### 3. `PostQueuedCompletionStatus` means not every dequeue corresponds to real I/O completion
The IOCP docs explicitly note that threads may inject application-defined completion packets with `PostQueuedCompletionStatus`.

Practical implication:
- a queue/dequeue trace alone can mix:
  - true overlapped I/O completion
  - control-plane wakeups
  - shutdown markers
  - retry/time-based work
- the first useful reduction is often to distinguish posted control packets from I/O-owned packets before following callbacks deeper

### 4. `GetQueuedCompletionStatus` failure still may carry a real dequeued packet
Microsoft’s docs distinguish two failure shapes:
- failure with `*lpOverlapped == NULL` -> no packet dequeued
- failure with `*lpOverlapped != NULL` -> a packet for a failed I/O operation was dequeued

Practical implication:
- analysts should not collapse all FALSE returns into “nothing happened”
- failure-side consumers may still be the real policy owner when the interesting effect is retry, degrade, reconnect, backoff, or session teardown

### 5. Thread-pool wrappers should be treated as context-unpack layers until proven otherwise
The high-value practical lesson from the Microsoft model plus observed framework patterns is:
- thread-pool APIs make callback registration visible early
- but helper-owned unpack / cleanup / dispatch layers often sit between submission and the behavior-changing callback body

Practical implication:
- avoid concluding from the first helper callback symbol alone
- prefer the first point where the callback-specific context, request object, or policy branch becomes specific enough to predict later behavior
- cleanup-only or common wrapper code is usually not the real consumer, even if it is the first function hit by tracing

### 6. libuv has a concrete two-stage ownership split: worker thread then loop thread
The libuv guide plus `threadpool.c` make the practical chain explicit:
- `uv_queue_work(loop, req, work_cb, after_work_cb)` stores both callbacks in `uv_work_t`
- `uv__work_submit()` posts internal `uv__work` into the global threadpool queue
- a worker thread runs `uv__queue_work()`, which calls `req->work_cb(req)`
- when worker execution finishes, the result is inserted into `loop->wq` and `uv_async_send(&loop->wq_async)` is triggered
- later, on the event-loop thread, `uv__work_done()` drains the queue and `uv__queue_done()` calls `req->after_work_cb(req, err)`

Practical implication:
- the worker-thread `work_cb` is often only the production/computation boundary
- the first behavior-changing consumer may instead be the loop-thread `after_work_cb`
- when the target’s visible effect is UI/network/session mutation, reverse the loop-thread callback first before over-analyzing worker-side computation internals

### 7. libuv cancellation truth also lives in the loop-thread completion path
`threadpool.c` shows cancellation marks work as `uv__cancelled`, then still routes completion through the loop’s async completion machinery, where `uv__work_done()`/`uv__queue_done()` ultimately deliver `after_work_cb(req, err)` with cancellation status.

Practical implication:
- for stalled or suppressed behavior, the decisive proof object may be in the completion callback’s error-path handling rather than in the worker body
- if the question is “why didn’t the later effect happen?”, inspect loop-thread done/cancel handling before assuming the job never existed

## Concrete operator tactics added

### A. Minimal IOCP proof slice
For one suspected request family, record:
- issuance site and associated handle family
- completion key value/family
- recovered `OVERLAPPED` owner object
- first branch after dequeue that selects success/failure/retry/dispatch
- one later state write or output path

This is usually a better proof package than a wide queue timeline.

### B. Posted-control-vs-real-I/O discriminator
If IOCP traces look noisy, first classify packets into:
- posted control packets (`PostQueuedCompletionStatus`-style)
- true overlapped-I/O completions
- failed-I/O completions

Only then decide which dequeue family deserves deeper callback tracing.

### C. libuv first-consumer shortcut
When the target uses libuv-like async work and the behavior of interest is visible only after work “finishes,” jump quickly to:
- `uv__work_done`
- `uv__queue_done`
- `after_work_cb`

and treat `work_cb` as upstream computation unless proven to already own the effect.

### D. Queue order skepticism rule
For completion-driven systems, avoid proving ownership from queue chronology alone.
Prefer one identity chain:
- submitted/issued object
- dequeued packet/work item
- recovered owner/context
- first consequence-bearing callback
- one downstream effect

## KB-facing synthesis
These sources support tightening the native completion/thread-pool workflow note around three sharper rules:
1. at IOCP dequeue time, distinguish completion-family identity (`completion key`) from concrete owner recovery (`OVERLAPPED*`)
2. treat posted packets and failed-I/O packets as distinct practical families, not just noise
3. for libuv-style systems, explicitly split worker-thread production from loop-thread consequence ownership

## Candidate follow-up improvements
- Add one narrower native continuation specifically for Windows service + IOCP session ownership if the branch starts accumulating several real cases
- Add one cross-link from runtime-evidence compare-run guidance into completion-order skepticism for multi-worker queue cases
- Add one protected/native comparison note for thread-pool wrappers when helper/trampoline names are misleadingly “clean” compared with actual callback ownership
