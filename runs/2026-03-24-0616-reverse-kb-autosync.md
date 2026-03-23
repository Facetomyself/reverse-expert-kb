# Reverse KB Autosync Run Report

Date: 2026-03-24 06:16 Asia/Shanghai
Mode: external-research-driven
Scope: `research/reverse-expert-kb/`
Primary branch worked: native practical subtree
Chosen seam: native GUI delivery-boundary stop rule — per-window subclass ownership vs Qt `AutoConnection` / queued delivery consumer boundary

## Summary
This run intentionally avoided another browser/mobile/protected-runtime pass and also avoided spinning up a new broad native GUI page.

Recent runs had already covered:
- runtime-evidence practical work
- malware persistence proof quality
- iOS practical continuation quality

That made native desktop a better branch-balance choice.
Inside native desktop, the GUI/message-pump branch had already been established recently, so the right move here was not another generic GUI overview.
The practical gap was thinner:
- analysts can still stop too early once they see `CallWindowProc`, subclass wrappers, `emit`, or a recovered Qt slot graph
- that can flatten two meaningfully different proof problems into one generic “framework found” bucket

This run therefore did a real explicit multi-source search pass and tightened one operator stop rule:
- **Win32:** subclass presence is not consumer proof until the exact per-window original-proc chain is preserved
- **Qt:** visible `emit` / recovered connection graph is not enough until direct/immediate vs queued/receiver-loop-delivered ownership is classified, especially for `AutoConnection`

That is a KB improvement, not just source collection:
- the canonical native GUI workflow note now preserves the stricter boundary explicitly
- the native subtree guide now remembers the same stop rule at branch-routing level
- the run artifact records the source-backed reasoning and degraded source behavior clearly

## Direction review
This run stayed aligned with the reverse KB’s intended direction:
- improve the KB itself, not just stash notes
- keep work practical and case-driven
- prefer one thinner operator seam over broad taxonomy growth
- preserve workflow truth that changes how a real analyst decides where to stop and where to hand off next

Why this seam was worth doing now:
- the native desktop branch remains thinner than browser/mobile/protected-runtime
- the GUI branch already existed, so a smaller practical refinement had real leverage
- the chosen stop rule directly affects runtime proof quality in real Win32/Qt cases
- it avoided another wording-only maintenance pass while also avoiding a low-value new abstract page

## Branch-balance review
Current balance view after this run:
- **Easy to overfeed:** browser anti-bot, protected-runtime, mobile/WebView continuation seams
- **Recently fed enough:** runtime-evidence, malware persistence, iOS practical continuation
- **Still worth practical strengthening:** native desktop, especially GUI/event-loop ownership where framework visibility can still be mistaken for consumer proof

Why this branch was the right target:
- it is underfed relative to browser/mobile density
- it has practical operator value across ordinary desktop reversing
- the selected seam was narrow enough to improve proof quality without drifting into another large native-framework tutorial

Anti-stagnation check:
- this was a real external-research-driven run
- explicit `exa,tavily,grok` search was attempted
- the output materially sharpened a canonical workflow page
- the run did not collapse into index-only / family-count-only / wording-only maintenance

## External research performed
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries used:
1. `Win32 message pump subclass SetWindowLongPtr CallWindowProc reverse engineering workflow first consumer`
2. `Qt signal slot queued connection event loop reverse engineering first consumer practical`
3. `reverse engineering GUI message loop callback dispatch first meaningful consumer Windows Qt`

Saved raw search artifact:
- `sources/native-and-desktop/2026-03-24-native-gui-consumer-search-layer.txt`

Follow-up fetch/validation used:
- Microsoft Learn — Using Window Procedures
- Raymond Chen / The Old New Thing — original window procedure belongs to the specific window subclassed
- Qt documentation — Threads and QObjects
- Woboq — queued connection internals

## Search audit
Search sources requested:
- exa
- tavily
- grok

Search sources succeeded:
- exa
- tavily

Search sources failed:
- grok

Exa endpoint:
- `http://158.178.236.241:7860`

Tavily endpoint:
- `http://proxy.zhangxuemin.work:9874/api`

Grok endpoint:
- `http://proxy.zhangxuemin.work:8000/v1`

Degraded-mode note:
- this run explicitly attempted all three requested sources
- retained usable search results came from Exa and Tavily
- the saved search artifact shows Grok JSON-parse failures (`Expecting value: line 1 column 1`) and no retained Grok-backed hits for this run
- this therefore counts as a degraded but valid external-research-driven run, with the degraded source set recorded explicitly

## New findings
High-signal source-backed reminders retained this run:
- Win32 message-loop / `WndProc` discovery is still only framework reduction, not consumer proof
- `CallWindowProc` visibility is not by itself enough; the saved original proc belongs to the exact window instance that was subclassed
- Qt delivery classification is not just “signal exists or not”; `AutoConnection` can resolve into direct or queued behavior depending on receiver thread affinity and event-loop reality
- for truly queued Qt cases, the meaningful proof boundary is often receiver-side event-loop delivery or the first slot-side reducer after that delivery, not merely the `emit` site

## Sources consulted
Primary sources used conservatively:
- Microsoft Learn — Using Window Procedures
- Raymond Chen / The Old New Thing — original proc per window instance
- Qt documentation — Threads and QObjects
- Woboq — queued connection internals

Supporting search-layer results retained in the audit trail:
- Microsoft Learn API pages for `CallWindowProcA` and `SetWindowLongPtrA`
- Stack Overflow / KDAB / deKonvoluted / Qt ecosystem references for delivery intuition and debugging cues

## Reflections / synthesis
The practical improvement here is small but important.

The GUI page already preserved:
- do not stop at `WndProc`
- do not assume all Qt signal/slot edges are queued

What it still risked flattening was the proof boundary itself:
- in Win32, shared-looking subclass wrappers can still hide different per-window ownership chains
- in Qt, `AutoConnection` can make two very similar-looking static graphs behave as different delivery shapes at runtime

The better rule is:
- if the case is Win32 subclass-heavy, preserve the exact per-window original-proc chain before treating the wrapper as the first real consumer
- if the case is Qt direct or same-thread `AutoConnection`, the slot-side state write may already be the right consumer boundary
- if the case is Qt queued or cross-thread `AutoConnection`, preserve receiver-loop delivery separately and do not collapse the `emit` site into the final proof object

That changes how an analyst picks hooks, what they consider “good enough” proof, and when they hand off to reverse-causality or broader runtime evidence.

## Candidate topic pages to create or improve
Improved this run:
- `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md`
- `topics/native-practical-subtree-guide.md`

Plausible future continuations if more external source pressure justifies them:
- a thinner native Windows worker/UI bridge continuation once a GUI consumer is proved and the remaining question is worker dispatch ownership
- a macOS/Cocoa-native practical continuation if native-desktop balance still needs a thinner but practical branch next
- a more concrete Qt receiver-thread / event-loop handoff continuation only if it can stay operator-focused and case-driven

## Next-step research directions
Good next candidates after this run:
- another underfed native-desktop seam that is still practical rather than tutorial-shaped
- protocol / firmware or desktop service/daemon continuations if they remain thinner than browser/mobile
- avoid another tiny native GUI wording-only pass unless a contradiction or new source-backed practical gap appears

## Concrete scenario notes or actionable tactics added this run
Added or sharpened this run:
- in Win32 subclass cases, treat `CallWindowProc` as subclass-chain evidence rather than automatic proof that the current wrapper is the decisive consumer
- preserve the exact per-window original-proc chain before generalizing from sibling controls or shared wrappers
- in Qt `AutoConnection` cases, classify whether the truthful boundary is slot-immediate or receiver-loop-delivered
- in truly queued Qt cases, preserve receiver-side delivery as its own boundary when the meaningful reducer lives after event-loop return

## KB changes made
### New source note
Added:
- `sources/native-and-desktop/2026-03-24-native-gui-delivery-boundary-notes.md`

### Canonical workflow note materially refined
Updated:
- `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md`

Material improvements:
- strengthened the Qt delivery section to preserve `AutoConnection` as a real branch in proof choice rather than a background detail
- added the stricter rule that direct/same-thread vs queued/cross-thread delivery changes where the truthful consumer boundary lives
- strengthened runtime-proof guidance so `CallWindowProc` is treated as subclass-chain evidence, not automatic consumer proof
- sharpened the Qt multi-receiver pattern so receiver-side event-loop delivery is preserved separately when queued delivery is real
- upgraded the operator checklist with explicit per-window subclass-chain and `AutoConnection` stop rules

### Native subtree memory updated
Updated:
- `topics/native-practical-subtree-guide.md`

Change:
- preserved the same stop rule at the branch-routing level so the native subtree remembers not to flatten shared subclass wrappers or Qt `AutoConnection` / queued delivery into generic framework proof

## Files changed
Added:
- `sources/native-and-desktop/2026-03-24-native-gui-consumer-search-layer.txt`
- `sources/native-and-desktop/2026-03-24-native-gui-delivery-boundary-notes.md`
- `runs/2026-03-24-0616-reverse-kb-autosync.md`

Updated:
- `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md`
- `topics/native-practical-subtree-guide.md`

## Best-effort errors logging note
No `.learnings/ERRORS.md` entry was required for the main workflow.
Observed degradation was recorded in this report instead:
- initial search-artifact write failed because the target source directory did not yet exist
- Grok returned JSON-parse failures in the explicit multi-source search attempt

## Commit / sync status
Plan for this run:
1. commit only the intended reverse-KB files changed by this workflow
2. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
3. keep this run report as the archival record

## Bottom line
This was a real external-research-driven native-desktop maintenance run on a thinner but practical seam.

The KB now preserves a sharper stop rule:
- do not treat subclass visibility or `CallWindowProc` as consumer proof until per-window ownership is preserved
- do not treat visible `emit` or recovered Qt connection graphs as final proof until direct/immediate vs queued/receiver-loop-delivered ownership is classified
- then pick the first delivery-shape-appropriate consumer that actually predicts later behavior
