# Source Notes — Unix-Domain Socket FD / Credential Passing to First Consumer

Date: 2026-05-02 04:50 Asia/Shanghai
Branch: native desktop/server practical workflows
Search artifact: `sources/native/2026-05-02-0450-unix-domain-socket-fd-credential-search-layer.txt`

## Scope

These notes support a workflow page for Linux / Unix native service reversing where a local IPC boundary uses AF_UNIX sockets, ancillary data, credential checks, or file-descriptor passing.

The practical question is not “does this process use a Unix socket?” It is:

```text
which connected peer, credential object, received descriptor, dispatch record, and handler-owned consumer actually owns the later behavior?
```

## Source-backed facts worth preserving

### AF_UNIX is local IPC, not a complete service contract

`unix(7)` frames AF_UNIX / AF_LOCAL as local interprocess communication with pathname, unnamed, and Linux abstract namespace sockets. Linux pathname sockets have filesystem permission behavior, while abstract sockets are independent of filesystem pathnames and their socket permissions have no meaning.

Operator implication:
- a socket path or abstract name is only an ingress locator
- for pathname sockets, directory/socket permissions can matter but are not portable enough to serve as the whole security proof
- for abstract sockets, filesystem ownership/mode is the wrong proof object

### Credentials have multiple semantics

`unix(7)` distinguishes:
- `SO_PEERCRED`: read-only peer credentials for connected AF_UNIX stream sockets and socket pairs; returned credentials are those in effect at `connect(2)`, `listen(2)`, or `socketpair(2)` time
- `SO_PASSCRED` / `SCM_CREDENTIALS`: per-message ancillary credentials; to receive `struct ucred`, `SO_PASSCRED` must be enabled; kernel checks specified credentials, with privilege exceptions
- `SO_PASSSEC` / `SCM_SECURITY` and `SO_PEERSEC`: SELinux/security-label surfaces when enabled/supported

Operator implication:
- `SO_PEERCRED` proves a connection-time peer property, not necessarily the sender for every later delegated object
- `SCM_CREDENTIALS` proves a per-message credential object under kernel checks, but it is still weaker than proving authorization branch and handler-owned consumer
- security-label evidence can route authorization, but a label string is not the final behavior proof

### FD passing duplicates an open-file-description reference

`unix(7)` describes `SCM_RIGHTS` as sending/receiving a set of open file descriptors, but clarifies that what is semantically passed is a reference to an open file description; in the receiver, a different descriptor number is likely used. It is equivalent to duplicating a file descriptor into another process's descriptor table.

Operator implication:
- the integer observed in sender and receiver can differ
- the object identity is the open file description / target object, not the raw fd number
- post-receive flags, `FD_CLOEXEC`, file offset, socket peer, pipe endpoint, memfd/seal state, device node, namespace, and lifecycle can matter before claiming consequence ownership

### Ancillary-data receipt can truncate or discard the real proof object

`unix(7)` notes that if the ancillary receive buffer is too small or absent, file descriptor ancillary data may be truncated or discarded and excess fds are automatically closed in the receiving process. `MSG_CTRUNC` is set when ancillary data is truncated/discarded. Excess fds may also be closed when `RLIMIT_NOFILE` would be exceeded. `SCM_MAX_FD` limits descriptor arrays.

Operator implication:
- a `recvmsg(...)` return is not enough; inspect `msg_control`, `cmsghdr`, `cmsg_type`, count, `MSG_CTRUNC`, and close-on-exec handling
- a missed ancillary buffer can make the payload bytes visible while the behavior-bearing descriptor never survived
- `MSG_CMSG_CLOEXEC` from `recvmsg(2)` is relevant when descriptor lifetime across exec changes the later effect

### Ancillary data is attached to message-delivery boundaries

`unix(7)` says at least one byte of real data should be sent with ancillary data; Linux requires this for stream sockets. It also describes ancillary data on stream sockets as forming a barrier for received data.

Operator implication:
- payload framing and control-message association must be preserved before mapping a descriptor to a command
- a stream read that ignores `recvmsg(...)` control data can make the analyst see payload bytes but miss the capability transfer

### Runtime observation has a lower-surface option

Inspektor Gadget’s `fdpass` gadget documents tracing file descriptor passing via Unix sockets / `SCM_RIGHTS` and gives examples in D-Bus, `runc`, and the Linux Bluetooth stack. It currently shows sender-side events.

Operator implication:
- lower-surface tracing can answer “which process sent which fd over which socket” better than static xrefs alone
- sender-side proof is still weaker than receiver-side `recvmsg(...)`, dispatch, and handler-consumer proof
- common real-world families include D-Bus brokered fd passing, container runtime terminal/socket handoff, and Bluetooth/socket delegation

## Durable workflow split

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

## Practical observation surfaces

Static / code:
- `socket(AF_UNIX, ...)`, `socketpair(...)`, `bind`, `listen`, `accept`, `connect`
- `sendmsg`, `recvmsg`, `CMSG_FIRSTHDR`, `CMSG_NXTHDR`, `SCM_RIGHTS`, `SCM_CREDENTIALS`, `SO_PASSCRED`, `SO_PEERCRED`, `SO_PASSSEC`, `SO_PEERSEC`
- binding/adaptor code that routes messages after credential/fd extraction

Runtime / OS:
- `strace -e trace=socket,connect,accept,sendmsg,recvmsg,getsockopt,setsockopt`
- eBPF / tracepoint / gadget observation of fd passing, with caution around sender-only visibility
- `/proc/<pid>/fd`, `/proc/<pid>/fdinfo`, socket inode correlation, peer credential capture, namespace/cgroup/container context
- application logs around authorization, broker dispatch, connection ownership, and descriptor handoff

## Sources consulted

- Search artifact: `sources/native/2026-05-02-0450-unix-domain-socket-fd-credential-search-layer.txt`
- Linux man-pages, `unix(7)` — https://man7.org/linux/man-pages/man7/unix.7.html
- Linux man-pages, `recv(2)` / `recvmsg(2)` — https://man7.org/linux/man-pages/man2/recvmsg.2.html
- Linux man-pages, `send(2)` / `sendmsg(2)` — https://man7.org/linux/man-pages/man2/sendmsg.2.html
- TLPI supplementary code, `scm_cred_recv.c` — https://man7.org/tlpi/code/online/dist/sockets/scm_cred_recv.c.html
- Inspektor Gadget, `fdpass` gadget — https://www.inspektor-gadget.io/docs/latest/gadgets/fdpass/
