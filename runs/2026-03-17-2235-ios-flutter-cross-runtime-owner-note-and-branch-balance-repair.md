# Run Report — 2026-03-17 22:35 Asia/Shanghai — iOS Flutter cross-runtime owner note and branch-balance repair

## Summary
This autosync run chose **practical branch deepening inside a weaker mobile sub-branch** rather than more browser/mobile micro-variant growth.

The immediate trigger was direction review after the same-day subtree-guide and branch-balance repairs.
Those repairs had improved branch shape for native, runtime-evidence, malware, protected-runtime, and protocol/firmware work.
Inside the mobile branch, the iOS ladder had already been clarified around topology -> gate -> owner -> policy consumer, but one practical gap still remained:
- repeated source pressure existed for **Flutter/cross-runtime owner recovery on iOS**
- the KB mentioned that pattern in source notes, run reports, and one scenario inside the broad iOS owner note
- there was still no dedicated canonical workflow page for it

Concretely, this run:
- performed direction review with branch-balance awareness
- confirmed browser anti-bot and mobile protected-runtime remain the strongest and most crowded top-level practical branches
- confirmed that adding another browser/mobile micro-note would be a poor balancing choice unless it filled a clearly reusable operator gap
- identified iOS Flutter/cross-runtime owner recovery as a real practical gap with enough source pressure to justify a canonical page
- created a new concrete workflow note: `topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md`
- updated the mobile subtree guide, the broader iOS owner note, `mobile-reversing-and-runtime-instrumentation.md`, and `index.md` so the new note is routed as part of the iOS practical ladder rather than left orphaned
- kept the run search-free and conservative because the required source pressure already existed locally in recent source notes and earlier run reports

## Scope this run
- perform direction review and branch-balance check
- improve the KB itself rather than only preserving more source notes
- fill one practical operator gap in the iOS branch with a case-driven canonical workflow note
- update navigation so the new note becomes part of the real branch shape
- produce a run report, commit KB changes if any, and run archival sync

## Branch-balance review
### Current branch picture
The KB still remains strongest in:
- browser anti-bot / widget / request-signature workflows
- mobile protected-runtime / challenge-loop / hybrid ownership workflows

Recent maintenance also strengthened weaker branches materially:
- native practical routing
- runtime-evidence routing
- malware practical routing
- protected-runtime/deobfuscation routing
- protocol/firmware routing

That means browser/mobile should now be deepened more selectively.
The standard should no longer be “we have more source pressure here, so add another note.”
The better question is:
- does this run fill a reusable operator gap that the KB still cannot route cleanly?

### Why this mobile-adjacent run still made sense
This run did **not** deepen a crowded browser/mobile micro-branch for its own sake.
Instead, it repaired an explicit gap in the iOS practical ladder:
- broad iOS owner localization already existed
- callback/result-to-policy work already existed
- source notes repeatedly showed a narrower but recurring case family where the real bottleneck is cross-runtime owner recovery across iOS shell, Flutter bridge, Dart runtime, and native helpers
- that gap was large enough to keep leaking back into broader pages and reports

So this run was branch-balance compatible because it:
- avoided browser anti-bot growth entirely
- chose a reusable, case-driven mobile sub-branch gap rather than another family-label page
- converted repeated source pressure into one canonical route instead of leaving the pattern diffused across reports and source notes

### Direction decision for this run
The right move was **not** another browser-runtime note, not another broad mobile synthesis pass, and not another search-heavy ingest.
It was to create one practical note for a clearly recurring iOS operator bottleneck:
- when Flutter/Dart execution is part of the real owner search
- when repack/rewrite success is attractive but brittle
- when the best move is often to prefer the runtime that actually executes and prove one consequence-bearing owner there

### Balancing implication
Future autosync runs should continue to prefer:
- weaker branches or weaker branch-shape surfaces first
- practical route-guide or workflow-note repair over abstract taxonomy growth
- mobile/browser deepening only when it fills a real reusable operator gap rather than adding yet another family micro-variant

Good next directions still include:
- deobfuscation case-driven deepening
- firmware/protocol practical leaf refinement only when a repeated bottleneck emerges
- malware leaf expansion if a similarly clear operator gap appears
- iOS/mobile deepening only if another repeatable gap proves too large for existing notes

## Sources consulted
Canonical/navigation pages:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/topics/mobile-protected-runtime-subtree-guide.md`
- `research/reverse-expert-kb/topics/mobile-reversing-and-runtime-instrumentation.md`
- `research/reverse-expert-kb/topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `research/reverse-expert-kb/topics/ios-objc-swift-native-owner-localization-workflow-note.md`
- `research/reverse-expert-kb/topics/ios-result-callback-to-policy-state-workflow-note.md`

Recent run/source material used for synthesis:
- `research/reverse-expert-kb/runs/2026-03-17-1420-sperm-ios-batch-1.md`
- `research/reverse-expert-kb/runs/2026-03-17-1420-sperm-ios-batch-2.md`
- `research/reverse-expert-kb/runs/2026-03-17-1435-ios-branch-balance-and-ladder-consolidation.md`
- `research/reverse-expert-kb/sources/ios-runtime-and-sign-recovery/2026-03-17-sperm-ios-batch-1-notes.md`
- `research/reverse-expert-kb/sources/ios-runtime-and-sign-recovery/2026-03-17-sperm-ios-batch-2-notes.md`

## New findings
### 1. The iOS Flutter/cross-runtime pattern had enough source pressure to deserve canonical status
The KB already had repeated evidence for the same practical lesson:
- Flutter/iOS cases are often not best solved by forcing rebuild/rewrite success
- the recurring bottleneck is proving the first consequence-bearing owner across iOS shell, Flutter bridge, Dart runtime, and native helpers
- that lesson was too important to remain only in run reports and source notes

### 2. The broad iOS owner note was carrying too much cross-runtime weight
The general iOS owner-localization note should stay broad and reusable for ObjC / Swift / native cases.
Leaving the Flutter/Dart cross-runtime workflow inside it risked making the page less crisp.
This run improved branch clarity by pulling that pattern into its own specialized note.

### 3. The most durable practical rule is “prefer the runtime that actually executes”
The strongest reusable iOS Flutter rule after this run is:
- freeze one representative flow
- stop treating repack/rewrite success as the real milestone
- recover candidate owners in the runtime that already executes
- prove one Dart owner plus one downstream consequence before deepening lower-level helpers

### 4. This fills a real branch gap without drifting into abstract taxonomy
The new page is not a family-label page for Flutter.
It is a concrete operator workflow note about:
- shell vs bridge vs owner vs worker separation
- live-runtime fallback when rebuild paths are brittle
- proving one consequence-bearing owner instead of collecting framework trivia

## Reflections / synthesis
This was the right kind of autosync run.
It improved the KB itself and reduced a repeated pattern leak.

The deeper structural takeaway is that the iOS ladder is now more precise:
- broad gate stabilization
- broad owner localization
- specialized Flutter/cross-runtime owner recovery when needed
- callback/result-to-policy consequence work later

That matters because Flutter/iOS targets can feel like a special-case swamp even when the real expert move is still simple:
- stop asking which framework is most interesting
- ask which runtime first owns the exact field or effect you care about
- prove that owner with one visible consequence

The new note keeps that rule explicit.

## Candidate topic pages to create or improve
This run created one new canonical page and suggests a few nearby possibilities if later source pressure justifies them:
- `topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md` ✅ created this run
- plausible future nearby improvements:
  - a dedicated Chomper / execution-assisted owner-recovery workflow note if repeated iOS black-box invocation cases continue to accumulate
  - a dedicated iOS traffic-topology relocation note if non-jailbroken full-tunnel / transparent MITM cases continue to recur enough to justify a narrower entry note
  - a cross-platform Flutter owner-localization bridge note only if Android and iOS material converge enough that a platform-specific note no longer explains the recurring bottlenecks well

## Next-step research directions
Preferred direction after this run:
1. keep biasing autosync work toward weaker branches or clearly missing route-guide/workflow-note surfaces rather than crowded browser/mobile family variants
2. continue converting repeated source pressure into canonical pages only when a practical operator gap is clearly reusable
3. if mobile/iOS work is chosen again soon, prefer a similarly sharp missing bottleneck rather than more ambient branch density
4. watch whether Chomper/execution-assisted owner recovery now has enough repeated case pressure to justify its own practical note

## Concrete scenario notes or actionable tactics added this run
This run added or clarified the following practical guidance in canonical pages:
- iOS Flutter targets should be handled as a cross-runtime owner-localization problem when the real bottleneck spans iOS shell, Flutter bridge, Dart runtime, and native workers
- repack/rewrite success should not be treated as mandatory if the live runtime already executes the target flow well enough to recover the owner there
- the preferred compact role labels for these cases are now: trigger -> bridge -> owner -> worker -> effect
- the mobile subtree guide now routes Flutter-shaped iOS cases into a dedicated note instead of leaving the pattern implicit inside broader owner-localization guidance
- the broad iOS owner note now stays cleaner by routing the specialized Flutter/cross-runtime pattern outward instead of trying to carry it inline

## Search audit
This run did **not** use web research.

- Search sources requested: none
- Search sources succeeded: none
- Search sources failed: none
- Exa endpoint: not used in this run (host configuration notes indicate `http://158.178.236.241:7860`)
- Tavily endpoint: not used in this run (host configuration notes indicate `http://proxy.zhangxuemin.work:9874/api`)
- Grok endpoint: not used in this run (host configuration notes indicate `http://proxy.zhangxuemin.work:8000/v1`)

## Files changed this run
- `research/reverse-expert-kb/topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md`
- `research/reverse-expert-kb/topics/mobile-protected-runtime-subtree-guide.md`
- `research/reverse-expert-kb/topics/ios-objc-swift-native-owner-localization-workflow-note.md`
- `research/reverse-expert-kb/topics/mobile-reversing-and-runtime-instrumentation.md`
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/runs/2026-03-17-2235-ios-flutter-cross-runtime-owner-note-and-branch-balance-repair.md`

## Commit / sync status
Pending at report-write time.
This run should:
- commit the reverse-KB files changed by this run
- then run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

If sync fails, local progress should still be preserved and the failure should be noted without discarding KB changes.

## Outcome
The reverse KB now has a dedicated practical workflow note for iOS Flutter/cross-runtime owner recovery, plus updated routing so that the note behaves like a real part of the iOS branch rather than a pattern scattered across reports.
This run improved a concrete operator gap while staying branch-balance aware.
