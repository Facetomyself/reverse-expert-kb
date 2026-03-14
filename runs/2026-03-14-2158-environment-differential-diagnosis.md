# Run Report — 2026-03-14 21:58 Asia/Shanghai

## Focus
Continue turning the mobile / protected-runtime subtree into a coherent practical analyst playbook by adding a diagnosis-oriented workflow note for condition-sensitive drift.

This run focused on a recurring gap across several already-strong pages: the KB had good material on environment checks, misleading evidence, signature workflows, challenge workflows, and alternative observation surfaces, but it still lacked a compact triage method for deciding what kind of drift a case was actually exhibiting.

## What was added
### New concrete workflow note
- `topics/environment-differential-diagnosis-workflow-note.md`

This page adds a practical triage workflow centered on:
- finding the **first divergence point** between two runs
- varying only **one condition axis** at a time
- classifying drift into four useful families:
  - execution drift
  - trust drift
  - session drift
  - observation drift
- using a simple diagnosis matrix to choose the next move
- routing the analyst toward the right deeper workflow note rather than blindly patching local checks or overfocusing on one symptom

## Navigation updates
Updated:
- `index.md`
- `topics/mobile-protected-runtime-subtree-guide.md`

These updates make the mobile subtree’s concrete-note layer more coherent by explicitly adding a triage/diagnosis note to complement the already-added pages for:
- signature / preimage recovery
- challenge / loop-slice analysis
- observation-surface selection

## Why this matters
The subtree was becoming stronger on practical **branch-specific workflows**, but it still needed a page for the earlier diagnosis step that comes before selecting the right branch.

This run helps solve that by giving the subtree a reusable answer to questions like:
- is this really anti-instrumentation, or is it packaging drift?
- is this signature failure, or trust drift?
- is this challenge randomness, or session drift?
- is the app broken, or is the evidence channel broken?

That makes the subtree feel more like an actual investigation system rather than only a set of topic notes.

## Follow-up directions
Natural next steps from here:
1. add a browser-side environment-differential / evidence-trust workflow note for symmetry with the mobile branch
2. add more concrete target-family notes under browser or mobile risk-control branches
3. continue strengthening the “diagnosis -> workflow-note -> deeper branch” navigation style across the KB

## Files changed
- `research/reverse-expert-kb/topics/environment-differential-diagnosis-workflow-note.md`
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/topics/mobile-protected-runtime-subtree-guide.md`
