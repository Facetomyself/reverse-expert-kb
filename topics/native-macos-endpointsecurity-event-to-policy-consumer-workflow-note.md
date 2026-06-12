# macOS EndpointSecurity event to policy-consumer workflow note

Topic class: workflow note
Ontology layers: native desktop/server practical branch, macOS security telemetry, event-consumer proof
Maturity: draft-practical
Related pages:
- topics/native-practical-subtree-guide.md
- topics/native-binary-reversing-baseline.md
- topics/native-macos-servicemanagement-xpc-helper-consumer-workflow-note.md
- topics/native-macos-notificationcenter-to-observer-consumer-workflow-note.md
- topics/kernel-callback-telemetry-to-enforcement-consumer-workflow-note.md
- topics/malware-analysis-overlaps-and-analyst-goals.md
- topics/runtime-evidence-package-and-handoff-workflow-note.md

## Why this matters

macOS EndpointSecurity gives defenders, EDR-style agents, enterprise controls, and sometimes malware-adjacent tooling a high-value stream of process, file, and security events. In reverse work, it is tempting to treat an `EndpointSecurity.framework` import, an `es_new_client(...)` hit, or a recovered `es_event_type_t` list as proof that the target owns a security decision or telemetry effect.

That is usually too strong.

EndpointSecurity cases have several separate proof objects:

```text
client created
  != subscribed/eligible for this event type
  != kernel generated the relevant event
  != message delivered to this handler
  != AUTH/NOTIFY action classified and responded/logged
  != cache/mute/deadline behavior understood
  != policy reducer / alert / enforcement consumer/effect owned
```

Compact branch-memory split:

```text
client != subscribed != event-generated != delivered != responded/logged != policy-consumed/effected
```

The useful reversing output is not “this binary uses EndpointSecurity.” It is one bounded chain from a specific generated event to the first target-owned policy reducer, alert/queue writer, denial/allow response, XPC handoff, rule engine, or persistence/telemetry effect.

## Scope

Use this note when the visible surface includes:
- `EndpointSecurity.framework`
- `es_new_client`, `es_delete_client`
- `es_subscribe`, `es_unsubscribe`, `es_subscriptions`
- `es_handler_block_t` or block/callback wrappers receiving `es_message_t`
- `es_respond_auth_result`, `es_respond_flags_result`
- `es_mute_*`, `es_unmute_*`, `es_clear_cache`
- `ES_EVENT_TYPE_AUTH_*` / `ES_EVENT_TYPE_NOTIFY_*`
- `es_message_t` fields such as process, event type, action, deadline, sequence number, thread, or event-specific unions

This note is mainly about macOS-native event delivery and first consumer proof. It does **not** replace:
- XPC helper proof when the first real consumer is across an `NSXPCConnection` / Mach service boundary;
- malware persistence proof when EndpointSecurity only observes a persistence artifact;
- generic kernel-callback telemetry reduction when the target is not EndpointSecurity-shaped;
- detection-rule handoff when the output is a YARA/Sigma/rule-pack artifact rather than the target app's runtime decision.

## Preconditions

Prefer at least one of these observation surfaces:
- static xrefs to EndpointSecurity symbols and recovered event arrays;
- block/callback recovery around `es_new_client` handler construction;
- dynamic hooks on `es_new_client`, `es_subscribe`, `es_respond_*`, `es_mute_*`, `es_clear_cache`, and handler entry;
- trace/log evidence carrying `event_type`, `seq_num` / `global_seq_num`, process audit token, event-specific file/process fields, and downstream queue/state writes;
- compare runs that can generate or suppress one representative event.

Environment assumptions matter:
- EndpointSecurity requires the right entitlement / system-extension posture / OS support.
- Auth events have deadlines; late or missing responses are a behavior object, not just a trace inconvenience.
- Muting and cache behavior can make later no-hit evidence misleading.

## Investigation frame

- **Target:** a macOS app, daemon, system extension, EDR/security tool, helper, or malware-adjacent monitor using EndpointSecurity.
- **Boundary:** kernel/security-subsystem event generation to user-space handler delivery, then handler to policy reducer / response / telemetry effect.
- **Observation surface:** EndpointSecurity API calls, event subscription arrays, handler block entry, `es_message_t` decode, AUTH response calls, mute/cache calls, downstream queues/XPC/rule engines/loggers.
- **Artifact goal:** one event-owned chain from `event_type + subject/process/file fields` to first consumed policy/enforcement/telemetry effect.
- **Cheapest next discriminant:** hook `es_subscribe` and the handler block first; if the relevant event reaches the handler, hook `es_respond_*` / first downstream queue or reducer. If it does not, check subscription, entitlement/client creation result, muting, cache, and event-generation realism before widening.

## Practical workflow

### 1. Separate client creation from event-interest truth

Freeze:
- where `es_new_client(...)` is called;
- the handler block/function pointer and its retained owner;
- client creation result / failure handling;
- where `es_subscribe(...)` is called and with which event array;
- whether later `es_unsubscribe`, `es_unsubscribe_all`, or `es_delete_client` can retire the client.

Do not treat framework import or client creation as monitoring proof.

A good intermediate output:

```text
client_owner | handler_owner | creation_result | subscribed_events | subscription_time | retire/unsubscribe path
```

### 2. Prove the representative event is generated and eligible

Pick one event family instead of surveying all enums.

For an AUTH case, record:
- event type;
- subject process / target path / file or process fields;
- action kind and deadline;
- whether this event type supports ordinary auth result or flags response;
- whether cache semantics may apply.

For a NOTIFY case, record:
- event type;
- result/action fields;
- process and event-specific payload;
- sequence number / global sequence number if available;
- whether notification order/drop/loss matters for the target logic.

Do not treat an enum in an array as current event proof. Generate or observe one concrete event.

### 3. Confirm handler delivery before claiming policy ownership

At handler entry, capture:

```text
client | event_type | action_type | seq/global_seq | process/audit_token | target fields | deadline | owner object | current queue/thread
```

Then immediately ask: what is the first target-owned consumer?

Common first consumers:
- inline allow/deny decision and `es_respond_auth_result(...)`;
- rule-engine lookup;
- path/process reputation cache;
- XPC handoff to a privileged helper or GUI agent;
- telemetry/log queue;
- alert/notification pipeline;
- suppression/mute/cache management path.

If the handler only decodes and forwards, stop at the forwarding boundary and route to the corresponding IPC/queue/helper note.

### 4. Split AUTH response truth from NOTIFY/logging truth

AUTH path proof should preserve:

```text
handler entered != decision computed != es_respond_* called != response accepted != cached/suppressed future AUTH != downstream policy state updated
```

NOTIFY path proof should preserve:

```text
handler entered != payload decoded != queued/logged != alert/reducer consumed != user/security effect owned
```

A denial/allow call is usually stronger than a log write for enforcement, but still weaker than proving a durable rule update, alert state, XPC consumer, or later behavior if the case asks about those effects.

### 5. Handle mute/cache/deadline as first-class false-stop classes

When handler hits are missing or inconsistent, check:
- event was never generated under the test action;
- client creation/subscription failed;
- relevant event type was not subscribed;
- process/path/event was muted;
- AUTH result was cached, suppressing future AUTH events while NOTIFY may still appear;
- deadline was missed and the client was penalized/killed;
- event-type availability differs by OS version;
- downstream consumer coalesces/deduplicates events.

Do not immediately infer “target ignored this event” from a missing handler hit.

### 6. Produce a small evidence table

For each representative event, prefer:

| Field | Evidence |
|---|---|
| event type | `ES_EVENT_TYPE_AUTH_*` / `NOTIFY_*` and source xref |
| subscription proof | `es_subscribe` caller + event array |
| generation proof | test action / trace / OS event evidence |
| delivery proof | handler entry + sequence/action fields |
| response/log proof | `es_respond_*` / queue/log call |
| mute/cache/deadline state | observed or ruled out |
| first consumer/effect | reducer / XPC / alert / policy state / enforcement |
| false stop ruled out | why import/subscription/handler alone is not the final claim |

## Hook / breakpoint plan

Static:
- recover `es_event_type_t` arrays and event-name wrappers;
- recover block captures around `es_new_client` handler setup;
- locate helpers around `es_respond_auth_result`, `es_respond_flags_result`, mute/unmute, cache clear, and subscription listing;
- find downstream reducers by xrefing decoded event fields, path/process keys, verdict enums, and queue writes.

Dynamic:
- hook `es_new_client` return and handler pointer/block owner;
- hook `es_subscribe` to dump event arrays;
- hook handler entry to capture `event_type`, action type, sequence numbers, process/target fields, and deadline;
- hook `es_respond_auth_result` / `es_respond_flags_result` for result and cache flag;
- hook `es_mute_*` / `es_unmute_*` / `es_clear_cache` when missing events are part of the question;
- hook first downstream queue/XPC/log/reducer write, not just the EndpointSecurity callback.

## Common failure modes

- **Subscription overread:** `es_subscribe` lists an event, but the test never generated that event or the handler never received it.
- **AUTH/NOTIFY flattening:** a NOTIFY log path is mistaken for enforcement, or an AUTH response is mistaken for later policy state consumption.
- **Cache/mute blindness:** missing later AUTH callbacks are read as target behavior even though an earlier cached allow/deny or mute explains the absence.
- **Handler-as-consumer mistake:** handler entry proves delivery, but the behavior-owning reducer is an XPC helper, queue worker, rule engine, or UI/alert pipeline one hop later.
- **Deadline distortion:** slow instrumentation changes AUTH response timing, producing behavior that the target would not show in a clean run.
- **Entitlement/client-state mismatch:** client creation/subscription fails in the analysis environment, but static xrefs are still overread as live event ownership.

## Useful outputs

- EndpointSecurity event-to-consumer evidence table.
- Event subscription map with handler owner and downstream consumer.
- AUTH response proof: event -> decision -> `es_respond_*` -> cache flag -> accepted result.
- NOTIFY telemetry proof: event -> decoded payload -> queue/log/alert -> first reducer/effect.
- Compare-run diagnosis for missing events: generation vs subscription vs mute/cache vs deadline vs downstream consumer.

## Sources / provenance

Source note:
- `sources/native/2026-06-13-macos-endpointsecurity-event-policy-consumer-notes.md`

Search artifact:
- `sources/native/2026-06-13-0450-macos-endpointsecurity-search-layer.json`

Primary sources consulted:
- Apple Developer Documentation, `es_new_client(_:_:)`
- Apple Developer Documentation, `es_message_t`
- Apple Developer Documentation, EndpointSecurity `Message`
- Apple Developer WWDC20, `Build an Endpoint Security app`

Implementation-shape source consulted:
- Rust `endpoint-sec` / `endpoint-sec-sys` documentation and generated bindings for message lifetime, auth deadlines, action fields, subscription, response, cache, and mute API shape.
