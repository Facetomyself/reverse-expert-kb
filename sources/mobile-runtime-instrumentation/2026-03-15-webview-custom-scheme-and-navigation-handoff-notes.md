# Source Notes — WebView Custom-Scheme and Navigation-Handoff Localization

Date: 2026-03-15
Topic: hybrid Android apps, WebView navigation callbacks, custom schemes, route-driven page→native handoff

## Why this source cluster was consulted
The KB already had practical notes for:
- hybrid WebView/native ownership diagnosis
- page→native bridge payload recovery
- native→page response handoff

A recurring concrete gap remained between them:
- some apps show no useful `addJavascriptInterface(...)` bridge
- message-port paths are absent or secondary
- page actions still clearly trigger native behavior
- the real handoff happens through navigation, custom schemes, route changes, deep links, or URL-carried command state

This note therefore focuses on **navigation-driven page→native handoff** rather than generic WebView security.

## Queries used
Search-layer / search.py tutorial-oriented queries:
- `Android WebView shouldOverrideUrlLoading custom scheme deeplink bridge workflow`
- `WebViewClient shouldOverrideUrlLoading custom URL bridge Android`
- `Android WebView shouldOverrideUrlLoading addJavascriptInterface postWebMessage hybrid bridge workflow`

## Sources consulted
### Existing KB material
- `topics/webview-native-mixed-request-ownership-workflow-note.md`
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-mixed-request-ownership-notes.md`
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-bridge-payload-recovery-notes.md`

### Official / semi-official API-shape anchors
1. Android WebView / WebViewClient API references
- Attempted via `web_fetch`, but Android Developers pages hit redirect-limit failures in this environment.
- Still useful as API-shape anchors from search results and prior source notes:
  - `WebViewClient.shouldOverrideUrlLoading(...)`
  - `WebView.loadUrl(...)`
  - WebView navigation / route handling boundaries
- Practical takeaway:
  - navigation callbacks are first-class analyst surfaces when the page hands control to native code by URL rather than object bridge.

### Practical implementation / discussion evidence
2. Search-layer results around `shouldOverrideUrlLoading(...)` and custom URL handling
- Useful result classes included:
  - implementation/discussion pages centered on `shouldOverrideUrlLoading(...)`
  - practical notes about custom schemes and links opened from WebView
  - community discussion that custom URL handling quirks can affect whether navigation callbacks fire consistently
- Quality:
  - mixed, weaker than official docs, but directionally useful for recurring workflow emphasis
- Practical takeaway:
  - URL / route / scheme handling is a realistic handoff family, and callback coverage/timing should be verified rather than assumed

3. Existing hybrid-app source notes already in the KB
- These were stronger than fresh web results for workflow synthesis.
- Durable signals retained:
  - hybrid ownership problems are often caused by confusing intent owner with transport owner
  - bridge-family-first reasoning is valuable, but object bridges are not the only family
  - response-handoff analysis already showed that hybrid loops are often asymmetric across directions
- Practical takeaway:
  - a dedicated note on navigation-driven handoff fits the existing practical sequence better than a broader abstract WebView taxonomy page

## Durable practical findings
### 1. Navigation itself can be the bridge family
A recurring pattern is:
- page JS or route logic builds a URL-like target
- WebView navigation boundary fires
- native router/deep-link handler parses the target
- native controller/request path takes over

This can happen through:
- `myapp://...`
- `jsbridge://...`
- `intent://...`
- ordinary `https://...` routes whose host/path/query select native behavior
- route reload/bootstrap patterns carrying lookup keys or encoded state

### 2. `shouldOverrideUrlLoading(...)` is often an intent boundary, not just a navigation detail
For reversing, the value is not only “what page is loading?”
The real value is often:
- what command or action is encoded in the URL?
- what payload fields survive in query/fragment/path before native parsing?
- which native dispatcher is selected next?

### 3. Navigation observation and request observation must be separated
A navigation callback may reveal:
- the page’s structured intent
- action ids
- challenge ids
- route-scene selection
- lookup keys for later native state recovery

But it may not itself show the final request transport.
This supports a practical split between:
- **navigation handoff boundary**
- **native request/transport boundary**

### 4. Custom URLs are easy to under-classify
Analysts often dismiss them as UI routing noise.
In practice they may carry:
- request role selection
- token seed references
- challenge context
- serialized payloads
- lookup keys into native state stores

### 5. First native parser is often more valuable than deep transport hooks
Once a raw URL is captured, the next best anchor is usually:
- route parser
- deep-link dispatcher
- action switch on scheme/path/query
- controller that maps URL fields into request or signing helpers

This often preserves more structure than jumping straight into later network/signature code.

## Workflow implications for the KB
A concrete workflow note should emphasize:
- target-vs-non-target action comparison
- custom-scheme / intent / `https` route / reload-refresh family split
- `shouldOverrideUrlLoading(...)` and `loadUrl(...)` as practical hook surfaces
- raw URL capture before native normalization
- separation of navigation handoff from later native request ownership
- failure diagnosis for “no object bridge visible” cases

## Candidate page created from this note
- `topics/webview-custom-scheme-and-navigation-handoff-workflow-note.md`

## Limits / cautions
- Fresh web evidence for Android API docs was partially blocked by `web_fetch` redirect failures in this environment.
- Search results were useful mainly for workflow emphasis and API-surface confirmation, not for strong claims about all implementations.
- The strongest grounding came from integrating existing KB hybrid notes with conservative API-shape evidence.
- Keep claims narrow: this is a recurring handoff family, not a universal explanation for all hybrid apps.