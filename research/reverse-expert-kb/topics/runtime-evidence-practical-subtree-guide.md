# Runtime-Evidence Practical Subtree Guide

Topic class: subtree guide
Ontology layers: runtime-evidence practice branch, observability/replay/causality routing, operator ladder
Maturity: structured-practical
Related pages:
- topics/runtime-behavior-recovery.md
- topics/hook-placement-and-observability-workflow-note.md
- topics/record-replay-and-omniscient-debugging.md
- topics/representative-execution-selection-and-trace-anchor-workflow-note.md
- topics/compare-run-design-and-divergence-isolation-workflow-note.md
- topics/causal-write-and-reverse-causality-localization-workflow-note.md
- topics/runtime-evidence-package-and-handoff-workflow-note.md
- topics/analytic-provenance-and-evidence-management.md
- topics/notebook-and-memory-augmented-re.md
- sources/runtime-evidence/2026-03-21-evidence-package-and-handoff-notes.md

## 1. Why this guide exists
This guide exists because the KB’s runtime-evidence branch already has a strong synthesis page and several useful practical leaves, but it is still easy to read as a short conceptual cluster instead of a usable operator ladder.

The branch already had practical entry surfaces for:
- broad runtime answerability and observability framing
- hook-placement and truth-boundary selection when runtime work is clearly needed but the best observation surface is still unclear
- record/replay and execution-history tradeoffs when live reruns are too fragile or expensive
- reverse-causality localization when one suspicious late effect is already visible and revisitable enough
- runtime-evidence package / handoff continuation once one representative execution, compare-run result, or causal claim is already good enough but still not re-findable enough for reuse
- provenance / evidence-linkage continuation once one representative execution, compare-run result, or causal claim is already good enough and the real bottleneck is preserving how the evidence stays reusable

What this guide needs to preserve canonically is the compact routing rule that answers:
- when should I stay at broad runtime-observation strategy versus dropping into a narrower practical note?
- when is the real problem still observation-surface choice rather than replay or reverse-causality?
- when is the case really about capture stability and revisitable evidence rather than ordinary live hooks?
- when should I design a compare pair and isolate one first meaningful divergence before broader backward search?
- when is the next useful move to walk backward from one late effect instead of collecting more trace?
- when has the case narrowed further into choosing one watched object and one first bad write or decisive reducer behind it?
- when should runtime-evidence work stop deepening technically and continue instead into evidence-linkage / provenance packaging?

This page makes the branch read more like the native, protocol, malware, and protected-runtime practical subtrees:
- a branch entry surface
- a small set of recurring bottleneck families
- a compact ladder for moving from broad runtime uncertainty toward one smaller causal or branch-specific target
- one practical continuation surface for evidence reuse once the core technical proof is already good enough

## 2. Core claim
Runtime-evidence practical work is easiest to navigate when the analyst first classifies the current bottleneck into one of six recurring families:

1. **observability / layer-selection uncertainty**
   - the analyst still does not know what to observe, at which layer, or which live evidence would collapse the uncertainty fastest
2. **hook-placement / truth-boundary uncertainty**
   - runtime work is clearly needed and a broad layer is already plausible, but several candidate observation surfaces or hook points still compete and the current hooks are noisy, semantically late, too early to interpret, or attached to the wrong ownership boundary
3. **capture-stability / replay-worthiness uncertainty**
   - the interesting behavior is transient, expensive to reproduce, or too painful to keep rediscovering live, so the real question is whether to stabilize one representative execution for later revisits
4. **representative-execution and trace-anchor selection**
   - replay already looks attractive, but the analyst still needs to choose which execution window is worth preserving and which first event family should partition the trace before broader backward search begins
5. **compare-run design and first-divergence isolation**
   - two nearby runs already exist or can be produced, but the analyst still needs to design a useful compare pair, hold the right invariants steady, choose one compare boundary, and isolate the first meaningful divergence before deeper causal work begins
6. **late-effect to causal-boundary localization**
   - one suspicious late effect or one now-bounded compare-run divergence is already visible and revisitable enough, but the first causal write, branch, queue edge, or state reduction that predicts it is still unknown
7. **evidence package / handoff continuation**
   - one representative execution, compare-run result, or causal claim is already good enough technically, but still too scattered, assumption-heavy, or analyst-private to survive delay, handoff, or branch-specific reuse cleanly

A compact operator ladder for this branch is:

```text
choose the current runtime-evidence bottleneck
  -> secure the most trustworthy observation or replay surface
  -> reduce one visible question or effect into one smaller proof boundary
  -> hand back one smaller next target for native, protocol, malware, mobile, protected-runtime, or provenance work
```

The subtree is strongest when read as:
- **observe** the right behavior at the right layer
- **place** one smaller hook family at the right truth boundary
- **stabilize** one representative execution when live reruns are too fragile
- **choose** one representative execution window and one first trace anchor before broader backward search begins
- **design** one useful compare pair and isolate one first meaningful divergence before broad reverse-causality work
- **walk backward** from one visible late effect or one bounded divergence to one causal boundary that predicts it
- **package** one runtime result into a re-findable handoff unit when the technical proof is already good enough but still too scattered for reuse
- **preserve** the evidence linkage once the package already exists and the remaining bottleneck is broader reuse, handoff, or resumption

## 3. How to choose the right entry note
### Start with `runtime-behavior-recovery`
Use:
- `topics/runtime-behavior-recovery.md`

Start here when:
- the main uncertainty is still what to observe
- several observation surfaces are plausible and the analyst does not yet know which one will produce the next trustworthy object
- the case still needs broad framing around runtime answerability, observability, hook placement, or trace usefulness
- the analyst is still deciding whether dynamic validation or dynamic discovery is the real next move

Do **not** start here when:
- runtime work is clearly needed and the broad layer is already plausible, but the main remaining uncertainty is one smaller truth-boundary / hook-family choice
- the main bottleneck is already whether one execution should be captured for stable revisits
- the main bottleneck is already how to design a useful compare pair and isolate one first meaningful divergence
- a suspicious late effect is already visible and the real next move is backward causality reduction
- the case has already narrowed to one replay/query/watchpoint-style proof target

### Start with `hook-placement-and-observability-workflow-note`
Use:
- `topics/hook-placement-and-observability-workflow-note.md`

Start here when:
- runtime work is clearly needed
- a broad observation layer is already plausible enough to commit to
- several candidate hook points, owners, reducers, serializers, callbacks, queues, or consumers still compete
- the current uncertainty is still **which truthful observation surface to use next** rather than **whether runtime evidence matters at all**
- the next useful output is one smaller hook family plus one compare-ready result that shrinks the next decision

Do **not** start here when:
- the case still needs broader runtime-behavior framing before any layer can be chosen responsibly
- the real bottleneck is now capture stability or replay-worthiness rather than ordinary hook placement
- one suspicious late effect is already stable enough that reverse-causality localization is the clearer next move
- strong anti-instrumentation or observation-topology relocation pressure dominates the case and the problem is no longer ordinary hook placement

### Start with `record-replay-and-omniscient-debugging`
Use:
- `topics/record-replay-and-omniscient-debugging.md`

Start here when:
- the behavior is transient, delayed, or expensive to reproduce
- repeated live debugging is wasting effort
- the analyst needs to decide whether deterministic replay, time-travel debugging, or indexed execution history would make the case materially easier
- the real uncertainty is about capture cost versus evidence stability rather than about one specific causal boundary

Do **not** start here when:
- live observation is already stable enough and replay tradeoffs are no longer the main question
- replay already looks attractive, but the missing proof has narrowed further into which execution window to preserve and which first event family should anchor triage
- one representative execution and one first anchor already exist, but the next missing step is designing a useful compare pair and isolating one first meaningful divergence
- the effect boundary and one promising causal window already exist, making reverse-causality localization the clearer next step
- the case is mainly about provenance packaging after the causal boundary is already known

### Start with `representative-execution-selection-and-trace-anchor-workflow-note`
Use:
- `topics/representative-execution-selection-and-trace-anchor-workflow-note.md`

Start here when:
- replay or execution-history capture already looks attractive
- the behavior is transient, delayed, or expensive enough that one recorded run is probably worth keeping
- several recording windows are possible and the analyst still needs to choose the smallest representative execution
- a trace can be captured, but first triage still lacks one stable event family to partition the trace before broader backward search begins
- the real uncertainty is no longer broad replay worthiness, but practical capture-window and first-anchor selection

Do **not** start here when:
- the main uncertainty is still whether replay/tooling is worth using at all
- the truthful observation surface is still unclear and ordinary hook-placement work is not finished yet
- one stable anchor already exists, but the real missing step is still designing a useful compare pair and isolating the first meaningful divergence rather than walking backward from a bounded effect immediately
- one stable anchor already exists and the real missing proof is now the first causal write, branch, queue edge, or state reduction
- the technical replay result is already good enough and the real bottleneck is packaging, provenance, or handoff

### Start with `compare-run-design-and-divergence-isolation-workflow-note`
Use:
- `topics/compare-run-design-and-divergence-isolation-workflow-note.md`

Start here when:
- two nearby runs already exist or can be produced
- one representative execution and one first anchor are already good enough to support comparison
- the analyst still needs to design the pair on purpose instead of diffing broad traces blindly
- the real missing step is choosing one compare boundary and isolating the first meaningful divergence before deeper backward reasoning begins
- broad replay/tooling and broad anchor-selection questions are already mostly settled

Do **not** start here when:
- the truthful observation surface is still unclear
- replay worthiness is still the main question
- one good compare pair already exists and the first meaningful divergence is already known
- the technical result is already good enough and now needs packaging, provenance, or handoff more than new divergence analysis

### Start with `causal-write-and-reverse-causality-localization-workflow-note`
Use:
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`

Start here when:
- one suspicious late state, value, event, branch, delayed consequence, or already-bounded compare-run divergence is already visible
- replay, reverse execution, indexed query support, or at least one stable compare-run pair exists
- the next useful milestone is the first causal write, branch, queue edge, reducer, or state slot that predicts the visible effect or divergence
- the workflow can now be reduced into one effect boundary, one backward search window, and one proof-of-dependency boundary

Do **not** start here when:
- observation itself is still too noisy or distorted to trust
- the case still needs broad layer-selection or runtime-surface choice
- the target is better framed first as protocol parser-to-state proof, native interface-path proof, VM trace reduction, or mobile ownership diagnosis

## 4. Compact ladder across the branch
A useful way to read the branch is as eight common runtime-evidence bottleneck families that often chain into one another.

### A. Observation uncertainty -> informative runtime surface
Typical question:
- what should I observe next, and at what layer, to collapse uncertainty fastest?

Primary note:
- `topics/runtime-behavior-recovery.md`

Possible next handoff:
- `topics/hook-placement-and-observability-workflow-note.md` when the broad layer is now plausible but the truthful observation boundary is still unclear
- `topics/record-replay-and-omniscient-debugging.md` when live reruns are too fragile or expensive
- domain-specific branches once one observation surface becomes clearly best, such as:
  - `topics/mobile-protected-runtime-subtree-guide.md`
  - `topics/browser-runtime-subtree-guide.md`
  - `topics/firmware-and-protocol-context-recovery.md`

### B. Plausible layer -> truthful hook family
Typical question:
- if runtime work is clearly needed, which smallest truthful observation surface and hook family will shrink the next decision fastest?

Primary note:
- `topics/hook-placement-and-observability-workflow-note.md`

Possible next handoff:
- `topics/record-replay-and-omniscient-debugging.md` when the right surface is known but the behavior is too fragile to keep rediscovering live
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md` when one late effect is now stable enough to walk backward from
- target-specific branches once one hook surface has reduced the case into a narrower owner/parser/consumer question

### C. Fragile live behavior -> stable execution history
Typical question:
- should I keep poking this behavior live, or capture one representative execution so evidence stops evaporating?

Primary note:
- `topics/record-replay-and-omniscient-debugging.md`

Possible next handoff:
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md` when one suspicious late effect is now stable enough to walk backward from
- `topics/analytic-provenance-and-evidence-management.md` when the replay artifact now needs stronger evidence linkage or team handoff discipline

Routing reminder:
- leave broad replay/tooling discussion once one representative execution is already good enough and the real bottleneck becomes causal-boundary proof, branch-specific follow-up, or evidence packaging

### D. Replay-worthy behavior -> representative execution and first anchor
Typical question:
- which execution window is worth preserving, and which first event family should partition the trace before broader backward search begins?

Primary note:
- `topics/representative-execution-selection-and-trace-anchor-workflow-note.md`

Possible next handoff:
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md` when one stable anchor already exists and the next missing proof is the first causal write, branch, queue edge, reducer, or state slot behind the visible effect
- `topics/runtime-evidence-package-and-handoff-workflow-note.md` when the recording/anchor choice is already settled and the main remaining need is preserving the replay result for later reuse or handoff
- branch-specific practical notes when the chosen anchor has already reduced the case into one narrower owner/parser/consumer question

Routing reminder:
- leave representative-execution / anchor-selection work once one bounded execution and one stable first anchor are already good enough and the real bottleneck becomes reverse-causality, branch-specific proof, or packaging

### E. Representative anchor -> useful compare pair and first divergence
Typical question:
- how do I design one useful compare pair, hold the right invariants steady, and isolate one first meaningful divergence before broader backward reasoning begins?

Primary note:
- `topics/compare-run-design-and-divergence-isolation-workflow-note.md`

Possible next handoff:
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md` when the first meaningful divergence is now bounded and the missing proof is the first earlier causal boundary behind it
- branch-specific practical notes when the compare result now clearly belongs to one narrower native, protocol, malware, mobile, browser, or protected-runtime question
- `topics/runtime-evidence-package-and-handoff-workflow-note.md` when the compare result is already technically good enough and mainly needs preservation for later reuse

Routing reminder:
- leave compare-run design work once one trustworthy compare pair and one first meaningful divergence are already good enough and the real bottleneck becomes reverse-causality, branch-specific proof, or packaging

### F. Visible late effect or bounded divergence -> first causal boundary
Typical question:
- what first earlier write, branch, reduction, queue edge, or ownership handoff actually predicts the late effect or divergence I care about?

Primary note:
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`

Possible next handoff:
- `topics/native-interface-to-state-proof-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/staged-malware-execution-to-consequence-proof-workflow-note.md`
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- `topics/runtime-evidence-package-and-handoff-workflow-note.md`
- `topics/analytic-provenance-and-evidence-management.md`

Routing reminder:
- leave broad reverse-causality work once one causal boundary is already good enough and the real bottleneck becomes branch-specific proof or evidence packaging

### G. Visible bad late object -> first bad write or decisive reducer
Typical question:
- which exact late object should I watch, and what first bad write or decisive reducer behind it actually predicts the consequence I care about?

Primary note:
- `topics/first-bad-write-and-decisive-reducer-localization-workflow-note.md`

Possible next handoff:
- `topics/runtime-evidence-package-and-handoff-workflow-note.md` when one useful watched-object boundary is already proved and the real remaining need is preserving the result for reuse
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md` when the case broadens back out from one watched object into a larger causal window or neighboring upstream proof boundary
- branch-specific practical notes when the localized write/reducer now clearly belongs to one narrower native, protocol, malware, mobile, or protected-runtime proof target

Routing reminder:
- leave broad watchpoint or first-bad-write work once one watched object, one useful write/reducer boundary, and one downstream dependency already make the next task obvious

### H. Good runtime proof -> reusable evidence package
Typical question:
- how do I preserve one already-good compare-run result, replay anchor, or causal-boundary claim so it survives delay, handoff, and branch-specific reuse?

Primary note:
- `topics/runtime-evidence-package-and-handoff-workflow-note.md`

Possible next handoff:
- `topics/analytic-provenance-and-evidence-management.md` when the problem broadens from one package into a larger evidence-linkage system
- `topics/notebook-and-memory-augmented-re.md` when the real need is wider notebook/memory design rather than one specific package
- branch-specific practical notes when the packaged claim now supports a narrower native, protocol, malware, browser, mobile, or protected-runtime continuation

Routing reminder:
- leave package-focused work once one claim is already re-findable, bounded, and useful to the next consumer, and the real bottleneck becomes narrower technical proof or broader provenance-system design

## 5. The branch’s practical routing rule
When a case is clearly runtime-evidence shaped, ask these in order:

1. **Do I still not know what to observe or at what layer?**
   - if yes, start with broad runtime-behavior recovery framing
2. **Is runtime work clearly needed and is the broad layer already plausible, but the truthful observation surface or minimal hook family still unclear?**
   - if yes, start with hook-placement / observability workflow
3. **Do I already know the interesting behavior, but reruns are too fragile or expensive?**
   - if yes, start with replay / execution-history stabilization
4. **Does replay already look worthwhile, but I still need to choose which execution window is worth preserving and which first event family should anchor triage?**
   - if yes, start with representative-execution / trace-anchor selection
5. **Do I now have two nearby runs, but still need to design the compare pair and isolate one first meaningful divergence?**
   - if yes, start with compare-run design / divergence-isolation
6. **Is one suspicious late effect or one bounded divergence already visible and revisitable enough?**
   - if yes, start with reverse-causality localization
7. **Has the case narrowed further into one visible bad late object where the real missing step is choosing the watched object and finding the first bad write or decisive reducer behind it?**
   - if yes, start with first-bad-write / decisive-reducer localization
8. **Is the technical proof already good enough, but still too scattered to survive delay, handoff, or branch-specific reuse cleanly?**
   - if yes, start with runtime-evidence packaging / handoff

If more than one feels true, prefer the earliest bottleneck that still blocks later work.
That usually means:
- solve observation-surface choice before arguing about replay or reverse causality
- solve the truthful hook boundary before broadening into larger trace collection
- solve capture stability before assuming the visible effect can be revisited reliably
- solve representative-execution and first-anchor selection before broadening into reverse-causality
- solve watched-object / first-bad-write reduction before drifting back into broader trace browsing
- solve the first causal boundary before packaging it for reuse
- solve package clarity before broadening into larger provenance-system design

## 6. What this branch is strongest at
This branch is currently strongest at practical guidance for:
- deciding whether runtime evidence is the right next move at all
- distinguishing broad layer-selection questions from smaller hook-placement / truth-boundary questions
- distinguishing live-observation questions from execution-history questions
- turning one visible late effect into one causal-boundary question instead of a larger trace tour
- turning one visible bad late object into one watched-object / first-bad-write / decisive-reducer question instead of generic reverse-debugger tourism
- bridging runtime evidence into smaller next tasks in native, protocol, malware, mobile, and protected-runtime branches

That makes the branch good at cases where the main problem is not raw tooling availability, but choosing the most decision-relevant runtime-evidence move.

## 7. What this branch is still weaker at
This branch is still weaker than browser/mobile in some areas:
- it has fewer concrete child notes than the denser practical branches
- provenance/externalization is now recognized as a continuation surface, but it is still represented mostly through one adjacent cross-cutting page rather than a denser runtime-specific packaging stack
- runtime-evidence packaging and notebook discipline are now represented more explicitly, but still with a thinner continuation stack than the denser branches
- there is still room for a later branch pass focused specifically on richer compare-run preservation examples, workflow-specific evidence handoff patterns, or package templates

A practical continuity rule worth preserving now is:
- once one representative execution, compare-run pair, causal boundary, or watched-object / first-bad-write result is already good enough, do **not** keep the case in broad runtime-evidence routing just because the material is still messy
- route into `topics/analytic-provenance-and-evidence-management.md` when the real missing value is preserving how the evidence, assumptions, and causal claim stay linked for later reuse rather than finding one more upstream runtime surface

That means the right near-term maintenance pattern is usually:
- branch-shape repair
- conservative navigation strengthening
- new practical leaves only when a real operator gap appears

## 8. Common mistakes this guide prevents
This guide is meant to prevent several recurring branch-level mistakes:
- collecting more trace before deciding what uncertainty the runtime work is supposed to collapse
- skipping from broad runtime theory straight to replay even though the real bottleneck is one smaller truthful hook boundary
- treating record/replay like a generic debugger feature instead of a stability decision
- widening into full execution-history browsing when one narrow causal boundary would already shrink the task
- widening into generic reverse-debugger exploration when the real next move is one watched object and one first useful write/reducer boundary
- forcing runtime-evidence work to stay abstract even after the right hook boundary is already plausible
- drifting back into browser/mobile growth simply because those branches have denser source pressure

## 9. How this guide connects to the rest of the KB
Use this subtree when the case is best described as:
- uncertainty about what runtime evidence would matter most
- uncertainty about which truthful observation surface or hook family should be chosen next
- uncertainty about whether execution should be captured for stable revisits
- uncertainty about the first causal boundary behind a visible late effect
- uncertainty about the right watched object and first bad write / decisive reducer behind one visible bad late object
- uncertainty about how to preserve one already-good runtime result so it survives delay, handoff, or branch-specific reuse

Then route outward as soon as the case becomes more specific:
- to `topics/mobile-protected-runtime-subtree-guide.md` when platform/runtime resistance on mobile becomes the real branch entry problem
- to `topics/browser-runtime-subtree-guide.md` when the decisive observation surfaces are browser/runtime and token/session/widget shaped
- to `topics/firmware-and-protocol-context-recovery.md` when the issue is mainly protocol or environment-context recovery
- to `topics/native-practical-subtree-guide.md` when the runtime question has already reduced into a quieter native semantic or route-to-consequence problem
- to `topics/runtime-evidence-package-and-handoff-workflow-note.md` when the main remaining bottleneck is packaging one already-good runtime result into a re-findable evidence unit
- to `topics/analytic-provenance-and-evidence-management.md` when the main remaining bottleneck is preserving, packaging, or handing off the evidence cleanly

## 10. Topic summary
This subtree guide turns the runtime-evidence branch into a clearer operator ladder.

The compact reading is:
- choose the right observation surface
- place one smaller hook family at the right truth boundary
- stabilize execution history when live evidence is too fragile
- walk backward from one visible late effect to one causal boundary
- shrink one visible bad late object into the right watched object and one first useful write/reducer boundary
- package one already-good runtime result into a re-findable evidence unit when reuse is the real bottleneck

That makes the branch easier to enter, easier to sequence, and less dependent on already knowing whether the right next move is more observation, more hook-placement refinement, more replay, narrower reverse-causality proof, first-bad-write / watched-object reduction, or package/handoff work.
