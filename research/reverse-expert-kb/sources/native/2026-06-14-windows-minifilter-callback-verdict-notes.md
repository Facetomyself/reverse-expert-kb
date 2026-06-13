# Windows Minifilter Callback / User-Mode Verdict / I/O Completion Source Notes

Date: 2026-06-14
Scope: source-backed notes for a native Windows workflow page about file-system minifilter callbacks, user-mode verdict handoff, and first policy/effect proof.
Search artifact: `sources/native/2026-06-14-0450-windows-minifilter-search-layer.json`

## Sources consulted

- Microsoft Learn, "Initiating Filtering" — `https://learn.microsoft.com/en-us/windows-hardware/drivers/ifs/initiating-filtering`
- Microsoft Learn, "Writing Pre-operation Callback Routines" — `https://learn.microsoft.com/en-us/windows-hardware/drivers/ifs/writing-preoperation-callback-routines`
- Microsoft Learn, "Pending an I/O Operation in a Preoperation Callback Routine" — `https://learn.microsoft.com/en-us/windows-hardware/drivers/ifs/pending-an-i-o-operation-in-a-preoperation-callback-routine`
- Microsoft Learn, "Completing an I/O Operation in a Preoperation Callback Routine" — `https://learn.microsoft.com/en-us/windows-hardware/drivers/ifs/completing-an-i-o-operation-in-a-preoperation-callback-routine`
- Microsoft Learn, "Communication Between User-mode and Minifilters" — `https://learn.microsoft.com/en-us/windows-hardware/drivers/ifs/communication-between-user-mode-and-kernel-mode`
- Microsoft Learn, `FltSendMessage` — `https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/fltkernel/nf-fltkernel-fltsendmessage`

## Extracted source facts

- A minifilter becomes active only after registration and `FltStartFiltering(...)`; after that call, Filter Manager can present I/O requests and volume notifications even before `FltStartFiltering` returns.
- Pre-operation callbacks are registered through `FLT_REGISTRATION.OperationRegistration` and passed to `FltRegisterFilter(...)`; the minifilter receives only operation types for which it registered a pre-operation or post-operation callback.
- When Filter Manager calls a pre-operation callback, the minifilter temporarily controls the I/O operation until it returns a non-pending status or later calls `FltCompletePendedPreOperation(...)` for a pended operation.
- A pre-operation callback can pass through without a post callback, pass through with a post callback, complete the operation immediately, or pend the operation.
- Pended pre-operation work uses `FLT_PREOP_PENDING`; the driver retains control until a work routine calls `FltCompletePendedPreOperation(...)`. The docs warn that pended work must be IRP-based and that large-scale pending should use cancel-safe queues rather than flooding system work queues.
- Completing an operation means halting lower-stack/file-system processing, assigning final `IoStatus.Status`, and returning it to Filter Manager with `FLT_PREOP_COMPLETE`. Completion may also happen later from the work routine for a pended operation via `FltCompletePendedPreOperation(..., FLT_PREOP_COMPLETE, ...)`.
- Filter Manager communication ports let a kernel minifilter communicate with user-mode services. The driver creates a server port with `FltCreateCommunicationPort(...)`; a user-mode service connects with `FilterConnectCommunicationPort(...)`; each connection has private endpoints and a message queue.
- `FltSendMessage(...)` sends a minifilter message to a waiting user-mode application and can optionally receive a reply. This supports antivirus / scanner-style user-mode verdict workflows, but a send or reply is still weaker than proving the kernel-side completion status and downstream file-system/user-visible effect.

## Practical synthesis

The useful reverse-engineering split is:

```text
registered/started != operation-selected != pre-callback-entered != verdict/context-built != pended/sent != replied/decided != completed/resumed != user-visible effect
```

This prevents four common overreads:

1. Treating a registered minifilter or altitude as proof it saw the operation under analysis.
2. Treating pre-callback entry as proof of a block/allow decision.
3. Treating a user-mode scan message as proof of a returned verdict.
4. Treating a returned verdict as proof of the kernel-side `IoStatus` / completion path and the final user-visible file-system outcome.

## Operator implications

- Freeze the exact operation class (`IRP_MJ_CREATE`, write, set information, cleanup, etc.) before widening into policy logic.
- In pre-op traces, capture callback return status, `Data->IoStatus.Status`, completion context, whether a post-op callback is requested, and whether `FLT_PREOP_PENDING` transfers ownership to a worker or queue.
- For scanner/verdict designs, pair `FltSendMessage(...)` with the connected client port, timeout behavior, user-mode receive/reply, reply decode, and the later `FltCompletePendedPreOperation(...)` call.
- For missing or inconsistent decisions, check operation mismatch, altitude/order, volume attachment, non-IRP/paging I/O restrictions, queue/cancel behavior, disconnected user-mode service, timeout fallback, and post-op-only consumers before claiming target policy behavior.
