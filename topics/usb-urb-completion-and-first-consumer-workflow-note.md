# USB URB Completion and First Consumer Workflow Note

Topic class: workflow note
Ontology layers: firmware/protocol, USB I/O, async completion, first consumer proof
Maturity: practical
Related pages:
- topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-firmware-practical-subtree-guide.md
Related source notes:
- sources/protocol-and-network-recovery/2026-04-06-usb-urb-completion-and-first-consumer-notes.md
- sources/protocol/2026-04-18-usb-urb-giveback-cancel-and-usbmon-realism-notes.md

## 1. What this note is for
Use this note when a target already plausibly depends on **USB URB / async transfer completion**, but the investigation still lacks the first trustworthy consumer boundary that turns visible submit/completion traffic into actual behavior ownership.

Typical situations:
- `usb_submit_urb(...)`, libusb async submit, or endpoint activity is visible, but the real missing step is which first completion consumer actually owns the result
- `usb_unlink_urb()` / `usb_kill_urb()` or `libusb_cancel_transfer()` is visible, but the analysis still flattens cancel request, callback fate, and safe-idle truth together
- usbmon or trace output shows URB completion/status, but monitor-visible completion metadata and later consumer truth are still being collapsed together
- endpoint direction, status, and `actual_length` are visible, but the analysis still treats transfer existence, completion visibility, callback/giveback truth, and later behavior as one story

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
- the main uncertainty is whether **submit truth**, **retire/cancel truth**, **monitor-visible completion truth**, **callback/giveback truth**, **first completion consumer truth**, or **later visible consequence truth** actually owns the claim you care about
- the next useful output is one smaller trustworthy chain such as:
  - submit -> completion callback -> first parser/dispatcher consumer -> visible consequence
  - submit -> cancel request -> callback with cancelled/unlinked status -> first still-relevant consumer or explicit no-consumer conclusion
  - usbmon callback record -> driver callback -> request/response matcher -> visible behavior
  - libusb transfer completion -> first app-side callback consumer -> later state/update consequence

Do **not** start here when:
- the real bottleneck is still descriptor/ring ownership rather than completed USB transfer handling
- the real question is still generic device enumeration, interface/endpoint discovery, or non-USB transport framing
- completion callback ownership is already proved and the real missing step is later parser/business logic outside the USB seam

## 3. Core claim
A recurring USB-reversing mistake is to stop too early at one of these milestones:
- “the app submits a transfer”
- “cancel was requested, so this transfer is gone”
- “usbmon shows the URB completed”
- “there is a completion callback”
- “endpoint traffic is visible, so this code path must own the behavior”

The smaller reusable ladder is:

```text
submitted / queued
  != retired or safely reusable
  != usbmon callback/completion visible
  != giveback / callback finished
  != first completion consumer proved
  != later visible consequence truth
```

A second stop rule worth preserving for cancel-heavy cases is:

```text
cancel requested
  != callback cannot still run
  != object is safe to free or reuse
  != parser/router will never still see bytes or status
```

## 4. Boundary objects to keep separate

### A. Submission / queueing truth
Visible objects:
- `usb_submit_urb(...)`
- libusb `libusb_submit_transfer(...)`
- endpoint, direction, transfer type, buffer setup

Kernel-grounded reminder:
- URB execution is inherently asynchronous; `usb_submit_urb()` returns after successful queueing, not after later behavior ownership is settled

This is weaker than proof that the completion you care about is the one that later matters.

### B. Retire / cancel truth
Useful objects:
- `usb_unlink_urb()`
- `usb_kill_urb()`
- `libusb_cancel_transfer()`
- caller-side “shutdown” or “stop polling” branches

Kernel- and libusb-backed reminder:
- `usb_unlink_urb()` is asynchronous and normally returns before the completion handler finishes
- `usb_kill_urb()` waits until the completion handler has finished and the URB is totally idle
- libusb async cancellation is also non-blocking; callback delivery later carries the cancelled result

This is weaker than proof that the callback path is gone, that the object is safe to reuse, or that the later parser/router will never still see the result.

### C. usbmon / monitor-visible completion truth
Useful objects:
- usbmon `C` callback/completion events
- status, endpoint, and `actual_length`/length fields
- binary-api `len_cap` / dropped-event reality when available

usbmon-backed reminder:
- usbmon reports driver-to-HCD requests, not a bus analyzer’s perfect truth object
- data may be absent even when length is nonzero
- monitor-visible completion metadata can therefore be real while payload capture is partial, absent, or dropped

This is weaker than full parser-input truth and weaker than first completion consumer proof.

### D. Giveback / callback truth
This is the first place where the transfer becomes callback-owned.
Typical shapes:
- kernel URB completion handler
- libusb transfer callback
- driver “done” callback or wrapper

Kernel/libusb reminders:
- callback delivery is where `urb->status`, libusb transfer status, and actual length become meaningfully inspectable
- callback context can still be restricted enough that “some code ran” is weaker than “the bytes were meaningfully consumed”
- some periodic transfers only continue because the callback resubmits them; do not overread repeated activity as one static owner without freezing that resubmit boundary

### E. First completion consumer truth
This is the first method/path that turns the completion into meaningful behavior.
Typical shapes:
- first parser that reads the completed bytes
- request/response matcher
- first router/dispatcher that assigns the transfer to state
- first branch that decides keep/retry/discard/decode

This is often one hop later than the callback itself.

### F. Later visible consequence truth
This is where the analyst proves the completed transfer actually matters:
- one later state change, response parse, device command result, or app-visible behavior depends on the completion consumer you froze
- one later handler/result only exists because the earlier completion-owned path ran

## 5. Default workflow

### Step 1: freeze one transfer family, one capture surface, and one visible consequence
Do not widen into every endpoint or URB.
Pick one high-leverage chain:
- one interrupt/bulk transfer with visible later effect
- one request/response pair
- one usbmon callback record that should explain later behavior
- one libusb async transfer whose callback should explain a later parser or UI/state update

### Step 2: separate submit/setup from retire truth
Before explaining behavior, freeze:
- which transfer was submitted
- whether cancel/unlink/kill was requested or completed
- whether the object is only “requested to stop” or truly callback-finished / idle

Cheap operator rule:
- if all you have is `usb_unlink_urb()` or `libusb_cancel_transfer()` return, you are still too early to narrate callback fate

### Step 3: separate usbmon visibility from callback fate
Before treating one completion as behavior truth, freeze:
- whether the monitor saw a callback/completion event or only a submission
- whether payload bytes were actually captured or only length/status metadata was captured
- whether dropped/truncated capture reality might still hide the parser-facing payload slice

Cheap operator rule:
- `usbmon callback line visible != callback/giveback finished with the bytes you think the parser saw`

### Step 4: freeze one callback/giveback boundary
Pick the smallest callback boundary that matters:
- one URB completion handler
- one libusb transfer callback
- one wrapper callback that decides resubmit/cancel/discard/decode

Stop there only if the callback itself already decides fate.
Otherwise keep reducing.

### Step 5: freeze one first parser/router consumer
Pick the smallest consumer that matters:
- one first parser/decoder
- one request/response matcher
- one queue/router that makes the result behaviorally real

This is usually the right reducer when callback existence alone is still too weak.

### Step 6: prove one later visible consequence
Stop once you can show:
- submit -> completion or cancel-fate -> callback/giveback -> first consumer -> visible consequence

Do not keep widening into whole-driver or whole-application narration if this smaller chain already answers the operator’s question.

## 6. Practical stop rules this note preserves
- `submitted != retired or safely reusable`
- `usb_unlink_urb() returned != completion handler finished`
- `libusb_cancel_transfer() returned != callback arrived with cancelled status`
- `usbmon callback visible != full payload captured`
- `status/actual_length visible != parser input truth`
- `callback exists != first parser/router consumer proved`
- `callback fired != later visible consequence truth`
- for libusb isochronous cases: `transfer status COMPLETED != every packet/frame clean`

## 7. Practical scenarios

### Scenario A: `usb_submit_urb(...)` plus `usb_unlink_urb()` is visible
Wrong stop:
- “the driver submitted then unlinked the URB, so the transfer path is dead”

Better stop:
- freeze whether you only have async cancel request truth or whether the completion handler has actually finished and the object is idle
- then decide whether one callback/parser path still fired and owned later behavior

### Scenario B: usbmon shows a callback/completion line
Wrong stop:
- “usbmon shows completion, so later app behavior is explained”

Better stop:
- keep monitor-visible completion metadata separate from full payload capture
- then keep payload capture separate from the first callback/parser/router that gave the completed bytes meaning

### Scenario C: libusb async callback exists
Wrong stop:
- “the callback exists, so that’s already the owner”

Better stop:
- prove which callback-side parser/matcher/router actually owns the later behavior you care about
- if cancellation is involved, keep `cancel requested` separate from `callback returned with cancelled status`

### Scenario D: periodic interrupt/ISO traffic looks continuous
Wrong stop:
- “continuous activity means one long-lived consumer path is already obvious”

Better stop:
- freeze whether the activity only persists because the completion callback resubmits the transfer
- then decide whether the real owner is resubmit logic, parser/router logic, or one later consequence-bearing consumer

## 8. Why this note exists in the firmware/protocol branch
The firmware/protocol subtree already had practical notes for descriptor ownership, request lifetime realism, MMIO effect proof, and deferred worker consequences.
What it lacked at first was a thinner practical continuation for **USB URB / async transfer completion ownership**.

This note now preserves the sharper ladder:
- submission / queueing
- retire / cancel truth
- usbmon / monitor-visible completion truth
- callback / giveback truth
- first completion consumer
- later visible consequence

instead of collapsing everything into “USB traffic exists” or “cancel happened.”

## 9. Sources
See:
- `sources/protocol-and-network-recovery/2026-04-06-usb-urb-completion-and-first-consumer-notes.md`
- `sources/protocol/2026-04-18-usb-urb-giveback-cancel-and-usbmon-realism-notes.md`

Primary anchors retained:
- Linux kernel URB documentation
- Linux usbmon documentation
- libusb async/callback semantics retained conservatively through accessible mirrors/snippets after official SourceForge pages were surfaced by search but blocked during direct fetch
- explicit `search-layer` multi-source attempt with `--source exa,tavily,grok`
