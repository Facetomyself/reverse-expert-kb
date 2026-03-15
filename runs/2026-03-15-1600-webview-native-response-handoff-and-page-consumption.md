# Run Report — 2026-03-15 16:00 Asia/Shanghai

## 1. Scope this run
This run continued the KB correction toward practical, case-driven hybrid/mobile reversing notes.

The starting review covered:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent mobile subtree structure
- the immediate prior workflow note `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- adjacent practical notes on hybrid ownership, request finalization, Android trust-path localization, and mobile preimage recovery
- recent source notes under `sources/mobile-runtime-instrumentation/`

The practical gap after the prior run was clear:
- the KB already had a concrete note for **page→native bridge payload recovery**
- but it still lacked the equally common next bottleneck in hybrid cases:
  - **how native results get handed back into the page, and which page-side consumer actually matters**

This run therefore focused on creating a concrete workflow page for:
- native→page return-path localization
- `evaluateJavascript(...)` outbound emission capture
- message-channel and `postWebMessage`-style return paths
- reload/URL/bootstrap refresh style native→page handoff
- separation of outbound handoff from the first meaningful page-side consumer

## 2. New findings
- The next practical child page after bridge-payload recovery was not another general hybrid/WebView synthesis page, but a concrete reverse-direction workflow note.
- A durable practical split emerged and was made explicit in the KB:
  - **native→page handoff is not the same as page-side consumption**
- Three native→page return families were strong enough to treat as equal-class workflow targets:
  - `evaluateJavascript(...)`
  - message-channel / `postWebMessage` / `WebMessagePort`
  - URL/reload/bootstrap refresh handoff
- A strong recurring analyst bottleneck was captured explicitly:
  - analysts often prove that native code retrieved or generated the decisive value, but still cannot explain the page-side callback/store/request helper that turns that value into meaningful behavior
- The most reusable operational distinction added this run is:
  - **UI-only consumer vs request-driving consumer vs challenge-state consumer**

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- `topics/webview-native-mixed-request-ownership-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/mobile-signature-location-and-preimage-recovery-workflow-note.md`

### External / search material
Search-layer queries:
- `Android WebView evaluateJavascript response handoff postWebMessage reverse engineering`
- `Android WebView JavascriptInterface evaluateJavascript native to web bridge reverse engineering`
- `Android WebView WebMessagePort postWebMessage native to page communication`

Primary externally consulted materials:
- Android Developers — `WebView` API reference
  - `https://developer.android.com/reference/android/webkit/WebView`
- Android Developers — `WebMessagePort` API reference
  - `https://developer.android.com/reference/android/webkit/WebMessagePort`
- OWASP MASTG — Java objects exposed through WebViews
  - `https://mas.owasp.org/MASTG/tests/android/MASVS-PLATFORM/MASTG-TEST-0033/`
- TechYourChance — Communication with WebView in Android
  - `https://www.techyourchance.com/communication-webview-javascript-android/`

### Source-quality judgment
- Android Developers API references were strong enough to anchor API-shape reasoning for `evaluateJavascript(...)` and `WebMessagePort`, although `web_fetch` hit redirect limits on those URLs in this environment.
- OWASP MASTG was most useful as a terminology/bridge-surface anchor, even though its strongest material is still page→native rather than native→page.
- Practical implementation/tutorial material was weaker than official docs, but valuable here because it exposed real outbound native→page surfaces, callback-return semantics, and console-observation patterns that map directly onto analyst workflow.

## 4. Reflections / synthesis
This run stayed aligned with the human correction by resisting another easy-but-weaker move.

The weak move would have been:
- add another broad page about WebView communication
- add generic bridge taxonomy in both directions
- or create a vague "hybrid state sync" page

The stronger move was:
- identify the exact next analyst bottleneck after bridge-payload recovery
- define native→page handoff families as concrete workflow entry points
- separate outbound handoff from the first meaningful page consumer
- show where to place hooks at the emission boundary and where to move next in the page runtime
- classify consumers by whether they merely update UI or actually drive protected behavior

The best synthesis from this run is:

**In hybrid Android cases, proving that native code retrieved the right result is often not enough. The decisive explanation frequently lives in the first page-side consumer that turns that result into a request, state transition, or challenge advance.**

That changes breakpoint choice.
Instead of stopping at native response handlers or flooding page hooks, the KB now recommends:
- capture the outbound native emission first
- classify the return family
- localize the first page consumer
- classify whether that consumer is UI-only, store/cache, request-driving, challenge-driving, or another bridge round trip
- then route forward into browser request-finalization tracing or another mobile ownership/signature note as appropriate

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`

### Improved this run
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`

### New source note added
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-response-handoff-notes.md`

### Candidate future creation/improvement
- a future concrete note on **hybrid hidden-field / global-store consumer localization** once more real examples accumulate
- a future note on **native-provided challenge result → page widget callback chaining** for cases where the visible page event is downstream of native challenge processing
- improve `topics/mobile-reversing-and-runtime-instrumentation.md` with a compact subsection linking:
  - hybrid ownership diagnosis
  - page→native bridge payload recovery
  - native→page response handoff
  - request ownership and finalization tracing

## 6. Next-step research directions
1. Continue filling the hybrid/mobile branch with concrete loop-completion notes rather than broad architecture pages.
2. High-value adjacent topics now include:
   - hidden-field and global-store consumer localization in hybrid apps
   - native challenge result → page callback chaining
   - hybrid page-consumer → request-finalization crossover patterns
   - compare-run diagnosis where the same native result produces different page-side outcomes
3. Keep preferring pages that include:
   - target pattern / scenario
   - analyst goal
   - concrete workflow
   - outbound emission boundary
   - first consumer boundary
   - likely failure modes
   - route-forward guidance into neighboring practical notes
4. Keep the hybrid/mobile subtree coherent as a practical sequence:
   - hybrid ownership diagnosis
   - page→native bridge payload recovery
   - native→page response handoff
   - page/request consumer localization
   - request finalization or native request ownership as needed

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated workflow page for **WebView/native response handoff and page consumption**.
- Added explicit equal-class treatment of three native→page return families:
  - `evaluateJavascript(...)`
  - message-channel / `postWebMessage` / `WebMessagePort`
  - reload/URL/bootstrap refresh handoff
- Added concrete guidance to separate:
  - outbound native emission
  - first page-side consumer
  - consumer role
  - next operational bottleneck
- Added practical advice to classify consumers as:
  - UI-only
  - store/cache
  - request-driving
  - challenge-driving
  - bridge-back-to-native
- Added explicit failure diagnosis for:
  - proving native retrieval but not the page-side effect
  - over-stopping at `evaluateJavascript(...)`
  - assuming symmetric inbound/outbound bridge families
  - missing reload/bootstrap-style handoff because no explicit callback string is present

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
  - `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-response-handoff-notes.md`
  - navigation updates in `topics/mobile-protected-runtime-subtree-guide.md` and `index.md`
  - this run report
- Tooling fragility encountered this run and recorded in source notes:
  - `web_fetch` redirect-limit failures on some official Android documentation URLs
- Next operational steps after writing this report:
  - commit the KB changes in `/root/.openclaw/workspace`
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, preserve local state and keep the failure recorded in this run report
