# Overlapped event vs IOCP packet vs thread-pool I/O callback notes

Date: 2026-03-27
Branch: native desktop/server practical workflows
Focus: practical stop rules for Windows overlapped I/O cases where analysts over-collapse event signaling, IOCP delivery, and TP_IO callback truth

## Question
What is the smallest practical rule that prevents analysts from stopping too early when a Windows target mixes:
- explicit `OVERLAPPED.hEvent` signaling
- I/O completion port delivery
- `CreateThreadpoolIo` / `StartThreadpoolIo` / `CancelThreadpoolIo`
- `FILE_SKIP_COMPLETION_PORT_ON_SUCCESS`

## Main answer
The durable operator rule is:

- **event signaled != IOCP packet dequeued != TP_IO callback delivered**

These are different proof objects.

A more precise native stop rule is:
- an explicit `OVERLAPPED.hEvent` can become signaled even when no IOCP packet is queued for that operation under `FILE_SKIP_COMPLETION_PORT_ON_SUCCESS`
- a handle-associated IOCP may still carry posted control packets whose `lpOverlapped` is not a real I/O-owned `OVERLAPPED`
- `CreateThreadpoolIo(...)` only binds the handle/callback object; it does not prove delivery for any specific operation
- `StartThreadpoolIo(...)` is required before **each** asynchronous operation that is meant to produce a TP_IO callback
- when an overlapped operation returns immediately with success on a handle using `FILE_SKIP_COMPLETION_PORT_ON_SUCCESS`, the TP_IO callback is not called and `CancelThreadpoolIo(...)` is required to retire the pending notification expectation

So the practical diagnostic ladder is:
1. did the operation complete?
2. if yes, was only the explicit event/signaling path observed?
3. was an IOCP packet actually queued/dequeued, or was this a skip-on-success case?
4. if the target uses TP_IO, was `StartThreadpoolIo(...)` issued for this operation?
5. if the I/O returned immediate success under skip-on-success, did the code call `CancelThreadpoolIo(...)` rather than waiting for a callback that will never arrive?
6. only after that ask which callback/consumer first changed behavior

## Why this matters in reversing
Without this split, a practical analysis goes wrong in three common ways:
- seeing an event become signaled and overreading that as proof that the IOCP worker or TP_IO callback must also have run
- seeing a `CreateThreadpoolIo(...)` registration and overreading that as proof that all overlapped completions on the handle will reach the callback
- seeing a `GetQueuedCompletionStatus(...)` loop and assuming every dequeued packet is genuine I/O-owned completion rather than possible `PostQueuedCompletionStatus(...)` control traffic

## Source-backed points collected this run

### 1. IOCP is packet delivery, not generic completion folklore
Microsoft Learn on IOCP says asynchronous I/O completion packets are queued to the associated completion port and consumed via `GetQueuedCompletionStatus(...)`.

Practical implication:
- do not narrate “the operation completed” as if that automatically proves “the packet was dequeued by the worker that matters”

### 2. `PostQueuedCompletionStatus(...)` style traffic must stay separate from I/O-owned packets
The KB already preserved this from prior work, and this run keeps it because it is the neighboring confusion surface.

Practical implication:
- packet dequeue alone is weaker than request ownership unless one carrier (`completion key`, `OVERLAPPED*`, task object) leads to a real consumer

### 3. `CreateThreadpoolIo(...)` is object creation; `StartThreadpoolIo(...)` is per-operation intent
Microsoft Learn states you must call `StartThreadpoolIo(...)` before initiating **each** asynchronous operation.

Practical implication:
- handle binding is not operation delivery proof
- reverse one operation at a time, not one `TP_IO` object at a time

### 4. Immediate success under `FILE_SKIP_COMPLETION_PORT_ON_SUCCESS` suppresses TP_IO callback delivery
Microsoft Learn for `CreateThreadpoolIo(...)`, `StartThreadpoolIo(...)`, and `CancelThreadpoolIo(...)` all preserve the same special case:
- if the handle uses `FILE_SKIP_COMPLETION_PORT_ON_SUCCESS`
- and the asynchronous operation returns immediately with success
- then the callback is not called
- and thread-pool I/O notification must be canceled

Practical implication:
- “callback absent” is not evidence that the callback family is dead, unrelated, or bypassed by some mystery branch
- first ask whether this operation completed synchronously in a skip-on-success configuration

### 5. Raymond Chen gives the operator-friendly interpretation
Raymond Chen’s discussion of `SetFileCompletionNotificationModes(...)` clarifies that suppressing completion-port-on-success changes what the completion machinery reports, while explicit event signaling remains conceptually separate. He also distinguishes the file object’s hidden handle event from an explicit event in `OVERLAPPED.hEvent`.

Practical implication:
- if an analyst only observes event-based completion, they still have not proved IOCP or TP_IO callback ownership
- explicit event visibility should often be treated as a branch-separation clue, not end-state proof

### 6. Winsock’s overlapped completion matrix reinforces the split
Microsoft’s summary table for overlapped completion indication mechanisms distinguishes:
- event-object notification
- completion-routine notification
- possible completion-port notification when no other WinSock-supported mechanism is selected

Practical implication:
- completion mechanism selection must be localized per operation shape rather than narrated as one undifferentiated “async completion” object

## Practical RE stop rules to preserve canonically
- **event signaled != IOCP packet dequeued != TP_IO callback delivered**
- `CreateThreadpoolIo(...)` != per-operation callback proof
- `StartThreadpoolIo(...)` must be checked per operation, not once per handle
- immediate success under `FILE_SKIP_COMPLETION_PORT_ON_SUCCESS` can legitimately produce no TP_IO callback
- absence of callback + presence of success is a reason to check `CancelThreadpoolIo(...)`, not a reason to overread alternate callback ownership
- IOCP worker visibility still requires separation of posted control packets from real I/O-owned packets

## Good fit in the KB
This material is a thinner continuation inside:
- `topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md`

It strengthens that note with one more practical split around mixed completion semantics:
- explicit event path
- IOCP packet path
- TP_IO callback path

## Sources consulted
- Microsoft Learn: `CreateIoCompletionPort`
- Microsoft Learn: `GetQueuedCompletionStatus`
- Microsoft Learn: `I/O Completion Ports`
- Microsoft Learn: `CreateThreadpoolIo`
- Microsoft Learn: `StartThreadpoolIo`
- Microsoft Learn: `CancelThreadpoolIo`
- Microsoft Learn: `Summary of Overlapped Completion Indication Mechanisms in the SPI`
- Raymond Chen, The Old New Thing: synchronous-success completion-notification behavior under `SetFileCompletionNotificationModes`
