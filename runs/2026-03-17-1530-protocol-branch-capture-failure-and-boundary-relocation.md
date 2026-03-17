# Run Report — 2026-03-17 15:30 Asia/Shanghai — protocol branch capture-failure and boundary-relocation consolidation

## Summary
This autosync run chose **canonical protocol-branch maintenance** over more source extraction.

The immediate goal was to convert the newest `sperm/md` protocol/network ingest into a stronger practical entry surface for the weaker firmware/protocol branch.
The KB already had good practical notes for:
- ingress ownership
- parser-to-state consequence
- replay/state-gate diagnosis
- reply-emission / transport handoff

But it still lacked a first-class workflow note for the operator step that often comes **before** all of those:
- diagnosing why meaningful traffic is still not visible from the current surface
- proving whether the case is dominated by proxy bypass, trust-path mismatch, non-HTTP/private-overlay boundaries, environment-conditioned visibility, or a deeper content pipeline
- relocating to the first trustworthy object before doing parser/state work

Concretely, this run:
- reviewed recent protocol and iOS consolidation work for branch-balance context
- used the newest protocol batch-3 source note as the main practical pressure signal
- created a new canonical workflow note for protocol capture-failure and boundary relocation
- updated the protocol and firmware parent pages so this note becomes part of the practical branch, not an orphan
- updated `index.md` so the firmware/protocol branch now reads in a more realistic operator order

## Scope this run
- perform direction review with branch-balance awareness
- strengthen the weaker firmware/protocol branch rather than deepening already-strong browser/mobile areas again
- improve canonical KB routing, not just source-note accumulation
- produce a run report, commit if needed, and archival-sync the reverse KB

## Branch-balance review
### Current branch picture
Recent runs have been heavily influenced by the `sperm/md` ingest stream.
That stream has materially enriched:
- Android / protected-runtime
- browser anti-bot / JS runtime
- protocol / network
- iOS practical reversing

However, the broader KB still remains strongest in:
- browser anti-bot / request-signature / widget/session workflows
- mobile protected-runtime / challenge-loop / hybrid-app workflows

The firmware/protocol branch has improved a lot, but still has fewer practical entry surfaces than the strongest branches.
That made it a good candidate for canonical strengthening this run.

### Direction decision for this run
The right move was **not** to do more source-first browser/mobile growth.
It was to spend this run on protocol-branch consolidation, specifically by filling a practical navigation gap:
- before ingress ownership
- before parser-state proof
- before replay-state gates
- before output-side transport handoff

That gap was the recurring real-world question:
- *why is the meaningful traffic/object still not visible from where I am looking?*

### Branch-balance implication
This run respected branch-balance guidance because it:
- avoided deepening already-dominant browser/mobile micro-branches again
- improved a weaker but high-value branch
- converted source pressure into canonical workflow routing instead of merely stacking more extraction notes

Future autosync runs should continue to prefer:
- weaker practical branches
- branch consolidation
- high-value scenario notes

especially in:
- malware practical workflows
- deobfuscation case-driven workflows
- native desktop/server practical routing
- further protocol/firmware subtree refinement if a similarly clear gap appears

## Sources consulted
Canonical/navigation pages:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/topics/protocol-state-and-message-recovery.md`
- `research/reverse-expert-kb/topics/firmware-and-protocol-context-recovery.md`
- `research/reverse-expert-kb/topics/protocol-ingress-ownership-and-receive-path-workflow-note.md`
- `research/reverse-expert-kb/topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`

Recent run/source material used for synthesis:
- `research/reverse-expert-kb/runs/2026-03-17-1448-sperm-protocol-network-batch-3.md`
- `research/reverse-expert-kb/runs/2026-03-17-1435-ios-branch-balance-and-ladder-consolidation.md`
- `research/reverse-expert-kb/sources/protocol-and-network-recovery/2026-03-17-sperm-protocol-network-batch-3-notes.md`
- `research/reverse-expert-kb/sources/ios-runtime-and-sign-recovery/2026-03-17-sperm-ios-batch-2-notes.md`

## New findings
### 1. The protocol branch was still missing a practical entry note for pre-parser visibility failures
This was the most important structural gap found this run.
The branch already had practical notes for later stages, but not for the step where the analyst still cannot trust the current capture surface.

### 2. “Can’t capture it” is often a boundary-selection problem, not a protocol-semantics problem
The latest protocol ingest strongly reinforced that the right next move is often to prove:
- proxy bypass
- trust-path mismatch
- private overlay / socket-boundary ownership
- environment gate
- or content-pipeline continuation

before building parser/state models.

### 3. The nearest trustworthy object is often not the packet
The new canonical note explicitly normalizes several higher-value boundaries:
- transparent interception
- socket write/read plaintext
- serializer or framework objects
- manifest/key/content pipeline boundaries

That keeps the protocol branch aligned with the KB’s broader reduction-first philosophy.

### 4. The protocol branch now has a more realistic operator order
After this run, the branch no longer jumps too quickly from broad synthesis into ingress/parser/state notes.
It now has a clearer earlier entry surface for the very common situation where meaningful visibility has not yet been secured.

## Reflections / synthesis
This was the right kind of autosync run.
It improved the KB itself instead of merely preserving another batch of notes.

The deeper takeaway is that the protocol branch is now reading more like the other strong practical branches:
- first choose the right surface
- then prove the right owner or handoff
- then localize consequence/state edges
- then move into replay or output-side proof

That makes the protocol subtree more usable in real investigations and less dependent on analysts already knowing the right entry point.

## Candidate topic pages to create or improve
This run created one new canonical page and suggests a few plausible nearby future pages if later source pressure justifies them:
- `topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md` ✅ created this run
- possible future child pages:
  - transparent interception proof workflow note
  - socket-boundary private-overlay recovery note
  - HLS/M3U8 manifest-key-content pipeline note
  - environment-conditioned visibility note for protocol/network cases

## Next-step research directions
Preferred direction after this run:
1. continue biasing autosync work toward weaker branches unless another nearly-complete local consolidation step appears
2. keep converting `sperm/md` source pressure into canonical subtree improvements instead of only adding extraction notes
3. look for similarly clear practical routing gaps in:
   - malware branch
   - deobfuscation branch
   - native branch
4. if protocol work is chosen again soon, prefer a similarly practical follow-up such as:
   - explicit transparent-interception proof
   - socket-boundary overlay recovery
   - manifest/key/content pipeline continuation

## Concrete scenario notes or actionable tactics added this run
This run added or clarified the following practical tactics in canonical pages:
- classify capture failure before repeating more bypass work
- distinguish proxy bypass, trust-path mismatch, private-overlay boundaries, environment gates, and deeper content pipelines as separate failure families
- use one narrow compare pair to prove the failure family
- relocate to the nearest trustworthy object rather than insisting on raw packet capture
- treat transparent interception, socket plaintext, and manifest/key/content artifacts as valid protocol entry surfaces
- route into ingress/parser/replay/output notes only after the new boundary is proved

## Files changed this run
- `research/reverse-expert-kb/topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md`
- `research/reverse-expert-kb/topics/protocol-state-and-message-recovery.md`
- `research/reverse-expert-kb/topics/firmware-and-protocol-context-recovery.md`
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/runs/2026-03-17-1530-protocol-branch-capture-failure-and-boundary-relocation.md`

## Commit / sync status
Pending at report-write time.
This run should commit if diffs remain and then run:
- `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

If sync fails, local progress should still be preserved and the failure should be noted without discarding KB changes.

## Outcome
The reverse KB now has a clearer protocol/firmware practical entry surface for cases where the analyst still cannot trust the current capture boundary.
This makes the weaker protocol branch more usable, more case-driven, and better aligned with the KB’s broader workflow philosophy.
