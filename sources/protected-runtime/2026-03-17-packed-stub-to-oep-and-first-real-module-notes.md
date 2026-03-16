# Source notes — packed stub to OEP and first real module / consumer workflow

Generated: 2026-03-17 03:30 Asia/Shanghai

## Focus
Strengthen the KB’s deobfuscation / protected-runtime practical branch with a workflow for the recurring case where:
- packing, shelling, staged bootstrap, or loader-heavy startup is already visible
- the analyst can already see a stub, loader loop, memory-copy/decrypt behavior, import repair, or section-permission churn
- but the first trustworthy post-unpack execution boundary is still unclear
- and the investigation still needs one reusable static handoff target rather than another vague “probably unpacked now” trace

This note is intentionally workflow-centered.
It is meant to support a practical KB page rather than a packer taxonomy.

## Source base used
### Existing KB synthesis pages
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/runtime-behavior-recovery.md`
- `topics/native-binary-reversing-baseline.md`
- `topics/record-replay-and-omniscient-debugging.md`

### Existing practical notes used for pattern transfer
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- `topics/flattened-dispatcher-to-state-edge-workflow-note.md`
- `topics/native-semantic-anchor-stabilization-workflow-note.md`
- `topics/native-interface-to-state-proof-workflow-note.md`

### Existing source notes
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`
- `sources/datasets-benchmarks/2026-03-14-obfuscation-benchmarks-source-notes.md`
- `sources/protected-runtime/2026-03-14-evaluation-and-cases.md`

## High-signal extracted patterns

### 1. Packed-target work often stalls after stub recognition, not before it
Practical protected-target work repeatedly reaches a middle state where the analyst already knows they are looking at:
- a packer stub
- a shell/loader stage
- a decrypt/copy/fixup loop
- an import-resolution or relocation-heavy bootstrap
- or a staged memory-permission transition before real execution

But progress still stalls because “stub found” does not yet answer:
- where the first trustworthy OEP-like handoff really is
- whether the current jump lands in real code or just another loader stage
- which memory image should be dumped or preserved
- which first module/import/object boundary proves that unpacking has reached a reusable analysis state

Useful reformulation:
- finding the stub is orientation
- proving one trustworthy post-unpack boundary is the milestone

### 2. The right unit of progress is often one post-unpack boundary plus one reusable static target
Across packer/shell/deprotect practice signals, the highest-payoff next object is often one of:
- one OEP candidate whose downstream imports/strings/xrefs now look materially more ordinary
- one first real module/object/import family that survives beyond the stub
- one dumped image whose section layout and relocation/import state are now stable enough for real static work
- one first consumer routine after unpacked control leaves the loader logic

That is usually more useful than trying to model every stub helper or anti-dump detail first.

### 3. A useful operator model is stub -> memory transition -> OEP candidate -> first real consumer
A compact workflow shape that keeps recurring is:

```text
packed / loader stub visibility
  -> one narrow bootstrap window
  -> one decisive memory transition or control-transfer boundary
  -> one OEP candidate
  -> one first real import/module/object/consumer anchor
  -> one reusable static target
```

The import/module/consumer anchor matters because OEP by itself is easy to overclaim.
A better handoff is:
- one OEP-like boundary
- plus one downstream ordinary-code anchor proving that the analyst is no longer just naming loader churn

### 4. OEP claims need a consequence-oriented proof style
A useful normalization is that “this looks like OEP” is not enough.
Better proof styles include:
- the transfer lands in code that now references stable imports, strings, or object layouts absent from the stub
- the target memory image remains stable enough to dump and re-open statically
- compare-runs or trace alignment show that this is the first boundary after which ordinary business logic, parser logic, request shaping, policy logic, or payload logic becomes visible
- the first downstream consumer routine can now be named as a realistic next static target

### 5. The workflow should end with a quieter post-unpack target, not a larger bootstrap diary
The best resulting artifacts are usually:
- one dump candidate with a stated reason it is “late enough” and “stable enough”
- one post-unpack module/object/import cluster worth static cleanup
- one first consumer/basic-block family worth careful reconstruction
- one justified watchpoint/hook on the first ordinary-code object after unpacking

If the workflow ends only with a longer list of stub helpers, analyst payoff is still weak.

## Suggested KB contribution
Create a concrete workflow note centered on:
- packed/stub-heavy startup regions
- proving one trustworthy OEP candidate instead of merely recognizing a stub
- coupling the OEP candidate to one first real module/import/object/consumer anchor
- handing back one reusable post-unpack static target

## Compact operator framing
```text
packed or shell-like startup is already visible
  -> pick one late effect or one hoped-for real-code region
  -> mark one narrow bootstrap window
  -> identify one decisive memory/control-transfer boundary
  -> prove one OEP candidate with one downstream ordinary-code anchor
  -> return to static work with one reusable dumped or post-unpack target
```

## Retention note
- No large binaries retained.
- This note is a compact practical consolidation intended to support immediate KB improvement in an underdeveloped deobfuscation / packing branch.
