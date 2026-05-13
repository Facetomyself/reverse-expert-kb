# Source notes — Android A/B slot selection, AVB rollback, and successful-boot proof (2026-05-14)

## Scope

Bounded source notes for the protocol / firmware branch on Android A/B slot state, Boot Control HAL surfaces, AVB rollback indexes, U-Boot Android A/B support, and what an analyst can and cannot infer from those artifacts.

The practical target is not an Android update tutorial. It is a reverse-analysis proof split for cases where slot metadata, active slot, boot-success state, AVB verification, rollback indexes, and userspace consumption can be mistaken for one another.

## Search artifact

- `sources/protocol/2026-05-14-0450-android-ab-slot-rollback-search-layer.json`

Search sources requested explicitly through `search-layer --source exa,tavily,grok`.

## High-signal external references

- Android A/B seamless updates — `https://source.android.com/docs/core/ota/ab`
- Android A/B implementation — `https://source.android.com/docs/core/ota/ab/ab_implement`
- Android Boot Control HAL `IBootControl.hal` — `https://android.googlesource.com/platform/hardware/interfaces/+/refs/heads/android16-qpr2-release/boot/1.0/IBootControl.hal`
- Android Verified Boot / AVB README — `https://android.googlesource.com/platform/external/avb/+/refs/heads/master/README.md`
- U-Boot Android A/B updates — `https://docs.u-boot.org/en/stable/android/ab.html`
- U-Boot Android Verified Boot 2.0 — `https://docs.u-boot.org/en/latest/android/avb2.html`

## Extracted details with operator value

### Android A/B updates separate current, active, and successful slot concepts

AOSP A/B update documentation describes two sets of partitions where the system runs from the current slot while the inactive slot can be updated. The inactive slot may be marked active for the next boot, but the running system still needs to survive the first boot and mark the slot successful. A slot that is selected for next boot is therefore not automatically the same proof object as a slot that successfully reached stable userspace.

Analyst implication:

```text
slot metadata visible != selected for next boot != currently booted slot != marked successful != stable runtime consumed it
```

### Boot Control HAL is a useful observation surface, but not a complete boot-chain proof

The Boot Control HAL exposes methods such as:
- `getNumberSlots()`
- `getCurrentSlot()`
- `markBootSuccessful()`
- `setActiveBootSlot(slot)`
- `setSlotAsUnbootable(slot)`
- `isSlotBootable(slot)`
- `isSlotMarkedSuccessful(slot)`
- `getSuffix(slot)`

The HAL comments preserve useful distinctions:
- `getCurrentSlot()` returns the slot the current boot is booted from and must match the suffix passed from the bootloader
- `markBootSuccessful()` marks the current slot as successfully booted
- `setActiveBootSlot()` marks a slot as active for boot and overrides unbootable state
- a slot may be bootable or unbootable independently of whether it is marked successful
- the bootloader passes the suffix through `androidboot.slot_suffix` or `/firmware/android/slot_suffix`

Analyst implication:

```text
HAL current slot != active-for-next slot != bootable bit != successful bit != behavior owner
```

### AVB rollback protection is a separate proof object from slot selection

AVB’s README states that rollback protection uses rollback indexes baked into VBMeta structs and stored rollback indexes in tamper-evident storage. The device rejects an image unless each image rollback index is greater than or equal to the stored rollback index, and stored rollback indexes increase over time. The same README notes A/B support where partition descriptor names omit slot suffixes and slot-specific VBMeta / rollback data may differ.

Analyst implication:

```text
selected slot != AVB verification accepted != rollback index accepted/advanced != later userspace stable
```

Rollback evidence can prove why an image could be accepted or rejected. It does not by itself prove the slot was selected, that handoff happened, or that the later behavior under analysis belongs to that slot.

### U-Boot Android A/B and AVB make the seam visible in embedded cases

U-Boot’s Android A/B documentation describes `bcb ab_select` reading A/B metadata from a special partition such as `misc`, determining a slot, and then generating next kernel command-line parameters such as `androidboot.slot_suffix=` and `root=`. U-Boot’s AVB 2.0 documentation exposes `avb verify [slot_suffix]`, rollback-index read/write commands, and example boot scripts where AVB verification gates continuation before `bootm`.

Analyst implication:

```text
bcb ab_select chose suffix != avb verify accepted != bootm handed off != kernel consumed suffix/root != update_engine marked success
```

This is the Android-shaped sibling of the U-Boot and UEFI boot-chain notes, not a replacement for them.

## Practical synthesis

The useful workflow split for Android A/B / AVB cases is:

```text
A/B metadata / bootloader control block visible
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

## Evidence package candidates

For a real case, collect:
- A/B metadata source and timestamp: `misc` / bootloader control block / vendor boot metadata / fastboot slot state
- active slot, current slot, bootable bit, successful bit, retry/priority fields when available
- bootloader logs or command-line evidence for `androidboot.slot_suffix=` and root partition
- resolved `boot_a` / `boot_b`, `vbmeta_a` / `vbmeta_b`, vendor/system slots, dynamic partition mapping, and image hashes
- AVB verification result, vbmeta digest, rollback index locations and stored rollback posture when relevant
- kernel `/proc/cmdline`, boot properties, `ro.boot.slot_suffix`, update_engine / bootctl state, and first userspace consumer of the state
- explicit gap if the case stops before `markBootSuccessful()` or before proving behavior ownership

## Confidence and caveats

Confidence is moderate-to-high for the proof split because it is backed by official AOSP / Android interface material and U-Boot documentation. The exact slot metadata layout and rollback storage can be vendor-specific, so a real case must bind generic surfaces to the device bootloader, fastboot implementation, AVB integration, and userspace updater involved.
