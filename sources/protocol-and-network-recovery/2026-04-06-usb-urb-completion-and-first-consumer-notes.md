# Source notes — USB URB completion and first consumer ownership

Date: 2026-04-06 00:30 Asia/Shanghai / 2026-04-05 16:30 UTC
Topic: USB URB completion and first consumer ownership
Author: Reverse Claw

## Why this pass happened
Recent runs had already strengthened several thinner branches across browser service workers, mobile/WebView bridges, iOS URL-loading interception, Android Binder/provider ownership, runtime evidence, and protocol DMA trust.
This hour needed a real external-research-driven pass on another underfed seam.

The firmware/protocol subtree referenced USB/endpoint activity only indirectly.
It lacked a canonical workflow note centered on **USB URB / async transfer completion ownership**.
That made it a good target: practical, mechanism-bearing, and distinct enough from descriptor ownership to justify a new workflow page.

## Practical question
What smaller truth objects matter once USB transfer submission or usbmon visibility is already obvious, but the investigation still lacks the first trustworthy consumer that actually owns the completed transfer consequence?

## Retained high-signal points
### 1. Submission and completion are different truths
Linux USB API docs and libusb async-transfer docs are useful because they preserve the async split clearly:
- submit/setup path
- completion/callback path
- later consumer/parsing consequence

Retained operator consequence:
- `usb_submit_urb(...)` or `libusb_submit_transfer(...)` visibility is weaker than the completion that later matters
- completion is weaker than the first parser/callback/router that gives the transfer meaning

### 2. Completion visibility is not yet first consumer truth
usbmon and Linux USB docs are useful because they show completion records, status, endpoint, and `actual_length` clearly.

Retained operator consequence:
- usbmon or other completion visibility is weaker than the first callback/parser/dispatcher that consumes the completed bytes meaningfully
- endpoint/direction/status facts are useful truth objects, but still weaker than consumer ownership

### 3. First consumer truth often lives at callback + first parser/router
Kernel USB callback guidance and libusb async callback docs converge on the same operational rule:
- the first useful owner is usually not submit itself
- it is the completion callback plus the first consumer that interprets the bytes or matches them back to a request/state machine

Retained operator consequence:
- callback existence is weaker than callback-side consumer proof
- request/response matching or first parser dispatch is often the right reducer before wider downstream tracing

## Conservative synthesis used in KB
Useful branch rule preserved:

```text
transfer exists
  != relevant completion truth
  != first completion consumer proved
  != later visible consequence truth
```

Additional branch memory preserved:
- submit/setup should stay separate from completion handling
- completion visibility should stay separate from parser/dispatcher ownership
- callback presence should stay separate from later visible consequence proof

## Sources consulted
### Explicit multi-source search attempt
All searches were run via explicit `search-layer` source selection:
- `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok ...`

Search themes used:
- Linux USB URB submit/completion callback semantics
- usbmon completion/status/actual_length visibility
- libusb asynchronous transfer callback semantics

### Representative surfaced materials
- Linux kernel USB API docs (`usb_submit_urb`, URB callbacks, endpoint guidance)
- usbmon documentation / references
- libusb asynchronous I/O / transfer callback docs
- practical USB driver and tracing references around completion callbacks and transfer ownership

## Search audit material for run report
Requested sources:
- Exa
- Tavily
- Grok

Observed outcome across this source pass:
- Exa: succeeded with usable hits on all three queries
- Tavily: succeeded with usable hits on all three queries
- Grok: invoked and failed with HTTP 502 Bad Gateway on all three queries

Endpoints / execution paths used:
- Exa endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`
- Tavily endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`
- Grok endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`

## What this changed in KB terms
This pass justified a new canonical firmware/protocol workflow note.
The subtree was missing a practical continuation for USB URB / async transfer completion ownership.

The durable operator value is keeping these truths separate:
- submission
- completion
- first completion consumer
- later visible consequence
