# Protocol Modbus Register-Map to Device-State Consumer Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, protocol state/message recovery, industrial protocol, register-map validation, device-state consumer proof
Maturity: practical
Related pages:
- topics/protocol-firmware-practical-subtree-guide.md
- topics/protocol-state-and-message-recovery.md
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md
- topics/analytic-provenance-and-evidence-management.md
Related source notes:
- sources/protocol/2026-06-05-modbus-register-map-state-consumer-notes.md

## 1. When to use this note
Use this note when a protocol or firmware case has narrowed into **Modbus-shaped register/coil interaction**, but the analyst still cannot tell whether visible reads/writes correspond to the device state or behavior under analysis.

Typical entry conditions:
- Modbus RTU / ASCII / TCP traffic is visible, or firmware contains clear Modbus function-code handling
- the analyst has a vendor register map, a scanner output, captured `Read Holding Registers` / `Write Single Register` traffic, or exception responses
- the current uncertainty is no longer “is this Modbus?”, but which unit, function, address convention, datatype, scale/word order, acceptance state, and device-side consumer actually own the behavior
- the target may be an industrial controller, HVAC/generator/solar/power device, gateway, PLC/HMI integration, or firmware service exposing a Modbus register model

Do **not** use this note when:
- Modbus framing is not yet visible; use capture/boundary-relocation or layer-peeling notes first
- the traffic is merely TCP/serial bytes with no trustworthy function-code/register interpretation yet
- the Modbus register/coil proof is already stable and the real task has moved into a private payload schema, firmware state reducer, or hardware-side effect

## 2. Core claim
The recurring Modbus reverse-engineering mistake is to stop at:

```text
register map row or successful read/write == device state/behavior proved
```

That is too early.

The useful proof ladder is:

```text
ADU/PDU captured
  -> unit/slave and transaction/message instance matched
  -> function code and data model selected
  -> address convention translated into the actual PDU offset
  -> range/block access accepted or rejected with the right exception meaning
  -> datatype / scale / word order / bit-field interpretation validated against a known live value
  -> safe write/readback or trigger-linked observation proves the device-side consumer/effect
```

Compact stop rule:

```text
map row != PDU offset != accepted access != decoded value != live validation != device-state consumer/effect
```

TCP correlation variant:

```text
transaction id echoed != same unit/function/address semantics != application state consumed
```

## 3. What counts as the right proof object
High-value proof objects:
- one request/response pair with transport (`RTU`, `ASCII`, or `TCP`), unit/slave identifier, function code, start address, quantity/value, and response/exception frozen
- one address-translation decision: vendor reference number vs register number vs zero-based PDU offset, including any `40001` / `30001` / `0xxxx` prefix convention
- one function/data-model decision: coil, discrete input, input register, or holding register, with read/write posture
- one datatype decision validated by a known live value: signed/unsigned 16-bit, scaled integer, float/int across two registers, string, status bit-field, word/byte order
- one acceptance boundary: normal response, exception response, timeout/no response, gateway path/target failure, block-size reduction, or non-contiguous range split
- one device-state consumer/effect: local display agreement, firmware state variable, control-loop input, changed mode/setpoint, subsequent status bit, actuator output, alarm/fault transition, or downstream gateway object update

Useful but often too early by themselves:
- a vendor map row without firmware revision / addressing convention / live validation
- a scanner table that silently chooses zero-based or one-based addressing
- `FC03` / `FC04` success without knowing whether the target data model uses holding vs input registers as documented
- a plausible float/int decode without a known physical value, local display, or trigger-linked state check
- an exception response interpreted as application semantics rather than Modbus-level validation failure
- a Modbus TCP transaction identifier echo without proving unit/function/address semantics and later device-state consumption

## 4. Default workflow

### Step 1 — Freeze transport and message identity
Record:

```text
capture surface | RTU/ASCII/TCP | client/master | server/slave/unit | transaction id if TCP | function | start address | quantity/value | response | exception/no-response | timing/trigger
```

For Modbus TCP, the transaction identifier is a correlation aid, not state proof. Preserve the request/response match, then keep moving toward unit/function/address and application consumer evidence.

### Step 2 — Translate the map row into the wire address
Treat every register-map row as ambiguous until translated.

Check:
- whether the map uses Modicon references (`40001`, `30001`, `00001`, `10001`) or plain register numbers
- whether the map starts at one or zero
- whether the scanner/tool expects a zero-based PDU address or a human reference number
- whether the same apparent register appears under different bank/function-code names across tools

Stop only when one map row produces a request using the intended PDU offset and data model.

### Step 3 — Validate function-code and data-model posture
Separate:
- coils (`FC01` read, `FC05` / `FC15` write)
- discrete inputs (`FC02` read)
- holding registers (`FC03` read, `FC06` / `FC16` write)
- input registers (`FC04` read)

A device may expose measurements through holding registers or use holding registers for read-only values. The map and live behavior decide; the prefix convention is only a hint.

### Step 4 — Use exceptions as boundary evidence, not final semantics
For exception responses, preserve:

```text
original function | exception function/function+0x80 | exception code | requested range | device state | gateway involvement | retry/block-split result
```

Common interpretations:
- `01 Illegal Function`: unsupported function or wrong state for that action
- `02 Illegal Data Address`: bad start/range/implemented-space, often exposed by crossing an undefined gap
- `03 Illegal Data Value`: malformed/invalid request structure or parameter, not necessarily application-level “setpoint too high”
- `04 Server Device Failure`: device failed while attempting action
- `0A/0B`: gateway path or target-device reachability problem, not necessarily register semantics

### Step 5 — Decode values only after range and type are stable
For value interpretation, test against one known physical/state anchor:
- local display value
- safe setpoint displayed by the device
- induced status bit / alarm / mode change
- firmware variable or control-loop state
- gateway destination object value

Try only bounded alternatives:
- signed vs unsigned 16-bit
- scale factor / multiplier vs divisor
- two-register word order and byte order
- bit index convention for status fields
- string length, padding, and byte order

Do not turn a numerically plausible decode into a semantic claim without one live validation point.

### Step 6 — Prove the consumer or effect
For reads, prove where the value is used:

```text
register response -> decoded value -> local display / firmware state / gateway object / control-loop input / app callback
```

For writes, prove acceptance and effect separately:

```text
write request -> normal response -> readback or status transition -> first device/gateway/firmware consumer -> durable effect
```

Safe writes should be small, reversible, and scoped to setpoints or mode bits whose physical effect is acceptable in the lab. If safe write is not possible, use compare reads, local display correlation, firmware hooks, or gateway object updates.

## 5. Instrumentation and observation surfaces

### Wire / tool surfaces
- Wireshark Modbus dissector, serial capture, `tcpdump`, logic analyzer, RS-485 tap
- Modbus scanners that expose raw PDU address and function code, not only human register notation
- paired reads at `address` and `address-1` when the map convention is ambiguous
- block-size reduction when `Illegal Data Address` appears near gaps

### Firmware / runtime surfaces
- function-code dispatch table
- address-range validation checks
- register-bank getters/setters
- scaling/endianness conversion helpers
- state-variable writes after `FC06` / `FC16`
- exception-generation path
- gateway mapping table from Modbus point to another protocol object

### Evidence row
Use one compact row per candidate register:

```text
unit | fc | map_ref | pdu_offset | quantity | response/exception | raw words/bits | decode hypothesis | live anchor | consumer/effect | confidence | next check
```

## 6. Common failure modes

### Off-by-one map drift
A map row says `40001`, a tool asks for `1`, but the wire PDU should carry address `0`. Confirm with one known value and record the tool convention.

### Prefix confusion
`4001` might mean holding register 1 in one document or coil 4001 in another notation. Freeze the function code and bank, not only the printed number.

### Block-read overclaim
A single `FC03` range can fail because it crosses an unimplemented gap. Split reads before concluding the whole map is wrong or the device rejected a value.

### Exception-code overinterpretation
`Illegal Data Value` is about Modbus request structure/value validity at the protocol layer. It does not automatically mean the application rejected a semantic setpoint.

### Plausible float trap
Many two-register values can decode into plausible floats under some byte/word order. Require a known live value before treating that decode as semantic truth.

### Write-response trap
A normal `FC06` / `FC16` response is still acceptance/echo truth. It is not yet proof that the control loop, actuator, gateway point, or saved configuration consumed the new value.

## 7. Stop rules
Stop when you can state one bounded claim like:

```text
For unit 7, vendor row "40021" maps to PDU offset 20 under FC03. Words [0x02D5] decode as scaled temperature /10 and match the local display at 72.5. The value is read by the gateway point `Chiller.Temp` and updates the dashboard within one poll cycle.
```

or:

```text
For unit 3, FC16 to PDU offset 199 is accepted and the subsequent FC03 readback plus firmware setter hit prove the setpoint store changed, but no actuator/control-loop consumer has been proved yet. Current claim stops at stored setpoint, not physical effect.
```

If the claim still depends on “the map probably means…” or “the value looks right,” the workflow is not done.
