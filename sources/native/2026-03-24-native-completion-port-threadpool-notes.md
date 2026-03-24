# 2026-03-24 Native completion-port / thread-pool / libuv ownership notes

Scope: source-backed practical continuation support for `topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md`
Branch: native practical subtree
Mode intent: external-research-driven

## Research target
Sharpen the native completion/dequeue continuation with practical stop rules that help analysts avoid reopening broad callback mapping when the real missing proof is narrower delivery ownership.

## Why this branch was chosen
Recent reverse-KB maintenance had already spent substantial effort on internal branch sync and canonical wording. This run deliberately chose a still-practical native continuation seam so the run would produce source-backed operator value instead of another wording/index-only pass.

## High-signal takeaways

### 1. IOCP dequeue order is not simple submit order
Source signals support a practical warning: completion packets may be queued FIFO, but worker release/processing order can still differ because waiting threads are released in LIFO order and actual handling depends on concurrency and scheduler state.

Practical KB impact:
- do not infer first real consumer from “the first request I issued” alone
- prove the first dequeue-time owner with `OVERLAPPED*`, completion key, or recovered request object rather than using issuance order as a proxy

Sources:
- Microsoft Learn: `GetQueuedCompletionStatus`
- Exa/Tavily surfaced discussion on LIFO dequeue observations

### 2. Control packets can masquerade as I/O-owned work in IOCP loops
`PostQueuedCompletionStatus` can inject control-plane packets that look like ordinary dequeued items at the worker loop level.

Practical KB impact:
- separate control-plane packets from I/O-owned packets before claiming ownership of a behavior-changing consumer
- this is especially important when worker loops multiplex shutdown/retry/control and real I/O completions in the same dequeue path

Sources:
- KB/article on IOCP server design surfaced by Tavily
- Microsoft API semantics around completion ports

### 3. `GetQueuedCompletionStatus(FALSE)` does not always mean “nothing was delivered”
Microsoft documents that failure returns can still correspond to a dequeued completion packet when `lpOverlapped` is non-NULL.

Practical KB impact:
- failed completion delivery may still own retry/backoff/degrade behavior
- do not discard the path just because the API return is false

Sources:
- Microsoft Learn: `GetQueuedCompletionStatus`

### 4. `TP_IO` has a real immediate-success gap analysts should remember
`CreateThreadpoolIo` is not enough by itself. Microsoft’s contract requires `StartThreadpoolIo`, and when the bound handle uses `FILE_SKIP_COMPLETION_PORT_ON_SUCCESS`, immediately successful overlapped I/O may skip the callback path and require `CancelThreadpoolIo`.

Practical KB impact:
- if a callback never appears, do not immediately conclude the callback is dead code or unrelated
- first verify notification mode and immediate-success semantics
- this gives a concrete stop rule for thread-pool I/O cases where analysts might otherwise reopen broad worker/callback searches

Sources:
- Microsoft Learn: `CreateThreadpoolIo`

### 5. libuv has two distinct ownership boundaries around `uv_queue_work()`
The libuv docs and discussion signals support a practical split:
- `work_cb` runs on a worker thread
- `after_work_cb` runs on the loop thread
- libuv internally synchronizes the work/done handoff
- `uv_async_send()` does not automatically provide the same memory-order guarantee

Practical KB impact:
- do not flatten “background work happened” into “worker thread owns the result”
- if the effect disappears only at loop-thread delivery, inspect `after_work_cb` and any `uv_async_send()` continuation before reopening worker-body analysis

Sources:
- libuv docs: thread pool work scheduling
- libuv discussion #4765

## Canonical changes this research supports
- strengthened `native-completion-port-and-thread-pool-first-consumer-workflow-note.md`
- synchronized stop rules into `native-practical-subtree-guide.md`
- synchronized the same continuation seam into `native-binary-reversing-baseline.md`

## Source list
- https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-getqueuedcompletionstatus
- https://learn.microsoft.com/en-us/windows/win32/api/threadpoolapiset/nf-threadpoolapiset-createthreadpoolio
- https://docs.libuv.org/en/latest/threadpool.html
- https://github.com/libuv/libuv/discussions/4765
- search-layer raw capture: `sources/native/2026-03-24-native-completion-port-threadpool-search-layer.txt`

## Confidence / limits
- Exa and Tavily both returned usable results.
- Grok attempt failed with 502 and is treated as degraded mode for this run.
- The additions are intentionally workflow-shaped and conservative; they encode stop rules and interpretation boundaries rather than low-level implementation folklore beyond what the sources support.
