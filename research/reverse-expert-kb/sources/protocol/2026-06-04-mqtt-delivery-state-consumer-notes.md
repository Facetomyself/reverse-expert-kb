# 2026-06-04 — MQTT delivery-state to application consumer notes

## Source anchors

- OASIS MQTT Version 5.0 — https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
- OASIS MQTT Version 3.1.1 — https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html
- Eclipse Mosquitto `handle_publish.c` — https://github.com/eclipse-mosquitto/mosquitto/blob/d0152406/src/handle_publish.c
- Wireshark MQTT dissector — https://github.com/wireshark/wireshark/blob/master/epan/dissectors/packet-mqtt.c

## Findings worth preserving

### MQTT is a broker-mediated application-message protocol, not just visible packets

OASIS MQTT 5.0 defines an Application Message as payload data plus QoS, Properties, and Topic Name when transported by MQTT. It defines a Subscription as a Topic Filter plus maximum QoS, associated with a Session. The Server accepts Application Messages, processes Subscribe/Unsubscribe requests, and forwards messages that match Client Subscriptions.

Reverse implication: a captured `PUBLISH` frame is usually only message-on-wire truth. It does not by itself prove subscription match truth, broker acceptance, queued delivery truth, retained-message replay truth, or application callback/state consumer truth.

### Packet Identifier is a per-session lifecycle object

MQTT 5.0 requires non-zero, currently unused Packet Identifiers for new `SUBSCRIBE`, `UNSUBSCRIBE`, or QoS>0 `PUBLISH` packets. A Packet Identifier becomes reusable only after the corresponding acknowledgement flow completes: `PUBACK` for QoS 1, `PUBCOMP` or a QoS-2-ending `PUBREC` reason code for QoS 2, and `SUBACK`/`UNSUBACK` for subscribe operations. Identifiers are independently assigned by Client and Server.

Reverse implication: a repeated `Packet Identifier` is not automatically a duplicate application event. It can be retransmission, reuse after acknowledgement, independent client/server namespace collision, or a new application message after the lifecycle is complete.

### QoS handshakes are delivery-progression evidence, not application-consumer evidence

MQTT 3.1.1 and 5.0 split `PUBLISH`, `PUBACK`, `PUBREC`, `PUBREL`, and `PUBCOMP` into explicit QoS flows. MQTT 5.0 also states that when a client reconnects with Clean Start 0 and a session is present, both Client and Server must resend unacknowledged QoS>0 `PUBLISH` and `PUBREL` packets with original Packet Identifiers, and that this is the only circumstance where resend is required.

Reverse implication: QoS 1/2 acknowledgement progress proves protocol-side progression, but it is still earlier than application callback, state reducer, device command, or durable effect. Retransmission after reconnect can make a real packet appear again without proving a second application-owned consequence.

### Retained messages are state-replay artifacts, not fresh publisher events

MQTT 5.0 says a retained `PUBLISH` sent from Client to Server replaces the existing retained message for that topic; zero-byte retained payload removes it. New non-shared subscriptions receive matching retained messages according to Retain Handling. Retain As Published controls whether forwarded messages keep the original RETAIN flag. MQTT 3.1.1 also states retained messages do not form part of Session state and must not be deleted when Session ends.

Reverse implication: if an analyst sees a `PUBLISH` immediately after subscribing, the right first question is whether it is retained replay, live publisher traffic, or a session-queued delivery. Treating retained state replay as current sensor/device behavior is a common false proof.

### Subscription options and MQTT 5 properties can hide the real boundary

MQTT 5.0 adds subscription options such as No Local, Retain As Published, and Retain Handling, and properties such as Subscription Identifier, Topic Alias, Response Topic, Correlation Data, Content Type, Message Expiry, and Session Expiry. Wireshark's dissector preserves these as explicit protocol fields/properties.

Reverse implication: a topic string and payload are sometimes insufficient for replay or attribution. The behavior-bearing object may be a subscription option, session property, response/correlation field, topic alias mapping, expiry rule, or subscription identifier rather than the payload bytes alone.

### Broker implementation code shows the split between parse, ACL, store, queue, acknowledgement, and later client delivery

Mosquitto `handle_publish.c` parses fixed-header flags, QoS, RETAIN, topic, Packet Identifier, properties, Topic Alias, payload, ACL, and then calls `handle__accepted_publish`. In accepted handling it calls plugin message-in hooks, detects stored duplicate/mid reuse cases, stores messages, queues matching subscriptions via `sub__messages_queue`, sends `PUBACK` or `PUBREC`, and writes queued messages.

Reverse implication: even inside one broker implementation, publish handling is not one event. The proof ladder is parse -> authorization/plugin acceptance -> store/deduplicate/expiry -> subscription queue -> QoS acknowledgement -> outbound delivery -> client-side application consumer.

## Compact workflow split

```text
PUBLISH captured != broker accepted != subscription/session matched != queued/delivered != ack lifecycle complete != callback/application state consumed
```

A narrower retained/session variant:

```text
topic/payload visible != live publisher event != retained/session replay classified != fresh application consequence proved
```

## Evidence row shape

For MQTT-shaped protocol cases, preserve at least:

```text
client_id | direction | packet_type | topic/topic_alias | qos | dup | retain | packet_id | properties | subscription_filter/id/options | session_present/expiry | retained/session-queued/live classification | broker accept/ACL/store/queue evidence | ack stage | client callback/handler | first state/effect consumer
```

## Search audit data

Search-layer query used explicit `--source exa,tavily,grok`.

- Sources requested: `exa,tavily,grok`
- Sources succeeded: `exa,tavily`
- Sources failed: `grok` with HTTP 502 from `http://proxy.zhangxuemin.work:8000/v1/chat/completions`
- Exa endpoint observed in prior run/config: `http://158.178.236.241:7860`
- Tavily endpoint observed in prior run/config: `http://proxy.zhangxuemin.work:9874/api`
- Grok endpoint: `http://proxy.zhangxuemin.work:8000/v1/chat/completions`
