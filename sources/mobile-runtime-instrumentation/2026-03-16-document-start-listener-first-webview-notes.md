# Source Notes — 2026-03-16 — Document-start listener-first WebView timing

## Scope
Focused source pass for one narrow hybrid-app diagnosis pattern:
- native emission is visible
- bridge exposure may even be correct
- but the first meaningful page consumer still misses the message or callback because listener/port registration happens too late, especially after SPA-style route remounts

This pass was used to improve an existing concrete workflow note rather than create a new abstract topic page.

## Queries used
Search-layer / Grok-oriented exploratory queries:
- `Android WebView WebMessagePort listener registration order message lost page ready`
- `Android WebView evaluateJavascript onPageFinished SPA route remount callback timing`
- `Android WebView WebMessageListener document start injection listener timing`

## Sources consulted
### Official / stronger references
1. AndroidX WebKit release notes
   - https://developer.android.com/jetpack/androidx/releases/webkit
   - High-value practical signal surfaced through search results:
     - `addDocumentStartJavascript` is intended to inject JavaScript before page scripts execute
     - `addWebMessageListener` can be combined with document-start injection for more reliable two-way communication
   - Practical implication for RE:
     - if a target only works when page-side listeners exist before app scripts run, then late observer placement can create false negatives that look like payload corruption or bridge failure

2. Android WebView `WebMessagePort` API reference
   - https://developer.android.com/reference/android/webkit/WebMessagePort
   - Useful anchor for treating message ports as a first-class return family, not just a footnote to `addJavascriptInterface(...)`

3. Android Developers native-bridge security guidance
   - https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridges
   - Search result snippets reinforced a practical timing concern:
     - message-based bridges and listener registration order matter operationally, not just from a security perspective

### Practical implementation / recurrence references
4. CommonsWare — Replacing `addJavascriptInterface()` with HTML Message Channels
   - https://commonsware.com/blog/2017/01/23/replacing-addjavascriptinterface-html-message-channels.html
   - Strong practical extraction:
     - `createWebMessageChannel()` + `postWebMessage()` setup is timing-sensitive
     - JavaScript must already be prepared to receive the message or port handoff
     - this is directly relevant to cases where the first useful message is missed and later traffic looks fine

5. Stack Overflow recurrence signal — using `WebMessagePort` instead of `addJavascriptInterface()`
   - https://stackoverflow.com/questions/41753104/how-do-you-use-webmessageport-as-an-alternative-to-addjavascriptinterface
   - Used conservatively as recurrence evidence that practitioners repeatedly trip on page-load ordering and initialization timing

6. Stack Overflow recurrence signal — SPA route timing after `onPageFinished`
   - https://stackoverflow.com/questions/57692933/how-to-run-javascript-after-page-load-in-android-webview-for-single-page-appli
   - Useful recurrence signal:
     - SPA route changes may not trigger a full reload boundary
     - `onPageFinished` can therefore be a misleading timing anchor for later route-local consumer readiness

7. Stack Overflow recurrence signal — `evaluateJavascript` timing in SPA navigation
   - https://stackoverflow.com/questions/48986858/timing-of-evaluatejavascript-after-onpagefinished-in-webview-for-spa-navigati
   - Useful recurrence signal:
     - route-local readiness can drift after the last visible page-load event

## Practical findings extracted
### 1. "Bridge exists" and "listener exists early enough" are separate questions
The most durable operator rule from this pass is:

```text
bridge visible
  or native emission visible
  != listener / port / route-local consumer was ready early enough
```

### 2. Document-start tooling is useful as a diagnosis contrast, not just an implementation feature
For RE work, document-start listener injection matters because it clarifies a concrete compare-run question:
- does the target only succeed when the page-side observer/listener exists before app scripts or route setup execute?
- if so, a later hook point may systematically miss the real first consumer

That makes document-start placement a powerful diagnosis contrast for hybrid timing failures.

### 3. `onPageFinished` is often too coarse for SPA-like hybrid timing
The practical problem is not only page load.
In hybrid targets with client-side routing:
- WebView-level load completion may happen once
- route-local listeners/stores can remount later
- the first meaningful consumer may appear after the last obvious page-load callback

### 4. Message-port handoff can fail only on the first useful message
A recurring high-value scenario is:

```text
port created
  -> port passed to page
  -> listener attaches too late on page side
  -> first meaningful message lost
  -> later traffic appears normal
```

This can mislead analysts into blaming payload format or token generation rather than registration order.

### 5. Compare-runs should record early-observer timing explicitly
Useful fields for this failure family:
- document-start observer present at
- port/listener registration at
- route mount/remount at
- native first emission at
- first meaningful consumer at
- first request-driving effect at

## Resulting KB integration direction
This pass justified improving:
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`

Possible secondary integration later:
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- `index.md`

## Evidence quality note
Strongest support here came from:
- AndroidX WebKit release-note material surfaced through search results
- Android WebView API references
- CommonsWare’s concrete message-channel setup explanation

Q&A sources were used only as recurrence evidence for practical analyst pain points.

## Practical bottom line
The durable operator rule from this pass is:

```text
if a hybrid case succeeds only when the page-side listener exists before app scripts or route-local setup,
then late hooks make a correct native emission look broken.

So compare:
  document-start observer timing
  listener/port registration timing
  route remount timing
  first native emission timing
  first request-driving consumer timing
```