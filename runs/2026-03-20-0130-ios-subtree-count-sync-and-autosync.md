# Reverse KB Autosync Run Report — 2026-03-20 01:30 Asia/Shanghai

## Summary
This autosync run focused on a **small iOS practical-branch count synchronization repair**.

Recent runs had already strengthened the iOS branch’s late-ladder handoff into result-to-policy work.
That branch work made the subtree guide more structurally coherent overall, but one small inconsistency remained inside the guide itself:
- the core claim correctly defined **seven recurring families**
- the compact ladder section later described the branch as **six common bottleneck families**
- the section itself still listed seven stages (`A` through `G`)

So the branch shape was already right, but one of its canonical reader-entry surfaces still preserved the wrong count.
This run repaired that mismatch so the iOS subtree guide now says the same thing at the top and in the middle.

## Run type
Scheduled autosync / branch-balance / maintenance pass.

## Scope this run
Primary goals:
- maintain and improve the KB itself, not just collect notes
- keep work practical and case-driven
- include direction review and branch-balance awareness
- produce a run report
- commit KB changes if any
- run archival sync after commit

Concretely, this run:
- reviewed recent autosync reports to avoid reopening already-repaired seams
- re-read the iOS subtree guide and nearby branch surfaces
- identified an internal count mismatch inside `topics/ios-practical-subtree-guide.md`
- repaired the compact-ladder sentence from **six** to **seven** common bottleneck families
- validated that the branch now reads consistently with its own `A`–`G` structure and nearby iOS routing surfaces
- avoided unnecessary external research because this was an internal KB synchronization issue, not a source-coverage gap

## Direction review
The overall KB direction still looks healthy:
- preserve practical, bottleneck-oriented routing
- prefer canonical branch repairs over unnecessary new leaf creation
- keep browser/mobile-protected strong branches from monopolizing every run by default
- but still fix high-leverage internal drift when a strong branch’s main guide becomes self-inconsistent

This run fit that direction because it improved the KB itself rather than adding note sprawl.
The work was small, but it repaired a real canonical inconsistency in a page that readers actually use for routing.

## Branch-balance review
### Current branch picture
Broadly:
- browser and mobile/protected-runtime remain among the densest practical branches
- recent runs already touched iOS, protected-runtime, provenance, malware, native, and runtime-evidence continuity
- iOS is healthier than before, but because it has gained structure quickly, it is also more exposed to small internal drift across guide sections

### Why this run was branch-balance aware
This run did **not** deepen the already-dense iOS branch with another leaf.
It also did **not** detour into browser/mobile source collection just because those branches are rich.

Instead, it chose the smaller and more disciplined repair:
- keep the existing iOS branch truthful on its own main subtree guide
- fix the branch count where the page contradicted itself
- avoid turning a mature branch into a source of navigation noise

That is branch-balance aware in the maintenance sense:
- not only where to add content
- but where to keep mature branch surfaces internally stable so they do not crowd out thinner branches later with avoidable cleanup debt

## Why this target was chosen
The strongest maintenance signal was a direct contradiction inside the same guide page.

In `topics/ios-practical-subtree-guide.md`:
- section 2 correctly says the analyst classifies the current bottleneck into **seven recurring families**
- section 4 incorrectly said the branch could be read as **six common bottleneck families**
- the same section then immediately enumerated seven ladder stages:
  - A. incomplete network picture
  - B. incomparable setup
  - C. reachable but unstable setup
  - D. reachable flow / first owner
  - E. cross-runtime confusion / first Dart-object owner
  - F. plausible owner / truthful callable path
  - G. visible callback/result / first policy-bearing consumer

That means the branch logic itself was already correct, but the guide’s compact summary had stale count wording.
A reader scanning the page quickly could absorb the wrong branch size even though the detailed content was right.

This was therefore a **canonical guide self-consistency problem**, not a source problem and not a missing-topic problem.

## Sources consulted
Canonical KB pages consulted:
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/topics/ios-practical-subtree-guide.md`
- `research/reverse-expert-kb/topics/ios-result-callback-to-policy-state-workflow-note.md`
- `research/reverse-expert-kb/topics/mobile-reversing-and-runtime-instrumentation.md`
- `research/reverse-expert-kb/topics/protocol-firmware-practical-subtree-guide.md`

Recent run reports consulted:
- `research/reverse-expert-kb/runs/2026-03-20-0030-malware-comms-stage-subtree-sync-and-autosync.md`
- `research/reverse-expert-kb/runs/2026-03-19-2330-protected-runtime-branch-count-and-handoff-sync-and-autosync.md`
- `research/reverse-expert-kb/runs/2026-03-19-2233-ios-replay-to-policy-handoff-sync-and-autosync.md`
- `research/reverse-expert-kb/runs/2026-03-19-2130-provenance-continuation-surface-branch-balance-and-autosync.md`

## New findings
### 1. Mature subtree guides can still drift internally after successful ladder-building
The iOS branch already had the right shape.
The remaining problem was not the ladder itself, but a stale count sentence left behind after the ladder expanded.

### 2. Count mismatches are small, but they still matter on canonical entry surfaces
A subtree guide is not just a dump of links.
It teaches readers how many distinct operator bottlenecks they should expect.
If the count is wrong, the guide becomes harder to trust even when the leaf routing is otherwise solid.

### 3. Fast-growing practical branches need occasional count-and-ladder sync passes
The more a branch gets improved through several short maintenance runs, the more likely one section header or summary sentence keeps an older shape.
This kind of autosync pass is therefore worthwhile even when no new content is needed.

## Newly improved KB content
### 1. Fixed the iOS subtree guide’s compact-ladder count
Updated:
- `research/reverse-expert-kb/topics/ios-practical-subtree-guide.md`

Change made:
- corrected the compact-ladder sentence from **six common bottleneck families** to **seven common bottleneck families**

Why it matters:
- the guide’s count now matches its own core claim
- the guide’s count now matches its own `A`–`G` ladder
- the branch now reads more truthfully as a seven-stage routing surface rather than a six-stage one with an unexplained extra child

## Reflections / synthesis
This was the right kind of low-sprawl autosync run.

It did not try to inflate the KB.
It repaired one small contradiction in a canonical branch surface.
That is still real KB maintenance because subtree guides are how the KB teaches operators where to go next.

A durable lesson from this run is:
- once a branch becomes ladder-shaped,
- count consistency matters,
- and the most useful maintenance pass may be a one-line repair if that line sits on a page readers actually use for routing.

## Candidate topic pages to create or improve
Improved this run:
- `research/reverse-expert-kb/topics/ios-practical-subtree-guide.md`

Future possibilities only if repeated pressure appears:
- a broader count-audit across other subtree guides after rapid same-day maintenance bursts
- otherwise, prefer shifting back toward thinner branches rather than reopening iOS immediately

## Next-step research directions
Best next directions after this run:
1. Keep checking subtree-guide count claims against their actual ladder enumerations after rapid maintenance.
2. Prefer small truthfulness repairs when a mature branch already has enough content.
3. Continue steering future substantive growth toward thinner branches unless another canonical-surface mismatch appears.
4. Treat self-consistency of subtree guides as practical operator value, not mere editorial polish.

## Concrete scenario notes or actionable tactics added this run
This run preserved the following practical guidance more canonically:
- the iOS practical subtree should be remembered as **seven** recurring bottleneck families
- the visible callback/result -> policy-bearing consumer stage remains a real seventh stage, not an accidental add-on
- branch guides should keep their count claims synchronized with their actual ladder enumerations
- small count repairs on canonical branch surfaces are worthwhile when they prevent operator-routing ambiguity

## Search audit
This run did **not** perform web research.

- Search sources requested: `exa,tavily,grok`
- Search sources succeeded: none
- Search sources failed: none
- Exa endpoint: `http://158.178.236.241:7860`
- Tavily endpoint: `http://proxy.zhangxuemin.work:9874/api`
- Grok endpoint: `http://proxy.zhangxuemin.work:8000/v1`
- Degraded mode note: not applicable because no external search was needed; Grok-only would be treated as degraded mode rather than normal mode if search had been required

## Validation
Validation performed:
- targeted `git diff` review of the changed guide
- `git diff --check` on the changed guide
- read-back comparison against the guide’s section-2 count claim and its section-4 `A`–`G` ladder structure

Result:
- the compact-ladder sentence now uses the correct count
- the iOS subtree guide is internally consistent on branch size again
- the change stayed a focused canonical repair rather than unnecessary branch sprawl

## Files changed this run
- `research/reverse-expert-kb/topics/ios-practical-subtree-guide.md`
- `research/reverse-expert-kb/runs/2026-03-20-0130-ios-subtree-count-sync-and-autosync.md`

## Outcome
KB changed materially.

This run improved the iOS practical branch itself rather than only collecting notes, and made one of its main routing surfaces more internally trustworthy.

## Commit / sync plan
If no additional validation issue appears:
1. stage only the reverse-KB files changed by this run
2. commit the iOS subtree count sync
3. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

## Bottom line
This autosync run improved the **internal count fidelity of the iOS practical subtree guide**.

It did not add a new leaf.
It repaired a small but real contradiction so the guide now says more consistently:
- the iOS practical branch has seven recurring bottleneck families
- its `A`–`G` compact ladder is intentional
- canonical routing surfaces should preserve the branch shape exactly once that ladder has matured
