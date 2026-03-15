# Run Report — 2026-03-16 00:00 Asia/Shanghai

## 1. Scope this run
This run continued the KB’s practical pivot by looking for a missing **middle-layer mobile workflow page** rather than creating another abstract synthesis page.

The starting review covered:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent runs from 2026-03-15
- `topics/mobile-protected-runtime-subtree-guide.md`
- adjacent practical notes including:
  - `topics/mobile-response-consumer-localization-workflow-note.md`
  - `topics/attestation-verdict-to-policy-state-workflow-note.md`
  - `topics/mobile-challenge-trigger-and-loop-slice-workflow-note.md`
  - `topics/environment-differential-diagnosis-workflow-note.md`

The practical gap identified this run was:
- the KB already had notes for transport ownership, response-consumer localization, attestation consequence localization, trust-path localization, and hybrid WebView handoff
- but it still lacked a dedicated practical note for cases where analysts already see a parsed result object or callback with one or more **result codes / enums**, yet still cannot explain which reduction step turns those values into a behavior-changing local policy bucket

This gap appears repeatedly in mobile targets where:
- a protobuf/JSON/custom response object is already known
- one or more fields like `code`, `status`, `type`, `mode`, `reason`, or enum values are visible
- decompiled output around the decisive branch is flattened or misleading
- retry/error classification and policy classification are interleaved
- later behavior changes only after a smaller app-local policy bucket is selected

This run therefore focused on creating a concrete workflow page for:
- result-code / enum-to-policy mapping localization
- separating raw field visibility from normalization and policy reduction
- moving from decompiler output to smali switch reconstruction when needed
- proving the first state write or scheduler that operationalizes the mapping

## 2. New findings
- A durable KB gap existed between:
  - “the relevant result code or enum is visible”
  - and “the first app-local policy bucket that predicts later behavior is localized”
- The strongest reusable practical split added this run is:

```text
parsed response / verdict object
  -> raw result codes / enums / sibling flags visible
  -> helper reduces them into fewer policy buckets
  -> switch / ordinal map / branch selects a policy category
  -> state write / scheduler / gate makes the category operational
  -> later allow / retry / degrade / challenge / block consequence appears
```

- The most important new operational distinction added this run is:
  - **visible result code is not yet visible policy**
- A recurring analyst mistake captured explicitly this run:
  - stopping at one visible integer/enum field, even though the app later collapses several raw values into a much smaller business/risk state space
- A second important distinction added this run is:
  - **decompiler-visible control flow is not always switch ownership truth**
- The new note makes explicit that a frequent next move is not “more parser hooks” but:
  - reconstructing `packed-switch` / `sparse-switch` / ordinal-mapping boundaries
  - then following the first operational state write or scheduler

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/mobile-response-consumer-localization-workflow-note.md`
- `topics/attestation-verdict-to-policy-state-workflow-note.md`
- `topics/mobile-challenge-trigger-and-loop-slice-workflow-note.md`
- `topics/environment-differential-diagnosis-workflow-note.md`
- `topics/protocol-state-and-message-recovery.md`

### External / search material
Search-layer queries:
- `Android reverse engineering enum result code mapping state machine challenge policy app`
- `Android reverse engineering switch enum result code callback state write mobile app`
- `protobuf enum result code mapping reverse engineering Android app challenge flow`

Primary externally consulted materials:
- `pbtk` repository / README
  - `https://github.com/marin-m/pbtk`
- SysDream — reverse engineering of protobuf-based applications
  - `https://sysdream.com/reverse-engineering-of-protobuf-based/`
- Arkadiy Tetelman — reverse engineering protobuf definitions from compiled binaries
  - `https://arkadiyt.com/2024/03/03/reverse-engineering-protobuf-definitiions-from-compiled-binaries/`
- Android/Dalvik bytecode switch-shape references surfaced through search-layer
- supporting search-layer signal from Stack Overflow / JEB-style enum-switch reconstruction references

### New source notes written this run
- `sources/mobile-runtime-instrumentation/2026-03-16-result-code-enum-to-policy-mapping-notes.md`

### Source-quality judgment
- The strongest practical value came from combining:
  - existing KB mobile workflow structure
  - protobuf structure-recovery references that make result fields and enums easier to name
  - switch-shape reasoning that explains why decompiler output can hide the real mapping boundary
- Direct fetch of the Android bytecode documentation hit redirect limits in this environment.
- Because of that limitation, this run intentionally stayed workflow-centered and avoided overclaiming toolchain-specific details.
- The evidence is strong enough for a concrete workflow note, but not for a universal theory of enum lowering across all Android toolchains.

## 4. Reflections / synthesis
This run stayed aligned with the human correction by resisting the weaker move.

The weak move would have been:
- write a broad enum-analysis page
- create an abstract state-machine taxonomy page
- or produce a generic protobuf result-code overview

The stronger move was:
- identify the exact practical gap in the current mobile subtree
- model the gap as a **result-code / enum-to-policy mapping** problem
- separate raw field visibility, normalization, policy mapping, and first operational consumer
- make smali switch reconstruction an explicit fallback when high-level decompiler output stays misleading
- route the result into adjacent practical pages on response-consumer localization, attestation consequence, and challenge-loop analysis

The best synthesis from this run is:

**In many mobile reversing cases, the hard part is not seeing the result code. The hard part is proving which reduction step turns visible result fields into the first behavior-changing local policy bucket.**

That changes breakpoint choice.
Instead of stopping at getters, callbacks, or parser output, the KB now recommends:
- find the earliest stable raw code visibility boundary
- test whether a normalization helper or switch boundary reduces those values further
- reconstruct the real branch owner when decompiler output looks flattened
- prove consequence at the first state write or scheduler that predicts later behavior

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/result-code-and-enum-to-policy-mapping-workflow-note.md`

### Improved this run
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`

### New source note added
- `sources/mobile-runtime-instrumentation/2026-03-16-result-code-enum-to-policy-mapping-notes.md`

### Candidate future creation/improvement
- a future concrete note on **smali switch reconstruction patterns for protected Android targets** if enough code-grounded material accumulates
- a future note on **policy-bucket compare-run diagnosis** when visible result fields stay constant but local state still diverges
- improve `topics/mobile-challenge-and-verification-loop-analysis.md` with a compact section linking:
  - response-consumer localization
  - result-code / enum-to-policy mapping
  - first challenge consequence

## 6. Next-step research directions
1. Continue filling the mobile subtree with concrete middle-layer workflow pages instead of broad architecture pages.
2. Good adjacent practical gaps now include:
   - policy-bucket compare-run diagnosis
   - delayed scheduler / timer ownership after policy mapping
   - switch reconstruction for obfuscated Kotlin/Java enum lowering in protected targets
   - site/app-family-specific mobile challenge and verdict cases once better grounded public material accumulates
3. Keep preferring pages that include:
   - target pattern / scenario
   - analyst goal
   - concrete workflow
   - where to place breakpoints/hooks
   - likely failure modes
   - what state or request change proves the hook matters
4. Preserve the mobile subtree as an investigator playbook with usable entry points:
   - transport ownership
   - trust-path localization
   - response-consumer localization
   - attestation verdict consequence localization
   - result-code / enum-to-policy mapping localization
   - challenge-loop / request-consequence analysis
   - hybrid page/native handoff as needed

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated workflow page for **result-code / enum-to-policy mapping localization**.
- Added an explicit practical split between:
  - raw result field visibility
  - normalization
  - policy mapping
  - first state-write / scheduler consequence
- Added concrete guidance to move from high-level decompiler output to **`packed-switch` / `sparse-switch` / ordinal-mapping reconstruction** when branch ownership stays unclear.
- Added explicit separation of:
  - raw result code
  - normalized code
  - policy bucket
  - scheduler decision
  - business gate
- Added practical failure diagnosis for:
  - stopping at one visible integer/enum field
  - trusting flattened decompiler control flow too much
  - confusing retry/error logic with policy logic
  - comparing runs only at raw field visibility instead of at mapping/state-write boundaries

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/result-code-and-enum-to-policy-mapping-workflow-note.md`
  - `sources/mobile-runtime-instrumentation/2026-03-16-result-code-enum-to-policy-mapping-notes.md`
  - navigation updates in `topics/mobile-protected-runtime-subtree-guide.md` and `index.md`
  - this run report
- Tooling limitation encountered this run and recorded conservatively:
  - direct fetch of an Android bytecode reference hit redirect limits under `web_fetch`
- Next operational steps after writing this report:
  - commit the KB changes in `/root/.openclaw/workspace`
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, preserve local state and record the failure locally in the run report
