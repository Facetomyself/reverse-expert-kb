# Source note — io_uring submission/completion to first consumer

Date: 2026-05-30

Scope: source-backed notes for a native Linux workflow seam where a target uses `io_uring` and the analyst must avoid overreading ring setup, SQE preparation, or CQE visibility as behavior ownership.

Search artifact:
- `sources/native/2026-05-30-0450-io-uring-submission-completion-consumer-search-layer.json`

## Sources consulted

- `io_uring(7)` Linux manual page — https://man7.org/linux/man-pages/man7/io_uring.7.html
- `io_uring_enter(2)` Linux manual page — https://man7.org/linux/man-pages/man2/io_uring_enter.2.html
- `io_uring_sqe_set_data(3)` liburing manual page — https://man7.org/linux/man-pages/man3/io_uring_sqe_set_data.3.html
- `io_uring_cqe_seen(3)` liburing manual page — https://man7.org/linux/man-pages/man3/io_uring_cqe_seen.3.html
- Debian/liburing `io_uring_cancelation(7)` — https://manpages.debian.org/testing/liburing-dev/io_uring_cancelation.7.en.html
- Debian/liburing `io_uring_multishot(7)` — https://manpages.debian.org/testing/liburing-dev/io_uring_multishot.7.en.html
- Jens Axboe / liburing wiki, `io_uring and networking in 2023` — https://github.com/axboe/liburing/wiki/io_uring-and-networking-in-2023

## Extracted practical facts

### SQE preparation is not kernel-owned work yet

`io_uring(7)` describes the normal model as:

1. set up shared submission/completion rings;
2. create one SQE per requested operation and place it on the SQ;
3. call `io_uring_enter(2)` / a liburing submit helper to tell the kernel to dequeue and begin processing SQEs;
4. consume CQEs that the kernel writes back after request processing.

For reversing, `io_uring_get_sqe(...)`, `io_uring_prep_*`, and writes to SQE fields prove request construction, not accepted kernel work. The first stronger submit boundary is the `io_uring_enter(...)` / `io_uring_submit(...)` path and the number of submissions it reports or attempts.

### Completion order and request identity must be proved by `user_data`

`io_uring(7)` explicitly warns that requests can complete in any order, and recommends checking which request a CQE corresponds to, commonly via `user_data`.

`io_uring_sqe_set_data(3)` says a pointer or 64-bit value may be associated with an SQE and recovered from the CQE. It also warns that if `user_data` is not set, the field may contain a value from a previous use of that SQE.

Reverse implication:
- do not infer request identity from SQE slot reuse, nearby buffer address, or submission order when multiple requests are in flight;
- hook or trace the write to `sqe->user_data` / `io_uring_sqe_set_data*` and the CQE consumer’s read of `cqe->user_data` / `io_uring_cqe_get_data*`;
- stale or uninitialized `user_data` is itself a possible false-owner source.

### CQE visibility is not consumer proof until the app marks or routes it

`io_uring_cqe_seen(3)` marks a completion as consumed and makes the CQ slot reusable. Before that, a CQE may be visible in the shared ring but not yet routed into the target’s dispatcher, parser, object lifetime, or state transition.

Reverse implication:
- a CQE in memory, an `io_uring_wait_cqe(...)` return, or a ring-tail movement proves completion availability;
- the behavior owner is often one step later: the switch on `user_data`, callback table lookup, connection object lookup, buffer-id branch, state-machine reducer, or task object free/reuse path.

### Cancellation and timeout evidence is two-sided and racy

The liburing cancellation overview describes cancel requests keyed by `user_data` or fd, with separate CQEs for the cancel request and the canceled/original request. It also states CQE order is not guaranteed; the cancel CQE may arrive before or after the original request’s CQE. Result values such as `0`, `-ENOENT`, `-EALREADY`, `-ECANCELED`, or ordinary completion/error must be interpreted as different proof objects.

Reverse implication:
- a submitted cancel SQE does not prove the target request was canceled;
- a cancel success CQE is still not the same as the original request’s final consumer state;
- `-EALREADY` and `-ENOENT` should trigger a search for original-request completion, object lifetime, and close/drain logic before claiming no effect or cancellation effect.

### Multishot requests invert the one-SQE/one-CQE assumption

The liburing multishot overview states that a single SQE can generate multiple CQEs. `IORING_CQE_F_MORE` marks that more completions are expected; a final CQE without `F_MORE` indicates termination through error, explicit cancel, or an operation-specific condition. Multishot receive may also use provided buffers, with buffer selection encoded in CQE flags.

Reverse implication:
- do not free or retire the owner after the first CQE if `F_MORE` is set;
- preserve each CQE instance, buffer-id, and `res` separately;
- the final CQE is a lifetime boundary, not merely another data event.

## Operator synthesis

The compact seam to preserve in the KB:

```text
ring setup != SQE prepared != submitted/accepted != completion visible != CQE consumed/routed != request-owned effect
```

Smaller request-identity rule:

```text
slot/index order != user_data identity != live owner object != effect owner
```

Smaller cancellation/lifetime rule:

```text
cancel submitted != target found != target completed/canceled != owner retired safely
```

This page belongs in the native async branch because the target usually remains a readable Linux native process, but direct call graph proof breaks at a kernel-shared completion-ring boundary.
