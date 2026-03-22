# Opaque-Predicate and Control-Flow-Flattening Practical Sources — 2026-03-22

## Search capture
- `sources/obfuscation-deobfuscation/2026-03-22-opaque-predicate-search-layer.txt`

## Source set used for this run

### 1. Quarkslab — Deobfuscation: recovering an OLLVM-protected program
URL:
- https://blog.quarkslab.com/deobfuscation-recovering-an-ollvm-protected-program.html

Why it matters:
- classic practical OLLVM unflattening / deobfuscation reference
- reinforces the operator pattern of finding a smaller trustworthy state object and recovering useful control-flow rather than beautifying the whole function first

Fetch note:
- direct `web_fetch` hit a Vercel security checkpoint / 429 in this environment
- source remained discoverable via search-layer and cross-source citation, so it was kept as a referenced source but not relied upon for detailed quoted extraction in this run

### 2. OpenAnalysis — angr control-flow deobfuscation notes
URL:
- https://research.openanalysis.net/angr/symbolic%20execution/deobfuscation/research/2022/03/26/angr_notes.html

High-signal takeaways used:
- practical CFF recovery can be framed as: identify dispatcher state -> associate original basic block with a state -> symbolically solve next state(s) when execution returns to the dispatcher
- symbolic execution is especially useful when direct pattern matching for `mov state, imm` is brittle or incomplete
- the useful operator output is often a smaller state graph / next-state relation, not a perfect whole-function restoration

### 3. Tigress docs — Flatten transformation
URL:
- https://tigress.cs.arizona.edu/transformPage/docs/flatten/index.html

High-signal takeaways used:
- flattening varies meaningfully by dispatch form: `switch`, `goto`, `indirect`, and `call`
- next-state computation itself can be obfuscated
- conditional branches may be preserved, computed, or encoded through flag-register-based logic
- block splitting, block randomization, and dispatch obfuscation materially change what the analyst should expect to remain stable

### 4. Tigress docs — AddOpaque transformation
URL:
- https://tigress.cs.arizona.edu/transformPage/docs/addOpaque/index.html

High-signal takeaways used:
- opaque predicates are not just a cosmetic extra; they can split basic blocks, add bogus branches, or force copied-code shapes that complicate trivial state-update reading
- input- and entropy-backed opaque construction means some branch expressions are better treated as reduction problems than as literal business logic
- this supports a workflow distinction between direct next-state recovery and helper/branch-normalization recovery

### 5. d0minik — Binary Ninja Shenanigans: Control Flow Unflattening
URL:
- https://d0minik.me/posts/cff/

High-signal takeaways used:
- practical HLIL/MLIL reduction can recover OBB/state mappings by finding state-comparison sites rather than starting from fully exact semantics
- identifying the most-written state variable and deriving its dependencies is a useful small-object heuristic
- the patch-worthy target is often the jump back to the dispatcher, replaced by direct MLIL goto to the next original block once the state mapping is trusted

### 6. cdong1012/ollvm-unflattener
URL:
- https://github.com/cdong1012/ollvm-unflattener

High-signal takeaways used:
- modern practical unflatteners increasingly combine static CFG repair with symbolic execution / Miasm-guided state recovery
- breadth-first multi-function follow-up matters when a flattened function’s immediate callees are also part of the protected surface
- useful tool reality check: analysts often accept partial automation that restores enough CFG truth for the next manual step

## Additional fetch-level degradation observed
- Quarkslab article: `429` / Vercel security checkpoint during direct `web_fetch`
- ReverseEngineering Stack Exchange discussion: `403` / anti-bot interstitial during direct `web_fetch`

These fetch degradations did not block the run because:
- the required explicit multi-source search attempt succeeded first
- sufficient practical source material remained available from OpenAnalysis, Tigress, d0minik, and the GitHub tool page

## Practical synthesis direction extracted from the sources
The strongest recurring practical pattern across these sources is:

```text
recognize flattening / dispatcher churn
  -> classify the dispatch form and branch-obfuscation shape
  -> choose one smaller state object or next-state relation
  -> normalize opaque/helper-mediated next-state computation
  -> prove one trustworthy successor edge or OBB mapping
  -> only then decide whether full CFG repair / patching is worth it
```

That direction is stronger than either of these weaker defaults:
- trying to name every handler / case before proving a consequence-bearing state edge
- doing only top-level deobfuscation taxonomy maintenance without preserving operator workflow
