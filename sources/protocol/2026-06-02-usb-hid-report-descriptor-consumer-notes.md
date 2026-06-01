# USB HID report descriptor to semantic consumer notes — 2026-06-02

## Scope
Source-backed notes for a protocol/firmware workflow continuation around USB HID report descriptors, hidraw report bytes, parser output, and first semantic consumer proof.

The practical problem is not merely “can we parse a HID descriptor?” It is whether the analyst can prove the chain from descriptor-declared report layout to the exact report instance, parsed field meaning, event / hidraw delivery surface, and first target-local consumer that owns the behavior under investigation.

## Source facts preserved

### Linux HID introduction / report descriptor documentation
- Linux HID documentation describes HID report descriptors as fixed bytes that advertise what reports may be sent between device and host and the meaning of each individual bit. Example wording: a report with ID 3 may define bits 8–15 as mouse delta X.
- HID reports themselves carry only data values; the descriptor supplies the interpretation. Reports can be Input, Output, or Feature reports.
- Linux HID can expose report descriptors under `/sys/bus/hid/devices/.../report_descriptor` and also through hidraw.
- Report IDs matter: when a report ID is needed, it is transmitted as the first byte of any report. A device with one report may omit it.
- The Linux docs explicitly warn that default HID parsing may not handle wrong descriptors or devices requiring special handling, and point to quirks, descriptor fixes, modifying transmitted data on the fly, or specialized drivers.
- The docs recommend using parsers such as `hid-tools` rather than hand parsing, and show `hid-recorder` matching raw report bytes to decoded button / axis meanings.

Primary source: https://docs.kernel.org/hid/hidintro.html

### Linux hidraw documentation
- `hidraw` gives raw access to USB and Bluetooth HID reports; unlike parsed HID interfaces, reports are sent/received unmodified.
- `read()` on hidraw returns queued reports from the device; for USB devices these are reports from the Interrupt IN endpoint.
- On numbered-report devices, the first byte returned by `read()` is the report number; for unnumbered reports, data begins at the first byte.
- `write()` should include the report number in the first byte, or `0` for devices without numbered reports; report data begins in the second byte.
- hidraw supports ioctls to get descriptor size / descriptor bytes, raw VID/PID/bus info, raw name/physical path, and Feature / Input / Output report get/set operations.
- hidraw is specifically useful for custom or non-conformant devices where descriptor-based parsed interfaces can lie or reject needed communication.

Primary source: https://docs.kernel.org/hid/hidraw.html

### Parser/library evidence
- The Rust `hidparser` crate describes a parser that converts a raw report descriptor into a `ReportDescriptor` object containing input/output/feature reports.
- Its example exposes report fields as variable, array, or padding fields with bit ranges, usages, usage ranges, and report IDs. This is a useful reminder that parser output is descriptor-interpretation truth, not live report-instance or app-state truth.

Primary source: https://docs.rs/hidparser/latest/hidparser/

### Search-result practitioner/tooling signal
- Search results surfaced practical tooling and case surfaces: Linux `hidraw-dump`, `hid-tools`, Python/Rust HID parsers, Wireshark HID report descriptor parser work, and a USB-device reverse-engineering walkthrough that treats the descriptor as the “template” for interpreting reports.
- This supports a workflow note focused on descriptor-to-report-to-consumer lineage rather than another generic USB transfer-completion note.

## Practical synthesis

The false inference to avoid is:

```text
HID descriptor parsed or hidraw bytes visible == semantic device/app behavior proved
```

A sharper proof ladder is:

```text
descriptor bytes visible
  != report ID / report type selected
  != field layout decoded correctly
  != live report instance delivered through the chosen surface
  != field values parsed with correct descriptor quirks / units / array-vs-variable semantics
  != evdev / hidraw / app callback consumer proved
  != behavior or state effect owned
```

A second useful split for non-conformant devices:

```text
declared descriptor contract != observed wire/report behavior != kernel quirk/fixup output != application-owned meaning
```

## Operator tactics
- Freeze one report family first: input vs output vs feature, report ID, transport surface, and trigger.
- Capture descriptor bytes and parse them with a tool, but validate at least one live report instance against observed trigger deltas.
- If using hidraw, remember report-ID byte placement differs between numbered and unnumbered devices.
- If default evdev events disagree with hidraw bytes, classify the mismatch before choosing hooks: descriptor bug, kernel fixup/quirk, unit/logical range interpretation, array-vs-variable field, or app-side custom protocol overlay.
- Preserve both the raw report byte slice and the decoded field tuple in evidence rows: `surface | report_id | direction/type | raw bytes | field bits | usage/page | logical/physical range | parser/tool | callback/event consumer | first state/effect`.

## KB integration target
- New workflow note: `topics/protocol-usb-hid-report-descriptor-to-semantic-consumer-workflow-note.md`
- Parent/routing updates: `topics/protocol-firmware-practical-subtree-guide.md`, `topics/protocol-state-and-message-recovery.md`, `topics/firmware-and-protocol-context-recovery.md`, `index.md`
