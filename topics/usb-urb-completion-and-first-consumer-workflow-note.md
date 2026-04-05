# USB URB Completion and First Consumer Workflow Note

Topic class: workflow note
Ontology layers: firmware/protocol, USB I/O, async completion, first consumer proof
Maturity: emerging
Related pages:
- topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md
- topics/firmware-and-protocol-context-recovery.md
Related source notes:
- sources/protocol-and-network-recovery/2026-04-06-usb-urb-completion-and-first-consumer-notes.md

## 1. What this note is for
Use this note when a target already plausibly depends on **USB URB / async transfer completion**, but the investigation still lacks the first trustworthy consumer boundary that turns visible submit/completion traffic into actual behavior ownership.

Typical situations:
- `usb_submit_urb(...)`, libusb async submit, or endpoint activity is visible, but the real missing step is which first completion consumer actually owns the result
- usbmon or trace output shows URB completion/status, but completion visibility and later consumer truth are still being flattened together
- endpoint direction, status, and `actual_length` are visible, but the analysis still collapses transfer existence, completion callback, parsing/dispatch, and later behavior into one story

This note is for the narrower question:

```text
Which first URB/transfer completion consumer actually owns the behavior that matters?
```

Not the broader question:

```text
Does this target use USB or async transfers at all?
```

## 2. When to use it
Use this note when most of the following are true:
- the broad firmware/protocol problem has already narrowed specifically into USB URB / async transfer completion
- one endpoint/transfer family is already visible
- the main uncertainty is whether **submission truth**, **completion truth**, **first completion consumer truth**, or **later visible consequence truth** actually owns the claim you care about
- the next useful output is one smaller trustworthy chain such as:
  - submit -> complete callback -> first parser/dispatcher consumer -> visible consequence
  - usbmon completion record -> driver callback -> request/response matcher -> visible behavior
  - libusb transfer completion -> first app-side callback consumer -> later state/update consequence

Do **not** start here when:
- the real bottleneck is still descriptor/ring ownership rather than completed USB transfer handling
- the real question is still generic device enumeration, configuration, or endpoint discovery
- completion callback ownership is already proved and the real missing step is later parser/business logic outside the USB seam

## 3. Core claim
A recurring USB-reversing mistake is to stop too early at one of these milestones:
- “the app submits a transfer”
- “usbmon shows the URB completed”
- “there is a completion callback”
- “endpoint traffic is visible, so this code path must own the behavior”

The smaller reusable target is:

```text
transfer exists
  != relevant completion truth
  != first completion consumer proved
  != later visible consequence truth
```

## 4. Boundary objects to keep separate
### A. Submission truth
Visible objects:
- `usb_submit_urb(...)`
- libusb `libusb_submit_transfer(...)`
- endpoint, direction, transfer type, buffer setup

This is weaker than proof that the completion you care about is the one that later matters.

### B. Completion truth
Useful objects:
- URB status
- `actual_length`
- endpoint/direction
- one completion record or callback timing boundary

This is weaker than proof that the later parser/dispatcher/handler actually consumed it meaningfully.

### C. First completion consumer truth
This is the first method/path that turns the completion into meaningful behavior.
Typical shapes:
- URB completion callback
- libusb transfer callback
- first driver/app parser that reads the completed bytes
- first matcher/router that assigns the transfer to a request/state machine entry

### D. Later visible consequence truth
This is where the analyst proves the completed transfer actually matters:
- one later state change, response parse, device command result, or app-visible behavior depends on the completion consumer you froze
- one later handler/result only exists because the earlier completion-owned path ran

## 5. Practical stop rules this note preserves
- `transfer submitted != relevant completion proved`
- `completion record visible != first completion consumer proved`
- `endpoint traffic visible != this callback/parser owned the behavior`
- `callback exists != later visible consequence truth`
- `status/actual_length visible != parser/dispatcher ownership proved`

## 6. Default workflow
### Step 1: freeze one transfer family, one completion family, and one visible consequence
Do not widen into every endpoint or URB.
Pick one high-leverage chain:
- one interrupt/bulk transfer with visible later effect
- one request/response pair
- one usbmon completion record that should explain later behavior

### Step 2: separate submit from completion truth
Before explaining behavior, freeze:
- which transfer was submitted
- which completion belongs to it
- status / length / endpoint facts that matter

### Step 3: freeze one first completion consumer
Pick the smallest consumer that matters:
- one completion callback
- one first parser/dispatcher
- one response/request matcher

### Step 4: prove one later visible consequence
Stop once you can show:
- submit -> completion -> first consumer -> visible consequence

Do not keep widening into whole-driver narration if this smaller chain already answers the operator’s question.

## 7. Practical scenarios
### Scenario A: `usb_submit_urb(...)` is visible
Wrong stop:
- “the driver submits the URB, so this path owns the device behavior”

Better stop:
- freeze one completion and one first completion consumer that actually interprets it.

### Scenario B: usbmon shows completed traffic
Wrong stop:
- “the monitor shows completion, so later app behavior is explained”

Better stop:
- keep completion visibility separate from the first callback/parser/router that gives the bytes meaning.

### Scenario C: libusb async callback exists
Wrong stop:
- “the callback exists, so that’s already the owner”

Better stop:
- prove which first callback-side consumer/matcher/parser actually owns the later behavior you care about.

## 8. Why this note exists in the firmware/protocol branch
The firmware/protocol subtree already had practical notes for descriptor ownership, request lifetime realism, MMIO effect proof, and deferred worker consequences.
What it lacked was a thinner practical continuation for **USB URB / async transfer completion ownership**.

This note fills that gap and preserves the smaller ladder:
- submission
- completion
- first completion consumer
- later visible consequence

instead of collapsing everything into “USB traffic exists.”

## 9. Sources
See:
- `sources/protocol-and-network-recovery/2026-04-06-usb-urb-completion-and-first-consumer-notes.md`

Primary anchors retained:
- Linux USB API docs
- usbmon references
- libusb async-transfer docs
- explicit `search-layer` multi-source attempt with `--source exa,tavily,grok`
