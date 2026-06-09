# Native Windows Service Trigger to Worker Consumer Workflow Note

Topic class: workflow note  
Ontology layers: workflow/sensemaking, runtime-evidence bridge, native desktop/server practical branch  
Maturity: emerging  
Related pages:
- topics/native-binary-reversing-baseline.md
- topics/native-practical-subtree-guide.md
- topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md
- topics/native-windows-named-pipe-impersonation-to-handler-consumer-workflow-note.md
- topics/native-etw-provider-session-consumer-workflow-note.md
- topics/runtime-behavior-recovery.md

## 1. What this workflow note is for

Use this note when a Windows service is started, stopped, or signaled through service trigger events and the visible trigger configuration is not enough to explain the target behavior.

Typical surfaces:
- `sc qtriggerinfo`, `QueryServiceConfig2(... SERVICE_CONFIG_TRIGGER_INFO ...)`, `ChangeServiceConfig2(... SERVICE_CONFIG_TRIGGER_INFO ...)`
- `SERVICE_TRIGGER_INFO`, `SERVICE_TRIGGER`, trigger subtype GUIDs, device-interface triggers, firewall-port triggers, IP availability triggers, ETW custom triggers, named-pipe / RPC endpoint triggers
- `StartServiceCtrlDispatcher*`, `ServiceMain`, `SERVICE_TRIGGER_STARTED_ARGUMENT`
- `RegisterServiceCtrlHandlerEx*`, `HandlerEx`, `SERVICE_CONTROL_TRIGGEREVENT`, `SERVICE_ACCEPT_TRIGGEREVENT`
- services that idle-stop and are reactivated by endpoint, device, ETW, or network availability events
- named-pipe trigger cases where `npsvctrig.sys`, ETW, SCM, and the service’s own pipe server can be confused as one mechanism

The goal is to move from:

```text
service trigger configuration or trigger-looking handler exists
```

to:

```text
one proved chain from trigger condition / SCM action
through service entry or HandlerEx routing
into one worker handoff and first worker-owned effect
```

## 2. When to use this note

Use this note when most of the following are true:
- the target is a Windows native service, helper, broker, updater, endpoint agent, or service-hosted component
- trigger-start / trigger-stop behavior is visible or suspected
- the analyst can see trigger configuration, trigger GUIDs, service control handlers, or service startup arguments
- the current uncertainty is whether a configured trigger actually fired and reached behavior-bearing service code
- repeated trigger events, idle-stop transitions, or already-running service behavior may matter
- named-pipe / RPC / ETW / device triggers create extra transport or kernel-side evidence that can be overread as service-side consumer proof

Do **not** use this as the primary note when:
- the service is simply started manually or at boot and trigger semantics do not matter; use the general service-dispatcher note
- the interesting boundary is already reduced to a pipe request plus impersonation lifetime; use the named-pipe impersonation note
- the interesting boundary is ETW provider/session/event consumer truth rather than service trigger action selection; use the ETW provider/session note
- the first trustworthy native semantic anchor is still missing; stabilize names/types/routes first

## 3. Core claim

Windows service trigger analysis should keep trigger eligibility, trigger firing, SCM action selection, service entry, control acceptance, handler routing, worker handoff, and effect ownership separate.

Compact stop rule:

```text
configured != fired != selected != entered != accepted/routed != handed off != consumed/effected
```

Expanded ladder:

```text
trigger configured
  != condition fired / endpoint event observed
  != SCM selected start/stop/control action
  != service process entered because of trigger
  != accepted-controls posture permits this control now
  != HandlerEx / ServiceMain routed the event
  != worker handoff / retained task exists
  != first worker-owned consumer/effect
```

Why this matters:
- `SERVICE_TRIGGER` or `sc qtriggerinfo` is configuration truth, not event truth
- a trigger condition can be true at boot or become true at runtime, so boot-time and live-event proof differ
- an already-running service can receive `SERVICE_CONTROL_TRIGGEREVENT`; `ServiceMain` is not the only relevant surface
- `dwControlsAccepted` / `SERVICE_ACCEPT_TRIGGEREVENT` is runtime posture; a static HandlerEx arm may be inactive in the current state
- control handlers are expected to return quickly, so behavior often belongs to a secondary thread, thread-pool callback, queue item, or retained task object
- named-pipe service triggers add a lower layer where NPFS/minifilter observation and ETW publication can prove trigger publication without proving service-side request consumption

## 4. Boundaries to mark explicitly

### A. Trigger configuration / eligibility boundary

Capture:
- service name and trigger source: `QueryServiceConfig2`, `sc qtriggerinfo`, registry-backed service-trigger material, or installer/configuration code
- trigger type, subtype GUID, action, and data-item matching semantics
- whether the trigger starts, stops, or signals an already-running service
- OS-version assumptions, because network endpoint triggers and service triggers have version constraints

Do not conclude:
- that the trigger fired
- that SCM selected this service in the current run
- that the service consumed the trigger-caused event

### B. Condition-fired / endpoint-observed boundary

Capture the event that allegedly makes the trigger true:
- device interface arrival / present-at-boot condition
- first IP address availability or last removal
- firewall port open/close condition
- ETW custom provider event
- named-pipe or RPC endpoint request
- group policy or domain join/leave transition

For named-pipe triggers, separate:
- client open/wait attempt against the pipe name
- NPFS/minifilter observation
- ETW trigger publication
- SCM action
- service-side pipe handler consumption

Do not treat a pipe name or trigger GUID as proof that a live endpoint event happened.

### C. SCM action-selection boundary

Capture:
- start/stop action selected by SCM
- queued trigger behavior when the service is stopping or already running
- whether SCM supplied `SERVICE_TRIGGER_STARTED_ARGUMENT` to `ServiceMain`
- whether trigger-stop is blocked by dependent services
- low-memory or queueing caveats where trigger requests are not guaranteed

Do not confuse SCM action selection with service-owned behavior. A service process can enter and report state without reaching the worker that owns the target effect.

### D. Service entry / accepted-control posture boundary

Capture:
- `StartServiceCtrlDispatcher*` connection and `ServiceMain` entry
- `argv[1] == SERVICE_TRIGGER_STARTED_ARGUMENT` when present
- `RegisterServiceCtrlHandlerEx*` and the handler context
- `SetServiceStatus` calls and `SERVICE_STATUS.dwControlsAccepted`
- whether `SERVICE_ACCEPT_TRIGGEREVENT` is set before queued/repeated trigger-event controls are expected

Do not treat a static `HandlerEx` switch arm as enough. A service only accepts most controls when its runtime status says it accepts them.

### E. Handler / ServiceMain routing boundary

Capture:
- `HandlerEx(dwControl == SERVICE_CONTROL_TRIGGEREVENT)` routing
- start-argument routing in `ServiceMain`
- control-specific switch buckets, queue selection, or operation-class selection
- stop/preshutdown/shutdown interactions if trigger-stop or idle-stop behavior is relevant

Do not stop at handler entry. The handler executes in the control-dispatcher context and should return quickly; lengthy work is normally moved elsewhere.

### F. Worker handoff / retained-task boundary

Capture the first durable obligation created by the trigger route:
- `CreateThread`, `_beginthreadex`, thread-pool work, timer queue, APC, IOCP, or custom queue submission
- retained task/context object populated from trigger state
- service-owned session/object ownership transfer
- queued pipe/RPC/device/network operation family
- callback pointer or worker routine that predicts the later effect

This is usually the first place where trigger/control truth becomes behaviorally useful.

### G. First worker-owned consumer / effect boundary

Capture:
- first state mutation, mode transition, or persistent flag owned by the worker path
- first file/network/IPC/device operation only reachable through the trigger-owned worker path
- first downstream callback or reducer reached after handoff
- compare-run difference when the trigger condition is suppressed, delayed, or repeated

This is where the analyst can finally claim the trigger-owned service path matters.

## 5. Default workflow

### Step 1: classify the trigger source and action

Start with one service and one trigger. Record:

```text
service -> trigger type/subtype/data -> action -> expected service surface
```

Avoid mapping every configured trigger first. Most cases need one representative trigger-to-effect chain, not a full trigger inventory.

### Step 2: prove event truth separately from configuration truth

Use the cheapest discriminant for the trigger class:
- for device triggers, prove arrival/presence and matching hardware/compatible ID data
- for firewall/IP triggers, prove the network condition rather than only service configuration
- for ETW custom triggers, prove provider event emission and payload match
- for named-pipe/RPC triggers, prove endpoint request/pipe wait/open and keep trigger-publication evidence separate from service-side handling

### Step 3: freeze SCM selection before service logic

Look for evidence that SCM actually selected the action:
- service start reason / `SERVICE_TRIGGER_STARTED_ARGUMENT`
- service state transition correlated with the event
- queued `SERVICE_CONTROL_TRIGGEREVENT` when the service is running or transitioning
- negative evidence when the trigger is configured but dependencies, state, or low-memory behavior prevent the expected action

### Step 4: check accepted-controls posture before trusting HandlerEx

For already-running or repeated trigger events, static `HandlerEx` presence is not enough. Verify:
- the handler was registered with `RegisterServiceCtrlHandlerEx*`
- `dwControlsAccepted` included the relevant accepted bit at the relevant time
- the handler returned a value that preserves or rejects queued trigger semantics intentionally

### Step 5: reduce handler/start routing to one worker-owned obligation

Break/watch at the transition from service plumbing to retained work:
- queue insertion
- thread start
- thread-pool submit
- task/context object population
- selected dispatcher bucket

Prefer one retained object or callback pointer over a broad “service started” claim.

### Step 6: prove one consequence and then widen only if needed

The useful artifact is:

```text
trigger source -> SCM action -> service entry/control -> worker handoff -> consumer/effect
```

Only after this chain is proved should you widen into sibling triggers, adjacent services, or broader service-host lifecycle analysis.

## 6. Minimal breakpoint / hook plan

### Static triage

- Enumerate trigger configuration with `sc qtriggerinfo` or `QueryServiceConfig2(... SERVICE_CONFIG_TRIGGER_INFO ...)`.
- Find service entry / handler registration: `StartServiceCtrlDispatcher*`, `ServiceMain`, `RegisterServiceCtrlHandlerEx*`, `SetServiceStatus`.
- Mark `HandlerEx` arms for `SERVICE_CONTROL_TRIGGEREVENT`, stop, preshutdown, device, session, and param-change controls.
- Identify nearby worker-handoff APIs and retained task/context structures.

### Runtime proof

- Observe the trigger condition or endpoint event.
- Correlate SCM state transition or trigger-start argument.
- Break on `HandlerEx` / `ServiceMain` route and record accepted-controls posture.
- Break on queue/thread/thread-pool handoff from the selected route.
- Watch the retained task/context until the first worker-owned consumer or effect.

### Compare-run discriminants

Run at least one pair when feasible:
- trigger condition present vs absent
- service already running vs stopped
- service stopping/idle-timeout transition vs stable running
- named-pipe trigger request observed at NPFS/minifilter/ETW layer vs service-side pipe handler consumption

The compare goal is to avoid treating configuration, publication, and service-side behavior as one event.

## 7. Common false stops

- `SERVICE_TRIGGER` exists, so the trigger fired.
- `sc qtriggerinfo` shows a named pipe / RPC / device trigger, so a live endpoint event happened.
- SCM started the service, so the target behavior is trigger-owned.
- `SERVICE_TRIGGER_STARTED_ARGUMENT` reached `ServiceMain`, so the worker path is known.
- `HandlerEx` has a `SERVICE_CONTROL_TRIGGEREVENT` case, so repeated trigger events are accepted in the current state.
- `SetServiceStatus(SERVICE_RUNNING)` happened, so service-owned work is complete.
- `npsvctrig.sys` / ETW showed endpoint trigger publication, so the service-side pipe or RPC handler consumed the request.
- one control-handler breakpoint hit, so the later effect belongs to the handler rather than a secondary worker.

## 8. Evidence package to leave behind

A useful final note for a case should contain:
- trigger configuration and source class
- observed trigger event / endpoint event
- SCM action and service state/argument evidence
- accepted-control posture at the relevant state
- handler or ServiceMain route
- worker handoff object/function/context
- first worker-owned consumer/effect
- one false-stop explicitly ruled out

## 9. Source-backed anchors

- Microsoft’s service-trigger documentation: trigger configuration uses `ChangeServiceConfig2(... SERVICE_CONFIG_TRIGGER_INFO ...)`, matching data items, boot-time or runtime condition truth, trigger-start `argv[1]`, queued trigger controls, `SERVICE_ACCEPT_TRIGGEREVENT`, and `QueryServiceConfig2` / `sc qtriggerinfo` inspection.
- Microsoft’s control-handler documentation: handlers are registered with `RegisterServiceCtrlHandler*` / `RegisterServiceCtrlHandlerEx*`, controls are gated by accepted-control state, handlers execute in the control-dispatcher context, and lengthy work should move to a secondary thread.
- Microsoft’s `SERVICE_STATUS` documentation: `dwControlsAccepted` is the current control-acceptance posture.
- Inbits’ `npsvctrig.sys` reversing note: named-pipe service triggers involve a minifilter, WNF-synchronized trigger list, ETW publication, and SCM consumption, which creates a real boundary between endpoint trigger publication and service-side handler consumption.
