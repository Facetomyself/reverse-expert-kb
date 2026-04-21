# 2026-04-22 — Windows service dispatcher / worker handoff realism notes

Topic focus: native service/daemon dispatcher visibility versus worker-owned consumer truth in ordinary Windows service cases

## Why this note exists
The native branch already had a `native-service-dispatcher-to-worker-owned-consumer-workflow-note.md`, but its middle rungs were still too easy to compress into a vague story like:

- `StartServiceCtrlDispatcher` is visible
- `ServiceMain` is visible
- a control handler is visible
- therefore the service path is basically owned

The official Windows service docs support a sharper practical split:
- dispatcher connection is one proof object
- `ServiceMain` entry is another
- handler registration and accepted-controls posture are another
- control-handler invocation is another
- worker handoff / retained task truth is another
- first worker-owned consumer is still one hop later

That is exactly the kind of middle ladder reversers need when the service shell is easy to read but the first behavior-owning worker path is still unclear.

## Source set used
### Official / high-confidence
1. Microsoft Learn — `StartServiceCtrlDispatcherW`
   - https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-startservicectrldispatcherw
2. Microsoft Learn — `RegisterServiceCtrlHandlerEx`
   - https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-registerservicectrlhandlerexa
3. Microsoft Learn — `Service Control Handler Function`
   - https://learn.microsoft.com/en-us/windows/win32/services/service-control-handler-function
4. Microsoft Learn — `Writing a ServiceMain Function`
   - https://learn.microsoft.com/en-us/windows/win32/services/writing-a-servicemain-function
5. Microsoft Learn — `SetServiceStatus`
   - https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-setservicestatus
6. Microsoft Learn — `Writing a Service Program's main Function`
   - https://learn.microsoft.com/en-us/windows/win32/services/writing-a-service-program-s-main-function
7. Microsoft Learn — `Service State Transitions`
   - https://learn.microsoft.com/en-us/windows/win32/services/service-status-transitions

### Search artifact
- `sources/native/2026-04-22-0450-native-service-dispatcher-worker-handoff-search-layer.txt`

## High-signal takeaways
### 1. Dispatcher connection truth is not the same thing as worker ownership
From `StartServiceCtrlDispatcherW` and `Writing a Service Program's main Function`:
- the main thread connects to the SCM and becomes the service control dispatcher
- the dispatcher thread does not return until all running services in the process have entered `SERVICE_STOPPED`
- the dispatcher invokes handlers for control requests or creates a new thread to execute the appropriate `ServiceMain`

Practical implication:
- `StartServiceCtrlDispatcher*` is a strong orientation anchor
- but it is still dispatcher-connection truth, not proof that the behavior-owning path has been reduced to a worker-owned consumer
- the fact that the dispatcher can create a new `ServiceMain` thread is itself a reminder that dispatcher-visible control flow and behavior ownership can diverge immediately

### 2. `ServiceMain` entry, handler registration, and accepted-controls posture are separate proof objects
From `RegisterServiceCtrlHandlerEx`, `Writing a ServiceMain Function`, and `SetServiceStatus`:
- `ServiceMain` should immediately register the control handler
- the registration call must occur before the first `SetServiceStatus` because it yields the service status handle and puts the handler in place before accepted controls are advertised
- the sample `ServiceMain` guidance reports `SERVICE_START_PENDING` first and recommends not accepting controls during initialization
- only after initialization is complete does the service report `SERVICE_RUNNING` and advertise controls it accepts

Practical implication:
- `ServiceMain` entry does not yet prove the handler exists
- handler registration does not yet prove controls are accepted
- `SERVICE_RUNNING` state is SCM-visible status posture, not automatically proof that the first worker-owned consumer has already been reduced
- a visible `SetServiceStatus(...SERVICE_RUNNING...)` call is therefore weaker than a proved worker/task/callback path

### 3. Handler invocation is still weaker than worker handoff truth
From `Service Control Handler Function` and `Service State Transitions`:
- the handler executes in the context of the control dispatcher
- the handler must return within 30 seconds or the SCM returns an error
- lengthy processing should move to a secondary thread; for Vista and later, Microsoft explicitly recommends using a thread-pool worker
- when handling stop or similar controls, the handler should usually set a pending state and return, with the real work completing later

Practical implication:
- handler entry is often a reduction boundary, not the behavior-owning consumer
- in stop/pause/reconfigure flows, the practical next target is usually the retained task object, queue insertion, secondary thread, or thread-pool callback created because the handler must return quickly
- this is strong source-backed support for separating **control-handler invocation** from **worker handoff** and from **first worker-owned consumer**

### 4. SCM-visible state transitions are not consumer truth
From `Service State Transitions` and `SetServiceStatus`:
- the SCM only knows service state through `SetServiceStatus`
- pending states and accepted-controls posture determine how the SCM interacts with the service
- services can update status from any thread to reflect state changes
- `SERVICE_STOPPED` is terminal for practical analysis: cleanup should be complete and no further work should be assumed after that status is reported

Practical implication:
- SCM-visible state is one interaction contract, not automatic proof of behavior ownership
- status updates can be real yet still sit earlier than the decisive worker-owned consumer
- one `STOP_PENDING` or `RUNNING` report is therefore weaker than proving which task/thread/callback actually carries the target behavior

### 5. The useful practical ladder is narrower than “service logic”
A source-backed operator ladder that now deserves to live canonically is:

```text
dispatcher connected
  != ServiceMain entered
  != handler registered / accepted-controls truth
  != control-handler invocation
  != worker handoff / retained task truth
  != first worker-owned consumer
  != later effect
```

This is the real value of the source pass.
It gives reversers a disciplined way to avoid stopping at service shell visibility.

## KB-facing synthesis
The existing native service/worker note was directionally right, but it needed a sharper Windows-heavy middle ladder.

The official docs now justify preserving three smaller operator rules in the KB:
1. SCM-visible service posture is not worker-owned consumer truth.
2. Handler invocation is not the same thing as the worker handoff that long-lived or consequence-bearing work actually uses.
3. `SERVICE_STOPPED` should be treated as a terminal status boundary, not as an invitation to keep attributing later work to the same live service path.

## Best KB contribution from this run
Materially extend the canonical native service/worker workflow note and synchronize the native parent pages so they preserve:
- dispatcher connection truth
- `ServiceMain` entry
- handler registration / accepted-controls truth
- handler invocation
- worker handoff / retained task truth
- first worker-owned consumer truth
- later effect

without collapsing those into one vague “service path is visible” story.
