# Protected-Runtime Practical Subtree Guide

Topic class: subtree guide
Ontology layers: protected-runtime practice branch, deobfuscation / anti-tamper routing, operator ladder
Maturity: structured-practical
Related pages:
- topics/anti-tamper-and-protected-runtime-analysis.md
- topics/obfuscation-deobfuscation-and-packed-binaries.md
- topics/vm-trace-to-semantic-anchor-workflow-note.md
- topics/flattened-dispatcher-to-state-edge-workflow-note.md
- topics/packed-stub-to-oep-and-first-real-module-workflow-note.md
- topics/decrypted-artifact-to-first-consumer-workflow-note.md
- topics/integrity-check-to-tamper-consequence-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md
- topics/protected-runtime-observation-topology-selection-workflow-note.md

## 1. Why this guide exists
This guide exists because the KB’s protected / deobfuscation branch already has several strong practical notes, but until now it has been easier to read as a flat list of sibling pages than as a usable operator ladder.

The branch already had practical entry surfaces for:
- VM or flattened execution that is visible but still semantically noisy
- packed or staged bootstrap where the first trustworthy post-unpack handoff is still unclear
- decrypted artifacts that are readable but not yet tied to their first ordinary consumer
- integrity / self-check logic that is visible but not yet tied to its first real consequence
- runtime-table / initialization-obligation cases where live state is truer than repaired static artifacts
- observation-topology failures where direct attach/spawn/app-local hooks are themselves the unstable thing

What was missing was the compact routing rule that answers:
- where should I start when a target is clearly protected-runtime shaped?
- which note comes next after the current bottleneck is reduced?
- when am I still in protection churn versus when have I reached a reusable static or runtime target?

This page makes that branch read more like the malware, protocol, and mobile practical subtrees:
- a branch entry surface
- a small set of recurring bottleneck families
- a compact ladder for moving from protected churn toward one smaller trustworthy target

## 2. Core claim
Protected-runtime practical work is easiest to navigate when the analyst first classifies the current bottleneck into one of six recurring families:

1. **observation-topology failure**
   - direct attach, spawn, or app-local observation is detected, too visible, too late, or semantically misleading
2. **trace / dispatcher churn**
   - visible VM, flattened control flow, handler churn, or repetitive protected execution is the main problem
3. **packed / staged bootstrap handoff**
   - a stub, shell, decrypt/copy/fixup loop, or staged loader is already visible, but the first trustworthy post-unpack handoff is still unclear
4. **artifact-to-consumer proof**
   - strings, config, tables, bytecode, or normalized buffers are already readable enough to inspect, but the first ordinary consumer is still missing
5. **runtime-artifact / initialization-obligation recovery**
   - static dumps, repaired artifacts, or offline reconstructions look damaged, under-initialized, or close-but-wrong, while live/runtime state appears truer
6. **integrity / tamper consequence proof**
   - checks are visible, but the first reduced result or consequence-bearing tripwire is still unclear

A compact operator ladder for this branch is:

```text
choose the current protection-shaped bottleneck
  -> recover the smallest more trustworthy boundary, artifact, or obligation
  -> prove one consequence-bearing edge or downstream effect
  -> hand back one quieter static/runtime target
```

The subtree is strongest when read as:
- **reposition** observation when the current topology itself is the problem
- **anchor** noisy execution when trace/dispatcher churn dominates
- **handoff** out of staged startup when packing/bootstrap dominates
- **consume** recovered artifacts when readable material exists but ordinary use is still unproved
- **stabilize** one truthful runtime artifact plus one minimal init obligation when static views are still lying
- **tripwire** the first behavior-changing integrity consequence when checks are already visible

## 3. How to choose the right entry note
### Start with `protected-runtime-observation-topology-selection-workflow-note`
Use:
- `topics/protected-runtime-observation-topology-selection-workflow-note.md`

Start here when:
- direct attach, spawn, app-local hooks, or ordinary instrumentation are themselves unstable, detected, semantically late, or misleading
- the next real decision is not yet which function or handler to hook, but which observation topology should exist at all
- boundary-side, lower-surface, embedded, relocated, or trace/DBI-backed observation looks more promising than repeating the current posture
- the analyst needs one better observation boundary before narrower packed, VM, artifact-consumer, or integrity work becomes trustworthy

Do **not** start here when:
- the current observation model is already good enough and the bottleneck is now inside one visible packed, VM, artifact, or integrity path
- the case is already narrowed to a specific Android surface-choice problem handled better by the Android observation notes

### Start with `vm-trace-to-semantic-anchor-workflow-note`
Use:
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`

Start here when:
- virtualization, flattening, handler churn, or noisy protected execution is already visible
- some trace, DBI, replay, or runtime-guided evidence already exists
- the next bottleneck is reducing repetitive execution into one stable semantic anchor plus one consequence-bearing handler/state edge

Do **not** start here when:
- the dominant uncertainty is still the packed/bootstrap handoff
- the dominant uncertainty is already one integrity consequence branch
- the main issue is no longer execution churn, because a readable artifact is already in hand
- the observation model itself is still failing and topology selection is the real next move

### Start with `packed-stub-to-oep-and-first-real-module-workflow-note`
Use:
- `topics/packed-stub-to-oep-and-first-real-module-workflow-note.md`

Start here when:
- a stub, shell, decrypt/copy/fixup loop, import-repair stage, or staged loader is already visible
- the real bottleneck is one trustworthy OEP-like boundary plus one first ordinary-code anchor downstream from it
- the analyst needs one reusable post-unpack dump, image state, module/object cluster, or first real consumer target

Do **not** start here when:
- there is no real loader/stub handoff problem and the target is already post-unpack
- unpacking is solved enough, but later VM/flattened execution still dominates
- the readable object already exists and the real bottleneck is its consumer

### Start with `decrypted-artifact-to-first-consumer-workflow-note`
Use:
- `topics/decrypted-artifact-to-first-consumer-workflow-note.md`

Start here when:
- strings, config, bytecode, tables, decrypted buffers, normalized blobs, or recovered code artifacts are already readable enough to inspect
- the analyst still does not know which ordinary parser, policy, scheduler, request builder, or payload consumer first makes them behaviorally relevant
- the next useful output is one first consumer routine, state write, or downstream operational edge

Do **not** start here when:
- the artifact itself is still too unstable because unpacking or trace churn is unresolved
- integrity-result reduction is the dominant hidden boundary rather than artifact use
- the real problem is that replay stays close-but-wrong because one runtime obligation is still missing

### Start with `runtime-table-and-initialization-obligation-recovery-workflow-note`
Use:
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`

Start here when:
- repaired dumps, unpacked images, static tables, or offline reconstructions still look damaged, under-initialized, or close-but-wrong
- live/runtime memory, initialized tables, post-init images, or command-sequenced state looks truer than the static view
- the next useful output is one minimal init chain, one runtime-artifact family, one initialized-image dump point, or one side-condition checklist that explains why replay is drifting

Do **not** start here when:
- the static/runtime discrepancy is still too vague and the real bottleneck remains packed handoff, trace churn, or artifact-consumer proof
- the current issue is already a visible integrity/tamper reducer rather than close-but-wrong replay or under-initialized artifacts

### Start with `integrity-check-to-tamper-consequence-workflow-note`
Use:
- `topics/integrity-check-to-tamper-consequence-workflow-note.md`

Start here when:
- CRC, checksum, self-hash, signature, anti-patch, anti-hook, or other integrity logic is already visible
- the key unknown is the first reduced result, state bucket, or consequence-bearing tripwire that predicts later degrade / decoy / suppress / exit behavior
- the best next output is one reducer helper, state flag, or branch worthy of compare-run proof

Do **not** start here when:
- the real bottleneck is still identifying where protected execution hands off into ordinary code
- the target is dominated by flattened execution churn rather than visible integrity logic
- the case is already better framed as a mobile-specific attestation/result-to-policy problem
- the nearer missing edge is actually one runtime artifact or initialization obligation that explains why otherwise plausible replay is still drifting

## 4. Compact ladder across the branch
A useful way to read the branch is as six common bottleneck families that often chain into one another.

### A. Observation-topology failure -> one more truthful boundary
Typical question:
- is the current attach/spawn/app-local observation posture itself the thing that is failing or distorting the evidence?

Primary note:
- `topics/protected-runtime-observation-topology-selection-workflow-note.md`

Possible next handoff:
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- `topics/packed-stub-to-oep-and-first-real-module-workflow-note.md`
- `topics/decrypted-artifact-to-first-consumer-workflow-note.md`
- `topics/integrity-check-to-tamper-consequence-workflow-note.md`
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`

### B. Trace or dispatcher churn -> semantic anchor
Typical question:
- which small stable thing predicts later behavior better than the raw protected execution does?

Primary note:
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`

Possible next handoff:
- `topics/flattened-dispatcher-to-state-edge-workflow-note.md`
- `topics/native-semantic-anchor-stabilization-workflow-note.md`
- `topics/native-interface-to-state-proof-workflow-note.md`

### C. Packed startup -> trustworthy post-unpack handoff
Typical question:
- where does loader churn end and reusable post-unpack analysis begin?

Primary note:
- `topics/packed-stub-to-oep-and-first-real-module-workflow-note.md`

Possible next handoff:
- `topics/vm-trace-to-semantic-anchor-workflow-note.md` when unpacking is solved but later protected execution still dominates
- `topics/native-semantic-anchor-stabilization-workflow-note.md` when the post-unpack region is readable but semantically slippery
- `topics/decrypted-artifact-to-first-consumer-workflow-note.md` when the handoff yields one readable artifact whose first consumer is still unclear
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md` when the recovered image remains under-initialized and live/runtime state looks truer

### D. Readable artifact -> first ordinary consumer
Typical question:
- what first parser, policy, scheduler, request, or payload consumer proves this recovered artifact actually matters?

Primary note:
- `topics/decrypted-artifact-to-first-consumer-workflow-note.md`

Possible next handoff:
- `topics/native-interface-to-state-proof-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md` when the artifact is still close-but-wrong because one runtime obligation is missing

### E. Static artifact drift -> runtime artifact or init obligation
Typical question:
- which live/runtime artifact or minimal init chain explains why repaired static views or offline replay are almost right but still untrustworthy?

Primary note:
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`

Possible next handoff:
- `topics/decrypted-artifact-to-first-consumer-workflow-note.md`
- `topics/native-interface-to-state-proof-workflow-note.md`
- `topics/mobile-signing-and-parameter-generation-workflows.md`
- `topics/integrity-check-to-tamper-consequence-workflow-note.md`

### F. Integrity logic -> first consequence-bearing tripwire
Typical question:
- what first reduced result or branch turns visible checks into real behavioral change?

Primary note:
- `topics/integrity-check-to-tamper-consequence-workflow-note.md`

Possible next handoff:
- `topics/environment-differential-diagnosis-workflow-note.md` when compare conditions still dominate trust
- `topics/attestation-verdict-to-policy-state-workflow-note.md` when the case is really a mobile verdict-to-policy problem
- `topics/native-interface-to-state-proof-workflow-note.md` when the tripwire has already reduced into an ordinary consequence consumer

## 5. The branch’s practical routing rule
When a case is clearly protected-runtime shaped, ask these in order:

1. **Is the current observation model itself failing or distorting the evidence?**
   - if yes, start with observation-topology selection
2. **Am I still stuck in protected execution churn?**
   - if yes, start with semantic-anchor or dispatcher/state-edge reduction
3. **Am I still stuck proving the post-unpack handoff?**
   - if yes, start with packed-stub -> OEP
4. **Do I already have a readable recovered artifact, but no ordinary consumer?**
   - if yes, start with decrypted-artifact -> first consumer
5. **Are static artifacts or offline replay close-but-wrong because one runtime artifact or init obligation is still missing?**
   - if yes, start with runtime-table / initialization-obligation recovery
6. **Are checks already visible, but the first behavior-changing consequence is still hidden?**
   - if yes, start with integrity-check -> tamper consequence

If more than one feels true, prefer the earliest boundary that still blocks later work.
That usually means:
- repair observation topology before overcommitting to one noisy hook plan
- resolve packed/bootstrap handoff before artifact-consumer proof
- resolve trace/dispatcher churn before claiming artifact semantics
- resolve runtime-artifact / init-obligation drift before rewriting core logic again
- resolve integrity result reduction before treating later degrade/decoy behavior as explained

## 6. What this branch is strongest at
This branch is currently strongest at practical notes for:
- choosing a better observation topology when direct observation itself is failing
- reducing virtualized or flattened execution into one semantic anchor or state edge
- turning stub-heavy startup into one trustworthy post-unpack handoff
- turning readable artifacts into one first ordinary consumer
- turning close-but-wrong replay into one smaller runtime-artifact or initialization-obligation target
- turning visible integrity logic into one consequence-bearing tripwire

That makes the branch good at cases where the main problem is not abstract taxonomy, but converting visible protection-related material into one quieter next object.

## 7. What this branch is still weaker at
This branch is still weaker than browser/mobile in some areas:
- it has fewer compact route guides and branch-level summaries
- it still relies more on practical notes than on a fully mature synthesis ladder
- anti-cheat / trusted-runtime / privilege-heavy subareas remain more lightly integrated
- there is still room for a later route-guide pass focused specifically on anti-instrumentation / anti-debug surface selection

That means the right near-term maintenance pattern is usually:
- branch-shape repair
- conservative navigation strengthening
- concrete workflow deepening only when a real operator gap appears

## 8. Common mistakes this guide prevents
This guide is meant to prevent several recurring branch-level mistakes:
- treating all protected-runtime cases as “just obfuscation”
- deepening one practical note without clarifying where it sits in the branch
- mistaking visible checks or visible loaders for solved handoffs
- creating more leaf pages when the real gap is branch routing
- drifting back into browser/mobile growth just because those areas already have denser source pressure

## 9. How this guide connects to the rest of the KB
Use this subtree when the case is best described as:
- active resistance, staged bootstrap, flattened/virtualized execution, integrity-sensitive behavior, or protected artifacts whose first reliable consumer is still unclear

Then route outward as soon as the case becomes ordinary enough:
- to `topics/native-semantic-anchor-stabilization-workflow-note.md` when code is readable but meaning is still unstable
- to `topics/native-interface-to-state-proof-workflow-note.md` when one representative route-to-consequence chain is now the real bottleneck
- to `topics/runtime-behavior-recovery.md` when broader evidence strategy is still the main issue
- to `topics/mobile-protected-runtime-subtree-guide.md` when the target is clearly mobile/platform-constrained rather than generic protected-runtime

## 10. Topic summary
This subtree guide turns the protected-runtime / deobfuscation practical branch into a clearer operator ladder.

The compact reading is:
- reposition observation when the current topology is the bottleneck
- anchor protected execution churn
- hand off out of packed startup
- prove the first ordinary consumer of recovered artifacts
- stabilize one truthful runtime artifact and one minimal init obligation when static views are still lying
- prove the first consequence-bearing integrity tripwire

That makes the branch easier to enter, easier to sequence, and less dependent on already knowing which leaf note to read first.
