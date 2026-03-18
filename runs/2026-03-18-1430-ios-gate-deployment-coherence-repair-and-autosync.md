# Reverse KB Autosync Run Report — 2026-03-18 14:30 Asia/Shanghai

## Summary
This autosync run focused on an **iOS gate/deployment-coherence repair** rather than new topic proliferation.

The practical gap was not that the iOS branch lacked pages.
It was that several durable lessons from the recent iOS source batches were still only partially preserved in canonical branch pages:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md` already modeled packaging, install-path, and instrumentation gates well, but it under-preserved some operator-important distinctions from the newer iOS source notes
- the branch still risked collapsing too much early iOS drift into a vague “jailbreak detection” story
- recent source notes had made three practical reminders clearer:
  - rootful vs rootless is an operational branch, not a cosmetic label
  - Frida deployment coherence can explain apparent instability before stronger anti-instrumentation claims are justified
  - Flutter-oriented repack/rewrite failure should often be treated as a setup/gate issue first, with live-runtime owner recovery as the practical fallback

So this run tightened the **iOS practical branch itself** by pushing those reminders into the canonical pages that analysts will actually read.

## Direction review
This run stayed aligned with the current reverse-KB direction:
- maintain and improve the KB itself, not just collect notes
- keep work practical and case-driven
- prefer branch-shape and workflow-truthfulness repair when the branch already has the right pages but still leaks important reasoning into source notes or run reports
- continue avoiding easy low-value growth in already-dense browser/mobile micro-variant areas unless a real reusable operator gap appears

This was a good fit for autosync because the needed work was not “add another iOS note.”
It was “make the current iOS note stack tell the truth more precisely.”

## Branch-balance review
Current branch density remains uneven:
- browser remains heavy
- mobile remains one of the densest families
- malware and some non-mobile branches remain thinner

That made it important **not** to respond to fresh iOS source pressure by creating another narrow iOS leaf automatically.

This run stayed branch-balance aware by doing maintenance that improves retrieval quality without materially increasing branch sprawl:
- no new browser note
- no new mobile micro-leaf
- no speculative new iOS child page
- instead: sharpen the already-existing iOS gate/setup and cross-runtime routing pages so they preserve more durable practical distinctions

In other words, this run spent mobile budget on **canonical repair**, not density growth.

## Why this target was chosen
The recent iOS source notes had already contributed strong practical lessons, especially from:
- `sources/ios-runtime-and-sign-recovery/2026-03-17-sperm-ios-batch-1-notes.md`
- `sources/ios-runtime-and-sign-recovery/2026-03-17-sperm-ios-batch-2-notes.md`

But some of their best durable guidance still needed better canonical preservation:
- rootful vs rootless should influence how the analyst compares runs and judges trustworthiness of later evidence
- Frida startup/transport/version mismatches can create fake “target instability” if runs are not operationally comparable
- rewrite/repack failure in Flutter-shaped iOS work should not be mistaken for proof that progress depends on repack success

These are exactly the kinds of details that belong in the branch’s practical routing pages, because they change how an analyst sequences work.

## Sources consulted
Canonical pages consulted:
- `research/reverse-expert-kb/topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `research/reverse-expert-kb/topics/ios-practical-subtree-guide.md`
- `research/reverse-expert-kb/topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md`
- `research/reverse-expert-kb/topics/mobile-reversing-and-runtime-instrumentation.md`
- `research/reverse-expert-kb/topics/mobile-protected-runtime-subtree-guide.md`

Recent source notes consulted:
- `research/reverse-expert-kb/sources/ios-runtime-and-sign-recovery/2026-03-17-sperm-ios-batch-1-notes.md`
- `research/reverse-expert-kb/sources/ios-runtime-and-sign-recovery/2026-03-17-sperm-ios-batch-2-notes.md`

Recent run reports reviewed for branch context:
- `research/reverse-expert-kb/runs/2026-03-18-1030-ios-subtree-guide-branch-balance-and-autosync.md`
- `research/reverse-expert-kb/runs/2026-03-18-1130-protected-runtime-branch-shape-repair-and-autosync.md`
- `research/reverse-expert-kb/runs/2026-03-18-1233-protocol-branch-shape-count-repair-and-autosync.md`
- `research/reverse-expert-kb/runs/2026-03-18-1330-malware-branch-self-description-repair-and-autosync.md`

## What changed
### 1. Strengthened the iOS gate note’s deployment-coherence model
Updated:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`

Changes made:
- expanded the packaging/install-path gate to preserve that rootful vs rootless differences can affect persistence, service paths, and tool layout in ways that make later evidence non-comparable
- expanded the instrumentation-visibility gate to preserve that Frida deployment incoherence can explain instability before deeper anti-instrumentation claims are justified
- strengthened compare-pair guidance so analysts explicitly record install/signing path, rootful-vs-rootless mode, Frida launch mode, and USB/network transport path
- added a new Flutter/repack failure scenario that routes analysts toward live-runtime owner recovery instead of treating repack success as mandatory

### 2. Tightened the iOS subtree guide’s setup-stage wording
Updated:
- `topics/ios-practical-subtree-guide.md`

Changes made:
- preserved the reminder that early iOS setup should not be flattened into one vague “jailbroken vs not” split
- made installation/signing path, rootful-vs-rootless mode, Frida deployment coherence, and repack/rewrite stability explicit parts of family-2 gate reasoning
- clarified when the gate page is the right entry note before ownership work

### 3. Strengthened the iOS Flutter cross-runtime note’s fallback rule
Updated:
- `topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md`

Changes made:
- made the live-runtime fallback rule more explicit: when reFlutter/repack work stops yielding a stable runnable artifact, rewrite success should no longer be treated as a precondition for progress
- reinforced that owner localization in the runtime that actually executes is the stronger practical move in those cases

### 4. Synced broader mobile branch navigation with the repaired lesson
Updated:
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/mobile-protected-runtime-subtree-guide.md`

Changes made:
- preserved the three recurring iOS reminders at the mobile parent level:
  - install/signing path is part of the runtime gate surface
  - rootful vs rootless is an operational distinction
  - Frida deployment coherence can explain apparent instability
- updated subtree guidance so the iOS gate note is more clearly framed as the place to separate those issues before deeper hooks, bypasses, or request work

## New findings / durable synthesis
### 1. “Jailbroken vs not” is too coarse for the current iOS branch
The branch is now mature enough that a generic early split like “jailbroken vs stock” loses practical value.
At minimum, the analyst often needs to preserve:
- install/signing path
- rootful vs rootless mode
- deployment topology
- Frida coherence
- rewrite/repack stability

That is a more truthful practical gate surface.

### 2. Deployment incoherence can masquerade as protection pressure
A durable lesson from the recent source notes is that some apparent anti-instrumentation instability is not yet proof of target resistance.
It may still be:
- mismatched Frida versions
- different startup modes
- different service paths
- different USB/network transport assumptions

That matters because it changes what the analyst should compare first.

### 3. Flutter rewrite failure is often a routing signal, not a dead end
When Flutter-oriented repack/rewrite work keeps failing while the live app still executes the target flow, that is often a signal to switch routing:
- stop optimizing for static rewrite success
- localize the owner in the runtime that already runs truthfully
- only return to rewrite work later if it becomes clearly worth the cost

That rule was already visible in the source notes; this run promoted it more clearly into canonical workflow guidance.

## Reflections / synthesis
This was the right kind of autosync maintenance run.
It improved the KB itself by preserving operator-important distinctions that were at risk of staying trapped in source notes.

The key improvement is not flashy, but it is durable:
- before this run, the iOS branch already had good pages
- after this run, those pages preserve a more truthful model of early setup drift, deployment coherence, and cross-runtime fallback behavior

That should reduce a specific failure mode in future work:
- over-claiming jailbreak detection or anti-instrumentation too early
- comparing operationally different runs as if they were equivalent
- overinvesting in repack/rewrite paths after the live runtime has already become the truer source of evidence

## Candidate topic pages to create or improve
Improved this run:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `topics/ios-practical-subtree-guide.md`
- `topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/mobile-protected-runtime-subtree-guide.md`

Future possibilities only if repeated case pressure accumulates:
- a narrower iOS deployment-coherence checklist note if enough future cases keep needing the same compare-run normalization surface
- a dedicated iOS live-runtime fallback note only if Flutter/repack and non-Flutter owner-replay cases start converging on one reusable operator ladder distinct from the current gate/owner/replay pages
- otherwise, prefer continuing to strengthen the current iOS ladder rather than growing more narrow sibling leaves

## Next-step research directions
Best next directions after this run:
1. Continue preferring branch-truthfulness repairs over adding another iOS micro-leaf by default.
2. Keep preserving fresh source-driven practical distinctions in canonical pages as soon as they become stable.
3. If future iOS sources keep reinforcing deployment-coherence issues, consider a compact compare-run normalization checklist embedded in the relevant page rather than as a separate note unless a real standalone operator gap appears.
4. Continue branch-balance discipline: mobile work is still justified when it repairs routing and evidence trust, not when it merely adds more dense surface area.

## Search audit
This run did **not** perform web research.

Requested sources:
- none

Succeeded sources:
- none

Failed sources:
- none

Configured endpoints relevant to search-bearing runs:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Degraded mode note:
- not applicable in this run because no external search was executed
- if search had been needed, the explicit request would have been `--source exa,tavily,grok`
- Grok-only execution would be treated as degraded mode rather than normal mode

## Validation
Validation performed:
- read-back inspection of all changed iOS/mobile branch pages
- targeted grep checks for the newly preserved concepts:
  - rootful / rootless
  - TrollStore / Apple ID install-path distinctions
  - Frida deployment coherence and USB/network transport
  - reFlutter/repack live-runtime fallback wording
- `git diff` review of changed reverse-KB pages

Result:
- the iOS gate note, iOS subtree guide, iOS Flutter owner note, and two broader mobile navigation pages now describe the same practical distinctions more consistently
- the changes remain branch-repair oriented rather than branch-sprawl oriented

## Commit / sync plan
If no additional validation issue appears:
1. stage only the reverse-KB files changed by this run
2. commit the iOS gate/deployment-coherence repair
3. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

## Bottom line
This autosync run improved the **iOS practical branch itself** by repairing how it models early setup and deployment truth.

It preserved three durable operator reminders more canonically:
- install/signing path and rootful-vs-rootless mode belong inside the gate surface
- Frida deployment coherence can explain instability before stronger anti-instrumentation claims are warranted
- Flutter-oriented repack failure should often route the analyst toward live-runtime owner recovery rather than block progress

That keeps the reverse KB more practical, more internally truthful, and less likely to overstate early iOS diagnoses.