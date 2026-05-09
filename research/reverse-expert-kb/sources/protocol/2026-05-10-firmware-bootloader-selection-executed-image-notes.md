# Firmware bootloader selection -> executed image notes — 2026-05-10

Scope: source-backed notes for a practical firmware / U-Boot-shaped seam where the analyst already has bootloader environment, bootflow, extlinux, FIT, or boot logs, but still needs to prove which boot object was actually selected, verified, handed off, and consumed.

## Source-backed observations

### U-Boot environment is configuration / setup evidence, not execution truth
U-Boot documents environment variables as user configuration that may exist in an in-memory copy or be saved persistently to flash. Default environment can also be supplied by board `.env` files or older C environment definitions.

Practical implication:
- `bootcmd`, `bootargs`, `boot_targets`, `bootmeths`, `fdtfile`, and related variables are important boot-chain evidence
- but environment text alone does not prove that this boot executed that variable value, that persistent storage matched the current in-memory environment, or that a later boot stage consumed the resulting arguments

High-signal source:
- U-Boot, `Environment Variables` — https://docs.u-boot.org/en/latest/usage/environment.html

### Standard Boot / bootflow selection separates boot device, method, bootflow, and actual boot attempt
U-Boot Standard Boot defines `bootdev`, `bootmeth`, and `bootflow` separately. It scans boot devices and boot methods, finds bootflows, and tries to boot them. Ordering can be influenced by environment variables such as `boot_targets` and `bootmeths`; global boot methods such as VBE and EFI boot manager may participate separately.

Practical implication:
- a found `extlinux.conf`, EFI entry, bootflow listing, or selected `boot_targets` order is only part of the proof
- a reverse run should preserve which device/method/bootflow was enumerated, which one was attempted, which one failed or fell through, and which one actually reached handoff

High-signal source:
- U-Boot, `Standard Boot Overview` — https://docs.u-boot.org/en/latest/develop/bootstd/overview.html

### extlinux / distro boot config is a boot description, not a consumed runtime state claim
U-Boot's distro configuration model loads boot configuration files such as `/extlinux/extlinux.conf` or `/boot/extlinux/extlinux.conf`, with entries naming kernel, initrd, FDT / FDT directory, overlays, and `append` command-line material. The docs explicitly note that `append` can use environment variables, including A/B slot-like cases.

Practical implication:
- extlinux lines are candidate bootflow contract material
- if environment substitution, default labels, fallback, or multiple partitions are possible, the analyst still needs evidence of the chosen label, selected slot, effective kernel/initrd/FDT tuple, and final kernel command line

High-signal source:
- U-Boot, `Generic Distro Configuration Concept` — https://docs.u-boot.org/en/latest/develop/distro.html

### `bootm` separates current load address, FIT configuration, subimages, initrd, FDT, and handoff form
The `bootm` command can boot legacy images or FIT images. FIT form can name a configuration (`#conf`), subimages (`:kernel-1`), extra configurations/overlays, initrd, and FDT objects. When arguments are omitted, current image address and same-FIT defaults can affect what is used.

Practical implication:
- a memory address, load command, FIT blob, or `bootm` string is not by itself the executed OS tuple
- freeze the selected FIT configuration and image components before naming the executed kernel or DTB

High-signal source:
- U-Boot, `bootm command` — https://docs.u-boot.org/en/v2024.04/usage/cmd/bootm.html

### FIT / verified boot adds configuration and key-trust proof objects
U-Boot's FIT docs frame FIT as a standard packaging format for images U-Boot reads and boots. Verified boot documentation separates signed images, public keys stored in a trusted place, and verification. FIT signature docs further distinguish image hashes/signatures, signed configurations, required keys, and mix-and-match / rollback style risks.

Practical implication:
- `hash ok`, `signature ok`, signed image nodes, or a trusted-key node are not the same proof object as selected configuration, accepted policy, and handoff to the kernel
- when security posture matters, preserve whether a single image hash, signed image, signed configuration, required key, or chain-of-trust stage is being proved

High-signal sources:
- U-Boot, `Flat Image Tree (FIT)` — https://docs.u-boot.org/en/stable/usage/fit/index.html
- U-Boot, `U-Boot Verified Boot` — https://docs.u-boot.org/en/latest/usage/fit/verified-boot.html
- U-Boot, `U-Boot FIT Signature Verification` — https://docs.u-boot.org/en/latest/usage/fit/signature.html

### Kernel command line is a later consumer surface
Linux kernel docs treat the command line as parsed by `__setup()`, `early_param()`, `core_param()`, and module parameters; unrecognized material can pass onward to init. `/proc/cmdline` and module parameter exposure can therefore act as later-stage consumer evidence when U-Boot `bootargs` / extlinux `append` material is suspected.

Practical implication:
- comparing bootloader-side `bootargs` / `append` text to `/proc/cmdline`, early boot logs, and init/service behavior can distinguish configured intent from consumed runtime truth
- do not treat a bootloader variable as consumed until the next stage demonstrates it or the handoff path is directly observed

High-signal source:
- Linux kernel docs, `The kernel's command-line parameters` — https://docs.kernel.org/admin-guide/kernel-parameters.html

## Durable proof split

```text
bootloader env / boot config found
  != bootdev / bootmeth / bootflow selected
  != kernel / initrd / FDT / overlay tuple loaded
  != FIT configuration and signature / policy accepted
  != command line / device tree handed off
  != kernel / init / service consumed that state
  != first behavior-bearing effect proved
```

Compact branch memory:

```text
env/config != selected bootflow != loaded tuple != verified policy != handed off != consumed/effected
```

## Suggested operator evidence package

- boot source table: boot device, partition, bootmeth, bootflow / extlinux label / EFI entry / FIT config
- environment evidence: persistent vs in-memory env, `bootcmd`, `bootargs`, `boot_targets`, `bootmeths`, variables used by config substitution
- loaded tuple: kernel, initrd, FDT, overlays, FIT config/subimages, current load address if `bootm` defaults matter
- policy evidence: hash/signature logs, required key, signed image vs signed configuration, fallback or failure path
- handoff evidence: final command line, FDT path or live FDT marker, early kernel log, `/proc/cmdline`, init/service effect
- compare pair: same boot config with changed environment / selected slot / fallback device, then observe final cmdline and first behavior-bearing consumer
