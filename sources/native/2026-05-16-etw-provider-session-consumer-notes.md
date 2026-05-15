# Source notes — Windows ETW provider / session / consumer proof

Date: 2026-05-16
Scope: source-backed notes for a native/runtime-evidence workflow page about Event Tracing for Windows (ETW) proof boundaries.

## Search artifact

- `sources/native/2026-05-16-0450-etw-provider-session-consumer-search-layer.json`

Search was explicitly run through search-layer with `--source exa,tavily,grok`.

## High-signal sources

### Microsoft Learn — Event Tracing overview

URL: https://learn.microsoft.com/en-us/windows/win32/etw/event-tracing-portal

Useful points:
- ETW is framed around three different roles: starting/stopping trace sessions, instrumenting an application to provide trace events, and consuming trace events.
- Trace events contain an event header and provider-defined data describing state of an application or operation.
- The source split already implies that provider existence, session control, and event consumption are different proof objects.

Reverse-analysis implication:
- A provider GUID or static `EventWrite` callsite is not enough to claim a trace consumer saw or acted on anything.
- Session state, enablement, event emission, delivery, decoding, and downstream consumer behavior need separate evidence.

### Microsoft Learn — Configuring and Starting an Event Tracing Session

URL: https://learn.microsoft.com/en-us/windows/win32/etw/configuring-and-starting-an-event-tracing-session

Useful points:
- A controller configures `EVENT_TRACE_PROPERTIES` and calls `StartTrace` to start a session.
- Providers are enabled into a session with `EnableTrace`, `EnableTraceEx`, or `EnableTraceEx2`.
- `TraceSetInformation` can add extended data and expose provider/session-related information.
- Multiple sessions may enable and receive events from the same provider, so "provider enabled somewhere" is not necessarily "enabled by the consumer/session under analysis."

Reverse-analysis implication:
- Session existence and provider enablement are distinct from provider registration and event write callsites.
- When multiple sessions or controllers exist, bind the specific session handle/name, provider GUID, level/keyword/filter state, and consumer path before claiming ownership.

### Microsoft Learn — EventRegister / TraceLoggingRegisterEx

URLs:
- https://learn.microsoft.com/en-us/windows/win32/api/evntprov/nf-evntprov-eventregister
- https://learn.microsoft.com/en-us/windows/win32/api/traceloggingprovider/nf-traceloggingprovider-traceloggingregisterex

Useful points:
- `EventRegister` registers an ETW provider and returns a handle used to write ETW events.
- `TraceLoggingRegisterEx` registers a TraceLogging provider and can specify an ETW enable callback.
- Registration lifetime and enable callback behavior are separate from individual event writes.

Reverse-analysis implication:
- Static or dynamic registration truth only proves the provider can participate in ETW.
- Enable-callback evidence can show controller/session interaction, but it still does not prove that a specific event was emitted, delivered, decoded, or consumed.

### Microsoft Learn — EventWrite / EnableTraceEx2

URLs:
- https://learn.microsoft.com/en-us/windows/win32/api/evntprov/nf-evntprov-eventwrite
- https://learn.microsoft.com/en-us/windows/win32/api/evntrace/nf-evntrace-enabletraceex2

Useful points:
- `EventWrite` writes an ETW event using the current thread's activity ID.
- `EnableTraceEx2` configures how a provider logs events to a trace session, including enable/disable/capture-state style control and level/keyword/filter selection.

Reverse-analysis implication:
- `EventWrite` call entry is only an attempted emission point; verify return/status and whether enablement/filter posture would actually accept the event.
- Activity ID, provider GUID, event descriptor/id, level, keywords, and payload schema are part of the proof package if correlation matters.

### Microsoft Learn — Consuming Events / OpenTrace / ProcessTrace

URLs:
- https://learn.microsoft.com/en-us/windows/win32/etw/consuming-events
- https://learn.microsoft.com/en-us/windows/win32/api/evntrace/nf-evntrace-opentracea
- https://learn.microsoft.com/en-us/windows/win32/api/evntrace/nf-evntrace-processtrace

Useful points:
- Consumers process events from log files or real-time sessions.
- `EVENT_TRACE_LOGFILE` identifies the log file or real-time session and the `BufferCallback`, `EventCallback`, or `EventRecordCallback` used to process events.
- `OpenTrace` opens a trace processing handle for a real-time session or ETL file.
- `ProcessTrace` delivers events from trace processing sessions to the consumer.

Reverse-analysis implication:
- Delivery to a callback and downstream semantic consumption are separate proof objects.
- An ETL file containing an event is weaker than proving the real-time consumer callback, decoder, rule, or reducer acted on that same event in the target behavior.

## Durable operator split

```text
provider known/registered
  != session started
  != provider enabled for this session with relevant level/keywords/filters
  != event write attempted/accepted
  != event delivered to ETL or real-time consumer callback
  != payload decoded/correlated
  != first consumer-owned effect proved
```

Compact memory:

```text
registered != enabled != written != delivered != decoded != consumed/effected
```
