# Source notes — USB URB giveback, cancel, and usbmon realism

Date: 2026-04-18 04:50 Asia/Shanghai / 2026-04-17 20:50 UTC
Topic: USB URB completion ownership, cancel/giveback realism, and usbmon capture limits
Author: Reverse Claw

## Why this pass happened
Recent external runs had rotated across malware, iOS, runtime-evidence, protected-runtime, and a thinner Linux malware continuation.
The protocol / firmware branch had not taken the external slot since the retired-owner vs callback-firing run on 2026-04-13.

The existing USB URB workflow note was still useful, but thinner and less source-backed than neighboring protocol leaves around pending-owner realism and descriptor trust.
That made it a good bounded target for this hour:
- practical
- underfed enough to deserve another external pass
- narrow enough to extend without widening into generic USB or driver taxonomy

## Practical question
Once a case is already narrowed to one USB transfer family, what smaller truth objects still matter before the analyst can honestly claim the completed transfer owns behavior?

More specifically:
- does `usb_submit_urb(...)` or `libusb_submit_transfer(...)` only prove queueing?
- does `usb_unlink_urb()` / `libusb_cancel_transfer()` only prove cancel request, not callback fate?
- does one usbmon callback/completion line only prove monitor-visible completion metadata, not full payload or consumer truth?
- where is the first trustworthy giveback / callback / parser / router boundary?

## Search posture for this run
Search was attempted via the search-layer skill with explicit requested sources:
- Exa
- Tavily
- Grok

Observed source reality:
- Exa: succeeded
- Tavily: succeeded
- Grok: invoked and failed with repeated `502 Bad Gateway` errors through the configured proxy path

Saved search trace:
- `sources/protocol/2026-04-18-0450-usb-urb-giveback-search-layer.txt`

## Retained practical support

### 1. Linux kernel URB docs sharpen queueing vs cancel vs callback-idle truth
Retained sources:
- `https://docs.kernel.org/6.17/driver-api/usb/URB.html`
- `https://docs.kernel.org/6.2/driver-api/usb/callbacks.html`
- older URB documentation surfaced through search for cross-checking historical wording

Retained points:
- `usb_submit_urb()` queues work asynchronously and returns immediately after successful queueing
- `usb_unlink_urb()` is asynchronous: when it returns, the URB will not normally have finished yet, and the driver must still wait for the completion handler
- `usb_kill_urb()` waits until the URB has been returned and the completion handler has finished; only then is the URB totally idle
- even when error or unlink is reported, some data may already have transferred because the transfer is packetized
- completion handlers may run in atomic context; sleeping there is explicitly forbidden
- interrupt URBs are not auto-restarted; if the analyst thinks “continuous USB activity” implies one stable owner, resubmission in the completion path may be the real truth object

Operator consequence:
- queueing truth, cancel-request truth, callback-finished truth, and safe-to-reuse truth are different proof objects
- one observed cancel/unlink call is weaker than “this callback cannot still run”
- one callback invocation is still weaker than the first parser/router consumer that gives the bytes meaning

### 2. usbmon preserves monitor-visible completion metadata, not full consumer truth
Retained source:
- `https://docs.kernel.org/usb/usbmon.html`

Retained points:
- usbmon reports requests made by peripheral-specific drivers to host-controller drivers; if the HCD is buggy, traces may not correspond to bus transactions precisely
- text events distinguish submission (`S`), callback (`C`), and submission error (`E`)
- for callbacks, the reported data length is the actual length, but data words are present only when the data tag is `=`
- usbmon may not capture data even when length is nonzero
- in the binary API, `length` and `len_cap` are different fields, and dropped-event counters are explicit

Operator consequence:
- one usbmon callback/completion line is monitor-visible completion truth first, not parser-input truth
- status/length metadata can be real while payload capture is partial, absent, or dropped
- `usbmon callback visible != full payload captured != first parser/router consumer proved`

### 3. libusb async docs sharpen submit/cancel/callback separation on the user-space side
Retained sources:
- Android GoogleSource mirror of vendored libusb `io.c` comments surfaced by search
- `https://vovkos.github.io/doxyrest/samples/libusb/struct_libusb_transfer.html`
- official libusb SourceForge pages were surfaced by search, but direct fetches hit anti-bot blocking; retained claims were kept conservative and anchored to accessible mirrors/snippets

Retained points:
- libusb’s asynchronous interface explicitly separates submission and completion handling
- libusb documents cancellation as asynchronous/non-blocking in its API comments: `libusb_cancel_transfer()` returning does not mean cancellation is complete; completion is signaled later through the callback with `LIBUSB_TRANSFER_CANCELLED`
- `libusb_transfer.status` and `actual_length` are for callback-time use; the callback is invoked when the transfer completes, fails, or is cancelled
- for isochronous transfers, overall transfer status may still read `COMPLETED` even when some packet-level errors occurred; packet descriptors carry the finer truth

Operator consequence:
- `libusb_cancel_transfer()` return is weaker than callback-fate truth
- one overall libusb transfer status can still be weaker than per-packet truth on isochronous paths
- user-space async USB traces should preserve the same split as kernel URB cases: submitted -> callback-delivered -> first app-side parser/router consumer

## Cross-source synthesis
A compact ladder worth preserving canonically is:

```text
submitted / queued
  != retired or safely reusable
  != usbmon callback/completion visible
  != giveback / callback finished
  != first parser/router consumer proved
  != later visible consequence truth
```

A second cancel-heavy split worth preserving is:

```text
cancel requested
  != callback cannot still run
  != object is safe to free or reuse
  != parser/router will never still see status/bytes
```

A third capture-heavy split worth preserving is:

```text
usbmon status/actual_length visible
  != full payload captured
  != full parser input truth
  != first behavior-owning consumer truth
```

## What this batch does *not* justify
This pass does **not** justify broad claims such as:
- usbmon alone is bus-perfect truth in every case
- one completion callback is automatically the first behavior-owning consumer
- all post-cancel callbacks are stale-owner bugs rather than normal async completion/cancel delivery
- descriptor/ring ownership questions are solved just because one USB transfer family is visible
- isochronous `COMPLETED` means every packet/frame was clean

The narrower justified claim is:
- when one USB transfer family is already isolated, the next honest reduction is usually to keep queueing, cancel/retire, monitor-visible completion, callback-fate, and first parser/router consumer truth separate instead of flattening them into “USB traffic happened”

## KB maintenance conclusion from this batch
This batch justified:
- materially extending `topics/usb-urb-completion-and-first-consumer-workflow-note.md`
- synchronizing the protocol / firmware subtree guide, the protocol parent page, and the top-level index so the sharper stop rules do not remain leaf-local
- recording a fresh protocol-branch source note and explicit tri-source search artifact under `sources/protocol/`

## Search audit material for run report
Requested sources:
- Exa
- Tavily
- Grok

Observed outcome across this pass:
- Exa: succeeded
- Tavily: succeeded
- Grok: invoked and failed with HTTP 502 Bad Gateway

Endpoints / execution paths used:
- Exa endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok --queries "Linux usb_submit_urb usb_unlink_urb usb_kill_urb completion handler documentation" "Linux usbmon completion status actual_length documentation" "libusb asynchronous transfer callback cancel transfer status documentation" "Linux USB URB completion callback interrupt context documentation" --mode deep --intent exploratory --num 5 --domain-boost docs.kernel.org,kernel.org,libusb.sourceforge.io,libusb.info`
- Tavily endpoint: via the same `search.py` invocation above
- Grok endpoint: via configured completions proxy surfaced in runtime errors: `http://proxy.zhangxuemin.work:8000/v1/chat/completions`
