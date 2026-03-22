# Pending-request correlation and async reply notes

Date: 2026-03-22
Scope: practical notes for protocol / RPC / firmware-adjacent cases where a structurally valid reply, completion, or response-like message is still ignored until it matches one local pending-request owner, async handle, callback queue, or completion slot.

## Why this source batch matters
The protocol branch already covered replay gates broadly, but it still lacked a narrow practical note for a recurring operator failure mode:
- the analyst can already build or observe a structurally plausible response or completion
- the parser may even accept it
- yet nothing advances because one local pending-request record, async handle, callback queue, or correlation-owned slot is the real consumer gate

This batch does not prove one universal implementation pattern.
It is useful because several source families converge on the same workflow lesson:
- do not stop at packet correctness
- localize the owner that matches response-like traffic to one live outstanding request state

## Retained sources

### 1. Microsoft Learn - Receiving the Asynchronous Reply
URL: https://learn.microsoft.com/en-us/windows/win32/rpc/receiving-the-asynchronous-reply

Retained points:
- async RPC reply consumption is not just “reply arrived”; the client still calls `RpcAsyncCompleteCall` with the asynchronous handle to receive the reply
- calling completion before the server has sent the reply returns `RPC_S_ASYNC_CALL_PENDING`
- this is strong evidence that one local handle-owned completion object can be the decisive response-consumption gate rather than reply bytes alone

Operator value:
- good concrete example of a response-like artifact being insufficient until the right pending async state object owns it
- useful for framing cases where a captured reply exists but the analyst still has not found the local consumer that turns it into valid completion

### 2. Microsoft Learn - `RPC_ASYNC_STATE`
URL: https://learn.microsoft.com/en-us/windows/win32/api/rpcasync/ns-rpcasync-rpc_async_state

Retained points:
- `RPC_ASYNC_STATE` explicitly holds the state of an asynchronous remote procedure call
- it includes runtime-owned and user-associated state (`RuntimeInfo`, `UserInfo`, notification type, event/callback/IOC metadata)
- notification and completion are attached to one async state object, not to reply bytes in the abstract

Operator value:
- useful anchor for the idea that one pending request can have a durable state carrier with runtime-owned fields and one chosen notification path
- reinforces the workflow move of watching the live request-state holder, not only the response serializer or transport

### 3. Trail of Bits - RPC Investigator
URL: https://blog.trailofbits.com/2023/01/17/rpc-investigator-microsoft-windows-remote-procedure-call/

Retained points:
- practical RPC work benefits from visibility into active interfaces, procedures, and ETW-observed in-flight RPC activity
- ETW visibility plus server/interface metadata helps correlate active calls rather than treating procedure signatures as enough
- the tool is useful precisely because active RPC operations and interface context must be tied together

Operator value:
- supports a workflow centered on finding one active call owner / in-flight operation rather than only decompiling static stubs
- especially relevant when the next bottleneck is “which outstanding request does this completion belong to?”

### 4. csandker - Offensive Windows IPC Internals 3: ALPC
URL: https://csandker.io/2022/05/24/Offensive-Windows-IPC-3-ALPC.html

Retained points:
- RPC commonly rides over ALPC for local transport
- ALPC message flow is asynchronous and port/object based, with connection and communication-port state, not just free-floating request/reply bytes
- one communication step can combine send/wait/receive style behavior, and the surrounding port/message object structure matters operationally

Operator value:
- supports the broader lesson that transport/runtime ownership can matter more than visible reply bytes
- useful when a reply-like object is real but still not consumed because the owning communication object / outstanding request state is wrong

### 5. RabbitMQ tutorial - RPC / correlationId
URL: https://www.rabbitmq.com/tutorials/tutorial-six-java

Retained points:
- client creates a callback queue and sends each request with `replyTo` + unique `correlationId`
- when a response arrives on the callback queue, the client checks `correlationId` and only returns the response if it matches the outstanding request
- this is a clean, explicit example of pending-request ownership being a first consumer gate

Operator value:
- generic but pedagogically strong model for response matching
- useful as a practical analogy for proprietary protocols: if a “correct” response is ignored, the missing proof may be one ownership / correlation match, not broad parser failure

### 6. Berkeley BitBlaze / Replayer framing
URL: https://people.eecs.berkeley.edu/~dawnsong/bitblaze/protocol.html

Retained points:
- application dialogue replay is a key downstream goal of protocol RE
- replay is not a one-shot extraction problem; protocol behavior often depends on interaction structure
- processing behavior reveals high-value protocol information

Operator value:
- broad support for treating response consumption / dialogue continuation as a central practical goal
- useful parent source for why this narrower workflow note belongs under protocol replay work rather than as an isolated messaging pattern

## Cross-source synthesis
A durable workflow lesson emerges:

```text
request method/shape already known
  -> response/completion bytes are visible or reconstructable
  -> replay still no-ops or gets ignored
  -> one local pending-request owner decides whether the response is consumed
  -> the true next task is to localize that owner and its matching fields/slot/handle
```

High-value owner patterns suggested by this batch:
- async handle / async-call state object
- callback queue + correlation ID matcher
- pending slot / request table entry
- completion port / event / callback registration tied to one request state
- transport-owned message object that must still be associated with one live outstanding operation

## What this batch does *not* justify
Do not overclaim from this source set.
It does **not** prove that every ignored reply is caused by correlation mismatch.
Other gates may still dominate:
- freshness / nonce
- auth / MAC
- wrong transport wrapper
- session phase
- output handoff never happened

The right claim is narrower:
- when request family and parser visibility are already decent, one recurring hidden gate is pending-request ownership
- this gate deserves its own practical workflow note because it is smaller and more operator-useful than another generic replay-gate discussion

## KB action justified by this batch
This batch is strong enough to support a concrete workflow page on:
- pending-request / correlation-owned response consumption
- especially for cases where structurally plausible response-like traffic still fails to advance behavior

Suggested placement:
- child note under the protocol replay / protocol-firmware practical subtree
- linked from the broader replay-precondition/state-gate note as a narrower handoff when the gating question has already collapsed to outstanding-request ownership
