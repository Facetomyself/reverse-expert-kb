# Protected-runtime copied-code branch inflation -> trustworthy successor split notes

Date: 2026-04-14
Branch target: protected-runtime deobfuscation / copied-code branch-inflation continuation
Purpose: preserve a source-backed operator refinement for the case where one normalized next-carrier already exists, but copied-code / question-opaque branch inflation still hides which successor split is real enough to trust.

## Search artifact
Raw multi-source search artifact:
- `sources/protected-runtime/2026-04-14-0450-copied-code-successor-split-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed source behavior for this run:
- Exa returned usable Tigress, Binary Ninja, and Miasm-oriented surfaces
- Tavily returned overlapping useful Tigress, Binary Ninja, angr, and MODeflattener surfaces
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` errors through the configured proxy path

## Retained source anchors
1. Tigress flattening documentation
   - `https://tigress.cs.arizona.edu/transformPage/docs/flatten/index.html`
2. Tigress AddOpaque documentation
   - `https://tigress.cs.arizona.edu/transformPage/docs/addOpaque/index.html`
3. Binary Ninja automated opaque-predicate removal
   - `https://binary.ninja/2017/10/01/automated-opaque-predicate-removal.html`
4. d0minik Binary Ninja control-flow unflattening write-up
   - `https://d0minik.me/posts/cff/`
5. MODeflattener / Miasm OLLVM deflattener write-up
   - `https://mrt4ntr4.github.io/MODeflattener/`
6. angr symbolic-execution documentation
   - `https://docs.angr.io/en/latest/core-concepts/symbolic.html`

## High-signal retained findings

### 1. Tigress makes copied-code branch inflation explicit, not hypothetical
The flattening docs keep three operator-relevant levers separate:
- dispatch form
- next-variable obfuscation via `--FlattenObfuscateNext`
- conditional-branch encoding via `--FlattenConditionalKinds=branch|compute|flag`

The AddOpaque docs make the second practical seam explicit:
- `--AddOpaqueKinds=question` can split one real statement into an original-vs-copy branch family
- `--AddOpaqueObfuscate=true` lightly obfuscates copied code in one branch
- split kinds such as `block`, `deep`, `recursive`, and `inside` affect where the copied-code branch family appears

Operator consequence:
- once one next-carrier is already recovered, visible branch width can still be lying because the branch family may be copied-code inflation rather than the real successor split
- a copied arm being large or obfuscated is weaker than proving that its condition actually owns different successor values

### 2. Binary Ninja supports constant-wrapper cleanup, but also tells you where that stops
The Binary Ninja MLIL/data-flow workflow is useful because it shows a robust way to remove branches whose condition is already constant at the IL level.
It also records its own limits:
- loops can block this style of cleanup
- writable segments weaken constant propagation assumptions
- unmodeled data sources break the inference chain

Operator consequence:
- patching a constant wrapper branch is real progress
- but it is not the same thing as proving that a still-conditional copied-code branch family carries a trustworthy true/false successor split
- use constant-branch cleanup as noise reduction first, not as proof that the remaining split is already understood

### 3. State-carrier recovery and split ownership are separable steps
The d0minik unflattening write-up keeps these steps separate in a practically useful way:
- identify the state variable / dependency family
- build state-to-OBB mappings from compare structure
- when retaining control-flow, check whether the relevant branch actually depends on the state-variable dependency family

Operator consequence:
- after one normalized next-carrier exists, the right next question is often not “what other branch looks important?”
- it is “which branch actually depends on the carrier family strongly enough to own the split?”

### 4. Miasm/SSA material sharpens the split into true_next / false_next
MODeflattener is useful because it treats conditional relevant blocks as:
- one state-carrier family
- one conditional reducer
- one `true_next` value
- one `false_next` value
- later backbone mapping from those values back into real destinations

Operator consequence:
- if both visible arms normalize to the same next value or the same mapped backbone destination, the copied-code branch family is weaker than it looked
- if the arms reduce to distinct `true_next` / `false_next` values that map cleanly through the backbone, that is the stronger split worth preserving

### 5. Symbolic execution is most useful here as a narrow split extractor
angr’s symbolic-execution docs are broad, but they support one practical constraint-centered move:
- use symbolic execution to answer one bounded A-to-B branch question and recover conditions for taking one path or another

Operator consequence:
- for this continuation, symbolic execution is best used from one relevant block to one dispatcher re-entry or one candidate target family
- do not widen immediately into whole-function beautification if the real missing object is only one trustworthy successor split

## Practical synthesis worth preserving canonically
A compact split for this seam is:

```text
normalized next-carrier recovered
  != visible copied-code / question-opaque branch family understood
  != branch actually depends on the carrier or its dependency family
  != trustworthy successor split recovered
  != safe CFG repair
```

A second compare-heavy reminder worth preserving is:

```text
raw branch arms differ
  != normalized carrier outputs differ
  != backbone-mapped destinations differ
  != later state edge differs
```

These splits keep analysts from overreading:
- a large copied arm
- one still-visible branch instruction
- one constant-wrapper patch
- one state value recovered in isolation

as if any of those alone already settled the real successor split.

## Best KB use of this material
This material is best used as a thinner continuation under the existing opaque-predicate / computed-next-state branch.

It should *not* become:
- a broad new control-flow-flattening overview page
- a duplicate of the existing opaque-predicate note
- a generic “use symbolic execution” reminder divorced from branch ownership

The durable operator value is narrower:
- freeze one normalized next-carrier first
- compare copied / noisy arms at the level of carrier outputs and mapped destinations
- prove which branch really depends on the carrier family
- preserve only that trustworthy successor split before wider CFG repair or downstream state-edge work

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source result.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked; its failure is recorded clearly.
