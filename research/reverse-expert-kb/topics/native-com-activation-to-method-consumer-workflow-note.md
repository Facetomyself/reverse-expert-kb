# Native COM Activation to Method Consumer Workflow Note

Topic class: workflow note
Ontology layers: workflow/sensemaking, runtime-evidence bridge, native desktop/server practical branch
Maturity: emerging
Related pages:
- topics/native-binary-reversing-baseline.md
- topics/native-practical-subtree-guide.md
- topics/native-virtual-dispatch-slot-to-concrete-implementation-workflow-note.md
- topics/native-plugin-loader-to-first-real-module-consumer-workflow-note.md
- topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md
- topics/native-windows-named-pipe-impersonation-to-handler-consumer-workflow-note.md
- topics/runtime-behavior-recovery.md

## 1. What this workflow note is for

Use this note when a Windows native target exposes a COM / DCOM local-server, in-proc server, broker, shell extension, updater, service helper, automation object, or malware persistence / hijack path and the visible CLSID, AppID, registry key, `CoCreateInstance(...)`, or `IClassFactory::CreateInstance(...)` evidence is not enough to explain the behavior.

Typical surfaces:
- CLSID / ProgID / AppID strings or registry keys
- `InprocServer32`, `LocalServer32`, `TreatAs`, `ServiceParameters`, or related COM launch metadata
- `CoCreateInstance`, `CoCreateInstanceEx`, `CoGetClassObject`, `CoRegisterClassObject`, `CoRevokeClassObject`
- `IClassFactory::CreateInstance`, `QueryInterface`, vtable/interface-slot calls after activation
- proxy/stub, marshaling, apartment, or DCOM activation traces
- service or broker processes that publish class objects and later dispatch method calls to worker code

This is not an exploitation recipe. It is a stop-rule note for proving which registered class, runtime class object, object instance, interface pointer, method entry, and handler-owned consumer actually own the later effect.

The goal is to move from:

```text
COM registration / CLSID / activation API visible
```

to:

```text
one proved chain from the selected class registration or running class object
through activation, factory/object/interface binding, and method ingress
into one behavior-changing handler, state update, resource access, launch, reply, or downstream effect
```

## 2. When to use this note

Use this note when most of the following are true:
- the target is a Windows native service, broker, updater, desktop helper, shell/Office-style extension, automation object, local IPC endpoint, or malware component
- COM is the most concrete ingress, launch, module-selection, privilege-boundary, or local/remote object surface
- the analyst can see registration material or activation APIs, but the first method-owned consumer is still unclear
- a static CLSID-to-server mapping competes with runtime class-table publication, already-running servers, `TreatAs`/AppID indirection, proxy/stub behavior, or DCOM/local activation differences
- the requested IID, returned interface pointer, apartment/thread delivery, or `QueryInterface` path can change which implementation receives the call
- the interesting question is not merely "which CLSID exists?" but "which method on which object instance caused the effect?"

Do **not** use this as the primary guide when:
- the first trustworthy native semantic anchor is still missing; start with semantic-anchor stabilization
- the bottleneck is a generic vtable/interface-slot implementation after activation is already proved; hand off to virtual-dispatch implementation proof
- the server/module owner is still unknown before any COM-specific activation proof; start with plugin/module loader proof
- the route is clearly service-control-manager control dispatch rather than COM activation; start with service-dispatcher / worker-owned consumer proof
- the remaining ambiguity is only later async callback or event-loop delivery after the method consumer is already reduced

## 3. Core claim

In COM-shaped Windows reversing, registration and activation are usually setup or reduction truth. They are weaker than method-consumer truth.

```text
CLSID / ProgID / AppID / registry mapping visible
  != selected launch context or running class object proved
  != class factory acquired or published for this client
  != object instance created and requested interface returned
  != correct interface pointer / proxy / apartment path bound
  != behavior-bearing method entered with the relevant parameters
  != handler-owned state change, resource access, launch, reply, or downstream effect proved
```

Compact branch memory:

```text
registered != activated != factory-selected != object-created != interface-bound != method-entered != consumed/effected
```

Common false stops:
- treating a CLSID or `LocalServer32` path as proof that the current process launched or handled the request
- treating `CoCreateInstance` success as proof that the later behavior was caused by the returned object
- treating `CoRegisterClassObject` as proof that clients used that class object
- treating `IClassFactory::CreateInstance` as proof that a specific behavior-bearing method ran
- treating an interface IID or proxy/stub artifact as proof of the concrete in-process handler
- treating process launch under COM SCM as proof of method-level effect ownership

## 4. Practical workflow

### Step 1 — Freeze the exact COM claim

Write the smallest claim you need to prove.

Good claim shapes:
- "this CLSID's local server was selected for this client activation"
- "this running EXE server's class object serviced the activation rather than a fresh launch"
- "this requested IID returned this concrete interface pointer"
- "this method invocation, not just activation, performed the state write / launch / reply"

Avoid starting with:
- "the COM object did it"
- "the CLSID points to the malware"
- "CoCreateInstance proves execution"

Those are usually too broad to test.

### Step 2 — Separate install-time registration from runtime publication

For registration evidence, collect:
- CLSID / ProgID / AppID
- `InprocServer32` or `LocalServer32` path and bitness / registry-view posture
- service-hosted or local-server launch hints
- `TreatAs`, elevation, surrogate, or AppID indirection if present
- timestamp / hive / user-vs-machine scope if relevant

For runtime publication evidence, collect:
- server process identity and command line
- `CoRegisterClassObject` hit / class-table registration
- class object pointer identity and registration token when observable
- `CoRevokeClassObject` or shutdown timing when lifecycle matters

Stop rule:
- registry truth is not running-server truth
- running-server truth is not selected-factory truth

### Step 3 — Prove activation context and class-object selection

At the client side, bind:
- `CoCreateInstance`, `CoCreateInstanceEx`, or `CoGetClassObject` callsite
- CLSID, `CLSCTX_*`, requested IID(s), machine name / remote posture, and HRESULT
- caller process/thread/apartment and impersonation/security posture if relevant
- returned class-object or object/interface pointer

At the server side, bind:
- whether the server was already running or launched by COM/SCM
- whether the relevant class object was registered before the activation
- whether the factory object's `QueryInterface` / `CreateInstance` path fired for this activation

Useful breakpoints / hooks:
- client: `CoCreateInstance`, `CoCreateInstanceEx`, `CoGetClassObject`
- server: `CoRegisterClassObject`, `IClassFactory::CreateInstance`, server-side `QueryInterface`
- lifecycle: `CoRevokeClassObject`, process start/exit, class-factory refcount/lock helpers when available

Stop rule:
- activation success is object-reference truth, not method behavior truth

### Step 4 — Bind the returned interface to one concrete implementation

After activation, reduce the interface pointer:
- record the requested IID and returned pointer
- resolve proxy vs direct in-proc pointer where possible
- if the call is marshaled, identify the proxy/stub or generated dispatch layer separately from the server handler
- map the vtable/interface slot or dispatch ID to one concrete server-side method
- keep aggregation and `QueryInterface` paths separate if the object can expose multiple identities

Good evidence:
- returned pointer's vtable/module ownership
- server-side method prologue hit paired to the client's call
- marshaled call ID / method ordinal / dispatch ID matched to handler entry
- object instance state or `this` pointer continuity from factory output into method entry

Stop rule:
- `IID` requested is not method entered
- proxy/stub delivery is not handler-owned effect

### Step 5 — Prove method entry and parameter ownership

For the candidate behavior-bearing method, freeze:
- method identity / slot / dispatch ID
- object instance identity
- decoded parameters after unmarshaling or `IDispatch` coercion
- caller identity / security context when authorization or privilege matters
- immediate branch decision that routes into the candidate handler

Useful checks:
- compare a successful activation with a no-op method call
- compare two methods on the same interface if the effect belongs to only one
- break on state/resource writes, process launch, file/registry/network operations, or reply construction after method entry
- keep client-side wrapper calls separate from server-side handler entry

Stop rule:
- method entry is still weaker than the first durable state/effect consumer if the method only enqueues, posts, or forwards work

### Step 6 — Follow handoff to the first behavior-changing consumer

If the method immediately does the work, prove the resource/state/effect inside the method lifetime.

If the method forwards work, hand off deliberately:
- queued task / thread pool / completion callback
- service worker / broker dispatcher
- named-pipe / RPC / ALPC secondary path
- event-loop / message-pump delivery
- policy engine, reducer, or rule evaluator

Package the result as:

```text
COM proof boundary reached: <highest proven boundary>
first behavior-owning consumer: <function/thread/object/handler/effect>
next missing boundary if not proved: <specific gap>
```

## 5. Evidence ladder

A useful ladder for case notes:

```text
artifact layer:
  CLSID / ProgID / AppID / registry values

selection layer:
  class context, launch path, running-server class table, security / bitness / user scope

factory layer:
  CoGetClassObject / CoRegisterClassObject / IClassFactory selected

object layer:
  CreateInstance / requested IID / returned interface pointer / QueryInterface

call layer:
  proxy/stub or direct vtable/IDispatch method delivery

consumer layer:
  handler-owned state change, resource access, launch, reply, or downstream effect
```

Only the last reached layer should be claimed as proved.

## 6. Red flags and compare-pair tests

Red flags:
- CLSID resolves to several bitness/user-scope candidates
- `TreatAs`, AppID, surrogate, service-hosting, or activation permission changes the selected server
- a running EXE server publishes a class object, so no fresh launch occurs during the observed client action
- a proxy/stub or `IDispatch` layer absorbs the visible call before the real handler
- activation succeeds but the requested method is never called
- method entry occurs but only posts work to another thread or service worker
- authorization or impersonation changes between activation and method body

Compare-pair tests:
- same CLSID, different requested IID
- same activation, no subsequent method call
- same method, different parameters
- registry artifact present vs class-table registration absent
- server already running vs forced cold activation
- direct in-proc server vs local-server / proxy path
- method entry with downstream queue disabled vs enabled

## 7. Output shape for reports

When writing a case note, prefer:

```text
Visible COM evidence:
- ...

Highest proven boundary:
- registered / activated / factory-selected / object-created / interface-bound / method-entered / consumed

Evidence:
- ...

First consumer or next missing boundary:
- ...

Overclaim avoided:
- ...
```

The main operator discipline is simple: do not let a COM-shaped artifact or activation API impersonate method-consumer truth.
