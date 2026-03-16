# Run Report — 2026-03-17 07:30 Asia/Shanghai — Native callback-consumer branch-balance pass

## Summary
This autosync run focused on **maintaining and improving the KB itself** by strengthening a still-underdeveloped but high-value native practical branch inside `research/reverse-expert-kb/`.

Recent branch-balance work had already improved:
- native semantic-anchor stabilization
- native interface-to-state proof
- protocol replay/state-gate and reply-emission branches
- malware handoff/evidence packaging
- packed-stub/OEP deobfuscation workflow coverage
- iOS owner-localization and result-to-policy localization

That left one recurring native gap:
- the KB had good guidance for readable static structure and representative interface proof
- but it still lacked a canonical note for the common async/event-driven native case where callback registration, message pumps, completion paths, or reactor-loop plumbing are already visible and yet the first consequence-bearing callback consumer is still unproved

This run filled that gap with a concrete workflow note centered on **registration -> dispatch -> first consequence-bearing event-loop consumer**, plus the supporting source note and navigation updates needed to make the native branch more usable.

## Scope this run
- perform a direction review against recent runs and current branch balance
- avoid deepening already-strong browser/mobile/WebView micro-branches
- strengthen a thinner native practical branch with a case-driven workflow note instead of a broad async-native taxonomy page
- update native/navigation pages only where needed for clean routing
- produce a run report, commit if changed, and sync the reverse-KB subtree afterward

## Branch-balance review
### Strong branches right now
The KB remains especially strong in:
- browser anti-bot / request-finalization / first-consumer workflows
- mobile protected-runtime / WebView / challenge-loop workflows
- protocol / firmware practical workflows
- protected-runtime / deobfuscation practical workflows

It is also now materially stronger than before in:
- native baseline practical workflows
- malware practical handoff workflows
- iOS practical localization workflows

### Weaker or still-thinner areas before this run
Relative to those stronger branches, the native branch still had a gap around async/event-driven ownership.
It already had:
- `native-semantic-anchor-stabilization-workflow-note`
- `native-interface-to-state-proof-workflow-note`

But it still lacked the frequent real-world middle-late state where:
- static structure is readable
- callbacks/registrations/message loops/completions are visible
- the direct call graph no longer explains real execution order
- and the analyst still cannot tell which consumer actually changes behavior first

### Why this was a good branch-balance target
This run fit the autosync direction rules because it:
- improved the KB itself rather than just collecting notes
- stayed practical and workflow-centered
- repaired a real routing gap in a thinner branch
- resisted the easier but less balanced option of adding yet another browser/mobile micro-variant

## Direction review
This run stayed aligned with the current reverse-KB direction rules:
- keep growth practical and case-driven
- improve canonical topic pages and navigation, not just scratch notes
- prefer operator bottlenecks over abstract taxonomy growth
- keep branch balance visible rather than deepening whatever branch already has the most source energy

The chosen topic is intentionally not a broad “asynchronous native programming” survey.
It is a concrete workflow bridge for a recurring operator bottleneck:
- callback or dispatch structure is visible
- registration is easy to overread as ownership
- but the first queue/dispatch/consumer edge that actually changes later behavior is still unproved

## New findings
### A practical native async gap was real
The native branch now clearly had three adjacent but distinct practical states:
1. readable code but unstable meaning
2. several plausible interface paths but no proved one
3. visible callback/event-loop structure, but no proved consequence-bearing consumer

The KB had pages for the first two states but not the third.

### Existing browser/mobile lessons transferred well without collapsing branches together
Several existing strong pages already reinforced a useful operator lesson:
- visible payload is not meaningful consumption
- visible registration is not consequence ownership
- the decisive boundary is often later than the most obvious callback surface

Those lessons already existed in mobile and browser form, but the native branch still benefited from its own canonical note framed around:
- callback registration
- message pumps
- queued work and completions
- reactor/event-loop dispatch
- first behavior-changing consumer

### The native branch now has a more realistic progression
The native practical branch now reads more coherently as:
1. baseline static/native orientation
2. semantic-anchor stabilization
3. representative interface-path proof
4. callback-registration to event-loop consumer proof when direct caller/callee reasoning breaks at async boundaries

That makes the native subtree much more usable for desktop/server binaries that are structurally readable but operationally event-driven.

## Sources consulted
Canonical KB pages and guides reviewed this run included:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/topics/native-binary-reversing-baseline.md`
- `research/reverse-expert-kb/topics/native-semantic-anchor-stabilization-workflow-note.md`
- `research/reverse-expert-kb/topics/native-interface-to-state-proof-workflow-note.md`
- `research/reverse-expert-kb/topics/runtime-behavior-recovery.md`

Recent run reports reviewed included:
- `research/reverse-expert-kb/runs/2026-03-17-0630-ios-result-callback-policy-branch-balance-pass.md`
- `research/reverse-expert-kb/runs/2026-03-17-0532-protocol-reply-emission-branch-balance-pass.md`
- `research/reverse-expert-kb/runs/2026-03-17-0330-packed-stub-oep-branch-balance-pass.md`

Existing native source notes reused this run:
- `research/reverse-expert-kb/sources/native-binary/2026-03-17-semantic-anchor-stabilization-notes.md`
- `research/reverse-expert-kb/sources/native-binary/2026-03-16-native-interface-state-proof-workflow-notes.md`

New source note added this run:
- `research/reverse-expert-kb/sources/native-binary/2026-03-17-native-callback-registration-and-event-loop-consumer-notes.md`

## Reflections / synthesis
The strongest practical pattern reused across the KB remains:

```text
some relevant structure is already visible
  -> choose one bounded ownership question
  -> separate visible surfaces from real consumption
  -> prove one consequence-bearing edge
  -> return to a smaller and more trustworthy map
```

This run gave the native branch its own explicit async/event-driven version of that pattern.
That is valuable because a lot of desktop/server reversing does not stall on unreadable code.
It stalls on event-driven indirection:
- posted work
- message pumps
- completions
- callbacks
- notification fan-out
- queue/dequeue boundaries

Without a dedicated workflow note, the analyst can easily spend too long mapping framework plumbing or registration sites that look central but do not actually own behavior.

## Candidate topic pages to create or improve
### Created this run
- `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md`

### Improved this run
- `topics/native-binary-reversing-baseline.md`
- `index.md`

### Candidate future improvements
- a follow-on native note around worker-queue ownership or delayed-task scheduling if repeated cases cluster there strongly enough to justify a narrower split
- a future OS-specific practical note only if Windows message-loop, macOS run-loop, and Linux reactor differences begin to overwhelm the current shared workflow note
- a later refinement pass on the native branch once more desktop/server practical children accumulate

## Concrete scenario notes or actionable tactics added this run
The new workflow note now explicitly preserves these tactics:
- registration visibility is not consequence ownership
- separate event source, registration, dispatch reduction, consequence-bearing consumer, and effect
- prefer the first callback or continuation that changes state, schedules real work, or selects an output family
- do not stop at framework dispatch helpers if a smaller downstream consumer better predicts behavior
- use one narrow proof move: one queue watch, one dispatch breakpoint, one follow-up task hook, one compare run, or one reverse-causality step from a visible late effect
- stop after one grounded async chain instead of cataloging the whole framework first

## Files changed this run
- `research/reverse-expert-kb/sources/native-binary/2026-03-17-native-callback-registration-and-event-loop-consumer-notes.md`
- `research/reverse-expert-kb/topics/native-callback-registration-to-event-loop-consumer-workflow-note.md`
- `research/reverse-expert-kb/topics/native-binary-reversing-baseline.md`
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/runs/2026-03-17-0730-native-callback-consumer-branch-balance-pass.md`

## Next-step research directions
Good future branch-balance candidates now include:
- continuing to rotate among weaker practical branches rather than returning immediately to browser/mobile density
- selective native follow-ons only if they add a clearly distinct operator bottleneck
- deeper firmware/protocol, malware, or deobfuscation follow-ons if fresh routing gaps appear
- periodic top-level navigation review so the index reflects the KB’s real center of gravity and not just file accumulation

## Commit / sync status
Completed after report writing.
This run:
- committed only the reverse-KB files touched by this pass
- left unrelated pre-existing reverse-KB modifications out of the commit
- ran `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh` successfully

### Final status update
- final local commit in `/root/.openclaw/workspace`:
  - `b04448b` — `kb: add native callback consumer workflow note`
- required sync command:
  - `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
- sync result:
  - initial sync succeeded: `Synced research/reverse-expert-kb -> https://github.com/Facetomyself/reverse-expert-kb (branch main)`
  - after amending the commit so this report reflected final status, a second plain sync hit a non-fast-forward rejection because the archive had already received the pre-amend subtree state
  - archival sync was then repaired successfully with a lease-checked forced subtree push against the known remote head
  - final archival state: `https://github.com/Facetomyself/reverse-expert-kb` `main` updated successfully to the final subtree state

## Outcome
This run materially improved the reverse KB by adding a missing native async workflow bridge, tightening the native branch’s internal routing, and keeping branch balance pointed toward practical, case-driven analyst bottlenecks rather than defaulting back into already-dense browser/mobile micro-variants.
