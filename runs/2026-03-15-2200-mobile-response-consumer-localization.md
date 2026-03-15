# Run Report — 2026-03-15 22:00 Asia/Shanghai

## 1. Scope this run
This run continued the KB correction toward practical, case-driven mobile reversing notes.

The starting review covered:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- the mobile subtree guide
- adjacent practical notes on:
  - Android trust-path localization
  - Cronet / mixed-stack request ownership
  - mobile challenge trigger and loop-slice analysis
  - WebView/native response handoff and page consumption
- recent runs from today to avoid duplicating already-added hybrid/mobile workflow notes
- recent mobile source notes

The practical gap identified this run was:
- the KB already had practical notes for request ownership, trust-path localization, hybrid handoff, and challenge-loop analysis
- but it still lacked a concrete response-side workflow for the stage between “the right request/response family is known” and “the first native branch/state transition that actually changes behavior is localized”

This gap appears often in Android reversing when server-issued challenge / risk / attestation / config material is:
- received successfully
- parsed quickly through protobuf/JSON/custom decode paths
- normalized into local objects or enums
- then consumed by callbacks, state controllers, or schedulers before the analyst can see which branch actually matters

This run therefore focused on creating a concrete workflow page for:
- response-side native consumer localization
- separation of raw bytes, parser boundary, normalized object, and first meaningful consumer
- hook placement around parser, mapper, callback, state-write, and consequence boundaries
- practical routing from response-side diagnosis into challenge-loop or signing analysis

## 2. New findings
- A durable KB gap existed between transport-side diagnosis and challenge-loop diagnosis.
- The most reusable practical split for that gap is:

```text
raw response bytes
  -> parser / decoder boundary
  -> generated or normalized response object
  -> callback / dispatcher / state write
  -> first meaningful consumer
  -> downstream request / challenge / trust consequence
```

- The strongest new operational distinction added this run is:
  - **parser visibility is not the same as consequence visibility**
- A recurring analyst mistake was captured explicitly:
  - stopping at a protobuf/JSON parse hook or generated message class, even though the decisive branch only appears in a later dispatcher, state write, or request scheduler
- The KB now has a better practical bridge between:
  - request ownership / transport understanding
  - and challenge-state / follow-up-request consequence analysis
- The note also made explicit that the first useful target is often not “the first parser” but:
  - the first **policy/state consumer**, or
  - the first **request-driving consumer**

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/android-network-trust-and-pinning-localization-workflow-note.md`
- `topics/cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note.md`
- `topics/mobile-challenge-trigger-and-loop-slice-workflow-note.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/protocol-state-and-message-recovery.md`

### External / search material
Search-layer queries:
- `Android reverse engineering response parser callback localization protobuf challenge token app decision point`
- `Android protobuf parser callback reverse engineering locate first consumer network response token`
- `Android app challenge response handling reverse engineering callback parser state machine`

Primary externally consulted materials:
- `pbtk` repository / README
  - `https://github.com/marin-m/pbtk`
- SysDream — reverse engineering of protobuf-based applications
  - `https://sysdream.com/reverse-engineering-of-protobuf-based/`
- HTTP Toolkit — reverse engineering Android apps with JADX & Frida
  - `https://httptoolkit.com/blog/android-reverse-engineering`
- Project Zero — *The State of State Machines*
  - `https://projectzero.google/2021/01/the-state-of-state-machines.html`

Additional source cluster surfaced through search results:
- protobuf-inspector
- micro-protobuf / protobuf definition recovery references
- recent protobuf-definition extraction references

### Source-quality judgment
- The strongest practical grounding came from the protobuf structure-recovery references plus the Android reversing workflow material.
- The state-machine source was not mobile-parser-specific, but was useful for reinforcing the note’s key methodological distinction: first meaningful consequence matters more than first visible callback.
- One fetch failed in this environment for a promising protobuf-definition recovery article, so the synthesis stayed conservative and workflow-centered.
- Because of that limitation, this run intentionally avoided writing a broad protobuf taxonomy page and instead produced a concrete consequence-oriented workflow note.

## 4. Reflections / synthesis
This run stayed aligned with the human correction by avoiding an easy but weaker move.

The weak move would have been:
- add a generic Android protobuf-reversing page
- write another abstract protocol-message page
- or create a broad “response parsing in mobile apps” taxonomy

The stronger move was:
- identify the exact practical gap in the current mobile subtree
- model the gap as a **response-consumer localization** problem
- separate raw bytes, parser boundary, normalized object boundary, and first meaningful consumer
- classify consumers by role
- route the result directly into adjacent practical pages on challenge loops, trust paths, and signing analysis

The best synthesis from this run is:

**In many mobile reversing cases, the hard part is not seeing the response. The hard part is proving which first native consumer turns that response into a state change, follow-up request, or challenged branch.**

That changes breakpoint choice.
Instead of stopping at parser hooks or generated message classes, the KB now recommends:
- find the earliest structured-object boundary
- follow the first fan-out after parsing
- classify each visible consumer by role
- prove consequence through a state change or follow-up request
- only then deepen into challenge-loop or request-shaping analysis

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/mobile-response-consumer-localization-workflow-note.md`

### Improved this run
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`

### New source note added
- `sources/mobile-runtime-instrumentation/2026-03-15-mobile-response-consumer-localization-notes.md`

### Candidate future creation/improvement
- a future concrete note on **protobuf-lite / descriptor-poor message-structure recovery in Android apps** if enough strongly grounded material accumulates
- a future note on **result-code / enum-to-state mapping localization** when server responses are known but the important mapping layer is heavily obfuscated
- improve `topics/mobile-challenge-and-verification-loop-analysis.md` with a compact section linking:
  - request ownership
  - response-consumer localization
  - challenge trigger localization
  - validation consequence analysis

## 6. Next-step research directions
1. Continue filling the mobile subtree with concrete “middle-of-the-loop” pages rather than broad architecture pages.
2. Good adjacent practical gaps now include:
   - result-code / enum mapping localization
   - attestation verdict to policy-state transition patterns
   - compare-run diagnosis where similar parsed responses produce different state writes
   - descriptor-poor protobuf-lite recovery tactics only if source quality is strong enough
3. Keep preferring pages that include:
   - target pattern / scenario
   - analyst goal
   - concrete workflow
   - where to place breakpoints/hooks
   - likely failure modes
   - what consequence proves the hook matters
4. Preserve the mobile subtree as a practical sequence of analyst entry points:
   - transport ownership
   - trust-path localization
   - response-consumer localization
   - challenge-loop or request-shaping analysis
   - mixed hybrid/page-side handoff as needed

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated workflow page for **mobile response consumer localization**.
- Added an explicit practical split between:
  - raw bytes
  - parser / decoder boundary
  - normalized object
  - first meaningful consumer
- Added concrete hook-placement guidance for:
  - parser boundary
  - normalization boundary
  - callback / dispatcher boundary
  - state-write boundary
  - request-scheduler / consequence boundary
- Added explicit consumer-role classification:
  - parser-only
  - normalization
  - cache/store
  - UI-only
  - policy/state
  - request-driving
- Added practical failure diagnosis for:
  - parser hooks that reveal structure but not behavior
  - confusion between callback reachability and operational consequence
  - over-stopping at transport capture or generated message classes
  - skipping the response-side native logic and jumping straight to challenge UI

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/mobile-response-consumer-localization-workflow-note.md`
  - `sources/mobile-runtime-instrumentation/2026-03-15-mobile-response-consumer-localization-notes.md`
  - navigation updates in `topics/mobile-protected-runtime-subtree-guide.md` and `index.md`
  - this run report
- Tooling limitation encountered this run and recorded conservatively:
  - one `web_fetch` candidate source failed during protobuf-related source gathering
- Next operational steps after writing this report:
  - commit the KB changes in `/root/.openclaw/workspace`
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, preserve local state and record the failure locally in the run report
