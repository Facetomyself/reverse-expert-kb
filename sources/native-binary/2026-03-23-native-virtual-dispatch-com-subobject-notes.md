# 2026-03-23 — Native virtual-dispatch COM/subobject narrowing notes

Purpose:
- strengthen the native virtual-dispatch practical branch with a more concrete continuation around COM-style interface pointers, multiple-inheritance/subobject offsets, RTTI-assisted narrowing, and thunk/adjustor handling

## Why this pass was chosen
Recent autosync runs had already spent real external-search pressure on:
- exception / SEH boundaries
- COM CLSID hijack
- VEH dispatcher work
- protected-runtime streaming / replay seams
- WMI subscription consumer proof

That meant this run should not spend another slot on the same dense branches unless a blocking repair appeared.
The native desktop/server practical branch remained comparatively thinner in recent hours, especially around the question:
- once a vtable or COM-style slot call is visible, how should the operator reduce secondary-interface/subobject ambiguity into one concrete implementation proof?

This pass therefore aimed to deepen the **native virtual-dispatch implementation uncertainty** seam rather than polish top-level wording.

## Search shape used
Explicit multi-source search was attempted via:
- `search-layer` with `--source exa,tavily,grok`
- exploratory intent
- three queries around:
  - concrete implementation behind virtual calls
  - multiple inheritance / RTTI / subobject layout
  - COM interface-slot / QueryInterface / vtable workflow

Raw search trace saved at:
- `sources/native-binary/2026-03-23-native-virtual-dispatch-com-subobject-search-layer.txt`

## High-signal takeaways

### 1. The practical bottleneck is often not slot indexing, but proving **which subobject/interface pointer owns the slot**
Across COM and multiple-inheritance references, the recurring analyst error is not failing to recognize a vtable call.
It is misidentifying the supplying pointer.

Useful consequence:
- after dispatch-site recognition, the next explicit proof boundary should often be:
  - which retained interface pointer or adjusted subobject pointer is being used
  - what offset adjustment happened before the call
  - whether the slot belongs to the primary object base or a secondary embedded interface/base

### 2. QueryInterface and factory edges are stronger practical anchors than broad method-table naming
The COM-oriented material reinforced that the workflow should bias toward:
- locating `CoCreateInstance` / class-factory / provider creation
- identifying the IID requested or compared
- following the returned/retained interface pointer
- proving one later slot invocation through that retained pointer family

Useful consequence:
- for undocumented COM-like cases, the operator should prefer:
  - interface identity
  - retention site
  - one later slot-to-effect proof
rather than trying to fully name all methods first.

### 3. Multiple inheritance and COM secondary interfaces should be treated as the same practical narrowing family
Raymond Chen’s COM layout note, Babkin’s constructor/layout write-up, and RTTI/multiple-inheritance references all point to the same operator reality:
- a call can be made through a pointer that targets a non-primary region of the object
- pointer adjustments and thunks can make the decompiler look locally plausible while still assigning the wrong owner
- the trustworthy move is to prove the supplying base/subobject first, then narrow implementations within that family only

Useful consequence:
- the KB should state explicitly that:
  - secondary COM interfaces
  - multiple-inheritance subobjects
  - adjusted `this` thunks / interface-pointer shifts
should be treated as one recurring proof problem, not separate trivia buckets

### 4. RTTI is useful as a **candidate shrinker**, not as the stopping point
RTTI-heavy references were useful, but the practical value here is limited and specific:
- RTTI can reduce candidate families
- RTTI can expose class hierarchy and vtable neighborhoods
- RTTI can help confirm whether several candidate tables belong to one derived family

But RTTI does not replace:
- retained-pointer proof
- subobject ownership proof
- one concrete slot-to-effect chain

Useful consequence:
- the workflow should recommend RTTI only as a candidate-narrowing aid after the proof boundary has already been chosen

### 5. Thunks / adjustor layers should be treated as boundary markers, not analytic endpoints
The combined sources reinforce a recurring trap:
- analysts stop at CFG wrappers, import helpers, or adjustor thunks and treat them as “the implementation”
- in practice, those layers often only normalize the pointer or forward to the real override

Useful consequence:
- add an explicit rule:
  - if the slot lands in a thunk, capture what it adjusts and where it forwards
  - only treat it as final when it is itself the first effect-bearing body

## Concrete workflow change justified by this pass
Strengthen `topics/native-virtual-dispatch-slot-to-concrete-implementation-workflow-note.md` by making these practical moves more explicit:
- add a separate COM / multiple-inheritance pattern around **secondary interface or subobject ownership**
- explicitly frame RTTI as candidate narrowing, not workflow completion
- add an adjustor-thunk stop rule so the operator keeps pushing toward the first effect-bearing body

## Sources consulted
Primary grounding:
- ALSchwalm, “Reversing C++ Virtual Functions: Part 1” — <https://alschwalm.com/blog/static/2016/12/17/reversing-c-virtual-functions/>
- Dennis Babkin, “Reverse Engineering Virtual Functions Compiled With Visual Studio C++ Compiler” — <https://dennisbabkin.com/blog/?t=reverse-engineer-virtual-functions-vs-cpp-compiler-vtable-purecall-cfg>
- Raymond Chen, “The layout of a COM object” — <https://devblogs.microsoft.com/oldnewthing/20040205-00/?p=40733>
- Hex-Rays, “Igor’s tip of the week #93: COM reverse engineering and COM Helper” — <https://hex-rays.com/blog/igors-tip-of-the-week-93-com-reverse-engineering-and-com-helper>

Secondary / directional support from the multi-source search trace:
- Binary Ninja, “Enhancing COM Reverse Engineering in Binary Ninja 4.0” — <https://binary.ninja/2024/02/12/enhancing-com-reverse-engineering.html>
- OpenRCE, “Part II: Classes, Methods and RTTI” — <https://www.openrce.org/articles/full_view/23>
- Quarkslab, “Visual C++ RTTI Inspection” — <https://blog.quarkslab.com/visual-c-rtti-inspection.html>
- TopicSec, “Devil is Virtual: Reversing Virtual Inheritance in C++ Binaries” — <https://topicsec.github.io/posts/devil-is-virtual/>

## Confidence
- strong that this fills a real native practical gap
- moderate for ABI/compiler-specific details, which remain implementation-dependent
- intentionally conservative about universal layout claims; the durable lesson is the proof order, not one compiler’s exact structure
