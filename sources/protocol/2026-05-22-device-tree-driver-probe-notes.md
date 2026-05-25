# Device tree / DTB to driver probe consumer notes — 2026-05-22

## Search context
Search command:

```bash
python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py \
  --queries \
    "Linux device tree binding compatible property driver probe firmware reverse engineering" \
    "DeviceTree specification compatible reg interrupts status phandle driver binding" \
    "embedded firmware reverse engineering device tree dtb driver probe hardware behavior" \
  --mode deep \
  --intent exploratory \
  --num 5 \
  --source exa,tavily,grok
```

Saved raw result set:
- `sources/protocol/2026-05-22-0450-device-tree-driver-probe-search-layer.json`

Search outcome:
- Exa returned Linux kernel / Devicetree specification / supporting material.
- Tavily returned Linux kernel / Devicetree specification / supporting Q&A material.
- Grok was invoked but returned HTTP 502 Bad Gateway on all three query attempts.

## Source-backed observations

### Devicetree is hardware-description data, not execution proof
The Linux Devicetree usage model describes DT as a data structure/language for describing hardware so the operating system does not need hard-coded machine details. Linux uses DT data for platform identification, runtime configuration, and device population.

Reverse implication:
- a recovered DTS/DTB node is an environment-description artifact
- it can be strong evidence about intended or boot-passed hardware description
- it is not by itself proof that a particular driver bound, probed successfully, consumed a property, touched MMIO, requested an IRQ, or caused the target behavior

### `compatible` is a selection input, not behavior ownership
The Linux usage model explains that root `compatible` values are sorted from most specific to less specific and used to select matching machine setup. Kernel Devicetree documentation also emphasizes documented compatible strings and existing bindings.

Reverse implication:
- `compatible` can route analysis toward candidate machine setup or driver match tables
- fallback compatible strings and board-family claims can mislead if treated as exact hardware identity
- exact driver ownership still needs match/probe/bind evidence, not just a visible string

### `/chosen`, memory, and early scan data are runtime configuration boundaries
The Linux usage model describes `/chosen` as a common place for bootargs and initrd address/size data, and describes early boot scans for chosen/root/memory data.

Reverse implication:
- bootargs/initrd/memory-range fields are important runtime-configuration artifacts
- they should be kept separate from later device-population and driver-consumer proof
- a bootarg or chosen property can be consumed early without proving that a peripheral node ever bound to a driver

### Driver binding makes match, probe, per-device state, and sysfs evidence separate proof objects
The Linux driver binding documentation describes binding as associating a device with a driver. New devices and new drivers trigger matching; if a match is found, the driver field is set and the driver's `probe()` callback is called. On successful probe, per-device state is initialized and class/sysfs links may appear.

Reverse implication:
- DT node visibility is weaker than bus/device registration
- device/driver match is weaker than successful probe
- probe entry is weaker than resource acquisition and per-device state setup
- sysfs links can support binding state, but they do not automatically prove the property or behavior under analysis was consumed

### Binding design rules help distinguish hardware ABI from Linux-driver convenience
The Linux binding-writing guidance says bindings should describe hardware, not Linux or current driver support; `compatible` should be specific; phandle entries like clocks, DMAs, interrupts, and resets should be explicitly ordered; and node names are not stable ABI compared with phandles or compatibles.

Reverse implication:
- when reversing vendor DTBs, treat properties as a hardware-description ABI first
- `reg`, `interrupts`, `clocks`, `resets`, `dmas`, `pinctrl`, `status`, aliases, and overlays need proof of resolver and consumer placement
- a property may be correct hardware description yet unused by the current driver path, or used by bootloader/firmware rather than the Linux driver of interest

### DTSpec frames nodes/properties and FDT as passed data
The Devicetree specification describes a devicetree as nodes with property/value pairs; a boot program loads a devicetree into client memory and passes a pointer to the client program. It also describes properties and node naming conventions such as `node-name@unit-address`, with unit address matching the first `reg` address.

Reverse implication:
- DTB/FDT location and handoff are their own proof boundary
- decompiling DTS from an image is not equal to proving the same blob was the boot-passed FDT
- `reg` / unit-address evidence helps locate candidate MMIO/peripheral regions, but it does not prove actual access or effect

## Practical synthesis
The useful stop rule for firmware reversing is:

```text
DTB node visible != selected FDT != populated device != matched driver != probe succeeded != resource/property consumed != behavior/effect owned
```

This note should be used when an analyst has a DTS/DTB, boot log, `/proc/device-tree`, driver match table, or sysfs evidence and is tempted to narrate a device-tree node as behavior ownership. The proof should instead walk from selected boot-passed FDT, through device population and driver binding, into one concrete probe/resource/property consumer and then to the first behavior-bearing effect.

## Sources consulted
- Linux kernel documentation, Linux and the Devicetree — https://docs.kernel.org/devicetree/usage-model.html
- Linux kernel documentation, Driver Binding — https://docs.kernel.org/driver-api/driver-model/binding.html
- Linux kernel documentation, DOs and DON'Ts for designing and writing Devicetree bindings — https://docs.kernel.org/devicetree/bindings/writing-bindings.html
- Devicetree Specification current release page — https://www.devicetree.org/specifications/
- Devicetree Specification, Chapter 2: The Devicetree — https://devicetree-specification.readthedocs.io/en/latest/chapter2-devicetree-basics.html
