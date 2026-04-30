# CAN / UDS diagnostic-session and state-consumer notes — 2026-05-01

Source class: external research synthesis
Search artifact: `sources/protocol/2026-05-01-0450-can-uds-diagnostic-state-search-layer.txt`

## Scope

This note supports a practical protocol / firmware workflow page for automotive UDS-on-CAN style diagnostic analysis. It is intentionally bounded to reverse-analysis proof selection:

- identify the diagnostic endpoint and request/response IDs
- keep transport reassembly separate from UDS application semantics
- keep service/subfunction/DID/RID enumeration separate from current ECU state truth
- keep session/security/unlock/TesterPresent timing separate from one behavior-bearing state or actuator/update consumer

It is not an exploitation recipe, seed/key cracking guide, or unsafe vehicle-control procedure.

## Source-backed observations

### UDS is a client/server diagnostic application protocol, commonly transported over CAN/ISO-TP

`udsoncan` describes UDS / ISO-14229 as an application protocol interface used for diagnostics, debugging, and ECU configuration. It emphasizes that UDS specifies message formatting rather than implementation internals. In the usual vehicle setting, a tester client talks to a server ECU on the CAN bus.

Dissecto's UDS knowledge base similarly places UDS at the application layer, commonly transported by ISO-TP on CAN or by DoIP/HSFZ. It describes vehicle-as-server, tester-as-client, request/response-driven communication, and SID-first messages.

CSS Electronics separates UDS application-layer concepts from CAN / ISO-TP transport. It specifically describes UDS on CAN / DoCAN as a stack where ISO 14229 application/session logic rides above ISO 15765-2 transport and CAN physical/data-link layers.

Practical consequence for the KB:

```text
CAN frame observed != ISO-TP payload reassembled != UDS request/response interpreted != ECU state consumer proved
```

### Service identifiers, positive responses, and negative responses are separate proof objects

The `uds` knowledge-base service page lists request SIDs, positive response SIDs, and `0x7F` as the negative response service identifier. It also documents the common +0x40 positive response relationship for standardized services, e.g. `0x10` -> `0x50`, `0x22` -> `0x62`, `0x27` -> `0x67`, `0x31` -> `0x71`.

Dissecto highlights that positive responses are generally `requestServiceId | 0x40`, while negative responses use `0x7f`. It also notes the `suppressPosRspMsgIndicationBit` in the subfunction byte for some services and that broadcasts often suppress positive responses, while negative response `0x78` (`requestCorrectlyReceived-ResponsePending`) delays a later positive response.

Practical consequence:

```text
service enumerated != positive response observed != negative response interpreted correctly != delayed positive response / suppression handled != state/effect consumed
```

### Sessions and security levels gate service availability but do not themselves prove behavior

`udsoncan` separates diagnostic sessions from security levels. Default sessions expose limited functionality; non-default sessions can be entered with DiagnosticSessionControl, but session switching is not itself a security mechanism. SecurityAccess unlocks manufacturer-defined levels and features, and TesterPresent can keep session/security posture alive for a time window.

Caring Caribou's UDS module exposes this same workflow shape: discovery of request/response arbitration IDs, service and subservice scans, TesterPresent to keep elevated sessions alive, seed collection for a specified session/security level, DID dumping, memory read, and automatic diagnostic scans. This is valuable as an observation surface but not sufficient by itself to prove safe, current, consequence-bearing behavior.

Practical consequence:

```text
session entered != security level unlocked != keepalive maintained != protected service accepted now != behavior-bearing consumer changed
```

### DIDs, RIDs, and routine/control services are contract selectors before they are state proof

UDS services such as ReadDataByIdentifier (`0x22`), WriteDataByIdentifier (`0x2E`), InputOutputControlByIdentifier (`0x2F`), RoutineControl (`0x31`), RequestDownload / TransferData (`0x34`/`0x36`), TesterPresent (`0x3E`), and ReadDTCInformation (`0x19`) are documented in the UDS service lists and tutorials.

Dissecto calls out that DIDs and routine meanings are OEM-specific, that RoutineControl can be used for arbitrary OEM functions, and that InputOutputControl can overwrite input signals or control actuators. CSS Electronics likewise frames UDS use cases around diagnostics, DTCs, parameter values, sessions, resets, firmware flashing, and settings modification.

Practical consequence: once a DID/RID/service is found, the operator still needs one consumer/effect proof: parser branch, state write, actuator/test-routine effect, configuration persistence, DTC update, programming-state transition, or follow-on ECU behavior.

### Scanning tools are useful evidence surfaces but can create false certainty

Caring Caribou documents modes for discovery, services, subservices, TesterPresent, seed collection, DID dumping, memory read, and automated scans. These surfaces are useful for selecting endpoints and contracts, but the module documentation itself warns by shape: discovery has verification options, timeouts/delays matter, and service/DID enumeration depends on request/response IDs and current ECU/session posture.

HydraScope / Dissecto material similarly emphasizes UDS scanning and SecurityAccess testing as a workflow area. The analyst should treat scans as hypotheses:

- found request/response IDs are candidate endpoint contracts
- supported services are scoped to the current session/security/time window
- negative responses may mean unsupported, precondition missing, delayed, security denied, wrong length/range, or session mismatch
- lack of a positive response can mean timeout, suppression bit, transport loss, wrong IDs, gateway behavior, ECU busy, or state expiry

## Durable KB split

The practical split to preserve:

```text
CAN IDs found
  != ISO-TP stream reassembled
  != UDS service/subfunction/DID/RID contract selected
  != diagnostic session/security/keepalive posture valid now
  != request accepted under current preconditions
  != positive/negative/delayed response interpreted correctly
  != ECU state, routine, actuator, DTC, configuration, or flash/update consumer changed
```

Compact memory:

```text
ids != reassembled != service-contract != session/security-live != accepted/responded != state-consumed
```

## Sources consulted

- Search artifact: `sources/protocol/2026-05-01-0450-can-uds-diagnostic-state-search-layer.txt`
- `udsoncan`, “Introduction to UDS” — https://udsoncan.readthedocs.io/en/latest/udsoncan/intro.html
- `uds` Python package knowledge base, “Diagnostic Services” — https://uds.readthedocs.io/en/latest/pages/knowledge_base/service.html
- Dissecto / HydraScope knowledge base, “UDS” — https://munich.dissec.to/kb/chapters/uds/uds.html
- CSS Electronics, “UDS Explained - A Simple Intro” — https://www.csselectronics.com/pages/uds-protocol-tutorial-unified-diagnostic-services
- Caring Caribou UDS module documentation — https://raw.githubusercontent.com/CaringCaribou/caringcaribou/master/documentation/uds.md
