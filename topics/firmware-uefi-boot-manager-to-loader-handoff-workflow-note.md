# Firmware UEFI boot-manager to loader handoff workflow note

Topic class: workflow note
Ontology layers: firmware boot chain, UEFI boot manager, loader handoff proof, runtime consumer proof
Maturity: structured-practical
Related pages:
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-firmware-practical-subtree-guide.md
- topics/firmware-bootloader-selection-to-executed-image-workflow-note.md
- topics/firmware-hardware-observation-to-executed-image-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/analytic-provenance-and-evidence-management.md
- sources/protocol/2026-05-13-uefi-boot-manager-loader-handoff-notes.md

## Why this matters

UEFI boot evidence is easy to overread. A reverser may see `Boot0007`, `BootOrder`, `BootNext`, an EFI System Partition path, a Secure Boot state, or OS-side `BootCurrent` and quietly upgrade it to:

```text
this exact loader and later runtime path executed
```

That jump is too large. UEFI boot-manager state describes candidates, order, one-shot overrides, active flags, device paths, optional data, and sometimes policy posture. It does not by itself prove which loader bytes were resolved, loaded, verified, started, handed off to an OS, or consumed by the behavior under analysis.

This note preserves the UEFI-shaped boot-chain seam that sits next to the U-Boot / extlinux / FIT bootloader-selection workflow. It is for desktop/server firmware cases and embedded cases where U-Boot is using `bootefi bootmgr` or UEFI variable semantics.

## Scope

Use this note when:
- `Boot####`, `BootOrder`, `BootNext`, `BootCurrent`, `Timeout`, an EFI System Partition path, a NVRAM boot entry, `efibootmgr` output, U-Boot `eficonfig`, `bootefi bootmgr`, Secure Boot variables, or firmware boot logs are visible
- the current uncertainty is which boot entry, device path, loader image, policy result, and next-stage handoff actually correspond to the observed boot
- the analyst needs one boot-chain evidence unit before interpreting kernel, bootloader, bootkit, protocol, or runtime behavior

Do not use it as:
- a boot configuration tutorial
- a Secure Boot bypass guide
- a replacement for hardware/image-lineage proof when the acquired firmware bytes still do not map to the current machine
- a UEFI module internals workflow once the loader/handoff path is already trustworthy

## Investigation frame

- **Target:** UEFI desktop/server/embedded boot path, including U-Boot systems using UEFI boot options.
- **Boundary:** UEFI boot-manager variables -> selected boot option -> device-path resolution -> loader image start -> verification/policy result -> OS or next-loader handoff -> first runtime consumer.
- **Observation surface:** firmware setup / boot log, UEFI shell, `efibootmgr -v`, `/sys/firmware/efi/efivars`, ESP contents, device paths, Secure Boot state/variables, loader logs, `BootCurrent`, kernel command line, init/service traces.
- **Artifact goal:** one trustworthy statement of which boot option and loader image reached the behavior under analysis, including policy result and next-stage consumption if relevant.
- **Cheapest next discriminant:** compare `BootCurrent` / boot-log attempt evidence with `BootOrder` / `BootNext` / ESP file identity before widening static analysis.

## Core proof ladder

```text
Boot#### entry visible
  != active and ordered candidate selected
  != BootNext / timeout / UI override resolved
  != device path resolved to current ESP / file / network target
  != loader image loaded and started
  != Secure Boot / verification policy accepted the image
  != loader handed off kernel/initrd/root/cmdline state
  != OS/runtime consumed it in the behavior under analysis
```

Compact branch memory:

```text
entry != selected != resolved != loaded != verified != handed off != consumed/effected
```

## Practical workflow

### 1. Name the boot-manager evidence without upgrading it

Classify the artifact precisely:

| Evidence | What it can support | What it does not automatically prove |
| --- | --- | --- |
| `Boot####` variable | a candidate load option, description, attributes, device path, optional data | active selection, successful load, current runtime path |
| `LOAD_OPTION_ACTIVE` / active flag | candidate is eligible for automatic attempt | it was the winning entry, or returned no failure |
| `BootOrder` | ordered candidate list | first listed entry succeeded, no fallback occurred |
| `BootNext` | one-shot next-boot override | durable boot order, post-boot persistence, later behavior ownership |
| `Timeout` / UI selection | possible automatic or manual selection window | which choice happened without logs/current-state evidence |
| `BootCurrent` | OS-side correlation to the entry used to start the current system | exact loader bytes, policy result, rootfs/cmdline consumption, later effect |
| ESP file path | candidate loader location | file identity at boot time, device-path resolution, verification, handoff |

Stop rule:

```text
UEFI boot entry found != selected boot path proved
```

### 2. Resolve selection before loader identity

Before naming a loader as executed, preserve:
- `BootNext` one-shot override versus ordinary `BootOrder`
- active/inactive state of the selected entry
- firmware UI/manual selection if logs imply human or setup-screen intervention
- timeout behavior and fallback after failed return status
- whether the entry is OS loader, UEFI shell, diagnostic utility, network boot, recovery loader, or another boot manager

Important compare:

```text
BootOrder first active entry
  vs BootNext
  vs BootCurrent
  vs boot log / firmware event log
```

If `BootNext` existed before boot, do not let the persisted `BootOrder` alone explain the current runtime. If `BootCurrent` names a later entry, treat earlier entries as attempted-or-skipped candidates until failure/return evidence is available.

### 3. Resolve device path to current bytes

UEFI load options carry device-path information. For evidence packaging, bind the path to bytes:
- disk/GPT identity, partition GUID, filesystem, or network target
- ESP mount that corresponds to the firmware path, not just a similar OS mount point
- loader path such as `\\EFI\\vendor\\loader.efi`, fallback path, shim, GRUB/systemd-boot/Windows Boot Manager, network image, or recovery utility
- file hash / timestamp / package provenance when bootkit, tampering, or update lineage matters
- optional data / command-line-like fields passed to the EFI application

Stop rule:

```text
device path string != current file identity != loaded image identity
```

A stale `efibootmgr -v` path can be real configuration and still not identify the bytes that were present during the boot under analysis.

### 4. Separate loader start from successful handoff

A boot option can be launched and still return to the boot manager or fail before OS handoff. Preserve:
- load/start attempt evidence
- return status or fallback evidence if available
- whether the target is a final OS loader or an intermediate manager such as shim, GRUB, Windows Boot Manager, systemd-boot, iPXE, recovery utility, or UEFI shell
- any second-stage config selected by that loader
- kernel/initrd/root/cmdline or chainloaded target it eventually handed off

Stop rule:

```text
loader started != OS/runtime handoff succeeded
```

If a boot entry starts shim/GRUB/systemd-boot, the next proof object is the loader's selected target, not the original `Boot####` entry alone.

### 5. Treat Secure Boot / verification as policy evidence, not runtime proof

Secure Boot variables and status can matter, but keep them separate:
- setup/user/deployed mode and Secure Boot enabled state
- PK/KEK/db/dbx or platform trust anchors when relevant
- whether the loader image was signed, measured, blocked, shim-verified, or chain-verified
- whether a failure caused fallback to another boot option
- whether measured boot / TPM event logs are needed for stronger lineage

Stop rule:

```text
Secure Boot enabled != this loader accepted != this later runtime behavior owned by it
```

Policy acceptance helps explain why a path could run. It does not by itself prove that the path did run or that the later behavior is owned by that path.

### 6. Use the next stage as the consumption check

Once the selected entry and loader bytes are plausible, move one step forward:
- `BootCurrent` plus boot logs can correlate current OS to an entry
- kernel command line and initrd/root selection can prove loader-to-kernel handoff content
- bootloader logs can show selected menu entry, timeout choice, or fallback
- init/service logs can prove rootfs, boot mode, recovery mode, or feature flag consumption
- runtime behavior under the trigger proves the first behavior-bearing consumer

Stop rule:

```text
handoff happened != behavior-bearing consumer proved
```

Do not keep re-reading NVRAM variables if the missing proof object has shifted to loader menu selection, kernel command line, initramfs behavior, root filesystem choice, or service-level consumption.

### 7. Package one UEFI boot evidence unit

Before handing the case to kernel, protocol, malware, bootkit, or runtime analysis, package:

```text
Boot#### id + description + attributes
  + BootNext/BootOrder/BootCurrent relationship
  + device path -> current byte identity
  + loader-start / fallback evidence
  + verification / policy result if relevant
  + next-stage handoff tuple
  + first runtime consumer or explicit gap
```

This makes later claims auditable and prevents rediscovering the same boot path after every confusing static or runtime observation.

## Common failure modes

- **entry overread:** `Boot####` exists, so the analyst claims it ran.
- **order overread:** the first `BootOrder` entry is treated as the winning path even though `BootNext`, manual UI selection, inactive flags, or fallback may have changed the current boot.
- **path overread:** an ESP path is treated as loaded bytes without verifying partition identity and file provenance.
- **loader overread:** shim/GRUB/systemd-boot/Windows Boot Manager start is treated as final kernel/rootfs selection.
- **policy overread:** Secure Boot state or signature presence is treated as proof of current execution or later behavior ownership.
- **current-state overread:** `BootCurrent` is treated as proof of exact loader bytes and all downstream config rather than as one strong correlation surface.

## Useful outputs

- boot-entry evidence table: `Boot####`, attributes, order, next/current, device path, optional data
- device-path-to-byte provenance record: partition GUID, ESP path, file hash, package/update origin
- loader handoff map: entry -> EFI application -> second-stage config -> kernel/initrd/root/cmdline or next-loader target
- verification/policy note: Secure Boot / shim / measured-boot evidence and what it proves
- runtime-consumer note: first kernel/init/service/behavior surface that consumed the handoff state

## Sources / provenance

- `sources/protocol/2026-05-13-uefi-boot-manager-loader-handoff-notes.md`
- UEFI Specification, Boot Manager chapter — `https://uefi.org/specs/UEFI/2.10/03_Boot_Manager.html`
- TianoCore EDK II Driver Writer's Guide, boot option processing — `https://raw.githubusercontent.com/tianocore-docs/edk2-UefiDriverWritersGuide/master/3_foundation/315_platform_initialization/31512_boot_manager_boot_option_processing.md`
- `efibootmgr(8)` manual — `https://man.archlinux.org/man/efibootmgr.8.en`
- U-Boot `eficonfig` command — `https://docs.u-boot.org/en/stable/usage/cmd/eficonfig.html`
