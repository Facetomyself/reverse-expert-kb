# Unity / IL2Cpp State-Ownership and Persistence Workflow Note

Topic class: concrete workflow note
Ontology layers: mobile practical workflow, managed/native bridge diagnosis, protected-runtime game branch
Maturity: practical
Related pages:
- topics/mobile-reversing-and-runtime-instrumentation.md
- topics/mobile-protected-runtime-subtree-guide.md
- topics/native-interface-to-state-proof-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/anti-tamper-and-protected-runtime-analysis.md
- topics/trace-guided-and-dbi-assisted-re.md
- topics/observation-distortion-and-misleading-evidence.md

## 1. When to use this note
Use this note when the case is clearly Unity / IL2Cpp-shaped and the main bottleneck is no longer basic visibility, but **proving which state owner or update path actually controls the behavior you care about**.

Typical entry conditions:
- metadata dumps, strings, class names, or generated bindings provide some orientation already
- there are many plausible classes, components, managers, or wrappers
- obvious hooks fire, but the feature or outcome still does not line up cleanly with what the analyst changed or observed
- a value appears to change locally, then reverts, gets overwritten, or fails to persist across scenes, reloads, saves, or network refreshes
- the target feels partly mobile, partly native, and partly protected-runtime shaped

Use it for cases like:
- one currency/inventory/progression value appears writable but does not stick
- one battle/result/reward path is visible, but the first state owner is still unclear
- save-data structure is partly understood, but runtime state or reload/apply order still defeats the analysis
- anti-cheat / integrity / environment pressure makes some hooks noisy or misleading, even though metadata extraction succeeded

Do **not** use this note when the real bottleneck is still broader and earlier, such as:
- the app still needs basic environment-gate diagnosis
- anti-instrumentation failure dominates before any useful feature path is visible
- one request/signature field is already isolated and the task is mainly request-shaping recovery
- the problem is better modeled as a pure browser/WebView or firmware/protocol case

## 2. Core claim
In Unity / IL2Cpp mobile-game analysis, the best next move is often **not** more metadata dumping or broad class browsing.
It is to prove one concrete chain from:
- one visible feature or operator-relevant action
- through one managed entry or lifecycle callback family
- into one real object/state owner
- across one overwrite, refresh, serialization, or native boundary
- and then one visible persistence or rejection effect

The central practical question is usually:

```text
Which object instance, manager, lifecycle callback, serializer,
or managed/native handoff actually owns the durable behavior
once names and wrappers stop being trustworthy?
```

Until that ownership is proved, many Unity / IL2Cpp cases stay stuck in a loop of:
- readable labels
- plausible methods
- unstable hooks
- and no trustworthy explanation of why the value still reverts or the feature still fails

## 3. The five boundaries to mark explicitly

### A. Feature / action boundary
Freeze one feature or one reproducible action only.
Examples:
- spend currency
- claim reward
- complete battle
- load or save profile
- enter scene
- equip item

What to capture:
- one action that can be repeated in a controlled way
- one visible success/failure/revert outcome

### B. Managed entry / lifecycle boundary
This is where Unity/IL2Cpp-visible logic first becomes locally navigable.
Common anchors include:
- button/event callbacks
- scene lifecycle families such as awake/start/update-like paths
- result handlers
- manager/controller dispatchers
- model update calls that fan into several objects

What to capture:
- the first family of managed or generated methods clearly related to the feature
- which entry is easiest to compare and prove

### C. State-owner boundary
This is the most important boundary.
The key question is not “which method looked relevant?” but:
- which object instance, singleton, manager, component, or state slot actually owns the durable value?

Common useful anchors:
- manager singletons
- player/profile/state containers
- inventory/config/runtime model objects
- scene-global caches
- result application objects

What to capture:
- the narrowest object or field family whose change best predicts later behavior

### D. Overwrite / refresh / serialization boundary
This is where many Unity / IL2Cpp cases really fail.
Typical anchors include:
- frame/update-loop overwrite
- network result application
- save/load conversion
- serializer/deserializer steps
- scene transition reload or object reinit
- native plugin or engine callback returning authoritative data

What to capture:
- the first boundary where the candidate state can be confirmed, rejected, refreshed, or replaced

### E. Proof-of-effect boundary
This is where ownership is proved.
Typical outcomes include:
- value persists across one scene transition
- value reverts at one known update or result-apply step
- save material rehydrates into runtime state or fails to
- server or authoritative result overrides the local edit
- anti-cheat or integrity path reacts in one visible way

What to capture:
- one visible downstream effect linked back to the chosen state-owner path

## 4. Default workflow

### Step 1: Freeze one representative feature and one compare pair
Pick one feature/action only.
Good examples:
- spend 100 coins
- claim one reward
- finish one match with one result state
- modify one save-related value then reload once

Then build one compare pair with one changed condition only, such as:
- baseline action vs one local field mutation
- baseline run vs one scene transition/reload
- baseline run vs one save-load cycle
- minimal observation vs heavier hook setup

Avoid mixing too many uncontrolled differences.

### Step 2: Find the first stable managed entry family
Do not browse the whole dump.
Choose one entry family that:
- is close to the feature/action
- is reproducible across runs
- offers a reasonable bridge into object/state updates

Useful local labels:
- feature trigger
- lifecycle/update handler
- state owner candidate
- overwrite/refresh boundary
- visible effect

This usually shrinks a large Unity/IL2Cpp surface into one manageable chain.

### Step 3: Localize one real state owner
This is the decisive move.
Look for the first object or slot that would still matter even if method names were misleading.
Usually this is one of:
- a profile/player-state object
- a manager singleton
- an inventory or progression container
- a result/status struct or object family
- a serializer-facing data object

If many candidates exist, prefer the one that is:
- most stable across scene or callback variants
- easiest to observe dynamically
- closest to a visible persist/revert effect

### Step 4: Find the first overwrite or authority boundary
Once one candidate owner exists, ask:
- what could overwrite it?
- what could rehydrate it?
- what could reject it?
- what later source is more authoritative than the local setter?

Typical answers:
- update loop or frame tick
- network result apply
- scene reload/reconstruction
- save-load apply path
- native plugin callback
- integrity or anti-cheat gate

Do **not** stop at the first successful setter or hook if the value still fails behaviorally.

### Step 5: Prove one downstream persistence or rejection effect
Use one narrow proof target only.
Examples:
- the chosen field survives one scene transition
- the chosen field reverts exactly at one result-apply callback
- the save blob round-trips into one runtime object correctly
- the server result overwrites one local mutation at one known boundary
- one integrity path fires only after the candidate state mutation or observation setup

The goal is not full engine understanding.
It is one trustworthy ownership chain.

### Step 6: Hand off to one narrower next task only
After proving ownership, route to one next bottleneck only, such as:
- serializer structure recovery
- network result authority analysis
- anti-cheat/integrity evidence-trust diagnosis
- native plugin or engine callback localization
- save-data encryption/decryption detail work

Do not keep all Unity / IL2Cpp problems inside one giant page.

## 5. Practical scenario patterns

### Scenario A: Obvious setter fires, but value reverts later
Pattern:

```text
feature action
  -> visible setter or field write
  -> UI/value changes briefly
  -> later update/result/load path restores old value
```

Best move:
- stop treating the setter as the state owner
- localize the first overwrite/authority boundary
- prove which later path actually owns durable behavior

### Scenario B: Save-data edits are visible, but runtime behavior disagrees
Pattern:

```text
serialized material changed
  -> app loads
  -> some values appear changed
  -> later runtime path or scene logic disagrees or rewrites them
```

Best move:
- separate serialized representation from runtime state owner
- prove where deserialization or post-load normalization reduces into the in-memory object that really matters

### Scenario C: Class names are readable, but too many managers/components look plausible
Pattern:

```text
metadata dump gives many promising names
  -> hooks on several methods all seem relevant
  -> none explains one durable feature outcome
```

Best move:
- stop browsing by name alone
- choose one feature/action and localize the narrowest object whose state predicts later effect
- let ownership proof outrank naming elegance

### Scenario D: Hooked behavior diverges more under heavier instrumentation
Pattern:

```text
minimal observation gives plausible behavior
  -> broader hooks or tracing changes timing/semantics
  -> apparent state paths multiply or stop matching outcome
```

Best move:
- classify as possible evidence-distortion or protected-runtime pressure
- reduce hook scope
- prefer one compare pair and one later visible effect instead of broader instrumentation first

## 6. Breakpoint / hook placement guidance
Useful anchors include:
- feature-trigger callbacks
- scene/lifecycle entry points relevant to the feature
- manager singleton getters or owner-object retrieval points
- first field write on the candidate state owner
- serializer/deserializer boundaries
- result-apply or reward-apply handlers
- scene reload/reconstruction boundaries
- native plugin callbacks that refresh or replace state
- one later visible effect proving persist/revert/reject behavior

If evidence is noisy, anchor on:
- one object field, not every wrapper method
- one compare pair, not many scene variants
- one later visible consequence, not all intermediate callbacks

## 7. Failure patterns this note helps prevent

### 1. Mistaking readable metadata for proved ownership
Names and generated wrappers help navigation, but they do not prove which object owns durable behavior.

### 2. Treating the first setter as the decisive edge
In game/runtime code, visible setters are often followed by later overwrite, refresh, or authority boundaries.

### 3. Mixing runtime state and persistence state too early
Save blobs, in-memory objects, and server-approved state often diverge until one authority boundary is proved.

### 4. Broadening hooks when evidence trust is already degrading
Heavier instrumentation often creates more confusion if the first ownership chain is still unproved.

### 5. Turning a practical Unity / IL2Cpp problem into abstract engine taxonomy
The right next move is usually one feature -> owner -> overwrite/persist proof, not broad engine mapping.

## 8. Relationship to nearby pages
- `topics/mobile-reversing-and-runtime-instrumentation.md`
  - use as the broad mobile parent when layer choice, instrumentation, and environment constraints still dominate
- `topics/mobile-protected-runtime-subtree-guide.md`
  - use for routing inside the mobile/protected subtree once the case is clearly in this branch
- `topics/native-interface-to-state-proof-workflow-note.md`
  - use when the case behaves more like ordinary native baseline work and the main issue is proving one interface-to-state chain
- `topics/runtime-behavior-recovery.md`
  - use for broader runtime-evidence framing and observability logic
- `topics/anti-tamper-and-protected-runtime-analysis.md`
  - use when anti-cheat / integrity / anti-analysis resistance dominates the case
- `topics/trace-guided-and-dbi-assisted-re.md`
  - use when traces or DBI become the better path to reducing noisy protected execution
- `topics/observation-distortion-and-misleading-evidence.md`
  - use when instrumentation starts changing semantics or evidence quality directly

## 9. Minimal operator checklist
Use this note best when you can answer these in writing:
- what is the one feature or action I am trying to preserve or explain?
- what single condition changed in the compare pair?
- which managed entry or lifecycle family is the cleanest anchor?
- what object or state slot is my best real owner candidate?
- what overwrite / refresh / serialization boundary could defeat the naive local write?
- what one visible effect will prove persist, revert, or reject behavior?
- which narrower workflow note should take over next?

If you cannot answer those, the case may still need a broader environment, observability, or anti-instrumentation pass first.

## 10. Source footprint / evidence quality note
This note is intentionally workflow-first.

It is grounded by:
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/native-interface-to-state-proof-workflow-note.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/runtime-behavior-recovery.md`
- `topics/trace-guided-and-dbi-assisted-re.md`
- `topics/observation-distortion-and-misleading-evidence.md`
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`
- `sources/mobile-runtime-instrumentation/2026-03-16-unity-il2cpp-mobile-game-practice-notes.md`

The evidence base is sufficient for a practical workflow note because the aim is not to define the whole Unity or IL2Cpp ecosystem.
The aim is to normalize a recurring operator move that the KB already had signal for but no canonical note for.

## 11. Bottom line
When Unity / IL2Cpp mobile-game reversing stalls, the best next move is often not more dumping, broader browsing, or more hooks.
It is to localize one real state owner, identify the first overwrite/refresh/serialization boundary that can defeat naive local edits, and prove one visible persistence or rejection effect before broadening the analysis.
