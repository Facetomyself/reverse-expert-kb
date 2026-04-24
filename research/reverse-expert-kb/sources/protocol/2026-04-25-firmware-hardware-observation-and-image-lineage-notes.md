# Firmware hardware observation and image-lineage notes — 2026-04-25

Source class: external research synthesis
Search artifact: `sources/protocol/2026-04-25-0450-firmware-hardware-observation-search-layer.txt`
Run: `runs/2026-04-25-0450-run-report.md`

## Why this source note exists
The protocol / firmware branch is strong on message, parser, descriptor, mailbox, interrupt, and completion-consumer proof. It is thinner at the earlier hardware-acquisition boundary where an analyst has a board, a UART/JTAG/SWD/SPI surface, or a flash dump and must decide whether the artifact in hand is actually the image and execution context worth reversing.

The practical failure mode is overclaiming:

```text
pads found / flash dumped / UART visible / JTAG attached
  == firmware recovered / executing image understood / useful dynamic proof obtained
```

That equality is usually false. Hardware observation surfaces produce different proof objects.

## Source-backed observations

### SPI flash dump is not automatically the execution truth
Wrongbaud's router teardown shows a common ladder: identify the SPI flash, attempt in-circuit `flashrom`, fail because the target circuit/SoC still affects lines, remove the chip, successfully dump it, then use `binwalk` to identify U-Boot images, kernel, and SquashFS. The useful operator lesson is not merely "dump flash"; it is that **in-circuit failure, off-board success, partition carving, and bootloader/rootfs identification are separate proof objects**.

William Durand's SPI flash reconstruction writeup reinforces the same split from the opposite side: the dump produced recognizable kernel/filesystem material, but meaningful reconstruction depended on correlating `binwalk` offsets with UART/kernel-log MTD partition lines, `dd`-carved partition ranges, device tree material, and loader/header observations. A raw magic-number hit was not enough to decide where the booted kernel actually began.

### UART is a context and trigger surface, not always a shell
Wrongbaud's UART section treats serial discovery as a way to obtain debug output and sometimes terminal access; pin identification, logic-level/baud confirmation, and TX/RX role are separate from getting an authenticated console. West Side Electronics' search snippet similarly shows boot logs and a password-gated U-Boot console, where the operator used the logs and later patch/reflash work to reach console access.

Practical implication: UART output can give partition maps, bootargs, loader strings, reset reasons, password prompts, and trigger timing even when it does not give shell authority.

### JTAG/SWD attach proves control/visibility only after memory-map and halt-state checks
HardBreak's JTAG/SWD extraction page shows the generic OpenOCD/J-Link path: identify pins, connect debugger, verify target voltage / TAP or SWD target discovery, halt/reset, then dump a specific memory range. The durable KB point is that **TAP found != flash readable != current boot image dumped**. A dump range must be justified by the memory map, the halted state, and any readout-protection or remap behavior.

### External flash bus tracing can replace unavailable debug with code-fetch evidence
Dominik Zürner's SPI instruction-tracing article is a concrete higher-signal case. With a UART password prompt but no useful debug access, the analyst dumped the SPI flash, handled 8051 code banking, then sniffed QSPI/XIP flash reads during idle and password-entry runs. Diffing observed flash-read/code-fetch addresses narrowed the password-check logic. This is a useful branch addition because it treats a bus trace as **executed-fetch / coverage evidence**, not merely as another static dump.

## Durable workflow split to preserve

```text
physical interface found
  != electrical/protocol session stable
  != artifact bytes acquired
  != bytes mapped to boot partitions / memory ranges
  != current boot actually used those bytes
  != code path executed under the trigger of interest
  != first behavior-bearing consumer identified
```

## Operator implications
- Prefer correlating at least two surfaces when possible: UART boot log + flash partition offsets, JTAG halt PC + memory map, QSPI trace + static bank/overlay model, or bootloader env + observed storage layout.
- Treat vendor OTA images, off-board flash dumps, and live memory dumps as different lineage objects. They may overlap but often omit bootloaders, calibration/NVRAM, mutable config, or a repaired/remapped runtime view.
- When static reversing stalls on banked/XIP firmware, a logic-analyzer trace can answer a narrower question: "which code regions were fetched during this trigger?" That is weaker than full instruction trace, but stronger than a blind string/xref search.
- Do not let debug-port availability drive the proof object. A password-gated UART may still be the best source of partition truth; a JTAG attach may be misleading if the dump range is wrong; a clean flash dump may be stale if boot ROM remaps or chooses another image slot.

## Sources consulted
- Wrongbaud, "Router Analysis Part 1: UART Discovery and SPI Flash Extraction" — https://wrongbaud.github.io/posts/router-teardown/
- William Durand, "SPI flash content analysis and firmware reconstruction" — https://williamdurand.fr/2022/03/10/spi-flash-content-analysis-and-firmware-reconstruction/
- Dominik Zürner, "Extracting a UART Password via SPI Flash Instruction Tracing" — https://zuernerd.github.io/blog/2026/01/07/switch-password.html
- HardBreak Wiki, "Extract Firmware using JTAG/SWD" — https://www.hardbreak.wiki/hardware-hacking/interface-interaction/jtag-swd/extract-firmware-using-jtag-swd
