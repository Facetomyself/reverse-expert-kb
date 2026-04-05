# iOS URL Loading Interception and First Consumer Workflow Note

Topic class: workflow note
Ontology layers: iOS runtime, URL loading, request interception, first consumer proof
Maturity: emerging
Related pages:
- topics/mobile-reversing-and-runtime-instrumentation.md
- topics/ios-trust-path-and-pinning-localization-workflow-note.md
- topics/webview-native-mixed-request-ownership-workflow-note.md
Related source notes:
- sources/mobile/2026-04-05-ios-url-loading-interception-and-first-consumer-notes.md

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
  - scheme-handler registration -> current `WKWebView` config -> `startURLSchemeTask(...)` -> synthetic/modified resource -> page-visible consequence
  - delegate/trust path -> request continues -> later response ownership, once trust-handling is already narrowed enough to hand off here

Do **not** start here when:
- the real bottleneck is still broad iOS trust/pinning localization rather than interception ownership
- the real question is still mixed WebView/native ownership without evidence of iOS URL-loading interception
- interception selection is already proved and the real missing step is later parser/business-logic consequence outside the URL-loading seam

## 3. Core claim
A recurring iOS/network-reversing mistake is to stop too early at one of these milestones:
- “a custom `NSURLProtocol` subclass exists”
- “`protocolClasses` is configured”
- “a `WKURLSchemeHandler` exists”
- “the app has URLSession/WebView delegate code, so it must own this request”

The smaller reusable target is:

```text
interception family exists
  != current session/webview uses it
  != relevant request was selected by it
  != first interception consumer proved
  != later visible request/response consequence truth
```

## 4. Boundary objects to keep separate
### A. Registration truth
Visible objects:
- `URLProtocol.registerClass(...)`
- `URLSessionConfiguration.protocolClasses`
- `WKWebViewConfiguration.setURLSchemeHandler(_:forURLScheme:)`
- delegate attachment / ownership scaffolding

This is weaker than proof that the current request path actually used the registration that matters.

### B. Current-owner truth
Useful questions:
- is the request using the shared session or a custom configuration?
- does the current `URLSessionConfiguration` actually include the protocol class you care about?
- is the current `WKWebViewConfiguration` the one with the relevant scheme handler attached?
- is the current request path even eligible for this protocol/scheme family?

This matters because “interceptor exists” is weaker than “the current request path is owned by it.”

### C. Interception-selection truth
Typical smaller truths:
- one `canInit(with:)` / eligibility method actually selected the request
- one scheme family really resolved into `startURLSchemeTask(...)`
- one current configuration/session/webview path actually routes here rather than to default loading

Do not flatten “request looks similar” into “this interceptor owned it.”

### D. First consumer truth
This is the first method/path that turns the request into meaningful app behavior.
Typical shapes:
- `startLoading()` in a `URLProtocol` subclass
- `startURLSchemeTask(_: )` in a `WKURLSchemeHandler`
- the first synthetic response creation / redirect / mutation path
- the first delegate-owned challenge/continuation path after interception has already been selected

### E. Later visible consequence truth
This is where the analyst proves the URL-loading-owned chain actually matters:
- one response body/header/redirect/resource visible to the page or app depends on the interception path
- one request mutation or synthetic response path actually changes later behavior
- one later trust/response/business consequence depends on the earlier interception-owned step

## 5. Practical stop rules this note preserves
- `custom protocol or scheme handler exists != current request path uses it`
- `protocolClasses visible != relevant request was selected by it`
- `delegate/trust path visible != request-interception ownership proved`
- `request entered URL loading stack != first interception consumer proved`
- `resource visible in page/app != this interception family owned the visible consequence`
- `shared-session behavior != custom-session behavior`
- `scheme handler registered != current webview/config used it`

## 6. Default workflow
### Step 1: freeze one request family, one candidate interceptor, and one visible consequence
Do not widen into every request.
Pick one high-leverage chain:
- one request that should hit a custom protocol
- one custom-scheme resource in WKWebView
- one synthetic/modified resource path
- one trust/delegate path that appears adjacent to interception ownership

### Step 2: separate registration from current-session/current-webview truth
Before explaining behavior, freeze:
- which protocol/scheme handler is registered
- whether the current `URLSessionConfiguration` or `WKWebViewConfiguration` actually carries it
- whether the request family is eligible for this path

### Step 3: freeze one interception-selection boundary
Pick the smallest selection object that matters:
- one `canInit(with:)` or similar eligibility boundary
- one scheme match
- one configuration/session switch

### Step 4: prove one first interception consumer
Prefer the first consumer that best predicts visible behavior:
- `startLoading()` that creates or redirects the response
- `startURLSchemeTask(...)` that supplies resource bytes
- first synthetic response / header/body mutation path

### Step 5: stop once one smaller trustworthy chain exists
Examples:
- protocol registration -> current session config -> `canInit(with:)` match -> `startLoading()` -> visible response
- scheme-handler registration -> current webview config -> `startURLSchemeTask(...)` -> page-visible resource consequence
- request selected into custom protocol -> trust/delegate continuation -> later visible request/response effect

## 7. Practical scenarios
### Scenario A: `NSURLProtocol` subclass is visible
Wrong stop:
- “custom protocol exists, so this request must pass through it”

Better stop:
- freeze current session/configuration truth and one actual `canInit(with:)` / `startLoading()` chain.

### Scenario B: `WKURLSchemeHandler` exists for a custom scheme
Wrong stop:
- “custom scheme handler is registered, so this page-visible resource is solved”

Better stop:
- prove the current `WKWebViewConfiguration` and one `startURLSchemeTask(...)` path that actually supplied the resource.

### Scenario C: trust/delegate code is visible near URL loading
Wrong stop:
- “delegate challenge handling proves request ownership”

Better stop:
- keep interception-selection truth separate from later trust/delegate consequence unless the request is already proved to flow through that path.

## 8. Why this note exists in the iOS/mobile branch
The mobile subtree already had practical notes for WebView mixed ownership, bridge payloads, bootstrap handoffs, and iOS trust/pinning localization.
What it lacked was a thinner practical continuation for **URL-loading interception ownership** on iOS.

This note fills that gap and preserves the smaller ladder:
- registration
- current session/webview ownership
- interception selection
- first interception consumer
- later visible consequence

instead of collapsing everything into “custom protocol/scheme handler exists.”

## 9. Sources
See:
- `sources/mobile/2026-04-05-ios-url-loading-interception-and-first-consumer-notes.md`

Primary anchors retained:
- Apple docs for `NSURLProtocol`, `WKURLSchemeHandler`, and URL loading system behavior
- explicit `search-layer` multi-source attempt with `--source exa,tavily,grok`
- practical session/configuration notes around `protocolClasses` and custom protocol reach
