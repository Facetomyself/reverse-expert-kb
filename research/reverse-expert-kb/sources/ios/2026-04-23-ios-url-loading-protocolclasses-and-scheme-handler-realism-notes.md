# 2026-04-23 iOS URL-loading protocol-class and scheme-handler realism notes

Date: 2026-04-23 04:50 Asia/Shanghai / 2026-04-22 20:50 UTC
Theme: keep URL-loading registration truth, current session or webview ownership truth, selection truth, first consumer truth, and resource-still-needed / visible-consequence truth separate.

## Why this note exists
The KB already had a bounded iOS URL-loading workflow note, but that branch was still thin in two practical ways:
- it still flattened **global `URLProtocol.registerClass(...)` visibility**, **session-scoped `URLSessionConfiguration.protocolClasses` truth**, **`canInit(with:)` selection truth**, **`canonicalRequest(for:)` cache/equality truth**, and **`startLoading()` consumer truth** too easily
- it still flattened **one `WKURLSchemeHandler` registration**, **current `WKWebViewConfiguration` ownership**, **whether WebKit even delegates the current scheme**, **`webView(_:start:)` truth**, and **later `webView(_:stop:)` cancellation / no-longer-needed truth** too easily

This source pass keeps only the smaller Apple-doc-backed operator facts needed to strengthen the canonical workflow note and sync it into the iOS subtree guide and mobile parent page.

## Retained doc anchors (Apple)
### `URLProtocol`
- Doc endpoint: `https://docs.developer.apple.com/tutorials/data/documentation/foundation/urlprotocol.json`
- Retained:
  - `URLProtocol` is an abstract class for protocol-specific URL loading
  - the system creates the appropriate protocol object for the corresponding request
  - the protocol class should be registered during app launch so the system is aware of it
- Practical meaning:
  - a visible subclass is only family truth until one current request is proved to route through it
  - the first strong boundary is still one request-owned selection / consumer chain, not mere subclass presence

### `registerClass(_:)`
- Doc endpoint: `https://docs.developer.apple.com/tutorials/data/documentation/foundation/urlprotocol/registerclass(_:).md`
- Retained:
  - register custom `URLProtocol` subclasses before making URL requests
  - when the URL loading system begins a request, it tries to initialize each registered protocol class with the request
  - the first subclass whose `canInit(with:)` returns true is used to load the request
  - there is **no guarantee that all registered protocol classes will be consulted**
  - classes are consulted in the **reverse order of registration**
  - the same reverse-order style also governs canonical-request creation
- Practical meaning:
  - **registered globally != current request selected this class**
  - one earlier/later registration can hide another candidate interceptor
  - “my class exists” is weaker than “this request reached my `canInit(with:)` and won selection”

### `canonicalRequest(for:)`
- Doc endpoint: `https://docs.developer.apple.com/tutorials/data/documentation/foundation/urlprotocol/canonicalrequest(for:).md`
- Retained:
  - each protocol implementation defines its own canonical form
  - the same input request should always yield the same canonical form
  - the canonical form is used for URL-cache lookup and equality checks between `URLRequest` objects
- Practical meaning:
  - request equality / cache truth can diverge from raw pre-canonical request visibility
  - **selection truth != canonical/cache-equivalence truth != first consumer truth**
  - when compare pairs lie, one “same-looking” request object may still normalize differently before later cache or consumer reasoning

### `URLSessionConfiguration.protocolClasses`
- Doc endpoint: `https://docs.developer.apple.com/tutorials/data/documentation/foundation/urlsessionconfiguration/protocolclasses.md`
- Retained:
  - `protocolClasses` is an array of extra custom `URLProtocol` subclasses for a session
  - `URLSession` searches the **default protocols first** and only then checks custom protocols until one `canInit(with:)` returns true
  - custom `URLProtocol` subclasses cannot be used with **background sessions**
  - default value is an empty array
- Practical meaning:
  - **class visible somewhere != current session configuration carries it**
  - **configuration carries it != request will ever reach it**, because default protocols are searched first
  - background-session traffic should not be overread as if the same custom interceptor path could own it

### `WKWebViewConfiguration.setURLSchemeHandler(_:forURLScheme:)`
- Doc endpoint: `https://docs.developer.apple.com/tutorials/data/documentation/webkit/wkwebviewconfiguration/seturlschemehandler(_:forurlscheme:).md`
- Retained:
  - registers an object to load resources for the specified scheme
  - scheme names are case sensitive and have explicit character rules
  - registering a handler for a scheme WebKit already handles, such as `https`, is a programmer error and raises `NSInvalidArgumentException`
  - calling the method more than once for the same scheme is also a programmer error
  - Apple explicitly recommends custom scheme names that reduce future conflicts
- Practical meaning:
  - **scheme-handler visible != current WebKit-owned request can use it**
  - standard WebKit-owned schemes like `https` should not be narrated as if they are solved by ordinary `WKURLSchemeHandler` registration
  - repeated registration bugs can create noise that is still weaker than current-webview ownership truth

### `WKWebViewConfiguration.urlSchemeHandler(forURLScheme:)`
- Doc endpoint: `https://docs.developer.apple.com/tutorials/data/documentation/webkit/wkwebviewconfiguration/urlschemehandler(forurlscheme:).md`
- Retained:
  - returns the handler object currently registered for the specified scheme, or `nil`
  - scheme-name validation matches the same case-sensitive naming rules
- Practical meaning:
  - the current configuration can be queried directly
  - **generic handler existence != current `WKWebViewConfiguration` ownership truth**

### `WKURLSchemeHandler`
- Doc endpoint: `https://docs.developer.apple.com/tutorials/data/documentation/webkit/wkurlschemehandler.md`
- Retained:
  - the protocol is for URL schemes that WebKit doesn’t handle
  - when a web view encounters a resource using the custom scheme, it creates a `WKURLSchemeTask` and passes it to the handler
  - `webView(_:start:)` begins the load and `webView(_:stop:)` may arrive later when the resource is no longer needed
- Practical meaning:
  - the right consumer boundary is not handler registration alone, but one task-bearing `start` path for the current resource
  - later `stop` truth is a separate liveness/cancellation object and should not be flattened into successful delivery

### `webView(_:start:)`
- Doc endpoint: `https://docs.developer.apple.com/tutorials/data/documentation/webkit/wkurlschemehandler/webview(_:start:).md`
- Retained:
  - when the web view encounters a resource with the custom scheme, it calls `webView(_:start:)` on the appropriate handler
  - the handler uses `WKURLSchemeTask` to report progress and deliver resource data back to the web view
- Practical meaning:
  - **current resource routed here != later page-visible consequence already proved**, but `start` is the first strong scheme-consumer boundary

### `webView(_:stop:)`
- Doc endpoint: `https://docs.developer.apple.com/tutorials/data/documentation/webkit/wkurlschemehandler/webview(_:stop:).md`
- Retained:
  - WebKit calls `stop` when it no longer needs the resource, commonly on navigation but also for other reasons
  - the load should be stopped immediately
  - after `stop`, calling methods on the provided `urlSchemeTask` raises an exception
- Practical meaning:
  - **`start` truth != resource-still-needed truth != page-visible delivery truth**
  - handler code that still tries to report progress after `stop` is not consumer truth; it is already canceled / invalid task behavior

## Operator ladders retained
### URLProtocol / URLSession ladder
```text
URLProtocol subclass or global registerClass visible
  != current URLSessionConfiguration carries the class
  != default protocols fell through to the custom class
  != canInit(with:) selected the request
  != canonicalRequest(for:) / cache-equivalence truth
  != startLoading() first consumer truth
  != later visible consequence
```

### WebKit custom-scheme ladder
```text
scheme handler registered
  != current WKWebViewConfiguration owns that handler
  != current resource uses a scheme WebKit delegates to custom handlers
  != webView(_:start:) fired for this resource
  != resource still needed / not yet stopped
  != page-visible consequence truth
```

## Practical workflow cues retained
- freeze whether the case is **global URLProtocol registration**, **session-scoped `protocolClasses`**, or **WebKit custom-scheme** first; do not narrate them as one generic interception family
- if the case is `URLSession`-shaped, ask whether the current session is background-shaped before promising any custom `URLProtocol` path
- if `protocolClasses` is present, remember Apple says default protocols are checked first; treat config membership as weaker than actual selection
- if one `URLProtocol` subclass is “definitely registered,” still prove one `canInit(with:)` win before claiming current-request ownership
- if compare pairs lie around repeated-looking requests, freeze `canonicalRequest(for:)` / cache-equivalence truth before overreading raw request-object similarity
- if the case is WebKit-shaped, verify the current configuration’s handler with `urlSchemeHandler(forURLScheme:)` and keep `https` / other WebKit-handled schemes out of ordinary custom-scheme claims
- if `webView(_:start:)` already fired, keep later `webView(_:stop:)` separate: cancellation/no-longer-needed truth is weaker than page-visible completion

## Search-layer trace
See:
- `sources/ios/2026-04-23-0450-ios-url-loading-search-layer.txt`

Observed degraded mode:
- Grok was explicitly invoked via `--source exa,tavily,grok` but returned repeated 502 proxy errors
- Exa and Tavily still returned enough Apple documentation surfaces to support a conservative, bounded iOS URL-loading continuation and canonical-sync pass
