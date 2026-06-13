# Native Windows Minifilter Callback to Policy Consumer Workflow Note

Topic class: workflow note
Ontology layers: native practical workflow, file-system filter driver evidence, kernel/user-mode policy handoff
Maturity: draft-practical
Related pages:
- topics/native-practical-subtree-guide.md
- topics/native-binary-reversing-baseline.md
- topics/native-etw-provider-session-consumer-workflow-note.md
- topics/native-windows-service-trigger-to-worker-consumer-workflow-note.md
- topics/malware-analysis-overlaps-and-analyst-goals.md
- sources/native/2026-06-14-windows-minifilter-callback-verdict-notes.md

## 1. When to use this note

Use this note when a Windows native target exposes file-system minifilter surfaces and the current risk is overreading filter-driver evidence.

Common entry signals:
- `FltRegisterFilter`, `FltStartFiltering`, `FltUnregisterFilter`, `FLT_REGISTRATION`, or operation-registration tables
- pre-operation / post-operation callbacks for `IRP_MJ_CREATE`, read, write, set-information, cleanup, close, or security-related file operations
- return statuses such as `FLT_PREOP_SUCCESS_NO_CALLBACK`, `FLT_PREOP_SUCCESS_WITH_CALLBACK`, `FLT_PREOP_PENDING`, or `FLT_PREOP_COMPLETE`
- `FltCompletePendedPreOperation`, deferred work items, cancel-safe callback-data queues, or scanner-style pended I/O
- `FltCreateCommunicationPort`, `FilterConnectCommunicationPort`, `FltSendMessage`, user-mode scanner / policy service receive-reply logic, or timeout fallbacks
- EDR, antivirus, DLP, ransomware-protection, backup, encryption, or file-monitor components where it is unclear whether a callback only observed I/O, pended it, asked user mode, blocked it, or allowed it

Do **not** use this note as a generic minifilter programming tutorial. The reverse-engineering question is narrower:

> Which boundary is the first truthful proof object: active filter registration, relevant operation selection, callback entry, verdict context construction, pended/user-mode decision, kernel-side completion/resume, or final file-system/user-visible effect?

## 2. Core split

Keep this ladder visible:

```text
filter registered / started
  != relevant operation selected for this instance and volume
  != pre-operation callback entered for the file operation under analysis
  != verdict context or scan request constructed
  != I/O pended or message sent to user mode
  != user-mode reply / local policy decision received and decoded
  != kernel-side complete / resume status applied
  != first user-visible or policy-owned effect proved
```

Compact stop rule:

```text
registered != operation-selected != pre-callback-entered != pended/sent != replied/decided != completed/resumed != effect-owned
```

The usual mistake is to collapse all of this into one sentence like "the minifilter blocked the file" or "the AV saw it." A loaded driver may not be attached to the relevant volume, may not register the operation class, may pass the operation through, may only request a post callback, may pend without receiving a user-mode reply, may timeout to allow/deny, or may complete/resume with a status whose user-visible effect differs from the policy label recovered statically.

## 3. Proof objects

### 3.1 Registration / active filtering truth

What it proves:
- the driver registered with Filter Manager
- the operation-registration table and callback entry points exist
- after `FltStartFiltering(...)`, Filter Manager may begin presenting I/O and volume notifications

Useful evidence:
- `FltRegisterFilter(...)` arguments and returned filter handle
- `FLT_REGISTRATION.OperationRegistration` entries and `IRP_MJ_*` operation codes
- `FltStartFiltering(...)` success or failure and unload path
- instance setup / volume attach evidence, altitude, and volume path where available

What it does **not** prove:
- that the operation under analysis matched any registered callback
- that the filter instance was attached to the relevant volume at the relevant time
- that a callback decided allow/deny rather than only observing or requesting a post callback

Stop when:
- you can name the filter handle, relevant instance/volume, operation classes, and callback entry points well enough that the next uncertainty is operation delivery rather than generic driver presence.

### 3.2 Operation-selection / callback-entry truth

What it proves:
- Filter Manager delivered a specific operation class to a specific pre-operation or post-operation callback
- the callback has temporary control of that operation while executing

Useful evidence:
- breakpoint/hook at the pre-op callback with `Data`, `FltObjects`, file object, process/thread, major/minor function, target path/name state, and instance/volume
- callback return value and whether it requested a post callback
- `CompletionContext` when `FLT_PREOP_SUCCESS_WITH_CALLBACK` is used
- path normalization / name-query helper calls if the policy depends on normalized path rather than raw file object fields

What it does **not** prove:
- that the callback constructed the policy context used later
- that it blocked, allowed, pended, or sent work to user mode
- that post-operation status or final file-system outcome is known

Stop when:
- one representative operation is tied to the exact callback invocation and callback return class.

### 3.3 Verdict-context / scan-request truth

What it proves:
- the callback selected some facts as policy input: file name, process identity, desired access, create options, section state, content hash/sample, stream context, or cached metadata
- a local verdict path or user-mode request may now be reachable

Useful evidence:
- stream/instance/file contexts allocated or looked up
- policy key construction, path/process normalization, access mask decode, content sampling, cache lookup, or rule-table query
- request struct populated before `FltSendMessage(...)`, queue insertion, or worker handoff

What it does **not** prove:
- that the operation was pended or held safely while the verdict is computed
- that user mode received the request or returned a matching reply
- that a local rule decision became `IoStatus.Status`

Stop when:
- the policy inputs for one representative operation are captured, including what remains untrusted or missing.

### 3.4 Pending / user-mode message truth

What it proves:
- the minifilter retained control by returning `FLT_PREOP_PENDING`, queued work, or sent a message to a connected user-mode service
- a scanner-style service boundary may own the next decision

Useful evidence:
- `FLT_PREOP_PENDING` return and NULL completion context
- `FltQueueDeferredIoWorkItem(...)`, cancel-safe queue insertion, worker start, or callback-data ownership
- `FltCreateCommunicationPort(...)`, `FilterConnectCommunicationPort(...)`, connect/disconnect callbacks, and client-port handle
- `FltSendMessage(...)` sender buffer, timeout, reply buffer, status, and correlation id
- user-mode `FilterGetMessage` / `FilterReplyMessage` or equivalent receive-reply path

What it does **not** prove:
- that the message reached the intended user-mode service
- that the service reply is current, trusted, or correlated to this I/O operation
- that the kernel later applied the reply as the final completion/resume status

Stop when:
- the held operation, message identity, user-mode service endpoint, timeout posture, and reply correlation are frozen.

### 3.5 Reply / local-decision truth

What it proves:
- a policy decision was produced or received: allow, deny, quarantine, modify, rescan, fallback, cache-hit, or timeout default
- the decision has enough local context to explain why this operation should continue or fail

Useful evidence:
- reply payload decode and correlation to request id / stream context / operation pointer
- local policy function result and cache state
- timeout fallback branch, disconnected-service branch, malformed-reply handling, or fail-open/fail-closed policy
- worker-to-completion handoff

What it does **not** prove:
- that `IoStatus.Status` was set as expected
- that `FltCompletePendedPreOperation(...)` resumed or completed this exact operation
- that the calling process saw the expected success/failure or that later enforcement/logging happened

Stop when:
- one decision is tied to one held operation and the remaining gap is kernel-side application of that decision.

### 3.6 Completion / resume truth

What it proves:
- the minifilter applied a final or continuing disposition to the operation
- `FLT_PREOP_COMPLETE` plus `IoStatus.Status` can stop lower filters / file system from receiving the operation
- `FltCompletePendedPreOperation(...)` can resume processing for a pended operation, including with complete/pass-through style outcomes

Useful evidence:
- `Data->IoStatus.Status` and `Information` before completion
- callback status passed to `FltCompletePendedPreOperation(...)`
- post-operation callback entry and final status when `FLT_PREOP_SUCCESS_WITH_CALLBACK` was used
- caller-visible NTSTATUS / Win32 error and file-system side effect

What it does **not** prove:
- that the later policy/log/alert/quarantine consumer ran
- that the user-mode message path was the source of the decision unless correlation was preserved
- that similarly named operations in other processes, volumes, or streams had the same outcome

Stop when:
- the final kernel-side disposition and first user-visible effect are paired with the earlier decision evidence.

## 4. Breakpoint / hook plan

Prefer a narrow representative operation over global callback inventory.

1. Registration and attach:
   - `FltRegisterFilter`, `FltStartFiltering`, instance setup, operation-registration table, altitude/volume evidence.
2. Operation delivery:
   - selected pre-op callback for the operation under analysis; capture major/minor function, file object/path, process/thread, desired access/options, callback return status.
3. Policy context:
   - path/process normalization, stream/file/instance context lookup, cache/rule lookup, scan-request struct population.
4. Hold / handoff:
   - `FLT_PREOP_PENDING`, queue insertion, worker entry, `FltSendMessage`, client port, timeout, request id.
5. User-mode service:
   - receive, decode, scan/rule decision, reply, timeout/disconnect/fallback behavior.
6. Kernel apply:
   - worker result handling, `IoStatus.Status`, `FltCompletePendedPreOperation`, post-op callback if used, and final caller-visible status/effect.

## 5. False-stop checklist

Before claiming "the minifilter blocked/allowed this file," rule out:

- **Driver-present false stop**: `FltRegisterFilter` or a loaded `.sys` is visible, but `FltStartFiltering` failed or the instance never attached to the target volume.
- **Operation-mismatch false stop**: the operation under analysis is not one of the registered `IRP_MJ_*` classes, or the relevant behavior is post-op-only.
- **Callback-entry false stop**: pre-op entry is observed, but return status is pass-through or only requests a post callback.
- **Name/context false stop**: raw file-object/path evidence differs from the normalized name or stream context used by policy.
- **Pending false stop**: the operation is pended, but the worker queue, cancel path, or `FltCompletePendedPreOperation` path is not tied back to the original callback data.
- **User-mode-message false stop**: `FltSendMessage` sends a request, but no correlated reply or timeout/fallback branch is proved.
- **Decision false stop**: a rule says deny/allow, but `IoStatus.Status` / completion callback status is not captured.
- **Effect false stop**: kernel completion is proved, but the user-visible status, file-system side effect, alert, quarantine, or downstream policy consumer is still inferred.

## 6. Evidence table shape

For one representative file operation, record:

```text
filter/altitude:
instance/volume:
operation class:
process/thread:
file object / normalized path:
pre-op callback:
callback return:
completion context / post-op requested:
policy inputs:
context/cache/rule id:
pended/queued:
client port / user-mode service:
message id / timeout:
reply / local decision:
IoStatus.Status / Information:
FltCompletePendedPreOperation status:
post-op final status:
caller-visible result:
first downstream consumer/effect:
false stops ruled out:
```

## 7. Hand-off rules

- If the decisive proof object is a user-mode policy service reached over ALPC, RPC, named pipe, COM, or another local IPC after the minifilter message, hand off to the relevant native IPC workflow after preserving the minifilter request identity.
- If the minifilter only emits telemetry, hand off to ETW / runtime-evidence pages instead of narrating enforcement.
- If the same minifilter seam appears in malware, ransomware, or EDR analysis, use this page for kernel/user-mode file-operation proof, then hand off to malware consequence or reporting pages for persistence, impact, and detection packaging.
- If the target is protected-runtime or anti-cheat shaped, avoid stopping at callback-family inventory; preserve the completed/resumed operation or rights/policy consumer before moving into broader kernel-callback telemetry analysis.
