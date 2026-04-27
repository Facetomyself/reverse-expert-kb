# Native D-Bus Service Activation to Method Consumer Workflow Note

Topic class: workflow note
Ontology layers: workflow/sensemaking, runtime-evidence bridge, native desktop/server practical branch
Maturity: emerging
Related pages:
- topics/native-binary-reversing-baseline.md
- topics/native-practical-subtree-guide.md
- topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md
- topics/runtime-behavior-recovery.md

## 1. What this workflow note is for

This note covers Linux / desktop / server native reversing cases where the interesting behavior is exposed through D-Bus:

- a system or session bus name is visible
- a `.service` file, `SystemdService=`, or systemd unit hints at activation
- object paths, interfaces, members, signatures, or introspection XML are recoverable
- but the investigation still stalls because no one has proved which service process, method handler, binding dispatch path, or handler-owned consumer actually owns the behavior

This is not a D-Bus API tutorial.
It is a stop-rule note for native service reversing.

The goal is to move from:

```text
bus name / object path / interface / method visible
```

to:

```text
one proved chain from bus instance and current owner
through activation / delivery and binding dispatch
into one handler-owned consumer and downstream effect
```

## 2. When to use this note

Use this note when most of the following are true:
- the target is a relatively ordinary Linux native service, daemon, desktop helper, settings daemon, device manager, updater, or agent
- D-Bus is the most visible ingress or control surface
- a bus name, `.service` file, systemd unit, object path, interface, method name, or introspection result is available
- static xrefs from handler names or binding tables are not enough to prove which path was actually invoked
- bus/service lifecycle may matter: activatable vs currently owned, system vs session bus, systemd activation, policy gating, or current unique-name owner
- one narrow method-to-consumer proof would make a large amount of service scaffolding trustworthy

Do **not** use this as the primary guide when:
- the first trustworthy semantic anchor is still missing; use semantic-anchor stabilization first
- several broad non-D-Bus entry families still compete; use interface-to-state proof first
- the case is mostly protocol replay / wire-format reconstruction rather than local service ownership
- the D-Bus method handler is already proved and the only remaining ambiguity is a deeper worker queue, callback, or event-loop consumer

## 3. Core claim

In D-Bus-shaped native service work, the visible API contract is usually not the behavior proof.
The operator needs to keep these proof objects separate:

```text
service file / activatable name found
  != bus instance and policy path selected
  != current owner / unique connection identified
  != activation request succeeded
  != name acquired by the process that matters
  != object path / interface / member contract selected
  != method call delivered to that owner
  != binding dispatch reached the native handler
  != first handler-owned consumer / side effect
```

The common mistake is to stop at one of the earlier rungs:
- `.service` file found
- `busctl --activatable` lists the name
- introspection XML has the method
- `busctl call` returns something
- a binding stub or generated adaptor name matches the interface

Those are useful, but they do not yet prove that the current run delivered the target method to the intended process and that the native handler changed behavior.

## 4. The boundaries to mark explicitly

### A. Bus-instance and scope boundary

First decide which bus is relevant:
- system bus
- user/session bus
- container / namespace-local bus
- custom address via environment or launch wrapper
- compatibility/autolaunch case

What to capture:
- the bus address or bus type
- whether the name is acquired, activatable, or absent on that bus
- whether a different bus instance gives a contradictory answer

Stop rule:

```text
name found on one bus != target behavior reachable on the bus the client uses
```

### B. Activation / launch-route boundary

Activation metadata includes:
- `.service` files with `Name=` and `Exec=`
- system-bus `User=`
- `SystemdService=` indirection
- systemd unit aliases or `BusName=` posture
- policy files under the system-bus configuration tree

What to capture:
- whether the service is merely activatable or currently owned
- which executable / systemd unit would be launched
- whether policy can block auto-start or delivery
- whether activation occurred in the run being studied

Stop rule:

```text
activatable != activated != owned by this process != call delivered
```

### C. Current owner / unique-connection boundary

A well-known name is a routing name. A unique name identifies the current connection.

What to capture:
- current unique owner from `GetNameOwner`, `busctl status`, or equivalent
- process ID / credentials when available
- `NameOwnerChanged` transitions around activation or restart
- whether a crash/restart changed the owner between observation and call

Stop rule:

```text
well-known name visible != same unique connection handled this method
```

### D. Contract-selection boundary

D-Bus method calls are shaped by:
- service / destination name
- object path
- interface
- member / method name
- signature and arguments
- reply / error behavior

What to capture:
- selected object path and interface from introspection or source/binary artifacts
- exact signature and representative arguments
- whether introspection is missing, stale, policy-filtered, generated, or broader than what the current service instance actually dispatches

Stop rule:

```text
introspection visible != method implemented by the current owner != handler reached
```

### E. Delivery and binding-dispatch boundary

Bus-level delivery is the point where the selected call reaches the owner connection.
Binding dispatch is the next point where framework glue maps it to a native handler.

Useful proof surfaces:
- `busctl monitor` / `dbus-monitor` / pcapng capture
- match rules for destination/interface/member/path
- `StartServiceByName` / `NameOwnerChanged` / reply-error observation
- GLib/GDBus, QtDBus, sd-bus, libdbus, or generated-adaptor dispatch surfaces
- breakpoints on method tables, vtables, generated stubs, or handler symbols

Stop rule:

```text
message observed on bus != binding dispatch entered != final native handler owns behavior
```

### F. First handler-owned consumer / effect boundary

The first real consumer is the smallest handler-side action that predicts later behavior.
Typical candidates:
- state / settings write
- authorization or policy reducer
- worker enqueue or retained task object
- device/session/object lookup that selects a durable owner
- file, network, IPC, or reply-producing branch
- signal emission or property-change path that later consumers depend on

Stop rule:

```text
handler entry != worker/task/state consumer != downstream effect
```

## 5. Default workflow

### Step 1: choose one method-shaped question

Do not start by mapping every bus name and every object path.
Choose one target behavior and one candidate D-Bus method or signal family.

Good questions:
- which method toggles the setting / mode / policy I care about?
- which object path owns the device/session/object instance?
- does this call activate the service, or is it already owned?
- which native handler consumes these arguments?

### Step 2: freeze the bus and current owner

Record:
- system vs session/user bus
- acquired vs activatable state
- current unique owner if acquired
- PID / executable / credentials if available
- activation transition if not already owned

If owner state changes during the run, treat the old proof as stale until one call is tied to the new unique owner.

### Step 3: reduce the contract to one object/interface/member/signature

Use introspection, strings, generated adaptor artifacts, source symbols, or binary tables to choose:

```text
destination name + object path + interface + member + signature + representative arguments
```

If introspection fails or is policy-limited, use message traces and binary/static artifacts instead of treating missing XML as missing implementation.

### Step 4: prove delivery before handler claims

Capture one method call at the bus boundary and preserve:
- sender
- destination / current unique owner
- path
- interface
- member
- signature and arguments
- reply, error, or timeout
- whether auto-start was allowed

This separates call-shape truth from handler truth.

### Step 5: cross the binding boundary

Map the D-Bus contract into native code:
- GLib/GDBus: generated skeleton/adaptor method table or `GDBusInterfaceVTable`-style dispatch
- QtDBus: adaptor meta-object / slot dispatch / `qt_metacall`-style edge
- sd-bus: vtable entry and handler callback
- libdbus/custom: message filter, dispatch loop, method-name comparisons

The exact binding family matters less than the proof shape:

```text
bus-delivered method -> binding dispatch -> native handler candidate
```

### Step 6: prove one handler-owned consumer

Do not stop at handler entry if the handler only validates, routes, or enqueues.
Follow one more edge to the first durable consumer:
- state write
- retained task/context
- worker queue insertion
- device/session object mutation
- external effect
- reply-producing or signal-producing branch

Rewrite the working map only after this consumer is proved.

## 6. Minimal evidence package

A useful evidence package contains:
- bus type/address and observed name state
- activation route: `.service`, `Exec=`, `SystemdService=`, unit alias, or explicit no-activation finding
- current unique owner / PID / credentials at call time
- object path, interface, member, signature, and representative arguments
- bus-level delivery evidence and reply/error/timeout result
- binding dispatch or native handler proof
- first handler-owned consumer and downstream effect
- any policy or scope caveat that could make replay or another host behave differently

## 7. Handoff rules

Handoff to `native-service-dispatcher-to-worker-owned-consumer-workflow-note.md` when:
- the D-Bus handler is proved, but the service-owned worker path or retained task still hides the real consumer

Handoff to `native-callback-registration-to-event-loop-consumer-workflow-note.md` when:
- the handler posts into an event loop, callback framework, or deferred completion and the next proof object is delivered callback ownership

Handoff to `protocol-method-contract-to-minimal-replay-fixture-workflow-note.md` when:
- the method contract is now the stable object and the next need is a minimal replay/edit/fuzz fixture rather than native service ownership

Handoff to `runtime-behavior-recovery.md` or compare-run notes when:
- the call is delivered and handler entry is proved, but the behavior difference only appears later and needs causal localization.

## 8. Compact reminder

Keep the smaller ladder visible:

```text
listed != activatable != owned != delivered != dispatched != consumed
```

For D-Bus service reversing, that is the practical difference between a contract-shaped guess and a behavior-owned proof.
