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
- topics/ios-objc-swift-native-owner-localization-workflow-note.md
- topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md
- topics/ios-chomper-owner-recovery-and-black-box-invocation-workflow-note.md
- topics/ios-result-callback-to-policy-state-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md

## 1. Why this guide exists
This guide exists because the KB’s iOS practical branch now has several useful workflow notes, but until now it has still been easier to read as a small cluster of sibling notes than as a clear operator ladder.

The branch already had practical entry surfaces for:
- traffic-observation topology repair when proxy-visible evidence is incomplete or misleading
- environment normalization and deployment-coherence repair when install/signing path, rootful-vs-rootless mode, Frida recipe, or repack-vs-live-runtime choice still make runs incomparable
- packaging / jailbreak / runtime-gate diagnosis when the app still diverges before later analysis is trustworthy
- ObjC / Swift / native owner localization once the target flow is reachable enough to study
- Flutter/Dart cross-runtime owner localization when iOS shell, engine routing, and Dart ownership all compete
- execution-assisted owner replay when the owner path is already plausible and the next bottleneck is minimal truthful invocation
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
iOS practical work is easiest to navigate when the analyst first classifies the current bottleneck into one of seven recurring families:

1. **traffic-topology uncertainty**
   - the user-visible action clearly performs network work, but the current observation surface is still too partial or misleading to trust
2. **environment-normalization uncertainty**
   - the case is iOS-shaped, but install/signing path, rootful-vs-rootless mode, Frida deployment recipe, or repack-vs-live-runtime choice still make runs operationally incomparable
3. **broad setup / runtime-gate uncertainty**
   - the case is iOS-shaped, but packaging, signing, jailbreak environment, instrumentation visibility, or realism drift still dominates even after basic normalization
4. **post-gate owner uncertainty**
   - the flow is reachable enough to study, yet several ObjC / Swift / native boundaries still compete and the first consequence-bearing owner is unclear
5. **cross-runtime owner uncertainty**
   - the path is clearly Flutter/Dart shaped and the real owner search spans iOS shell, bridge/engine routing, Dart state, and native workers
6. **controlled-replay / init-obligation uncertainty**
   - one owner path is already plausible enough to target, but the next bottleneck is reconstructing minimal init/context obligations until one truthful callable path exists
7. **callback/result-to-policy consequence uncertainty**
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
- **own** one consequence-bearing path
- **replay** one truthful callable owner path when static cleanup is no longer the cheapest next move
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

### Start with `ios-result-callback-to-policy-state-workflow-note`
Use:
- `topics/ios-result-callback-to-policy-state-workflow-note.md`

Start here when:
- callbacks, completions, Swift result wrappers, or native-return wrappers are already visible
- the current bottleneck is no longer visibility or broad owner search, but the first behavior-changing local policy state
- you need to separate callback surface, normalization, policy mapping, and first consumer
- one downstream effect could prove the right policy-bearing boundary

Do **not** start here when:
- the true owner is still unclear
- the case still needs controlled replay to make the owner callable at all
- the visible callback is still trapped inside broader setup drift or untrusted observation

## 4. Compact ladder across the branch
A useful way to read the branch is as six common bottleneck families that often chain into one another.

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

### D. Reachable flow -> first consequence-bearing owner
Typical question:
- which ObjC / Swift / native boundary first owns the state write, request-finalization step, or policy effect that actually matters?

Primary note:
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`

Possible next handoff:
- `topics/ios-chomper-owner-recovery-and-black-box-invocation-workflow-note.md` when the owner is already good enough and the real bottleneck has shifted into minimal truthful init/context obligation recovery and reduced invocation contract
- `topics/ios-result-callback-to-policy-state-workflow-note.md`
- request/signature or native proof pages when the owner narrows the case further

### E. Cross-runtime confusion -> first Dart/object owner
Typical question:
- which boundary first turns shell trigger plus Flutter routing into the actual artifact or consequence I care about?

Primary note:
- `topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md`

Possible next handoff:
- `topics/ios-chomper-owner-recovery-and-black-box-invocation-workflow-note.md` when the owner is already plausible enough and the real bottleneck has shifted from owner choice into truthful callable-path recovery
- request/signature recovery or native proof pages once the owner is proved

### F. Plausible owner -> truthful callable path
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

### G. Visible callback/result -> first policy-bearing consumer
Typical question:
- which callback / wrapper / mapper / consumer first turns visible result material into one local behavior change?

Primary note:
- `topics/ios-result-callback-to-policy-state-workflow-note.md`

Routing reminder:
- enter this stage once controlled replay, black-box invocation, or narrower init-obligation repair is already good enough to expose truthful result material
- do not stay in broad replay or init-obligation work once the real missing proof is no longer owner callability but the first app-local policy consequence

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
4. **Is the flow now reachable enough, but the first consequence-bearing owner still unclear?**
   - if yes, start with broad ObjC / Swift / native owner localization
5. **Is that ownership problem clearly Flutter/Dart cross-runtime shaped?**
   - if yes, switch to the specialized Flutter/cross-runtime owner note
6. **Is one owner already plausible enough, and is the real bottleneck no longer owner choice but making that owner callable truthfully?**
   - if yes, stop broad owner-localization work and continue into controlled replay / black-box invocation
7. **Is replay already good enough, but the remaining gap has narrowed into one runtime table family, initialized-image boundary, side-condition, or minimal init/context obligation?**
   - if yes, leave broad replay work and continue into runtime-table / initialization-obligation recovery
8. **Are callbacks or result wrappers already visible, but the first behavior-changing policy state still hidden?**
   - if yes, continue into result/callback-to-policy-state work

If more than one feels true, prefer the earliest boundary that still blocks later work.
That usually means:
- fix the traffic surface before arguing about trust or owner details
- normalize one comparable environment/deployment recipe before diagnosing deeper gate logic
- prove one broad gate family before deep owner search
- prove one owner before building a replay harness
- prove one truthful callable path before cataloging many setup helpers
- leave broad replay/harness work once one truthful callable path is already good enough and the real bottleneck has shifted
- if replay is already close-but-wrong, reduce one narrower runtime-table or initialization obligation before widening outward again
- prove one policy-bearing consumer before widening callback coverage

## 6. What this branch is strongest at
This branch is currently strongest at practical guidance for:
- separating traffic-topology problems from broader iOS gate problems
- separating setup/gate uncertainty from post-gate owner localization
- separating ordinary ObjC / Swift / native owner problems from Flutter/Dart cross-runtime owner problems
- treating execution-assisted replay as a continuation of owner recovery rather than tool tourism
- separating visible callback/result material from the first true policy-bearing consumer

That makes the branch good at cases where iOS work is already partly reachable, but the next useful move still depends on disciplined routing rather than broader tracing.

## 7. What this branch is still weaker at
This branch is still weaker than the densest browser/mobile areas in some ways:
- it only recently gained enough leaf notes to justify its own dedicated subtree guide
- iOS-specific trust-path and request-signature continuations are still mostly connected through broader mobile pages rather than a denser iOS-only continuation stack
- more case pressure may later justify narrower notes around trust-path continuation, result-code families, or PAC/arm64e-era protected-runtime specifics

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
- treating visible callback or result wrappers as behavioral ownership by default
- leaking routing logic into run reports instead of preserving it canonically in the KB itself

## 9. How this guide connects to the rest of the KB
Use this subtree when the case is best described as:
- an iOS investigation where the next bottleneck is still choosing the right observation surface, proving one gate family, narrowing one owner, reconstructing one callable path, or proving one result-to-policy consumer

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
- prove the right owner
- reconstruct the smallest truthful callable path when needed
- reduce one narrower runtime-table or initialization obligation when replay is already close-but-wrong
- prove the right callback/result consumer

That makes the branch easier to enter, easier to sequence, and less dependent on already knowing which iOS workflow note to read first.
