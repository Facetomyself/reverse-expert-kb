# iOS URL Loading Interception and First Consumer Workflow Note

Topic class: workflow note
Ontology layers: iOS runtime, URL loading, request interception, first consumer proof
Maturity: practical
Related pages:
- topics/ios-practical-subtree-guide.md
- topics/mobile-reversing-and-runtime-instrumentation.md
- topics/ios-trust-path-and-pinning-localization-workflow-note.md
- topics/webview-native-mixed-request-ownership-workflow-note.md
Related source notes:
- sources/mobile/2026-04-05-ios-url-loading-interception-and-first-consumer-notes.md
- sources/ios/2026-04-23-ios-url-loading-protocolclasses-and-scheme-handler-realism-notes.md

## 1. What this note is for
Use this note when an iOS target already plausibly depends on **URL-loading interception or custom URL-loading ownership**, but the investigation still lacks the first trustworthy consumer boundary that turns visible protocol registration, scheme handling, or delegate presence into actual behavior ownership.

Typical situations:
- a custom `URLProtocol`/`NSURLProtocol` subclass is visible, but you still do not know whether the request that matters actually flowed through it
- `protocolClasses` or shared-session interception is visible, but current-session/configuration truth is still unclear
- a `WKURLSchemeHandler` exists, but the real missing step is which first handler path actually supplied the resource/page-visible result
- a URL-loading delegate / challenge path is visible, but request interception, trust handling, and later response ownership are still being flattened together

This note is for the narrower question:

```text
Which first URL-loading interception or scheme-handling consumer actually owns the request/response behavior that matters?
```

Not the broader question:

```text
Does this app use custom URL loading or interception at all?
```

## 2. When to use it
Use this note when most of the following are true:
- the broad mobile/runtime problem has already narrowed specifically into iOS URL-loading interception, custom protocol registration, or WebKit scheme handling
- one candidate interception family is already visible
- the main uncertainty is whether **registration truth**, **current-session / current-webview ownership truth**, **interception-selection truth**, **first consumer truth**, or **later visible consequence truth** actually owns the claim you care about
- the next useful output is one smaller trustworthy chain such as:
  - protocol registration -> current session/config -> `canInit(with:)` match -> `startLoading()` -> visible request/response consequence
  - scheme-handler registration -> current `WKWebView` config -> `webView(_:start:)` / `WKURLSchemeTask` progress -> synthetic/modified resource -> page-visible consequence
  - delegate/trust path -> request continues -> later response ownership, once trust-handling is already narrowed enough to hand off here

Do **not** start here when:
- the real bottleneck is still broad iOS trust/pinning localization rather than interception ownership
- the real question is still mixed WebView/native ownership without evidence of iOS URL-loading interception
- interception selection is already proved and the real missing step is later parser/business-logic consequence outside the URL-loading seam

## 3. Core claim
A recurring iOS/network-reversing mistake is to stop too early at one of these milestones:
- “a custom `NSURLProtocol` subclass exists”
- “`URLProtocol.registerClass(...)` succeeded, so the request must be mine”
- “`protocolClasses` is configured, so this session must use the custom protocol”
- “a `WKURLSchemeHandler` exists, so the resource path is solved”
- “the app has URLSession/WebView delegate code, so it must own this request”

The smaller reusable target is still:

```text
interception family exists
  != current session/webview uses it
  != relevant request was selected by it
  != first interception consumer proved
  != later visible request/response consequence truth
```

But the practical branch now also needs two thinner ladders kept explicit.

For Foundation / `URLProtocol` / `URLSession` cases:

```text
global registerClass or protocolClasses visibility
  != current session/config carries the class
  != default protocols fell through to the custom class
  != canInit(with:) selected the request
  != canonicalRequest(for:) / cache-equivalence truth
  != startLoading() first consumer truth
  != later visible consequence
```

For WebKit custom-scheme cases:

```text
scheme handler registered
  != current WKWebViewConfiguration owns that handler
  != current resource uses a scheme WebKit delegates to custom handlers
  != webView(_:start:) fired for this resource
  != resource still needed / not yet stopped
  != page-visible consequence truth
```

## 4. Boundary objects to keep separate
### A. Registration truth
Visible objects:
- `URLProtocol.registerClass(...)`
- `URLSessionConfiguration.protocolClasses`
- `WKWebViewConfiguration.setURLSchemeHandler(_:forURLScheme:)`
- delegate attachment / ownership scaffolding

Useful reminder:
- Apple documents `registerClass(...)` as making the subclass visible to the URL loading system, but the system only uses the first class whose `canInit(with:)` returns true and does **not** guarantee that all registered classes are consulted.
- Apple documents `protocolClasses` as session-local extra protocol classes and says `URLSession` checks default protocols first.
- Apple documents `setURLSchemeHandler(_:forURLScheme:)` as configuration-local registration for custom schemes and treats built-in WebKit-owned schemes like `https` as programmer-error cases.

This is all weaker than proof that the current request path actually used the registration that matters.

### B. Current-owner truth
Useful questions:
- is the request using the shared session or a custom configuration?
- does the current `URLSessionConfiguration` actually include the protocol class you care about?
- is the current session a background session, where Apple says custom `URLProtocol` subclasses do not apply?
- is the current `WKWebViewConfiguration` the one with the relevant scheme handler attached?
- is the current request path even eligible for this protocol/scheme family, or is it still a WebKit-owned scheme like `https` that ordinary `WKURLSchemeHandler` registration cannot own?

This matters because “interceptor exists” is weaker than “the current request path is owned by it.”

### C. Interception-selection truth
Typical smaller truths:
- one `canInit(with:)` / eligibility method actually selected the request
- one session really fell through its default protocol handling into the custom class
- one `canonicalRequest(for:)` normalization / cache-equivalence question is now stable enough not to lie about apparently similar requests
- one scheme family really resolved into `webView(_:start:)`
- one current configuration/session/webview path actually routes here rather than to default loading

Do not flatten “request looks similar” into “this interceptor owned it.”

### D. First consumer truth
This is the first method/path that turns the request into meaningful app behavior.
Typical shapes:
- `startLoading()` in a `URLProtocol` subclass
- `webView(_:start:)` in a `WKURLSchemeHandler`
- the first synthetic response creation / redirect / mutation path
- the first delegate-owned challenge/continuation path after interception has already been selected

### E. Resource-still-needed / task-liveness truth
This is especially important for `WKURLSchemeHandler` cases.
Typical smaller truths:
- `webView(_:start:)` already fired, so the custom scheme did own this resource at least briefly
- later `webView(_:stop:)` means WebKit no longer needs the resource
- after `stop`, continued `WKURLSchemeTask` progress reporting is already invalid task behavior rather than successful delivery

Do not flatten “start happened” into “resource remained live long enough to create the page-visible consequence.”

### F. Later visible consequence truth
This is where the analyst proves the URL-loading-owned chain actually matters:
- one response body/header/redirect/resource visible to the page or app depends on the interception path
- one request mutation or synthetic response path actually changes later behavior
- one later trust/response/business consequence depends on the earlier interception-owned step

## 5. Practical stop rules this note preserves
- `custom protocol or scheme handler exists != current request path uses it`
- `registerClass(...) visible != current session/config carries that class`
- `protocolClasses visible != default protocols fell through to the custom class`
- `background-session traffic visible != same custom URLProtocol path can own it`
- `canInit(with:) candidate exists != canonical/cache-equivalence truth frozen`
- `delegate/trust path visible != request-interception ownership proved`
- `request entered URL loading stack != first interception consumer proved`
- `webView(_:start:) fired != resource still needed / page-visible consequence proved`
- `resource visible in page/app != this interception family owned the visible consequence`
- `scheme handler registered != current webview/config used it`
- `custom-scheme registration exists != ordinary https request can route through it`

## 6. Default workflow
### Step 1: freeze one request family, one candidate interceptor, and one visible consequence
Do not widen into every request.
Pick one high-leverage chain:
- one request that should hit a custom protocol
- one custom-scheme resource in WKWebView
- one synthetic/modified resource path
- one trust/delegate path that appears adjacent to interception ownership

### Step 2: separate global registration from current session / current webview truth
Before explaining behavior, freeze:
- whether the case is driven by global `registerClass(...)`, session-local `protocolClasses`, or WebKit custom-scheme registration
- whether the current `URLSessionConfiguration` or `WKWebViewConfiguration` actually carries it
- whether the request family is eligible for this path at all
- whether background-session or built-in-scheme rules already rule the candidate out

### Step 3: freeze one interception-selection boundary
Pick the smallest selection object that matters:
- one `canInit(with:)` or similar eligibility boundary
- one default-protocol-vs-custom-protocol fall-through question
- one `canonicalRequest(for:)` / cache-equivalence boundary if similar-looking requests still lie
- one scheme match plus current-configuration ownership check such as `urlSchemeHandler(forURLScheme:)`

### Step 4: prove one first interception consumer
Prefer the first consumer that best predicts visible behavior:
- `startLoading()` that creates or redirects the response
- `webView(_:start:)` that begins supplying resource bytes through `WKURLSchemeTask`
- first synthetic response / header/body mutation path

If the case is WebKit-shaped, also freeze whether later `webView(_:stop:)` means the resource ceased to matter before the supposed consequence.

### Step 5: stop once one smaller trustworthy chain exists
Examples:
- global registration or session-local protocol class -> current session config -> `canInit(with:)` match -> `canonicalRequest(for:)` if needed -> `startLoading()` -> visible response
- scheme-handler registration -> current webview config -> scheme eligible for custom handling -> `webView(_:start:)` -> not-stopped / still-needed truth -> page-visible resource consequence
- request selected into custom protocol -> trust/delegate continuation -> later visible request/response effect

## 7. Practical scenarios
### Scenario A: `URLProtocol.registerClass(...)` is visible globally
Wrong stop:
- “the class is registered, so this request must pass through it”

Better stop:
- freeze whether the current request is actually in the right session/runtime to see that class at all
- then prove one `canInit(with:)` win and one `startLoading()` chain
- if several protocol classes compete, remember Apple says reverse registration order matters and not all registered classes are guaranteed to be consulted

### Scenario B: `protocolClasses` exists on one session configuration
Wrong stop:
- “the session carries my class, so this request is intercepted”

Better stop:
- check whether the current request uses that exact configuration
- check whether the session is background-shaped
- keep default-protocol handling and one later `canInit(with:)` win separate from mere config membership

### Scenario C: `WKURLSchemeHandler` exists for a custom scheme
Wrong stop:
- “custom scheme handler is registered, so this page-visible resource is solved”

Better stop:
- prove the current `WKWebViewConfiguration`
- verify the current scheme is actually one WebKit delegates to custom handlers
- then freeze one `webView(_:start:)` path that actually supplied the resource

### Scenario D: `webView(_:start:)` already fired
Wrong stop:
- “the page must already have consumed the resource”

Better stop:
- keep `start` truth separate from later `stop` / no-longer-needed truth
- if `webView(_:stop:)` fires, treat later task activity as cancellation noise or invalid-task behavior first, not durable delivery truth

### Scenario E: trust/delegate code is visible near URL loading
Wrong stop:
- “delegate challenge handling proves request ownership”

Better stop:
- keep interception-selection truth separate from later trust/delegate consequence unless the request is already proved to flow through that path.

## 8. Why this note exists in the iOS/mobile branch
The mobile subtree already had practical notes for WebView mixed ownership, bridge payloads, bootstrap handoffs, and iOS trust/pinning localization.
What it lacked was a thinner practical continuation for **URL-loading interception ownership** on iOS.

This note now fills that gap more concretely and preserves the smaller ladders:
- global `registerClass(...)` or session-local `protocolClasses` truth
- current session/webview ownership
- request-selection truth
- first interception consumer truth
- resource-still-needed / task-liveness truth when relevant
- later visible consequence

instead of collapsing everything into “custom protocol/scheme handler exists.”

## 9. Sources
See:
- `sources/mobile/2026-04-05-ios-url-loading-interception-and-first-consumer-notes.md`
- `sources/ios/2026-04-23-ios-url-loading-protocolclasses-and-scheme-handler-realism-notes.md`

Primary anchors retained:
- Apple docs for `URLProtocol`, `registerClass(_:)`, `canonicalRequest(for:)`, and `URLSessionConfiguration.protocolClasses`
- Apple docs for `WKWebViewConfiguration.setURLSchemeHandler(_:forURLScheme:)`, `urlSchemeHandler(forURLScheme:)`, `WKURLSchemeHandler`, `webView(_:start:)`, and `webView(_:stop:)`
- explicit `search-layer` multi-source attempt with `--source exa,tavily,grok`
- practical session/configuration notes around `protocolClasses`, built-in WebKit-owned schemes, and `WKURLSchemeTask` lifecycle
