# iOS Practical Subtree Guide

Topic class: subtree guide
Ontology layers: iOS mobile practice branch, workflow routing, operator ladder
Maturity: structured-practical
Related pages:
- topics/mobile-reversing-and-runtime-instrumentation.md
- topics/mobile-protected-runtime-subtree-guide.md
- topics/ios-traffic-topology-relocation-workflow-note.md
- topics/ios-environment-normalization-and-deployment-coherence-workflow-note.md
- topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md
- topics/ios-trust-path-and-pinning-localization-workflow-note.md
- topics/ios-objc-swift-native-owner-localization-workflow-note.md
- topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md
- topics/ios-chomper-owner-recovery-and-black-box-invocation-workflow-note.md
- topics/ios-request-signing-finalization-and-preimage-routing-workflow-note.md
- topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md
- topics/ios-mitigation-aware-replay-repair-workflow-note.md
- topics/ios-result-callback-to-policy-state-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md

## 1. Why this guide exists
This guide exists because the KB’s iOS practical branch now has several useful workflow notes, but until now it has still been easier to read as a small cluster of sibling notes than as a clear operator ladder.

The branch already had practical entry surfaces for:
- traffic-observation topology repair when proxy-visible evidence is incomplete or misleading
- environment normalization and deployment-coherence repair when install/signing path, rootful-vs-rootless mode, Frida recipe, or repack-vs-live-runtime choice still make runs incomparable
- packaging / jailbreak / runtime-gate diagnosis when the app still diverges before later analysis is trustworthy
- trust-path and pinning localization once traffic topology is truthful enough and the remaining bottleneck is routing-vs-trust-vs-post-trust diagnosis on iOS
- ObjC / Swift / native owner localization once the target flow is reachable enough to study
- Flutter/Dart cross-runtime owner localization when iOS shell, engine routing, and Dart ownership all compete
- execution-assisted owner replay when the owner path is already plausible and the next bottleneck is minimal truthful invocation
- iOS request-signing finalization / preimage routing when one owner path is already plausible and the next question is whether to prove one last iOS request-finalization boundary, move earlier into preimage/state capture, or keep one truthful black-box path
- callback/block landing and signature-recovery proof once one callback family is already plausible but the truthful landing and parameter contract still need to be proved under modern iOS conditions
- callback/result-to-policy consequence proof once visible result material exists but the first behavior-changing consumer is still unclear

What was missing was the compact routing rule that answers:
- where should I start when a case is clearly iOS-shaped?
- which note comes next after the current bottleneck is reduced?
- when am I still fixing visibility or setup versus proving ownership, controlled replay, or policy consequence?

This page makes the iOS branch read more like the KB’s stronger practical subtrees:
- a branch entry surface
- a small set of recurring bottleneck families
- a compact ladder for turning one reachable iOS flow into one smaller trustworthy working model

A newer practical reminder is also now worth preserving canonically: before broad iOS gate diagnosis, some cases first need a narrower environment-normalization pass so install/signing path, rootful-vs-rootless differences, Frida deployment recipe, and repack-vs-live-runtime choice stop contaminating later comparisons.

## 2. Core claim
iOS practical work is easiest to navigate when the analyst first classifies the current bottleneck into one of eight recurring families:

1. **traffic-topology uncertainty**
   - the user-visible action clearly performs network work, but the current observation surface is still too partial or misleading to trust
2. **environment-normalization uncertainty**
   - the case is iOS-shaped, but install/signing path, rootful-vs-rootless mode, Frida deployment recipe, or repack-vs-live-runtime choice still make runs operationally incomparable
3. **broad setup / runtime-gate uncertainty**
   - the case is iOS-shaped, but packaging, signing, jailbreak environment, instrumentation visibility, or realism drift still dominates even after basic normalization
4. **trust-path / pinning uncertainty**
   - traffic topology is truthful enough and the run is comparable enough, but the decisive request family is still blocked by routing-vs-trust-vs-post-trust uncertainty on iOS
5. **post-gate owner uncertainty**
   - the flow is reachable enough to study, yet several ObjC / Swift / native boundaries still compete and the first consequence-bearing owner is unclear
6. **cross-runtime owner uncertainty**
   - the path is clearly Flutter/Dart shaped and the real owner search spans iOS shell, bridge/engine routing, Dart state, and native workers
7. **controlled-replay / init-obligation uncertainty**
   - one owner path is already plausible enough to target, but the next bottleneck is reconstructing minimal init/context obligations until one truthful callable path exists
8. **iOS signing-finalization / preimage-routing uncertainty**
   - one owner path is already plausible and maybe even callable, but it is still unclear whether the cheapest next reduction is one last iOS request-finalization boundary, one earlier preimage/state capture point, or stopping at a truthful black-box request path
9. **callback/block landing and signature-contract uncertainty**
   - one callback/block family is already plausible, but the truthful invoke landing and usable runtime contract are still not proven strongly enough to trust owner, replay, or policy claims
10. **callback/result-to-policy consequence uncertainty**
   - visible callbacks or result wrappers already exist, but the first behavior-changing consumer or local policy state is still unclear

Inside families 2 and 3, a recurring practical reminder now deserves to stay explicit: do not collapse all early iOS setup into one vague "jailbroken vs not" bucket. Installation/signing path, rootful vs rootless mode, Frida deployment coherence, and rewrite/repack stability can each change whether later evidence is trustworthy; some cases first need environment normalization before broader gate diagnosis is even meaningful.

A compact operator ladder for this branch is:

```text
iOS-shaped case
  -> choose the earliest still-blocking iOS bottleneck
  -> reduce it to one smaller trustworthy boundary
  -> prove one downstream effect
  -> hand back one more reliable route into the next iOS step
```

The subtree is strongest when read as:
- **see** one truthful traffic surface
- **normalize** one comparable environment/deployment recipe
- **stabilize** one trustworthy runtime/setup state
- **localize** one decisive trust path when routing-vs-trust remains the blocker
- **own** one consequence-bearing path
- **replay** one truthful callable owner path when static cleanup is no longer the cheapest next move
- **reduce** one iOS-shaped signing/finalization boundary before flattening the case into generic preimage work
- **land** one callback/block family on one truthful invoke boundary with one usable contract
- **repair** one replay-close mitigation-aware path by isolating one smaller context/materialization/init gap
- **consume** one callback/result into one local policy effect

## 3. How to choose the right entry note
### Start with `ios-traffic-topology-relocation-workflow-note`
Use:
- `topics/ios-traffic-topology-relocation-workflow-note.md`

Start here when:
- the target flow clearly performs meaningful network work
- ordinary proxy capture is partial, misleading, or empty enough that later reasoning is not trustworthy
- the main question is still whether the current traffic-observation surface is wrong
- one relocated VPN / full-tunnel / transparent MITM style surface could falsify the current diagnosis

Do **not** start here when:
- one decisive request family is already visible enough and the real bottleneck is now setup/gate, owner, or callback consequence
- the case is not primarily network-surface shaped

### Start with `ios-environment-normalization-and-deployment-coherence-workflow-note`
Use:
- `topics/ios-environment-normalization-and-deployment-coherence-workflow-note.md`

Start here when:
- the case is clearly iOS-shaped, but install/signing path, rootful-vs-rootless mode, Frida deployment recipe, or repack-vs-live-runtime choice still make runs operationally incomparable
- you still cannot tell whether the current instability is target-shaped or setup-shaped
- the next useful output is one representative flow and one compare pair that are actually comparable
- the strongest immediate risk is blaming the target before the environment recipe is normalized

Do **not** start here when:
- the current problem is still primarily traffic-topology blindness
- one comparable representative flow already exists and the real bottleneck has clearly shifted into a broader gate-family question, owner localization, or result-to-policy proof

### Start with `ios-packaging-jailbreak-and-runtime-gate-workflow-note`
Use:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`

Start here when:
- the case is clearly iOS-shaped, but broader packaging, signing, jailbreak, tooling, realism, or early-vs-late divergence still dominates
- you can already reach or partly reach the flow, and the environment is normalized enough that the remaining drift is now worth treating as a true gate-family problem
- the next useful output is one representative flow, one compare pair, and one proved gate family
- rootful vs rootless differences, install/signing path, Frida deployment coherence, or repack/rewrite instability are still relevant, but now as part of a real gate diagnosis rather than basic run incomparability

Do **not** start here when:
- the current problem is still primarily traffic-topology blindness
- the case is not yet normalized enough for the compared runs to be operationally meaningful
- the case is already stable enough that the real bottleneck is post-gate owner localization

### Start with `ios-trust-path-and-pinning-localization-workflow-note`
Use:
- `topics/ios-trust-path-and-pinning-localization-workflow-note.md`

Start here when:
- traffic topology is already truthful enough that one decisive request family can be reasoned about
- the run is normalized enough that the remaining divergence is worth treating as trust-shaped rather than setup-shaped
- the current bottleneck is whether the target family is failing at Foundation/Security/native trust evaluation or later policy logic
- generic trust hooks or pinning bypasses partly work, but not on the request family that matters

Do **not** start here when:
- the current problem is still primarily traffic-topology blindness
- compared runs are still too operationally incomparable to trust the diagnosis
- the real bottleneck has clearly shifted into post-gate owner localization rather than trust-path localization

### Start with `ios-objc-swift-native-owner-localization-workflow-note`
Use:
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`

Start here when:
- the target flow is already reachable enough to study
- selectors, Swift methods, wrappers, or native helpers are visible enough to navigate
- the main uncertainty is which boundary first owns one state write, request-finalization step, or other durable consequence
- the path is broadly iOS-shaped rather than distinctly Flutter/Dart cross-runtime

Do **not** start here when:
- broad setup/gate uncertainty still dominates
- the decisive complication is clearly Flutter/Dart cross-runtime owner search
- the owner is already plausible enough and the real bottleneck is now controlled replay or result-to-policy consequence proof

### Start with `ios-flutter-cross-runtime-owner-localization-workflow-note`
Use:
- `topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md`

Start here when:
- the target is clearly Flutter/Dart shaped on iOS
- iOS shell code, bridge/engine routing, Dart state, and native helpers all look relevant
- repack/rewrite/static instrumentation attempts are brittle enough that live-runtime owner recovery may now be cheaper
- the real question is which Dart/object boundary actually owns the artifact or consequence

Do **not** start here when:
- the case is not meaningfully cross-runtime
- broad setup/gate work still dominates
- one owner is already plausible enough and the real next bottleneck is controlled replay rather than owner choice

### Start with `ios-chomper-owner-recovery-and-black-box-invocation-workflow-note`
Use:
- `topics/ios-chomper-owner-recovery-and-black-box-invocation-workflow-note.md`

Start here when:
- one owner path is already plausible enough to target
- live traces already expose enough setup and call-chain truth that execution-assisted replay looks cheaper than more static cleanup
- the current bottleneck is now minimal init/context obligation recovery and reduced invocation contract
- the question has shifted from “who owns this?” to “what is the smallest truthful way to call it?”

Do **not** start here when:
- the owner is still unclear
- broad setup/gate or traffic-topology uncertainty still dominates
- the case is still better framed as result-to-policy reduction rather than controlled owner replay

### Start with `ios-request-signing-finalization-and-preimage-routing-workflow-note`
Use:
- `topics/ios-request-signing-finalization-and-preimage-routing-workflow-note.md`

Start here when:
- one owner path is already plausible enough to target and maybe even partly callable
- the real question is no longer broad owner choice, but whether one last iOS request-finalization boundary still matters
- you need to decide whether to keep reducing locally on iOS request builders/finalization, move one hop earlier into preimage/state capture, or stop at one truthful black-box path
- the target still feels iOS-shaped rather than purely generic signing-taxonomy shaped

Do **not** start here when:
- the owner is still unclear
- the case still primarily needs broad controlled replay / init-obligation repair before any request-shaping conclusion is trustworthy
- the remaining gap is already clearly result/callback-to-policy consequence rather than request shaping

### Start with `ios-block-callback-landing-and-signature-recovery-workflow-note`
Use:
- `topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md`

Start here when:
- one callback/block family is already plausible enough to freeze
- the current bottleneck is whether the invoke landing and parameter contract are truthful enough to trust
- PAC / arm64e / dyld-cache truthfulness now affects confidence in the callback view
- placeholder block signatures still make replay, owner, or policy claims too speculative

Do **not** start here when:
- the broad bottleneck is still visibility, setup/gate drift, or owner localization
- the callback/result is already trustworthy enough and the real gap is the first policy-bearing consumer
- the remaining problem is already better framed as one narrower runtime-table/init obligation

### Start with `ios-mitigation-aware-replay-repair-workflow-note`
Use:
- `topics/ios-mitigation-aware-replay-repair-workflow-note.md`

Start here when:
- one owner path, callback family, or dispatch family is already plausible enough that broad owner search should stop
- the callback landing is already trustworthy enough, or already reduced enough, that the real bottleneck is now replay-close repair rather than landing proof
- replay is structurally close, but one authenticated-context, object-materialization, initialized-image, or narrower runtime obligation still appears to be missing
- PAC / arm64e / dyld-cache truth still affects whether the remaining replay claim is trustworthy

Do **not** start here when:
- the callback/block landing itself is still not trustworthy enough to support replay claims
- the code view is still too untruthful to say whether the family is even right
- the remaining problem is already clearly the first behavior-changing consumer rather than replay repair

### Start with `ios-result-callback-to-policy-state-workflow-note`
Use:
- `topics/ios-result-callback-to-policy-state-workflow-note.md`

Start here when:
- callbacks, completions, Swift result wrappers, or native-return wrappers are already visible
- the landing/contract is already trustworthy enough that the callback family itself is no longer the main uncertainty
- the current bottleneck is no longer visibility or broad owner search, but the first behavior-changing local policy state
- you need to separate callback surface, normalization, policy mapping, and first consumer
- one downstream effect could prove the right policy-bearing boundary

Do **not** start here when:
- the true owner is still unclear
- the case still needs controlled replay to make the owner callable at all
- the visible callback is still trapped inside broader setup drift or untrusted observation
- the landing or signature contract is still too ambiguous to support policy claims

## 4. Compact ladder across the branch
A useful way to read the branch is as eleven common bottleneck families that often chain into one another.

### A. Incomplete network picture -> truthful traffic surface
Typical question:
- is the target request really absent, or am I still standing on the wrong observation surface?

Primary note:
- `topics/ios-traffic-topology-relocation-workflow-note.md`

Possible next handoff:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- trust-path / request-ownership notes once one decisive request family is visible

### B. Incomparable setup -> one normalized representative flow
Typical question:
- are these runs even operationally comparable, or am I still mixing install/signing, rootful/rootless, Frida recipe, and repack/live-runtime differences together?

Primary note:
- `topics/ios-environment-normalization-and-deployment-coherence-workflow-note.md`

Possible next handoff:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md`

### C. Reachable but unstable setup -> proved gate family
Typical question:
- which install/signing/tooling/jailbreak/realism boundary first explains why the now-comparable flow diverges?

Primary note:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`

Possible next handoff:
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`
- `topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md`

### D. Reachable request family -> first decisive trust path
Typical question:
- is the target request family still failing at routing-vs-trust-vs-post-trust boundaries, and where does the decisive iOS trust decision actually happen?

Primary note:
- `topics/ios-trust-path-and-pinning-localization-workflow-note.md`

Possible next handoff:
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md` when trust is no longer the earliest blocker and the remaining gap is consequence ownership
- `topics/ios-result-callback-to-policy-state-workflow-note.md` when trust appears to pass and the remaining failure is later policy logic
- request/signature or native proof pages when the localized trust path narrows the case further

### E. Reachable flow -> first consequence-bearing owner
Typical question:
- which ObjC / Swift / native boundary first owns the state write, request-finalization step, or policy effect that actually matters?

Primary note:
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`

Possible next handoff:
- `topics/ios-chomper-owner-recovery-and-black-box-invocation-workflow-note.md` when the owner is already good enough and the real bottleneck has shifted into minimal truthful init/context obligation recovery and reduced invocation contract
- `topics/ios-result-callback-to-policy-state-workflow-note.md`
- request/signature or native proof pages when the owner narrows the case further

### F. Cross-runtime confusion -> first Dart/object owner
Typical question:
- which boundary first turns shell trigger plus Flutter routing into the actual artifact or consequence I care about?

Primary note:
- `topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md`

Possible next handoff:
- `topics/ios-chomper-owner-recovery-and-black-box-invocation-workflow-note.md` when the owner is already plausible enough and the real bottleneck has shifted from owner choice into truthful callable-path recovery
- request/signature recovery or native proof pages once the owner is proved

### G. Plausible owner -> truthful callable path
Typical question:
- do I still need more code readability, or do I already know enough to reconstruct the smallest truthful invocation path?

Primary note:
- `topics/ios-chomper-owner-recovery-and-black-box-invocation-workflow-note.md`

Routing reminder:
- leave broad replay / harness work here once one truthful callable path is already good enough
- if replay is close-but-wrong, continue into `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`
- if replay or live invocation already exposes result material and the real gap is now the first behavior-changing local policy state, continue into `topics/ios-result-callback-to-policy-state-workflow-note.md`

Possible next handoff:
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`
- `topics/ios-result-callback-to-policy-state-workflow-note.md`
- narrower request/signature or consequence pages once controlled replay is truthful enough

### H. Plausible iOS signer path -> finalization / preimage / black-box routing
Typical question:
- do I still need one iOS-specific request-finalization boundary, one earlier preimage/state capture point, or is one truthful black-box request path already enough?

Primary note:
- `topics/ios-request-signing-finalization-and-preimage-routing-workflow-note.md`

Possible next handoff:
- `topics/mobile-signature-location-and-preimage-recovery-workflow-note.md` when one earlier input/preimage family is now the true bottleneck
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md` when outputs are close-but-wrong because one runtime artifact or init chain is still missing
- `topics/ios-result-callback-to-policy-state-workflow-note.md` when truthful result material already exists and the real gap has shifted into consequence proof

### I. Plausible callback/block family -> truthful landing and usable contract
Typical question:
- is this callback/block family really landing where I think it is, and is its contract narrow enough to trust?

Primary note:
- `topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md`

Routing reminder:
- enter this stage when one callback family is already plausible but PAC-era confidence, dyld/cache truth, or placeholder signatures still make stronger claims unsafe
- do not jump straight from vague block visibility into policy interpretation if the landing itself is still structurally ambiguous

Possible next handoff:
- `topics/ios-pac-shaped-callback-and-dispatch-failure-triage.md`
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`
- `topics/ios-result-callback-to-policy-state-workflow-note.md`

### J. Replay-close mitigation-aware path -> one smaller repair target
Typical question:
- is this iOS path already replay-close enough that the real remaining gap is one authenticated-context, object-materialization, or narrower init/runtime obligation rather than broader owner or landing uncertainty?

Primary note:
- `topics/ios-mitigation-aware-replay-repair-workflow-note.md`

Routing reminder:
- enter this stage once one callback/dispatch family or owner path is already plausible enough and the replay path is structurally close
- do not stay in broad callback-landing work once the landing is already trustworthy enough and the real gap is now replay repair
- do not reopen broad owner search if the strongest evidence already says the case is replay-close and late-failing

Possible next handoff:
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`
- `topics/ios-result-callback-to-policy-state-workflow-note.md`
- narrower owner or callback pages only if the replay-close classification collapses back into wrong-family or untruthful landing

### K. Visible callback/result -> first policy-bearing consumer
Typical question:
- which callback / wrapper / mapper / consumer first turns visible result material into one local behavior change?

Primary note:
- `topics/ios-result-callback-to-policy-state-workflow-note.md`

Routing reminder:
- enter this stage once controlled replay, black-box invocation, or narrower init-obligation repair is already good enough to expose truthful result material
- do not stay in broad replay or init-obligation work once the real missing proof is no longer owner callability but the first app-local policy consequence
- if the landing or callback contract itself is still doubtful, route back to `topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md` first
- if the path is only replay-close and the remaining gap is still one smaller context/materialization/init proof, route to `topics/ios-mitigation-aware-replay-repair-workflow-note.md` first

Possible next handoff:
- challenge-loop, attestation, request-shaping, or native proof pages depending on the proved consumer

## 5. The branch’s practical routing rule
When a case is clearly iOS-shaped, ask these in order:

1. **Is the decisive request family still invisible because the observation surface may be wrong?**
   - if yes, start with traffic-topology relocation
2. **Are the compared runs still operationally incomparable because install/signing path, rootful-vs-rootless mode, Frida recipe, or repack-vs-live-runtime choice changed too much at once?**
   - if yes, start with environment normalization and deployment-coherence repair
3. **Is broader setup, signing, jailbreak, tooling, or realism drift still the earliest blocker even after normalization?**
   - if yes, start with packaging / jailbreak / runtime-gate diagnosis
4. **Is the decisive request family reachable enough, but the remaining blocker is still routing-vs-trust-vs-post-trust diagnosis on iOS?**
   - if yes, start with trust-path / pinning localization
5. **Is the flow now reachable enough, but the first consequence-bearing owner still unclear?**
   - if yes, start with broad ObjC / Swift / native owner localization
6. **Is that ownership problem clearly Flutter/Dart cross-runtime shaped?**
   - if yes, switch to the specialized Flutter/cross-runtime owner note
7. **Is one owner already plausible enough, and is the real bottleneck no longer owner choice but making that owner callable truthfully?**
   - if yes, stop broad owner-localization work and continue into controlled replay / black-box invocation
8. **Is the owner already plausible/callable enough, but it is still unclear whether one last iOS request-finalization boundary or one earlier preimage/state capture point is the cheaper next reduction?**
   - if yes, continue into iOS request-signing finalization / preimage routing
9. **Is replay already good enough, but the remaining gap has narrowed into one runtime table family, initialized-image boundary, side-condition, or minimal init/context obligation?**
   - if yes, leave broad replay work and continue into runtime-table / initialization-obligation recovery
10. **Is one callback/block family already plausible, but the landing or signature contract still too ambiguous to trust?**
   - if yes, continue into callback/block landing and signature-recovery work
11. **Is the path already replay-close, but the remaining gap still looks like one authenticated-context, object-materialization, or narrower init/runtime obligation?**
   - if yes, continue into mitigation-aware replay-repair work
12. **Are callbacks or result wrappers already visible, and is the landing already trustworthy enough, but the first behavior-changing policy state still hidden?**
   - if yes, continue into result/callback-to-policy-state work

If more than one feels true, prefer the earliest boundary that still blocks later work.
That usually means:
- fix the traffic surface before arguing about trust or owner details
- normalize one comparable environment/deployment recipe before diagnosing deeper gate logic
- prove one broad gate family before deep trust-path or owner work
- localize one decisive trust path before broadening into consequence ownership when routing-vs-trust is still unresolved
- prove one owner before building a replay harness
- prove one truthful callable path before cataloging many setup helpers
- leave broad replay/harness work once one truthful callable path is already good enough and the real bottleneck has shifted
- before flattening the case into generic signing taxonomy, ask whether one last iOS request-finalization boundary is still the real missing proof
- if replay is already close-but-wrong, reduce one narrower runtime-table or initialization obligation before widening outward again
- if one callback family is plausible but the landing or signature contract is still doubtful, prove that boundary before stronger owner or policy claims
- if the path is already replay-close and late-failing, isolate one smaller context/materialization/init repair target before reopening broad owner work
- prove one policy-bearing consumer before widening callback coverage

## 6. What this branch is strongest at
This branch is currently strongest at practical guidance for:
- separating traffic-topology problems from broader iOS gate problems
- separating setup/gate uncertainty from trust-path localization and then from post-gate owner localization
- separating ordinary ObjC / Swift / native owner problems from Flutter/Dart cross-runtime owner problems
- treating execution-assisted replay as a continuation of owner recovery rather than tool tourism
- separating callback/block landing truth from later owner or policy claims
- separating visible callback/result material from the first true policy-bearing consumer

That makes the branch good at cases where iOS work is already partly reachable, but the next useful move still depends on disciplined routing rather than broader tracing.

## 7. What this branch is still weaker at
This branch is still weaker than the densest browser/mobile areas in some ways:
- it only recently gained enough leaf notes to justify its own dedicated subtree guide
- the branch now has a dedicated iOS trust-path continuation, but iOS-specific request-signature continuations are still mostly connected through broader mobile pages rather than a denser iOS-only continuation stack
- the branch now has a dedicated PAC/arm64e mitigation-aware continuation page for cases where modern iOS work has already narrowed into authenticated-pointer / cache-truthfulness / replay-close confusion rather than broad setup or owner uncertainty
- it now also has a narrower callback/dispatch continuation for cases where one authenticated handoff is already frozen and the real next question is whether the failure is wrong-family, wrong-context, lying-code-view, or replay-close missing-obligation drift
- it now also has a dedicated mitigation-aware replay-repair continuation for cases where callback/owner choice is already plausible enough and the real remaining gap is one smaller authenticated-context, object-materialization, or init/runtime obligation

That means the right near-term maintenance pattern is usually:
- branch-shape repair
- conservative navigation strengthening
- concrete workflow-note deepening only when a real iOS operator gap appears

## 8. Common mistakes this guide prevents
This guide is meant to prevent several recurring branch-level mistakes:
- treating all iOS practical notes as flat siblings instead of a common ladder
- jumping into owner or callback work while the observation surface is still untrustworthy
- widening into replay harness work before one owner is narrowed enough to target
- confusing Flutter/bridge visibility with actual Dart/object ownership
- treating plausible callback/block presence as proof of a truthful landing
- treating visible callback or result wrappers as behavioral ownership by default
- reopening broad owner or callback-family work when the case is already replay-close and really needs one smaller mitigation-aware repair target
- leaking routing logic into run reports instead of preserving it canonically in the KB itself

## 9. How this guide connects to the rest of the KB
Use this subtree when the case is best described as:
- an iOS investigation where the next bottleneck is still choosing the right observation surface, proving one gate family, narrowing one owner, reconstructing one callable path, proving one callback/block landing boundary, or proving one result-to-policy consumer

Then route outward as soon as the case becomes more specifically shaped:
- to broader mobile/runtime synthesis when platform comparison or observation-surface theory matters more than the iOS ladder itself
- to request/signature, challenge-loop, response-consumer, attestation, or native proof pages once the iOS-specific bottleneck is reduced
- to runtime-table/init-obligation work when controlled replay is already close and the remaining gap is one narrow runtime obligation

## 10. Topic summary
This subtree guide turns the iOS practical branch into a clearer operator ladder.

The compact reading is:
- choose the right traffic surface
- normalize the right environment/deployment recipe
- stabilize the right runtime/setup gate
- localize the right trust path when routing-vs-trust is still the blocker
- prove the right owner
- reconstruct the smallest truthful callable path when needed
- reduce one narrower runtime-table or initialization obligation when replay is already close-but-wrong
- prove the right callback/block landing when the callback family is plausible but still structurally ambiguous
- repair the right replay-close mitigation-aware path when the landing is already good enough but one smaller context/materialization/init gap remains
- prove the right callback/result consumer

That makes the branch easier to enter, easier to sequence, and less dependent on already knowing which iOS workflow note to read first.
