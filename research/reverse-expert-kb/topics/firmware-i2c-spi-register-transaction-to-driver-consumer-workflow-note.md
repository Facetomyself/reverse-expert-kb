# Firmware I2C / SPI register transaction to driver consumer workflow note

Topic class: workflow note
Ontology layers: firmware/protocol practical branch, embedded bus transaction proof, driver-consumer localization
Maturity: source-backed-practical
Related pages:
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-firmware-practical-subtree-guide.md
- topics/firmware-devicetree-to-driver-consumer-workflow-note.md
- topics/firmware-acpi-namespace-to-driver-consumer-workflow-note.md
- topics/peripheral-mmio-effect-proof-workflow-note.md
- topics/isr-and-deferred-worker-consequence-proof-workflow-note.md
- topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/runtime-behavior-recovery.md

## Why this matters
I2C and SPI traces are seductive evidence: an address ACKs, a chip-select toggles, a register-looking byte pair appears, or a Linux driver calls `i2c_transfer(...)` / `spi_sync(...)`. None of that alone proves the behavior the operator usually needs.

The practical proof object is usually smaller and later:

```text
one bus-visible or driver-issued transaction
  -> one decoded register/status/field meaning
  -> one driver-owned cache/state/IRQ/workqueue consumer
  -> one subsystem or userspace-visible effect
```

This note exists to stop a common firmware / embedded-Linux overread:

```text
bus/node visible
  != device instantiated/bound
  != probe/resources initialized
  != register transaction issued
  != transfer completed/ACKed
  != register value decoded/cache-updated
  != IRQ/poll/workqueue consumer ran
  != subsystem or userspace-visible effect owned
```

## Scope
Use this when the target is firmware, embedded Linux, a board support package, or a driver stack where the visible surface is one of:
- Devicetree / ACPI / board-file description for I2C or SPI children
- bus captures from a logic analyzer or firmware trace
- Linux I2C helpers: `i2c_transfer`, `__i2c_transfer`, `i2c_master_send`, `i2c_master_recv`, `i2c_smbus_*`
- Linux SPI helpers: `spi_sync`, `spi_async`, `spi_message`, `spi_transfer`, controller transfer callbacks
- `regmap_*` wrappers over I2C/SPI
- IRQ, poll, workqueue, or subsystem state changes that appear to follow register traffic

Do not use this as the primary page when:
- the bottleneck is only proving the selected boot image, Devicetree overlay, or ACPI namespace node; start with the firmware boot / DT / ACPI pages first
- the proof object is memory-mapped register side effects rather than serial bus transactions; use the peripheral/MMIO page
- the proof object is a generic message protocol after bus payload extraction; route into protocol parser/state or replay-precondition pages

## Investigation frame
- **Target:** one I2C/SPI-attached peripheral, sensor, EEPROM, PMIC, controller, display/touch/audio component, radio, flash, TPM-like device, or board-management chip.
- **Boundary:** board description / bus transaction / register helper / completion / driver consumer / subsystem effect.
- **Observation surface:** DTS/AML/board-info, driver probe, transfer helper, regmap, logic analyzer, ftrace/kprobe, IRQ handler, workqueue, subsystem API, sysfs/debugfs/userspace effect.
- **Artifact goal:** one transaction-to-consumer evidence row that explains what was read/written, whether it completed, how it was decoded, which driver state changed, and what effect depended on it.
- **Cheapest next discriminant:** freeze whether the current evidence is still only `node/address/chip-select visible`, or whether the target driver has actually bound and issued one transaction whose result is consumed.

## Practical workflow

### 1. Separate description from live binding
Start with the board description, but do not stop there.

Collect:
- bus/controller identity
- I2C address or SPI chip-select
- `compatible`, `modalias`, ACPI HID/CID, board-info type, or scanned-device path
- expected driver name and match table entry
- interrupt, reset GPIO, regulator, clock, mux, pinctrl, and power-sequencing dependencies

Then prove:
- the I2C `i2c_client` or SPI `spi_device` exists for this bus segment
- the expected `i2c_driver.probe(...)` or `spi_driver.probe(...)` actually ran and returned success
- resources were acquired and the driver did not fall back, defer probe forever, bind to a generic stub, or hand ownership to another component

False stop:
- I2C devices are not hardware-enumerated. An ACK, DTS node, or sysfs-created client is not chip identity or runtime behavior proof.

### 2. Freeze the bus transaction shape before decoding semantics
For I2C, record:
- adapter/bus segment and mux path if any
- client address and flags
- SMBus vs plain I2C helper
- `i2c_msg` sequence count, read/write direction, repeated-start/no-stop expectations
- register/index byte, payload width, return status, and retry/error path

For SPI, record:
- controller, `spi_device`, chip-select, mode, speed, bits-per-word, lane width, and IRQ if relevant
- `spi_message` and `spi_transfer` boundaries, not just a continuous byte stream
- TX/RX buffers, dummy bytes, command/address/data phases, chip-select hold/change, per-transfer overrides, DMA split, completion status

False stop:
- one MOSI/MISO byte string is not a register operation until chip-select, mode, word size, transfer boundaries, and dummy/turnaround bytes are fixed.

### 3. Move one layer up from raw transfer to register helper
Most useful semantics are not in the bus helper itself. Look for:
- local wrappers such as `foo_read`, `foo_write`, `read_reg`, `write_reg`, `update_bits`
- `regmap_read`, `regmap_write`, `regmap_update_bits`, `regmap_bulk_read`, `regmap_field_*`
- paging/window selection helpers
- endian/format conversion
- cache/volatile/precious register policy
- read-modify-write masks and status-bit clearing behavior

Ask what the helper claims the transaction means:
- configuration write?
- status poll?
- interrupt reason read/clear?
- FIFO drain/fill?
- calibration/OTP read?
- mode change?
- power/reset sequencing?

False stop:
- `regmap_update_bits(...)` is not necessarily one visible write that changed hardware state. Check cache, volatile policy, read-modify-write result, dirty/cache-only mode, paging, and whether the old value already matched.

### 4. Prove transfer completion and error posture
Do not treat transaction issuance as completion.

For I2C:
- confirm return value equals expected message count or byte count
- distinguish NACK, arbitration loss, timeout, adapter functionality mismatch, and retry success
- separate probe/detect reads from runtime reads

For SPI:
- confirm synchronous wrapper return or async completion
- check `spi_message.status`, actual length, timeout/error handler, controller fallback, and split transfer behavior
- keep queued async message truth separate from completed message truth

False stop:
- an issued transfer can fail, retry, complete partially, or complete after the caller path already chose a fallback state.

### 5. Locate the first driver-owned consumer
After one register value is trustworthy, find the first consumer that makes it behaviorally relevant:
- direct local state field update
- regmap cache / field cache update that later gates behavior
- IRQ handler status decode
- workqueue/threaded-IRQ callback
- poll loop reducer
- subsystem notification or registration update
- userspace-visible sysfs/debugfs/input/hwmon/rtc/power-supply/netdev/drm/MTD/regulator/char-device effect

Use a narrow row:

```text
register/status value
  -> decoded field/mask
  -> consumer function
  -> state/subsystem write
  -> externally visible or downstream effect
```

False stop:
- an IRQ line firing or status register read is not enough. The handler may discard it, clear it, debounce it, schedule work that never runs, or update a private cache that no later consumer uses.

### 6. Decide whether the transaction belongs to bootloader, probe, or runtime behavior
A bus trace may belong to:
- boot ROM or bootloader preinit
- kernel probe/setup
- runtime poll/IRQ handling
- suspend/resume/shutdown
- userspace-triggered ioctl/sysfs/debugfs access
- a different OS image or slot than the current runtime

Tie each transaction to a phase and owner before using it in a behavior claim.

False stop:
- a bootloader or probe-time register write may explain initialization, but not necessarily the runtime state transition under the trigger being investigated.

## Hook / breakpoint plan

Static first:
1. match `compatible` / ACPI / board-info / modalias to driver
2. inspect `probe`, resource acquisition, reset/power sequencing, and subsystem registration
3. identify local register helpers and `regmap_config`
4. identify IRQ/poll/workqueue/subsystem consumers

Runtime on Linux:
- `i2c_new_client_device`, `i2c_add_driver`, target `probe`
- `i2c_transfer`, `__i2c_transfer`, `i2c_smbus_*`
- `spi_register_driver`, target `probe`, `spi_sync`, `spi_async`, controller transfer/completion path
- `regmap_read`, `regmap_write`, `regmap_update_bits`, `regmap_bulk_read`, `regmap_field_*`
- target IRQ handler / threaded IRQ / workqueue callback
- first subsystem-visible update or userspace-visible read path

Hardware-side when needed:
- logic analyzer on SDA/SCL or CS/SCK/MOSI/MISO
- trigger on chip-select/address and correlate timestamps to kernel traces
- compare boot/probe/runtime traces separately

## Common failure modes

| Failure mode | Symptom | Next discriminant |
|---|---|---|
| Node/address overread | DTS/ACPI/sysfs shows a device, but no behavior follows | prove driver bind and successful probe |
| Wrong bus segment | ACK or transfer appears on a muxed bus but not the intended peripheral | include adapter/mux path and client identity |
| Probe/detect confusion | ID reads appear but runtime behavior is absent | separate detection/probe from runtime transaction |
| SPI framing lie | bytes decode only under assumed mode/CS/word boundaries | freeze chip-select, mode, transfer split, dummy bytes, completion |
| regmap cache lie | driver state changes without bus traffic, or bus traffic lacks expected write | inspect cache-only/volatile/RMW/page policy |
| Completion lie | call issued but return/completion indicates timeout or fallback | capture status/actual length/retry path |
| IRQ/status overread | interrupt/status read exists but effect is missing | follow handler -> worker -> subsystem consumer |
| phase mismatch | bus trace came from bootloader/probe/suspend, not the trigger | tag every transaction with phase and owner |

## Useful output shape

Produce one row per representative behavior claim:

```text
case/trigger:
bus/controller:
node/source:
address/chip-select:
driver/probe:
resource state:
transaction API:
message/transfer shape:
register/page/width/mask:
return/completion:
decoded value:
cache/RMW/paging state:
consumer function:
IRQ/workqueue/poll path:
subsystem/userspace effect:
false stops ruled out:
```

## Sources / provenance
- Source note: `sources/firmware/2026-06-16-i2c-spi-register-transaction-driver-consumer-notes.md`
- Search artifact: `sources/firmware/2026-06-16-0450-i2c-spi-search-layer.json`
