# Native Practical Subtree Guide

Topic class: subtree guide
Ontology layers: native baseline practice branch, workflow routing, operator ladder
Maturity: structured-practical
Related pages:
- topics/native-binary-reversing-baseline.md
- topics/native-semantic-anchor-stabilization-workflow-note.md
- topics/native-interface-to-state-proof-workflow-note.md
- topics/native-virtual-dispatch-slot-to-concrete-implementation-workflow-note.md
- topics/native-plugin-loader-to-first-real-module-consumer-workflow-note.md
- topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md
- topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md
- topics/runtime-behavior-recovery.md

## 1. Why this guide exists
This guide exists because the KB’s native practical branch already has several useful workflow notes, but until now it has been easier to read as a small set of siblings than as a clear operator ladder.

The branch already had practical entry surfaces for:
- readable native code whose first trustworthy semantic anchor is still unstable
- plausible interface paths whose first consequence-bearing state edge is still unproved
- plugin/module loader paths whose first real loaded-module consumer is still unclear
- service/daemon control and worker-owned paths whose first behavior-changing consumer is still unclear
- async callback, completion, queue, or event-loop structure whose first behavior-changing consumer is still unclear

What was missing was the compact routing rule that answers:
- where should I start when a case is clearly native-baseline shaped?
- which note comes next after the current bottleneck is reduced?
- when am I still stabilizing meaning versus when am I proving one operational route versus one service-owned worker path versus one async consumer?

This page makes the branch read more like the malware, protocol, and protected-runtime practical subtrees:
- a branch entry surface
- a small set of recurring bottleneck families
- a compact ladder for turning readable native structure into one smaller trustworthy working map

## 2. Core claim
Native practical work is easiest to navigate when the analyst first classifies the current bottleneck into one of six recurring families:

1. **semantic-anchor instability**
   - code is readable enough to navigate, but names, types, signatures, object roles, or subsystem labels are still too slippery to trust
2. **interface-path overabundance**
   - one semantic anchor is stable enough, but several imports/strings/xrefs/callbacks/handlers still expose too many plausible routes and no one consequence-bearing path has been proved yet
3. **virtual-dispatch implementation uncertainty**
   - one route or object family is already plausible, but a visible vtable/interface-slot call still leaves several candidate runtime types, subobjects, or concrete implementations competing
4. **module-owner uncertainty**
   - one route or implementation family is plausible enough, but plugin/module loaders, export resolution, factory registration, or provider installation still leave several loaded components competing and the first real module consumer is still unclear
5. **service-owned worker uncertainty**
   - service/daemon entry, control handlers, command dispatchers, or worker launchers are visible enough to read, but the first worker-owned consumer that actually changes behavior is still unclear
6. **async ownership break**
   - one route or owner is already plausible, but direct call-graph reading breaks at registration, queue, completion, callback, or event-loop delivery boundaries and the first consequence-bearing consumer is still unclear

A thinner Windows-heavy reminder now worth preserving inside family 4 before jumping ahead to async work:
- in loader/import-heavy cases, delay-load helpers, forwarded exports, API-set-style indirection, or repeated `GetProcAddress` calls can make resolution mechanics look like the answer
- but the branch should separate **resolution truth** from **consumer truth** and keep reducing until one caller-side retained use, table slot, provider object, or later dispatch edge first makes the resolved target behaviorally relevant

A compact operator ladder for this branch is:

```text
choose the current native bottleneck
  -> reduce it to one smaller trustworthy object or route
  -> prove one consequence-bearing edge or downstream effect
  -> hand back one more reliable subsystem map
```

The subtree is strongest when read as:
- **anchor** one trustworthy semantic meaning
- **prove** one representative interface-to-state route
- **reduce** one visible virtual/interface dispatch into a concrete implementation
- **reduce** one plugin/module loader path into a real loaded-module consumer
- **reduce** one service/daemon dispatcher path into a real worker-owned consumer
- **deliver** one async callback or event-loop consumer chain

## 3. How to choose the right entry note
### Start with `native-semantic-anchor-stabilization-workflow-note`
Use:
- `topics/native-semantic-anchor-stabilization-workflow-note.md`

Start here when:
- pseudocode is readable enough to navigate
- names, recovered types, signatures, object roles, or subsystem labels still feel plausible but unproved
- the next bottleneck is choosing one trustworthy semantic anchor before broader relabeling or deeper proof work
- one narrow proof could collapse ambiguity across several nearby functions, fields, or helpers

Do **not** start here when:
- one semantic anchor is already trustworthy enough and the real problem is that several interface paths still compete
- the current ambiguity really lives at async delivery boundaries rather than local meaning
- the case is still dominated by protection churn, environment reconstruction, or protocol-state recovery instead of ordinary native interpretation

### Start with `native-interface-to-state-proof-workflow-note`
Use:
- `topics/native-interface-to-state-proof-workflow-note.md`

Start here when:
- one semantic anchor is already stable enough to navigate
- imports, strings, xrefs, callbacks, command handlers, parser entries, or dispatch shims expose several plausible operational routes
- the next bottleneck is proving one representative path from interface entry through one consequence-bearing state edge into one downstream effect
- the best next output is one grounded route, not a broader subsystem survey

Do **not** start here when:
- the first trustworthy semantic anchor is still missing
- direct call-graph reading is already broken mainly by queue/callback/event-loop delivery rather than by too many entry families
- the target is better framed as protocol parser-to-state work, malware stage-to-consequence proof, or protected-runtime reduction

### Start with `native-virtual-dispatch-slot-to-concrete-implementation-workflow-note`
Use:
- `topics/native-virtual-dispatch-slot-to-concrete-implementation-workflow-note.md`

Start here when:
- one semantic anchor and one route are already plausible enough that broad route choice is no longer the real bottleneck
- one visible indirect call clearly looks like vptr/vtable dispatch, COM-style interface-slot dispatch, or an equivalent table-mediated call
- several candidate runtime types, subobjects, interface families, or concrete implementations still compete
- the next useful output is one proved chain from retained object/interface family through one slot into one concrete implementation and one downstream effect

Do **not** start here when:
- the real bottleneck is still choosing the right interface family
- the earlier semantic-anchor problem is still unresolved
- the main uncertainty is still plugin/module ownership rather than concrete slot implementation
- the concrete implementation is already known and the remaining ambiguity now lives inside loader/provider ownership, service/worker ownership, or callback/event delivery

### Start with `native-plugin-loader-to-first-real-module-consumer-workflow-note`
Use:
- `topics/native-plugin-loader-to-first-real-module-consumer-workflow-note.md`

Start here when:
- one route or concrete implementation family is already plausible enough that the bottleneck is no longer broad route choice
- plugin/module loaders, manifest readers, export resolvers, factory registration, or provider installation paths are visible enough to study
- the main uncertainty is no longer “which broad subsystem?” but “which loaded component first becomes behaviorally real?”
- the next useful output is one proved chain from load decision through module/export/factory edge into one first real consumer

Do **not** start here when:
- the real bottleneck is still choosing the right interface family
- the earlier semantic-anchor problem is still unresolved
- the main uncertainty is still concrete virtual/interface-slot implementation rather than loaded-module ownership
- the case is still stalled at packed/bootstrap readiness rather than ordinary native module ownership
- the loaded-module owner is already known and the remaining uncertainty now lives inside callback or event delivery

### Start with `native-service-dispatcher-to-worker-owned-consumer-workflow-note`
Use:
- `topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md`

Start here when:
- one interface family, route, or loaded-module owner is already plausible enough that broad route choice is no longer the real bottleneck
- service/daemon entry, control handlers, command dispatchers, worker launchers, or retained service tasks are visible enough to study
- the main uncertainty is no longer choosing the route or loaded-module owner, but proving which service-owned worker path first changes later behavior
- the next useful output is one proved chain from service/bootstrap or command ingress through dispatcher reduction into one worker-owned consumer

Do **not** start here when:
- the real bottleneck is still choosing the right interface family
- the earlier semantic-anchor problem is still unresolved
- the module/plugin owner is still under-reduced
- the remaining uncertainty already lives mainly inside narrower callback or event-loop delivery rather than service/worker ownership

### Start with `native-callback-registration-to-event-loop-consumer-workflow-note`
Use:
- `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md`

Start here when:
- one interface family, route, loaded-module owner, or service-owned worker path is already plausible
- registrations, completions, callback tables, message pumps, observer lists, queues, or event-loop reducers are visible enough to study
- the main uncertainty is no longer choosing the route, module owner, or service-owned worker path, but proving which async delivery or callback consumer first changes later behavior
- the next useful output is one proved chain from event source or registration through dispatch reduction into one consequence-bearing consumer

Do **not** start here when:
- the real bottleneck is still choosing the right interface family
- the earlier semantic-anchor problem is still unresolved
- the module/plugin owner is still under-reduced
- the service/daemon worker-owned path is still under-reduced
- the case is mainly mobile/WebView, firmware/protocol, or protected-runtime shaped rather than ordinary native async ownership

## 4. Compact ladder across the branch
A useful way to read the branch is as five common bottleneck families that often chain into one another.

### A. Readable structure -> trustworthy semantic anchor
Typical question:
- which label, type, object role, signature, or subsystem meaning would most reduce nearby ambiguity if I could prove it against one real consequence?

Primary note:
- `topics/native-semantic-anchor-stabilization-workflow-note.md`

Possible next handoff:
- `topics/native-interface-to-state-proof-workflow-note.md`
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`

### B. Stable anchor -> representative interface-to-state proof
Typical question:
- which entry family, handler, parser, command path, or exported surface should I prove first so the subsystem becomes operationally trustworthy?

Primary note:
- `topics/native-interface-to-state-proof-workflow-note.md`

Possible next handoff:
- `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/malware-reporting-and-handoff-evidence-packaging-workflow-note.md`

### C. Plausible route -> virtual-dispatch implementation proof
Typical question:
- which concrete implementation behind this visible vtable or interface-slot call first changes later behavior in a way that makes the route trustworthy?

Primary note:
- `topics/native-virtual-dispatch-slot-to-concrete-implementation-workflow-note.md`

Possible next handoff:
- `topics/native-plugin-loader-to-first-real-module-consumer-workflow-note.md`
- `topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md`
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`

### D. Plausible route or implementation family -> loaded-module owner proof
Typical question:
- which loaded module, resolved export, factory product, or installed provider first changes later behavior in a way that makes the route or implementation family trustworthy?

Primary note:
- `topics/native-plugin-loader-to-first-real-module-consumer-workflow-note.md`

Possible next handoff:
- `topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md`
- `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md`
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`
- `topics/runtime-behavior-recovery.md`

### E. Plausible route, implementation family, or module owner -> service-owned worker proof
Typical question:
- which service-owned thread, queued task, worker routine, or retained task object first changes later behavior in a way that makes the route, implementation family, or module owner trustworthy?

Primary note:
- `topics/native-service-dispatcher-to-worker-owned-consumer-workflow-note.md`

Possible next handoff:
- `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md`
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`
- `topics/runtime-behavior-recovery.md`

### F. Plausible route, implementation family, module owner, or service-owned worker path -> async callback/event-loop consumer proof
Typical question:
- which posted task, delivered callback, completion, or event-loop consumer first changes later behavior in a way that makes the route, implementation family, owner, or service-owned worker path trustworthy?

Primary note:
- `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md`

Common thinner continuation:
- `topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md` when the async-ownership break has already narrowed specifically into posted work, completion packets, thread-pool callbacks, or queue-dequeue ownership rather than broad callback-plumbing truth
  - preserve extra stop rules there: do not infer dequeue/consumer order from submit order alone in IOCP cases, do not flatten posted control packets into I/O-owned completions, do not treat `GetQueuedCompletionStatus(FALSE)` with non-NULL `lpOverlapped` as “no delivery happened,” do not collapse IOCP `completion key` family identity into `OVERLAPPED*` owner recovery, do not assume `TP_IO` callbacks must fire for immediately successful overlapped operations under `FILE_SKIP_COMPLETION_PORT_ON_SUCCESS`, and do not flatten libuv worker-side `work_cb` ownership into loop-thread `after_work_cb` or `uv_async_send()` ownership
- `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md` when the async-ownership break has already narrowed specifically into Win32 message-pump / subclass, Qt signal-slot ownership, or macOS Cocoa / XPC / dispatch delivery ownership and the real bottleneck is one per-instance, per-connection, or per-responder first consumer rather than broad callback-plumbing truth
  - preserve extra stop rules there: do not flatten shared subclass wrappers into one owner; in Win32 helper-based subclass cases recover the exact `HWND` plus callback+subclass-ID pair and instance-local reference data; do not flatten Qt `AutoConnection` / queued delivery into generic “signal found” proof without proving receiver thread affinity and actual delivery mode; and do not flatten `NSApplication sendEvent:`, XPC proxy setup, or dispatch-source registration into automatic consumer proof

Possible next handoff:
- `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md`
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`
- `topics/runtime-behavior-recovery.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`

Routing reminder:
- leave broad async callback/event-loop work once one consequence-bearing consumer is already good enough and the real bottleneck becomes reverse-causality, broader runtime-evidence strategy, or one narrower output-side continuation

## 5. The branch’s practical routing rule
When a case is clearly native-baseline shaped, ask these in order:

1. **Is code readable, but the first trustworthy local meaning still unstable?**
   - if yes, start with semantic-anchor stabilization
2. **Is one semantic anchor stable enough, but several entry or handler routes still compete?**
   - if yes, start with interface-to-state proof
3. **Is one route or object family already plausible, but a visible vtable/interface-slot call still leaves the concrete implementation unclear?**
   - if yes, continue into virtual-dispatch slot / concrete-implementation proof
4. **Is one route or implementation family plausible enough, but plugin/module loaders or provider install paths still leave the real owner unclear?**
   - if yes, continue into loaded-module owner proof
5. **Is one route, implementation family, or module owner already plausible, but service/daemon control or worker ownership is still under-reduced?**
   - if yes, continue into service-dispatcher / worker-owned-consumer proof
6. **Is one route, implementation family, module owner, or service-owned worker path already plausible, but ownership now breaks at queue/callback/event-loop delivery?**
   - if yes, continue into callback-consumer proof

If more than one feels true, prefer the earliest boundary that still blocks later work.
That usually means:
- stabilize one semantic anchor before comparing many interface paths
- leave broad semantic-anchor work once one anchor is already good enough and the real bottleneck becomes choosing one representative interface route
- prove one representative interface route before reducing visible virtual/interface-slot dispatch into one concrete implementation
- prove one concrete implementation before reducing loader/provider ambiguity
- prove one loaded-module owner before widening into service/daemon worker ambiguity
- prove one service-owned worker path before mapping a whole event framework
- prove one consequence-bearing consumer before cataloging sibling callbacks or neighboring handlers
- leave broad async callback/event-loop work once one consequence-bearing consumer is already good enough and the real bottleneck becomes reverse-causality, broader runtime-evidence strategy, or one narrower output-side continuation

## 6. What this branch is strongest at
This branch is currently strongest at practical notes for:
- turning readable but semantically slippery native structure into one trustworthy anchor
- turning several plausible interface paths into one proved state/effect chain
- turning visible vtable/interface-slot dispatch into one concrete implementation proof
- turning visible plugin/module loader structure into one first real module consumer proof
- turning visible service/daemon control structure into one first worker-owned consumer proof
- turning visible async framework structure into one consequence-bearing consumer proof

That makes the branch good at cases where the main problem is not broad taxonomy or missing visibility, but choosing one proof-worthy reduction step inside a mostly readable native target.

## 7. What this branch is still weaker at
This branch is still weaker than browser/mobile in some areas:
- it has had less explicit subtree-level routing until now
- Windows/Linux/macOS-specific operator differences are still lightly integrated
- it still relies more on workflow notes than on a denser native synthesis stack
- GUI message-pump / subclass, Qt signal-slot ownership, and a first macOS Cocoa/XPC/dispatch stop rule now have a narrower continuation page, but other OS-specific service/daemon variants and further desktop-framework splits are still lightly integrated

That means the right near-term maintenance pattern is usually:
- branch-shape repair
- conservative navigation strengthening
- concrete workflow deepening only when a real native operator gap appears

## 8. Common mistakes this guide prevents
This guide is meant to prevent several recurring branch-level mistakes:
- broad relabeling before one semantic anchor has survived proof pressure
- jumping into async callback mapping while the real bottleneck is still choosing the right interface family or proving one concrete slot implementation
- treating the native practical notes as flat parallel choices rather than a common progression with narrower handoff points
- widening subsystem coverage before one consequence-bearing chain is grounded
- drifting toward broader browser/mobile/protected-runtime work just because those branches already have denser source pressure

## 9. How this guide connects to the rest of the KB
Use this subtree when the case is best described as:
- a relatively ordinary native binary where code is readable enough to navigate, but the current bottleneck is still choosing one trustworthy anchor, one representative route, or one consequence-bearing async consumer

Then route outward as soon as the case becomes more specifically shaped:
- to `topics/runtime-behavior-recovery.md` when broader observability or proof strategy is still the main issue
- to `topics/causal-write-and-reverse-causality-localization-workflow-note.md` when one late effect is already visible and the real need is backward localization
- to `topics/protocol-state-and-message-recovery.md` when the real object has become protocol-state or parser-state recovery
- to `topics/malware-practical-subtree-guide.md` when the case is operationally malware-shaped rather than baseline-native
- to `topics/protected-runtime-practical-subtree-guide.md` when resistance, packing, or integrity logic becomes the real branch entry problem

## 10. Topic summary
This subtree guide turns the native practical branch into a clearer operator ladder.

The compact reading is:
- anchor one trustworthy semantic meaning
- prove one representative interface-to-state route
- reduce one visible virtual/interface dispatch into a concrete implementation
- reduce one plugin/module loader path into a real owner
- reduce one service/daemon dispatcher path into a real worker-owned consumer
- prove one async callback or event-loop consumer chain

That makes the branch easier to enter, easier to sequence, and less dependent on already knowing which native workflow note to read first.
