# Protocol USB HID Report Descriptor to Semantic Consumer Workflow Note

Topic class: workflow note
Ontology layers: protocol/firmware, USB HID, descriptor-to-report lineage, first semantic consumer proof
Maturity: practical
Related pages:
- topics/protocol-state-and-message-recovery.md
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-firmware-practical-subtree-guide.md
- topics/usb-urb-completion-and-first-consumer-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
Related source notes:
- sources/protocol/2026-06-02-usb-hid-report-descriptor-consumer-notes.md

## 1. What this note is for
Use this note when a target already looks **USB HID-shaped** and the analyst can see report descriptors, hidraw bytes, evdev events, or report parser output, but still cannot prove which semantic consumer owns the behavior.

Typical situations:
- `/sys/bus/hid/devices/.../report_descriptor`, `HIDIOCGRDESC`, hidraw dumps, or `hid-tools` output are visible, but the app/device behavior is still not explained
- a descriptor parser decodes usages, report IDs, report sizes/counts, arrays, variables, or padding, but the live report instance and target-local consumer are still unproved
- hidraw bytes and evdev/input events disagree, and the analyst needs to distinguish descriptor bug, kernel fixup/quirk, field interpretation issue, or app-side custom overlay
- an Output or Feature report seems to configure the device, but the write/control transfer, report ID, device acceptance, and later state/effect are being collapsed together

This note is for the narrower question:

```text
Which descriptor-declared report field, live report instance, and first semantic consumer actually own the behavior?
```

Not the broader question:

```text
Does USB traffic or an HID device exist?
```

For low-level submit/completion/cancel uncertainty, use `usb-urb-completion-and-first-consumer-workflow-note.md` first. Return here once the missing proof object is HID report meaning rather than URB fate.

## 2. When to use it
Use this note when most of the following are true:
- the device/interface is already plausibly HID-shaped
- one descriptor, report ID, hidraw stream, evdev stream, or report parser output is visible
- the current uncertainty is whether **descriptor truth**, **report-ID/type truth**, **field-layout truth**, **live report-instance truth**, **kernel-fixup / parsed-event truth**, or **application/device semantic-consumer truth** owns the claim
- the next useful artifact is one smaller report-lineage evidence row, not a full USB stack model

Do **not** start here when:
- the real bottleneck is still USB enumeration, endpoint discovery, transfer completion, cancel/retire semantics, or callback delivery; use the USB URB note
- the device is only HID-like as a transport for a private binary protocol and the descriptor adds no useful field meaning; route to layer-peeling / private-overlay notes after freezing the transport boundary
- parsed field meaning and first consumer are already proved, and the missing object is later state-machine or replay-gate logic

## 3. Core claim
A recurring HID reverse-engineering mistake is to stop too early at one of these milestones:
- “the HID descriptor was parsed”
- “hidraw bytes are visible”
- “evdev generated an event”
- “Report ID N has a field with Usage X”
- “a Feature report was sent, so configuration changed”

The smaller reusable ladder is:

```text
descriptor bytes visible
  != report ID / report type selected
  != field layout decoded correctly
  != live report instance delivered through the chosen surface
  != field values parsed with correct descriptor quirks / units / array-vs-variable semantics
  != evdev / hidraw / app callback consumer proved
  != behavior or state effect owned
```

For non-conformant devices, keep a second split visible:

```text
declared descriptor contract
  != observed wire/report behavior
  != kernel quirk/fixup output
  != application-owned meaning
```

## 4. Boundary objects to keep separate

### A. Descriptor bytes and parser output
Useful objects:
- `/sys/bus/hid/devices/.../report_descriptor`
- `HIDIOCGRDESCSIZE` / `HIDIOCGRDESC`
- `hid-decode`, `hid-recorder`, `hidrdd`, Wireshark descriptor parsing, or language-level parsers
- report collections, report IDs, input/output/feature report declarations
- report size/count, usage page/usage, logical/physical min/max, unit/exponent, array/variable/constant flags

This is descriptor-interpretation truth. It is weaker than proof that one live report instance used that layout under the trigger of interest.

Cheap rule:
- parser output is a map, not the journey; freeze one live report instance before narrating behavior ownership.

### B. Report ID, direction, and report type truth
Separate:
- Input reports from device to host
- Output reports from host to device
- Feature reports used for configuration/state
- numbered reports where the first byte is the report ID
- unnumbered reports where data begins at the first byte, while some APIs still expect a leading zero for writes/feature calls

This is often where off-by-one report parsing begins.

Cheap rule:
- if the first byte might be a report ID, do not interpret offsets until numbered-vs-unnumbered truth is frozen for that surface.

### C. Live report-instance truth
Useful surfaces:
- hidraw `read()` / `write()`
- `HIDIOCGINPUT`, `HIDIOCSOUTPUT`, `HIDIOCGFEATURE`, `HIDIOCSFEATURE`
- evdev/input events after kernel HID parsing
- USB bus capture if hidraw or evdev is unavailable
- target-local app callbacks or driver handlers

A live report proves a value existed at one surface. It does not automatically prove the same value was accepted, decoded, routed, or consumed by the target behavior.

Cheap rule:
- pair one raw report with one trigger and one decoded field tuple before widening to every report family.

### D. Kernel parser / quirk / fixup truth
HID cases often lie because one of these layers changes meaning:
- the device descriptor is wrong or incomplete
- the kernel applies a quirk or descriptor fixup
- evdev exposes a normalized event that hides raw report layout
- hidraw exposes raw reports that the application interprets manually
- the application carries a private overlay on top of HID Feature / Output reports

Do not treat evdev and hidraw disagreement as noise. The mismatch is often the discriminant.

Cheap rule:
- when evdev and hidraw disagree, classify the split before deciding whether to hook kernel parsing, hidraw reads/writes, or app-specific report consumers.

### E. First semantic consumer truth
This is the first target-local place where the report field becomes behavior:
- app callback maps usage/value to state
- driver parser updates a device state object
- output/feature response changes a mode/configuration bit
- firmware command handler consumes a report field as private protocol data
- UI/control-loop/game/input logic reacts to a decoded value

This may be one hop after hidraw `read()`, evdev delivery, or Feature-report return.

Cheap rule:
- stop at the first consumer only if it decides behavior; otherwise hand off to parser-to-state or replay-precondition notes.

## 5. Default workflow

### Step 1: freeze one report family and one trigger
Pick one target chain:
- one Input report that explains a visible event/state transition
- one Output report that changes LED, mode, force-feedback, or device state
- one Feature report that configures or queries a hidden mode
- one vendor-defined report that carries a private protocol payload

Record:

```text
transport | device path | VID/PID | report type | report ID | trigger | raw bytes | expected effect
```

### Step 2: parse the descriptor, but keep parser output provisional
Decode:
- collections and report IDs
- field bit ranges and byte offsets
- usage pages/usages or vendor-defined regions
- array vs variable fields
- constant padding
- logical/physical ranges and units

Then validate with one live report sample.

### Step 3: align raw bytes to field tuples
For the selected report instance, produce a row like:

```text
surface | report_id | raw bytes | field bits | usage/page | decoded value | parser/tool | timestamp/trigger
```

If the report is numbered, preserve whether the report-ID byte is included in that surface.

### Step 4: compare hidraw, evdev, and app-local truth
Use the smallest comparison that answers the case:
- hidraw bytes vs evdev event
- descriptor parser output vs kernel-normalized event
- app read buffer vs parser callback field tuple
- output/feature write buffer vs later device response

Classify mismatches as:
- descriptor contract bug
- report-ID / offset error
- array-vs-variable confusion
- logical/physical/unit interpretation drift
- kernel quirk/fixup
- app-specific overlay or private vendor protocol

### Step 5: freeze the first semantic consumer
Hook or inspect the first consumer likely to own behavior:
- hidraw read/write wrapper
- evdev event callback
- HID parser field dispatch
- app-level report decoder
- Feature/Output report request builder and response checker
- first state reducer or control loop after decoded value

Stop when one decoded field or report payload demonstrably changes the behavior you care about.

## 6. Common failure modes

### Parsed descriptor overclaim
Symptom:
- a report descriptor decodes cleanly, but live behavior does not match the claimed field meaning.

Fix:
- validate one report ID / field tuple against a live trigger and captured bytes.

### Report-ID offset drift
Symptom:
- every decoded field is shifted by one byte or the wrong report family appears selected.

Fix:
- prove whether the API surface includes the report ID byte and whether the device actually uses numbered reports.

### hidraw / evdev mismatch
Symptom:
- raw reports suggest one value, but normalized input events show another.

Fix:
- check kernel quirks/fixups, descriptor correction, logical/physical scaling, and whether the app bypasses evdev entirely.

### Feature/Output report acceptance overclaim
Symptom:
- a host sent bytes and the analyst assumes the device changed state.

Fix:
- require device ACK/response, changed subsequent Input report, mode bit, or first device/app state consumer.

### Vendor-defined payload flattening
Symptom:
- vendor-page fields are treated as ordinary HID semantics even though the real payload is a private protocol.

Fix:
- freeze HID report framing, then route the payload to layer-peeling, parser-to-state, or replay-precondition notes.

## 7. Useful outputs
- descriptor-to-report evidence row
- report-ID / offset map
- hidraw-vs-evdev mismatch classification
- Feature/Output report acceptance test
- hook plan for first semantic consumer

A compact row shape:

```text
device | VID:PID | surface | report_type | report_id | raw bytes | field bit range | usage/page | decoded value | parser/fixup note | first consumer | effect
```

## 8. Handoff rules
- If the missing proof object is transfer completion/cancel/giveback, route to `usb-urb-completion-and-first-consumer-workflow-note.md`.
- If the report payload is a vendor/private protocol after the HID framing is frozen, route to `protocol-layer-peeling-and-contract-recovery-workflow-note.md`.
- If one decoded field reaches a parser but the state consequence remains unclear, route to `protocol-parser-to-state-edge-localization-workflow-note.md`.
- If a Feature/Output report looks structurally correct but is rejected or inert, route to replay-precondition / acceptance-gate work.

## 9. Sources / provenance
- `sources/protocol/2026-06-02-usb-hid-report-descriptor-consumer-notes.md`
- Linux HID report descriptor introduction: https://docs.kernel.org/hid/hidintro.html
- Linux hidraw documentation: https://docs.kernel.org/hid/hidraw.html
- Rust `hidparser` documentation: https://docs.rs/hidparser/latest/hidparser/
- Search artifact: `sources/protocol/2026-06-02-0450-usb-hid-report-consumer-search-layer.json`
