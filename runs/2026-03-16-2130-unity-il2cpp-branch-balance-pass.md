# Run Report — 2026-03-16 21:30 — Unity / IL2Cpp branch-balance pass

## 1. Scope this run
This run was a scheduled autosync / branch-balance / maintenance pass for `research/reverse-expert-kb/`.

The key direction choice this run was to keep improving the KB itself while resisting drift back into the already-dense browser anti-bot, WebView, and generic mobile risk-control branches.
Recent runs had already repaired several underweighted practical branches with concrete notes:
- protocol parser -> state-edge localization
- native interface -> state proof
- malware staged execution -> consequence proof
- VM trace -> semantic anchor reduction
- flattened dispatcher -> state-edge reduction
- iOS runtime-gate diagnosis
- causal-write / reverse-causality runtime-evidence diagnosis

That left another repeatedly signaled but still underdeveloped practical branch:
- **Unity / IL2Cpp / mobile-game protected-runtime work**

The specific gap targeted this run was:

```text
metadata dumps, strings, class names, or generated bindings may exist,
static structure may look promising,
but the investigation still stalls because the analyst has not yet proved
which object instance, manager, serializer, update path,
or managed/native handoff actually owns the durable behavior.
```

So this run focused on adding a practical Unity / IL2Cpp workflow note centered on state ownership and persistence proof, plus the supporting source note and navigation updates needed to make that branch visible.

## 2. Direction review
### Current direction check
The KB still improves most when a run gives the analyst a better next move instead of widening taxonomy.
That still means preferring:
- practical workflow notes
- one representative feature/action
- one consequence-bearing state owner or edge
- one overwrite / refresh / authority boundary
- one proved downstream effect

That practical style is already strong in:
- browser first-consumer and request-finalization notes
- WebView/native handoff and lifecycle notes
- mobile challenge / policy / delayed-consequence notes
- native interface -> state proof
- protocol parser -> state consequence routing
- deobfuscation trace/dispatcher reduction notes
- malware staged handoff -> consequence proof
- iOS runtime-gate diagnosis
- runtime-evidence late-effect -> causal-boundary routing

What remained thin was a concrete branch for Unity / IL2Cpp and mobile game protection work.
The KB repeatedly acknowledged this practitioner signal in parent pages and source curation, but still lacked a canonical practical note for the most recurring bottleneck:
- not “how do I dump metadata?”
- but “which object or boundary actually owns the feature once names and wrappers stop being trustworthy?”

This run repaired that gap.

### Branch-balance review
An explicit branch-balance review was appropriate again because the KB had now completed a useful series of repairs to several thinner branches, and it was worth checking what still remained structurally underrepresented.

Current practical branch picture before this pass looked roughly like:
- **very strong:** browser anti-bot / captcha / request-signature / hybrid WebView workflows
- **strong:** mobile protected-runtime / challenge / ownership / policy / delayed-consequence notes
- **improving:** native, protocol, malware, deobfuscation, iOS, and runtime-evidence practical branches
- **still relatively thin:** Unity / IL2Cpp / mobile-game protected-runtime practical workflows

The specific imbalance visible here was:
- parent pages already said Unity / IL2Cpp and mobile game protection were recurring practitioner subdomains
- subtree guidance explicitly admitted weakness around systematic mobile game / anti-cheat separation
- but there was still no canonical operator-facing note for one of the most common practical middle states:
  - metadata exists
  - classes/wrappers look partly readable
  - a setter or callback seems plausible
  - yet the value still reverts, gets overwritten, or fails to persist because the real owner or authority boundary is unproved

That made this run a good fit for branch-balance repair.
It improved a repeatedly signaled branch without defaulting back into more browser/mobile-web micro-variants.

## 3. Files reviewed
Primary files reviewed this run:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent `runs/*.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/community-practice-signal-map.md`
- `topics/native-interface-to-state-proof-workflow-note.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/runtime-behavior-recovery.md`
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`

## 4. KB changes made
### A. Created a new Unity / IL2Cpp source note
Created:
- `sources/mobile-runtime-instrumentation/2026-03-16-unity-il2cpp-mobile-game-practice-notes.md`

What it adds:
- a workflow-centered consolidation for the repeatedly signaled Unity / IL2Cpp / mobile game protected-runtime branch
- explicit phrasing around the recurring bottleneck where metadata visibility exists but state ownership is still unproved
- practical scenario framing for:
  - visible class names but unclear owner
  - local value changes that revert later
  - save-data visibility without stable behavioral consequence
  - anti-cheat / integrity pressure degrading evidence quality

### B. Created a new practical workflow note
Created:
- `topics/unity-il2cpp-state-ownership-and-persistence-workflow-note.md`

What it adds:
- a concrete operator-facing note for Unity / IL2Cpp cases where names, wrappers, or setters are visible but durable behavior is still unexplained
- explicit routing from:
  - one feature/action boundary
  - one managed entry/lifecycle family
  - one real state owner
  - one overwrite / refresh / serialization boundary
  - one visible persist/reject effect
- scenario patterns for:
  - setter fires but value reverts later
  - save-data edits disagree with runtime behavior
  - readable metadata without proved ownership
  - heavier instrumentation causing evidence distortion

### C. Strengthened subtree navigation
Updated:
- `topics/mobile-protected-runtime-subtree-guide.md`

What changed:
- removed the prior claim that the subtree was simply weak on systematic mobile game / anti-cheat separation without acknowledging the new repair
- added the new Unity / IL2Cpp note into the concrete-note inventory
- added explicit routing guidance for when to read the new note first

### D. Updated top-level navigation
Updated:
- `index.md`

What changed:
- added the new Unity / IL2Cpp note into the mobile / protected-runtime practice subtree list
- added an explicit mobile-branch routing bullet for Unity / IL2Cpp state-ownership and persistence proof
- made the top-level map more honest about the KB’s growing practical game/protected-runtime branch

## 5. Why these changes matter
This run improved the KB itself rather than merely collecting another community source mention about Unity or game protection.

It did **not**:
- create a broad Unity taxonomy page
- return to browser or WebView timing variants
- turn the branch into a game-cheat or bypass checklist
- stop at metadata dumping guidance

It **did**:
- identify a practical branch that had repeated source pressure but no canonical note
- normalize the recurring operator bottleneck around state ownership and persistence proof
- connect the branch cleanly to existing native, runtime-evidence, and protected-runtime practical styles

The durable improvement is:

```text
the KB now has a practical Unity / IL2Cpp entry note for the moment when
metadata-visible classes, wrappers, or setters already exist,
but the analyst still cannot tell which object owner,
overwrite/refresh boundary, or persistence consequence actually matters.
```

That is much more useful than another broad “Unity / IL2Cpp matters” paragraph would have been.

## 6. New findings
### A. The real Unity / IL2Cpp gap was ownership proof, not visibility
The KB already had enough signal to say Unity / IL2Cpp and mobile game protection were recurring practical branches.
What it lacked was a compact operator note for the common middle state where visibility exists but ownership is still ambiguous.

### B. Unity / IL2Cpp cases fit the KB’s broader consequence-first style well
A now-clear cross-branch pattern is:
- native: interface -> state -> effect proof
- protocol: parser -> state consequence edge
- malware: staging handoff -> consequence proof
- runtime evidence: late effect -> causal boundary localization
- Unity / IL2Cpp: feature trigger -> state owner -> persistence/revert proof

That coherence makes the KB more consistent and easier to navigate.

### C. Persistence failure is often more informative than the first successful setter
One valuable normalization from this run is that Unity / IL2Cpp work should not stop at proving a local setter or readable class method.
The recurring practical leverage is often at the first overwrite / authority boundary:
- update loop
- serializer/deserializer boundary
- scene reload/reinit
- network result apply
- native plugin callback
- integrity/anti-cheat reaction

### D. This branch naturally bridges mobile, native, runtime-evidence, and protected-runtime work
That makes it a high-value branch-balance repair:
- it grows a genuinely thin branch
- it also improves structural linkage across several previously repaired branches

## 7. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- recent `runs/*.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/community-practice-signal-map.md`
- `topics/native-interface-to-state-proof-workflow-note.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/runtime-behavior-recovery.md`

### Existing source notes used this run
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`

### Fresh source consolidation created this run
- `sources/mobile-runtime-instrumentation/2026-03-16-unity-il2cpp-mobile-game-practice-notes.md`

## 8. Reflections / synthesis
A stronger KB-wide operator pattern is now visible:

```text
some useful structure is already visible
  -> freeze one representative feature/action
  -> localize one trustworthy owner or consequence-bearing edge
  -> identify the first boundary that can overwrite, reject, or re-authorize it
  -> prove one downstream effect
  -> return to one smaller next task
```

The Unity / IL2Cpp branch now has its own explicit version of that pattern.
That is healthy directionally because it keeps the KB centered on:
- ownership
- authority boundaries
- persistence/revert proof
- next trustworthy move

rather than on ever-larger metadata dumps or engine-taxonomy growth.

## 9. Candidate topic pages to create or improve
### Improved this run
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`

### Created this run
- `topics/unity-il2cpp-state-ownership-and-persistence-workflow-note.md`
- `sources/mobile-runtime-instrumentation/2026-03-16-unity-il2cpp-mobile-game-practice-notes.md`
- this run report

### Good next improvements
- a follow-on note around Unity save/serializer boundary localization if more cases cluster there
- a follow-on note around networked authoritative refresh vs local state mutation in mobile game flows
- a tighter anti-cheat / integrity evidence-trust bridge if more protected mobile game cases accumulate

## 10. Next-step research directions
1. Keep the Unity / IL2Cpp branch practical with small workflow notes instead of broad engine taxonomy growth.
2. Watch for a good follow-on split around serializer/apply boundaries if more save/persistence cases accumulate.
3. Watch for a good follow-on split around server-authoritative refresh and local-state overwrite if more networked game cases cluster there.
4. Continue resisting browser/WebView overconcentration unless a clearly missing high-value practical gap appears.
5. Revisit top-level navigation after a few more branch-balance passes so the KB’s center of gravity remains honest.

## 11. Concrete scenario notes or actionable tactics added this run
### Practical scenario normalized this run
**A Unity / IL2Cpp case already exposes metadata-visible classes, wrappers, or setters, but the analyst still cannot tell which object owner, overwrite/refresh boundary, or persistence consequence really controls behavior.**

### Concrete tactics added
- do not confuse readable metadata with proved ownership
- freeze one feature/action and one compare pair only
- localize one real state owner before broadening hooks
- look for the first overwrite / refresh / serialization / authority boundary instead of trusting the first setter
- prove one visible persist/reject effect before deepening save, anti-cheat, or native-plugin work

## 12. Commit / archival-sync status
### KB files changed this run
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/topics/mobile-protected-runtime-subtree-guide.md`
- `research/reverse-expert-kb/topics/unity-il2cpp-state-ownership-and-persistence-workflow-note.md`
- `research/reverse-expert-kb/sources/mobile-runtime-instrumentation/2026-03-16-unity-il2cpp-mobile-game-practice-notes.md`
- `research/reverse-expert-kb/runs/2026-03-16-2130-unity-il2cpp-branch-balance-pass.md`

### Commit intent
Commit only the reverse-KB files touched by this run.
Do not mix in unrelated workspace or pre-existing reverse-KB changes.

### Sync intent
After commit, run:
- `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

If sync fails:
- preserve local KB progress
- mention the failure briefly in this run report
- do not roll back the KB improvement

## 13. Bottom line
This autosync run improved the reverse KB by repairing another underrepresented practical branch: Unity / IL2Cpp / mobile-game protected-runtime workflow routing.

The KB already knew from practitioner signals that this branch mattered.
Now it also has a concrete workflow note for the common bottleneck where visibility exists but ownership is still unproved, which makes the mobile/protected subtree more balanced, more navigable, and more practically useful.
