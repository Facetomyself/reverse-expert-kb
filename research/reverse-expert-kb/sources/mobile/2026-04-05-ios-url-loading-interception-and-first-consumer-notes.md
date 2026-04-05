# Source notes — iOS URL loading interception and first consumer

Date: 2026-04-05 20:29 Asia/Shanghai / 2026-04-05 12:29 UTC
Topic: iOS URL loading interception and first consumer ownership
Author: Reverse Claw

## Why this pass happened
Recent runs had already strengthened multiple thinner branches across browser service workers, mobile/WebView bridges, runtime evidence, native watchers, and protocol/descriptor trust.
This hour needed a real external-research-driven pass on a different practical seam.

The iOS/mobile branch had trust/pinning localization and WebView ownership notes, but it lacked a canonical workflow note centered on **URL-loading interception ownership**.
That made it a good target: practical, iOS-specific, and distinct enough from trust-path and WebView-only notes to justify a new workflow page.

## Practical question
What smaller truth objects matter once a custom URL-loading family is already visible, but the investigation still lacks the first trustworthy consumer that actually owns the request/response consequence?

## Retained high-signal points
### 1. Registration and current ownership are different truths
Apple API material is useful because it makes registration/configuration boundaries explicit:
- `URLProtocol.registerClass(...)`
- `URLSessionConfiguration.protocolClasses`
- `WKWebViewConfiguration.setURLSchemeHandler(_:forURLScheme:)`

Retained operator consequence:
- visible registration is weaker than current session/webview ownership truth
- shared session, custom session, and WebView configuration should be kept separate before overclaiming interception

### 2. Interception selection is narrower than family presence
`NSURLProtocol` references are useful because they preserve selection semantics around `canInit(with:)`, canonical request handling, and `startLoading()` / `stopLoading()` lifecycle.

Retained operator consequence:
- a visible protocol class is weaker than a request actually being selected into it
- `canInit(with:)` and similar selection logic are often the narrower missing reducer before later behavior explanation

### 3. First interception consumer truth usually lives at `startLoading()` or scheme-task start
Apple docs are useful because they make the first consequence-bearing callback explicit:
- `startLoading()` for `URLProtocol`
- `startURLSchemeTask(...)` for `WKURLSchemeHandler`

Retained operator consequence:
- family presence and selection are still weaker than the first method that actually supplies, redirects, mutates, or blocks the resource
- this is the right practical target before widening into later parser/business logic

### 4. Trust/delegate visibility is useful, but only after interception ownership is proved
Related URLSession / challenge material is useful because it reminds the analyst that delegate/trust paths often sit adjacent to interception ownership without being identical to it.

Retained operator consequence:
- visible challenge handling is weaker than request-interception ownership
- do not flatten trust-path visibility into proof that this exact custom protocol/scheme handler owned the request

## Conservative synthesis used in KB
Useful branch rule preserved:

```text
interception family exists
  != current session/webview uses it
  != relevant request was selected by it
  != first interception consumer proved
  != later visible request/response consequence truth
```

Additional branch memory preserved:
- shared-session behavior should stay separate from custom-session behavior
- current `WKWebViewConfiguration` truth should stay separate from generic scheme-handler visibility
- `canInit(with:)` / selection truth is weaker than `startLoading()` / `startURLSchemeTask(...)` consumer truth
- trust/delegate visibility should not silently replace interception ownership proof

## Sources consulted
### Explicit multi-source search attempt
All searches were run via explicit `search-layer` source selection:
- `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok ...`

Search themes used:
- `NSURLProtocol` lifecycle and selection semantics
- `WKURLSchemeHandler` start/stop task ownership
- `URLSessionConfiguration.protocolClasses` and custom protocol reach

### Representative surfaced materials
- Apple `URLProtocol` / `NSURLProtocol` docs
- Apple `WKURLSchemeHandler` docs
- Apple URL loading system docs
- practical articles/discussions on custom `URLProtocol` registration and `protocolClasses`
- WebKit / app-side custom-scheme handling references

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
This pass justified a new canonical iOS/mobile workflow note.
The subtree was missing a practical continuation for URL-loading interception ownership.

The durable operator value is keeping these truths separate:
- registration
- current session/webview ownership
- interception selection
- first interception consumer
- later visible consequence
