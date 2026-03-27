# 2026-03-27 Linux reactor readiness vs delivery and consumer truth notes

Topic class: source-backed practical notes
Branch: native desktop/server practical workflows
Focus: epoll / eventfd / timerfd / libuv async wakeups

## Why this note exists
Linux reactor-shaped cases are easy to overread.
Analysts often stop at one of these weak proof objects:
- `epoll_wait(...)` returned
- `eventfd` became readable
- `timerfd` became readable
- `uv_async_send(...)` was called

But later case work often needs the stronger boundary:
- the fd was actually drained or rearmed the way this runtime expects
- one loop-thread callback was actually delivered
- one consequence-bearing consumer actually changed later behavior

Compact branch-memory shorthand preserved from this run:
- `registered != ready != returned != drained/rearmed != callback-delivered != consumed`
- for libuv async specifically: `uv_async_send-called != wakeup-observed != async-callback-delivered`

## Conservative retained takeaways
### 1. epoll readiness is not full consumption truth
The epoll man page preserves a useful split between:
- interest-list registration
- kernel ready-list membership
- one `epoll_wait(...)` return
- user-space draining until `EAGAIN`
- explicit rearm when `EPOLLONESHOT` is in play

Practical implication:
- do not stop at `epoll_wait(...)` return if the real question is whether one reactor consumer fully handled the fd, advanced state, or made the fd eligible for the next truthful wakeup
- in ET cases especially, `returned != drained`, and in ONESHOT cases `returned != rearmed`

### 2. eventfd readability is counter truth, not downstream consumer truth
The eventfd man page gives a narrow operator rule:
- writes add to a 64-bit counter
- readability means counter `> 0`
- a read returns an 8-byte value and either resets the counter to zero or decrements by one in semaphore mode

Practical implication:
- `eventfd` readable is only proof that the counter is nonzero
- it is weaker than proving which loop-side handler drained it
- it is weaker than proving one downstream state write or callback family that the drain caused

### 3. timerfd readability is expiration truth, not timer-handler truth
The timerfd man page preserves another useful split:
- timer armed
- one or more expirations occurred
- fd became readable
- read returned the expiration count since the last successful read or since settings changed
- later handler logic consumed that fact and changed behavior

Practical implication:
- timer readability proves expiration count availability, not that the application-level timer consumer already ran
- accumulated expiration count can matter in replay/compare work because a later handler may collapse several expirations into one branch or one batch-style update

### 4. libuv async wakeups are deliberately coalesced
libuv documents two practical facts worth preserving:
- `uv_async_send(...)` is safe from any thread and the callback runs on the loop thread
- libuv coalesces sends, so multiple sends before callback delivery may still yield only one callback invocation

Practical implication:
- do not count raw `uv_async_send(...)` frequency as callback frequency
- keep `send-called`, `loop-woken`, and `async-callback-delivered` separate
- when the real behavioral owner is later, keep the smaller split `async-callback-delivered != consequence-bearing-consumer`

## Suggested operator stop rule for Linux reactor cases
When a native async case narrows into Linux reactor ownership, preserve this ladder first:

```text
registered != ready != returned != drained/rearmed != callback-delivered != consumed
```

Use it like this:
- if you only proved `epoll_ctl(...)` / handle registration, you still have no delivery truth
- if you only proved `epoll_wait(...)` returned, you still may lack drain/rearm truth
- if you only proved `eventfd` / `timerfd` readability, you still may lack one loop-side handler or callback truth
- if you only proved `uv_async_send(...)`, you still may lack one loop-thread callback delivery, and coalescing means raw send count is weaker than it looks
- if you only proved one loop callback, you may still lack the later consequence-bearing consumer

## Sources retained
- epoll(7): <https://man7.org/linux/man-pages/man7/epoll.7.html>
- eventfd(2): <https://man7.org/linux/man-pages/man2/eventfd.2.html>
- timerfd_create(2): <https://man7.org/linux/man-pages/man2/timerfd_create.2.html>
- libuv async docs: <https://docs.libuv.org/en/v1.x/async.html>
- libuv threads guide: <https://docs.libuv.org/en/v1.x/guide/threads.html>
