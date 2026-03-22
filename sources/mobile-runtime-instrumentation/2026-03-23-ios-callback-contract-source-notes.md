# 2026-03-23 iOS callback landing / first runtime-backed contract notes

## Scope
External-research support note for a reverse-KB autosync run targeting a thinner iOS practical seam:
- callback/block landing is already plausible
- broad owner search is no longer the cheapest next move
- replay/policy claims are still too strong because the first trustworthy runtime contract is not frozen yet

The goal is not a broad PAC survey.
The goal is to support a practical rule for when to stop widening the callback search and instead freeze the first runtime-backed block contract.

## Mode
external-research-driven

## Search shape
Search was run through `search-layer` with explicit multi-source selection:
- `--source exa,tavily,grok`

Queries:
1. `iOS arm64e block callback signature recovery reverse engineering Block ABI invoke landing`
2. `dyld shared cache arm64e callback dispatch reverse engineering runtime landing block signature`
3. `Objective-C block ABI signature invoke reverse engineering iOS callback arm64e`

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
- none at invocation time

Endpoints used on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Search transcript:
- `sources/mobile-runtime-instrumentation/2026-03-23-ios-callback-contract-search-layer.txt`

## High-signal sources actually used

### 1. Clang Block ABI documentation
- URL: <https://clang.llvm.org/docs/Block-ABI-Apple.html>

Why it mattered:
- gives the most concrete source-backed reminder that a block is not just a vague callback token
- the block layout explicitly contains an `invoke` pointer and, when flags support it, a signature field in the descriptor
- this supports a practical distinction between:
  - seeing a block object
  - proving the invoke landing
  - recovering a usable signature contract

KB takeaway:
- when a block family is already plausible, the first good proof object is often the first runtime-backed contract composed of:
  - one concrete block object family
  - one truthful invoke landing
  - one recovered or constrained signature shape
- this is stronger than continuing to widen owner search across nearby wrappers

Caution:
- the spec itself says the signature field is not always populated
- so the operator rule must stay conservative: prefer signature recovery when present, not assume every block yields a perfect contract

### 2. Clang pointer-authentication documentation
- URL: <https://clang.llvm.org/docs/PointerAuthentication.html>

Why it mattered:
- gives a useful practical reminder that arm64e/PAC is about signed pointers plus discriminators/context, not just a generic crash aura
- the tooling-relevant takeaway is that authentication context matters, and `strip`-style or purely raw-pointer reasoning is not the same as proving a truthful callable path

KB takeaway:
- when a callback path is close but still late-failing, keep the possibility that the family is right but the authenticated pointer/context pair is wrong
- this reinforces the stop rule: once one runtime-backed contract exists, do not reopen broad owner search by default; first classify whether the remaining failure is actually context/materialization/init drift

Caution:
- this source is language/ABI guidance, not a reverse-engineering cookbook
- used here only to support conservative workflow framing

### 3. `ipsw` dyld shared cache guide
- URL: <https://blacktop.github.io/ipsw/docs/guides/dyld/>

Why it mattered:
- reinforces that modern iOS system truth often lives in the dyld shared cache
- explicitly shows arm64e cache structure, extraction, and symbol/ObjC surfacing options that affect whether callback-adjacent code views are honest enough

KB takeaway:
- before turning a callback-looking edge into a strong claim, freeze the cache/image truth surface
- a block contract should be considered runtime-backed only if the static/dyld view is coherent enough that the alleged invoke site is not just an extraction/symbolization artifact

Caution:
- this is tooling/workflow guidance, not direct proof of any single callback family
- used to support the code-view-truth prerequisite for callback proof

### 4. Everett LLDB block-signature note
- URL: <https://everettjf.github.io/2020/02/11/print-block-in-lldb/>

Why it mattered:
- gives an operator-facing method for turning `CDUnknownBlockType`-style vagueness into an actual runtime-visible parameter shape
- especially useful at the exact seam the KB needed: callback family plausible, but contract still too vague to trust replay/policy claims

KB takeaway:
- if the visible block is still only a placeholder, recovering the runtime-visible signature can be a better next proof object than adding more hooks around wrappers
- this supports preserving a specific practical stop rule:
  - stop broad owner/callback widening once one block family is plausible
  - freeze the first runtime-backed block contract instead

Caution:
- older article, not arm64e-specific by itself
- used for workflow value, not as a full modern ABI reference

## Practical synthesis for the KB
The narrow durable claim supported by this run is:
- once a modern iOS case has already narrowed into one plausible block/callback family, the next useful proof object is often the **first runtime-backed block contract**, not more broad owner search

That contract should mean:
- one plausible block family
- one dyld/cache-truthful invoke landing
- one runtime-visible or tightly constrained signature shape
- one downstream effect worth handing off

This lets the analyst classify the remaining uncertainty more honestly:
- wrong family
- right family, wrong context/materialization
- lying code view
- replay-close missing obligation

## What this run deliberately did not claim
- that every iOS callback must be solved through block-signature recovery
- that every block descriptor exposes a readable signature in practice
- that PAC theory alone explains callback failures
- that finding one invoke pointer is the same thing as proving downstream policy ownership

## Best canonical landing spot
These notes best support strengthening:
- `topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md`

And indirectly clarify handoff to:
- `topics/ios-mitigation-aware-replay-repair-workflow-note.md`
- `topics/ios-result-callback-to-policy-state-workflow-note.md`

## Bottom line
The practical iOS gap here is no longer “find more callback-shaped things.”
It is “freeze the first runtime-backed block contract, then decide whether the remaining failure is contract truth, context/materialization, or downstream consequence.”
