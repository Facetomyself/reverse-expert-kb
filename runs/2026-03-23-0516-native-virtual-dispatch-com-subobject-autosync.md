# 2026-03-23 05:16 — Native virtual-dispatch COM/subobject autosync

Mode: external-research-driven

## Summary
This run deliberately avoided another dense-branch internal sync and instead spent the slot on a thinner native practical seam: reducing visible virtual / COM-style dispatch into one concrete implementation when secondary interfaces, subobject offsets, RTTI hints, or thunks still blur ownership.

Material changes this run:
- added a new source-backed native note on COM/subobject narrowing:
  - `sources/native-binary/2026-03-23-native-virtual-dispatch-com-subobject-notes.md`
- archived the explicit three-source search trace:
  - `sources/native-binary/2026-03-23-native-virtual-dispatch-com-subobject-search-layer.txt`
- materially extended the practical native dispatch workflow note:
  - `topics/native-virtual-dispatch-slot-to-concrete-implementation-workflow-note.md`

## Direction review
Recent external-research-driven runs had already pushed:
- exception / SEH boundaries
- COM CLSID hijack
- VEH dispatcher work
- protected-runtime streaming / replay seams
- WMI permanent subscription consumer proof

That meant continuing to spend this slot on protected-runtime or malware-shaped micro-polish would risk branch imbalance.
This run therefore biased toward the underfed native desktop/server practical branch, in line with the anti-stagnation rule.

The practical direction maintained here is still:
- case-driven
- proof-boundary first
- concrete workflow deepening over abstract taxonomy growth

## Branch-balance review
Heavier recent pressure:
- protected-runtime practical branch
- Windows persistence / malware-leaning branches

Lighter recent pressure:
- native baseline practical branch, especially the mid-branch seam between:
  - interface-path proof
  - visible vtable / COM slot dispatch
  - later loader / service / callback continuations

Choice made for this run:
- strengthen the native **virtual-dispatch implementation uncertainty** step rather than do another top-level wording/index/family-count sync

## External research performed
Explicit multi-source search was attempted, as required, using:
- `search-layer`
- `--source exa,tavily,grok`
- exploratory mode / intent
- three focused queries around concrete implementation recovery, multiple inheritance / RTTI, and COM interface-slot workflows

Primary fetched reading used for synthesis:
- ALSchwalm — C++ virtual-call narrowing and candidate-table reduction
- Dennis Babkin — MSVC object layout, constructor overwrite order, multi-base/subobject realities, CFG-adjacent dispatch reading
- Raymond Chen — COM object layout and secondary-interface pointer framing
- Hex-Rays COM helper note — practical IID/interface/vtable labeling workflow support

Secondary / directional support captured from search results:
- Binary Ninja COM workflow improvements
- OpenRCE / Quarkslab RTTI material
- virtual inheritance / adjustor-thunk-adjacent references surfaced by search

## What changed in the KB
### 1. Added a concrete source note for COM/subobject narrowing
Created:
- `sources/native-binary/2026-03-23-native-virtual-dispatch-com-subobject-notes.md`

This note records the durable workflow lesson:
- the bottleneck is often not recognizing a virtual call, but proving which retained interface pointer or subobject actually owns the slot

### 2. Archived the explicit search trace
Saved:
- `sources/native-binary/2026-03-23-native-virtual-dispatch-com-subobject-search-layer.txt`

This preserves the exact three-source attempt and gives future runs a concrete audit trail instead of a vague “searched the web” claim.

### 3. Extended the native virtual-dispatch workflow note with a more practical continuation
Updated:
- `topics/native-virtual-dispatch-slot-to-concrete-implementation-workflow-note.md`

Material improvements:
- added a dedicated scenario pattern for **secondary interface / subobject ownership confusion**
- upgraded thunk handling from generic wrapper awareness to a practical rule:
  - capture what the thunk adjusts
  - keep going unless the thunk itself is the first effect-bearing body
- expanded the source grounding section to include the new COM/subobject note and explicit COM layout framing

## Practical synthesis
The useful new operational stance is:
1. recognize the slot call
2. prove which interface pointer or subobject region supplies it
3. use RTTI / constructor writes / `QueryInterface` / factory evidence only to shrink candidates
4. treat thunks as adjustment boundaries unless they themselves carry the first effect
5. stop only after one implementation-to-effect chain is grounded

This is a real practical continuation for the native branch, not just canonical wording cleanup.

## Why this run was not KB-internal-only
No external research avoidance happened here.
A real multi-source pass was attempted and succeeded, and the resulting KB change is source-backed, workflow-shaped, and branch-deepening.

## Search audit
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- exa
- tavily
- grok

Failed sources:
- none

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Artifacts:
- search trace: `sources/native-binary/2026-03-23-native-virtual-dispatch-com-subobject-search-layer.txt`

## Files changed
- `topics/native-virtual-dispatch-slot-to-concrete-implementation-workflow-note.md`
- `sources/native-binary/2026-03-23-native-virtual-dispatch-com-subobject-notes.md`
- `sources/native-binary/2026-03-23-native-virtual-dispatch-com-subobject-search-layer.txt`
- `runs/2026-03-23-0516-native-virtual-dispatch-com-subobject-autosync.md`

## Commit / sync intent
If KB diffs remain limited to this run’s reverse-KB files, commit them and then run:
- `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

## Next likely continuations
Good next native follow-ons if branch balance still permits later:
- a thinner native note on adjustor-thunk / `this`-correction proof boundaries
- a native continuation specifically for RTTI-assisted candidate shrink without hierarchy overfitting
- a narrower GUI/service handoff only if a real case-driven source pass justifies it
