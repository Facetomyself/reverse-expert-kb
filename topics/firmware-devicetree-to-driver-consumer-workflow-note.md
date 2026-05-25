# Firmware Devicetree / DTB to driver-consumer workflow note

Topic class: workflow note
Ontology layers: firmware context recovery, device-tree handoff, driver binding, resource/property consumer proof
Maturity: structured-practical
Related pages:
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-firmware-practical-subtree-guide.md
- topics/firmware-bootloader-selection-to-executed-image-workflow-note.md
- topics/firmware-hardware-observation-to-executed-image-workflow-note.md
- topics/peripheral-mmio-effect-proof-workflow-note.md
- topics/isr-and-deferred-worker-consequence-proof-workflow-note.md
- sources/protocol/2026-05-22-device-tree-driver-probe-notes.md
- sources/protocol/2026-05-26-devicetree-overlay-deferred-probe-notes.md

## Why this matters
Firmware reversing often recovers a device tree before it recovers the behavior that matters. A DTB, DTS, `/proc/device-tree` dump, boot log, or kernel source binding can make a peripheral look explained too early:

```text
compatible / reg / interrupts / clocks visible
  == driver and behavior explained
```

That is too strong. Devicetree evidence describes hardware and boot-passed configuration. Driver behavior still depends on which FDT was selected, whether the node was populated, which driver matched, whether `probe()` succeeded, which resources/properties were actually consumed, and which later handler or MMIO/IRQ path owned the observed effect.

Keep the compact stop rule visible:

```text
DTB node visible != selected FDT != populated device != matched driver != probe succeeded != resource/property consumed != behavior/effect owned
```

When overlays or supplier dependencies are involved, use the sharper extension:

```text
base DTB visible != overlay selected/applied != live tree mutated != device populated != match/bind selected != probe succeeded after suppliers ready != resource/property consumed != behavior/effect owned
```

## Scope
Use this note when:
- a firmware / embedded Linux case has a recovered DTB/DTS, `/proc/device-tree`, `/sys/firmware/devicetree/base`, bootloader-modified FDT, overlay, or boot log device-tree evidence
- the analyst is trying to map a node, `compatible`, `reg`, `interrupts`, `clocks`, `resets`, `dmas`, `pinctrl`, `status`, alias, phandle, or overlay to a concrete driver-owned behavior
- the desired artifact is a proof chain from device-tree evidence to the first driver/resource/property consumer and then to one behavior-bearing consequence

Do not use it as:
- a generic Devicetree tutorial
- a binding-authoring checklist
- proof that the currently selected image/bootflow is trustworthy; use the hardware observation and bootloader-selection notes first when image or FDT selection is still uncertain
- a replacement for peripheral/MMIO or ISR/deferred-worker proof once driver-resource consumption is already known

## Preconditions
Useful inputs include:
- recovered DTB/DTS from flash, OTA, kernel image, FIT, boot partition, or live `/proc/device-tree`
- boot logs naming FDT load address, overlays, machine compatible, OF population, deferred probe, or probe failure
- kernel source or modules containing OF match tables, binding YAML, and `probe()` / resource acquisition code
- sysfs evidence under `/sys/bus/*/devices`, `/sys/bus/*/drivers`, `/sys/firmware/devicetree/base`, `/proc/interrupts`, `/proc/iomem`, or driver-specific debugfs
- runtime traces around `of_*`, `platform_get_resource`, `devm_ioremap_resource`, `devm_request_irq`, regulator/clock/reset/pinctrl acquisition, DMA setup, or handler entry

## Investigation frame
- **Target:** embedded Linux / firmware target where DTB/DTS evidence appears to explain hardware or driver behavior
- **Boundary:** DTB artifact -> boot-selected FDT -> device population -> driver match/bind/probe -> resource/property consumer -> first behavior-bearing effect
- **Observation surface:** bootloader logs, kernel boot logs, `/proc/device-tree`, sysfs driver links, OF match tables, driver `probe()`, resource acquisition APIs, MMIO/IRQ/DMA traces
- **Artifact goal:** one narrow evidence row proving that a specific selected FDT node produced a specific device, matched a specific driver, passed `probe()`, and supplied the resource/property that later behavior consumed
- **Cheapest next discriminant:** compare the recovered DTB/DTS with the live boot-passed tree or boot log before spending time on driver internals

## Practical workflow
### 1. Freeze which tree is being claimed
Name the source of the tree:

| Evidence | What it supports | What it does not prove |
| --- | --- | --- |
| DTB carved from flash / FIT / boot partition | candidate hardware-description artifact | that this blob was selected this boot |
| vendor DTS source | intended board description | installed image, overlays, runtime mutation |
| bootloader FDT address / `fdt` commands | selected or modified boot-time FDT candidate | kernel-side device population success |
| `/proc/device-tree` / `/sys/firmware/devicetree/base` | live kernel-exposed tree after boot | probe success or resource consumption by a driver |
| driver binding YAML / OF match table | candidate match contract | that the device exists or bound on this target |

First stop rule:

```text
DTS/DTB recovered != boot-selected FDT != live kernel tree
```

If FDT selection is still uncertain, route back to bootloader-selection or executed-image proof before claiming driver behavior.

### 2. Separate hardware-description fields from runtime driver proof
Classify the node fields as candidate inputs, not as behavior proof:

- `compatible` -> candidate machine/driver match strings
- `reg` / unit address -> candidate MMIO or bus address range
- `interrupts` / `interrupt-parent` -> candidate IRQ line/specifier
- `clocks`, `resets`, `power-domains`, `regulators`, `pinctrl-*`, `dmas` -> candidate provider dependencies via phandle resolution
- `status` -> candidate enable/disable gate
- aliases -> naming/convenience evidence, not stable driver ownership
- overlays -> mutation layer that must be placed in time and scope

Second stop rule:

```text
property present != resolver ran != consumer used it
```

### 3. Prove population before matching
Ask whether the node became a device in the relevant bus/model:

- Was the node `status = "okay"` or otherwise enabled after overlays?
- Did the kernel populate it as a platform / I2C / SPI / MDIO / USB child / other bus device?
- Is there a sysfs device path linked back to the OF node?
- Did boot logs show OF population, skipped disabled nodes, missing parent bus, or deferred dependencies?

Third stop rule:

```text
enabled-looking node != populated device != current bus instance
```

### 4. Prove match, bind, and `probe()` separately
Driver binding documentation makes these separate stages:

```text
device registered -> driver match selected -> driver bound -> probe called -> probe succeeded -> per-device state installed
```

For a reverse case, preserve evidence for each stage when possible:
- OF match table entry selected for the `compatible`
- bus match path or module autoload evidence
- `/sys/bus/<bus>/drivers/<driver>/<device>` link
- probe entry log / ftrace / kprobe / dynamic debug / breakpoint
- successful return vs `-EPROBE_DEFER`, missing resource, reset/clock/regulator failure, or wrong fallback compatible
- driver-private state associated with the device object

Fourth stop rule:

```text
compatible matched != probe entered != probe succeeded != state installed
```

### 5. Follow the exact resource/property consumer
Do not stop at generic probe success if the claim is about a specific behavior. Follow the property or resource into the first consumer:

- `reg` -> `platform_get_resource(...)` / `of_address_to_resource(...)` -> `devm_ioremap_resource(...)` -> first MMIO read/write that matters
- `interrupts` -> `platform_get_irq(...)` / `irq_of_parse_and_map(...)` -> `request_irq(...)` -> first handler entry -> deferred worker if any
- `clocks` / `resets` / regulators -> provider lookup -> enable/deassert/set-rate -> first device access depending on it
- `pinctrl-*` / GPIOs -> state lookup/select -> first signal or mode-dependent behavior
- `dmas` -> channel request -> descriptor submit -> completion consumer
- custom vendor property -> `of_property_read_*` / `device_property_read_*` -> stored state -> branch/config consumer

Fifth stop rule:

```text
probe succeeded != this property/resource was consumed != this later behavior used it
```

### 6. Treat overlays and deferred probe as lifetime / placement proof, not behavior proof
Overlay evidence is stronger than a static base DTS only when it is placed in the current boot path and reflected in the kernel's live tree. Preserve the smaller ladder:

```text
base DTB visible != overlay selected/applied != live tree mutated != device populated
```

Useful discriminants:
- U-Boot / bootloader logs or FIT metadata showing which DTBOs were selected and whether `fdt apply` succeeded
- kernel live-tree evidence under `/proc/device-tree` or `/sys/firmware/devicetree/base`
- overlay notifiers, dynamic OF changes, or boot logs showing newly created / removed nodes
- comparison of base DTS, overlay fragments, and live-tree properties when the case depends on `status`, `compatible`, pinctrl, clocks, resets, GPIOs, or custom vendor properties

Do not treat an overlay-created node as stable behavior ownership if the overlay can be removed or if code cached pointers to overlay nodes/properties beyond the overlay lifetime. That is stale evidence until a current live-tree node, populated device, and driver-owned state are proved.

Deferred probe is the other common lie. A node may match a plausible driver and enter `probe()`, but supplier dependencies can still prevent final ownership:

```text
probe entered != supplier ready != final probe success != per-device state owns behavior
```

Check `/sys/kernel/debug/devices_deferred`, deferred-probe logs, dynamic debug around supplier lookup, and final retry success when phandles point to backlights, regulators, clocks, resets, GPIOs, DMA channels, pinctrl states, or power domains. If the device remains deferred, current no-behavior may be explained by missing supplier readiness rather than by parser/MMIO logic.

### 7. Hand off to peripheral, IRQ, DMA, or protocol proof when the bottleneck moves
Once driver-resource consumption is proved, route the case by the new missing object:

- MMIO effect unclear -> `peripheral-mmio-effect-proof-workflow-note.md`
- interrupt/deferred worker unclear -> `isr-and-deferred-worker-consequence-proof-workflow-note.md`
- descriptor/DMA ownership unclear -> `descriptor-ownership-transfer-and-completion-visibility-workflow-note.md`
- mailbox/doorbell unclear -> `mailbox-doorbell-command-completion-workflow-note.md`
- protocol parser/state unclear -> protocol parser / ingress / replay-precondition notes

Do not keep re-reading the DTB after the first truthful consumer has moved into driver runtime behavior.

## Common failure modes
- **Wrong tree overread:** carved DTB, vendor DTS, or inactive FIT configuration is narrated as the live boot-passed FDT.
- **Overlay blind spot:** base node looks disabled or incomplete, but bootloader or kernel overlays mutate `status`, `compatible`, pinctrl, or resources before population.
- **Overlay lifetime overread:** overlay application or a post-apply node is treated as behavior proof even though the current live tree, populated device, and driver-private state have not been proved, or stale overlay node pointers survive removal.
- **Fallback-compatible lie:** generic fallback compatible matches a driver that probes but lacks the feature or quirk needed for the observed behavior.
- **Probe-defer overread:** `probe()` entry is observed, but dependencies defer or fail and no per-device state owns the behavior; `/sys/kernel/debug/devices_deferred` or supplier-not-ready reasons are ignored.
- **Phandle-order lie:** clocks/resets/interrupts/DMA entries are present, but name/order mismatch sends the driver to a different provider or index.
- **Sysfs overread:** device/driver links prove binding state but not that the behavior-bearing property or resource was consumed.
- **MMIO-address overread:** `reg` maps a region, but the observed effect belongs to another bank, runtime remap, child node, or deferred worker.

## Useful outputs
- FDT provenance table: carved/vendor/live tree, hash/path/source, overlay status, boot-selected evidence
- node-to-driver ladder: node path, `compatible`, `status`, populated device path, driver name, match evidence, probe result
- resource/property consumer table: property, resolver API, stored field, first consumer function, later effect
- handoff row to MMIO / IRQ / DMA / protocol proof when driver-resource consumption is no longer the bottleneck

## Sources / provenance
- `sources/protocol/2026-05-22-device-tree-driver-probe-notes.md`
- `sources/protocol/2026-05-26-devicetree-overlay-deferred-probe-notes.md`
- Linux kernel documentation, Linux and the Devicetree — https://docs.kernel.org/devicetree/usage-model.html
- Linux kernel documentation, Driver Binding — https://docs.kernel.org/driver-api/driver-model/binding.html
- Linux kernel documentation, DOs and DON'Ts for designing and writing Devicetree bindings — https://docs.kernel.org/devicetree/bindings/writing-bindings.html
- Devicetree Specification current release page — https://www.devicetree.org/specifications/
- Devicetree Specification, Chapter 2: The Devicetree — https://devicetree-specification.readthedocs.io/en/latest/chapter2-devicetree-basics.html
