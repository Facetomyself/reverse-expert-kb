# 2026-03-26 Native APC / Alertable-Wait First-Consumer Notes

## Research question
What smaller, practical workflow rule should the native branch preserve for Windows user-mode APC cases once broad callback ownership is already understood, but queued-vs-delivered truth still hides the first real consumer?

## Directional conclusion
A useful thinner native continuation exists around **APC queued-vs-delivered truth**.

The main practical rule is:
- do not stop at `QueueUserAPC` / `NtQueueApcThread` visibility
- prove one truthful alertable-delivery boundary (`SleepEx`, `WaitFor*Ex(..., TRUE)`, `MsgWaitForMultipleObjectsEx(MWMO_ALERTABLE)`, or `NtTestAlert`)
- then freeze the first callback-owned consumer that actually changes behavior

This belongs under the native async branch as a thinner continuation beneath the broader callback/event-loop note, parallel in spirit to the existing completion-port/thread-pool continuation.

## Why this branch is worth adding
Recent native work already covered:
- semantic anchors
- interface-to-state proof
- loader/import first-consumer rules
- service-worker ownership
- broad callback/event-loop ownership
- completion-port/thread-pool dequeue ownership
- GUI message-pump/signal-slot ownership

What remained underfed was a Windows-specific but still practical seam where the bottleneck is neither generic callback plumbing nor IOCP/thread-pool dequeue realism, but ordinary user-mode APC delivery.

This seam has operator value because analysts can easily overread:
- queue API visibility as if it proved delivery
- injection folklore as if it proved execution
- dispatch trampolines as if they were the first effect-bearing owner

## Source takeaways

### 1. Microsoft Learn: `QueueUserAPC`
Source:
- <https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-queueuserapc>

Useful takeaways:
- user-mode APCs execute when the target thread performs an alertable wait
- the relevant waits include `SleepEx`, `SignalObjectAndWait`, `WaitForSingleObjectEx`, `WaitForMultipleObjectsEx`, and `MsgWaitForMultipleObjectsEx`
- when alertable, pending APCs are handled in FIFO order and the wait returns `WAIT_IO_COMPLETION`
- cross-process APC queueing is explicitly discouraged because of rebasing, cross-bitness, and other execution hazards
- `ReadFileEx`, `WriteFileEx`, and waitable timers use APC completion callbacks

Workflow implication:
- queue site != delivery truth
- target-thread alertability is the first decisive reduction boundary

### 2. NtDoc: `NtQueueApcThread`
Source:
- <https://ntdoc.m417z.com/ntqueueapcthread>

Useful takeaways:
- `NtQueueApcThread` exposes three APC callback arguments at the Native API level
- `NtTestAlert` is a manual way to drain pending APCs
- WoW64 APCs require routine encoding / wrapper handling rather than naive ordinary callback assumptions

Workflow implication:
- `NtTestAlert` is an especially useful runtime proof boundary when broad wait-loop tracing is noisy
- WoW64 should be treated as a thinner compatibility subcase, not flattened into same-bitness callback truth

### 3. repnz APC series: user APC API and internals
Sources:
- <https://repnz.github.io/posts/apc/user-apc/>
- <https://repnz.github.io/posts/apc/kernel-user-apc-api/>
- <https://repnz.github.io/posts/apc/wow64-user-apc/>

Useful takeaways:
- the alertable-state requirement is central for ordinary user APC delivery
- `NtQueueApcThread` / `QueueUserAPC` should be separated from actual delivery and dispatch
- `KiUserApcDispatcher` is the user-mode dispatch entry, but not necessarily the final behavior owner
- Wow64 introduces wrapper/encoding behavior that can muddy routine identity
- internal queue/unwait logic is useful for orientation, but the practical workflow still benefits most from isolating one delivered callback and one downstream effect

Workflow implication:
- treat `KiUserApcDispatcher` as a reduction boundary rather than a final stopping point
- prefer the first callback body or immediate downstream consumer that predicts later behavior

### 4. Pavel Yosifovich: APCs as a natural queue
Source:
- <https://scorpiosoftware.net/2024/07/24/what-can-you-do-with-apcs/>

Useful takeaways:
- APC-backed work queues can be elegant and operationally simple
- `SleepEx(0, TRUE)` can be used as an explicit drain of pending APCs
- the target thread might never enter an alertable wait, in which case APC execution never happens

Workflow implication:
- elegant queue structure is still weaker than one proved first consumer
- explicit alertable drains provide good runtime footholds

## Practical branch claim to preserve
The native branch should preserve a thinner continuation note roughly shaped like:

```text
APC production -> alertable-delivery truth -> user dispatch -> first consequence-bearing callback consumer -> effect
```

This note should sit under the native async branch and mainly help with:
- APC-backed async I/O completion
- timer / RPC / callback delivery that ultimately depends on user APC semantics
- deliberate alertable-wait work queues
- injection/instrumentation cases where queued-vs-delivered truth is the real bottleneck

## Stop rules worth preserving canonically
- Do not treat `QueueUserAPC` or `NtQueueApcThread` visibility as delivery proof.
- Do not treat cross-process queueing as execution proof.
- Do not stop at `KiUserApcDispatcher` if the real owner lives in the callback body or one immediate downstream consumer.
- If the target thread never becomes alertable, ordinary user APC claims stay weaker than they look.
- If the case is actually IOCP/thread-pool-shaped, hand off to the completion-port/thread-pool note instead of forcing APC framing.
- If the case is WoW64-heavy, freeze actual callback ownership before widening into wrapper/encoding internals.

## Files this research should support
- `topics/native-apc-alertable-wait-first-consumer-workflow-note.md`
- light sync in:
  - `topics/native-practical-subtree-guide.md`
  - `topics/native-binary-reversing-baseline.md`
  - `index.md`

## Search trace
- `sources/native/2026-03-26-apc-alertable-wait-search-layer.txt`
