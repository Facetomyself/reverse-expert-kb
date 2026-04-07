# Encoded-branch and obfuscated-next-state recovery notes

Date: 2026-04-08
Branch target: deobfuscation practice / flattened-control-flow continuation
Purpose: preserve a source-backed operator refinement for flattened-control-flow cases where the dispatcher is already known but the next-state relation is still hidden behind encoded branches or obfuscated `next`-variable handling.

## Research intent
Strengthen the existing opaque-predicate / computed-next-state workflow note with a narrower recovery rule for encoded-branch and obfuscated-next variants.

The practical operator problem is not merely:
- is there flattening here?

It is:
- which smaller value family is stable enough to carry one trustworthy successor relation back to dispatcher re-entry when the visible branch instruction is still noisy?

## Search artifact
Raw multi-source search artifact:
- `sources/deobfuscation/2026-04-08-0551-deobf-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Exa returned usable Tigress, Quarkslab, and tooling surfaces
- Tavily returned usable Tigress and supporting practical workflow surfaces
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` through the configured proxy path

## Retained sources
1. Tigress documentation — control-flow flattening
   - <https://tigress.cs.arizona.edu/transformPage/docs/flatten/index.html>
2. Quarkslab — recovering an OLLVM-protected program
   - <https://blog.quarkslab.com/deobfuscation-recovering-an-ollvm-protected-program.html>
3. Practical tooling surfaces retained conservatively as support for workflow shape, not as sole truth
   - Miasm/MODeflattener discussion surfaces
   - Binary Ninja / unflattener workflow surfaces
   - eShard D810 unflattening discussion surface

## High-signal retained findings

### 1. Tigress explicitly preserves obfuscated-next and encoded-branch variants as part of flattening, not as a separate unrelated problem
The Tigress flattening documentation explicitly states that:
- the `next` variable can be obfuscated using opaque predicates
- conditional branches can be encoded in several different ways

Practical consequence:
- once the dispatcher is already known, encoded-branch and obfuscated-next cases should still be treated first as **next-state recovery** problems
- do not automatically widen the task into a separate full-program deobfuscation campaign

### 2. The visible branch instruction is often not the first truthful successor object
Across the retained workflow/tooling surfaces, the recurring practical pattern is:
- dispatcher known
- state carrier present
- noisy branch or helper structure still obscures successor extraction
- workable recovery succeeds by reducing one state-carrier family or one successor-edge family first

Practical consequence:
- the first trustworthy object may be the normalized `next` carrier, helper output, or reduced index family
- the branch instruction the decompiler emphasizes may still be only wrapper noise

### 3. One successor edge or one reduced state family is often enough to restart progress
Quarkslab-style and tool-driven unflattening discussions consistently support the narrower operator rule:
- recover one trustworthy state mapping or one successor relation first
- then rewrite, simplify, or continue cleanup around that proof

Practical consequence:
- do not block on full CFG prettification
- stop once one edge, one two-way split, or one normalized next-carrier is strong enough to guide the next static or dynamic move

## Practical synthesis worth preserving canonically
The compact rule for this seam is:

```text
dispatcher recognized
  != next-carrier normalized
  != trustworthy successor relation
  != full deobfuscation required
```

Where:
1. **dispatcher recognized**
   - flattening / dispatcher family is already obvious
   - still only branch-family / control-structure truth

2. **next-carrier normalized**
   - one helper output, encoded `next` value, compare family, or table index is reduced into a stable successor-bearing object
   - this is often the real first bridge object in encoded-branch cases

3. **trustworthy successor relation**
   - one OBB/state or state/successor edge is now strong enough to predict later control flow
   - this is the real success boundary for the continuation note

4. **full deobfuscation required**
   - broader predicate cleanup, CFG beautification, or IL repair may still be useful later
   - but they are optional after one edge is already trustworthy enough to move the case forward

## Best KB use of this material
This material is best used to sharpen the existing practical workflow note for opaque predicates and computed next-state recovery.
It should not become a broad new survey page.

The operator-facing value is:
- do not overclaim from dispatcher recognition alone
- do not overfocus on the decompiler’s prettiest branch instruction
- prefer the last comparatively stable next-carrier before dispatcher re-entry
- stop once one trustworthy successor edge exists, then decide whether further cleanup is worth the cost

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source result set.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked; its failure is recorded clearly.
