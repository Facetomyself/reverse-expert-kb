# Android WebView / Native Bridge Payload Recovery Notes

Date: 2026-03-15
Topic: mobile runtime instrumentation, hybrid app reversing, WebView/native bridge payload capture, JS/native handoff diagnosis

## Scope
These notes support a concrete KB workflow page on **WebView/native bridge payload recovery**.

This is narrower than general hybrid request ownership.
The goal is to preserve analyst leverage for a recurring mid-case bottleneck:
- the analyst already suspects a JS/native bridge is involved
- WebView presence alone is no longer the real question
- the next practical need is to capture what crosses the bridge, in what shape, and how that handoff changes the next hook location

The page should stay workflow-centered rather than becoming a generic WebView security overview.

## Source cluster consulted

### 1. Android Developers — WebView native bridges risk guidance
- URL: https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridges
- Quality: official platform/security guidance, not a reversing guide, but strong for durable bridge-model anchors.
- Durable signals retained:
  - `addJavascriptInterface` creates an explicit JS↔Java communication surface.
  - message-channel style communication is a first-class alternative bridge family.
  - apps using these surfaces should be reasoned about as explicit cross-boundary systems, not as pure page logic.
- Practical analyst takeaway:
  - for reversing, bridge registration and invocation are not just security smells; they are ownership and payload checkpoints.

### 2. Android WebView API reference
- URL: https://developer.android.com/reference/android/webkit/WebView
- Quality: official API reference.
- Durable signals retained:
  - WebView exposes message-channel primitives such as `createWebMessageChannel()` and `postWebMessage(...)`.
  - bridge/handoff analysis should include message-port style paths, not just `addJavascriptInterface`.
- Practical analyst takeaway:
  - when `addJavascriptInterface` is absent, the handoff may still be happening through message channels and should not be misclassified as “no bridge”.

### 3. OWASP MASTG — Testing for Java objects exposed through WebViews
- URL: https://mas.owasp.org/MASTG/tests/android/MASVS-PLATFORM/MASTG-TEST-0033/
- Quality: security-testing guide rather than RE workflow, but useful because it preserves concrete Java/JS bridge examples.
- Durable signals retained:
  - canonical `addJavascriptInterface` usage shape
  - `window.<name>.<method>(...)` invocation model from JS side
  - bridge methods often expose structured arguments or return values that can be aligned with page actions
- Practical analyst takeaway:
  - bridge object name and exposed method shape are high-value anchors for payload recovery and stack alignment.

### 4. Custom-URL / `shouldOverrideUrlLoading(...)` practical evidence
- Representative surfaced result:
  - https://github.com/facebook/react-native/issues/10055
- Quality: implementation/problem evidence, not formal docs.
- Durable signals retained:
  - custom URL schemes often act as lightweight bridge/handoff paths
  - `shouldOverrideUrlLoading(...)` is a practical observation boundary when page JS or embedded content signals native code through navigation-style payloads
- Practical analyst takeaway:
  - not every WebView/native handoff uses object bridges; some use navigation-encoded payloads or action IDs.

### 5. Existing KB practical notes
- `topics/webview-native-mixed-request-ownership-workflow-note.md`
- `topics/mobile-signature-location-and-preimage-recovery-workflow-note.md`
- `topics/cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note.md`
- Quality: internal structured synthesis.
- Durable signals retained:
  - ownership diagnosis improves when intent owner, bridge boundary, transport owner, and response consumer are separated.
  - practical value comes from request-family-first reasoning, compare-run discipline, and capture-before-transform methodology.

## Practical synthesis

### Stable target/problem shape
A recurring hybrid Android path is:

```text
page event / WebView state change
  -> bridge payload created in JS or page wrapper
  -> bridge handoff surface used
       - addJavascriptInterface
       - WebMessage / message port
       - custom URL / shouldOverrideUrlLoading
  -> native side parses / normalizes payload
  -> native request builder, token helper, or transport owner consumes it
```

### Strongest durable analyst anchors
1. **Bridge registration surface**
   - object name, exposed methods, message-port creation, navigation callback registration
2. **Bridge invocation timing**
   - which user/page action precedes the handoff
3. **Argument shape**
   - raw string, JSON string, action ID + blob, token + route + metadata, URL-encoded command
4. **Post-bridge consumer**
   - native request wrapper, token helper, routing controller, trust/transport selector, response-to-page callback
5. **Lossy transformation boundary**
   - whether structured payload becomes opaque immediately after crossing to native code

### Recurring bridge families worth preserving

#### A. `addJavascriptInterface` object bridge
- Typical sign:
  - WebView registers a Java object under a JS-visible name.
- High-value capture points:
  - registration site
  - exposed method names
  - arguments at method entry
- Typical analyst use:
  - align page action -> bridge method -> native request/token path

#### B. Message-channel / `WebMessagePort` / `postWebMessage`
- Typical sign:
  - no obvious JS object bridge, but page/native messages still flow bidirectionally.
- High-value capture points:
  - channel creation
  - message post/send boundaries
  - callback handlers receiving message bodies
- Typical analyst use:
  - recover page-generated structured payloads when the app avoids direct object exposure.

#### C. Custom-URL / navigation bridge
- Typical sign:
  - page uses `myapp://...`, custom schemes, or encoded navigation actions.
- High-value capture points:
  - `shouldOverrideUrlLoading(...)`
  - URL parse/dispatch boundary in native code
- Typical analyst use:
  - recover action names, IDs, or serialized payloads carried in navigation rather than explicit JS method calls.

### High-value distinctions

#### Distinction 1: bridge payload capture is not the same as transport ownership
Capturing bridge arguments can show:
- the page’s request intent
- token or state material before native processing
- request role selection

But it does **not** by itself prove:
- which network stack finally sends the request
- whether the same payload feeds one or multiple native clients

#### Distinction 2: structured payload often matters more than final token
If the bridge hands over:
- action name
- route
- JSON config
- request body fragment
- session/challenge state

then the analyst usually gains more by preserving that structured payload than by only capturing the final downstream opaque field.

#### Distinction 3: custom URL bridges are easy to under-classify
Analysts may treat them as navigation noise.
In practice, they can carry the decisive action selector or serialized token/context blob.

### Evidence-backed practical recommendations
- Once hybrid ownership is suspected, inspect bridge registration before deepening broad WebView or native hooks.
- Record bridge object names, method names, and argument shapes as first-class evidence.
- Compare one target page action with one non-target page action to see which bridge methods diverge.
- Preserve structured payloads before the native side re-packs, hashes, or normalizes them.
- Treat message-channel and custom-URL handoff as equal-class bridge families, not edge cases.

## Representative artifacts worth preserving in the KB
- bridge registration record: object name / method / channel / callback
- bridge invocation record: timestamp, page trigger, argument shape
- payload-shape note: JSON / scalar / URL / encoded blob / mixed
- post-bridge consumer note: request builder / token helper / controller / transport selector
- compare-run note: target action vs non-target action at bridge boundary

## Conservative evidence note
These notes intentionally avoid claiming one universal hybrid bridge architecture.
The source cluster justifies a workflow page well because it strongly supports:
- JS/native bridge surfaces as recurring analyst checkpoints
- message channels as important non-`addJavascriptInterface` handoff paths
- custom-URL/navigation callbacks as practical bridge alternatives
- payload-shape capture as a durable RE tactic

It does **not** justify overclaiming exact internals for all hybrid frameworks.
The resulting KB page should therefore stay narrow, concrete, and workflow-centered.
