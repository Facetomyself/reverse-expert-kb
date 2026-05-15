# Native ETW Provider / Session / Consumer Workflow Note

Topic class: workflow note
Ontology layers: native practical workflow, runtime evidence, telemetry consumer proof
Maturity: draft-practical
Related pages:
- topics/native-practical-subtree-guide.md
- topics/runtime-evidence-practical-subtree-guide.md
- topics/runtime-behavior-recovery.md
- topics/analytic-provenance-and-evidence-management.md
- sources/native/2026-05-16-etw-provider-session-consumer-notes.md

## 1. When to use this note

Use this note when a Windows native target exposes Event Tracing for Windows (ETW) surfaces and the current risk is overreading telemetry evidence.

Common entry signals:
- provider GUIDs, manifests, TraceLogging provider definitions, or WPP/manifest-style event metadata
- `EventRegister`, `EventUnregister`, `TraceLoggingRegister`, `TraceLoggingRegisterEx`, or enable callbacks
- `EventWrite`, `EventWriteTransfer`, `TraceLoggingWrite`, or wrapper macros
- controller paths using `StartTrace`, `ControlTrace`, `EnableTraceEx`, or `EnableTraceEx2`
- consumer paths using `OpenTrace`, `ProcessTrace`, `EventRecordCallback`, ETL processing, or a real-time trace session
- security / EDR / diagnostic components where ETW is visible but it is unclear whether it is only telemetry, a policy input, or a behavior-changing control channel

Do **not** use this note as a generic ETW programming tutorial. The reverse-engineering question is narrower:

> Which ETW boundary is the first truthful proof object: provider registration, session enablement, event emission, delivery to a trace, payload decoding, or a consumer-owned effect?

## 2. Core split

Keep this ladder visible:

```text
provider known / registered
  != session started
  != provider enabled for this session with relevant level / keywords / filters
  != event write attempted or accepted
  != event delivered to ETL or real-time consumer callback
  != payload decoded and correlated
  != first consumer-owned effect proved
```

Compact stop rule:

```text
registered != enabled != written != delivered != decoded != consumed/effected
```

The usual mistake is to collapse all of this into one sentence like “ETW saw it” or “the provider logged it.” That is too coarse for reverse work. A provider may be registered but never enabled, enabled by a different session, filtered out by level/keywords, write an event that is not delivered to the consumer you care about, or deliver a payload that is decoded but not used by any policy/reducer/alert/action path.

## 3. Proof objects

### 3.1 Provider identity / registration truth

What it proves:
- a provider identity exists in the binary or runtime
- the process registered a provider handle or TraceLogging provider
- optional enable callbacks may exist and may be invoked when a controller interacts with the provider

Useful evidence:
- provider GUID / name / manifest / TraceLogging metadata
- `EventRegister(...)` or `TraceLoggingRegisterEx(...)` hit with provider identity
- registration handle lifetime and `EventUnregister(...)`
- enable-callback entry, control code, enable level, match-any / match-all keywords, and filter data

What it does **not** prove:
- that a specific session enabled the provider
- that a specific event write happened
- that a consumer received, decoded, or acted on the event

Stop when:
- you can name the provider identity, registration lifetime, and whether an enable callback gives a stronger route into session-specific evidence.

### 3.2 Session / controller truth

What it proves:
- a trace session was configured and started
- a controller attempted to enable a provider into that session
- level, keyword, and filter posture may explain why some events are included or excluded

Useful evidence:
- `StartTrace(...)` with session name, logger mode, output path / real-time mode, and properties
- `EnableTraceEx2(...)` or related enable APIs with provider GUID, control code, level, keywords, and filter data
- `ControlTrace(...)` stop/query/update paths
- system tooling evidence such as `logman query`, `tracelog`, WPR/WPA configuration, or session inventory when available

What it does **not** prove:
- that the provider emitted the event under analysis
- that the event reached the intended consumer
- that the ETL/session content became a behavior-changing input

Stop when:
- the specific session/controller/provider tuple is bound tightly enough that the next uncertainty is event emission or consumer delivery, not generic “ETW was enabled.”

### 3.3 Event emission truth

What it proves:
- a provider-side event write callsite was reached and attempted to emit one event
- the payload fields, activity ID, related activity ID, event descriptor/id, level, task/opcode, and keywords may be observable

Useful evidence:
- breakpoints/hooks on `EventWrite*`, `TraceLoggingWrite`, WPP helper wrappers, or provider-specific wrappers
- return/status from the write call where practical
- payload buffer and schema correlation
- thread/activity ID correlation with the action being analyzed

What it does **not** prove:
- that the event passed provider/session filters
- that it was delivered to the particular real-time consumer or ETL file
- that a downstream decoder or rule consumed it

Stop when:
- you can package the exact write point and payload, plus whether acceptance/filter state is known or still a gap.

### 3.4 Delivery truth

What it proves:
- an event reached an ETL file or a real-time consumer callback path
- a consumer `OpenTrace(...)` / `ProcessTrace(...)` path delivered an `EVENT_RECORD` / callback-visible event

Useful evidence:
- ETL content containing provider/event/payload with timestamps and activity IDs
- `OpenTrace(...)` bound to the session name or log file under analysis
- `ProcessTrace(...)` delivering into a specific callback
- `EventRecordCallback` / `EventCallback` entry with matching provider GUID, event id, timestamp, process/thread, and activity ID

What it does **not** prove:
- that the payload was decoded correctly
- that the callback’s downstream reducer/action path used this event
- that a stored ETL observation matches a live policy/alert/behavior path

Stop when:
- delivery is tied to the same session/file/consumer path that matters, or explicitly marked as an offline-only observation.

### 3.5 Decode / correlation truth

What it proves:
- a consumer or analyst mapped raw event data into field meaning
- the event can be correlated to a process, thread, activity, request, operation, or state transition

Useful evidence:
- TDH / manifest / TraceLogging schema lookup
- decoded field names, versions, and payload offsets
- activity-id and timestamp correlation against the target action
- consumer-side parser/reducer branch that recognizes the provider/event/field tuple

What it does **not** prove:
- that decoded information changed any later decision
- that the selected correlation is the first behavior-bearing consumer

Stop when:
- the decoded event is bound to one concrete operational question and the next missing proof is one consumer-owned effect.

### 3.6 Consumer-owned effect truth

What it proves:
- a consumer, rule, reducer, alert, state update, or downstream action used the event or decoded fields
- the ETW evidence is not merely logging but part of the behavior under analysis

Useful evidence:
- branch from callback/decoder into a rule, score update, block/allow decision, alert, queue item, database write, UI update, network send, or service action
- before/after compare with the same provider event delivered but a field, filter, or consumer branch changed
- durable side effect tied to the decoded event rather than to nearby non-ETW state

Stop when:
- one first consumer-owned effect is proved, or the handoff package explicitly says the case is only proven to delivery/decode and not yet to effect.

## 4. Practical workflow

1. **Classify the ETW surface.**
   - provider-only, controller/session, event-write, consumer/callback, ETL/offline, or downstream rule/action.

2. **Bind identity before meaning.**
   - freeze provider GUID/name, event descriptor/id, level, keywords, schema version, process/thread, and activity ID if available.

3. **Check session enablement separately from registration.**
   - provider registration says “can emit”; enablement says “this session may receive selected events.”

4. **Treat filters as proof-shaping state.**
   - level, keywords, match-any/match-all, stackwalk, provider filters, and session mode can explain why nearby events are absent.

5. **Separate write attempts from delivery.**
   - `EventWrite` callsite truth is weaker than callback/ETL truth. Package return/status and filter posture if available.

6. **Separate delivery from decode.**
   - one matching event in an ETL or callback is not automatically a semantic field claim. Bind schema and payload parsing.

7. **Separate decode from consumer effect.**
   - a decoded event is evidence. It is not proof that a policy, alert, reducer, or behavior-changing consumer used it.

8. **Produce the smallest honest handoff.**
   - write down the highest proven boundary and the next missing boundary rather than narrating a complete telemetry-to-effect chain you have not shown.

## 5. Compare-run patterns

Useful pairs:
- same provider registration, different session enablement
- same event write callsite, different level/keyword/filter posture
- same event delivered to ETL, no real-time consumer path
- same callback delivery, different schema/field decode
- same decoded event, consumer branch disabled or field changed
- same consumer rule path, one durable side effect present/absent

High-signal interpretation:
- If registration is identical but behavior differs, look at session enablement and filters before blaming provider code.
- If emission is identical but the consumer differs, check delivery path, session/file identity, and callback binding.
- If delivery is identical but behavior differs, check decode/schema version and the first consumer branch/reducer.
- If decode is identical but behavior differs, ETW may only be observational; move to the non-ETW state owner that actually controls the effect.

## 6. Common traps

- Treating a provider GUID in the binary as proof of runtime telemetry.
- Treating registration as proof that a session enabled the provider.
- Treating “provider enabled” as proof that the relevant level/keyword/filter allowed the event.
- Treating `EventWrite(...)` entry as proof of delivery to the consumer under analysis.
- Treating an ETL file event as proof of real-time consumer behavior.
- Treating decoded fields as if they already triggered a rule, score, alert, or state transition.
- Ignoring multi-session cases where a provider is enabled by one controller but the behavior belongs to another consumer.
- Ignoring activity-id / timestamp / process-thread correlation and accidentally attributing a nearby event to the wrong operation.

## 7. Evidence package shape

When this seam matters, package:

- provider identity: GUID/name, manifest/TraceLogging metadata, registration call, handle lifetime
- session identity: session name/handle, logger mode, ETL path or real-time mode, controller process if known
- enablement: API, control code, level, match-any / match-all keywords, filters, stack/capture-state options if relevant
- event write: callsite/wrapper, event id/descriptor, payload bytes/fields, activity ID, return/status, thread/process
- delivery: ETL record or real-time callback, `OpenTrace` / `ProcessTrace` path, timestamp/activity correlation
- decode: schema source, decoded fields, version, parser branch
- consumer effect: first reducer/rule/action/side effect, or an explicit gap if not yet proved

Minimum honest conclusion examples:
- “Provider registered and enable callback fired, but no event-write or consumer delivery proof yet.”
- “Event write and ETL delivery are proven; no live consumer-owned effect is proven.”
- “Real-time callback received and decoded the event; first durable effect is still unproved.”
- “Consumer rule used the decoded field and produced the queue/update/action; ETW is behavior-bearing for this path.”

## 8. Relationship to other branches

Use this note as:
- a native practical branch continuation when Windows telemetry/controller/consumer boundaries are the current liar
- a runtime-evidence continuation when a trace event is real but its evidentiary status is being overread
- a malware-analysis support seam when ETW appears in EDR, telemetry, loader, process, image, or threat-intel paths and the question is whether the event is merely observed or actually consumed

Do not let this page replace:
- generic hook-placement choice when ETW is only one candidate observation surface
- malware detection-rule handoff when the main missing object is YARA/Sigma/deployment packaging rather than ETW delivery
- protocol or service-contract recovery when the event payload merely hints at a separate API/message owner
