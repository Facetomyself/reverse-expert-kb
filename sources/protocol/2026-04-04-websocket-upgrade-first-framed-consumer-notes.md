# 2026-04-04 WebSocket upgrade -> first framed consumer notes

Date: 2026-04-04 21:21 Asia/Shanghai / 2026-04-04 13:21 UTC
Theme: keep opening-handshake truth separate from first framed-consumer truth.

## Why this note was retained
The protocol branch already had broad replay, contract, and state-gate notes.
What it still lacked was a thinner continuation for a very common WebSocket mistake:
- the analyst proves or sees a successful Upgrade
- then stops as if framed protocol ownership were already explained

This note keeps the first real framed consumer as the target.

## Primary retained references
### 1. RFC 6455
Source:
- RFC 6455 — The WebSocket Protocol
  - https://datatracker.ietf.org/doc/html/rfc6455

Retained points:
- WebSocket begins with an HTTP/1.1 opening handshake
- after the handshake, peers enter the data-framing phase
- communication thereafter is frame-based
- client-to-server frames are masked; server-to-client frames are not

Operator consequence:
- handshake acceptance is weaker than framed consumer ownership
- early framing errors can come from direction/masking misunderstandings rather than broad parser failure

### 2. Practical server-side framing explanation
Source:
- MDN — Writing WebSocket servers
  - https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers

Retained use:
- practical explanation of handshake transition and early framing behavior
- used as a readable implementation-oriented complement to RFC 6455, not as the sole protocol authority

## Practical synthesis retained
This continuation note keeps the following smaller split visible:

```text
Upgrade accepted
  != first frame emitted/received truth
  != first frame parsed/validated truth
  != first framed consumer truth
  != downstream effect ownership
```

The operator move is to ask:
- what first opcode/message-type dispatcher or post-deframing parser actually becomes the first consequence-bearing consumer after the opening handshake?

## Search-layer trace
See:
- `sources/protocol/2026-04-04-2121-websocket-search-layer.txt`

Observed degraded mode:
- Exa: returned results
- Tavily: returned results
- Grok: invoked but returned empty set
