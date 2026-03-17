# Run Report — 2026-03-17 14:35 Asia/Shanghai — iOS branch-balance and ladder consolidation

## Summary
This autosync run chose **canonical KB maintenance** over more source extraction.
The immediate goal was to convert the newly accumulated iOS `sperm/md` ingest into stronger KB structure while also performing an explicit branch-balance review.

Concretely, this run:
- reviewed current branch distribution and recent run concentration
- confirmed browser/mobile remain the dominant practical branches
- consolidated the iOS practical ladder around **topology -> gate -> owner -> policy consumer**
- strengthened the iOS gate note to cover observation topology and install/sign path as first-class gate surfaces
- strengthened the iOS owner-localization note with a clearer live-runtime fallback / cross-runtime owner-recovery pattern
- updated the mobile subtree guide so the iOS branch reads more coherently as a practical operator ladder

## Scope this run
- perform the required direction review and branch-balance check
- improve canonical KB pages rather than only adding more source notes
- make the iOS practical branch more operational and easier to route through
- preserve the result with a run report, commit, and sync

## Branch-balance review
### Current branch strength snapshot
A rough topic-count pass showed:
- browser: 27 topic files
- mobile: 24 topic files
- protocol / firmware: 8 topic files
- native: 8 topic files
- deobfuscation: 6 topic files
- malware: 5 topic files

### Interpretation
The KB still has a clear center of gravity in:
- browser anti-bot / request-signature / runtime workflows
- mobile protected-runtime / hybrid-app / challenge-loop workflows

Those branches are now strong enough that additional growth there should increasingly prefer:
- consolidation
- ladder cleanup
- route-guide clarification
- selective practical deepening only when fresh source material really changes the operator model

Meanwhile, weaker branches remain:
- malware practical workflows
- deobfuscation case-driven workflows
- protocol / firmware practical workflows
- native desktop/server practical workflows

### Direction decision for this run
Even though mobile is already strong, the recent `sperm/md` ingest had just opened a meaningful **iOS practical sub-branch** that still needed canonical folding.
So the right choice this run was not new browser/mobile expansion, but **iOS branch consolidation inside the already-strong mobile branch**.

That means this run still respected branch-balance awareness because it:
- did not deepen browser anti-bot again
- did not create more isolated source-only notes
- used the latest iOS ingest to tighten canonical routing and practical workflow language

### Next balancing implication
Future autosync runs should bias toward weaker but high-value branches unless another nearly-complete local consolidation step appears.
Especially attractive next directions now look like:
- malware branch deepening
- protocol / firmware branch practical strengthening
- deobfuscation case-driven expansion
- native desktop/server branch maturation

## Sources consulted
Canonical/navigation pages:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/topics/mobile-protected-runtime-subtree-guide.md`
- `research/reverse-expert-kb/topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `research/reverse-expert-kb/topics/ios-objc-swift-native-owner-localization-workflow-note.md`
- `research/reverse-expert-kb/topics/ios-result-callback-to-policy-state-workflow-note.md`

Recent run/source material used for synthesis:
- `research/reverse-expert-kb/runs/2026-03-17-1420-sperm-ios-batch-1.md`
- `research/reverse-expert-kb/runs/2026-03-17-1420-sperm-ios-batch-2.md`
- `research/reverse-expert-kb/sources/ios-runtime-and-sign-recovery/2026-03-17-sperm-ios-batch-1-notes.md`
- `research/reverse-expert-kb/sources/ios-runtime-and-sign-recovery/2026-03-17-sperm-ios-batch-2-notes.md`

## New findings
### 1. iOS practical routing benefits from making topology explicit before gate diagnosis
The latest source batches reinforced that many iOS cases fail early simply because the analyst is standing on the wrong capture or runtime-observation surface.
That belongs in canonical guidance, not only in source notes.

### 2. Install/sign path is part of the gate surface, not unrelated setup trivia
Apple-ID sign, certificate sign, TrollStore, jailbreak-side install, and rootful/rootless assumptions all materially affect later evidence quality.
The KB now says that more directly.

### 3. Cross-runtime iOS cases need a stronger live-runtime fallback rule
The Flutter-style source material reinforced a practical lesson worth canonicalizing: when repack/rewrite paths are brittle, move to the runtime that actually executes and recover the consequence-bearing owner there.

### 4. The iOS branch is strongest when read as a ladder, not a bag of notes
The most useful compact formulation after this run is:
- topology
- gate
- owner
- policy consumer

That reading order now appears more explicitly in the mobile subtree guide and adjacent iOS notes.

## Reflections / synthesis
This was the right kind of maintenance run.
It improved the KB itself instead of merely adding another extraction artifact.

The deeper structural takeaway is that the iOS branch now looks less like a special case and more like a compact instance of the KB’s wider philosophy:
- choose the right observation surface
- stabilize the first trustworthy prerequisites
- localize the real owner
- then reduce visible results into the first consequence-bearing policy consumer

That symmetry is valuable because it makes the KB easier to navigate across branches without flattening platform differences.

## Candidate topic pages to create or improve
Still plausible future iOS-facing pages if later source pressure justifies them:
- a dedicated iOS traffic-topology relocation workflow note
- a dedicated Chomper / execution-assisted owner-recovery workflow note
- a dedicated iOS cross-runtime owner-localization note for Flutter-like targets

Outside iOS, the strongest candidate areas for future improvement remain:
- malware practical branch pages
- protocol / firmware route-guide strengthening
- deobfuscation case-driven workflow deepening
- native practical branch maturation

## Next-step research directions
Preferred direction after this run:
1. bias upcoming autosync work toward weaker branches unless a very small remaining iOS consolidation step appears
2. prioritize practical scenario pages over new abstract taxonomy pages
3. when using the remaining `sperm/md` ingest later, fold insights into canonical pages sooner rather than letting source notes pile up

## Concrete scenario notes or actionable tactics added this run
This run added or clarified the following practical tactics in canonical pages:
- treat **observation / traffic topology** as an iOS gate-like prerequisite when current visibility is misleading
- treat **install/sign path** as part of the runtime gate surface
- use **topology -> gate -> owner** as a compact iOS triage rule
- for cross-runtime iOS cases, prefer **live-runtime owner recovery** when repack/rewrite paths are unstable
- read the iOS branch as a ladder ending in the first **behavior-changing policy consumer**

## Files changed this run
- `research/reverse-expert-kb/topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `research/reverse-expert-kb/topics/ios-objc-swift-native-owner-localization-workflow-note.md`
- `research/reverse-expert-kb/topics/mobile-protected-runtime-subtree-guide.md`
- `research/reverse-expert-kb/runs/2026-03-17-1435-ios-branch-balance-and-ladder-consolidation.md`

## Commit / sync status
Pending at report-write time.
This run should commit if diffs remain and then run:
- `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

If sync fails, local progress should still be preserved and the failure should be noted without discarding the KB changes.

## Outcome
The reverse KB now has a clearer iOS practical operator ladder and a more explicit branch-balance assessment.
This run improved canonical routing and workflow language rather than only extending source-note coverage.
