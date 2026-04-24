# Firmware hardware observation to executed-image workflow note

Topic class: workflow note
Ontology layers: firmware acquisition, hardware observation surface, image-lineage proof, executed-code proof
Maturity: structured-practical
Related pages:
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-firmware-practical-subtree-guide.md
- topics/runtime-behavior-recovery.md
- topics/analytic-provenance-and-evidence-management.md
- sources/protocol/2026-04-25-firmware-hardware-observation-and-image-lineage-notes.md

## Why this matters
Firmware reversing often starts before a clean binary exists. The analyst may have a board, exposed pads, a UART prompt, a JTAG/SWD attach, a SPI flash chip, a vendor update image, or a logic-analyzer trace.

The common mistake is to collapse early hardware visibility into execution truth:

```text
interface found / flash dumped / console output visible
  == firmware recovered / current code path understood
```

For practical reversing, those are different proof objects. This note preserves the ladder from **hardware observation surface** to **artifact bytes**, **image lineage**, **current boot selection**, and finally **executed behavior under the trigger of interest**.

## Scope
Use this note when:
- the target is an embedded / IoT / appliance / router / MCU-class device
- the current uncertainty is whether UART, JTAG/SWD, SPI flash, vendor images, boot logs, or bus traces actually describe the code currently executing
- the desired artifact is a trustworthy image map, boot partition lineage, executed-code slice, or narrow dynamic anchor for later static analysis

Do not use it as:
- a generic hardware-hacking tutorial
- a soldering / pinout / electronics safety guide
- a full protocol-parser or replay workflow once the firmware image and executed path are already trustworthy

## Preconditions
Useful inputs include any two of:
- board photos / chip markings / flash package markings
- UART boot logs, bootloader prompt, kernel logs, or console prompts
- SPI/I2C/QSPI flash dumps or vendor OTA images
- JTAG/SWD/OpenOCD/J-Link attach logs
- `binwalk`, `file`, `strings`, device-tree, bootargs, MTD partition logs, or bootloader environment output
- logic-analyzer captures of external flash or bus transactions under a known trigger

## Investigation frame
- **Target:** embedded device, router, appliance, MCU, or SoC firmware target
- **Boundary:** physical observation interface -> acquired bytes -> partition/image map -> selected boot image -> executed code path
- **Observation surface:** UART, JTAG/SWD, SPI flash dump, vendor update package, bootloader/kernel logs, QSPI/XIP trace, live RAM dump
- **Artifact goal:** one trustworthy image-lineage map plus one trigger-linked executed-code or first-consumer anchor
- **Cheapest next discriminant:** correlate the current artifact with an independent boot-time or runtime surface before widening static analysis

## Practical workflow
### 1. Classify the surface before trusting it
Name the proof object precisely:

| Surface | What it can prove | What it does not automatically prove |
| --- | --- | --- |
| UART TX boot log | bootargs, partition names, kernel messages, prompts, reset timing | shell authority, password bypass, full image contents |
| UART shell / bootloader prompt | interactive control in one boot stage | that all later runtime behavior uses the modified path |
| SPI flash dump | raw nonvolatile bytes from one storage device | selected boot slot, live remapped view, decrypted/unpacked runtime image |
| vendor OTA image | update payload / rootfs candidate | bootloader, calibration/NVRAM, device-local mutable state, exact installed slot |
| JTAG/SWD attach | debug/session visibility, halted PC/registers, memory read capability | correct dump range, current boot image, absence of readout/remap lies |
| QSPI/XIP trace | code-fetch or data-read addresses during one time window | semantic execution, branch reason, complete control-flow graph |

If the surface name is vague, the next claim will drift.

### 2. Stabilize the electrical / session layer without overclaiming
For hardware surfaces, first prove the session is real:
- UART: voltage level, GND, TX/RX role, baud rate, boot-time output, whether RX input changes behavior
- SPI/QSPI flash: chip ID, voltage, in-circuit vs off-board stability, repeated dump hashes, read-size consistency
- JTAG/SWD: target voltage, TAP/SWD discovery, reset/halt behavior, PC/register sanity, memory read repeatability

Stop rule:

```text
pins found != protocol session stable != bytes or control acquired
```

### 3. Build image lineage before reversing deeply
Separate the candidate images:
- off-board raw flash dump
- in-circuit dump
- vendor update image
- bootloader-visible flash map
- kernel-visible MTD map
- live RAM / decompressed / repaired runtime view

Correlate offsets with independent evidence:
- `binwalk` / magic numbers vs UART kernel MTD lines
- bootloader env / bootargs vs carved partitions
- file-system timestamps / image names vs installed version strings
- JTAG halted PC or vector table vs claimed base address
- device tree / boot log hardware names vs board markings

Stop rule:

```text
bytes acquired != partition mapped != selected boot slot != runtime image view
```

### 4. Use boot logs as context evidence even when access is gated
A password-gated UART is still valuable. Preserve:
- partition names and offsets
- bootargs and console device
- SoC / board / DDR / flash identifiers
- bootloader version strings
- reset loops, watchdog hints, password prompts, update-mode messages

These often make a static dump tractable without proving shell access.

### 5. If debug is blocked, consider bus-derived execution evidence
For XIP or external-flash-backed firmware, a logic analyzer trace can answer a narrower question:
- which flash addresses were fetched while idle?
- which addresses appear only during the trigger, login attempt, packet receipt, button press, or fault?
- do fetched addresses map into a known bank / overlay / partition slice?

Use compare pairs:

```text
idle flash-read coverage
  vs trigger flash-read coverage
  -> new address clusters
  -> bank / overlay mapping
  -> candidate function family for static recovery
```

Do not call this a full execution trace unless the capture and decoder justify it. Treat it as **fetch/coverage evidence** that guides the next static slice.

### 6. Freeze the first behavior-bearing consumer
Once image lineage is trustworthy, avoid stopping at broad success markers. Ask what the first durable consumer is:
- bootloader variable changed and later kernel bootargs consumed it
- patched credential check reached the prompt or shell path
- packet parser read from the mapped filesystem asset
- init script / service launched from the extracted rootfs
- MCU handler fetched the trigger-only code cluster and touched a state variable or output register

Final stop rule:

```text
physical interface found
  != electrical/protocol session stable
  != artifact bytes acquired
  != bytes mapped to boot partitions / memory ranges
  != current boot actually used those bytes
  != code path executed under the trigger of interest
  != first behavior-bearing consumer identified
```

## Common failure modes
- **In-circuit SPI lie:** the SoC or board circuit prevents stable reads; off-board dump differs or repeated hashes drift.
- **OTA image lineage lie:** the downloadable update lacks bootloader, calibration, writable config, or the currently selected inactive/active slot.
- **Magic-number overread:** `binwalk` finds a kernel/filesystem, but boot logs show padding, custom headers, shifted offsets, or multiple images.
- **Debug attach overread:** OpenOCD/J-Link reports a device, but the memory range dumped is not the current executable image.
- **UART authority overread:** boot output or a password prompt is treated like shell access instead of context evidence.
- **Bus-trace overread:** flash-read coverage is treated as exact branch semantics without mapping bank/overlay and trigger timing.

## Useful outputs
- hardware observation surface table with proof object per surface
- image-lineage map: raw flash / OTA / bootloader map / kernel MTD / live view
- offset-correlation table: source of each partition or code slice claim
- trigger-vs-idle bus-coverage diff
- narrowed static-analysis queue: functions/banks/partitions worth loading first
- first-consumer proof statement for the current trigger

## Sources / provenance
- `sources/protocol/2026-04-25-firmware-hardware-observation-and-image-lineage-notes.md`
- Wrongbaud, Router Analysis Part 1: UART Discovery and SPI Flash Extraction
- William Durand, SPI flash content analysis and firmware reconstruction
- Dominik Zürner, Extracting a UART Password via SPI Flash Instruction Tracing
- HardBreak Wiki, Extract Firmware using JTAG/SWD
