# Windows service trigger / handler / worker-consumer notes

Source class: external research notes  
Date: 2026-06-10  
Branch: native desktop/server practical workflows

## Sources consulted

- Microsoft Learn — Service Trigger Events: https://learn.microsoft.com/en-us/windows/win32/services/service-trigger-events
- Microsoft Learn — `SERVICE_TRIGGER`: https://learn.microsoft.com/en-us/windows/win32/api/winsvc/ns-winsvc-service_trigger
- Microsoft Learn — Service Control Handler Function: https://learn.microsoft.com/en-us/windows/win32/services/service-control-handler-function
- Microsoft Learn — `LPHANDLER_FUNCTION_EX`: https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nc-winsvc-lphandler_function_ex
- Microsoft Learn — `SERVICE_STATUS`: https://learn.microsoft.com/en-us/windows/win32/api/winsvc/ns-winsvc-service_status
- Inbits — Reversing `npsvctrig.sys` - Named Pipe Service Triggers: https://inbits-sec.com/posts/npsvctrig-notes/

## Facts worth preserving

### Trigger configuration is not trigger delivery

Microsoft’s service-trigger documentation splits trigger behavior into:

- service configuration via `ChangeServiceConfig2(... SERVICE_CONFIG_TRIGGER_INFO ...)`
- a `SERVICE_TRIGGER_INFO` array containing one or more `SERVICE_TRIGGER` records
- trigger type / subtype / action / optional trigger-specific data matching
- actual start or stop action when the condition is true at boot or becomes true at runtime
- `SERVICE_TRIGGER_STARTED_ARGUMENT` being supplied to `ServiceMain` as `argv[1]` when the service is started because of a trigger

Operator implication: `sc qtriggerinfo`, registry configuration, or `SERVICE_TRIGGER` reconstruction is only eligibility/configuration truth. It does not prove that the trigger condition fired, that SCM selected this service instance, or that the service’s worker path consumed the trigger-caused start.

### Trigger-event controls can arrive while the service is already running

Microsoft documents that when a trigger event occurs while a service is already running, SCM sends `SERVICE_CONTROL_TRIGGEREVENT`. A service stopping itself after idle timeout should be ready for trigger events during the stop transition; if it returns `ERROR_SHUTDOWN_IN_PROGRESS`, SCM queues trigger events until the service reaches stopped state, then applies the trigger action.

Operator implication: for trigger-start services, `ServiceMain` is not the only proof surface. HandlerEx/control paths and accepted-control posture matter, especially for repeated events, queued events, and stop/idle races.

### Accepted-controls posture is runtime truth, not static capability

The service control handler docs state that services register handlers with `RegisterServiceCtrlHandler*` / `RegisterServiceCtrlHandlerEx*`; acceptance of many controls is enabled or disabled through `SetServiceStatus` / `dwControlsAccepted`. `SERVICE_STATUS.dwControlsAccepted` describes which control codes the service currently accepts and processes. For trigger events, the service should set `SERVICE_ACCEPT_TRIGGEREVENT` when ready to handle queued trigger events.

Operator implication: a static `HandlerEx` switch arm for `SERVICE_CONTROL_TRIGGEREVENT` is weaker than runtime evidence that the service reported `SERVICE_ACCEPT_TRIGGEREVENT` at the relevant state. A handler arm can be dead for the present service state.

### Handler entry is usually a reduction boundary

Microsoft explicitly warns that service control handlers run in the control-dispatcher context and should return within 30 seconds; lengthy processing should move to a secondary thread. That makes HandlerEx entry weaker than worker-owned consumer proof.

Operator implication: if the target behavior appears after a stop, preshutdown, device, or trigger-event control, freeze handler entry only as the control-ingress boundary, then find the queued task/thread/work item/context object that owns the later effect.

### Named-pipe service triggers add a kernel/minifilter + ETW bridge

The Inbits `npsvctrig.sys` reversing note reports a concrete implementation path for named-pipe service triggers:

- `npsvctrig.sys` is a filesystem minifilter for named-pipe trigger behavior
- it maintains active trigger state synchronized through WNF from registry-backed network service trigger data
- it registers ETW providers, including `Microsoft-Windows-EndpointTriggerProvider`
- it attaches to NPFS, watches relevant create / named-pipe / FS control paths, and publishes ETW when a matching trigger condition occurs
- SCM consumes the ETW event and starts the corresponding service executable

Operator implication: for named-pipe trigger cases, the proof ladder includes an extra boundary: attempted pipe/open/wait event and kernel trigger publication are still not the same as SCM start selection or service-owned request handling. A pipe name in `qtriggerinfo` does not prove a live pipe handler processed the client request.

## Practical proof ladder

Preserve this stop rule for Windows service trigger / control work:

```text
trigger configured
  != condition fired / endpoint event observed
  != SCM selected action
  != service process entered because of trigger
  != accepted-controls posture permits this control now
  != HandlerEx / ServiceMain routed the event
  != worker handoff / retained task exists
  != first worker-owned consumer/effect
```

Compact branch memory:

```text
configured != fired != selected != entered != accepted/routed != handed off != consumed/effected
```

## Suggested observation points

- `QueryServiceConfig2(... SERVICE_CONFIG_TRIGGER_INFO ...)` / `sc qtriggerinfo` for configuration truth only.
- `StartServiceCtrlDispatcher*`, `ServiceMain`, and `argv[1] == SERVICE_TRIGGER_STARTED_ARGUMENT` for trigger-start entry truth.
- `RegisterServiceCtrlHandlerEx*`, `HandlerEx(dwControl == SERVICE_CONTROL_TRIGGEREVENT)`, and `SetServiceStatus` / `dwControlsAccepted` for control acceptance and routing truth.
- For named-pipe trigger cases, separate NPFS/minifilter evidence, ETW provider publication, SCM start action, and service-side pipe request handling.
- Break/watch after handler/entry on `CreateThread`, thread-pool submission, queue insertion, retained context population, or dispatcher bucket selection to prove worker-owned consumer truth.

## False stops

- `sc qtriggerinfo` shows trigger data, so the service ran because of that trigger.
- `SERVICE_TRIGGER` / registry data recovered, so a current event fired.
- `ServiceMain` entered, so trigger semantics are proved.
- `HandlerEx` has a `SERVICE_CONTROL_TRIGGEREVENT` arm, so the service accepts trigger controls in the relevant state.
- `SetServiceStatus(SERVICE_RUNNING)` happened, so the target behavior is service-owned.
- `npsvctrig.sys` or an ETW event indicates named-pipe trigger publication, so the service-side handler consumed the request.
