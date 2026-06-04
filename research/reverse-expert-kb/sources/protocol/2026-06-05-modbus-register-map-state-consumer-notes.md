# Source note — Modbus register-map to device-state consumer proof (2026-06-05)

## Scope
External-source support for `topics/protocol-modbus-register-map-to-device-state-consumer-workflow-note.md`.

Search artifact:
- `sources/protocol/2026-06-05-0450-modbus-register-state-search-layer.json`

## Sources consulted
- Modbus Organization, *Introduction to Modbus* — https://www.modbus.org/introduction-to-modbus
- NI, *What is the Modbus Protocol & How Does It Work?* — https://www.ni.com/en/shop/seamlessly-connect-to-third-party-devices-and-supervisory-system/the-modbus-protocol-in-depth.html
- Modbus Application Protocol Specification V1.1b3 search result — https://www.modbus.org/file/secure/modbusprotocolspecification.pdf
- Chipkin, *What Is the Modbus Transaction Identifier* — https://store.chipkin.com/articles/modbus-what-is-the-modbus-transaction-identifier
- Chipkin, *MODBUS Exception Responses* — https://store.chipkin.com/articles/modbus-exception-responses
- Chipkin docs, *How to Read a Modbus Register Map* — https://docs.chipkin.com/articles/how-to-read-a-modbus-register-map/

## Findings preserved for the KB

### Modbus is application-layer request/response, but data meaning is device-defined
The Modbus Organization introduction frames Modbus as an application-layer protocol for exchanging process data among industrial control devices. It standardizes command/function codes, addressing, and data formatting, while remaining deployable over serial, Ethernet/TCP, and other lower layers.

For reversing, this means protocol identity is only the beginning: a visible function code and register number still need device-local data-model and consumer proof.

### Core data model has four conceptual banks
NI summarizes the four common banks:
- coils: Boolean, master read/write
- discrete inputs: Boolean, master read-only
- holding registers: unsigned word, master read/write
- input registers: unsigned word, master read-only

NI also notes that these blocks are conceptual and may overlap or be implemented only partially by a slave device. The addressing scheme is defined by the slave device and its interpretation is part of the data model.

KB implication: **function code / bank truth is separate from printed register-map number truth**.

### PDU offset and human register notation drift
NI states that within the PDU, data-element addresses range from 0 to 65,535, while human numbering may be 1-based. Holding register 54 can correspond to address 53. Modicon-style prefixes (`0`, `1`, `3`, `4`) add another notation layer.

Chipkin’s register-map guide emphasizes that map conventions vary and recommends validating ambiguous rows by trying the documented address and address-1 against a known physical value.

KB implication: **map row != PDU offset**. Record the tool convention and the actual wire offset.

### Multi-register values require type, scale, and word/byte-order validation
NI notes that the standard’s simple word/bit model does not define richer multi-register types and that endianness/word order for multiword values is not defined by the standard. Chipkin’s register-map guide similarly highlights scale factors, signedness, floats, bit-fields, and four common byte/word-order permutations.

KB implication: a plausible float or scaled integer is not enough. Require a local display, known physical value, induced state, firmware variable, or gateway object as a validation anchor.

### Function-code validation and exceptions are boundary evidence
NI describes function-code handling as validation of function code, data address, and data range before execution; failures return exceptions. Chipkin’s exception page preserves useful exception meanings:
- `01 Illegal Function`: function not allowable or device not in the right state
- `02 Illegal Data Address`: address/range invalid, including a range that crosses an unimplemented register
- `03 Illegal Data Value`: request-structure/value issue; specifically not proof that an application data item is outside semantic expectation
- `04 Server Device Failure`: failure while attempting the action
- `0A/0B`: gateway path unavailable or target failed to respond

KB implication: **accepted access != semantic device effect** and **exception != application-state meaning** without one more consumer/effect check.

### Modbus TCP transaction identifier is correlation, not application proof
Chipkin’s transaction-identifier article describes a Modbus TCP frame as Transaction Identifier, Protocol Identifier, Length, Unit Identifier, Function Code, and Data Bytes. It notes the transaction identifier is echoed in the corresponding response and helps match/validate messages between client and server.

KB implication: transaction ID echo proves a request/response pairing, but does not prove unit/function/address semantics or device-state consumption.

## Practical synthesis
The source-backed stop rule added to the KB is:

```text
map row != PDU offset != accepted access != decoded value != live validation != device-state consumer/effect
```

For TCP-shaped cases:

```text
transaction id echoed != same unit/function/address semantics != application state consumed
```

This Modbus note complements the existing MQTT, BLE, USB HID, CAN/UDS, and Netlink notes by adding an industrial register-map false-proof pattern: visible protocol success and printed register documentation often look decisive before address convention, value interpretation, and first device-state consumer are actually proved.
