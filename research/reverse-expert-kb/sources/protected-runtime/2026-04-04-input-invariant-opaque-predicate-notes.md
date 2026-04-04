# 2026-04-04 input-invariant opaque predicate -> valid-input constraint recovery notes

Date: 2026-04-04 17:21 Asia/Shanghai / 2026-04-04 09:21 UTC
Theme: some opaque-predicate families are most usefully reduced by recovering the valid-input invariant they depend on, not by demanding a global constant-branch proof.

## Why this note was retained
The protected-runtime branch already had a broad workflow note for opaque predicates and computed next-state recovery.
What it lacked was a thinner continuation for a recurring operator move:
- the analyst already knows the branch family is suspicious
- broad next-state recovery is no longer the cheapest question
- the real leverage is recovering the valid-input constraint that makes the branch effectively fixed in accepted executions

## Primary retained references
### 1. Input-Invariant Opaque Predicates: More Challenges for Symbolic Execution (USENIX Security 2021)
Sources:
- USENIX presentation page
  - https://www.usenix.org/conference/usenixsecurity21/presentation/yadegari
- paper PDF
  - https://www.usenix.org/system/files/sec21fall-yadegari.pdf

Retained points:
- there exists a practically important opaque-predicate family tied to input invariants / valid-input structure
- naive symbolic exploration can misread these as larger branch-diversity problems than they are for accepted executions

Operator consequence:
- “prove global constancy” is sometimes the wrong question; recovering the accepted-input invariant can be cheaper and more useful

### 2. Heuristic / logic-oriented opaque-predicate literature
Sources:
- NDSS workshop paper on heuristic opaque-predicate detection
  - https://www.ndss-symposium.org/wp-content/uploads/2020/04/bar2020-23004.pdf
- Logic-Oriented Opaque Predicate Detection in Obfuscated Binary Code
  - https://dl.acm.org/doi/pdf/10.1145/2810103.2813617

Retained use:
- supporting literature that opaque predicates remain a practical branch-noise and deobfuscation problem
- used here mainly to justify the branch as a real operator concern, not to overclaim one canonical solving method

## Practical synthesis retained
This continuation note keeps the following smaller split visible:

```text
predicate structure visible
  != globally constant proof required
  != branch diversity under malformed inputs matters
  != valid-input invariant recovered
  != downstream simplification payoff applied
```

The operator move is to ask:
- what accepted-input, parser-normalized, checksum, range, or modular relation makes this branch effectively fixed for executions that actually matter?

## Search-layer trace
See:
- `sources/protected-runtime/2026-04-04-1721-input-invariant-opaque-search-layer.txt`

Observed degraded mode:
- Exa: returned results
- Tavily: returned results
- Grok: invoked but returned empty set
