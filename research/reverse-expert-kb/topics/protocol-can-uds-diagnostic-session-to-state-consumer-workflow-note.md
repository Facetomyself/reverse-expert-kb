# CAN / UDS Diagnostic Session to State Consumer Workflow Note

Topic class: workflow note
Ontology layers: protocol / firmware practical branch, automotive diagnostics, request/response contract proof, state/precondition proof
Maturity: draft-practical
Related pages:
- topics/protocol-firmware-practical-subtree-guide.md
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-state-and-message-recovery.md
- topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md
- topics/protocol-layer-peeling-and-contract-recovery-workflow-note.md
- topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md
- topics/protocol-ingress-ownership-and-receive-path-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/protocol-reply-emission-and-transport-handoff-workflow-note.md
- topics/peripheral-mmio-effect-proof-workflow-note.md

## 1. Problem shape

Use this note when a target is automotive-diagnostic / UDS-shaped and the analyst can see some mixture of:

- CAN arbitration IDs that look like diagnostic request/response pairs
- ISO-TP / DoCAN segmented diagnostic payloads
- UDS service identifiers such as `0x10`, `0x22`, `0x27`, `0x2E`, `0x2F`, `0x31`, `0x34`, `0x36`, `0x3E`
- positive responses such as `0x50`, `0x62`, `0x67`, `0x71`
- negative response `0x7F` with NRCs such as response-pending, conditions-not-correct, security denied, wrong session, or request-out-of-range
- session switching, `SecurityAccess`, `TesterPresent`, DID/RID enumeration, routine control, or read/write-data behavior
- an apparent ECU state change, DTC/configuration update, actuator/routine effect, programming transition, or follow-on response

The recurring failure is collapsing all of that into one claim:

> “This diagnostic service changes the ECU state.”

That may be true, but it is not proven by a CAN ID pair, service scan, DID/RID list, seed/key exchange, positive response, or one delayed response alone.

The proof object is narrower:

```text
one UDS request/response exchange, for one ECU endpoint and current session/security posture,
was transported, interpreted, accepted, and consumed by one behavior-bearing ECU state/effect path
```

## 2. Core split

Keep these proof objects separate:

```text
CAN IDs found
  != ISO-TP stream reassembled
  != UDS service/subfunction/DID/RID contract selected
  != diagnostic session/security/keepalive posture valid now
  != request accepted under current preconditions
  != positive/negative/delayed response interpreted correctly
  != ECU state, routine, actuator, DTC, configuration, or flash/update consumer changed
```

Compact branch memory:

```text
ids != reassembled != service-contract != session/security-live != accepted/responded != state-consumed
```

Useful stopping points are usually one of:

- a `0x22` / DID value is tied to one real ECU state source or firmware state field, not only an identifier list
- a `0x2E` / `0x2F` / `0x31` request is tied to one configuration write, IO-control consumer, routine handler, or actuator/test effect
- a `0x27` unlock is tied to one accepted protected operation under a maintained session/security window
- a `0x34` / `0x36` / `0x37` programming sequence is tied to one flash/update-state consumer, not merely a positive response
- a negative response or no-response case is explained by one current precondition, suppression, delay, gateway, transport, session, or security reason

## 3. Workflow

### Step 1 — Freeze the diagnostic endpoint and transport context

Record:

- bus / channel / gateway path
- 11-bit vs 29-bit IDs when known
- request arbitration ID and response arbitration ID
- physical vs functional addressing assumptions
- ISO-TP addressing mode, first-frame / consecutive-frame / flow-control behavior, block size, STmin, timeout posture
- capture surface: SocketCAN, CANedge/CAN logger, PCAN, Vector, J2534, gateway logs, embedded traces, or firmware hooks

Do not start with service semantics if the endpoint contract is still vague.

Stop rule:

```text
CAN frame seen != request/response pair selected != ISO-TP payload faithfully reassembled
```

### Step 2 — Select one UDS service contract

Freeze one request family:

- service ID
- subfunction when present
- DID / RID / memory address / data format identifier / block sequence counter when relevant
- suppress-positive-response bit posture where relevant
- expected positive response SID and payload shape
- expected negative-response interpretation

Treat service scans as contract selectors. They are not yet ECU behavior proof.

Examples:

- `0x10` DiagnosticSessionControl -> session selector, not proof that protected state changed durably
- `0x22` ReadDataByIdentifier -> DID selector, not proof of field semantics
- `0x27` SecurityAccess -> seed/key handshake selector, not proof that the next protected consumer accepted the request
- `0x31` RoutineControl -> routine selector, not proof that the routine finished or changed state

### Step 3 — Freeze session, security, and keepalive truth at request time

Before interpreting acceptance or rejection, record:

- current diagnostic session
- whether the session can expire or revert
- security level / unlock state
- seed/key level and whether the seed is fresh for this ECU/session
- `TesterPresent` cadence and suppress-positive-response posture
- recent resets, power cycles, gateway reconnects, bus-off events, or ECU sleeps
- whether the request is physical or functional and whether positive responses can be suppressed

Stop rule:

```text
session switch accepted != security level live != keepalive maintained != protected request accepted now
```

A common compare pair is:

- same request immediately after unlock vs after keepalive expiry
- same request in default vs extended/programming session
- same DID/RID with and without required precondition
- same request with positive-response suppression off vs on

### Step 4 — Interpret positive, negative, delayed, and absent responses conservatively

Do not overread one response byte.

Preserve:

- positive response SID and echoed subfunction / DID / RID material
- negative response SID `0x7F`, original service, and NRC
- response-pending / delayed-positive behavior
- timeout window and ECU busy state
- suppressed-positive-response cases
- transport failure vs application-layer rejection
- gateway routing or functional-addressing fanout

Stop rule:

```text
no positive response != service failed
positive response != effect consumed
0x78 response-pending != final rejection
NRC seen != exact root cause without current precondition proof
```

### Step 5 — Cross into the ECU-side parser / dispatcher / service handler

If firmware or ECU simulation is available, locate:

- ISO-TP receive completion
- UDS message dispatcher
- SID table / handler switch
- subfunction / DID / RID dispatch
- session/security/precondition checks
- negative-response construction
- positive-response construction
- state write, routine enqueue, actuator command, DTC/config update, flash/update state transition, or reply emitter

If firmware is not available, use compare evidence:

- controlled state change before/after one request
- changed DID value after one independent stimulus
- routine output correlated with actuator/test effect in a safe lab setting
- negative-response changes after one specific precondition is satisfied
- keepalive expiry causes protected operation rejection while endpoint/service still responds

### Step 6 — Prove the first state/effect consumer

The first consumer may be:

- a firmware state field backing a DID
- a configuration / NVM write path
- a DTC status update or clear path
- a routine worker / job queue
- an IO-control or actuator path in a safe bench environment
- a bootloader/programming-state transition
- a flash erase/write/verify state machine
- a gateway route or backend/cloud diagnostic handoff
- a follow-on ECU message or bus-level state consequence

Stop only after one consequence-bearing edge is tied to the selected request/response exchange.

Good evidence shapes:

- request payload -> SID/subfunction handler -> session/security check -> state write -> positive response
- request accepted -> routine worker queued -> completion/status DID changes predictably
- incorrect precondition -> specific NRC; corrected precondition -> same service reaches consumer
- `TesterPresent` disabled -> session expiry -> protected service rejection; enabled -> protected service reaches same consumer
- positive response seen but downstream state unchanged -> report response proof only, not state proof

## 4. Observation surfaces

### CAN / transport capture surfaces

Use for:

- request/response IDs
- ISO-TP segmentation and timing
- delayed / absent / suppressed response diagnosis
- gateway and addressing hypotheses

Do not use alone for:

- DID semantics
- session/security live truth beyond observable responses
- ECU state/effect ownership

### Diagnostic tooling surfaces

Tools such as Caring Caribou, HydraScope, udsoncan scripts, Scapy, or OEM tools are useful for:

- endpoint discovery
- service/subservice/DID/RID enumeration
- controlled request construction
- repeated compare runs
- seed collection or session/keepalive observation in authorized lab contexts

Do not treat a scan result as a consumer proof. Scans describe what the ECU answered under one timing/session/security posture.

### Firmware / ECU simulation surfaces

Use for:

- SID dispatcher localization
- session/security/precondition checks
- handler ownership
- positive/negative response construction
- first state/effect consumer

Do not use alone for:

- current vehicle/gateway transport truth unless the same endpoint/path is reproduced
- safety-critical behavior claims outside a controlled bench or simulation environment

## 5. Common false stops

### False stop A — “The service is supported”

Service support only says a request family answered under current conditions.

Ask next:

- in which session/security posture?
- under which addressing mode?
- with which DID/RID/subfunction?
- did the handler reach a state consumer or only a response stub?

### False stop B — “SecurityAccess succeeded”

SecurityAccess unlocks a level; it does not prove the protected operation reached the intended consumer.

Ask next:

- which level?
- is it still live?
- which service/subfunction/DID/RID did it unlock?
- did the next protected request actually pass checks and change state?

### False stop C — “Positive response means effect”

A positive response may confirm acceptance, echo a selector, or report routine start. It may not prove completion, persistence, actuator movement, flash write, or downstream behavior.

Ask next:

- is this a start, pending, completion, or status response?
- is a follow-up status/read required?
- what first state/effect proves the consequence?

### False stop D — “No response means unsupported”

No response can mean transport failure, gateway filtering, functional addressing, positive-response suppression, ECU busy, wrong timeout, bus load, sleep state, or session/security expiry.

Ask next:

- was ISO-TP complete?
- was the suppress-positive bit set?
- did negative response `0x78` imply delayed positive response?
- did a gateway or functional-addressing path change response expectations?

## 6. Handoff to other KB pages

- If the diagnostic traffic is not visible or the gateway path is unclear, go to `protocol-capture-failure-and-boundary-relocation-workflow-note.md`.
- If the visible object still mixes transport, wrapping, compression, or proprietary payload semantics, go to `protocol-layer-peeling-and-contract-recovery-workflow-note.md`.
- If a request is structurally plausible but rejected, go to `protocol-replay-precondition-and-state-gate-workflow-note.md`.
- If parser/dispatcher visibility exists but the first state write is unknown, go to `protocol-parser-to-state-edge-localization-workflow-note.md`.
- If the consequence is a peripheral or actuator-side effect, continue into `peripheral-mmio-effect-proof-workflow-note.md` or `isr-and-deferred-worker-consequence-proof-workflow-note.md`.

## 7. Source anchors

Source synthesis:
- `sources/protocol/2026-05-01-can-uds-diagnostic-session-and-state-notes.md`

Search artifact:
- `sources/protocol/2026-05-01-0450-can-uds-diagnostic-state-search-layer.txt`

Key external anchors:
- `udsoncan`, “Introduction to UDS”
- `uds` Python package knowledge base, “Diagnostic Services”
- Dissecto / HydraScope knowledge base, “UDS”
- CSS Electronics, “UDS Explained - A Simple Intro”
- Caring Caribou UDS module documentation
