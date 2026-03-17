# Source notes — integrity-check to tamper-consequence workflow

Generated: 2026-03-17 09:30 Asia/Shanghai

## Focus
Strengthen the KB’s protected-runtime practical branch with a workflow for the recurring case where:
- integrity, CRC, checksum, signature, or self-verification logic is already visible
- the analyst can already name candidate check helpers, code-region coverage, or result flags
- but the first local branch that turns that check result into a real consequence is still unclear
- and the investigation still needs one consequence-bearing tripwire rather than a broader catalog of checks

This note is intentionally workflow-centered.
It is meant to support a practical KB page rather than a general anti-tamper taxonomy.

## Source base used
### Existing KB synthesis pages
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/runtime-behavior-recovery.md`
- `topics/observation-distortion-and-misleading-evidence.md`

### Existing practical notes used for pattern transfer
- `topics/environment-differential-diagnosis-workflow-note.md`
- `topics/trace-slice-to-handler-reconstruction-workflow-note.md`
- `topics/flattened-dispatcher-to-state-edge-workflow-note.md`
- `topics/packed-stub-to-oep-and-first-real-module-workflow-note.md`
- `topics/attestation-verdict-to-policy-state-workflow-note.md`

### Existing source notes
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`
- `sources/protected-runtime/2026-03-14-evaluation-and-cases.md`

## High-signal extracted patterns

### 1. Integrity-check visibility is not yet behavioral leverage
Practical protected-target work often reaches a middle state where the analyst already knows they are looking at:
- CRC or checksum helpers
- self-hash / self-verify routines
- signature, code-section, or loader-integrity checks
- anti-patch / anti-hook / anti-dump verification passes
- result flags or compare outcomes near suspicious regions

But progress still stalls because “the check is here” does not yet answer:
- which local branch or reducer actually decides what happens next
- whether the check only logs, only seeds later state, or immediately gates execution
- where a failed or suspicious result becomes sleep, exit, fallback, decoy, degraded feature mode, or crash behavior
- which point is stable enough to use as the next hook, watchpoint, compare-run anchor, or static target

Useful reformulation:
- finding the check is orientation
- proving the first consequence-bearing tripwire is the milestone

### 2. The right unit of progress is often one tripwire plus one downstream effect
Across CRC / anti-hook / integrity-sensitive practice signals, the highest-payoff next object is often one of:
- one reduction helper that compresses many per-region checks into one suspicious/clean bucket
- one state flag, enum, or mode write that survives beyond the check helper
- one scheduler/request/policy branch that only changes after the integrity result is reduced
- one decoy/real-path split or exit/degrade split attributable to the check result

That is usually more useful than enumerating every protected region or every hash/check helper first.

### 3. A useful operator model is check surface -> result reduction -> tripwire -> consequence
A compact workflow shape that keeps recurring is:

```text
integrity / self-check visibility
  -> one narrow check window
  -> one result or reduction helper
  -> one consequence-bearing tripwire
  -> one downstream effect
  -> one smaller next static or runtime target
```

The reduction stage matters because many targets do not act directly on one raw checksum mismatch.
They first reduce many noisy checks into one smaller policy/result bucket.

### 4. Tripwire claims need consequence-oriented proof, not only check-oriented labeling
A useful normalization is that “this computes the CRC” or “this compares a digest” is not enough.
Better proof styles include:
- compare-runs showing that the first stable divergence appears at one branch/state write after the check result forms
- one state/mode flag that differs only when the integrity-sensitive behavior changes
- one later scheduler, request, or feature-path difference attributable to a single reducer or branch
- one decoy-vs-real path split or exit/degrade/crash family that only occurs after the candidate tripwire

### 5. The workflow should end with a quieter consequence target, not a larger integrity diary
The best resulting artifacts are usually:
- one reducer/helper worth careful pseudocode cleanup
- one state flag/object worth renaming and watching
- one consequence-bearing branch worth compare-run proof
- one later consumer/scheduler/request hook justified by the tripwire proof

If the workflow ends only with a richer list of checks and protected regions, analyst payoff is still weak.

## Suggested KB contribution
Create a concrete workflow note centered on:
- visible integrity / CRC / self-check logic
- proving one consequence-bearing tripwire instead of only cataloging checks
- coupling the tripwire to one downstream effect
- handing back one smaller static or runtime target for the next pass

## Compact operator framing
```text
integrity or tamper checks are already visible
  -> pick one late effect or one divergence worth explaining
  -> mark one narrow check window
  -> identify one result-reduction helper or state bucket
  -> prove one consequence-bearing tripwire
  -> return to static/runtime work with one smaller trustworthy target
```

## Retention note
- No large binaries retained.
- This note is a compact practical consolidation intended to support immediate KB improvement in an underdeveloped protected-runtime sub-branch.
