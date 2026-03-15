# WebView Custom-Scheme and Navigation-Handoff Workflow Note

Topic class: concrete workflow note
Ontology layers: mobile-practice branch, hybrid-app bridge methodology, navigation-driven native handoff diagnosis
Maturity: structured-practical
Related pages:
- topics/webview-native-mixed-request-ownership-workflow-note.md
- topics/webview-native-bridge-payload-recovery-workflow-note.md
- topics/webview-native-response-handoff-and-page-consumption-workflow-note.md
- topics/android-network-trust-and-pinning-localization-workflow-note.md
- topics/mobile-signature-location-and-preimage-recovery-workflow-note.md
- topics/browser-request-finalization-backtrace-workflow-note.md

## 1. Why this page exists
This page exists because hybrid Android investigations often miss one of the most practical WebView→native handoff families:
- no obvious `addJavascriptInterface(...)` bridge is found
- `postWebMessage(...)` or message-port usage is absent or sparse
- page actions still clearly trigger native behavior
- the real handoff is hidden inside navigation, custom schemes, deep links, route reloads, or URL-encoded command payloads

In these cases analysts often do one of three weak things:
- conclude there is “no bridge” because no object bridge is visible
- over-focus on `shouldInterceptRequest(...)` resource traffic and miss the control handoff
- notice `shouldOverrideUrlLoading(...)` but treat it as UI glue instead of the decisive request-intent boundary

This page is therefore not a generic WebView page.
It is a practical workflow note for recovering **navigation-driven page→native handoff** when URLs, schemes, fragments, or route transitions carry the decisive action.

## 2. Target pattern / scenario
### Representative target shape
A recurring navigation-handoff path looks like:

```text
page event / JS callback / button tap
  -> page builds navigation target
       - myapp://action?... 
       - jsbridge://...
       - intent://...
       - https://host/path#native_action=...
       - route reload carrying encoded bootstrap state
  -> WebView navigation boundary fires
       - shouldOverrideUrlLoading(...)
       - custom WebViewClient dispatch
       - loadUrl(...) / route mutation / deep-link router
  -> native dispatcher parses URL / query / fragment / command id
  -> native request builder / token helper / controller consumes parsed payload
  -> native transport or later page-return path continues
```

Common analyst situations:
- tapping a page button causes native auth/risk behavior even though no JS object bridge is visible
- the page changes `location.href`, opens a custom scheme, or reloads a route just before native code takes over
- `shouldInterceptRequest(...)` shows only ordinary page/resource traffic while the protected action happens elsewhere
- native code clearly receives action IDs or encoded blobs, but the analyst has not localized the page boundary where they were created
- custom URLs look like routing noise until compared against a non-target action

### Analyst goal
The practical goal is one or more of:
- prove that navigation itself is the bridge family
- capture the raw URL/route payload before native parsing destroys structure
- separate cosmetic navigation from operational native dispatch
- identify the first native parser/dispatcher after `shouldOverrideUrlLoading(...)`
- decide whether the next bottleneck is payload decoding, request ownership, signing, or native→page return path analysis

## 3. The first five questions to answer
Before deepening native tracing, answer these:

1. **Which exact page action causes the navigation-style handoff?**
2. **Is the decisive boundary a custom scheme, an `intent://` style URL, a normal `https://` route with encoded action data, or a reload/bootstrap refresh?**
3. **Does `shouldOverrideUrlLoading(...)` fire for the target action, and if not, which adjacent navigation/load boundary does?**
4. **What structure is still visible in the raw URL: action id, route, token seed, challenge id, JSON blob, base64 payload, or lookup key?**
5. **Which native parser or dispatcher consumes the URL next?**

These questions usually solve the case faster than broad hook expansion.

## 4. Practical workflow

### Step 1: compare one target action and one nearby non-target action
Do not reason about all page navigation.
Pick:
- one page action that leads to the protected/native behavior that matters
- one nearby action that does not

Record for each:
- visible trigger
- whether navigation happens
- exact URL / route / fragment / scheme
- whether `shouldOverrideUrlLoading(...)` fires
- which native code path follows

Useful scratch note:

```text
Action A: tap protected submit
  navigation: myapp://risk/submit?action=login&payload=...
  override callback: yes
  next native path: Router.dispatch() -> RiskController.start()

Action B: tap ordinary help link
  navigation: https://help.example.com/faq
  override callback: no / external open only
  next native path: none

initial conclusion:
  navigation callback is not generic UI glue; it is the request-intent bridge for the protected flow
```

### Step 2: classify the navigation handoff family
In practice, most page→native navigation bridges fall into four practical families.

#### Case A: custom-scheme action bridge
Signs:
- `myapp://...`, `jsbridge://...`, `app://...`
- action name and arguments encoded in host/path/query
- native router dispatches by scheme/path

#### Case B: `intent://` or deep-link dispatch bridge
Signs:
- `intent://...` style URLs or Android deep-link wrappers
- action ultimately resolves to app-native handler or route dispatcher
- payload may be partly encoded in extras-like fields

#### Case C: normal `https://` route carrying command state
Signs:
- no custom scheme, but route/query/fragment contains action selector or encoded blob
- WebViewClient/router treats specific hosts/paths as native handoff triggers
- analyst might misclassify it as ordinary web navigation

#### Case D: reload/bootstrap refresh carrying lookup state
Signs:
- route reload or `loadUrl(...)` mutation appears to refresh the page
- decisive state is carried in query keys, fragments, storage side effects, or bootstrap IDs
- native code then looks up fuller state from another store/controller

Do not assume bridge family means only JS objects or message ports.

### Step 3: capture the raw navigation payload before parsing
This is the highest-value move.
The best evidence is often the last raw URL before native code normalizes it.

Capture:
- full raw URL
- scheme / host / path / query / fragment
- whether values are URL-encoded, base64-ish, JSON-ish, or lookup-key shaped
- timing relative to the user action and next native dispatcher call

Representative capture template:

```text
navigation handoff family:
  custom-scheme / intent / https-route / reload-refresh

raw url:
  ...

fields visible before parse:
  action, route, challengeId, tokenSeed, scene, ts, payload, sigRef

first native parser:
  shouldOverrideUrlLoading / Router.parse / DeepLinkHandler.handle

expected next effect:
  request build / token generation / native page transition / another bridge round trip
```

### Step 4: separate navigation observation from request observation
This distinction matters.
A navigation bridge may carry the decisive **intent**, even when the decisive **request** happens later in native code.

Useful split:

```text
navigation boundary:
  where page intent crosses toward native code

request boundary:
  where native/client transport is actually selected or emitted
```

If you only watch WebView requests, you may miss the true handoff.
If you only watch native requests, you may miss the structured preimage carried in the URL.

### Step 5: follow the first native parser/dispatcher, not the deepest transport path
Once the raw URL is captured, the next best move is usually the **first native consumer**:
- URL parser
- route dispatcher
- deep-link handler
- action switch on path/query fields
- controller that converts URL fields into request-builder arguments

This often preserves more structure than jumping directly into later network/signature code.

## 5. Where to place breakpoints / hooks

### A. Page-side navigation creation boundary
Use when:
- you know the page action but not how the navigation target is built
- route strings or custom URLs may be composed dynamically in JS

Inspect:
- `location.href` assignments
- anchor/button handlers
- route helper functions
- whether the URL is assembled from token/state fields immediately before navigation

### B. `loadUrl(...)` / navigation-issue boundary
Use when:
- native code itself may be triggering or mutating the route
- reload/bootstrap refresh behavior is suspected

Inspect:
- outbound URL string
- whether route changes correlate to later native parsing or later page bootstrap reads

### C. `shouldOverrideUrlLoading(...)` / navigation-override boundary
Use when:
- custom-scheme or route-based handoff is likely
- you need the earliest reliable native-visible navigation event

Inspect:
- full raw URL
- return behavior (`true`/`false`) if observable
- whether target and non-target actions diverge here
- which parser/dispatcher is called next

Representative pseudocode sketch:
```javascript
// sketch only
Java.perform(function () {
  const WVC = Java.use('android.webkit.WebViewClient');
  WVC.shouldOverrideUrlLoading.overload('android.webkit.WebView', 'java.lang.String').implementation = function (wv, url) {
    console.log('nav-handoff', url);
    return this.shouldOverrideUrlLoading(wv, url);
  };
});
```

### D. Native URL parser / route-dispatch boundary
Use when:
- the raw URL is known
- you need to preserve fields before they are normalized into opaque controller arguments

Inspect:
- decoded query/fragment fields
- path-to-handler mapping
- whether lookup keys reference richer state elsewhere
- whether the next consumer is request-building, token-generation, or UI routing only

### E. First request-driving consumer boundary
Use when:
- you already know the navigation handoff is real
- you need to see how URL-derived fields become request parameters or signing inputs

Inspect:
- argument mapping from parsed route fields into request helpers
- whether target and non-target URLs reach different consumers
- whether the decisive downstream path is network, challenge, or page-return oriented

## 6. Representative code / pseudocode / harness fragments

### Navigation-handoff recording template
```text
page action:
  tap login / continue challenge / submit form

handoff family:
  custom-scheme / intent / https-route / reload-refresh

raw navigation target:
  ...

native override boundary:
  shouldOverrideUrlLoading / loadUrl / router callback

first native parser:
  ...

decoded fields:
  action, route, challengeId, payloadRef, scene, ts

next bottleneck:
  payload decode / request ownership / signing / response handoff
```

### Minimal mental model
```python
# sketch only
class NavigationHandoff:
    page_action = None
    family = None           # custom-scheme / intent / https-route / reload
    raw_target = None
    override_boundary = None
    first_parser = None
    decoded_fields = None
    next_owner = None
```

The point is to keep navigation-driven handoff explicit rather than treating it as background noise.

## 7. Likely failure modes

### Failure mode 1: analyst concludes there is no bridge because `addJavascriptInterface` is absent
Likely causes:
- handoff is route/navigation-driven
- custom scheme or `https` route is acting as the bridge

Next move:
- inspect navigation creation and `shouldOverrideUrlLoading(...)` before concluding page/native separation

### Failure mode 2: analyst over-trusts `shouldInterceptRequest(...)`
Likely causes:
- protected action is carried as navigation intent, not as page-owned request transport
- WebView request observation sees assets/noise but not the decisive handoff

Next move:
- treat navigation callbacks as a separate observation surface from request callbacks

### Failure mode 3: custom URLs are dismissed as UI routing only
Likely causes:
- action id, lookup key, or serialized payload is encoded into path/query/fragment
- first meaningful native consumer sits immediately behind the route parser

Next move:
- compare target vs non-target custom URLs and follow the first native dispatcher

### Failure mode 4: raw URL is captured, but the case still feels opaque
Likely causes:
- URL only contains a lookup key, not the full payload
- richer state is retrieved from storage/controller after route parse

Next move:
- hook the first parser/dispatcher and any follow-on lookup/read site before deepening transport hooks

### Failure mode 5: navigation is real, but the analyst still cannot explain later behavior
Likely causes:
- navigation solved intent handoff, but not transport ownership or response-consumer localization
- native code may send the request, then hand the result back to the page later

Next move:
- route forward into request-ownership, signature-location, or native→page response-handoff workflows

## 8. Environment assumptions
Hybrid Android apps often use navigation not only for visible page movement, but also for:
1. command selection
2. bridge payload transport
3. native route dispatch
4. bootstrap-state lookup
5. transition into later network/signature/challenge paths

This page focuses on the early and mid stages where the URL still preserves analyst-valuable structure.

## 9. What to verify next
Once navigation-driven handoff is localized, verify:
- whether the raw URL itself contains the decisive preimage or only a lookup key
- whether the first native consumer is a router, request builder, token helper, or page-transition controller
- whether the next bottleneck is native transport ownership, signature recovery, or native→page return-path analysis
- whether target and non-target actions differ by scheme/path/query fields or only by later lookup results

## 10. How this page connects to the rest of the KB
Use this page when the first bottleneck is **navigation/custom-scheme handoff localization**.
Then route forward based on what you find:

- if the broader hybrid question is still unresolved:
  - `topics/webview-native-mixed-request-ownership-workflow-note.md`
- if the next bottleneck is recovering structured page→native arguments across bridge families:
  - `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- if the next bottleneck is native transport ownership or Cronet ambiguity:
  - `topics/cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note.md`
- if the next bottleneck is URL-derived signing / request field recovery:
  - `topics/mobile-signature-location-and-preimage-recovery-workflow-note.md`
- if the next bottleneck is native→page return after native processing:
  - `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`

This page is meant to sit between broad hybrid ownership diagnosis and deeper payload/request/signature analysis.

## 11. What this page adds to the KB
This page adds grounded material the mobile subtree needed more of:
- explicit treatment of navigation/custom-scheme handoff as a first-class bridge family
- breakpoint placement centered on `shouldOverrideUrlLoading(...)`, `loadUrl(...)`, and first native URL parsers
- separation of navigation intent from request transport
- failure diagnosis for “no object bridge visible” cases
- a concrete workflow for preserving URL-carried structure before native normalization destroys it

It is intentionally closer to real hybrid-app debugging than to a generic WebView overview.

## 12. Source footprint / evidence note
Grounding for this page comes mainly from:
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-mixed-request-ownership-notes.md`
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-bridge-payload-recovery-notes.md`
- search-layer results around `shouldOverrideUrlLoading(...)`, custom schemes, and WebView navigation handling
- Android WebView API shapes and practical custom-URL handling discussions surfaced during search

This page intentionally stays conservative:
- it does not claim every hybrid app uses custom schemes
- it treats route/navigation-based handoff as one recurring family among several
- it focuses on workflow boundaries and evidence preservation, not one-size-fits-all hook recipes

## 13. Topic summary
WebView custom-scheme and navigation-handoff localization is a practical workflow for hybrid Android cases where page intent crosses into native behavior through URLs, route changes, deep links, or navigation callbacks rather than obvious JS object bridges.

It matters because analysts often miss the decisive handoff when no `addJavascriptInterface(...)` surface is visible. The faster route is usually to compare one target action against one non-target action, capture the raw navigation target, localize `shouldOverrideUrlLoading(...)` or adjacent route boundaries, preserve the last URL-carried structure before native parsing, and then follow the first native dispatcher into request ownership, signing, or response-handoff analysis.