# Firmware ACPI namespace / resource-description to driver-consumer workflow note

Topic class: workflow note
Ontology layers: firmware context recovery, ACPI namespace, device/resource enumeration, driver-consumer proof
Maturity: structured-practical
Related pages:
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-firmware-practical-subtree-guide.md
- topics/firmware-uefi-boot-manager-to-loader-handoff-workflow-note.md
- topics/firmware-devicetree-to-driver-consumer-workflow-note.md
- topics/peripheral-mmio-effect-proof-workflow-note.md
- topics/isr-and-deferred-worker-consequence-proof-workflow-note.md
- topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md
- sources/protocol/2026-05-28-acpi-namespace-driver-consumer-notes.md

## Why this matters
ACPI evidence often looks stronger than it is. A DSDT/SSDT dump, namespace path, `_HID`, `_CID`, `_CRS`, `_DSD`, `_DSM`, AML method trace, or sysfs ACPI object can make a device path feel explained too early:

```text
ACPI node / resource / method visible == driver-owned behavior explained
```

That is too strong. ACPI tables describe firmware-provided namespace, resources, and methods. Driver behavior still depends on which tables were loaded, whether the OS enumerated a device from the namespace, whether the case is ACPI-enumerated or bus-native-with-ACPI-companion, which bus-visible device was bound, which resource/method/property was actually consumed, and which later handler or hardware path owned the effect.

Keep the compact stop rule visible:

```text
ACPI table visible != namespace node loaded != device enumerated != bus object bound != resource/method consumed != handler/effect owned
```

For vendor method / `_DSM`-heavy cases, keep the narrower continuation:

```text
method exists != method called != return decoded != driver state updated != user/kernel request consumed != hardware/effect owned
```

## Scope
Use this note when:
- a firmware / OS-driver case is ACPI-shaped rather than Devicetree-shaped
- the analyst has DSDT/SSDT/AML material, live ACPI namespace paths, `_HID`, `_CID`, `_UID`, `_STA`, `_ADR`, `_CRS`, `_PRS`, `_SRS`, `_DSD`, `_DSM`, GPIO/I2C/SPI/serial-bus resources, PCI host-bridge routing, or ACPI method traces
- the desired artifact is a proof chain from ACPI evidence to the first driver/resource/method consumer and then to one behavior-bearing consequence

Do not use it as:
- a generic ACPI tutorial
- proof that a current firmware/boot path is trustworthy; use UEFI / boot-chain / executed-image notes first if table provenance is not stable
- a replacement for MMIO, IRQ/deferred-worker, DMA/descriptor, mailbox, or protocol proof once driver-resource consumption is already known
- a claim that Linux and Windows bind drivers identically; use this page to preserve proof objects, not to flatten OS-specific driver models

## Preconditions
Useful inputs include:
- firmware dump or live DSDT/SSDT tables, with OS override / firmware-version provenance if relevant
- decompiled AML / namespace paths from `iasl`, `acpidump`, debugger output, or kernel logs
- Linux sysfs ACPI paths under `/sys/bus/acpi/devices` and the actual bus device/driver links under `/sys/bus/platform`, `/sys/bus/i2c`, `/sys/bus/spi`, `/sys/bus/pci`, or related subsystems
- Windows Device Manager / PnP / driver-stack evidence, ETW/WinDbg/AMLI traces, or class-driver documentation for the target family
- runtime traces around ACPI method evaluation, resource parsing, device-property reads, IRQ/resource acquisition, GPIO/I2C/SPI/PWM/DMA lookup, or handler entry

## Investigation frame
- **Target:** ACPI-described firmware / OS-driver behavior where namespace/resource/method evidence appears to explain a device or control path
- **Boundary:** ACPI tables -> loaded namespace node -> OS-enumerated device or ACPI companion -> bus-visible driver binding -> resource/property/method consumer -> first behavior-bearing effect
- **Observation surface:** DSDT/SSDT/AML, ACPI namespace/sysfs, OS logs, driver match tables, PnP/bus device links, resolver APIs, AML method traces, IRQ/MMIO/DMA/GPIO traces
- **Artifact goal:** one narrow evidence row proving that a specific ACPI node/resource/method fed a specific bus device/driver state and then one behavior-bearing consumer
- **Cheapest next discriminant:** decide whether the behavior is ACPI-enumerated, bus-native-with-ACPI-companion, or method/control-surface-driven before following driver internals

## Practical workflow

### 1. Freeze table and namespace provenance
Name the ACPI material being claimed:

| Evidence | What it supports | What it does not prove |
| --- | --- | --- |
| firmware DSDT/SSDT dump | candidate namespace / AML implementation | that this exact table was loaded by the OS under the trigger |
| live OS ACPI namespace / sysfs path | namespace object loaded this boot | bus driver binding or behavior ownership |
| `_HID` / `_CID` / `_UID` | identity / compatibility / instance clue | successful device creation, driver match, or method use |
| `_STA` | firmware-present/enabled/status clue | that the OS created the expected bus object or that the driver consumed it |
| `_ADR` | bus address / child placement clue | request/effect ownership |

First stop rule:

```text
DSDT/SSDT recovered != namespace loaded != same OS-visible node under trigger
```

If table provenance is unstable because of firmware update, OS table override, virtualization, boot-mode difference, or dual-OS behavior, stabilize that first.

### 2. Classify the ACPI role before attributing behavior
ACPI can play at least three different roles:

1. **ACPI-enumerated device**
   - The platform firmware describes a device the OS cannot otherwise discover.
   - Linux often creates a platform/I2C/SPI device and binds the normal bus driver to that device.

2. **Bus-native device with ACPI companion**
   - PCI/USB or another bus discovers the device natively.
   - ACPI supplies power-management, routing, host-bridge windows, hotplug, or device-specific configuration.

3. **Vendor/class method surface**
   - A driver or service calls AML methods, `_DSM`, or vendor methods to query/control hardware.
   - The method call is the boundary, but the consumer may be kernel driver state, a user-space service, or a later hardware effect.

Second stop rule:

```text
ACPI node exists != this node is the primary binding object
```

Do not bind your mental model to `struct acpi_device`, a namespace path, or Device Manager node until you know which OS object actually receives the driver and request.

### 3. Prove enumeration and binding separately
For ACPI-enumerated devices, preserve each step:

```text
namespace node -> OS device object -> bus-visible device -> driver match -> bind/probe/start -> per-device state
```

Linux discriminants:
- `/sys/bus/acpi/devices/*/path`, `hid`, `modalias`
- linked physical device under platform/I2C/SPI/serdev/etc.
- `ACPI_HANDLE(dev)` / `ACPI_COMPANION(dev)` bridge in code
- `acpi_match_table`, `MODULE_DEVICE_TABLE(acpi, ...)`, bus match table, and actual driver link
- probe entry and successful return

Windows discriminants:
- PnP device instance / hardware IDs / compatible IDs
- driver stack and class driver path
- ACPI filter/function driver boundary when present
- whether the ACPI method is called by the kernel driver, class driver, or user-space control program through the driver

Third stop rule:

```text
_HID/_CID matched != bus object bound != driver state installed
```

### 4. Follow `_CRS` / resource descriptions into the exact consumer
Treat `_CRS` as current-resource evidence, not as effect proof.

Common resource paths:
- memory / I/O resource -> OS resource object -> driver map -> first meaningful MMIO or port access
- interrupt / GPIO interrupt -> OS IRQ/GPIO mapping -> request/register handler -> first handler entry -> deferred worker if any
- I2C/SPI serial-bus resource -> adapter/controller relation -> client/slave device creation -> bus transfer consumer
- DMA resource -> channel lookup / xlate -> descriptor submit -> completion consumer
- PCI host-bridge `_CRS` / `_PRT` / MCFG / `_CBA` -> bus window / routing / config-space access -> actual PCI device/driver consumer

Fourth stop rule:

```text
_CRS reports resource != OS assigned resource != driver consumed resource != behavior used it
```

For bridge/window resources, preserve producer/consumer direction. A host bridge aperture or routing table can explain reachability without proving that the endpoint driver caused the later behavior.

### 5. Treat `_DSD`, `_DSM`, and vendor methods as return-value contracts
For `_DSD`, `_DSM`, and vendor AML methods, record the call contract:
- namespace path and method name
- UUID/GUID, revision, function index, and arguments for `_DSM`
- input buffers/register selectors for vendor methods
- caller identity: kernel driver, class driver, user-space service through driver, test tool, or analyst-triggered `acpi_call`
- return bytes / package values and decode rule
- where the decoded value is stored and first consumed

Fifth stop rule:

```text
method exists != method called with this contract != return decoded != return consumed
```

A trace of `\\_SB....METHOD(...)` is a strong boundary fact. It is still not the same as proving that the result changed driver state, reached a user-visible policy, or drove hardware.

### 6. Use compare-run reduction for noisy AML/control paths
ACPI method traces can be noisy. Use a compare-run shape:
- quiet baseline with background services minimized
- one trigger at a time: keypress, lid event, brightness action, sensor read, power-state transition, dock/hotplug event
- record method entry, arguments, return, event notification, user/kernel consumer, and later effect
- re-run after suspend/resume, firmware setting change, OS switch, or driver reload if statefulness matters

Sixth stop rule:

```text
trace delta != causal method != current effect owner
```

A method can be background polling, status refresh, event fanout, or a stale control path. Use repeatable trigger alignment before freezing it as the owner.

### 7. Hand off once the bottleneck moves
Once ACPI-to-driver/resource consumption is proved, route by the next missing object:
- MMIO effect unclear -> `peripheral-mmio-effect-proof-workflow-note.md`
- interrupt/deferred worker unclear -> `isr-and-deferred-worker-consequence-proof-workflow-note.md`
- DMA/descriptor ownership unclear -> `descriptor-ownership-transfer-and-completion-visibility-workflow-note.md`
- mailbox/doorbell unclear -> `mailbox-doorbell-command-completion-workflow-note.md`
- request protocol unclear -> protocol parser / ingress / replay-precondition notes
- OS service/user-space handoff unclear -> native service / IPC / event-loop notes as appropriate

Do not keep re-reading AML after the first truthful consumer has moved into driver runtime behavior.

## Common failure modes
- **Table provenance overread:** a dumped DSDT/SSDT or decompiled AML is treated as the live OS-loaded table despite override, firmware update, virtualization, or OS-specific path changes.
- **Namespace-node overread:** `_HID` / `_CID` / sysfs ACPI object visibility is narrated as driver binding or request ownership.
- **ACPI companion confusion:** a PCI or other bus-native device is discovered by the bus, while ACPI only supplies routing/power/configuration; the ACPI node is overread as the primary device.
- **Resource-description overread:** `_CRS` shows a memory, IRQ, GPIO, DMA, I2C, SPI, or bridge window resource, but no driver has proved it consumed that resource for the behavior under analysis.
- **Method-trace overread:** AML method entry or `_DSM` return is treated as hardware effect without proving decoded-return consumption.
- **Caller confusion:** an analyst-triggered method call, user-space utility, class driver, and kernel function driver are collapsed into one owner.
- **Bridge/window direction error:** PCI host-bridge `_CRS`, `_PRT`, MCFG, or `_CBA` evidence is treated as endpoint behavior rather than reachability/routing/configuration evidence.
- **Cross-OS drift:** Windows and Linux traces are compared as if their driver stacks, class drivers, and ACPI consumption patterns must match exactly.

## Useful outputs
- ACPI provenance table: firmware version, DSDT/SSDT source, OS-loaded path, namespace node, override status
- enumeration/binding ladder: namespace path, `_HID`/`_CID`/`_UID`, OS device object, bus-visible device, driver, bind/probe/start evidence
- resource/method consumer table: `_CRS` / `_DSD` / `_DSM` / method, resolver/caller, decoded value, stored state, first consumer, later effect
- compare-run trace packet: baseline trace, trigger trace, method arguments/return, caller, downstream state/effect alignment

## Minimal checklist
Before claiming ACPI-owned behavior, answer:
1. Which DSDT/SSDT/namespace path is live for this OS boot?
2. Is the target ACPI-enumerated, bus-native-with-ACPI-companion, or vendor-method-driven?
3. Which bus-visible device and driver actually bound?
4. Which `_CRS` / `_DSD` / `_DSM` / AML method output was consumed?
5. Where is the first handler, MMIO, IRQ, DMA, request, or user/kernel policy consumer?
6. What later proof shows the effect belonged to this current ACPI-backed path rather than stale configuration, background polling, or another OS/device owner?
