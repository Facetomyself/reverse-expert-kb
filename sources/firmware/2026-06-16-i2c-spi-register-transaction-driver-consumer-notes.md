# 2026-06-16 — I2C / SPI register transaction to driver consumer notes

## Scope
Source-backed notes for a firmware / embedded Linux reversing seam where board description, bus capture, or kernel driver code exposes I2C / SPI traffic, but the analyst still needs to prove which driver-owned register transaction, status bit, IRQ, workqueue, subsystem update, or userspace-visible effect owns the behavior.

## Sources consulted
- Search artifact: `sources/firmware/2026-06-16-0450-i2c-spi-search-layer.json`
- Linux kernel documentation, `I2C and SMBus Subsystem` — https://docs.kernel.org/driver-api/i2c.html
- Linux kernel documentation, `Implementing I2C device drivers` — https://docs.kernel.org/i2c/writing-clients.html
- Linux kernel documentation, `How to instantiate I2C devices` — https://kernel.org/doc/html/v6.3/i2c/instantiating-devices.html
- Linux kernel documentation, `Serial Peripheral Interface (SPI)` — https://docs.kernel.org/driver-api/spi.html
- Linux source, `drivers/base/regmap/regmap-spi.c` — https://github.com/torvalds/linux/blob/master/drivers/base/regmap/regmap-spi.c
- Linux source, `drivers/i2c/i2c-core-base.c` — https://github.com/torvalds/linux/blob/master/drivers/i2c/i2c-core-base.c
- Electronics StackExchange, `How to reverse engineer I2C and SPI protocols?` — https://electronics.stackexchange.com/questions/350/how-to-reverse-engineer-i2c-and-spi-protocols

## Extracted facts / operator implications

### I2C device visibility is software-instantiated, not hardware-enumerated
- Linux I2C docs emphasize that I2C devices are not enumerated at the hardware level. Software must know which devices live on each bus segment and which address they use.
- Device instantiation may come from Devicetree, ACPI, board files, explicit `i2c_new_client_device(...)`, scanned devices, or user-space sysfs creation.
- Operator implication: `0xNN ACKed on bus` or a devicetree node is weaker than a bound `i2c_client` plus selected `i2c_driver.probe(...)` success. A captured bus transaction may belong to a different logical client, mux segment, scanned optional device, bootloader preinit, or a one-off detector.

### I2C client binding and access helpers are separate proof objects
- `struct i2c_adapter` represents the bus segment; `struct i2c_client` represents one slave device on that segment; `struct i2c_driver.probe` binds a driver to a client.
- I2C client docs show common driver wrappers around register reads/writes using SMBus helpers such as `i2c_smbus_read_byte_data`, `i2c_smbus_read_word_data`, `i2c_smbus_write_byte_data`, and `i2c_smbus_write_word_data`, or plain `i2c_transfer(...)` sequences.
- Operator implication: seeing an `i2c_transfer` or `i2c_smbus_*` call is bus-operation truth, not semantic register truth. The first useful proof often lives one layer up in the helper that maps `(reg, width, mask, cached field)` to a driver state update or subsystem event.

### I2C probe/detect can be misleading evidence
- Kernel docs warn that device detection is a legacy mechanism, can misdetect, and has side effects; many devices cannot be detected reliably without out-of-band board information.
- Operator implication: a read of a manufacturer/device ID register during detect proves probing or detection attempt, not that the same driver later owns runtime behavior. Separate `detected / instantiated / bound / initialized / runtime transaction / consumer`.

### SPI has controller/device/driver split and message completion semantics
- SPI docs split controller drivers (`spi_controller`) from protocol drivers (`spi_driver`) bound to `spi_device` instances.
- SPI I/O is message-oriented: protocol drivers submit `spi_message` objects made of one or more `spi_transfer` objects. Processing and completion can be asynchronous, with synchronous wrappers layered on top.
- `spi_device` carries board-specific mode, speed, bits-per-word, chip-select, IRQ, and controller data; `spi_transfer` can override per-transfer attributes.
- Operator implication: MOSI/MISO bytes or a `spi_sync(...)` call are weaker than proof that the selected `spi_device`, chip-select/mode/word-size, message/transfer sequence, completion status, and protocol-driver consumer are all aligned. Wrong CPOL/CPHA, bits-per-word, dummy bytes, chip select timing, DMA split, or async completion can make a plausible decode false.

### regmap-like layers hide and normalize register traffic
- Search returned Linux `regmap-spi.c` and historical regmap discussion around a generic I2C/SPI register-map library. Regmap abstracts common register I/O over slow control buses and may add caching, formatting, locking, paging, volatile/precious register policy, and update-bits operations.
- Operator implication: `regmap_read/write/update_bits/bulk_read` style evidence is often closer to semantic register access than raw bus calls, but cache hits, volatile rules, update-bits read-modify-write, paged register windows, and format endianness can still make a raw bus trace diverge from the driver's current state claim.

### Board description and driver consumer must be tied together
- Devicetree/ACPI/board-info evidence can describe bus speed, address, compatible string, IRQ, GPIOs, regulators, clocks, reset lines, and other board-specific wiring.
- Operator implication: a compatible node or ACPI entry is not yet behavior ownership. The route must pass through successful probe/resource acquisition, optional reset/config writes, interrupt/event handling, and the first subsystem/user-visible consumer such as input, hwmon, RTC, MTD, netdev, DRM, power-supply, regulator, or custom character device state.

## Practical split to preserve

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

## False stops
- Devicetree/ACPI node overread as live behavior.
- I2C address ACK overread as chip identity.
- Detect/probe ID read overread as runtime owner.
- SPI byte stream decoded without freezing chip-select, mode, bits-per-word, transfer boundaries, and dummy cycles.
- `i2c_transfer`, `spi_sync`, or `spi_async` hit overread as register semantics.
- `regmap_write` / `regmap_update_bits` overread without cache, volatile, paging, and RMW outcome checks.
- IRQ line or status bit overread without proving handler/workqueue/subsystem consumer.
- Bus trace from bootloader/firmware preinit overread as Linux runtime driver ownership.

## Suggested observation surfaces
- Static: Devicetree/ACPI/board files, driver `of_match_table` / `i2c_device_id` / `spi_device_id`, `probe`, register helper wrappers, `regmap_config`, IRQ/poll/workqueue handlers, subsystem registration.
- Kernel runtime: `i2c_new_client_device`, `i2c_add_driver`, `i2c_transfer`, `__i2c_transfer`, `i2c_smbus_*`, `spi_register_driver`, `spi_sync`, `spi_async`, `spi_finalize_current_message`, regmap helpers, IRQ handler, workqueue callback.
- Hardware/runtime: logic analyzer bus trace, debugfs/sysfs nodes, `/sys/bus/i2c/devices`, `/sys/bus/spi/devices`, `dmesg` probe logs, dynamic debug/ftrace/kprobes, subsystem-visible state.

## Reusable capture fields
`bus/controller | node/source | address/chip-select | compatible/modalias | driver | probe result | resources | register helper | reg/page/width/mask | transfer API | message/transfer boundaries | status/return | decoded value | regmap cache/RMW | IRQ/poll/workqueue | subsystem callback/state | userspace-visible effect | false stop ruled out`
