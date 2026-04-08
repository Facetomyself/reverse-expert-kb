# WebSocket upgrade vs first framed consumer notes

Date: 2026-04-08
Branch target: protocol practical workflows / WebSocket continuation
Purpose: preserve a source-backed operator refinement for cases where the WebSocket opening handshake is already visible but the first framed parser/dispatcher/consumer is still ambiguous.

## Research intent
Strengthen the existing WebSocket workflow note with a sharper separation between:
- successful Upgrade / open truth
- first framed traffic truth
- first behavior-changing framed consumer truth

## Search artifact
Raw multi-source search artifact:
- `sources/protocol/2026-04-08-0852-ws-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Exa returned usable RFC/MDN/library surfaces
- Tavily returned usable RFC/MDN/library surfaces
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` through the configured proxy path

## Retained sources
1. RFC 6455 — The WebSocket Protocol
   - opening handshake, framing, masking, and message model
2. MDN Web Docs — WebSocket `open` / `message` event surfaces
   - client-visible separation between successful connection establishment and later message delivery
3. libwebsockets callback surfaces
   - receive-callback and callback-family boundaries useful for practical consumer localization

## High-signal retained findings

### 1. RFC 6455 already keeps handshake success and framed traffic as separate proof objects
The RFC separates:
- opening handshake success
- framed data exchange after the protocol switch
- masking/unmasking and message framing rules

Practical consequence:
- `101 Switching Protocols` is route/transport truth, not application-owned framed-consumer truth
- the first trustworthy next object often lives after deframing/unmasking, not at the upgrade boundary

### 2. Browser/client `open` surfaces are weaker than message-bearing surfaces
MDN’s WebSocket surfaces preserve a clear split between:
- `open`
- later `message` events

Practical consequence:
- a client-side “connected” or `onopen` signal is weaker than the first application payload-bearing event
- do not stop at connection establishment when the real question is which framed payload first changes behavior

### 3. Library receive callbacks are still weaker than the first behavior-changing framed consumer
Framework/library surfaces such as libwebsockets expose receive callbacks and frame-adjacent delivery boundaries.

Practical consequence:
- a receive callback can be the right reduction boundary
- but it is still weaker than the first parser/dispatcher/reducer that actually predicts later behavior if callback visibility alone does not answer the case question

## Practical synthesis worth preserving canonically
A compact stop-rule ladder for this seam is:

```text
Upgrade accepted
  != first framed traffic
  != receive callback visibility
  != first behavior-changing framed consumer
```

This keeps four different successes separate:
1. **Upgrade accepted**
   - opening handshake succeeded
2. **first framed traffic**
   - frames are now actually flowing and visible
3. **receive callback visibility**
   - one framework/library callback sees framed payloads
4. **first behavior-changing framed consumer**
   - one parser/dispatcher/reducer actually predicts later behavior

## Best KB use of this material
This material is best used to sharpen the existing WebSocket workflow note.
It should not become a broad WebSocket protocol page.

The operator-facing value is:
- do not stop at `101 Switching Protocols`
- do not stop at `onopen`
- do not stop at raw receive-callback visibility when the real question is still consumer ownership
- stop only when one framed parser/dispatcher/consumer predicts later behavior strongly enough to guide the next move

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source result set.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked; its failure is recorded clearly.
