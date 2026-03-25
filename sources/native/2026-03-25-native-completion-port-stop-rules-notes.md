# Native completion-port / thread-pool stop-rules notes — 2026-03-25

Focus of this note:
- preserve source-backed practical stop rules for the native completion-port / thread-pool first-consumer branch
- keep the branch practical and case-driven instead of letting it collapse into broad “callback exists” or “queue visible” narration
- sharpen three specific ownership boundaries that are easy to overflatten:
  - IOCP posted control packets vs true I/O-owned completions
  - TP_IO object creation vs actual callback eligibility / notification delivery
  - libuv worker-side completion vs loop-thread consumer ownership

Search artifact:
- `sources/native/2026-03-25-native-completion-port-search-layer.txt`

## External sources consulted
Primary authoritative references:
- Microsoft Learn — `CreateThreadpoolIo`
- Microsoft Learn — `StartThreadpoolIo`
- Microsoft Learn — `CancelThreadpoolIo`
- Microsoft Learn — `PostQueuedCompletionStatus`
- libuv docs — Threads guide (`uv_queue_work`, worker thread vs `after_work_cb` on loop thread)
- libuv docs — `uv_async_t` / `uv_async_send`

Secondary/operator-signal results surfaced in search:
- Microsoft Q&A discussion on distinguishing `IoCompletionCallback` completions
- Stack Overflow discussions around IOCP completion keys / `FILE_SKIP_COMPLETION_PORT_ON_SUCCESS`
- libuv GitHub discussions/issues around worker completion and async delivery

## Practical findings worth preserving

### 1. IOCP dequeue visibility is weaker than I/O-owned completion truth
`PostQueuedCompletionStatus` matters because Microsoft explicitly says the posted packet simply feeds values back through `GetQueuedCompletionStatus`, and the system does not validate them; `lpOverlapped` need not even point to a real `OVERLAPPED`.

Practical consequence:
- an analyst should not treat every dequeued packet as evidence of a completed I/O-owned request
- posted control packets can look similar at the worker-loop boundary
- first separate queue-family/control-plane truth from actual I/O-owned request truth before claiming the consumer or ownership boundary is solved

Useful operator framing:
- `completion key` often reduces queue/handle/control family
- `OVERLAPPED*` often reduces concrete request/session owner
- but both are still weaker than proving one later state edge, retry policy, or emitted reply

### 2. `TP_IO` registration is weaker than callback-delivery truth
Microsoft Learn preserves several easy-to-miss contracts:
- `CreateThreadpoolIo` only creates the I/O object
- `StartThreadpoolIo` must be called **before each async I/O operation**
- if that is not done, the thread pool may ignore the completion and memory corruption can result
- if the overlapped operation fails synchronously (error other than `ERROR_IO_PENDING`), notifications must be canceled with `CancelThreadpoolIo`
- if the handle uses `FILE_SKIP_COMPLETION_PORT_ON_SUCCESS` and the async operation returns immediate success, the callback is not called and the notification must also be canceled

Practical consequence:
- “TP_IO exists” is not enough
- “the callback never fires” does not immediately mean the consumer is dead, bypassed, or irrelevant
- first check whether the real boundary is notification eligibility / cancellation behavior rather than later callback ownership

This is especially useful in reverse cases where the target seems to register a thread-pool I/O callback but some operations appear to bypass it.

### 3. libuv worker completion is weaker than loop-thread consumer truth
libuv’s threads guide preserves the split clearly:
- `uv_queue_work()` runs the `work_cb` in a worker thread
- once that finishes, the `after_work_cb` is called on the event-loop thread

Its async-handle docs preserve another stop rule:
- `uv_async_send()` wakes the loop and invokes the callback on the loop thread
- multiple sends may be coalesced rather than causing one callback per send

Practical consequence:
- do not flatten worker-side `work_cb` into final ownership of the behavioral outcome
- do not treat `uv_async_send()` visibility as one-to-one event truth
- when the visible effect only appears or disappears on the loop-thread side, the real first consumer may be `after_work_cb` or an async-handle continuation rather than the worker body

### 4. This branch benefits from preserving “dequeue reduction -> truthful owner -> later effect” as the canon
The native completion-port branch is strongest when it keeps asking:
- what exactly got dequeued?
- is it a control packet or a true completion-owned object?
- what field/object still identifies the live owner more truthfully than queue chronology alone?
- what later effect proves that this consumer, not just this wrapper, owns behavior?

That keeps the branch from drifting into:
- queue cataloging
- callback enumeration
- wrapper-name worship
- naive submit-order assumptions

## Recommended KB preservation points
These findings should be reflected in:
- `topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md`
- `topics/native-practical-subtree-guide.md`
- `topics/native-binary-reversing-baseline.md`
- `index.md`

## Search audit summary for this note
Requested sources:
- `exa,tavily,grok`

Succeeded:
- `exa`
- `tavily`

Failed:
- `grok` (`502 Bad Gateway` during `search-layer` execution)

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`
