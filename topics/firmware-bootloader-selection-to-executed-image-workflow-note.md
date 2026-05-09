# Firmware bootloader selection to executed-image workflow note

Topic class: workflow note
Ontology layers: firmware boot chain, image-lineage proof, bootloader handoff, runtime consumer proof
Maturity: structured-practical
Related pages:
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-firmware-practical-subtree-guide.md
- topics/firmware-hardware-observation-to-executed-image-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/analytic-provenance-and-evidence-management.md
- sources/protocol/2026-05-10-firmware-bootloader-selection-executed-image-notes.md

## Why this matters
Firmware analysis often gets a bootloader prompt, boot log, U-Boot environment dump, `extlinux.conf`, FIT image, device tree, or vendor update package and then quietly jumps to:

```text
boot config found == this image/path ran
```

That jump is usually too large. In U-Boot-shaped systems especially, environment variables, boot devices, boot methods, bootflows, FIT configurations, signatures, fallback attempts, command-line handoff, and kernel/init consumption are separate proof objects.

This note preserves the boot-chain seam that sits between broad hardware acquisition and later protocol/parser/runtime work.

## Scope
Use this note when:
- the target is an embedded/Linux/U-Boot-shaped firmware case
- the analyst has bootloader environment, `bootcmd`, `bootargs`, `boot_targets`, `bootmeths`, extlinux / distro boot config, FIT image material, boot logs, or `/proc/cmdline`
- the current uncertainty is not just whether bytes were acquired, but which boot object was selected, loaded, verified, handed off, and consumed

Do not use it as:
- a U-Boot exploitation guide
- a generic bootloader tutorial
- a replacement for hardware acquisition lineage when the analyst has not yet proved that the image source maps to the current device at all
- a kernel-rootcause workflow once boot selection and handoff are already trustworthy

## Investigation frame
- **Target:** embedded Linux / appliance / router / SoC firmware path using U-Boot, extlinux, FIT, EFI/VBE-style bootflow, or comparable bootloader selection logic
- **Boundary:** bootloader configuration -> selected bootflow -> loaded image tuple -> verification/policy -> OS handoff -> first runtime consumer
- **Observation surface:** U-Boot env/console/logs, extlinux config, FIT image tree, bootflow listing, boot logs, current load addresses, early kernel log, `/proc/cmdline`, live device tree, init/service traces
- **Artifact goal:** one trustworthy statement of which kernel/initrd/FDT/overlay/rootfs/cmdline tuple actually reached the behavior under analysis
- **Cheapest next discriminant:** compare bootloader-side configuration with next-stage consumed state before widening static analysis

## Core proof ladder

```text
bootloader env / boot config visible
  != boot device / boot method / bootflow selected
  != kernel / initrd / FDT / overlay tuple loaded
  != FIT configuration / signature / policy accepted
  != command line / device tree handed off
  != kernel / init / service consumed that state
  != first behavior-bearing effect proved
```

Compact branch memory:

```text
env/config != selected bootflow != loaded tuple != verified policy != handed off != consumed/effected
```

## Practical workflow

### 1. Name the boot evidence without upgrading it
Classify what you actually have:

| Evidence | What it can prove | What it does not automatically prove |
| --- | --- | --- |
| U-Boot environment dump | configured variables such as `bootcmd`, `bootargs`, `boot_targets`, `bootmeths` | current in-memory value, persistent value, selected bootflow, later consumption |
| `extlinux.conf` / distro boot file | candidate labels, kernel/initrd/FDT/append contract | selected label, substituted environment values, fallback device, final cmdline |
| bootflow scan/listing | discovered bootdev/bootmeth/bootflow candidates | successful handoff or later kernel/runtime consumption |
| FIT image / ITS | packaged kernels, ramdisks, FDTs, configurations, signatures | selected configuration, required policy accepted, current handoff tuple |
| `bootm` command/log | attempted OS boot command and possible current-load-address semantics | final selected subimages, verified policy, first runtime consumer |
| `/proc/cmdline` / early kernel log | next-stage consumed command-line evidence | original bootloader source, unobserved fallback reason, all DT/overlay truth |

Stop rule:

```text
boot evidence found != selected boot path proved
```

### 2. Freeze persistent-vs-current environment truth
U-Boot environment may be default, persistent, or in-memory-only. Preserve:
- source of environment: compiled/default `.env`, saved flash/NVRAM copy, current interactive shell state, boot-script mutation
- values that affect selection: `bootcmd`, `bootargs`, `boot_targets`, `bootmeths`, `fdtfile`, slot variables, rootfs variables, network/TFTP variables
- whether variables are read directly by a boot script, substituted into extlinux `append`, or only left as unused residue

Useful compare:

```text
printenv / saved env / default env / boot log expansion
  -> which value was current at this boot?
```

Do not patch or reason from `bootargs` alone if extlinux `append`, FIT config, EFI/VBE, Android-style bootmeth, or later scripts can override or ignore it.

### 3. Prove selected bootdev / bootmeth / bootflow before naming the OS tuple
For Standard Boot / distro boot-shaped cases, keep these separate:
- boot device: MMC/eMMC/SD/USB/NVMe/network and partition
- boot method: extlinux, EFI, VBE, PXE, script, Android, board-specific method
- bootflow: discovered config file or boot description
- boot attempt result: attempted, failed/fell through, or reached handoff

A found `/boot/extlinux/extlinux.conf` on one partition is not proof that it was selected if another bootdev, bootmeth, global boot method, bootable partition, or fallback path won first.

Stop rule:

```text
bootflow discovered != bootflow attempted != bootflow reached handoff
```

### 4. Freeze the loaded tuple, not just the container
When `bootm`, FIT, or distro boot is involved, record the tuple that matters:
- kernel image / subimage
- initrd / ramdisk, if any
- FDT / DTB source
- FDT overlays / extra FIT configurations
- rootfs selection or slot variable
- current load address when omitted `bootm` arguments or previous load commands matter

For FIT cases, distinguish:

```text
FIT blob present
  != default configuration selected
  != named configuration selected
  != kernel / ramdisk / FDT subimages selected
  != overlays / extra configs applied
```

If the analysis depends on behavior from a driver, device node, rootfs, or init script, tuple proof matters more than proving that a FIT or kernel-looking blob exists.

### 5. Treat verified boot as policy evidence, not automatic runtime proof
FIT / verified-boot evidence can answer several different questions:
- was an image hash checked?
- was an image signature checked?
- was a signed configuration required and accepted?
- was the public key in a trusted control FDT or other immutable place?
- did a failure fall back, halt, or select another image?

Do not collapse:

```text
hash/signature ok != selected configuration ok != handoff happened != runtime consumed it
```

When security posture matters, preserve signed-image vs signed-configuration proof. A signed kernel inside a different or mutable configuration is a different claim from a required signed configuration with the expected FDT/rootfs/args tuple.

### 6. Use the next stage as the consumption check
The most useful low-cost discriminator is often the next stage:
- early kernel log confirms machine, FDT, initrd, root device, panic/fallback, or command-line fragments
- `/proc/cmdline` confirms what the running kernel parsed, not merely what U-Boot stored
- `/proc/device-tree` or live DT dump confirms selected DT/overlay claims
- init/service logs confirm whether rootfs, slot, mode, feature flag, or debug parameter was consumed
- behavior under the trigger confirms the first effect-bearing consumer

Stop rule:

```text
handed off != consumed by the behavior-bearing runtime path
```

### 7. Package one boot-chain evidence unit
Before widening into static reverse engineering, produce a small evidence unit:

```text
device/partition/method/bootflow
  + selected kernel/initrd/FDT/overlay/rootfs/cmdline tuple
  + policy result if verified boot matters
  + next-stage consumed-state observation
  + first behavior-bearing consumer or explicit gap
```

This prevents rediscovering the same boot path in later parser, protocol, or persistence work.

## Common failure modes
- **environment overread:** saved `bootargs` or `bootcmd` is treated as the value used by this boot.
- **config-file overread:** a visible `extlinux.conf` is treated as selected even though another partition, global boot method, or fallback path won.
- **FIT-container overread:** a FIT image is treated as one image rather than a configuration selecting kernel/initrd/FDT/overlay subobjects.
- **signature overread:** `signature ok` is treated as proof of the expected configuration, rootfs, or runtime behavior.
- **slot overread:** A/B or rootfs variables are read statically but not checked against the final command line and mounted root.
- **handoff overread:** `bootm` or `bootflow boot` appears in logs, but no next-stage cmdline/DT/init consumer is preserved.
- **fallback blindness:** the first candidate fails and the later successful boot path is missed because the analyst stopped at the first plausible config.

## Useful outputs
- boot-chain table: bootdev -> bootmeth -> bootflow/config -> attempt result
- environment provenance table: default / saved / current / expanded values
- loaded tuple statement: kernel + initrd + FDT + overlays + rootfs/slot + cmdline
- verified-boot claim scope: image hash, image signature, signed config, key trust, fallback behavior
- next-stage consumption packet: early log, `/proc/cmdline`, live DT, init/service effect
- one first-consumer statement or a clear gap to resolve next

## Sources / provenance
- `sources/protocol/2026-05-10-firmware-bootloader-selection-executed-image-notes.md`
- U-Boot, `Environment Variables` — https://docs.u-boot.org/en/latest/usage/environment.html
- U-Boot, `Standard Boot Overview` — https://docs.u-boot.org/en/latest/develop/bootstd/overview.html
- U-Boot, `Generic Distro Configuration Concept` — https://docs.u-boot.org/en/latest/develop/distro.html
- U-Boot, `bootm command` — https://docs.u-boot.org/en/v2024.04/usage/cmd/bootm.html
- U-Boot, `Flat Image Tree (FIT)` — https://docs.u-boot.org/en/stable/usage/fit/index.html
- U-Boot, `U-Boot Verified Boot` — https://docs.u-boot.org/en/latest/usage/fit/verified-boot.html
- U-Boot, `U-Boot FIT Signature Verification` — https://docs.u-boot.org/en/latest/usage/fit/signature.html
- Linux kernel docs, `The kernel's command-line parameters` — https://docs.kernel.org/admin-guide/kernel-parameters.html
