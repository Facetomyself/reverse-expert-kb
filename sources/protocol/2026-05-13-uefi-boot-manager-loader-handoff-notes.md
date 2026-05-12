# Source notes — UEFI Boot#### / BootOrder to loader handoff

Date: 2026-05-13
Branch: protocol / firmware practical workflows
Run artifact: `sources/protocol/2026-05-13-0450-uefi-boot-manager-search-layer.json`

## Scope

These notes support a defensive reverse-engineering workflow for UEFI boot-manager evidence. The narrow question is not how to configure a boot entry, but how to avoid overreading `Boot####`, `BootOrder`, `BootNext`, EFI System Partition paths, Secure Boot state, or `BootCurrent` into proof that one loader image and later OS/runtime behavior actually executed.

## High-signal source points

### UEFI Boot Manager specification

Source:
- UEFI Specification, Boot Manager chapter — `https://uefi.org/specs/UEFI/2.10/03_Boot_Manager.html`

Useful points from the search/extraction pass:
- UEFI load options such as `Boot####` describe boot candidates.
- `LOAD_OPTION_ACTIVE` matters: the boot manager attempts active load options automatically using device-path information.
- Boot-manager evidence therefore has at least three separate claims: entry exists, entry is active/eligible, and entry was actually attempted.

Practical inference:
- a discovered `Boot####` variable is only candidate-entry truth until order, active state, one-shot override, and attempt/handoff evidence are tied to the observed boot.

### TianoCore EDK II Driver Writer's Guide — boot option processing

Source:
- `https://raw.githubusercontent.com/tianocore-docs/edk2-UefiDriverWritersGuide/master/3_foundation/315_platform_initialization/31512_boot_manager_boot_option_processing.md`

Useful points:
- the platform boot manager enumerates boot options by reading `BootOrder` and `Boot####` variables.
- a boot option is typically an OS loader, but can also be another UEFI application such as diagnostics or the UEFI shell.
- if a boot option returns and its return status is not `EFI_SUCCESS`, the boot manager processes the next boot option until an OS is booted, success is returned, or the list is exhausted.
- the boot manager uses the device path in each boot option to ensure the required device is present in the UEFI handle database.

Practical inference:
- `BootOrder` is not a single selected-loader proof. Fallback and return-status behavior mean the first listed entry can be only a failed attempt; device-path resolution and handle availability are distinct proof objects.

### efibootmgr manual

Source:
- `https://man.archlinux.org/man/efibootmgr.8.en`

Useful points:
- `efibootmgr` manipulates UEFI Boot Manager configuration and needs kernel access to EFI non-volatile variables through `/sys/firmware/efi/vars` or `/sys/firmware/efi/efivars/`.
- displayed variables include `BootCurrent`, `BootOrder`, `BootNext`, `Timeout`, and individual `Boot####` entries.
- `BootCurrent` is the boot entry used to start the currently running system.
- `BootOrder` is the order tried by the boot manager; if the first active entry is unsuccessful, the next entry is tried.
- `BootNext` schedules the next-running boot option for one boot only, supersedes `BootOrder`, and is deleted after first use.
- `Boot####` entries include active/inactive state and display labels.

Practical inference:
- OS-side `BootCurrent` is a strong next-stage correlation surface, but it is still not full proof of the exact loaded PE/EFI image bytes, Secure Boot policy result, bootloader-internal config, kernel/initrd/root selection, or later behavior-bearing consumer.

### U-Boot `eficonfig` / `bootefi bootmgr`

Source:
- `https://docs.u-boot.org/en/stable/usage/cmd/eficonfig.html`

Useful points:
- U-Boot's `eficonfig` edits UEFI boot options stored in `Boot####`; new options are appended to `BootOrder` unless the user changes order.
- `bootefi bootmgr` boots by trying boot options selected by `BootOrder` in sequence.
- U-Boot can store EFI variables on tamper-resistant media through OP-TEE / RPMB when configured.
- `eficonfig` can edit Secure Boot variables such as PK, KEK, db, and dbx when secure-boot support is enabled.

Practical inference:
- UEFI-style boot-manager evidence can appear inside U-Boot-shaped embedded cases too. Do not collapse U-Boot `bootefi bootmgr` configuration into current OS handoff until the entry, order, device path, policy, and next-stage consumed state are correlated.

### UEFI reversing practice sources

Sources:
- SentinelLabs, UEFI module emulation result from search — `https://www.sentinelone.com/labs/moving-from-manual-reverse-engineering-of-uefi-modules-to-dynamic-emulation-of-uefi-firmware/`
- Jethro Beekman, “Reverse Engineering UEFI Firmware” — `https://jbeekman.nl/blog/2015/03/reverse-engineering-uefi-firmware/`

Useful points:
- UEFI images are PE-format modules; firmware behavior depends on a services/protocol environment rather than a normal dynamic linker model.
- Reversing UEFI modules often requires reconstructing GUID/protocol dependencies and runtime services, not only reading a static PE image.

Practical inference:
- once boot-manager handoff is proved, deeper UEFI-module reverse work may need protocol-service reconstruction. That is a separate next object from proving that a `Boot####` entry launched.

## Operator synthesis

Preserve the proof ladder:

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

The practical stop rule is: do not write “this boot path executed” from `Boot####` / `BootOrder` alone. Freeze `BootCurrent` or boot-log attempt evidence, device-path-to-file/ESP identity, loader-image provenance, policy result if security matters, and one next-stage consumption surface before handing the case to kernel, bootkit, protocol, or runtime analysis.
