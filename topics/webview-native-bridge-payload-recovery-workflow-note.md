# WebView / Native Bridge Payload Recovery Workflow Note

Topic class: concrete workflow note
Ontology layers: mobile-practice branch, hybrid-app bridge methodology, payload-handoff recovery
Maturity: structured-practical
Related pages:
- topics/webview-native-mixed-request-ownership-workflow-note.md
- topics/mobile-signature-location-and-preimage-recovery-workflow-note.md
- topics/cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note.md
- topics/android-network-trust-and-pinning-localization-workflow-note.md
- topics/mobile-protected-runtime-subtree-guide.md
- topics/android-observation-surface-selection-workflow-note.md

## 1. Why this page exists
This page exists because hybrid Android analysis often gets stuck one step after ownership diagnosis.

The analyst already knows or strongly suspects:
- page logic matters
- native code matters too
- the decisive action crosses a WebView/native boundary

At that point, the real bottleneck is usually no longer “is this WebView or native?”
It is:

**What exact payload crosses the bridge, how is it shaped, and which native consumer receives it next?**

Without that step, analysts often do one of three weak things:
- keep tracing broad WebView traffic without catching the handoff payload
- jump too far downstream into native request code after structure has already been lost
- capture final opaque tokens without preserving the structured arguments that explain them

This page is therefore not a WebView security page and not a broad hybrid taxonomy page.
It is a practical workflow note for recovering the payload that crosses the JS/native bridge.

## 2. Target pattern / scenario
### Representative target shape
A recurring hybrid path looks like:

```text
page event / JS wrapper / embedded app script
  -> bridge payload created
  -> handoff surface used
       - addJavascriptInterface
       - WebMessage / message port
       - custom URL / navigation callback
  -> native side parses or normalizes payload
  -> native request/token/controller path consumes payload
  -> downstream transport or response logic continues
```

Common analyst situations:
- the page clearly triggers the protected action, but the final request only appears from native code
- WebView callbacks show user-flow timing, but not the decisive request parameters
- a token appears native-generated, yet the page obviously supplied action or context first
- custom scheme URLs or message posts appear, but they are dismissed as UI glue rather than a real request handoff path

### Analyst goal
The practical goal is one or more of:
- identify the exact bridge family in use
- capture arguments at the handoff boundary before structure is lost
- separate payload recovery from later transport ownership questions
- align one page action with one native consumer path
- decide whether the next bottleneck is bridge decoding, request ownership, trust-path localization, or preimage recovery

## 3. The first five questions to answer
Before deeper native tracing, answer these:

1. **Which exact page action or state transition causes the bridge handoff?**
2. **Which bridge family is used: object bridge, message channel, or custom URL/navigation?**
3. **What is the argument shape at the first native-visible boundary?**
4. **Is the payload still structured there, or already encoded/packed?**
5. **Which native consumer receives it next: request wrapper, token helper, routing controller, or response bridge?**

These five questions usually narrow the case faster than deeper blind hooks.

## 4. Practical workflow

### Step 1: anchor one target page action and one non-target action
Do not reason about bridge traffic in bulk.
Pick:
- one page action that leads to the behavior that matters
- one nearby action that does not

Record for each:
- visible page trigger
- whether a bridge boundary fires
- which bridge method/message/URL is used
- argument shape
- which native code path appears immediately after

Useful scratch note:

```text
Action A: tap protected submit
  bridge: NativeBridge.submitAction(json)
  args: {"route":"/api/foo","token":"...","scene":"risk_submit"}
  next native path: request wrapper + token helper

Action B: tap ordinary refresh
  bridge: NativeBridge.logEvent(json)
  args: {"event":"refresh"}
  next native path: analytics only

initial conclusion:
  bridge family is shared, but only one method/payload shape feeds the protected request path
```

### Step 2: identify the bridge family before deep payload parsing
In practice, most hybrid handoffs fall into three families.

#### Case A: `addJavascriptInterface` object bridge
Signs:
- WebView registers a Java object under a JS-visible name
- page JS calls `window.<name>.<method>(...)`
- native entry is a Java/Kotlin method with structured args or a string blob

#### Case B: `WebMessage` / `WebMessagePort` / message-channel bridge
Signs:
- no obvious object bridge, but page/native messages are exchanged
- channel creation or message handlers exist on both sides
- payload may arrive as stringified JSON or small command envelopes

#### Case C: custom URL / navigation bridge
Signs:
- page triggers `myapp://...` or encoded navigation actions
- `shouldOverrideUrlLoading(...)` or a URL parser dispatches native behavior
- payload may be URL-encoded rather than passed as ordinary method arguments

Do not assume “no `addJavascriptInterface`” means “no bridge”.

### Step 3: capture registration first, invocation second
Before decoding every payload, capture the registration boundary.
That often reveals names and structure for free.

High-yield registration surfaces:
- `addJavascriptInterface(obj, name)`
- message channel creation / callback registration
- WebView client attachment for navigation handoff paths
- custom URL dispatch registration in WebView client or bridge controller code

Then capture invocation boundaries:
- exposed bridge methods at method entry
- message receive callbacks
- `shouldOverrideUrlLoading(...)` arguments and post-parse handlers

Why this order helps:
- registration gives naming and topology
- invocation gives timing and payload
- together they explain the handoff without requiring full app-wide tracing

### Step 4: preserve payload shape before native normalization
This is the core move.
The most useful capture is usually not the final opaque output.
It is the last still-structured payload.

Typical useful shapes:
- raw JSON string
- route + action + metadata tuple
- URL with encoded query payload
- token seed + request role + session fields
- command envelope with `type`, `id`, and `payload`

Representative payload-shape template:

```text
bridge family:
  addJavascriptInterface / message port / custom URL

bridge name:
  NativeBridge / postMessage / myapp://action

payload shape:
  json-string / scalar / url-encoded / mixed

fields seen:
  action, route, tokenSeed, challengeId, requestBodyDigest, ts

first native consumer:
  RequestDispatcher.handle() / TokenHelper.sign() / Router.open()
```

If native code immediately re-packs the payload, this capture can still preserve the preimage for later signing or routing analysis.

### Step 5: separate payload recovery from transport ownership
Once payload capture is working, ask a separate question:
- which native path consumes it next?

Possible next owners include:
- native request builder
- token/signature helper
- transport selector
- WebView response callback path
- controller that decides whether to route the request back into page logic or out to native networking

This matters because bridge capture can prove **intent handoff** without yet proving final **transport ownership**.

## 5. Where to place breakpoints / hooks

### A. Bridge registration boundary
Use when:
- you still need to discover the bridge family and naming
- object names, exposed methods, or channel topology are still unknown

Inspect:
- bridge object name
- Java class name
- exposed method list where possible
- channel creation timing
- which WebView instance registers the bridge

Representative pseudocode sketch:
```javascript
// sketch only
Java.perform(function () {
  const WebView = Java.use('android.webkit.WebView');
  WebView.addJavascriptInterface.overload('java.lang.Object', 'java.lang.String').implementation = function (obj, name) {
    console.log('bridge-register', name, obj.$className || obj);
    return this.addJavascriptInterface(obj, name);
  };
});
```

### B. Bridge invocation boundary
Use when:
- you know the registration site or bridge class
- you need the actual per-action payloads

Inspect:
- method name
- argument count and types
- raw argument values before parsing
- alignment with the user/page action

Representative pseudocode sketch:
```javascript
// sketch only
Java.perform(function () {
  const Bridge = Java.use('com.example.NativeBridge');
  Bridge.submitAction.overload('java.lang.String').implementation = function (arg) {
    console.log('bridge-call submitAction', arg);
    return this.submitAction(arg);
  };
});
```

### C. Message-channel receive boundary
Use when:
- `addJavascriptInterface` is absent or unimportant
- page/native messaging still clearly occurs

Inspect:
- message body
- sender/receiver timing
- whether messages are plain JSON, command envelopes, or encoded blobs
- which handler consumes the message next

### D. Custom URL / `shouldOverrideUrlLoading(...)` boundary
Use when:
- page logic signals native code through navigation
- you suspect custom-scheme or encoded route handoff

Inspect:
- raw URL
- decoded parameters
- whether the URL selects an action, transports a payload, or both
- what parser/dispatcher handles it next

Representative pseudocode sketch:
```text
hook shouldOverrideUrlLoading(...)
  record raw URL
  parse scheme / host / path / query
  correlate with next native dispatcher call
```

### E. First native consumer boundary
Use when:
- bridge payload capture works
- you need to know what the native side does with it next

Inspect:
- whether it enters request assembly, token generation, routing, or response handling
- whether structure is lost here
- whether target and non-target actions diverge at this boundary

## 6. Representative code / pseudocode / harness fragments

### Bridge payload recording template
```text
page action:
  tap submit / open page / solve challenge / continue login

bridge family:
  object / message / custom-url

registration site:
  addJavascriptInterface / createWebMessageChannel / WebViewClient

invocation site:
  method / callback / shouldOverrideUrlLoading

payload shape:
  json / url / scalar / mixed

first native consumer:
  request helper / token helper / router / analytics

next bottleneck:
  payload decode / request ownership / signature preimage / trust path
```

### Minimal mental model
```python
# sketch only
class BridgeEvent:
    page_action = None
    family = None            # object / message / custom-url
    registration_site = None
    invocation_site = None
    payload_shape = None     # json / url / scalar / mixed
    first_native_consumer = None
```

The point is to make the bridge handoff explicit rather than intuitive.

## 7. Likely failure modes

### Failure mode 1: analyst captures final native token but not bridge payload
Likely causes:
- hooks are too far downstream
- structure is lost after native normalization or packing

Next move:
- move outward to bridge invocation and first native consumer boundaries
- preserve the last structured payload, not just the final field

### Failure mode 2: analyst over-focuses on WebView request callbacks
Likely causes:
- `shouldInterceptRequest(...)` and page callbacks reveal timing but not the handoff payload
- decisive data crosses through a bridge, not through visible page transport

Next move:
- inspect bridge registration and invocation instead of deepening only page-side network observation

### Failure mode 3: analyst assumes no bridge because `addJavascriptInterface` is absent
Likely causes:
- message-channel bridge in use
- custom-URL/navigation handoff in use

Next move:
- inspect message-port APIs and navigation overrides before concluding that page and native sides are independent

### Failure mode 4: custom URLs are dismissed as navigation noise
Likely causes:
- payload encoded into query/path parameters
- URL only used as an action selector for a later native payload lookup

Next move:
- decode the full URL and correlate it with the next native dispatcher call

### Failure mode 5: bridge payload is captured, but the next step is still unclear
Likely causes:
- payload recovery solved intent handoff, but not transport ownership
- native consumer path still fans out into multiple request families or controllers

Next move:
- route into request ownership or preimage recovery workflows based on the first native consumer

## 8. Environment assumptions
Hybrid Android apps often split work across:
1. page-triggered intent
2. bridge payload formation
3. native-side normalization or routing
4. transport ownership
5. response consumption

This page focuses mainly on step 2 and the start of step 3.
That is often the point where the most useful structure is still visible.

## 9. What to verify next
Once bridge payload capture is working, verify:
- whether target and non-target page actions use different bridge methods or payload fields
- whether the first native consumer is a request builder, token helper, or routing/controller layer
- whether the payload already contains the decisive request preimage
- whether the next real bottleneck is transport ownership, trust-path localization, or downstream signature generation

## 10. How this page connects to the rest of the KB
Use this page when the first bottleneck is **recovering what crosses the WebView/native bridge**.
Then route forward based on what you find:

- if the next bottleneck is hybrid ownership classification:
  - `topics/webview-native-mixed-request-ownership-workflow-note.md`
- if the next bottleneck is request transport ownership or Cronet ambiguity:
  - `topics/cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note.md`
- if the next bottleneck is trust / pinning after native handoff:
  - `topics/android-network-trust-and-pinning-localization-workflow-note.md`
- if the next bottleneck is field generation or structured preimage capture downstream:
  - `topics/mobile-signature-location-and-preimage-recovery-workflow-note.md`

This page is meant to sit between broad hybrid ownership diagnosis and deeper native request/signature/trust analysis.

## 11. What this page adds to the KB
This page adds grounded material the mobile subtree needed more of:
- bridge-family-first reasoning
- payload-shape capture before native normalization
- equal treatment of object bridges, message channels, and custom-URL handoff
- hook placement centered on registration, invocation, and first-consumer boundaries
- explicit separation of bridge payload recovery from later transport ownership

It is intentionally closer to real hybrid-app debugging than to WebView theory.

## 12. Source footprint / evidence note
Grounding for this page comes mainly from:
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-bridge-payload-recovery-notes.md`
- Android Developers guidance on WebView native bridges
- Android WebView API reference for message-channel primitives
- OWASP MASTG bridge examples showing canonical `addJavascriptInterface` usage
- practical custom-URL / navigation-handoff evidence around `shouldOverrideUrlLoading(...)`

This page intentionally stays conservative:
- it does not claim every hybrid framework uses the same bridge family
- it focuses on recurring workflow boundaries and payload-capture tactics
- it treats bridge capture as a mid-case analyst step, not as complete explanation of the whole network path

## 13. Topic summary
WebView / native bridge payload recovery is a practical workflow for hybrid Android cases where the page and native sides clearly interact, but the decisive analyst need is to capture what crosses the bridge before structure is lost.

It matters because analysts often hook too early on the page side or too late on the native side. The faster route is usually to identify the bridge family, capture registration and invocation, preserve the last structured payload, and then follow the first native consumer into request ownership, trust, or signature recovery as needed.
