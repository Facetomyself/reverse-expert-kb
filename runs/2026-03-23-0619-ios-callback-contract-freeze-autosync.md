# 2026-03-23 reverse KB autosync — iOS callback contract freeze

Mode: external-research-driven

## Summary
This run intentionally avoided another easy dense-branch sync pass.
Recent runs already kept native, malware, runtime-evidence, and protected-runtime practical leaves active enough that another small internal canonicalization pass would have risked stagnation.

I chose a thinner-but-still-practical iOS seam instead:
- the gap between “one callback/block family looks plausible” and “the analyst can now trust replay or policy claims”
- specifically, the KB was still weaker on preserving the stop rule for when to stop widening broad owner/callback search and instead freeze the first trustworthy runtime contract

The run therefore performed a real external multi-source search pass and converted the result into a practical KB improvement, not just another wording/index sync.

## Direction / branch-balance review
Recent run shape before this pass:
- native practical continuation: active
- runtime-evidence practical continuation: active
- malware continuation: active
- protected-runtime continuation: active
- iOS branch: established, but thinner at the callback-contract seam between plausible landing and trustworthy replay/policy handoff

Branch-balance judgment:
- this was a good slot for an iOS practical continuation rather than another native/protected/browser maintenance pass
- the chosen seam had real operator value and was still thin enough to benefit from source-backed strengthening
- this keeps the anti-stagnation rule healthy by doing real external research on a thinner practical branch instead of repeating internal count/index syncing

## Work performed
### 1. Reviewed recent autosync runs and current branch pressure
Checked recent run reports and KB top-level branch balance to avoid spending this run on another easy internal sync-only edit.

### 2. Selected an underfed iOS practical seam
Targeted the callback/block landing area where the branch already had:
- mitigation-aware PAC/arm64e continuation
- callback landing note
- replay-repair continuation

But still needed a clearer canonical stop rule:
- once one callback/block family is already plausible, do not reopen broad owner search by default
- first freeze the first runtime-backed block contract

### 3. Ran explicit multi-source search
Executed `search-layer` with explicit source selection:
- `--source exa,tavily,grok`

Search focus:
- iOS arm64e callback/block signature recovery
- dyld shared cache truth for callback/dispatch reasoning
- Objective-C/Clang Block ABI structure and runtime signature recovery

### 4. Grounded the change with source-backed practical synthesis
Pulled and used the following practical source surfaces:
- Clang Block ABI documentation
- Clang pointer-authentication documentation
- `ipsw` dyld shared cache guide
- Everett LLDB block-signature note

### 5. Updated the KB itself
Materially strengthened:
- `topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md`
- `topics/ios-practical-subtree-guide.md`
- `index.md`

Added source note:
- `sources/mobile-runtime-instrumentation/2026-03-23-ios-callback-contract-source-notes.md`

## KB changes
### Strengthened canonical rule in the callback note
Added a clearer operator framing around the **first runtime-backed block contract**.

The note now preserves that the proof object is:
- one plausible block/callback family
- one dyld/cache-truthful invoke landing
- one runtime-visible or tightly constrained signature shape
- one downstream effect worth handing off

This gives the branch a more practical stop rule:
- once that contract exists, treat it as the end of broad callback/owner widening for that stage unless later evidence breaks it

### Strengthened subtree routing
Updated the iOS subtree guide so the callback/block stage explicitly says:
- prefer freezing the first runtime-backed block contract
- do not widen broad owner search again too early

### Synced top-level index direction language
Updated the top-level branch-balance language so the iOS branch is remembered as not only established, but also now carrying a clearer callback/block stop rule.

## Why this matters
This run improved the KB itself instead of merely collecting notes because it converted external material into a durable practical routing rule.

The concrete operator value is:
- fewer cases drifting back into endless broad callback/owner search
- better separation between:
  - callback-family plausibility
  - invoke-landing truth
  - signature-contract truth
  - downstream owner/policy consequence
- cleaner handoff from callback proof into replay repair or policy-state work

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

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Search transcript:
- `sources/mobile-runtime-instrumentation/2026-03-23-ios-callback-contract-search-layer.txt`

## Files changed
- `topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md`
- `topics/ios-practical-subtree-guide.md`
- `index.md`
- `sources/mobile-runtime-instrumentation/2026-03-23-ios-callback-contract-source-notes.md`
- `runs/2026-03-23-0619-ios-callback-contract-freeze-autosync.md`

## Commit / sync status
KB changes were made and should be committed.
After commit, run:
- `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

## Next best follow-on
A good future iOS follow-on would be one still-practical case note on this exact seam:
- when the first runtime-backed block contract is frozen, how to decide whether the remaining failure is:
  - wrong family
  - wrong authenticated context/materialization
  - lying code view
  - replay-close missing obligation

That would deepen the branch without overfeeding it.
