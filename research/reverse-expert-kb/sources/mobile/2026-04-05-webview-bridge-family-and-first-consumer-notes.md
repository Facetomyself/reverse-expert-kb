# Source notes — WebView bridge family and first native consumer realism

Date: 2026-04-05 18:30 Asia/Shanghai / 2026-04-05 10:30 UTC
Topic: WebView/native bridge payload recovery and first-consumer realism
Author: Reverse Claw

## Why this pass happened
Recent runs had already strengthened multiple thinner branches across runtime evidence, native watchers, descriptor/DMA trust, and browser service-worker ownership.
This hour needed a real external-research-driven pass on another underfed seam.

The mobile/WebView subtree already had canonical notes, but the bridge-payload note still leaned too heavily toward the classic Android object-bridge picture.
The practical gap was to preserve broader bridge-family routing and the rule that visible JS/native messaging is still weaker than the first native consumer that actually treats the payload as meaningful.

## Practical question
What cross-platform bridge-family reminders and first-consumer stop rules matter most when page/native interaction is already obvious, but the analyst still has not frozen which seam really owns the payload?

## Retained high-signal points
### 1. Bridge family is itself a first-class truth object
Android docs, Chromium bridge internals, and Apple WebKit APIs are useful because they make clear that hybrid handoff does not live in one universal family:
- classic `addJavascriptInterface`
- message-channel / `WebMessagePort` / `postWebMessage`
- custom URL / navigation handoff
- request/resource interception handoff (`shouldInterceptRequest`, `WKURLSchemeHandler`)
- `WKScriptMessageHandler` / script-message bridges

Retained operator consequence:
- “JS talked to native somehow” is weaker than identifying the bridge family
- bridge-family ambiguity is often a better next reducer than premature payload decoding

### 2. Registration/scope truth is weaker than current frame/world usage truth
Platform docs are useful because registration often carries scope semantics:
- object/interface names
- handler names
- user-content-controller registration
- message-port creation
- request-interception ownership
- frame/script-world context in WKWebView-style messaging

Retained operator consequence:
- visible handler/interface registration is weaker than proving the current page/frame/world actually used it in the run that matters
- current frame/world/context should be preserved before narrating payload ownership too aggressively

### 3. Visible messaging call is weaker than first native consumer truth
Across Android and iOS bridge families, API docs and implementation notes converge on the same practical rule:
- a visible bridge call or posted message is not yet the same thing as the first native consumer that gives the payload behavioral meaning
- request-interception or scheme-handler paths can likewise sit above the true native owner

Retained operator consequence:
- capture should target one first meaningful consumer boundary, not just one visible JS/native crossing
- `evaluateJavaScript`, `postMessage`, or handler-name visibility is still weaker than the first request builder, router, token helper, or response constructor that interprets the payload

### 4. Request/resource-shaped bridges deserve equal status with direct bridge calls
Android and WebKit docs are useful because they preserve a seam analysts often underweight:
- sometimes the real bridge is not an object-call or message port
- it is request/resource interception or synthetic-response production

Retained operator consequence:
- do not overfit every hybrid case into `addJavascriptInterface` or pure script-message mental models
- if the page-visible effect is resource-shaped, interception or scheme handling may be the true first native consumer family

## Conservative synthesis used in KB
Useful branch rule preserved:

```text
bridge object/handler exists
  != current frame/world/context used it
  != visible bridge call or message proved first native consumer truth
  != payload ownership by the decisive native path
```

Additional branch memory preserved:
- bridge-family classification should happen before deep payload parsing when ambiguous
- registration/scope truth is weaker than current page/frame/world truth
- direct JS/native calls, script-message handlers, message ports, scheme handlers, and request interception should be treated as separate ownership families

## Sources consulted
### Explicit multi-source search attempt
All searches were run via explicit `search-layer` source selection:
- `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok ...`

Search themes used:
- Android WebView bridge families and `WebMessagePort`
- Chromium WebView bridge internals
- Apple `WKScriptMessageHandler`, `WKURLSchemeHandler`, and `evaluateJavaScript` APIs

### Representative surfaced materials
- Android Developers WebView native bridges guidance
- Android API references for `WebViewCompat.postWebMessage` / `WebMessagePortCompat`
- Chromium doc: Java Bridge in WebView
- Apple WebKit API references for `WKScriptMessageHandler`, `WKURLSchemeHandler`, and `evaluateJavaScript`
- OWASP MASTG WebView bridge examples

## Search audit material for run report
Requested sources:
- Exa
- Tavily
- Grok

Observed outcome across this source pass:
- Exa: succeeded with usable hits on all three queries
- Tavily: succeeded with usable hits on all three queries
- Grok: invoked and failed with HTTP 502 Bad Gateway on all three queries

Endpoints / execution paths used:
- Exa endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`
- Tavily endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`
- Grok endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`

## What this changed in KB terms
This pass did not justify a new WebView sibling page.
The correct move was to strengthen the existing bridge-payload note by preserving:
- broader bridge-family routing
- frame/world/context truth as a narrower stop rule
- equal status for direct bridge calls and request/resource-shaped bridge families
- first native consumer truth as the practical target beyond visible JS/native messaging
