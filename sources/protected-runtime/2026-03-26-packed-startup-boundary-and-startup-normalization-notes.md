# Packed Startup Boundary and Startup Normalization Notes — 2026-03-26

Topic focus:
- Windows/native packed-startup cases where analysts can already see a convincing stub exit or OEP-like transfer, but the first durable payload-bearing target is still one startup stage later

Primary question:
- what smaller proof object should be frozen before claiming the packer handoff has reached the first real payload owner?

## Search-backed source anchors retained
- Microsoft Learn — PE format
  - https://learn.microsoft.com/en-us/windows/win32/debug/pe-format
- Unprotect Project — TLS Callback
  - https://unprotect.it/technique/tls-callback/
- search-layer artifact for this run:
  - `sources/protected-runtime/2026-03-26-1816-packed-startup-handoff-search-layer.txt`

## Conservative synthesis
Two source-backed facts are enough to sharpen the KB without overclaiming internals:

1. PE/TLS startup surfaces are real pre-entry execution boundaries.
   - The PE format keeps `.tls` as a first-class image section/data-directory concept.
   - TLS callbacks can execute before the program's nominal main entry path that many analysts/debuggers want to treat as “the start”.

2. Therefore a visible unpacking transfer is not automatically the same thing as the first payload-bearing handoff.
   - Even after the stub exits, the next region can still be startup-owned rather than payload-owned.
   - In practical Windows/native packed cases, that startup-owned region may still be dominated by TLS callback replay, CRT/runtime startup, constructor/init-table work, import finalization, or loader-side image repair/remap activity.

## Practical refinement preserved this run
The branch should keep these proof objects separate:
- **raw PE entry truth**
- **startup-owned pre-entry truth**
- **raw post-unpack transfer truth**
- **startup-normalized payload handoff truth**
- **first real consumer truth**

Compact operator shorthand:

```text
raw_entry != pre_entry_startup != unpack_transfer != payload_handoff != consumed
```

This is narrower and more useful than another generic “OEP is tricky” reminder.

## Why this matters operationally
Two recurring mistakes keep showing up in packed/native cases:

### Subcase A: valid stub exit, invalid payload claim
- the analyst really did find the first convincing transfer out of the visible stub
- but the next region still mostly performs startup normalization rather than payload logic
- if the branch stops there, later static work keeps reopening loader/startup scaffolding instead of a stable payload target

### Subcase B: pre-entry activity is visible but flattened into “anti-debug stuff”
- TLS callback or adjacent startup activity runs before the expected entry path
- the analyst treats that only as anti-debug color instead of as a real startup-owned boundary that changes where payload proof should begin
- result: raw entry, pre-entry startup, and later payload handoff collapse into one vague startup story

## Practical stop rule
In Windows/native packed cases:
- if the current proof object is only the first strong transfer out of stub/decrypt/fixup churn, keep it as **raw post-unpack transfer truth**
- if the next region is still dominated by TLS callbacks, CRT/runtime startup, constructor/init-table replay, import finalization, or loader-side repair/remap, keep it as **startup-owned truth** rather than payload proof
- only upgrade the handoff when one import/module/object/consumer anchor remains useful after startup-owned work quiets down
- if a later consumer is already the smallest truthful object, freeze that instead of arguing abstractly about “the real OEP”

## Good canonical KB targets from this note
- `topics/packed-stub-to-oep-and-first-real-module-workflow-note.md`
- `topics/protected-runtime-practical-subtree-guide.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `index.md`

## Search/source quality note
This run used an explicit multi-source `search-layer --source exa,tavily,grok` attempt.
- Exa and Tavily returned usable leads, including the PE/TLS surfaces above.
- Grok returned no usable results in the recorded artifact.
- StackExchange follow-up fetch was blocked/403 and is therefore not used as a retained factual anchor.

So the retained synthesis here is intentionally modest and workflow-centered rather than overclaiming detailed loader internals from weak sources.
