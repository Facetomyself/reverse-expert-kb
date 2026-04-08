# Protocol WebSocket Upgrade to First Framed Consumer Workflow Note

Topic class: workflow note
Ontology layers: workflow/sensemaking, protocol practical branch, handshake boundary, framed-consumer recovery
Maturity: emerging
Related pages:
- topics/protocol-firmware-practical-subtree-guide.md
- topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/protocol-content-pipeline-recovery-workflow-note.md
Related source notes:
- sources/protocol/2026-04-04-websocket-upgrade-first-framed-consumer-notes.md

## 1. What this workflow note is for
This note covers a recurring protocol case where the analyst has already reduced the target into a WebSocket-shaped connection, but the remaining bottleneck is narrower than broad HTTP or replay-fixture work.

Typical symptoms:
- the HTTP Upgrade / opening handshake is already visible and plausibly understood
- one accepted `101 Switching Protocols` response or browser/client success signal tempts the analyst to stop too early
- the real uncertainty is not “did the handshake work?” but “which first framed consumer actually owns later behavior?”

The goal is to move from:

```text
one successful opening handshake / upgraded connection
```

to:

```text
one proved chain from handshake acceptance
into first frame emission / receipt
into one first framed consumer
and one downstream effect
```

## 2. When to use this note
Use this note when most of the following are true:
- the family is already clearly WebSocket-shaped
- opening handshake truth is mostly settled
- the main uncertainty is where framed behavior actually becomes meaningful after the Upgrade boundary
- one narrow proof against one early frame family would collapse a lot of uncertainty

Common shapes include:
- browser/client code where the Upgrade completes but the analyst still does not know which first message matters
- server-side reversing where handshake acceptance is visible but the first application-owned frame parser/dispatcher is not
- replay/debugging cases where HTTP correctness is already good enough, but framed payload ownership is still folklore

Do **not** use this as the primary note when:
- the opening handshake itself is still uncertain or failing for unclear reasons
- the case is better described as generic framed-binary or stream parsing rather than specifically WebSocket
- the real bottleneck is later application semantics after one first framed consumer is already known

## 3. Core claim
For WebSocket cases, **opening handshake success is weaker than proving the first frame-owned consumer**.

The wrong stopping point is often:

```text
HTTP Upgrade accepted == meaningful protocol ownership proved
```

The better question is:

```text
Which first frame or frame family actually becomes the first consequence-bearing consumer
after the handshake boundary?
```

## 4. Boundary objects to keep separate
### A. Opening-handshake truth
From RFC 6455:
- the protocol begins with an HTTP/1.1 Upgrade handshake
- after both peers send/receive the handshake, the data transfer phase begins

What to capture here:
- one request/response pair
- one accepted Upgrade boundary
- one connection identity

This is weaker than framed consumer truth.

### B. Frame-boundary truth
From RFC 6455:
- after the handshake, communication is via frames
- frame structure includes FIN/opcode/length and masking rules
- clients mask frames sent to servers; servers do not mask frames sent to clients

What to capture here:
- one earliest frame direction
- one opcode / payload shape family
- one masking / framing boundary

### C. First framed-consumer truth
This is the first parser/dispatcher/handler that turns framed bytes into meaningful application behavior.

Typical anchors:
- one first opcode dispatcher
- one first JSON / protobuf / custom payload parse
- one state transition driven by the first accepted frame
- one routing key / message-type switch that predicts later behavior

### D. Effect truth
This is where the analyst proves the first framed consumer actually matters.

## 5. Default workflow
### Step 1: freeze one upgraded connection, not the whole session family
Do not widen to every socket or channel.
Pick one connection with:
- a clean accepted handshake
- one early frame family with obvious downstream leverage
- one stable direction (client->server or server->client) to start with

### Step 2: separate Upgrade truth from framed-consumer truth
Write the local chain explicitly:
- handshake accepted
- first frame emitted/received
- frame parsed/validated
- first framed consumer
- downstream effect

This prevents stopping at `101 Switching Protocols`.

### Step 3: freeze one earliest frame family
Prefer one earliest recurring frame family with:
- stable opcode / message type
- clear direction
- obvious leverage on session state, auth state, or dispatch

Practical stop rules:
- do not flatten “first frame seen on wire” into “first meaningful consumer”
- do not overread browser API `onopen` / client success callbacks as proof of application-level framed ownership
- do not overread one library/framework receive callback as already-good application ownership if the real question is still which first framed parser/dispatcher/reducer changes behavior

### Step 4: preserve masking / direction truth
From RFC 6455:
- client-to-server frames are masked
- server-to-client frames are not masked

Operator consequence:
- if the earliest frame path looks wrong, check direction/masking assumptions before reopening broader parser doubt

### Step 5: prove one first framed consumer
Among candidate consumers, prefer the one that:
- predicts later behavior better than the handshake alone
- turns framed payload bytes into one state/dispatch decision
- survives compare-runs better than raw socket write/read visibility

### Step 6: use one narrow runtime move
Typical minimal proofs include:
- breakpoint/log on the first opcode/message-type dispatcher after unmasking/deframing
- compare one connection that stops after handshake with one that receives the first real frame
- compare a run that reaches `open` / `101 Switching Protocols` only with one that reaches the first `message` / receive callback carrying application payload
- watch one state variable or consumer queue fed only after the first framed payload is accepted

The aim is not full protocol recovery.
It is one proof that links handshake acceptance to a first consequence-bearing framed consumer.

A compact compare checklist for this seam is now worth keeping explicit:
- did the run only prove **Upgrade accepted**?
- did it prove **first framed traffic** but not yet the first parser/dispatcher that matters?
- did it prove one framework/library **receive callback** but not yet the first behavior-changing consumer?
- did it actually prove the first framed consumer that predicts later behavior?

That checklist helps keep handshake success, frame arrival, receive-callback visibility, and first durable consumer truth separate.

## 6. Practical stop rules this note preserves
- `Upgrade accepted != first framed traffic proved`
- `first framed traffic != first application-owned framed consumer proved`
- `browser/client open callback != first meaningful message consumer`
- `framework/library receive callback != first behavior-changing framed consumer`
- `one parseable frame != downstream effect ownership`

## 7. Sources
See: `sources/protocol/2026-04-04-websocket-upgrade-first-framed-consumer-notes.md`

Primary references:
- https://datatracker.ietf.org/doc/html/rfc6455
- https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers
