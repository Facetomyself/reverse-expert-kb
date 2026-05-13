# Firmware Android A/B slot rollback to stable-runtime workflow note

Topic class: workflow note
Ontology layers: firmware boot chain, Android A/B slot state, AVB rollback policy, runtime consumer proof
Maturity: structured-practical
Related pages:
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-firmware-practical-subtree-guide.md
- topics/firmware-bootloader-selection-to-executed-image-workflow-note.md
- topics/firmware-uefi-boot-manager-to-loader-handoff-workflow-note.md
- topics/firmware-hardware-observation-to-executed-image-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/analytic-provenance-and-evidence-management.md
- sources/protocol/2026-05-14-android-ab-slot-rollback-notes.md

## Why this matters

Android A/B and AVB evidence is easy to overread. A reverser may see slot metadata, `bootctl` output, `androidboot.slot_suffix=`, `vbmeta_a`, an AVB verification log, a rollback index, or an update-engine state and quietly upgrade it to:

```text
this exact slot is the stable runtime that owns the behavior
```

That jump is too large. A/B metadata, active-for-next selection, current boot suffix, loaded slot tuple, AVB / rollback policy, userspace consumption, and successful-boot marking are separate proof objects.

This note preserves the Android-shaped boot-chain seam that sits next to the U-Boot / extlinux / FIT and UEFI boot-manager workflow notes.

## Scope

Use this note when:
- an Android, Android-derived, ChromeOS-like, or embedded A/B-slot target exposes slot metadata, Boot Control HAL / `bootctl` state, fastboot slot state, `misc` / bootloader-control-block material, `androidboot.slot_suffix=`, `ro.boot.slot_suffix`, AVB / vbmeta material, rollback indexes, or update-engine state
- the current uncertainty is which slot was active, which slot actually booted, whether verification / rollback policy accepted it, whether userspace consumed the slot state, and whether the boot was marked successful or later retried/retired
- the analyst needs one boot-chain evidence unit before interpreting firmware, update, persistence, protocol, or runtime behavior

Do not use it as:
- an Android flashing tutorial
- a downgrade / rollback bypass guide
- a replacement for hardware/image-lineage proof when acquired bytes still do not map to the current device
- a kernel/rootcause workflow once selected slot, verification, handoff, and userspace consumption are already trustworthy

## Investigation frame

- **Target:** Android A/B boot path, including U-Boot Android A/B integrations and AVB-enabled embedded targets.
- **Boundary:** A/B metadata -> active slot selection -> current slot suffix -> loaded slot image tuple -> AVB / rollback policy -> kernel/userspace slot-state consumption -> successful/stable boot -> first behavior owner.
- **Observation surface:** `misc` / bootloader control block, bootloader logs, fastboot variables, Boot Control HAL / `bootctl`, U-Boot `bcb ab_select`, `androidboot.slot_suffix=`, `/proc/cmdline`, `ro.boot.slot_suffix`, AVB logs, vbmeta digest, rollback-index storage, update_engine logs, init/service traces.
- **Artifact goal:** one trustworthy statement of which slot and verified image set reached the behavior under analysis, including policy result, userspace consumption, and success/retire state if relevant.
- **Cheapest next discriminant:** compare active-for-next slot, current boot suffix, AVB result, and userspace `ro.boot.slot_suffix` / update-engine state before widening static analysis.

## Core proof ladder

```text
A/B metadata / bootloader-control artifact visible
  != active slot selected for next boot
  != current slot suffix passed by bootloader
  != slot image tuple loaded
  != AVB / rollback policy accepted it
  != kernel/userspace consumed suffix/root/vbmeta state
  != boot marked successful or slot retired/unbootable
  != observed behavior owned by that slot
```

Compact branch memory:

```text
metadata != active != current != verified != consumed != successful/stable != effect-owned
```

## Practical workflow

### 1. Name the slot evidence without upgrading it

Classify the artifact precisely:

| Evidence | What it can support | What it does not automatically prove |
| --- | --- | --- |
| `misc` / bootloader control block / A/B metadata | slot priorities, retry/success/bootable-style state, updater intent | current boot, verified acceptance, stable userspace behavior |
| fastboot active slot | bootloader's selected next-boot slot view | current running slot, successful boot, later effect ownership |
| Boot Control HAL / `bootctl` current slot | OS view of the slot passed by bootloader | active-for-next state, old attempted slot history, AVB acceptance details |
| `androidboot.slot_suffix=` | kernel command-line handoff of a slot suffix | which bootloader decision produced it, all slotted partitions consumed, stable boot |
| `ro.boot.slot_suffix` | Android property derived from boot state | image identity, rollback acceptance, update success |
| `isSlotMarkedSuccessful` / success bit | slot was marked successful | exact behavior owner, absence of earlier failed boot attempts |
| AVB / vbmeta digest | verified metadata and image lineage evidence | active slot selection or userspace stability by itself |
| rollback index | anti-rollback policy state | selected slot, handoff success, current behavior owner |

Stop rule:

```text
slot evidence found != stable runtime slot proved
```

### 2. Separate active-for-next from current boot

Preserve:
- the slot intended for the next boot: fastboot active slot, Boot Control HAL `setActiveBootSlot(...)`, bootloader metadata write, or updater state
- the slot actually booted this run: bootloader-selected suffix, `androidboot.slot_suffix=`, `/firmware/android/slot_suffix`, `getCurrentSlot()`, `ro.boot.slot_suffix`
- retry / priority / bootable / unbootable state when available
- whether the device fell back after a failed boot attempt before the observed runtime

Important compare:

```text
active slot before reboot
  vs current slot suffix
  vs bootloader fallback / retry evidence
  vs userspace update-engine state
```

If the active slot and current slot disagree, do not explain the case from static slot metadata alone. Treat fallback, retry exhaustion, slot-unbootable marking, or manual slot selection as live hypotheses until one is discriminated.

### 3. Resolve the slot image tuple, not just the suffix

A suffix is a selector, not the bytes. Bind the slot to the image set that matters:
- `boot_a` / `boot_b`, `vendor_boot_a` / `vendor_boot_b`, `dtbo_a` / `dtbo_b`, `vbmeta_a` / `vbmeta_b`, `system` / `vendor` / logical partitions when slotted or dynamic
- partition GUID / block device / logical-partition mapping at boot time
- image hashes, vbmeta digest, build fingerprint, timestamp, OTA package provenance
- rootfs and dynamic partition mapping consumed by init / mount / dm-verity

Stop rule:

```text
slot suffix != current image tuple != behavior-bearing runtime bytes
```

This matters when an analyst compares two slots, inspects an inactive partition, or assumes that `slot_a` and `slot_b` differ only in the file under current inspection.

### 4. Treat AVB and rollback as policy evidence, not slot truth

AVB / rollback evidence can answer:
- was the VBMeta chain cryptographically accepted?
- which descriptors and chained partitions were used?
- which rollback index locations were checked?
- were stored rollback indexes advanced or only compared?
- did verification failure halt, fallback, unlock-warning boot, or select another slot?

Do not collapse:

```text
AVB accepted != selected slot proved != userspace stable != effect-owned
rollback index advanced != all later behavior belongs to the new slot
```

If rollback evidence matters, preserve both sides:
- image rollback index from the relevant vbmeta / chained vbmeta
- stored rollback index location and current value, often in tamper-evident storage / RPMB / TEE-backed storage depending on integration

### 5. Use userspace consumption as the next-stage check

The cheapest strong discriminants are often in the next stage:
- `/proc/cmdline` and `ro.boot.slot_suffix` confirm the suffix Android consumed
- `bootctl get-current-slot`, `bootctl is-slot-marked-successful`, and `bootctl is-slot-bootable` confirm the userspace-facing view, not all bootloader history
- update_engine logs show whether post-install, first boot, merge, or success-marking logic ran
- init / mount / dm-verity logs show whether the expected root / dynamic partition mapping was consumed
- app/service behavior under the trigger proves the first effect-bearing consumer

Stop rule:

```text
current suffix consumed != boot marked successful != behavior owner proved
```

A first boot after OTA can execute enough userspace to expose useful artifacts and still not yet be marked successful or stable.

### 6. Package one Android A/B boot-chain evidence unit

Before widening into static reverse engineering, package:

```text
A/B metadata source and state
  + active-for-next slot
  + current boot suffix
  + resolved slot image tuple
  + AVB / rollback policy result if relevant
  + kernel/userspace consumed-state observation
  + successful / unbootable / retry state
  + first behavior-bearing consumer or explicit gap
```

This prevents later protocol, persistence, or update analysis from silently rediscovering the same slot/handoff ambiguity.

## Common failure modes

- **active-slot overread:** fastboot or updater says slot B is active, so slot B is treated as the current runtime without checking bootloader suffix and userspace state.
- **current-slot overread:** `ro.boot.slot_suffix=_a` is treated as proof that the inspected `boot_a` / `system_a` bytes match the booted image without hashing or partition mapping.
- **success-bit overread:** a marked-successful slot is treated as proof of the specific behavior under analysis, even though the behavior may be owned by a later service, dynamic partition, or persisted state.
- **AVB overread:** successful verification is treated as slot selection proof rather than policy acceptance for whichever slot tuple was verified.
- **rollback overread:** rollback-index evidence is treated as a complete boot-chain narrative rather than one acceptance/rejection gate.
- **fallback blindness:** the analyst ignores retry exhaustion or slot-unbootable transitions and explains the observed runtime from the originally requested slot.

## Minimal evidence questions

Ask these before making a durable claim:

1. Which artifact says the slot was active for next boot?
2. Which artifact says which slot actually booted this run?
3. Which partition/image tuple did that suffix resolve to at boot time?
4. Did AVB and rollback policy accept that exact tuple, and what was the failure behavior if not?
5. Did kernel and userspace consume the same suffix/root/vbmeta state?
6. Was the slot marked successful, retried, retired, or made unbootable after the observed boot?
7. Which first behavior-bearing consumer proves the runtime effect belongs to that slot rather than to stale persisted state or a later service?

## Source-backed anchors

- AOSP A/B docs: A/B updates use redundant partition sets; the running system uses one slot while the inactive slot can be updated, and a successful slot should be able to boot, run, and update.
- Boot Control HAL: exposes current slot, active boot slot selection, successful marking, unbootable marking, bootable queries, successful queries, and suffix lookup; the comments explicitly distinguish current slot from active/successful/bootable concepts.
- AVB README: rollback protection compares image rollback indexes against stored rollback indexes and advances stored values over time; AVB is A/B-aware and partition descriptor names avoid slot suffixes.
- U-Boot Android A/B docs: `bcb ab_select` reads A/B metadata from `misc` and emits a slot suffix that can feed `androidboot.slot_suffix=` / `root=`.
- U-Boot AVB docs: `avb verify [slot_suffix]` gates continuation and rollback-index commands expose the policy object separately from handoff.

## When to hand off to another note

- If the acquired firmware or partition dump may not be from the current device at all, use `firmware-hardware-observation-to-executed-image-workflow-note.md` first.
- If the case is U-Boot/extlinux/FIT-shaped and A/B is only one variable inside a broader boot script, pair this note with `firmware-bootloader-selection-to-executed-image-workflow-note.md`.
- If the case is UEFI-shaped rather than Android A/B-shaped, use `firmware-uefi-boot-manager-to-loader-handoff-workflow-note.md`.
- If slot and boot-chain evidence is trustworthy and the blocker is a parser, protocol, IPC, service, or hardware-side effect, move into the appropriate protocol / runtime / native note instead of continuing boot-chain archaeology.
