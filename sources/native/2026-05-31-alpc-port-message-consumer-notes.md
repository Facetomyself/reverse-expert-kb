# Windows ALPC Port/Message to Handler Consumer Source Notes — 2026-05-31

## Scope
Source-backed notes for a native Windows ALPC workflow note. The operator problem is not generic IPC taxonomy. It is preventing a reverse case from overreading an ALPC port name, one send event, or one receive syscall as proof that a specific server handler, security context, transferred handle/view, reply, or later effect actually owns the behavior.

## Sources consulted
- Search artifact: `sources/native/2026-05-31-0450-alpc-port-message-consumer-search-layer.json`
- Microsoft Learn, `ALPC` ETW class: https://learn.microsoft.com/en-us/windows/win32/etw/alpc
- csandker.io, `Offensive Windows IPC Internals 3: ALPC`: https://csandker.io/2022/05/24/Offensive-Windows-IPC-3-ALPC.html
- System Informer / phnt `ntlpcapi.h`: https://raw.githubusercontent.com/winsiderss/phnt/master/ntlpcapi.h
- csandker ALPC sample server: https://raw.githubusercontent.com/csandker/InterProcessCommunication-Samples/master/ALPC/CPP-ALPC-Basic-Client-Server/CPP-ALPC-Basic-Server/CPP-ALPC-Basic-Server.cpp
- csandker ALPC sample client: https://raw.githubusercontent.com/csandker/InterProcessCommunication-Samples/master/ALPC/CPP-ALPC-Basic-Client-Server/CPP-ALPC-Basic-Client/CPP-ALPC-Basic-Client.cpp

## External-source facts worth preserving

### ALPC evidence is visible through ETW, but ETW events are not handler proof
Microsoft documents an `ALPC` ETW class for advanced local procedure call events. To enable ALPC events, an NT Kernel Logger session uses `EVENT_TRACE_FLAG_ALPC`; consumers can set a callback for `ALPCGuid`. Event types include send message, receive message, wait for reply, wait for new message, and stop waiting.

Practical reading:
- ETW ALPC send/receive/wait events are good boundary evidence.
- They are not automatically payload-decode, handler-dispatch, impersonation, reply, or effect evidence.
- They should be correlated with port handle/name, `PORT_MESSAGE` metadata, process/thread, message id/callback id, receive-site, and downstream handler state before claiming behavior ownership.

### ALPC has a connection-port / communication-port split
The csandker ALPC writeup describes the common ALPC shape as a server-created connection port plus communication ports used for the conversation; it emphasizes that the port visible under `\\RPC Control` is typically the connection surface, not the whole conversation.

Practical reading:
- A named port object proves a potential entry surface, not an accepted client, a live request, or a handler-owned operation.
- Reverse cases should split `NtAlpcCreatePort` / named connection-port discovery from `NtAlpcConnectPort`, `NtAlpcAcceptConnectPort`, and the eventual message receive/dispatch loop.

### `PORT_MESSAGE` gives message identity, but not semantic ownership by itself
The phnt header exposes `PORT_MESSAGE` fields including data length, total length, type, data-info offset, client id, message id, and callback id / client-view-size union, plus request/reply/datagram/connection-request constants. It also exposes classic LPC and ALPC APIs such as connect/listen/accept/complete, request/reply, reply-wait-receive, impersonate-client, read/write-request-data, and ALPC-specific calls and attributes.

Practical reading:
- `MessageId`, `CallbackId`, `ClientId`, message type, data length, and receive-site are useful correlation fields.
- They do not by themselves prove the semantic method/opcode, security posture, transferred object lineage, or downstream consumer.
- Callback/reply-style correlation should be treated like request ownership: `message id/callback id visible != reply matched to current live request != caller consumed reply`.

### Message attributes and sections/handles/views can move the real proof object out of the flat payload
The sample server and client allocate ALPC message attributes, use security, view, and handle attributes, create port sections, and send/receive messages with `NtAlpcSendWaitReceivePort(...)`. The server accepts a connection, stores a port context derived from client PID/TID, receives data, optionally impersonates the client, and replies using the received message id.

Practical reading:
- The visible `PORT_MESSAGE` bytes may be only the control envelope.
- The behavior-bearing object may be a view/section mapping, transferred handle, security attribute, or context associated with the accepted port.
- Preserve separate evidence for attribute validity, view/handle transfer, mapped-buffer contents, handle object type/rights, and first handler consumer.

### Impersonation and client identity need their own proof boundary
The sample server sets security QoS fields and optionally calls an impersonation helper after receiving a message; phnt exposes `NtImpersonateClientOfPort(...)`. The code also records client PID/TID from the received connection request into a port context.

Practical reading:
- Client PID/TID in a message or context is weaker than successful impersonation or an in-impersonation-lifetime operation.
- In ALPC cases, preserve `client identity visible != QoS permits/selected != impersonation succeeded != in-lifetime handler operation != effect owned`.
- This parallels the KB's named-pipe impersonation seam but ALPC adds message attributes, views, connection/communication port split, and reply/wait correlation.

## Workflow implications
A good ALPC evidence row should include:

```text
port name / object path | server process | connection create/listen | client connect | accept/reject | communication port/context | message type/id/callback id | sender pid/tid | data/attribute/view/handle evidence | receive site | dispatch branch/opcode | impersonation/security state | reply/wait relation | first handler state/effect | lifetime note
```

Minimal stop rule to promote into the KB:

```text
port visible != connection accepted != message received != attributes/context decoded != handler dispatched != reply/impersonation/effect owned
```

A narrower reply/callback rule is also useful:

```text
sent != waited != received reply != matched to current request != caller consumed effect
```
