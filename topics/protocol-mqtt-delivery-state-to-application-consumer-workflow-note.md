# Protocol MQTT Delivery-State to Application Consumer Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, protocol state/message recovery, broker-mediated delivery, replay/consumer proof
Maturity: practical
Related pages:
- topics/protocol-firmware-practical-subtree-guide.md
- topics/protocol-state-and-message-recovery.md
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/analytic-provenance-and-evidence-management.md
Related source notes:
- sources/protocol/2026-06-04-mqtt-delivery-state-consumer-notes.md

## 1. When to use this note
Use this note when a protocol or firmware case has narrowed into **MQTT-shaped broker-mediated messaging**, but the analyst still cannot tell whether visible traffic became an application-owned state/effect.

Typical entry conditions:
- `CONNECT`, `SUBSCRIBE`, `PUBLISH`, `PUBACK`, `PUBREC`, `PUBREL`, `PUBCOMP`, or retained-message behavior is visible in a trace
- topic names, topic filters, QoS, retain flags, packet identifiers, or MQTT 5 properties are visible enough to hypothesize meaning
- the target may be IoT/firmware, broker-side service code, malware/C2-ish MQTT use, mobile/backend telemetry, or a test harness that talks MQTT
- the current uncertainty is no longer raw packet parsing, but which message instance actually reached the right subscription/session and first application handler

Do **not** use this note when:
- the protocol is only vaguely pub/sub-shaped and MQTT has not been identified
- the main blocker is TLS/session capture or socket-boundary relocation before MQTT frames are visible
- the MQTT chain is already proved and the real task has moved into payload schema recovery, device command semantics, or a downstream parser/state edge

## 2. Core claim
The recurring MQTT reverse-engineering mistake is to stop at:

```text
PUBLISH packet visible == topic/payload understood == subscriber behavior proved
```

That is too early.

The useful proof ladder is:

```text
PUBLISH captured
  -> broker accepted / authorized / parsed the right topic and properties
  -> subscription/session match selected a delivery target
  -> retained/session-queued/live-publisher class was resolved
  -> QoS packet-identifier lifecycle progressed honestly
  -> client library delivered a callback or queued message
  -> first application state/effect consumer ran
```

Compact stop rule:

```text
PUBLISH captured != broker accepted != subscription/session matched != queued/delivered != ack lifecycle complete != callback/application state consumed
```

Retained/session replay variant:

```text
topic/payload visible != live publisher event != retained/session replay classified != fresh application consequence proved
```

## 3. What counts as the right proof object
High-value proof objects:
- one `PUBLISH` instance with topic/topic-alias, QoS, DUP, RETAIN, packet identifier, and relevant MQTT 5 properties frozen
- one broker-side acceptance or rejection fact: ACL/plugin decision, parse success, message store insert, duplicate/mid reuse handling, or retained-store update
- one subscription/session match: topic filter, maximum QoS, subscription identifier, No Local / Retain Handling / Retain As Published posture, session present/expiry state
- one delivery progression fact: queued outbound message, callback invocation, application handler entry, reducer/state write, device command, or downstream effect
- one lifecycle classification: live publisher event, retained replay, queued session delivery, retransmission after reconnect, duplicate delivery, or identifier reuse after acknowledgement

Useful but often too early by themselves:
- topic strings and payload bytes in Wireshark
- a `PUBACK`, `PUBREC`, `PUBREL`, or `PUBCOMP` sequence without client-side handler proof
- a retained flag without knowing whether the current subscriber saw retained replay or live publisher traffic
- a Packet Identifier match without knowing whether the identifier is still in-flight, retransmitted, or legitimately reused
- a successful `SUBACK` without proving that the matched message crossed into the application consumer

## 4. Default workflow

### Step 1: Freeze direction and role before interpreting payload
Write down the role split first:

```text
publisher client -> broker
broker -> subscriber client
client library -> application callback / queue
```

Then freeze:
- client identifier if available
- direction of each frame
- broker endpoint / listener / bridge if visible
- clean start / session present / session expiry posture if available
- subscription filter and subscription options if available

This prevents the wire frame from being mistaken for the application event.

### Step 2: Classify the visible `PUBLISH`
For the `PUBLISH` under analysis, record:
- topic name or topic alias resolution
- QoS
- DUP flag
- RETAIN flag
- Packet Identifier if QoS > 0
- message expiry / response topic / correlation data / content type / subscription identifier / user properties when MQTT 5 is in play
- payload length and payload classifier, not only decoded text

Then label the candidate message class:
- live publisher traffic
- retained replay on subscribe
- queued session delivery
- reconnect retransmission
- duplicate delivery
- new message using a reused Packet Identifier after the previous lifecycle completed

If the class is uncertain, do not narrate a fresh state update yet.

### Step 3: Treat broker acceptance as a separate boundary
A broker may parse a frame yet reject or transform it before application-visible delivery.

Look for:
- protocol-valid parse of topic/QoS/properties
- ACL or plugin acceptance/rejection
- retained-message replacement/removal
- message expiry handling
- quota/receive-maximum handling
- duplicate or Packet Identifier reuse handling
- subscription queueing or no-matching-subscriber result

Broker acceptance answers “the broker treated this as a usable MQTT message.”
It still does not prove the subscriber application consumed it.

### Step 4: Prove subscription/session match before proving behavior
Subscription proof should preserve:
- topic filter and wildcard match
- maximum QoS / granted QoS
- MQTT 5 subscription identifier if present
- No Local if publisher and subscriber ClientID may overlap
- Retain Handling and Retain As Published if retained-state interpretation matters
- session present / session expiry / queued messages if reconnect or offline delivery matters

The false inference to avoid:

```text
SUBACK exists + later PUBLISH visible == this subscriber handler consumed this message
```

The more honest claim is:

```text
subscription admitted -> message matched subscription/session -> delivery crossed into client callback/queue -> handler consumed it
```

### Step 5: Use QoS as lifecycle evidence, not final consumer proof
QoS 1 and QoS 2 handshakes are important, but they answer delivery-protocol questions, not application-state questions by themselves.

Keep these separate:
- QoS 1 `PUBLISH -> PUBACK`
- QoS 2 `PUBLISH -> PUBREC -> PUBREL -> PUBCOMP`
- retransmission after reconnect with original Packet Identifier
- Packet Identifier reuse after the acknowledgement lifecycle has completed
- callback/handler/state effect

A QoS 2 completed handshake can still be too early if the question is “did the device/app state change?”

### Step 6: Prove one first application consumer
Stop only when one concrete consumer is visible, such as:
- MQTT client-library callback entry with the matched message object
- application queue/dequeuer consuming the message
- state reducer / mode flag / command dispatcher selected by topic + payload
- device actuator, RPC reply, database update, or downstream request caused by this message

If only the broker-side chain is visible, record it as broker-delivery truth and mark application-consumer proof unresolved.

## 5. Practical scenario patterns

### Scenario A: Retained state is mistaken for fresh device behavior
Pattern:

```text
SUBSCRIBE observed
  -> immediate PUBLISH with RETAIN=1 observed
  -> analyst claims a fresh sensor/device event
```

Better workflow:

```text
SUBSCRIBE options and retain handling
  -> retained-store replay classified
  -> payload mapped as last-known state
  -> first app handler or state reducer proved
  -> only then decide whether fresh behavior exists elsewhere
```

### Scenario B: Packet Identifier reuse is mistaken for duplicate application execution
Pattern:

```text
same Packet Identifier appears twice
  -> analyst claims duplicate command execution
```

Better workflow:

```text
identifier namespace and direction
  -> ack lifecycle state
  -> retransmission vs legal reuse classified
  -> callback / reducer hit counted once or twice with evidence
```

### Scenario C: QoS 2 is treated as “exactly once app effect”
Pattern:

```text
PUBLISH/PUBREC/PUBREL/PUBCOMP complete
  -> analyst claims exactly one durable device effect
```

Better workflow:

```text
QoS 2 protocol lifecycle complete
  -> subscriber delivery/callback proof
  -> app idempotence / reducer / command handler proof
  -> durable effect count
```

### Scenario D: Topic strings are understood but MQTT 5 properties own the behavior
Pattern:

```text
topic and payload look identical across runs
  -> one run behaves differently
```

Check:
- Subscription Identifier
- Response Topic / Correlation Data
- Topic Alias resolution
- Message Expiry / Session Expiry
- No Local / Retain Handling / Retain As Published
- User Properties or Content Type used by app code

If these differ, the “same payload” claim is not the same protocol object.

## 6. Evidence row

Use a row like:

```text
client_id | direction | packet_type | topic/topic_alias | qos | dup | retain | packet_id | properties | subscription_filter/id/options | session_present/expiry | retained/session-queued/live classification | broker accept/ACL/store/queue evidence | ack stage | client callback/handler | first state/effect consumer
```

## 7. Handoff rules

After the MQTT delivery-state chain is frozen:
- route to `protocol-parser-to-state-edge-localization-workflow-note.md` if the payload parser/reducer now owns the uncertainty
- route to `protocol-replay-precondition-and-state-gate-workflow-note.md` if a replayed message is structurally valid but not accepted under current session/broker state
- route to `protocol-pending-request-correlation-and-async-reply-workflow-note.md` if `Response Topic`, `Correlation Data`, or app-level request/reply ownership is the next bottleneck
- route to payload schema or layer-peeling work if MQTT is only the transport shell around a private binary/JSON/protobuf contract

Do not keep deepening MQTT protocol mechanics once one delivery-state chain is already good enough and the next proof object has moved into app payload semantics.

## 8. Sources

See: `sources/protocol/2026-06-04-mqtt-delivery-state-consumer-notes.md`.
