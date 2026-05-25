# Devicetree overlay / deferred-probe consumer notes — 2026-05-26

## Search context
Search command:

```bash
python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py \
  --queries \
    "Linux DeviceTree overlays live tree fdt overlay bootloader kernel reverse engineering" \
    "Linux driver probe deferred probe devicetree resource consumption ftrace dynamic debug" \
    "of_platform_populate devicetree platform device probe sysfs of_node driver binding" \
  --mode deep \
  --intent exploratory \
  --num 5 \
  --source exa,tavily,grok
```

Saved raw result set:
- `sources/protocol/2026-05-26-0450-devicetree-overlay-deferred-probe-search-layer.json`

Search outcome:
- Exa returned Linux kernel documentation, kernel source entry points, and supporting deferred-probe material.
- Tavily returned U-Boot overlay documentation, Linux overlay material, and embedded-vendor/practitioner overlay examples.
- Grok was invoked but returned HTTP 502 Bad Gateway on all three query attempts.

## Source-backed observations

### Overlays mutate the live tree, but mutation is not automatically consumer proof
The Linux kernel Devicetree overlay notes describe overlays as a mechanism for modifying the kernel's live tree so the modification affects kernel state. They also state that newly active device nodes should result in device creation, while disabled or removed nodes should lead to affected devices being deregistered.

Reverse implication:
- an overlay blob, `fdt apply` log, or post-apply node is stronger than a static base DTS, but it is still not the same as successful probe or behavior ownership
- overlay application should be placed on the proof ladder between selected FDT/live-tree truth and device population / driver binding
- overlay removal introduces a separate lifetime hazard: cached node/property pointers after overlay removal are explicitly called out as buggy, so stale pointer evidence is not stable consumer proof

### U-Boot overlay application is part of the boot tuple, not a driver claim
U-Boot documentation describes applying overlays by loading base DTB and overlay DTBO, selecting the working FDT, resizing it, applying the overlay, and then booting with the modified FDT. It also describes FIT-contained overlays and manual overlay application, and warns that apply errors can invalidate base and overlay blobs.

Reverse implication:
- bootloader overlay commands, FIT overlay lists, or DTBO paths belong in the selected boot tuple / FDT lineage evidence row
- they do not prove the kernel accepted the same tree, populated a device, bound a driver, or consumed a property
- the cheaper discriminant is often to compare bootloader-side intended FDT+overlay material with `/proc/device-tree` / `/sys/firmware/devicetree/base` and boot logs before deep driver work

### Platform-device creation and driver binding are narrower than node visibility
Linux platform-device documentation frames platform devices as device-model objects with resources such as addresses and IRQs; platform drivers provide `probe()` / `remove()` and should verify that the hardware exists and is working. Driver binding documentation frames binding as device registration or driver registration triggering match, setting the device's driver field, calling `probe()`, and then installing per-device state and sysfs links on success.

Reverse implication:
- an OF node or overlay-created node is a candidate enumeration source
- a platform device with resources is a narrower object, but still only setup truth
- driver match/bind, probe entry, successful probe return, per-device state, and class/sysfs exposure should remain separate proof rows

### Deferred probe is a first-class false-negative / false-positive trap
Deferred-probe troubleshooting material shows a common embedded failure mode: the target device's node and driver may both look plausible, but a phandle supplier such as a backlight, regulator, GPIO, clock, or reset provider is not ready. The consumer probe returns `-EPROBE_DEFER`, the device enters the deferred list, and later supplier registration may or may not make it retry successfully. Modern systems can expose `/sys/kernel/debug/devices_deferred`, including deferral reasons such as supplier-not-ready.

Reverse implication:
- `probe()` entry is not enough when a dependency can defer the device indefinitely
- provider phandles should be treated as live dependency edges, not static property decoration
- `/sys/kernel/debug/devices_deferred`, deferred-probe logs, dynamic debug around supplier lookup, and final successful retry can be decisive evidence before MMIO/IRQ behavior is attributed to the device

## Practical synthesis
The useful extension to the existing DTB proof ladder is:

```text
base DTB visible != overlay selected/applied != live tree mutated != device populated != match/bind selected != probe succeeded after suppliers ready != resource/property consumed != behavior/effect owned
```

For a reverse case, this means overlay and deferred-probe evidence should be recorded as placement/lifetime evidence, not flattened into driver behavior. The operator should prove:
1. which base FDT and overlays were selected by the boot path
2. whether the kernel live tree reflects those overlays under the current boot
3. whether the relevant node became a device on the expected bus
4. whether the matched driver reached a final successful probe rather than a deferred/failed probe state
5. which resource/property was consumed by the first behavior-bearing code path

## Sources consulted
- Linux kernel documentation, Devicetree Overlay Notes — https://docs.kernel.org/devicetree/overlay-notes.html
- U-Boot documentation, Device Tree Overlays — https://docs.u-boot.org/en/v2021.04/usage/fdt_overlays.html
- Linux kernel documentation, Platform Devices and Drivers — https://docs.kernel.org/driver-api/driver-model/platform.html
- Linux kernel documentation, Driver Binding — https://docs.kernel.org/driver-api/driver-model/binding.html
- Javier Martinez Canillas, `How to troubleshoot deferred probe issues in Linux` — https://blog.dowhile0.org/2022/06/21/how-to-troubleshoot-deferred-probe-issues-in-linux/
