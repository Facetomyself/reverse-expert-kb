# Run Report — 2026-03-15 18:00 Asia/Shanghai

## 1. Scope this run
This run continued the KB’s practical mobile/hybrid expansion and deliberately avoided creating another abstract WebView taxonomy page.

The review covered:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- current mobile/browser subtree guides
- the latest hybrid sequence pages:
  - `webview-native-mixed-request-ownership-workflow-note.md`
  - `webview-native-bridge-payload-recovery-workflow-note.md`
  - `webview-native-response-handoff-and-page-consumption-workflow-note.md`
- recent source notes and run reports

The concrete gap identified this run was:
- the KB already had pages for broad hybrid ownership, general bridge-payload recovery, and native→page return paths
- but it still lacked a dedicated practical note for one common hybrid family where analysts get misled early:
  - **navigation-driven page→native handoff via custom schemes, deep links, route changes, and `shouldOverrideUrlLoading(...)`-style boundaries**

This run therefore focused on creating a concrete workflow note for:
- custom-scheme / deep-link / route-based WebView→native handoff
- raw URL/route capture before native normalization
- first native parser / dispatcher localization
- separation of navigation intent from later request transport ownership

## 2. New findings
- The missing practical seam in the hybrid mobile branch was not “a better WebView theory page,” but a dedicated workflow note for **navigation/custom-scheme handoff localization**.
- A durable distinction was added explicitly:
  - **navigation handoff boundary**
  - **native request/transport boundary**
- The strongest practical addition this run is:
  - **absence of `addJavascriptInterface(...)` does not mean absence of a bridge**
- Custom schemes, deep links, ordinary `https` routes with encoded action state, and reload/bootstrap refreshes were elevated as separate recurring handoff families.
- `shouldOverrideUrlLoading(...)` was reframed as a high-value analyst boundary for intent recovery rather than just a web-navigation detail.
- The page now treats “raw URL before native parsing” as a first-class evidence object because it often preserves structured fields that later disappear into routers, controllers, signing helpers, or request builders.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/webview-native-mixed-request-ownership-workflow-note.md`
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-mixed-request-ownership-notes.md`
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-bridge-payload-recovery-notes.md`
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-response-handoff-notes.md`

### External / search material
Search-layer query cluster:
- `Android WebView shouldOverrideUrlLoading custom scheme deeplink bridge workflow`
- `WebViewClient shouldOverrideUrlLoading custom URL bridge Android`
- `Android WebView shouldOverrideUrlLoading addJavascriptInterface postWebMessage hybrid bridge workflow`

Useful returned result classes:
- practical discussions/tutorials centered on `shouldOverrideUrlLoading(...)`
- custom-scheme handling discussions
- Android/WebView API-shape references surfaced through search

### Tooling / source-quality notes
- `web_fetch` hit redirect-limit failures on Android Developers reference pages again during this run.
- That failure was logged in `.learnings/ERRORS.md` instead of being ignored.
- Existing KB source notes plus search-layer output were sufficient to continue conservatively without forcing brittle claims from blocked fetches.

## 4. Reflections / synthesis
This run stayed aligned with the human correction by filling a concrete operational gap rather than broadening abstract structure.

The weaker move would have been:
- another generic hybrid/WebView overview page
- a broad taxonomy of bridge families without a strong workflow center
- or more abstract splitting of “hybrid app communication patterns”

The stronger move was:
- identify a recurring mid-case bottleneck between existing practical pages
- build a page around how analysts actually get misled when object bridges are absent
- center the workflow on target-vs-non-target comparison, raw navigation capture, and first native parser localization
- separate navigation intent from later transport ownership

The best synthesis from this run is:

**In hybrid Android apps, navigation can itself be the bridge family.**

That changes hook placement.
Instead of stopping at WebView resource callbacks or hunting only for object bridges, the KB now recommends:
- test whether the real handoff is custom-scheme, deep-link, route-based, or reload/bootstrap driven
- capture the raw navigation target before native parsing destroys structure
- localize the first native parser/dispatcher
- only then route into request ownership, signing, or return-path analysis

That is much closer to how real hybrid debugging works than a generic WebView bridge taxonomy.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/webview-custom-scheme-and-navigation-handoff-workflow-note.md`

### Improved this run
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`

### New source note added
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-custom-scheme-and-navigation-handoff-notes.md`

### Candidate future creation/improvement
- a future concrete note on **route-parser lookup-key vs full-payload cases** once enough grounded examples accumulate
- a future note comparing **custom-scheme handoff vs object-bridge handoff failure modes** across several hybrid targets
- improve the hybrid branch guide text in `mobile-protected-runtime-subtree-guide.md` further once more concrete WebView child pages accumulate

## 6. Next-step research directions
1. Continue expanding the hybrid mobile branch by practical bottleneck, not by abstract protocol taxonomy.
2. High-value adjacent topics now include:
   - route-parser lookup-state recovery after URL handoff
   - compare-run diagnosis for target-vs-non-target navigation actions
   - hybrid pages where route intent, native signing, and native→page return all appear in one loop
3. Keep preferring pages that include:
   - target pattern / scenario
   - analyst goal
   - concrete workflow
   - where to hook/breakpoint
   - likely failure modes
   - representative code/pseudocode
4. Maintain the mobile hybrid subtree as an investigator playbook, not a generic WebView glossary.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated workflow page for **WebView custom-scheme and navigation-based handoff localization**.
- Added explicit operational separation of:
  - navigation handoff boundary
  - native request/transport boundary
- Added concrete guidance to classify navigation handoff into:
  - custom-scheme action bridge
  - `intent://` / deep-link dispatch bridge
  - ordinary `https` route carrying command state
  - reload/bootstrap refresh carrying lookup state
- Added breakpoint placement centered on:
  - page-side navigation creation
  - `loadUrl(...)`
  - `shouldOverrideUrlLoading(...)`
  - first native URL parser / route dispatcher
  - first request-driving consumer after route parse
- Added practical advice to treat these as common failure axes:
  - no object bridge visible but navigation bridge exists
  - over-trusting `shouldInterceptRequest(...)`
  - dismissing custom URLs as UI-only routing noise
  - capturing raw URL but missing that it only carries a lookup key

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/webview-custom-scheme-and-navigation-handoff-workflow-note.md`
  - `sources/mobile-runtime-instrumentation/2026-03-15-webview-custom-scheme-and-navigation-handoff-notes.md`
  - navigation updates in `topics/mobile-protected-runtime-subtree-guide.md` and `index.md`
  - this run report
- Tool failure encountered and recorded separately:
  - Android Developers pages hit repeated `web_fetch` redirect-limit failures
- Next operational steps after writing this report:
  - commit the KB changes in `/root/.openclaw/workspace`
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, preserve local state and keep the failure recorded in this run report
