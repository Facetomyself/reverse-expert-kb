# Reverse KB Autosync Run Report — 2026-03-21 19:16 Asia/Shanghai

Mode: external-research-driven

## Scope this run
This run intentionally avoided another internal-only native branch wording/count/index sync.
Recent same-day native maintenance had already improved branch routing and added service-dispatcher / worker-owned-consumer coverage, so this pass prioritized a real external research attempt on a still-practical native seam that remained underfed:

- native desktop/server practical branch
- specifically the gap between:
  - representative interface-to-state proof, and
  - later loader / service / async continuations
- target addition: **virtual-dispatch slot to concrete implementation proof**

Chosen bottleneck:
- a visible virtual / COM-style slot call is already known
- one route or object family is already plausible
- but the analyst still cannot yet prove which concrete implementation behind that slot actually carries the effect

## New findings
### 1. The native branch had a real mid-ladder gap
The KB already covered:
- semantic-anchor stabilization
- representative interface-path proof
- plugin/module-owner reduction
- service-owned worker reduction
- async callback / event-loop consumer proof

But it still skipped a very practical middle rung:
- visible vtable / interface-slot dispatch with unresolved concrete implementation ownership

That gap matters because many native cases do not jump directly from “one route is plausible” to “module owner is now the bottleneck.”
They often stall at:
- wrong subobject / base-offset assumptions
- several candidate runtime types
- COM/interface pointer retention without one proved effect-bearing slot
- thunk/CFG layers that make analysts stop before the real implementation body

### 2. External sources support a workflow centered on one slot-to-effect proof
The source pass consistently reinforced that the useful next target is not full devirtualization or whole-hierarchy reconstruction.
The useful next target is:
- one visible dispatch site
- one supplying object base / subobject or retained interface pointer
- one narrowed candidate table / type family
- one concrete implementation body
- one downstream effect-bearing consequence

### 3. COM-like cases benefit from interface-negotiation anchors
The source pass also reinforced that for COM-style targets the practical bridge is often:
- factory or object-acquisition edge
- `QueryInterface` / interface-identity anchor
- retained interface pointer
- one slot index
- one later effect

That is often stronger than trying to broadly name every interface method first.

## Sources consulted
Primary retained sources:
- <https://alschwalm.com/blog/static/2016/12/17/reversing-c-virtual-functions/>
- <https://dennisbabkin.com/blog/?t=reverse-engineer-virtual-functions-vs-cpp-compiler-vtable-purecall-cfg>
- <https://learn.microsoft.com/en-us/windows/win32/com/queryinterface--navigating-in-an-object>

Additional search-returned supporting sources considered directionally:
- <https://hex-rays.com/blog/igors-tip-of-the-week-93-com-reverse-engineering-and-com-helper>
- <https://binary.ninja/2024/02/12/enhancing-com-reverse-engineering.html>
- <https://stackoverflow.com/questions/3527440/decyphering-undocumented-com-interfaces>

Conservative evidence note:
- the retained synthesis was grounded primarily in the first three sources above
- helper/plugin/tooling references were used as supporting direction only, not as the main justification for the new workflow note

## Reflections / synthesis
The practical lesson from this run is that visible virtual dispatch deserves its own stop point in the native ladder.

Without that rung, analysts are too likely to do one of two bad things:
- stay abstract and keep cataloging classes, interfaces, or helper-produced structures without proving one implementation
- skip too early into module-owner / async continuations even though the concrete implementation behind the visible slot is still unresolved

The resulting workflow note therefore separates:
- dispatch-site recognition
- object-base / subobject proof
- candidate-table narrowing
- concrete implementation proof
- proof-of-effect

That separation is what keeps the branch practical.

## Candidate topic pages to create or improve
Created this run:
- `topics/native-virtual-dispatch-slot-to-concrete-implementation-workflow-note.md`

Improved this run:
- `topics/native-practical-subtree-guide.md`
- `topics/native-binary-reversing-baseline.md`
- `index.md`

Likely future follow-ons:
- a narrower case-driven note for COM factory / `QueryInterface` pointer-retention proof in sparse-name Windows targets
- a practical note for multiple-inheritance / subobject-offset misattribution traps
- a continuation page for thunk/CFG-heavy indirect-call surfaces where the guard layer obscures the true slot-bearing implementation

## Next-step research directions
Promising next native follow-ups now include:
- one concrete scenario page for COM-like undocumented interface recovery where one IID/slot pair must be tied to one file/network/state effect
- one case-driven continuation around subobject-offset and pointer-adjustment proof in multiple-inheritance binaries
- one workflow note around narrowing from shared implementation families to one environment- or feature-gated concrete owner when the slot body itself remains partially shared

## Concrete scenario notes or actionable tactics added this run
Added one source note and one workflow note that preserve these operator tactics:
- pick one visible dispatch site, not the whole hierarchy
- prove which object base or subobject supplies the table pointer
- use constructor writes, retained pointers, factory output, pure-virtual placeholders, and interface identity to narrow candidates
- prefer one retained interface/object family over broad class inventory
- stop only after one concrete implementation-to-effect chain is grounded

## Direction review
This run stayed aligned with the KB’s current direction rules:
- practical over abstract
- case-driven over taxonomy-driven
- branch-balance over dense-branch polishing
- one smaller trustworthy proof boundary over broad hierarchy narration

This was not a wording-only pass.
It produced:
- one new source-backed practical workflow note
- one new source note
- branch routing changes so the new native rung is actually visible and reusable

## Branch-balance review
### Before this run
The native branch already had better coverage for:
- semantic stabilization
- interface-path proof
- loader/provider ownership
- service/worker ownership
- async callback/event delivery

But it was thinner on:
- the intermediate “visible virtual dispatch, unresolved concrete implementation” seam

Recent runs also showed a drift risk toward internal branch-shape maintenance without enough source-backed practical additions.
This run directly countered that drift.

### After this run
The native branch now reads more cleanly as a six-family practical ladder:
- semantic-anchor instability
- interface-path overabundance
- virtual-dispatch implementation uncertainty
- module-owner uncertainty
- service-owned worker uncertainty
- async ownership break

That should reduce pressure to keep patching nearby notes indirectly when the real missing object is one concrete slot-to-effect proof.

## Search audit
Search sources requested: `exa,tavily,grok`

Search sources succeeded: `exa,tavily,grok`

Search sources failed: `none`

Search invocation policy used:
- explicit multi-source search via `search-layer --source exa,tavily,grok`
- no implicit/default source selection

Exa endpoint: `http://158.178.236.241:7860`
Tavily endpoint: `http://proxy.zhangxuemin.work:9874/api`
Grok endpoint: `http://proxy.zhangxuemin.work:8000/v1`

Queries used:
- `c++ reverse engineering virtual dispatch implementation recovery workflow`
- `reverse engineering vtable call target localization workflow`
- `binary reversing COM interface virtual call implementation workflow`

Conservative note:
- the search process did show Grok timeout noise during some sub-requests, but the overall explicit multi-source search invocation still returned usable results from all three requested sources and the run retained only the higher-signal references above
- one direct fetch target returned 403 and was not used as a primary source

## Files changed in this run
- `research/reverse-expert-kb/topics/native-virtual-dispatch-slot-to-concrete-implementation-workflow-note.md`
- `research/reverse-expert-kb/sources/native-binary/2026-03-21-native-virtual-dispatch-slot-to-concrete-implementation-notes.md`
- `research/reverse-expert-kb/topics/native-practical-subtree-guide.md`
- `research/reverse-expert-kb/topics/native-binary-reversing-baseline.md`
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/runs/2026-03-21-1916-native-virtual-dispatch-implementation-autosync.md`

## Commit / sync intent
If the working tree is clean enough for a focused KB commit:
- commit the reverse KB changes
- run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
- preserve the run as committed branch state rather than local-only drift
