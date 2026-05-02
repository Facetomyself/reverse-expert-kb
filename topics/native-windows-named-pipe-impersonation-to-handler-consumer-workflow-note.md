# Native Windows Named Pipe Impersonation to Handler Consumer Workflow Note

Topic class: workflow note
Ontology layers: workflow/sensemaking, runtime-evidence bridge, native desktop/server practical branch
Maturity: emerging
Related pages:
- topics/native-binary-reversing-baseline.md
- topics/native-practical-subtree-guide.md
- topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md
- topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/native-unix-domain-socket-fd-credential-first-consumer-workflow-note.md
- topics/malware-service-servicemain-consumer-proof-workflow-note.md
- topics/runtime-behavior-recovery.md

## 1. What this workflow note is for

Use this note when a Windows native target exposes a named-pipe service, helper, broker, updater, agent, local IPC endpoint, or malware/service-abuse path and the visible pipe name or `ImpersonateNamedPipeClient(...)` call is not enough to explain the behavior.

Typical surfaces:
- `\\.\pipe\...` names in strings or telemetry
- `CreateNamedPipe*`, `ConnectNamedPipe`, `ReadFile`, `WriteFile`, `TransactNamedPipe`, `CallNamedPipe`
- overlapped named-pipe server loops with per-instance state
- `ImpersonateNamedPipeClient`, `RevertToSelf`, `OpenThreadToken`, `DuplicateTokenEx`
- client identity checks such as `GetNamedPipeClientProcessId`, image checks, SID checks, session checks, or allowlists
- services that read a request, impersonate the client, access a protected resource, spawn/launch, update state, or dispatch to a worker

This is not an exploitation recipe. It is a stop-rule note for proving which pipe instance, client/request, impersonation lifetime, and handler-owned consumer actually own the later effect.

The goal is to move from:

```text
pipe name / pipe API / impersonation call visible
```

to:

```text
one proved chain from a current pipe instance and client request
through identity / impersonation-level truth and successful impersonation lifetime
into one handler operation or downstream effect
```

## 2. When to use this note

Use this note when most of the following are true:
- the target is a Windows service, broker, updater, desktop helper, agent, malware component, or privileged local daemon
- a named pipe is the most concrete ingress, trust-boundary, or IPC surface
- the analyst can see pipe creation/connect/read/write or impersonation APIs, but the behavior owner is still unclear
- the interesting question is not merely “what is the pipe name?” but “which client/request/token/handler caused the effect?”
- identity checks, impersonation level, or revert timing can change the meaning of later resource access
- overlapped I/O or multi-instance pipe loops make one static callsite too broad to trust

Do **not** use this as the primary guide when:
- the first trustworthy native semantic anchor is still missing; start with semantic-anchor stabilization
- the route is already clearly service-control-manager dispatch rather than pipe IPC; start with service-dispatcher / worker-owned consumer proof
- the remaining ambiguity is generic completion-port / thread-pool delivery after the pipe request is already reduced; hand off to the completion/async pages
- the case is Unix-domain socket / fd / credential passing; use the Unix-domain socket workflow note instead

## 3. Core claim

In Windows named-pipe work, pipe visibility and impersonation-call visibility are usually only reduction evidence. The behavior-bearing truth often lives several proof objects later:

```text
pipe name / instance visible
  != current client connection accepted
  != correct request bytes read on this pipe instance
  != client identity / token / impersonation level frozen
  != ImpersonateNamedPipeClient succeeded for the last read message
  != operation executed while impersonation lifetime was active
  != handler-owned state change, resource access, launch, reply, or downstream effect proved
```

Compact branch memory:

```text
pipe != connected != read != impersonated != in-lifetime operation != consumed/effected
```

Common false stops:
- a `\\.\pipe\...` string exists
- `CreateNamedPipe*` succeeds once
- a client connects, but not necessarily the client that owns the interesting request
- a `ReadFile` / `GetOverlappedResult` path exists, but the completed request is not tied to the handler
- `GetNamedPipeClientProcessId` returns a PID, and the PID is treated as strong identity
- `ImpersonateNamedPipeClient` appears in the binary, but return value and thread-token lifetime are not proved
- a token is opened or duplicated, but the later operation may occur after `RevertToSelf` or in a different worker thread

## 4. Boundaries to mark explicitly

### A. Pipe endpoint and instance boundary

First prove which pipe object exists and which instance handles the request.

Capture:
- exact pipe name and namespace assumptions
- `CreateNamedPipe*` open mode, pipe mode, remote-client flags, first-instance flag, and security attributes
- DACL/default-security behavior, especially whether Everyone/anonymous/default creator rights are being overread
- number of instances and whether a reused instance handled the current request
- whether the pipe is message-mode or byte-mode

Stop rule:

```text
pipe name visible != current pipe instance accepted this client/request
```

### B. Connection and request-read boundary

For message ownership, the last read request matters. Microsoft documents `ImpersonateNamedPipeClient` as impersonating the security context of the **last message read from the pipe**.

Capture:
- `ConnectNamedPipe` completion and accepted client
- read operation and byte count
- message boundary or framing for message-mode pipes
- overlapped `OVERLAPPED` object, event, `GetOverlappedResult`, and per-instance state
- whether a zero-byte, failed, partial, stale, or previous read is being mistaken for the behavior-bearing request

Stop rule:

```text
connection accepted != this request was read and owns the next impersonation
```

### C. Client identity and impersonation-level boundary

Identity evidence is not all equally strong.

Keep separate:
- PID evidence from `GetNamedPipeClientProcessId`
- process image/signature/session checks
- SID/group/token evidence
- client-controlled SQOS / impersonation-level settings
- server-side privilege posture such as whether the service can impersonate as expected

Stop rule:

```text
client PID / image / SID observed != usable impersonation context for this operation
```

Treat PID-only checks as weak. They may reduce the candidate set, but they are not the same as a durable token/SID/level proof, and historical research shows PID-based pipe trust can be a fragile security assumption.

### D. Impersonation success and lifetime boundary

`ImpersonateNamedPipeClient(...)` must be treated as a branching runtime fact, not a static label.

Capture:
- return value and `GetLastError` on failure
- thread that called it
- thread token after success if available
- whether code checks failure before privileged work
- `RevertToSelf` timing
- whether the operation moves to another worker thread or queued callback where the token may not follow

Stop rule:

```text
ImpersonateNamedPipeClient callsite exists != later operation ran under that client token
```

A particularly dangerous overread is:

```text
impersonation failed -> service still performs work under privileged service token
```

That is not client-owned behavior. It is a different, often more security-relevant, mechanism.

### E. Operation / handler consumer boundary

Only after request, identity, and impersonation lifetime are reduced should the service operation be treated as behavior proof.

Capture one first consumer:
- file/registry/object-manager access attempted while impersonated
- ACL decision or access denied/success path under the client token
- process/thread/job/session launch semantics if token duplication is involved
- command/method/opcode dispatch and selected handler
- state mutation, persistence update, device/service call, network/proxy action, or reply
- whether the handler reverts, queues work, duplicates a token, or hands off to a different component before the effect

Stop rule:

```text
handler branch plausible != first in-lifetime operation or downstream effect proved
```

## 5. Fast observation plan

### Static pass

1. Find pipe endpoint creation and connection:
   - `CreateNamedPipe*`, `ConnectNamedPipe`, `DisconnectNamedPipe`, `CreateFile*`, `CallNamedPipe`, `TransactNamedPipe`
2. Classify pipe/server mode:
   - message vs byte mode, overlapped vs synchronous, one instance vs multiple reused instances
3. Find read/framing paths:
   - `ReadFile`, `GetOverlappedResult`, request structs, opcodes, command strings, handler tables
4. Find identity and authorization checks:
   - `GetNamedPipeClientProcessId`, token/SID helpers, image checks, session checks, ACL helper calls
5. Find impersonation and token lifetime:
   - `ImpersonateNamedPipeClient`, `OpenThreadToken`, `DuplicateTokenEx`, `RevertToSelf`, process-creation or resource-access calls
6. Stop at one candidate consumer:
   - the first handler-owned operation whose behavior changes if the client/request/token changes

### Runtime pass

Start with one client request and one pipe instance.

Useful breakpoints / event surfaces:
- `CreateNamedPipeW/A`
- `ConnectNamedPipe`
- `ReadFile` / `GetOverlappedResult` for the relevant pipe handle
- `GetNamedPipeClientProcessId` if used
- `ImpersonateNamedPipeClient`
- `OpenThreadToken`, `DuplicateTokenEx`, `RevertToSelf`
- first resource operation after impersonation: file, registry, service, process, object-manager, RPC, device, or reply-builder calls

At each breakpoint, record:
- pipe handle / instance object
- client PID/process/session/SID where available
- request bytes and handler selection
- current thread ID and token posture
- whether the next operation is still in the impersonation lifetime

## 6. Minimal proof artifact

A good handoff artifact is a compact table:

| Rung | Evidence | Status |
| --- | --- | --- |
| Pipe endpoint / instance | name, handle, mode, DACL, instance | proved / weak / unknown |
| Client connection | PID/process/session/token hints | proved / weak / unknown |
| Request read | bytes, opcode, overlapped completion | proved / weak / unknown |
| Identity / level | PID/SID/token/SQOS/level | proved / weak / unknown |
| Impersonation lifetime | success, thread, token, revert point | proved / weak / unknown |
| Handler consumer | first operation/effect while valid | proved / weak / unknown |

The first trustworthy claim should be no broader than the weakest proved rung.

## 7. Source-backed cautions

- Microsoft documents impersonation as the server thread assuming the access token of the connected client, bounded by impersonation level, and returning to self afterward.
- Microsoft documents `ImpersonateNamedPipeClient` as using the security context of the last message read from the pipe and warns that failures must be checked to avoid privileged-server-context work.
- Microsoft named-pipe security documentation makes pipe DACLs and access checks part of the endpoint proof, not decoration.
- Microsoft overlapped named-pipe examples show why connect/read/write completion and pipe-instance state must be separated from handler truth.
- Project Zero's client-PID spoofing analysis is a reminder that `GetNamedPipeClientProcessId` is weak as a standalone trust proof; use it as a reduction clue, not final identity.

## 8. Handoff rules

Hand off to:
- `native-service-dispatcher-to-worker-owned-consumer-workflow-note.md` when the pipe request primarily selects a service worker or control path and impersonation is no longer the lie
- `native-completion-port-and-thread-pool-first-consumer-workflow-note.md` when the request is proved but completion/thread-pool delivery hides the consumer
- `malware-service-servicemain-consumer-proof-workflow-note.md` or malware persistence/comms pages when the pipe is part of a malware service-abuse chain
- `runtime-evidence-package-and-handoff-workflow-note.md` when preparing a shareable proof package

## 9. Practical next-step heuristic

If stuck, do not widen immediately into all pipe clients or all handlers.

Ask the smallest discriminating question:

```text
Can I prove one request was read by one pipe instance,
then prove the exact thread/token/lifetime under which the first consequence-bearing operation ran?
```

If not, the next cheapest check is usually one breakpoint at `ImpersonateNamedPipeClient` plus one immediately downstream resource or handler breakpoint, with pipe handle, last-read request, thread ID, token posture, and `RevertToSelf` timing recorded together.
