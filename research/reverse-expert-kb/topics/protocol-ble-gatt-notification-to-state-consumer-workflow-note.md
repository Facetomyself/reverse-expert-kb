# BLE GATT Notification / Indication to State Consumer Workflow Note

Topic class: workflow note
Ontology layers: protocol / firmware practical branch, BLE/GATT contract recovery, asynchronous delivery proof, parser/state consequence proof
Maturity: draft-practical
Related pages:
- topics/protocol-firmware-practical-subtree-guide.md
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-state-and-message-recovery.md
- topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md
- topics/protocol-ingress-ownership-and-receive-path-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/protocol-reply-emission-and-transport-handoff-workflow-note.md
- topics/android-binder-contentprovider-first-consumer-workflow-note.md
- topics/ios-url-loading-interception-and-first-consumer-workflow-note.md

## 1. Problem shape

Use this note when a target is BLE / GATT shaped and the analyst can see some mixture of:

- advertising devices and connection attempts
- discovered services / characteristics / descriptors
- characteristic UUIDs or handles in a mobile app or firmware image
- `setCharacteristicNotification`, CCCD writes, or subscribe/enable calls
- ATT Handle Value Notification / Indication packets
- mobile callbacks such as Android `onCharacteristicChanged(...)`
- a device state update, UI change, actuator behavior, or follow-on command that seems linked to a notification stream

The recurring failure is collapsing all of that into one claim:

> “The BLE notification contains the device state.”

That may be true, but it is not proven by service discovery, a UUID, a CCCD write, a packet capture, or a callback alone.

The proof object is narrower:

```text
one notification / indication value, for one characteristic handle and connection state,
was enabled, emitted, delivered, parsed, and consumed by one behavior-bearing state/effect path
```

## 2. Core split

Keep these proof objects separate:

```text
service/characteristic discovered
  != characteristic properties prove this path is active
  != CCCD/subscribe write reached the peer for this connection
  != ATT Handle Value Notification / Indication observed for the expected value handle
  != host/mobile stack callback delivered this value
  != parser decoded the value under the right MTU/endianness/session assumptions
  != app/device state reducer or hardware effect consumed it
```

Compact branch memory:

```text
discovered != subscribed != notified/indicated != delivered != parsed != consumed
```

The useful stopping point is usually not “I found the UUID.” It is one of:

- one decoded field changes one app-side state reducer, UI element, policy branch, or follow-on command
- one received value changes one device-side behavior or hardware effect
- one replayed / mutated notification stream causes a predictable consumer-side transition under controlled connection and subscription state

## 3. Workflow

### Step 1 — Freeze the BLE role and connection context

Record:

- central vs peripheral roles
- public vs random address / identity resolution when relevant
- bond / pairing / security posture
- connection interval / MTU if it affects segmentation or timing
- app or firmware version
- whether GATT cache / Service Changed behavior may make discovered handles stale

Do not jump straight from a scan result to protocol semantics. Advertising identity and GATT behavior can drift across firmware versions, pairing state, service cache, and app release.

### Step 2 — Select one service / characteristic / descriptor contract

For the candidate stream, freeze:

- service UUID
- characteristic UUID
- value handle if visible
- characteristic properties: notify, indicate, read, write, write-without-response
- CCCD descriptor handle (`0x2902`) when notifications or indications are involved
- expected value length and whether MTU or long values may affect delivery

Treat these as contract selectors. They are not yet behavior proof.

### Step 3 — Prove subscription / enablement on the connection of interest

For notify/indicate paths, prove the real peer-side enablement:

- observe or hook the CCCD write
- distinguish local descriptor database writes from peer-visible descriptor writes
- record value: commonly `0x0001` for notification and `0x0002` for indication, little-endian on the wire / API buffer in many stacks
- check write response / error / authentication failure
- re-check after reconnect, cache refresh, bond changes, or Service Changed events

Stop rule:

```text
property bit present != CCCD write attempted != peer accepted subscription != later event belongs to this subscription
```

### Step 4 — Tie the emitted ATT event to the selected characteristic value handle

Use the nearest available surface:

- BLE sniffer / HCI snoop / btmon / platform Bluetooth logs
- Android Bluetooth HCI snoop log plus app logs
- iOS PacketLogger / sysdiagnose where available
- BlueZ / `btmon` / `bluetoothctl` / D-Bus observations
- firmware-side stack events on Nordic / Zephyr / Silicon Labs / vendor SDKs

For each interesting value, preserve:

- connection identity
- ATT opcode family: notification vs indication
- attribute value handle
- raw value bytes
- timestamp / sequence / nearby writes or reads
- confirmation or error posture for indications when visible

Do not overread a sniffer line. Air-visible delivery is not the same as host-stack callback delivery, and indication confirmation is still weaker than application consumer proof.

### Step 5 — Cross the host/mobile stack callback boundary

On the controlling app or host side, locate the first callback that receives the value:

- Android: `BluetoothGattCallback.onCharacteristicChanged`, descriptor-write callbacks, read/write callbacks, coroutine/Rx/LiveData wrappers
- iOS: `centralManager`, `CBPeripheralDelegate.peripheral(_:didUpdateValueFor:error:)`, Combine/async wrappers, notification fanout
- Linux/BlueZ: D-Bus `PropertiesChanged`, `AcquireNotify`, custom GATT client callbacks, daemon-side dispatch
- embedded central: vendor-stack event handler and queue handoff

Freeze callback truth separately from parser truth:

```text
ATT event observed != platform callback delivered != wrapper stream enqueued != parser consumed
```

### Step 6 — Decode under current session assumptions

Before assigning semantics, lock down:

- endian and signedness
- fixed vs variable length
- bitfields / flags / status codes
- sequence counters / timestamps / freshness bytes
- multi-packet or chunked values
- encryption/compression/application framing layered inside the characteristic value
- whether the value is notification-only, read-after-notify, or notify-as-invalidator for a later read

Prefer compare pairs:

- same characteristic, changed device state
- same state, changed connection / MTU / app version
- CCCD disabled vs enabled
- notification vs explicit read
- mutation/replay where allowed in a lab setting

### Step 7 — Prove the first behavior-bearing consumer

The first consumer may be:

- a mobile app state reducer
- a UI model update
- a policy gate / error branch
- a command scheduler that sends a write in response
- a persistence layer / history recorder
- a network upload / cloud sync edge
- a device-side actuator / control loop update
- a firmware parser that routes the value into a state machine

Stop only after one consequence-bearing edge is tied to the decoded value.

Good evidence shapes:

- callback value -> parser function -> state field -> UI/state transition
- notification byte mutation -> predictable consumer branch change
- CCCD disabled -> callback/consequence disappears while other traffic remains stable
- same raw value replayed under same subscription state -> same reducer/effect
- indication confirmation seen but consumer absent -> report as transport/host proof only, not app behavior proof

## 4. Observation surfaces

### Packet / controller surfaces

Use for:
- connection and ATT event truth
- handle/value pairing
- notification vs indication distinction
- timing and loss questions

Do not use alone for:
- app callback delivery
- parser semantics
- state/effect ownership

### App / host-stack surfaces

Use for:
- subscription path
- descriptor writes
- callback delivery
- wrapper stream / async fanout
- parser and reducer localization

Do not use alone for:
- proving the peripheral emitted the same bytes observed by a sniffer
- proving current GATT cache / service handle truth without reconnect/cache checks

### Firmware / peripheral surfaces

Use for:
- characteristic update owner
- notify/indicate send call
- CCCD state handling
- event-handler ownership
- actuator or state-machine consequences

Do not use alone for:
- proving central-side callback delivery or app consumption

## 5. Common false stops

- **UUID stop**: a custom UUID names a candidate contract, not the active behavior.
- **Property stop**: notify/indicate property means possible, not subscribed or delivered.
- **CCCD stop**: enablement is setup truth, not event or consumer proof.
- **Sniffer stop**: packet visibility proves transport event, not app callback or parser consumption.
- **Callback stop**: `onCharacteristicChanged` / delegate entry proves delivery, not semantics.
- **Parser stop**: decoded fields are not enough if the state reducer or effect consumer is still unproved.
- **Read-after-notify confusion**: some designs notify only that a value changed and require a read for the real payload.
- **Cache drift**: stale GATT handles, Service Changed behavior, pairing state, or app cache can make yesterday’s handle map lie today.

## 6. Minimal evidence record

For each claimed BLE notification/indication behavior, preserve:

```text
Device / app context:
- peripheral identity, app/firmware version, bond/security state
- connection timestamp and MTU if relevant

GATT contract:
- service UUID
- characteristic UUID
- value handle
- properties
- CCCD handle and accepted value

Transport event:
- ATT opcode family: notification or indication
- raw value bytes
- timestamp / sequence
- confirmation/error posture if indication

Host/app delivery:
- callback method or stack event
- wrapper/fanout path if present
- parser function and decoded fields

Consumer proof:
- first state reducer / UI update / follow-on command / file/network write / actuator effect
- compare or mutation evidence tying raw value to consequence
```

## 7. Handoff rules

Hand off to `protocol-ingress-ownership-and-receive-path-workflow-note` when the main missing proof is the local receive owner before the GATT callback or firmware receive path.

Hand off to `protocol-parser-to-state-edge-localization-workflow-note` when callback delivery is already proven and the remaining work is locating the parser-to-state consequence.

Hand off to `protocol-replay-precondition-and-state-gate-workflow-note` when the value can be built or replayed but only works under unknown connection/security/session state.

Hand off to `protocol-reply-emission-and-transport-handoff-workflow-note` when notification consumption triggers a write/response and the first committed output path is now the real bottleneck.

Hand off to hardware / firmware effect notes when the consumer is below the BLE stack and the proof object is now a peripheral write, control-loop change, interrupt, or deferred worker consequence.

## 8. Source anchors

Primary source note:
- `sources/protocol/2026-04-30-ble-gatt-notification-consumer-notes.md`

Search artifact:
- `sources/protocol/2026-04-30-0450-ble-gatt-notification-consumer-search-layer.txt`

Source-backed anchors:
- Bluetooth SIG GATT overview for GATT role/hierarchy framing
- Bluetooth Core Specification ATT material for attribute protocol framing
- Silicon Labs GATT characteristic docs for characteristic value / client-server / notification concepts
- BLE reverse-engineering practitioner guides for pairing app decompilation with packet/GATT inspection
- Adafruit BLE light-bulb case for GATT exploration as candidate-contract discovery rather than final semantics

## 9. Compact checklist

```text
[ ] connection / role / security context frozen
[ ] service + characteristic + value handle selected
[ ] CCCD descriptor and accepted enable value proved
[ ] notification vs indication event observed for this handle
[ ] raw value preserved with timestamp / sequence / MTU assumptions
[ ] host/mobile callback delivery proved
[ ] parser decoded value under current session assumptions
[ ] first behavior-bearing consumer/effect proved
[ ] false stops avoided: UUID, property, CCCD, sniffer, callback, parser-only
```
