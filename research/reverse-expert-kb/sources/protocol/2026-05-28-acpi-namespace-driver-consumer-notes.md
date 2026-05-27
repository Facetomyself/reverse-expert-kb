# ACPI namespace / resource-description to driver-consumer notes — 2026-05-28

Source class: external research notes
Related workflow page: `topics/firmware-acpi-namespace-to-driver-consumer-workflow-note.md`
Search artifact: `sources/protocol/2026-05-28-0450-acpi-namespace-driver-consumer-search-layer.json`

## Sources consulted
- Linux kernel documentation, **ACPI Based Device Enumeration** — https://docs.kernel.org/firmware-guide/acpi/enumeration.html
- Linux kernel documentation, **ACPI Device Tree - Representation of ACPI Namespace** — https://docs.kernel.org/firmware-guide/acpi/namespace.html
- Linux kernel documentation, **ACPI considerations for PCI host bridges** — https://docs.kernel.org/PCI/acpi-info.html
- UEFI / ACPI Specification 6.5, **Device Configuration** — https://uefi.org/specs/ACPI/6.5/06_Device_Configuration.html (web fetch was blocked by anti-bot, but search snippets and Linux docs quote the relevant ACPI resource semantics)
- Microsoft Learn, **Other ACPI Namespace Objects** — https://learn.microsoft.com/en-us/windows-hardware/drivers/bringup/other-acpi-namespace-objects
- Microsoft Learn, **Device-Specific Methods (`_DSM`)** — https://learn.microsoft.com/en-us/windows-hardware/drivers/bringup/acpi-device-specific-methods
- Microsoft Learn, **HIDI2C Device-Specific Method (`_DSM`)** — https://learn.microsoft.com/en-us/windows-hardware/drivers/bringup/hidi2c-device-specific-method---dsm-
- Arvid Norlander, **Reverse engineering ACPI functionality on a Toshiba Z830 Ultrabook** — https://vorpal.se/posts/2022/aug/21/reverse-engineering-acpi-functionality-on-a-toshiba-z830-ultrabook/

## High-signal extracted facts

### Linux ACPI enumeration is not just “AML exists”
Linux ACPI documentation separates ACPI namespace objects from the devices drivers actually bind to.

Important operator points:
- ACPI exposes a namespace from DSDT/SSDT definition blocks.
- Linux creates `struct acpi_device` objects for namespace devices and exposes them under sysfs.
- For most platform-firmware-enumerated devices, Linux creates bus-visible physical devices such as `struct platform_device`, `struct spi_device`, or `struct i2c_client` and binds normal bus drivers to those objects.
- `struct acpi_device` is often the configuration companion, not the object a new driver should bind to directly.
- `ACPI_HANDLE(dev)` / `ACPI_COMPANION(dev)` are practical bridges from the bus-visible device object back to ACPI configuration.

Reverse implication: a recovered `_HID`/`_CID`, AML node, or sysfs ACPI object is not yet driver-owned behavior. The proof object is usually the later bus device, driver match/bind/probe, resource/property lookup, and first behavior consumer.

### `_CRS`, `_PRS`, and `_SRS` are resource-negotiation evidence, not effect proof
Linux PCI/ACPI docs quote ACPI semantics around current resources:
- `_CRS` reports current resource settings.
- `_PRS` reports possible resources.
- `_SRS` can configure resource settings.
- `_CRS` can be understood generically by the OS even before a device-specific driver exists.

Reverse implication: `_CRS` can explain why a memory range, interrupt, bus window, GPIO, SPI/I2C connection, or DMA channel is reserved/available. It does not prove the behavior-bearing driver consumed that resource, registered the handler, submitted DMA, or touched the peripheral.

### Bus-native and ACPI-described devices are different proof shapes
Linux docs explicitly distinguish natively discoverable bus devices, such as PCI, from devices that need platform firmware descriptions. For natively discoverable devices, ACPI may still provide power-management, hotplug, INTx routing, host-bridge windows, or configuration data, but driver binding happens through the bus-visible object.

Reverse implication: for PCI/USB-like cases, an ACPI namespace clue may be an auxiliary configuration or routing fact, not the primary device identity. For platform/I2C/SPI/SoC devices, ACPI may be the enumeration root. Preserve the distinction before attributing behavior.

### `_DSD` / `_DSM` are consumer-specific configuration/control surfaces
Linux ACPI enumeration docs show drivers using device-property APIs to read `_DSD`-style properties during probe. Microsoft Learn documents `_DSM` as UUID-scoped, device-specific functions, with a HIDI2C example where function 1 returns the HID descriptor register offset.

Reverse implication: `_DSD` / `_DSM` output is often a candidate configuration/control input, not a guarantee of use. In a reverse case, freeze the exact method/function/UUID/revision/index, then prove the OS/driver called it and consumed the return in the later behavior path.

### ACPI method traces are compare-run artifacts before they are ownership proof
The Toshiba Z830 case note is useful because it shows a practical reverse pattern:
- establish a quiet baseline
- collect ACPI method traces on Windows
- identify a narrow method such as `\\_SB.VALZ.GHCI(...)`
- compare traces around button / LED / battery events
- test hypotheses through Linux `acpi_call`
- keep user-space callers / services separate from kernel driver / AML method execution

Reverse implication: AML method entry and return values are high-value boundary facts, but behavior ownership still requires proving the driver or service consumed the result and caused the later effect.

## Practical stop rule synthesized

Use this compact ladder for ACPI-shaped firmware/driver cases:

```text
ACPI table visible != namespace node loaded != device enumerated != bus object bound != resource/method consumed != handler/effect owned
```

For `_DSM` / vendor-method cases, use the narrower continuation:

```text
method exists != method called != return decoded != driver state updated != user/kernel request consumed != hardware/effect owned
```

## Operator tactics worth promoting
- Capture table provenance first: firmware dump / live DSDT+SSDT / OS-overridden table / post-update firmware version.
- Name the namespace path and identity objects: path, `_HID`, `_CID`, `_UID`, `_STA`, `_ADR`.
- Decide whether the target is ACPI-enumerated, bus-native-with-ACPI-companion, or class/vendor-method-driven.
- For Linux, pivot from `/sys/bus/acpi/devices/*/path` and `modalias` to the actual platform/I2C/SPI/PCI device and its driver link before claiming ownership.
- For resources, track `_CRS` to the OS resource object, then to driver resolver API, stored state, and first handler/MMIO/DMA/IRQ consumer.
- For `_DSD` / `_DSM` / vendor methods, instrument method evaluation and the downstream consumer separately.
- If an AML method trace is noisy, use compare-run reduction with a quiet baseline and one trigger at a time.
