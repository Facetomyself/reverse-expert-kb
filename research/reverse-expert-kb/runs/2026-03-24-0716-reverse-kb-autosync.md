# Reverse KB Autosync Run Report

Date: 2026-03-24 07:16 Asia/Shanghai
Mode: external-research-driven
Scope: `research/reverse-expert-kb/`
Primary branch worked: native desktop practical subtree
Chosen seam: macOS event-delivery boundary — `NSApplication sendEvent:` / responder-chain / target-action / XPC proxy-to-exported-object / dispatch-source callback vs first real consumer

## Summary
This run intentionally avoided another internal-only canonical-sync pass.
Recent autosync history had already spent real attention on iOS continuation quality and on Win32/Qt GUI ownership.
That made native desktop still the right branch-balance target, but not for another tiny wording-only Win32/Qt repair.

The underfed practical seam was macOS desktop/event delivery:
- analysts can still stop too early once they find `NSApplication`, `sendEvent:`, responder-chain activity, XPC proxy setup, or dispatch-source registration
- that can collapse framework reduction and behavior ownership into one generic “Cocoa/XPC found” bucket

This run therefore did a real explicit multi-source search pass and tightened one operator stop rule:
- **Cocoa:** `NSApplication` / `sendEvent:` is often only framework reduction unless it actually suppresses, rewrites, retargets, or policy-gates later behavior
- **Responder / target-action:** visible selector names are not enough until one receiver actually performs the first durable write, mode change, task enqueue, or policy choice
- **XPC:** connection/proxy setup is not the truthful consumer until the service-side exported-object method or the first stateful reducer behind it is preserved
- **Dispatch sources:** registration and callback delivery are not automatically the decisive consumer until the first parser/classifier/state reducer after callback entry is identified

That improved the KB itself rather than just saving notes:
- the native GUI / event-delivery workflow note now preserves this macOS stop rule explicitly
- the native subtree guide now remembers the same rule at branch-routing level
- the native baseline page now remembers that the GUI/event-delivery continuation also covers macOS Cocoa/XPC/dispatch ownership
- the run archive records the search audit and the practical synthesis

## Direction review
This run stayed aligned with the reverse KB direction:
- improve the KB itself, not merely collect links
- keep work practical and case-driven
- strengthen an underfed branch rather than over-polishing dense branches
- preserve workflow truth that changes where a real analyst stops, hooks, and hands off

Why this seam was worth doing now:
- native desktop remains thinner than browser/mobile/protected-runtime branches
- Win32 and Qt had already gotten a recent stop-rule refinement, while macOS desktop had less practical memory in the branch
- the chosen seam is narrow and operator-relevant: it affects where analysts stop when global event hooks or IPC scaffolding are visible but consumer ownership is not yet honest
- it avoided drifting into another large taxonomy page or another branch-internal wording-only pass

## Branch-balance review
Current balance view after this run:
- **Easy to overfeed:** browser anti-bot, protected-runtime, already-dense mobile continuation seams
- **Recently fed enough:** iOS continuation quality, Win32/Qt GUI ownership boundary, runtime-evidence practical work
- **Still worth practical strengthening:** native desktop, especially macOS event delivery where framework visibility can still be mistaken for consumer proof

Why this branch was the right target:
- it is underfed relative to browser/mobile density
- it adds practical operator value across ordinary desktop reversing
- the work sharpened an existing canonical native continuation instead of fragmenting the KB with a detached macOS-only overview

Anti-stagnation check:
- this was a real external-research-driven run
- explicit `exa,tavily,grok` search was attempted
- the output materially sharpened canonical KB workflow guidance
- the run did not collapse into index-only / family-count-only / wording-only maintenance

## External research performed
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries used:
1. `macOS NSXPC XPC Mach service reverse engineering first consumer practical`
2. `Cocoa NSApplication sendEvent target action reverse engineering first meaningful consumer`
3. `macOS dispatch source runloop callback reverse engineering queued delivery practical`

Saved raw search artifact:
- `sources/native-and-desktop/2026-03-24-macos-event-delivery-search-layer.txt`

Follow-up fetch / validation used:
- Apple Cocoa Fundamentals / Core Application Architecture
- Apple Creating XPC Services
- Apple dispatch-source documentation
- CocoaDev note on overriding `NSApplication sendEvent:`

## Search audit
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- exa
- tavily
- grok

Failed sources:
- none as a fully missing source set

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Degraded-source note:
- this run explicitly attempted all three requested sources
- retained usable results were present from Exa, Tavily, and Grok
- Grok emitted JSON-parse errors during execution, so Grok should be treated as degraded-but-usable rather than cleanly healthy
- because Grok still returned retained results, this was not a Grok-absent run, but the degradation is recorded here explicitly

## New findings
High-signal source-backed reminders retained this run:
- `NSApplication` and the main event loop are framework structure, not by themselves consumer proof
- `sendEvent:` is often the earliest app-side event boundary, but not automatically the truthful consumer if it mainly forwards ordinary processing
- responder-chain / target-action routing should not be flattened into generic “GUI event handled” proof; the truthful consumer is often the first receiver that writes state, chooses policy, or enqueues real work
- `NSXPCConnection` / proxy setup reduces ownership uncertainty but often remains RPC scaffolding rather than the first behavior-bearing service-side consumer
- dispatch-source registration and callback delivery are not automatically the decisive boundary if the first parser/classifier/state reducer after callback entry is what really predicts later behavior

## Sources consulted
Primary sources used conservatively:
- Apple Cocoa Fundamentals / Core Application Architecture
- Apple Creating XPC Services
- Apple dispatch-source documentation
- CocoaDev note on overriding `NSApplication sendEvent:`

Supporting search-layer context retained conservatively:
- Mandiant Cocoa reversing intro
- SIMBL Cocoa reversing guide
- practical XPC reversing / interception notes from security blogs

## Reflections / synthesis
The practical gain here is not a broad macOS tutorial.
It is a small but important stop rule inside the native desktop branch.

The branch already preserved “do not stop at framework landmarks” for Win32 and Qt.
What it still risked under-preserving was the same mistake in macOS form:
- `NSApplication` or `sendEvent:` can look like the right answer simply because they are global and early
- `NSXPCConnection` and proxy setup can look like the right answer simply because they reveal the cross-process shape
- dispatch-source callbacks can look like the right answer simply because they are the first queued callback you can see

The better rule is:
- if `sendEvent:` only forwards, treat it as framework reduction and keep going
- if responder / target-action routing is still open, preserve the first receiver that actually changes behavior
- if XPC is involved, distinguish connection/proxy setup from the service-side exported-object method or first reducer that matters
- if dispatch sources are involved, distinguish callback delivery from the first parser/classifier/reducer that turns delivery into app-local meaning

That changes where analysts place hooks and where they declare the first honest consumer boundary in real macOS cases.

## Candidate topic pages to create or improve
Improved this run:
- `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md`
- `topics/native-practical-subtree-guide.md`
- `topics/native-binary-reversing-baseline.md`

Plausible future continuations if more source pressure justifies them:
- a thinner macOS XPC exported-object-to-policy continuation if a real case-backed operator gap appears
- a native desktop service/daemon continuation for launchd/helper-owned worker paths if native balance still needs another practical seam
- a more explicit responder-chain / target-action continuation only if it can stay workflow-centered rather than framework-tutorial shaped

## Concrete scenario notes or actionable tactics added this run
Added or sharpened this run:
- treat `NSApplication sendEvent:` as framework reduction unless it actually suppresses, rewrites, retargets, or policy-gates behavior
- in responder-chain / target-action cases, preserve the first receiver that writes durable state, changes mode, chooses policy, or enqueues work
- in XPC cases, preserve the boundary between proxy setup and the service-side exported-object method that first matters
- in dispatch-source cases, preserve the boundary between registration/callback delivery and the first parser/classifier/state reducer after callback entry

## KB changes made
### New source notes
Added:
- `sources/native-and-desktop/2026-03-24-macos-event-delivery-search-layer.txt`
- `sources/native-and-desktop/2026-03-24-macos-event-delivery-boundary-notes.md`

### Canonical workflow note materially refined
Updated:
- `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md`

Material improvements:
- extended the note from Win32/Qt-only framing into a practical native desktop GUI/event-delivery continuation that also preserves macOS Cocoa/XPC/dispatch ownership
- added explicit Cocoa guidance so `sendEvent:` is treated as framework reduction unless it actually changes ownership or policy
- added explicit XPC and dispatch-source stop rules so proxy setup and registration visibility are not mistaken for first-consumer proof
- added concrete pattern guidance for responder-chain / target-action and XPC / dispatch-source cases
- upgraded the operator checklist with macOS-specific consumer-boundary rules

### Native subtree memory updated
Updated:
- `topics/native-practical-subtree-guide.md`

Change:
- preserved the same stop rule at branch-routing level so the native subtree remembers not to flatten Cocoa `sendEvent:`, XPC proxy setup, or dispatch-source registration into automatic consumer proof

### Native baseline page updated
Updated:
- `topics/native-binary-reversing-baseline.md`

Change:
- preserved that the native desktop GUI/event-delivery continuation now also covers macOS Cocoa/XPC/dispatch ownership, not only Win32/Qt narrowing

## Files changed
Added:
- `sources/native-and-desktop/2026-03-24-macos-event-delivery-search-layer.txt`
- `sources/native-and-desktop/2026-03-24-macos-event-delivery-boundary-notes.md`
- `runs/2026-03-24-0716-reverse-kb-autosync.md`

Updated:
- `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md`
- `topics/native-practical-subtree-guide.md`
- `topics/native-binary-reversing-baseline.md`

## Best-effort errors logging note
No `.learnings/ERRORS.md` write was required for the main workflow.
Observed search degradation was recorded in this report instead:
- Grok emitted JSON-parse errors during the explicit multi-source search attempt, while still returning retained results

## Commit / sync status
Plan for this run:
1. commit only the intended reverse-KB files changed by this workflow
2. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
3. keep this run report as the archival record

## Bottom line
This was a real external-research-driven native-desktop maintenance run on an underfed macOS practical seam.

The KB now preserves a sharper stop rule:
- do not treat `NSApplication`, `sendEvent:`, responder-chain visibility, XPC proxy setup, or dispatch-source registration as consumer proof by default
- classify whether they are only framework reduction or the first actual behavior-changing consumer
- then preserve the earliest consumer that truly predicts later behavior
