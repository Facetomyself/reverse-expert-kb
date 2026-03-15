# Run Report — 2026-03-15 23:00 Asia/Shanghai

## 1. Scope this run
This run continued the KB’s practical pivot by looking for a still-missing concrete mobile workflow note rather than creating another abstract synthesis page.

The starting review covered:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent browser/mobile workflow pages and run reports from 2026-03-15
- `topics/mobile-protected-runtime-subtree-guide.md`
- adjacent practical notes including:
  - `topics/mobile-response-consumer-localization-workflow-note.md`
  - `topics/mobile-challenge-and-verification-loop-analysis.md`
  - `topics/mobile-risk-control-and-device-fingerprint-analysis.md`
  - `topics/environment-differential-diagnosis-workflow-note.md`

The practical gap identified this run was:
- the KB already had notes for request ownership, trust-path localization, response-consumer localization, challenge-loop analysis, and hybrid WebView handoff
- but it still lacked a dedicated practical note for **attestation-heavy Android targets** where the hard part is no longer finding the attestation family, but proving which local branch turns verdict material into a meaningful policy state

This gap appears repeatedly in modern Android cases where analysts can already see:
- integrity-token requests
- backend verification calls
- attestation-related callbacks or response objects

but still cannot explain which local transition actually causes:
- allow
- degrade / reduced mode
- retry / backoff
- challenge escalation
- block or device rebind/login refresh

This run therefore focused on creating a concrete workflow page for:
- verdict-to-policy-state localization
- separating verdict decode from policy mapping
- separating policy mapping from transient retry/fallback logic
- proving the first state write, gate, or scheduler that actually predicts later behavior

## 2. New findings
- A durable KB gap existed between:
  - “the attestation / device-verdict family is visible”
  - and “the first local branch that changes behavior is localized”
- The most reusable practical split for this family is:

```text
attestation request or token acquisition
  -> verdict material or verification response arrives
  -> decode / normalize / map result codes
  -> local policy state or gate is selected
  -> retry / fallback / challenge / reduced-mode / allow path fires
```

- The strongest new operational distinction added this run is:
  - **verdict mapping is not the same thing as retry / fallback handling**
- A recurring analyst mistake captured explicitly this run:
  - proving that a Play Integrity / attestation callback fires, then stopping there even though the decisive branch lives in a later mapping helper, state controller, or scheduler
- The KB now has a better practical bridge between:
  - attestation-family recognition
  - response-consumer localization
  - and downstream challenge / risk / request-consequence analysis
- A second important distinction added this run is:
  - **API visibility is not policy consequence visibility**

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/mobile-response-consumer-localization-workflow-note.md`
- `topics/mobile-challenge-and-verification-loop-analysis.md`
- `topics/mobile-risk-control-and-device-fingerprint-analysis.md`
- `topics/environment-differential-diagnosis-workflow-note.md`
- `topics/protocol-state-and-message-recovery.md`

### External / search material
Search-layer queries:
- `Android Play Integrity verdict reverse engineering app policy state transition callback device verdict`
- `Android attestation verdict callback state machine reverse engineering risk mode challenge app`
- `Android Play Integrity response handling app decision point retry challenge reverse engineering`

Primary externally consulted materials:
- Android Developers material surfaced through search-layer on Play Integrity verdicts
- Android Developers material surfaced through search-layer on Play Integrity error/retry concepts
- Guardsquare — `https://www.guardsquare.com/blog/bypassing-key-attestation-api`
- Approov — `https://approov.io/blog/limitations-of-google-play-integrity-api-ex-safetynet`

### New source notes written this run
- `sources/mobile-runtime-instrumentation/2026-03-15-attestation-verdict-to-policy-state-notes.md`

### Source-quality judgment
- The strongest practical value came from combining:
  - existing KB mobile workflow structure
  - Android Developers verdict/retry framing surfaced through search-layer
  - conservative external framing showing that visible attestation API usage is not equivalent to meaningful policy consequence
- Direct `web_fetch` on some `developer.android.com` Play Integrity pages hit redirect limits in this environment.
- Because of that tooling limitation, this run intentionally stayed workflow-centered and avoided overclaiming platform specifics that were not fully extracted locally.
- The evidence is strong enough for a concrete workflow note, but not for a deep authoritative taxonomy of Play Integrity internals.

## 4. Reflections / synthesis
This run stayed aligned with the human correction by resisting an easy but weaker move.

The weak move would have been:
- write a broad Play Integrity overview
- create an abstract attestation taxonomy page
- or produce a generic Android trust-verdict synthesis page

The stronger move was:
- identify the exact practical gap in the current mobile subtree
- model the gap as a **verdict-to-policy-state localization** problem
- separate request/token acquisition, structured verdict, mapping helper, and first behavior-changing consumer
- explicitly split verdict policy logic from transient retry/fallback logic
- route the result into adjacent practical pages on response-consumer localization, challenge loops, and environment-differential diagnosis

The best synthesis from this run is:

**In many attestation-heavy Android cases, the hard part is not finding the integrity family. The hard part is proving which local mapping step turns verdict material into the first state or gate that actually changes behavior.**

That changes breakpoint choice.
Instead of stopping at token acquisition or raw attestation callbacks, the KB now recommends:
- find the earliest stable structured verdict object
- localize the helper that reduces verdict material into local policy categories
- keep retry/error classification separate from trust-policy classification
- prove the first state write, gate, or scheduler that predicts later challenge / allow / block behavior

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/attestation-verdict-to-policy-state-workflow-note.md`

### Improved this run
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`

### New source note added
- `sources/mobile-runtime-instrumentation/2026-03-15-attestation-verdict-to-policy-state-notes.md`

### Candidate future creation/improvement
- a future concrete note on **result-code / enum-to-policy mapping localization** for cases broader than attestation-heavy targets
- a future concrete note on **attestation retry vs fallback-mode scheduler diagnosis** if stronger implementation-grounded sources accumulate
- improve `topics/mobile-challenge-and-verification-loop-analysis.md` with a compact section linking:
  - response-consumer localization
  - attestation verdict mapping
  - challenge escalation consequence

## 6. Next-step research directions
1. Continue filling the mobile subtree with narrow practical “middle-layer” pages instead of broad umbrella pages.
2. Good adjacent practical gaps now include:
   - result-code / enum-to-policy mapping outside attestation-heavy flows
   - attestation retry vs degraded-mode scheduler diagnosis
   - device verdict to challenge-trigger transition in hybrid risk-control apps
   - first downstream protected-request family that actually consumes verdict-derived state
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
   - attestation verdict to policy-state localization
   - challenge-loop / request-consequence analysis
   - hybrid page/native handoff as needed

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated workflow page for **attestation verdict to policy-state localization**.
- Added an explicit practical split between:
  - request/token acquisition
  - structured verdict / verification result
  - verdict-to-policy mapping
  - first state write / gate / scheduler
- Added explicit separation of:
  - verdict policy logic
  - error classification
  - retry/fallback logic
- Added concrete hook-placement guidance for:
  - attestation request / token-acquisition boundary
  - verdict-object creation / verification-response boundary
  - verdict-to-policy mapping helper
  - state-write / gate boundary
  - retry / scheduler boundary
- Added practical failure diagnosis for:
  - stopping at visible attestation callbacks
  - confusing retry/backoff with trust-policy logic
  - skipping the local mapping layer and jumping straight to final blocked requests
  - assuming local code fully explains server-side trust decisions

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/attestation-verdict-to-policy-state-workflow-note.md`
  - `sources/mobile-runtime-instrumentation/2026-03-15-attestation-verdict-to-policy-state-notes.md`
  - navigation updates in `topics/mobile-protected-runtime-subtree-guide.md` and `index.md`
  - this run report
- Tooling limitation encountered this run and recorded conservatively:
  - some `developer.android.com` Play Integrity pages hit redirect limits under `web_fetch`
- Next operational steps after writing this report:
  - commit the KB changes in `/root/.openclaw/workspace`
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, preserve local state and record the failure locally in the run report
