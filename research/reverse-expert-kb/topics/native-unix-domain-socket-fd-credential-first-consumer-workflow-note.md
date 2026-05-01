# Native Unix-Domain Socket FD / Credential to First Consumer Workflow Note

Topic class: workflow note
Ontology layers: workflow/sensemaking, runtime-evidence bridge, native desktop/server practical branch
Maturity: emerging
Related pages:
- topics/native-binary-reversing-baseline.md
- topics/native-practical-subtree-guide.md
- topics/native-dbus-service-activation-to-method-consumer-workflow-note.md
- topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/protocol-ingress-ownership-and-receive-path-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/runtime-behavior-recovery.md

## 1. What this workflow note is for

Use this note when a Linux / Unix native target exposes behavior through an AF_UNIX / AF_LOCAL IPC seam and the visible socket is not yet enough to explain the behavior.

Typical surfaces:
- pathname or abstract Unix-domain socket names
- `socketpair(...)` inherited across fork/exec
- `sendmsg(...)` / `recvmsg(...)` with ancillary data
- `SCM_RIGHTS` file-descriptor passing
- `SO_PEERCRED`, `SO_PASSCRED`, `SCM_CREDENTIALS`, `SO_PEERSEC`, or `SCM_SECURITY`
- brokers or daemons that receive a descriptor, authorize a peer, then route the request into one handler

This is not a Unix-socket API tutorial. It is a stop-rule note for native service reversing.

The goal is to move from:

```text
socket path / abstract name / sendmsg / recvmsg / credential check visible
```

to:

```text
one proved chain from endpoint and current peer
through credential semantics and intact ancillary receipt
into one descriptor lineage, dispatch decision, and first handler-owned consumer
```

## 2. When to use this note

Use this note when most of the following are true:
- the target is a local Linux / Unix daemon, desktop helper, broker, container/runtime helper, updater, agent, device service, or service supervisor
- a Unix-domain socket is the most concrete ingress, handoff, or privilege-boundary surface
- the interesting object may be a passed fd, not only payload bytes
- credential or security-label checks affect routing or authorization
- static xrefs to `sendmsg(...)`, `recvmsg(...)`, `getsockopt(SO_PEERCRED)`, or control-message helpers are visible but do not yet prove which request changes behavior
- one narrow endpoint-to-consumer proof would make the service path trustworthy

Do **not** use this as the primary guide when:
- the first trustworthy semantic anchor is still missing; start with semantic-anchor stabilization
- the case is explicitly D-Bus-shaped and the main liar is bus name / activation / object-interface-member dispatch; start with the D-Bus workflow note, then return here only if fd or credential ancillary data becomes the bottleneck
- the Unix socket is just a generic transport for a larger protocol grammar; start with protocol ingress / parser-to-state recovery once endpoint ownership is already settled
- the descriptor has already been received and retained, and the remaining problem is a generic callback/event-loop consumer

## 3. Core claim

In Unix-domain socket service work, socket visibility is usually only ingress evidence. The behavior-bearing truth may live several rungs later:

```text
socket endpoint found
  != connection / peer identity frozen
  != credential object selected with correct semantics
  != ancillary message received intact
  != received descriptor object lineage understood
  != dispatch / authorization branch selected
  != first handler-owned consumer or downstream effect proved
```

Compact branch memory:

```text
endpoint != peer/cred != ancillary-intact != fd-lineage != dispatched != consumed
```

The common mistake is to stop at one of the earlier rungs:
- a socket file exists
- an abstract socket name is visible in strings
- `connect(...)` or `accept(...)` succeeds
- `SO_PEERCRED` returns a uid/pid/gid
- a `recvmsg(...)` call returns payload bytes
- an `SCM_RIGHTS` or `SCM_CREDENTIALS` branch exists statically
- lower-surface tracing shows a sender-side fd-pass event

Those are useful reductions. They are not yet proof that the current peer, current credential, current descriptor object, and current handler branch own the later effect.

## 4. The boundaries to mark explicitly

### A. Endpoint and namespace boundary

First decide what kind of endpoint exists:
- pathname socket
- Linux abstract namespace socket
- unnamed/socketpair-only connection
- inherited fd from service manager, launcher, broker, or parent process
- container/namespace-local socket whose apparent path or inode differs from the analyst host view

What to capture:
- socket type: `SOCK_STREAM`, `SOCK_DGRAM`, or `SOCK_SEQPACKET`
- endpoint address and address length, not just printable `sun_path`
- namespace/container/chroot context
- filesystem directory/socket permissions for pathname sockets
- whether abstract socket permissions are being mistakenly inferred from nonexistent filesystem metadata

Stop rule:

```text
socket name visible != same endpoint used by this client/peer/run
```

### B. Connection and peer-identity boundary

Freeze the concrete peer relation before reading credential checks as behavior proof.

What to capture:
- accept/connect/socketpair inheritance path
- process IDs, executable paths, namespaces, cgroups, user IDs, groups, SELinux/AppArmor context if relevant
- whether a broker sits between the original client and the handler process
- whether reconnect, restart, or fd inheritance changed the peer between observation and behavior

Stop rule:

```text
listening endpoint exists != current connected peer owns this request
```

### C. Credential-semantics boundary

Credential APIs answer subtly different questions.

Keep separate:
- `SO_PEERCRED`: connection-time peer credentials for connected AF_UNIX stream sockets and socket pairs
- `SO_PASSCRED` / `SCM_CREDENTIALS`: per-message credentials received through ancillary data, with kernel checks and privilege exceptions
- `SO_PEERSEC` / `SO_PASSSEC` / `SCM_SECURITY`: security-label evidence where supported and enabled

What to capture:
- which API is used
- when the credential is sampled
- whether the checked credential is peer identity, per-message sender identity, broker identity, or delegated/declared credential
- the exact authorization branch and failure path

Stop rule:

```text
credential object read != authorization branch selected != handler consumer reached
```

### D. Ancillary-message integrity boundary

For descriptor or credential passing, the control buffer is often the proof object.

What to capture at `recvmsg(...)`:
- `msg_control`, `msg_controllen`, `cmsghdr.cmsg_level`, `cmsghdr.cmsg_type`, and count
- `SCM_RIGHTS`, `SCM_CREDENTIALS`, `SCM_SECURITY` separately
- `MSG_CTRUNC` and short control-buffer cases
- `MSG_CMSG_CLOEXEC` or later `fcntl(FD_CLOEXEC)` handling when exec/lifetime matters
- real-data byte association, especially on stream sockets where ancillary data acts as a barrier

Stop rule:

```text
recvmsg returned bytes != ancillary payload survived intact and belongs to this logical request
```

### E. Descriptor-lineage boundary

With `SCM_RIGHTS`, the raw fd number is not the identity. The receiver gets a descriptor referring to an open file description; the integer value can differ.

What to capture:
- sender-side fd object: file/socket/pipe/eventfd/memfd/device/pty/epoll/etc.
- receiver-side new fd number and `/proc/<pid>/fd` target
- `/proc/<pid>/fdinfo` when file offset, flags, mount/user namespace, or eventfd/epoll state matters
- whether the object is read, written, polled, mmaped, passed again, retained in a table, or closed
- whether descriptor truncation, `RLIMIT_NOFILE`, or close-on-exec changes lifetime

Stop rule:

```text
fd number seen != same open-file-description lineage retained into the behavior path
```

### F. Dispatch and first-consumer boundary

Only after endpoint, peer/credential, ancillary integrity, and descriptor lineage are reduced should the service dispatch path be treated as behavior proof.

What to capture:
- message opcode / command / method / framing associated with the ancillary object
- authorization gate and selected branch
- broker-to-worker or main-loop-to-handler delivery
- first function that uses the descriptor or credential to change state, create IO, spawn/attach, persist, proxy, or emit a response
- first downstream effect: file write/read, socket IO, terminal/session handoff, device handle use, process launch, state mutation, notification, or reply

Stop rule:

```text
dispatch branch plausible != first handler-owned consumer / effect proved
```

## 5. Fast observation plan

### Static pass

1. Find AF_UNIX creation and endpoint setup:
   - `socket(AF_UNIX, ...)`, `socketpair(...)`, `bind`, `listen`, `accept`, `connect`
2. Find credential and security options:
   - `getsockopt(SO_PEERCRED)`, `setsockopt(SO_PASSCRED)`, `SO_PASSSEC`, `SO_PEERSEC`
3. Find ancillary helpers:
   - `sendmsg`, `recvmsg`, `CMSG_FIRSTHDR`, `CMSG_NXTHDR`, `CMSG_DATA`, `SCM_RIGHTS`, `SCM_CREDENTIALS`
4. Trace retained objects:
   - fd arrays, connection objects, credential structs, authorization results, request structs, handler tables
5. Stop at one candidate consumer:
   - first branch that uses the passed fd or credential to change behavior

### Runtime pass

Start with one run and one logical request.

Useful captures:
- `strace -f -e trace=socket,connect,accept,sendmsg,recvmsg,getsockopt,setsockopt,fcntl,close,dup,execve`
- `/proc/<pid>/fd` and `/proc/<pid>/fdinfo` snapshots before and after the message
- lower-surface fd-pass tracing when available, but treat sender-side fd-pass as a reduction boundary, not final consumer proof
- application logs around auth, routing, broker dispatch, worker handoff, and descriptor use

Practical breakpoint / probe candidates:
- `sendmsg` and `recvmsg` wrappers
- first `CMSG_*` parser
- `SCM_RIGHTS` branch
- `SCM_CREDENTIALS` / `SO_PEERCRED` branch
- authorization decision
- table insertion / descriptor retention
- first read/write/poll/ioctl/mmap/use of the received fd
- first handler-owned side effect

## 6. Compare-run tactics

Use a small negative pair to avoid overreading static visibility:

- same endpoint, different peer uid/gid/pid
- same endpoint, missing `SO_PASSCRED`
- same payload bytes, no ancillary fd
- same `sendmsg(...)` call, receiver control buffer too small or `MSG_CTRUNC` set
- same descriptor pass, fd closed before handler use
- same descriptor pass, receiver execs with/without close-on-exec
- same broker-visible request, different downstream worker/handler selected

Ask which rung changes first:

```text
endpoint -> peer/cred -> ancillary-intact -> fd-lineage -> dispatched -> consumed
```

If the first mismatch is earlier than the supposed consumer, do not narrate it as handler behavior yet.

## 7. Handoff rules

Hand off to:
- D-Bus workflow when bus activation, name-owner, object/interface/member, or generated binding dispatch is the dominant liar
- protocol ingress / parser-to-state notes when the socket and peer are proved and the remaining problem is message grammar or state-machine consequence
- service-dispatcher / worker-owned-consumer note when the ancillary object is accepted but the worker handoff is still unclear
- callback/event-loop consumer note when the descriptor is retained but behavior waits behind queue, main-loop, epoll, reactor, or callback dispatch
- runtime-evidence / reverse-causality notes when one effect is visible and the question becomes which earlier write, fd, or credential branch caused it

## 8. Minimal evidence packet

For handoff or reporting, preserve:
- endpoint kind and namespace
- peer identity and credential API semantics
- `recvmsg(...)` control-data evidence, including truncation flags
- sender-side and receiver-side descriptor lineage
- selected command / request / opcode / method associated with the ancillary data
- authorization branch and handler dispatch evidence
- first consumer and one downstream effect

A good final claim has this shape:

```text
In run R, peer P connected to endpoint E.
The service sampled credential C using API S at boundary T.
Message M delivered ancillary object A intact (`SCM_RIGHTS` / `SCM_CREDENTIALS` / label L), without truncation.
Receiver descriptor F referred to object O and was retained in structure X.
Dispatcher branch B selected handler H.
H first used O/C at site U to produce effect Y.
```

That is the point where “Unix socket IPC happened” becomes a useful reverse-engineering proof.
