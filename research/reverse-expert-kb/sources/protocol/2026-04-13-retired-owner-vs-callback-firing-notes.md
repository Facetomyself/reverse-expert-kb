# Retired-owner vs callback-firing notes
Date: 2026-04-13
Branch: protocol / async pending-owner continuation
Status: retained synthesis notes for external-research-driven maintenance

## Why this batch exists
The protocol branch already had:
- broad pending-request correlation / async-reply ownership work
- a thinner generation / epoch / slot-reuse realism note
- a recent timeout/cancel cleanup sharpening pass

What still looked worth preserving as its own bounded continuation was a narrower compare seam:
- timeout/cancel cleanup already looks like the main liar
- yet one callback, handler, completion-queue tag, or future completion still appears near or after retirement
- analysts overread that delivery as proof that the same request stayed live

This batch was chosen to land that still-missing continuation instead of repeating broader timeout/cleanup wording.

## Search posture for this run
Search was attempted via the search-layer skill with explicit requested sources:
- Exa
- Tavily
- Grok

Result quality this run:
- Exa: succeeded
- Tavily: succeeded
- Grok: invoked but returned repeated `502 Bad Gateway` errors

Saved search trace:
- `sources/protocol/2026-04-13-0450-retired-owner-callback-firing-search-layer.txt`

## Retained practical support

### 1. Boost.Asio `basic_waitable_timer::cancel`
URL:
- https://www.boost.org/doc/libs/latest/doc/html/boost_asio/reference/basic_waitable_timer/cancel.html

Retained points:
- `cancel()` forces completion of pending async waits
- cancelled wait handlers are invoked with `boost::asio::error::operation_aborted`
- but if the timer has already expired, handlers may already have been invoked or queued for near-future invocation
- those already-queued handlers can no longer be cancelled and may still report successful wait completion

Operator value:
- strong source-backed reminder that cancel request / cancel return is weaker than actual handler fate
- useful concrete proof that a fired callback after a retire-looking boundary is not automatically contradictory or automatically live-owner proof

### 2. gRPC C++ `ClientContext::TryCancel()` and `CompletionQueue::Next()`
URLs:
- https://grpc.github.io/grpc/cpp/classgrpc_1_1_client_context.html
- https://grpc.github.io/grpc/cpp/classgrpc_1_1_completion_queue.html
- https://grpc.io/docs/guides/cancellation/

Retained points:
- `TryCancel()` is explicitly best-effort
- there is no guarantee the call will be cancelled
- `TryCancel()` does not change tags already pending on the completion queue; pending tags are still delivered
- `CompletionQueue::Next()` documents that each tag sent to the queue is delivered regardless of whether the operation succeeded; `ok` is the success/failure classifier
- gRPC cancellation guidance also makes clear that application work must still coordinate with cancellation rather than assuming the library can synchronously stop all ongoing processing

Operator value:
- strong source-backed reminder that cancel request, pending-tag delivery, `ok` classification, and same-request live-owner truth are different proof objects
- useful concrete analogy for protocol/RPC cases where one visible callback or queue event still arrives after a retire-looking boundary

### 3. Python `asyncio.wait_for()`
URL:
- https://docs.python.org/3/library/asyncio-task.html#asyncio.wait_for

Retained points:
- timeout cancels the task and raises `TimeoutError`
- `wait_for()` then waits until the future is actually cancelled
- the total wait time may exceed the timeout

Operator value:
- good official reminder that timeout observation is weaker than actual retirement completion
- useful for preserving the split between timeout boundary truth and true task-owner teardown truth

### 4. Tokio `time::timeout`
URL:
- https://docs.rs/tokio/latest/tokio/time/fn.timeout.html

Retained points:
- timeout is checked before polling the future
- if the future does not yield, it may complete and exceed the timeout without returning an error
- cancelling the timeout wrapper is done by dropping the future and requires no extra cleanup work

Operator value:
- strong reminder that deadline machinery and callback/task fate are not the same object
- useful source-backed support for not overreading one timeout boundary as proof that a still-running path or later completion became impossible

## Cross-source synthesis
A durable workflow lesson from this batch is:

```text
retire-looking boundary observed
  -> pending handler/tag/callback may still be deliverable
  -> delivered callback may carry abort/failure/success-shaped status
  -> runtime still needs one current-owner check before downstream effect is truthful
  -> callback delivery alone is weaker than same-request live-owner proof
```

A second compact split worth preserving is:

```text
timeout/cancel requested
  != owner fully retired
  != pending callback cannot still fire
  != fired callback still belongs to the same live request
  != later consequence truth
```

Useful cross-family reminders to preserve:
- cancel request is weaker than handler fate
- timeout boundary is weaker than actual retirement completion
- pending tag delivery is weaker than same-request ownership
- callback status/`ok` is weaker than downstream consume/wakeup truth

## What this batch does *not* justify
Do not overclaim from this source set.
It does **not** prove that every post-timeout callback implies a stale-owner race.
Other cases still exist:
- successful completion beating the cleanup path fairly
- framework-specific callback queuing or cooperative-yield semantics
- later generation/epoch reuse behind the same visible callback/tag
- broader parser/auth/output questions when owner-lifetime is not yet the real bottleneck

The narrower justified claim is:
- once timeout/cancel cleanup already looks like the main liar, one separate continuation should explicitly teach analysts to compare retirement truth against callback/tag/handler delivery truth instead of flattening them together.

## KB maintenance conclusion from this batch
This batch justified:
- adding a new bounded workflow note for retired-owner vs callback-firing compare work
- linking that continuation from the existing pending-request generation / epoch / slot-reuse note
- synchronizing the protocol subtree guide, protocol parent pages, and top-level index so the new seam does not live only as a leaf
