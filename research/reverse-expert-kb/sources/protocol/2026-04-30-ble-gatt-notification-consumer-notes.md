# Source Notes — BLE GATT Notification / Indication to State Consumer

Date: 2026-04-30 04:50 Asia/Shanghai
Scope: source-backed notes for a protocol / firmware workflow around Bluetooth LE GATT characteristic notifications, indications, CCCD enablement, handle identity, mobile callback delivery, and the first state-changing consumer.

## Search artifact

- `sources/protocol/2026-04-30-0450-ble-gatt-notification-consumer-search-layer.txt`

## Sources consulted

- Bluetooth SIG, “Intro to Bluetooth Generic Attribute Profile (GATT)” — https://www.bluetooth.com/bluetooth-resources/intro-to-bluetooth-gap-gatt/
- Bluetooth Core Specification HTML, Vol 3 Part F, Attribute Protocol (ATT) — https://www.bluetooth.com/wp-content/uploads/Files/Specification/HTML/Core-62/out/en/host/attribute-protocol--att-.html
- Silicon Labs, “Different Value Types of Characteristics” — https://docs.silabs.com/bluetooth/11.0.1/bluetooth-gatt/characteristics-value-types
- Reverse Engineering BLE Devices, “Application Protocol Reverse Engineering” — https://reverse-engineering-ble-devices.readthedocs.io/en/latest/protocol_reveng/00_protocol_reveng.html
- Adafruit Learning System, “Reverse Engineering a Bluetooth Low Energy Light Bulb — Explore GATT” — https://learn.adafruit.com/reverse-engineering-a-bluetooth-low-energy-light-bulb/explore-gatt
- Adafruit Learning System, “Reverse Engineering a Bluetooth Low Energy Light Bulb — Sniff Protocol” — https://learn.adafruit.com/reverse-engineering-a-bluetooth-low-energy-light-bulb/sniff-protocol
- Memfault Interrupt, “Bluetooth Low Energy: A Primer” — https://interrupt.memfault.com/blog/bluetooth-low-energy-a-primer

## Durable observations

### GATT hierarchy is a contract selector, not behavior proof

The Bluetooth and Silicon Labs material reinforces the hierarchy: profile -> service -> characteristic -> value / descriptors, with GATT client/server roles layered over ATT attributes and handles. For reverse work this is a selector ladder, not a proof of application behavior.

Practical consequence:
- discovered services and UUIDs identify candidate contracts
- characteristic properties tell which ATT/GATT operations are possible
- descriptor state, especially CCCD state for notify/indicate, can decide whether an asynchronous value path is even enabled
- none of those alone proves that a notification was sent, delivered to the app stack, parsed, or consumed by a state reducer

### Notification and indication differ at the evidence boundary

ATT/GATT documentation and vendor docs separate unacknowledged notifications from acknowledged indications. This matters because a sniffer-visible value update, a host-stack callback, and an application-level handler may diverge under connection churn, caching, subscription mistakes, MTU/fragment assumptions, or dropped callbacks.

Practical consequence:
- for notifications, do not overread air-visible traffic as host/application consumption
- for indications, confirmation/ack posture is a stronger but still not final application-consumer signal
- CCCD write success is setup truth, not proof that the later event reached the behavior-bearing consumer

### CCCD state is a frequent liar

Search results and vendor snippets repeatedly surface CCCD enablement problems. The common analyst mistake is treating a property bit or a local descriptor value as if it proves the peer-side subscription and later notification path.

Practical consequence:
- freeze the characteristic value handle and CCCD descriptor handle separately
- prove the actual CCCD write value (`0x0001` notification, `0x0002` indication in common little-endian notation) at the connection of interest
- keep local database updates, peer descriptor writes, and stack events separate
- re-check after reconnect, bonding, service-changed, or GATT cache refresh

### App reverse engineering and over-the-air observation should cross-check each other

The BLE reverse-engineering guide explicitly frames BLE application-protocol recovery as a parallel action: inspect/log Bluetooth packets and decompile the controlling Android app. Adafruit’s light-bulb case shows why: GATT exploration finds candidate services/characteristics, but the actual control semantics may only become clear once the app’s writes and observed device behavior are paired.

Practical consequence:
- use GATT exploration to bound service/characteristic candidates
- use app code to locate `BluetoothGatt`, `setCharacteristicNotification`, descriptor writes, `onCharacteristicChanged`, write/read callsites, parser helpers, and state reducers
- use packet or host-stack logs to confirm the selected characteristic/value handle and notification cadence
- stop only when one notification/indication value is tied to one parser/state/effect consumer

## Practical split to preserve

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

## Operator-facing implications

- Treat UUIDs and characteristic properties as routing hints.
- Treat CCCD writes as setup proof only.
- Treat sniffer-visible notifications as transport proof only.
- Treat mobile callbacks as delivery proof only.
- Treat decoded fields as parser proof only.
- Require one state reducer, UI update, command emission, file/network write, actuator change, or hardware-side consequence before claiming behavior ownership.

## Confidence

Medium-high for the workflow split. It is supported by official Bluetooth/GATT/ATT documentation, vendor GATT docs, and practitioner BLE reverse-engineering examples. The search run was degraded because Grok returned HTTP 502 for all attempts, but Exa and Tavily both produced usable source clusters and official pages were fetched directly.
