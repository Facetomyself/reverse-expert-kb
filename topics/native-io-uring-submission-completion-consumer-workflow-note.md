# Native io_uring submission/completion to first consumer workflow note

Topic class: workflow note
Ontology layers: native practical workflow, async ownership, Linux service/runtime evidence
Maturity: draft-practical
Related pages:
- topics/native-practical-subtree-guide.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/native-epoll-eventfd-first-consumer-workflow-note.md
- topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md
- topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md
- topics/runtime-behavior-recovery.md

## 1. Scope

Use this note when a Linux native target uses `io_uring` and the current lie is:

```text
ring setup, SQE construction, submit call, or CQE visibility == behavior-owned request proof
```

The useful proof object is usually not “the target uses io_uring.” It is one request lineage:

```text
ring setup
  -> SQE prepared with operation, fd/buffer, and user_data
  -> submitted / accepted for kernel processing
  -> CQE made visible
  -> CQE identity and result decoded
  -> first application dispatcher / object / state consumer
  -> later effect or safe lifetime transition
```

Compact stop rule:

```text
ring setup != SQE prepared != submitted/accepted != completion visible != CQE consumed/routed != request-owned effect
```

## 2. When this page is the right entry point

Start here when:
- `io_uring_setup`, `io_uring_queue_init`, `io_uring_get_sqe`, `io_uring_prep_*`, `io_uring_submit`, `io_uring_enter`, `io_uring_wait_cqe`, or raw SQ/CQ ring accesses are visible;
- the call graph becomes misleading because the kernel owns the wait/completion gap;
- request identity depends on `sqe->user_data`, a per-connection object, a buffer-id, or a target-local dispatcher rather than local call order;
- cancellation, timeouts, multishot operations, or ring draining make owner lifetime unclear.

Do not start here when:
- the real bottleneck is still broad subsystem naming or route choice before any async boundary is visible;
- the case is mostly protocol framing after a CQE has already been routed into a parser;
- the target is malware-shaped and the main question is persistence, command-and-control intent, or reporting/handoff rather than native async proof.

## 3. Proof ladder

### A. Ring instance and ownership truth

First freeze the ring instance before following individual SQEs.

Record:
- setup/init site (`io_uring_setup`, `io_uring_queue_init*`, raw `mmap` offsets);
- ring fd and whether it is wrapped in a connection/server object;
- setup flags such as SQPOLL/IOPOLL/deferred task-run only when they change observation semantics;
- shutdown path (`io_uring_queue_exit`, close, drain, cancellation sweep).

Stop rule:

```text
ring exists != this request belongs to this owner
```

A shared ring can carry many sockets/files/tasks. Do not treat ring ownership as request ownership.

### B. SQE preparation truth

At `io_uring_get_sqe` / `io_uring_prep_*` / raw SQE writes, capture:
- opcode and flags;
- fd or fixed-file index;
- buffer pointer / provided-buffer group / length / offset;
- linked-timeout or dependency flags;
- `user_data` assignment and whether it is pointer-shaped, index-shaped, generation-shaped, or stale/uninitialized.

The `user_data` field is the normal completion-side identity bridge. If it is not assigned for every SQE, stale values from prior SQE use can become false-owner evidence.

Stop rule:

```text
SQE slot/index order != user_data identity != live owner object
```

### C. Submit / accept-for-processing truth

Separate SQE construction from kernel notification.

Useful proof points:
- `io_uring_submit(...)`, `io_uring_submit_and_wait(...)`, or direct `io_uring_enter(...)`;
- `to_submit`, return value, and error path;
- SQPOLL-specific wake/wait behavior when the submitter is not the only actor consuming SQ entries;
- queue-full / dropped-SQE handling.

Stop rule:

```text
prepared != submitted != accepted/in-flight
```

A prep helper call without a submit boundary is only target-local intent.

### D. CQE visible truth

At completion retrieval, preserve:
- `cqe->user_data`;
- `cqe->res` as success byte count, fd, event mask, `-errno`, or operation-specific result;
- `cqe->flags`, especially `IORING_CQE_F_MORE` and buffer-selection bits;
- whether the completion was obtained by wait, peek, batch harvest, or direct CQ-ring access;
- whether `io_uring_cqe_seen(...)` / CQ head advancement has happened.

Stop rule:

```text
CQE visible != CQE consumed/routed != effect owned
```

A CQE in shared memory is availability truth. The first behavior owner is often one switch/table/object lookup later.

### E. First application consumer truth

The most useful breakpoints/hooks are often not only on liburing wrappers. Also watch:
- the switch or table keyed by `user_data` / request type;
- connection/session object lookup from `user_data`;
- buffer-id extraction and buffer-ring recycle path;
- state-machine reducer after `cqe->res` normalization;
- object free/reuse after `io_uring_cqe_seen(...)`;
- resubmission path for reads/accepts/timeouts.

The consumer is the first place where the completion becomes target semantics: message parse, connection state update, retry, close, timer expiry, callback invocation, or durable output.

Stop rule:

```text
identity decoded != state consumer ran != later effect owned
```

## 4. Cancellation, timeout, and drain hazards

Cancellation is a separate request, not a magic deletion of the original request.

Keep these rows separate:
- cancel SQE prepared/submitted;
- cancel CQE result (`0`, `-ENOENT`, `-EALREADY`, count for cancel-all cases);
- original request CQE result (`-ECANCELED`, `-EINTR`, ordinary success/error, or late completion);
- owner-object lifetime decision after both sides are reconciled.

Compact rule:

```text
cancel submitted != target found != target completed/canceled != owner retired safely
```

Tactics:
- if cancel returns `-ENOENT`, search for an earlier or racing ordinary completion;
- if cancel returns `-EALREADY`, keep waiting for the original request’s CQE before declaring the object safe to free;
- if linked timeouts are used, preserve both the primary request’s result and the timeout/cancel side effect;
- during ring shutdown, prove whether pending requests are drained, canceled, ignored, or allowed to race object teardown.

## 5. Multishot request hazards

For multishot accept/recv/read/poll, one SQE can generate many CQEs.

Preserve:
- initial multishot SQE identity and owner;
- every CQE instance, `res`, flags, and buffer id;
- `IORING_CQE_F_MORE` while the operation remains active;
- final CQE without `F_MORE` as a lifetime boundary;
- explicit cancel or operation-specific termination reason.

Stop rule:

```text
first CQE != multishot owner retired
F_MORE set != final lifetime boundary
final CQE != all prior data consumed
```

For provided-buffer paths, split buffer selection from parser ownership:

```text
buffer selected != bytes parsed != message/state consumed != buffer safely recycled
```

## 6. Observation plan

A practical minimum hook/breakpoint set:

1. Ring setup/init and shutdown.
2. `io_uring_get_sqe` / `io_uring_prep_*` family or raw SQE writes.
3. `io_uring_sqe_set_data*` and manual `sqe->user_data` writes.
4. `io_uring_submit*` / `io_uring_enter` boundaries.
5. `io_uring_wait_cqe`, `io_uring_peek_cqe`, batch-CQE harvest, or raw CQ reads.
6. `io_uring_cqe_seen` / CQ head advancement.
7. The target-local dispatcher keyed by `user_data`, request type, fd, buffer id, or connection object.
8. Cancel/timeout setup and both cancel-side and original-request CQE consumers.

Evidence row to keep in the notebook:

```text
ring | sqe_site | opcode | fd/fixed | buffer/bgid | user_data | submit_ret | cqe_res | cqe_flags | seen/reused | dispatcher | state/effect | lifetime note
```

## 7. Handoff rules

Handoff to protocol notes when the first consumer is clearly a frame/parser/state reducer:
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md`

Handoff to native callback/event-loop notes when `io_uring` only wakes a broader event framework:
- `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md`
- `topics/native-epoll-eventfd-first-consumer-workflow-note.md`

Handoff to runtime evidence notes when the problem becomes compare-run alignment, trace selection, or causality rather than request-lineage proof:
- `topics/runtime-behavior-recovery.md`
- `topics/compare-run-design-and-divergence-isolation-workflow-note.md`
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`

## 8. Summary

`io_uring` makes native async work look deceptively local because SQEs and CQEs are ordinary memory structures. Treat them as a shared kernel/user protocol with explicit proof boundaries.

The useful compact rule is:

```text
ring setup != SQE prepared != submitted/accepted != completion visible != CQE consumed/routed != request-owned effect
```

The practical win is to preserve `user_data`, `res`, flags, buffer id, cancellation result, multishot lifetime, and first dispatcher/consumer separately before claiming behavior ownership.
