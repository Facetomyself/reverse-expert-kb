# Source notes — opaque predicate / computed next-state recovery practical anchors

Date: 2026-04-05 08:25 Asia/Shanghai / 2026-04-05 00:25 UTC
Topic: opaque predicate and computed next-state recovery
Author: Reverse Claw

## Why this pass happened
Recent runs had already covered malware/Linux persistence and protocol pending-request lifetime realism.
This hour needed a real external-research-driven pass on a thinner practical branch without drifting back into another adjacent malware or protocol maintenance step.

The chosen seam was the existing `opaque-predicate-and-computed-next-state-recovery` note.
It already existed and was structurally sound, but it still benefited from fresher concrete operator anchors drawn from:
- Tigress transform docs
- Binary Ninja unflattening / branch-fixing workflows
- Miasm / OLLVM deflattening material

## Practical question
What concrete external sources most usefully reinforce this operational rule:

```text
recover one trustworthy next-state relation first,
not full deobfuscation first
```

and which transform/tooling details are worth preserving in the KB for future operators?

## Retained high-signal points
### 1. Tigress makes the transform knobs explicit
Search results surfaced Tigress documentation showing that flattening shape and next-variable obfuscation are separate concerns:
- dispatch form can be `switch`, `goto`, `indirect`, `call`, etc.
- the next variable can be obfuscated separately
- conditional branches can be encoded separately

Retained operator consequence:
- recognizing the dispatcher is weaker than recovering the next-state carrier
- encoded-branch or obfuscated-next variants should still be treated as a narrower next-state recovery problem, not automatically as a reason to widen into total deobfuscation

### 2. Binary Ninja-style practical unflattening often starts with one state mapping, not a perfect CFG
Search results surfaced several BN-oriented writeups and docs where the practical workflow is:
- identify the state variable or comparison family
- map one OBB to one state value or one successor relation
- patch or rewire only after a smaller relation is trusted

Retained operator consequence:
- one trustworthy edge or state mapping is a valid stopping milestone
- demanding total CFG prettification before trusting any edge is usually the wrong order of operations

### 3. Opaque predicate removal is useful, but mostly as noise reduction
BN opaque-predicate material is useful because it highlights architecture-agnostic IL/data-flow assisted cleanup.
But it also implicitly reinforces a stop rule:
- if loops, helpers, or richer value computation still hide the real successor relation, generic opaque cleanup alone is not the whole answer

Retained operator consequence:
- use opaque cleanup to reduce noise
- do not let generic branch cleanup replace the narrower task of proving one successor relation

### 4. Miasm / OLLVM deflattening material keeps the recovery target narrow
Search results surfaced Miasm and OLLVM unflattening references that fit the same practical pattern:
- symbolic execution / local emulation is used to extract successor relations
- the goal is not necessarily full semantic recovery of the entire function before progress

Retained operator consequence:
- symbolic execution is best treated here as a narrow successor extractor
- if one relation is enough to unblock CFG repair or downstream proof, stop there first

## Conservative synthesis used in KB
Useful branch rule preserved:

```text
dispatcher recognized
  != next-state carrier recovered
  != trustworthy successor relation
  != full deobfuscation required
```

Additional practical branch memory preserved:
- encoded-branch / obfuscated-next variants are still next-state recovery cases
- one mapped edge first, prettier CFG later
- opaque cleanup is subordinate to successor proof when the branch bottleneck is still next-state realism

## Sources consulted
### Explicit multi-source search attempt
All searches were run via explicit `search-layer` source selection:
- `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok ...`

Search themes used:
- OLLVM / Miasm / Binary Ninja control-flow flattening and unflattening
- Tigress flattening / obfuscated-next / opaque predicate knobs
- BN workflows and opaque predicate removal

### Representative surfaced materials
- Tigress control-flow flattening docs
- Tigress opaque predicate / encode-branches docs
- Binary Ninja opaque predicate removal blog
- Binary Ninja branch-obfuscation / control-flow unflattening writeups
- Miasm MODeflattener
- OLLVM unflattener references

## Search audit material for run report
Requested sources:
- Exa
- Tavily
- Grok

Observed outcome across this source pass:
- Exa: succeeded with usable hits on all three queries
- Tavily: succeeded with usable hits on all three queries
- Grok: invoked and failed with HTTP 502 Bad Gateway on all three queries

Endpoints / execution paths used:
- Exa endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`
- Tavily endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`
- Grok endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`

## What this changed in KB terms
This pass did not justify a new sibling page.
The right move was to strengthen the existing opaque-predicate / computed-next-state note by preserving:
- encoded-branch / obfuscated-next variants as a distinct practical reminder
- the operator rule that one trustworthy edge beats waiting for a perfect CFG
- the separation between noise reduction and successor proof
