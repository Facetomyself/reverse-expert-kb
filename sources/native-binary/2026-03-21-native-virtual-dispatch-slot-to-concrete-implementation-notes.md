# 2026-03-21 — Native virtual-dispatch slot to concrete implementation notes

Purpose:
- support a practical native workflow note for the recurring case where a visible virtual / COM-style call site is already known, but the analyst still has not proved which concrete slot implementation or object family actually carries the effect

## Why this seam matters
A common native stall happens after the analyst already has:
- readable decompilation
- one plausible object or interface family
- one visible indirect call of the form "load vptr / call slot" or COM-style interface invocation

But the analyst still cannot yet say:
- which concrete vtable family is active here
- which slot implementation is effect-bearing enough to trust
- whether the current object is a base/interface abstraction, a concrete implementation, or one of several sibling runtime types

This is not the earlier native problem of picking a broad route.
It is not the later async-native problem of proving which callback delivery matters after ownership is already known.
It is the narrower mid-branch problem of reducing one visible virtual-dispatch surface into one concrete implementation proof.

## External source takeaways

### 1. Virtual-call recovery is usually about narrowing runtime candidates, not fully devirtualizing every site
From ALSchwalm’s write-up on reversing C++ virtual functions:
- the useful immediate goal is often to determine which functions might be called at a particular site, not to pretend the runtime type is statically solved everywhere
- constructor-side vptr writes, vtable layout, and slot offsets provide the first trustworthy narrowing surface
- pure-virtual placeholders and inherited shared entries are practical filters, because some candidate tables are impossible or less informative

Practical consequence for the KB:
- the analyst should explicitly separate:
  - call-site recognition
  - candidate table / slot recovery
  - dynamic-type narrowing
  - one concrete implementation-to-effect proof
- stopping at “this is a vtable call” is too early

### 2. MSVC / COM-style cases often need object-layout and constructor overwrite reading, not just slot counting
From Dennis Babkin’s Visual Studio-focused write-up:
- constructor order and vftable overwrites reveal subobject layout and which base/derived table is live at different offsets
- multiple inheritance and separate subobject vptrs matter in practice, especially for COM-like shapes or interface-rich classes
- CFG / indirect-call wrappers can make novice analysis stop too early at the thunk instead of the real target-bearing table

Practical consequence:
- the operator should mark:
  - the object base used at the call site
  - the specific subobject offset that supplies the vptr
  - the constructor/initializer evidence showing which table becomes live there
- one wrong assumption about object base or subobject offset can misattribute the whole effect chain

### 3. COM recovery benefits from interface identity anchors and QueryInterface / factory edges
From Microsoft’s QueryInterface navigation page and search-returned COM reversing references:
- COM surfaces naturally separate interface negotiation from later high-performance use of the chosen contract
- interface identity, IID comparisons, class-factory creation, and returned interface pointers are often the practical bridge from abstract contract to later slot use
- for undocumented interfaces, QueryInterface callers, interface UUIDs, and returned pointer adjustments are stronger anchors than broad method-table naming attempts

Practical consequence:
- in COM-like cases, the next trustworthy move is often not “name every slot,” but:
  - prove which interface pointer is returned or retained
  - prove which slot index matters for the target effect
  - prove one later effect-bearing invocation through that retained interface pointer

### 4. Tooling and helper structures are useful only after the proof boundary is chosen
From search results around COM helper workflows and Binary Ninja COM improvements:
- helper plugins and structure-recovery aids can accelerate table labeling and interface reconstruction
- but they do not replace the core analytic choice of which slot, which table family, and which downstream effect to prove first

Practical consequence:
- the KB should frame helpers as acceleration, not as the workflow itself
- the workflow should remain centered on one slot-to-effect proof boundary

## Practical workflow shape supported by the sources
A compact operator sequence emerges:
1. recognize one virtual / COM-style dispatch site worth proving
2. recover the supplying object base, subobject offset, and slot index
3. enumerate the smallest realistic set of candidate tables / runtime types
4. eliminate impossible or weak candidates using constructor writes, pure-virtual placeholders, interface identity, or retained object evidence
5. prove one concrete slot implementation through one downstream state/effect edge
6. only then widen into sibling implementations, neighboring slots, or fuller class/interface reconstruction

## Strong stop rules
Good stopping point:
- one visible dispatch site has been reduced to one concrete implementation family and one effect-bearing consequence

Bad stopping points:
- “this is probably a vtable call”
- “the object seems COM-like”
- “the helper named some interfaces”
- “there are several candidate derived classes”
without a slot-to-effect proof

## Candidate page justified by this source pass
Create a practical native workflow note around:
- virtual-dispatch slot to concrete implementation proof

Why this page belongs:
- it is practical rather than taxonomic
- it fills a real native branch gap between interface-path proof and loader/service/async continuations
- it gives operators a case-driven answer when visible virtual dispatch is already known but concrete implementation ownership still blocks progress

## Sources consulted
- ALSchwalm, “Reversing C++ Virtual Functions: Part 1” — <https://alschwalm.com/blog/static/2016/12/17/reversing-c-virtual-functions/>
- Dennis Babkin, “Reverse Engineering Virtual Functions Compiled With Visual Studio C++ Compiler” — <https://dennisbabkin.com/blog/?t=reverse-engineer-virtual-functions-vs-cpp-compiler-vtable-purecall-cfg>
- Microsoft Learn, “QueryInterface Navigating in an Object” — <https://learn.microsoft.com/en-us/windows/win32/com/queryinterface--navigating-in-an-object>
- Search-layer results also surfaced supporting COM/interface-recovery references, including Hex-Rays COM helper and Binary Ninja COM workflow material; these were treated as directional support rather than primary grounding for claims in this note.

## Confidence
- strong for the workflow seam itself
- moderate for compiler/tool-specific details, which vary by ABI and implementation
- intentionally conservative about claiming full devirtualization; the emphasis is one concrete implementation proof, not universal static resolution
