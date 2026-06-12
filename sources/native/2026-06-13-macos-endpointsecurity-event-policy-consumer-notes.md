# macOS EndpointSecurity event / policy-consumer source notes — 2026-06-13

## Search context

Search artifact:
- `sources/native/2026-06-13-0450-macos-endpointsecurity-search-layer.json`

Explicit search command used `search-layer --source exa,tavily,grok` with three queries around EndpointSecurity client creation, subscription, event delivery, auth/notify messages, response, cache, mute, and first consumer proof.

Source outcome:
- Exa: usable results
- Tavily: usable results
- Grok: invoked but returned HTTP 502 for all three queries

## Source-backed facts worth preserving

### Apple EndpointSecurity client / subscription model

Apple documentation surfaced by Exa/Tavily shows the core API shape:
- `es_new_client(_:_:)` creates a client instance and connects it to the Endpoint Security subsystem.
- `es_subscribe(...)` subscribes a client to a set of `es_event_type_t` events.
- Subscription is cumulative: subscribing to new event types does not remove previous subscriptions.
- `es_subscriptions(...)` can list the current subscriptions.

Practical implication for reversing:
- A linked EndpointSecurity framework or an `es_new_client` hit is only **client-created** truth.
- `es_subscribe` argument recovery is **event-interest** truth.
- Neither proves that a relevant process/file/network event was delivered, responded to, cached, muted, logged, or consumed by policy state.

### Apple EndpointSecurity message model

Apple documentation summaries surfaced by search state that:
- `es_message_t` contains an event monitored by EndpointSecurity and an action to perform.
- The event is a union of event-specific structures.
- EndpointSecurity sends a message to subscribed clients for monitored event types.
- The handler receives an `es_message_t` pointer and decides how to respond.

Practical implication:
- `es_message_t` presence is **delivered-message** truth only when tied to a live handler entry and matching event type.
- Event fields such as process, file, target, or auth action are evidence for the observed system event, but not proof that the target app's policy reducer or enforcement/hunting output consumed the message.

### AUTH / NOTIFY split and response deadlines

The Rust `endpoint-sec` wrapper documentation, reflecting the EndpointSecurity API shape, preserves useful operational details:
- AUTH messages must be responded to before their deadline; otherwise the client may be killed for slowing the OS.
- Messages expose the action type: auth vs notify.
- Auth messages include an opaque auth ID used when responding.
- Notify messages describe the result of an action.

The generated bindings also preserve comments around `es_respond_auth_result(...)`:
- it responds to an auth event with an allow/deny-style result;
- the `cache` argument can cache the result for some event types;
- a cache hit may suppress future AUTH event production while NOTIFY may still be produced;
- some events require flags responses rather than ordinary auth-result responses.

Practical implication:
- AUTH handler entry is not enough; freeze whether `es_respond_auth_result(...)` / flags response was called, with which result, and whether cache semantics can make later missing AUTH events non-evidence.
- NOTIFY events are usually observation/log/reducer truth, not enforcement truth, unless a later consumer takes action.

### Mute / cache / drop-shaped false stops

Search surfaced Apple API symbols for process/path muting, muted-path/process listing, and unmute functions, plus cache-clearing/result APIs.

Practical implication:
- Missing EndpointSecurity handler hits can be caused by subscription mismatch, muting, cache hits for AUTH events, entitlement/TCC/client failure, event-type availability, or handler deadline/drop behavior.
- A compare run must separate **event did not occur**, **client was not eligible/subscribed**, **event was muted/cached**, **message was delivered but dropped/late**, and **handler consumed it but no downstream policy effect happened**.

## Operator synthesis

EndpointSecurity-shaped reverse work should preserve this ladder:

```text
client created
  != subscribed/eligible for this event type
  != kernel generated the relevant event
  != message delivered to this handler
  != AUTH/NOTIFY action classified and responded/logged
  != cache/mute/deadline behavior understood
  != policy reducer / alert / enforcement consumer/effect owned
```

The compact branch-memory split is:

```text
client != subscribed != event-generated != delivered != responded/logged != policy-consumed/effected
```

Use this seam when `es_new_client`, `es_subscribe`, `es_handler_block_t`, `es_message_t`, `es_respond_auth_result`, `es_respond_flags_result`, `es_mute_*`, or EndpointSecurity event enums are visible, but the real proof object is whether one delivered macOS security event drove a target-owned policy/enforcement/telemetry consumer.

## Sources

Primary / higher-authority:
- Apple Developer Documentation, `es_new_client(_:_:)` — https://developer.apple.com/documentation/endpointsecurity/es_new_client(_:_:)
- Apple Developer Documentation, `es_message_t` — https://developer.apple.com/documentation/endpointsecurity/es_message_t
- Apple Developer Documentation, `Message` — https://developer.apple.com/documentation/endpointsecurity/message
- Apple Developer video, `Build an Endpoint Security app` (WWDC20) — https://developer.apple.com/videos/play/wwdc2020/10159/

Implementation-shape / lower-authority but useful:
- Rust `endpoint-sec` `Message` docs — https://docs.rs/endpoint-sec/latest/endpoint_sec/struct.Message.html
- Rust `endpoint-sec-sys` generated bindings / comments for `ESClient.h` — https://docs.rs/endpoint-sec-sys/latest/src/endpoint_sec_sys/client.rs.html
