# Native Windows ALPC Port/Message to Handler-Consumer Workflow Note

Topic class: workflow note
Ontology layers: native IPC, Windows service/helper boundary, async/reply ownership, handler-consumer proof
Maturity: draft-practical
Related pages:
- topics/native-practical-subtree-guide.md
- topics/native-windows-named-pipe-impersonation-to-handler-consumer-workflow-note.md
- topics/native-com-activation-to-method-consumer-workflow-note.md
- topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md
- topics/native-etw-provider-session-consumer-workflow-note.md
- topics/runtime-behavior-recovery.md

## Use this note when
Use this note when a Windows native target already plausibly depends on **ALPC / local RPC-style port messaging**, but the investigation still lacks the first trustworthy handler-consumer boundary.

Typical cases:
- WinObj, ETW, handle inspection, or strings reveal a named ALPC port under `\\RPC Control`, but no accepted request path is proved yet.
- Static code shows `NtAlpcCreatePort`, `NtAlpcConnectPort`, `NtAlpcAcceptConnectPort`, `NtAlpcSendWaitReceivePort`, `NtRequestWaitReplyPort`, `NtReplyWaitReceivePort`, or adjacent `rpcrt4` / local-service IPC wrappers.
- A client send or server receive is visible, but the semantic method/opcode, message attributes, transferred handle/view, security context, or dispatch branch is still unclear.
- The target performs identity-sensitive work where ALPC client identity, QoS, impersonation, or per-port context may decide the later effect.
- A reply/wait path is visible, but the analyst has not proved the reply belongs to the current live request or that the caller consumed it.

Do not start here when:
- the evidence is clearly ordinary named pipe, COM activation, D-Bus, XPC, or socket IPC rather than ALPC-shaped messaging.
- one ALPC request chain is already proved and the remaining question is a downstream parser, protocol state, service worker, or malware behavior.
- the only evidence is a broad ETW ALPC event count with no target-local port/message/handler correlation; first reduce the trace into a representative port/message pair.

## Core stop rule
The compact seam for this note is:

```text
port visible != connection accepted != message received != attributes/context decoded != handler dispatched != reply/impersonation/effect owned
```

A narrower reply/callback seam is:

```text
sent != waited != received reply != matched to current request != caller consumed effect
```

A narrower identity seam is:

```text
client identity visible != QoS permits/selected != impersonation succeeded != in-lifetime handler operation != effect owned
```

The point is not to memorize ALPC internals. The point is to stop treating a named local port, one send event, or one receive syscall as proof that a particular handler, security context, transferred object, reply, or later behavior owns the case.

## Proof ladder

### Step 1: Freeze the port role, not just the name
Start by separating:
- named connection port / object path
- server process that created or owns the port
- client process that attempted the connection
- accepted/rejected connection request
- per-conversation communication port / port context
- later message loop or worker path

Evidence to prefer:
- `NtAlpcCreatePort` / `NtCreatePort` or wrapper site with object attributes and security descriptor.
- handle/object inspection tying port handles to the server and client processes.
- ETW ALPC send/receive/wait events correlated to process/thread and port/message identity.
- `NtAlpcConnectPort` / `NtAlpcAcceptConnectPort` / `NtCompleteConnectPort` return paths.

Do not stop at:
- one `\\RPC Control\\...` name.
- a service string that looks like a port.
- a handle table entry without connection/message proof.

### Step 2: Preserve message identity separately from message semantics
For each representative request, record:
- message type: connection request, request, reply, datagram, lost reply, close, exception, etc.
- data length / total length / data-info offset
- message id and callback id where present
- client id / sender thread if available
- receive syscall and receive site
- send flags / wait mode / timeout posture
- status code or exception/lost-reply path

Then decode semantics as a second step:
- opcode, method number, selector, or command field
- message version / size check / flags
- table lookup, switch arm, virtual/interface dispatch, or RPC stub path
- first target-local object or state field selected by the decoded request

Do not flatten:

```text
PORT_MESSAGE visible == method decoded == handler selected
```

A message envelope can be real while the semantic owner is still hidden in a separate buffer, attribute, view, or dispatch table.

### Step 3: Treat attributes, sections, handles, and views as first-class proof objects
ALPC messages may carry or reference more than flat inline bytes. In practical samples and Windows internals work, message attributes, security attributes, handle attributes, and view/section mappings can be the behavior-bearing part of the request.

For each attribute-bearing case, preserve:
- which attributes are valid / requested / received
- section or view creation and mapping lineage
- transferred handle object type, access rights, and target process lifetime
- security attribute / token / client identity evidence
- whether handler code actually reads the attribute or only receives it
- whether mapped data or transferred object is consumed before reply/effect

Do not stop at:
- `ValidAttributes` is nonzero.
- a section/view exists.
- a handle attribute is present.
- `MessageId` matches a reply.

The first truthful consumer is often the code path that dereferences the mapped view, duplicates/uses the transferred handle, or branches on the security/client attribute.

### Step 4: Split dispatch truth from handler-owned effect
Once a message is received, prove the handoff into one concrete handler:
- which loop or worker thread received it
- whether dispatch is inline, queued, threadpool-backed, or service-worker-backed
- selector/opcode-to-handler mapping
- handler object lifetime and per-client context
- first state mutation, object operation, privileged operation, file/registry/process/network effect, or reply object that belongs to that handler

Useful breakpoints / hooks:
- syscall boundary: `NtAlpcSendWaitReceivePort`, `NtRequestWaitReplyPort`, `NtReplyWaitReceivePort`, `NtAlpcAcceptConnectPort`.
- decode boundary: first read of message data or mapped view after receive.
- dispatch boundary: switch/table/interface call selected by decoded opcode.
- consumer boundary: first state reducer or privileged operation in the selected handler.
- reply boundary: reply construction and send, not just receive-side success.

Do not overread:
- receive success as handler proof.
- handler entry as later effect proof.
- a reply send as caller consumption proof.

### Step 5: Prove identity and impersonation only if the case needs it
ALPC is common in local service/helper paths where identity and impersonation can be the real policy decision.

Keep separate:
- client PID/TID / sender identity visible in message or context
- security QoS requested / accepted
- server policy check on SID/token/attributes
- successful impersonation call or framework equivalent
- operation performed while impersonating
- revert / lifetime end
- later effect ownership

This mirrors named-pipe impersonation discipline, but do not blindly import pipe assumptions. ALPC can add port context, security/message attributes, views, and reply/wait semantics that make the truthful identity consumer a different object than the first receive site.

### Step 6: Keep reply/wait correlation honest
In request/reply-shaped cases, preserve:
- send request boundary
- wait-for-reply or wait-for-new-message boundary
- reply message id / callback id / status relation
- lost reply / timeout / port closed / client died states
- caller-side decode of reply payload or attributes
- first caller-side state/effect after reply consumption

This matters when an analyst sees both a send and a later reply but has not proved they belong to the same live request or that the reply was consumed by the caller branch that matters.

## Minimal evidence row
Use a row like this for ALPC-shaped cases:

```text
port path | server pid/module | connection create/listen | client connect | accept/reject | communication port/context | message type/id/callback id | sender pid/tid | data/attribute/view/handle evidence | receive site | dispatch branch/opcode | identity/impersonation state | reply/wait relation | first handler state/effect | lifetime note
```

If that row cannot be filled, the missing column is usually the next best breakpoint or trace target.

## Common false claims

### False claim: `\\RPC Control\\Name` proves behavior ownership
Better claim:
- the port name is an entry surface. Prove server ownership, live connection, accepted request, decoded message, handler dispatch, and first effect separately.

### False claim: ETW send/receive events prove the handler ran
Better claim:
- ALPC ETW send/receive/wait events are boundary evidence. They still need target-local correlation to receive site, message identity, payload/attribute decode, dispatch, and consumer.

### False claim: receive syscall success proves semantic command handling
Better claim:
- receive success proves delivery to a port/message loop. It does not prove opcode decode, handler selection, security acceptance, or effect ownership.

### False claim: client PID/TID proves impersonated operation
Better claim:
- visible client identity is not the same as successful impersonation or an operation performed during impersonation lifetime.

### False claim: reply visible proves caller-side effect
Better claim:
- reply visibility is weaker than current-request match, reply decode, caller branch selection, and caller-side state/effect consumption.

## Handoff rules
Route out of this note when:
- the first ALPC handler is proved and the remaining work is a service-worker chain — use native service/worker or callback/event-loop notes.
- the message body is a protocol/RPC contract and replay becomes the goal — use protocol service-contract / Windows RPC / pending-request notes.
- the handler launches malware persistence/comms/stage behavior — use the appropriate malware staged execution, persistence, or request-builder note.
- the problem is now detection/handoff rather than mechanism proof — use runtime evidence package or malware reporting/detection handoff notes.

Stay on this note while the missing proof is still one of:
- connection accepted
- message delivered to target-local receive site
- attribute/view/handle decoded
- handler dispatch selected
- identity/impersonation accepted
- reply matched and consumed
- first handler-owned effect proved

## Source-backed notes
See:
- `sources/native/2026-05-31-alpc-port-message-consumer-notes.md`
