# Posted MMIO / Doorbell Observation Notes

Date: 2026-03-27 06:16 Asia/Shanghai / 2026-03-26 22:16 UTC
Topic: firmware/protocol practical continuation, posted MMIO writes, doorbell/notify observation realism

## Why this note exists
A recurring thin-but-practical firmware/protocol failure mode is overreading a doorbell or MMIO write as if it already proved device observation.

In many descriptor/mailbox/MMIO cases, the useful stop rule is narrower:
- staged descriptor or command data exists
- doorbell / submit / tail / MMIO write happened
- device or peer can now actually observe the kick under the case's ordering rules
- later completion / status / ISR / worker consequence proves it mattered

Those are not always the same proof object.

## Conservative retained takeaways
### 1. Linux kernel docs preserve a real split between ordered MMIO accessors and posted bus behavior
`device-io.rst` explicitly says normal `readl()` / `writel()` accessors are ordered relative to each other, but bus behavior can still be asynchronous, and PCI writes are commonly posted asynchronously.

Practical consequence:
- `writel()` occurring in code is stronger than a raw memory store
- but it is still weaker than proving the device has observed the write in cases where posted-write flush matters

### 2. Linux kernel docs explicitly recommend read-back from the device to flush pending posted writes when that property matters
`io_ordering.html` and `device-io.rst` both preserve the driver pattern of reading a safe register after an MMIO write to force pending writes to reach the device before continuing.

Practical consequence:
- `doorbell written` can still be weaker than `doorbell write flushed / device-observable`
- especially around lock release, producer handoff, or multi-CPU driver interactions

### 3. The more truthful proof chain is often `published object != notified peer != peer necessarily observed final state != later consequence`
For reverse-engineering work, this means analysts should preserve at least these separate boundaries when the case is MMIO/doorbell-shaped:
- descriptor or command prepared
- descriptor or command published to shared object/ring/mailbox memory
- notify / tail / doorbell MMIO write issued
- posted-write flush or equivalent device-observation condition satisfied when the platform/case requires it
- later completion/status/ISR/worker consequence

### 4. Non-relaxed vs relaxed accessors and generic memory-barrier talk do not remove the need for case-shaped bus-observation proof
Kernel docs preserve that normal accessors serialize MMIO operations, and memory-barriers docs preserve device-ordering concerns, but neither collapses away the practical driver rule that some buses still require a read-back or equivalent flush when the analyst specifically cares that the device has received the earlier write.

Practical consequence:
- barrier vocabulary alone is too abstract for the KB's workflow use
- the practical analyst target is the smallest trustworthy observation boundary in the case at hand

## Analyst stop rule worth preserving
For descriptor/mailbox/MMIO continuations, a conservative shorthand is:
- `published != doorbelled != observed-by-device != consequence`

Interpret conservatively:
- in some platforms/cases, `doorbelled` may be good enough operationally
- in others, especially when docs/code show safe-register read-back, config-space read fallback, or explicit flush sequencing, treating `doorbelled` as full observation proof is too strong

## Where this should affect KB routing
This note most directly sharpens:
- `topics/mailbox-doorbell-command-completion-workflow-note.md`
- `topics/descriptor-ownership-transfer-and-completion-visibility-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/protocol-firmware-practical-subtree-guide.md`

Reason:
- mailbox note should preserve that submit/doorbell publication may still be weaker than peer observation
- descriptor ownership/visibility note should preserve that notify is not automatically the full trust boundary
- MMIO effect note should preserve that the first effect-bearing write can still require observation realism before later consequence claims are trusted
- subtree routing should make this a named continuation seam instead of burying it under generic barrier language

## Sources used
- Linux kernel docs: <https://docs.kernel.org/driver-api/io_ordering.html>
- Linux kernel docs: <https://www.kernel.org/doc/Documentation/driver-api/device-io.rst>
- Linux kernel docs: <https://www.kernel.org/doc/html/latest/core-api/wrappers/memory-barriers.html>
- Eli Billauer: <https://billauer.se/blog/2014/08/wmb-rmb-mmiomb-effects/>

## Search-source context
Search for this note was attempted explicitly through `search-layer --source exa,tavily,grok`.
Observed result quality was degraded but usable:
- Exa returned usable material in the merged result set for this run
- Tavily returned usable material in the merged result set for this run
- Grok invocation failed with `502 Bad Gateway`

Accordingly, this note keeps only conservative workflow-facing claims and relies primarily on direct confirmation from the Linux kernel docs for the core stop rule.