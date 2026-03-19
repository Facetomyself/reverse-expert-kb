# Runtime-Evidence Practical Subtree Guide

Topic class: subtree guide
Ontology layers: runtime-evidence practice branch, observability/replay/causality routing, operator ladder
Maturity: structured-practical
Related pages:
- topics/runtime-behavior-recovery.md
- topics/hook-placement-and-observability-workflow-note.md
- topics/record-replay-and-omniscient-debugging.md
- topics/causal-write-and-reverse-causality-localization-workflow-note.md
- topics/analytic-provenance-and-evidence-management.md
- topics/notebook-and-memory-augmented-re.md

## 1. Why this guide exists
This guide exists because the KB’s runtime-evidence branch already has a strong synthesis page and several useful practical leaves, but it is still easy to read as a short conceptual cluster instead of a usable operator ladder.

The branch already had practical entry surfaces for:
- broad runtime answerability and observability framing
- hook-placement and truth-boundary selection when runtime work is clearly needed but the best observation surface is still unclear
- record/replay and execution-history tradeoffs when live reruns are too fragile or expensive
- reverse-causality localization when one suspicious late effect is already visible and revisitable enough

What this guide needs to preserve canonically is the compact routing rule that answers:
- when should I stay at broad runtime-observation strategy versus dropping into a narrower practical note?
- when is the real problem still observation-surface choice rather than replay or reverse-causality?
- when is the case really about capture stability and revisitable evidence rather than ordinary live hooks?
- when is the next useful move to walk backward from one late effect instead of collecting more trace?

This page makes the branch read more like the native, protocol, malware, and protected-runtime practical subtrees:
- a branch entry surface
- a small set of recurring bottleneck families
- a compact ladder for moving from broad runtime uncertainty toward one smaller causal or branch-specific target

## 2. Core claim
Runtime-evidence practical work is easiest to navigate when the analyst first classifies the current bottleneck into one of four recurring families:

1. **observability / layer-selection uncertainty**
   - the analyst still does not know what to observe, at which layer, or which live evidence would collapse the uncertainty fastest
2. **hook-placement / truth-boundary uncertainty**
   - runtime work is clearly needed and a broad layer is already plausible, but several candidate observation surfaces or hook points still compete and the current hooks are noisy, semantically late, too early to interpret, or attached to the wrong ownership boundary
3. **capture-stability / replay-worthiness uncertainty**
   - the interesting behavior is transient, expensive to reproduce, or too painful to keep rediscovering live, so the real question is whether to stabilize one representative execution for later revisits
4. **late-effect to causal-boundary localization**
   - one suspicious late effect is already visible and revisitable enough, but the first causal write, branch, queue edge, or state reduction that predicts it is still unknown

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
- **walk backward** from one visible late effect to one causal boundary that predicts it

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
- the effect boundary and one promising causal window already exist, making reverse-causality localization the clearer next step
- the case is mainly about provenance packaging after the causal boundary is already known

### Start with `causal-write-and-reverse-causality-localization-workflow-note`
Use:
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`

Start here when:
- one suspicious late state, value, event, branch, or delayed consequence is already visible
- replay, reverse execution, indexed query support, or at least one stable compare-run pair exists
- the next useful milestone is the first causal write, branch, queue edge, reducer, or state slot that predicts the visible effect
- the workflow can now be reduced into one effect boundary, one backward search window, and one proof-of-dependency boundary

Do **not** start here when:
- observation itself is still too noisy or distorted to trust
- the case still needs broad layer-selection or runtime-surface choice
- the target is better framed first as protocol parser-to-state proof, native interface-path proof, VM trace reduction, or mobile ownership diagnosis

## 4. Compact ladder across the branch
A useful way to read the branch is as four common runtime-evidence bottleneck families that often chain into one another.

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

### D. Visible late effect -> first causal boundary
Typical question:
- what first earlier write, branch, reduction, queue edge, or ownership handoff actually predicts the late effect I care about?

Primary note:
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`

Possible next handoff:
- `topics/native-interface-to-state-proof-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/staged-malware-execution-to-consequence-proof-workflow-note.md`
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- `topics/analytic-provenance-and-evidence-management.md`

Routing reminder:
- leave broad reverse-causality work once one causal boundary is already good enough and the real bottleneck becomes branch-specific proof or evidence packaging

## 5. The branch’s practical routing rule
When a case is clearly runtime-evidence shaped, ask these in order:

1. **Do I still not know what to observe or at what layer?**
   - if yes, start with broad runtime-behavior recovery framing
2. **Is runtime work clearly needed and is the broad layer already plausible, but the truthful observation surface or minimal hook family still unclear?**
   - if yes, start with hook-placement / observability workflow
3. **Do I already know the interesting behavior, but reruns are too fragile or expensive?**
   - if yes, start with replay / execution-history stabilization
4. **Is one suspicious late effect already visible and revisitable enough?**
   - if yes, start with reverse-causality localization

If more than one feels true, prefer the earliest bottleneck that still blocks later work.
That usually means:
- solve observation-surface choice before arguing about replay or reverse causality
- solve the truthful hook boundary before broadening into larger trace collection
- solve capture stability before assuming the visible effect can be revisited reliably
- solve the first causal boundary before broadening back into more generic trace collection

## 6. What this branch is strongest at
This branch is currently strongest at practical guidance for:
- deciding whether runtime evidence is the right next move at all
- distinguishing broad layer-selection questions from smaller hook-placement / truth-boundary questions
- distinguishing live-observation questions from execution-history questions
- turning one visible late effect into one causal-boundary question instead of a larger trace tour
- bridging runtime evidence into smaller next tasks in native, protocol, malware, mobile, and protected-runtime branches

That makes the branch good at cases where the main problem is not raw tooling availability, but choosing the most decision-relevant runtime-evidence move.

## 7. What this branch is still weaker at
This branch is still weaker than browser/mobile in some areas:
- it has fewer concrete child notes than the denser practical branches
- provenance/externalization still sits partly adjacent rather than fully laddered inside this subtree
- runtime-evidence packaging and notebook discipline could still use a tighter practical continuation guide
- there is still room for a later branch pass focused specifically on runtime-evidence packaging, compare-run preservation, or workflow-specific evidence handoff

A practical continuity rule worth preserving now is:
- once one representative execution, compare-run pair, or causal boundary is already good enough, do **not** keep the case in broad runtime-evidence routing just because the material is still messy
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
- forcing runtime-evidence work to stay abstract even after the right hook boundary is already plausible
- drifting back into browser/mobile growth simply because those branches have denser source pressure

## 9. How this guide connects to the rest of the KB
Use this subtree when the case is best described as:
- uncertainty about what runtime evidence would matter most
- uncertainty about which truthful observation surface or hook family should be chosen next
- uncertainty about whether execution should be captured for stable revisits
- uncertainty about the first causal boundary behind a visible late effect

Then route outward as soon as the case becomes more specific:
- to `topics/mobile-protected-runtime-subtree-guide.md` when platform/runtime resistance on mobile becomes the real branch entry problem
- to `topics/browser-runtime-subtree-guide.md` when the decisive observation surfaces are browser/runtime and token/session/widget shaped
- to `topics/firmware-and-protocol-context-recovery.md` when the issue is mainly protocol or environment-context recovery
- to `topics/native-practical-subtree-guide.md` when the runtime question has already reduced into a quieter native semantic or route-to-consequence problem
- to `topics/analytic-provenance-and-evidence-management.md` when the main remaining bottleneck is preserving, packaging, or handing off the evidence cleanly

## 10. Topic summary
This subtree guide turns the runtime-evidence branch into a clearer operator ladder.

The compact reading is:
- choose the right observation surface
- place one smaller hook family at the right truth boundary
- stabilize execution history when live evidence is too fragile
- walk backward from one visible late effect to one causal boundary

That makes the branch easier to enter, easier to sequence, and less dependent on already knowing whether the right next move is more observation, more hook-placement refinement, more replay, or narrower reverse-causality proof.
