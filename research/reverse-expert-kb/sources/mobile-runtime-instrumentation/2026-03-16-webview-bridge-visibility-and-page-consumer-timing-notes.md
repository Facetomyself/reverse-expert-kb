# Source Notes — 2026-03-16 — WebView bridge visibility vs page-consumer timing

## Scope
Focused source pass for a narrow but recurring hybrid-app failure mode:
- the Java/JS bridge or outbound native call is visible
- the app appears to survive reload/navigation at the WebView level
- but the decisive page-side consumer still misses the value because listener/store/route readiness and lifecycle timing diverge from bridge visibility

This pass was used to improve an existing concrete workflow note rather than create another abstract taxonomy page.

## Queries used
Search-layer / Grok-oriented exploratory queries:
- `Android WebView addJavascriptInterface injected object visible after reload lifecycle page consumer timing`
- `Android WebView evaluateJavascript listener registration timing SPA remount`
- `Android WebView postWebMessage WebMessagePort listener registration timing`

## Sources consulted
### Official / stronger references
1. Chromium WebView Java bridge design notes
   - https://chromium.googlesource.com/chromium/src/+/master/android_webview/docs/java-bridge.md
   - Strong practical anchors extracted:
     - adding or removing an injected object is not reflected on the JavaScript side until the next page load
     - injected-object visibility is a lifecycle/load-boundary question, not a free-floating runtime guarantee
     - bridge semantics should be reasoned about separately from later page callback/store use

2. Android Developers WebView JavaScript communication guide
   - surfaced through search results at:
     - https://developer.android.com/develop/ui/views/layout/webapps/webview/javascript
   - Search-layer result snippets reinforced a useful practical point:
     - JavaScript-interface object availability can persist across reloads/navigation in the same WebView instance
     - that persistence still does not prove that the operational page callback/store path is ready

3. Android Developers bidirectional channel guidance
   - surfaced through search results at:
     - https://developer.android.com/develop/ui/views/layout/webapps/webview-javascript
   - Search-layer snippet highlighted a practical message-channel timing rule:
     - listener/callback setup order matters for `WebMessagePort` / channel flows
     - early or asymmetric registration can cause message loss that looks like payload failure

### Practical implementation / recurrence references
4. TechYourChance — Communication with WebView in Android
   - https://www.techyourchance.com/communication-webview-javascript-android/
   - Useful recurring implementation details:
     - `evaluateJavascript(...)` is only proof of outbound emission
     - result values come back JSON-wrapped and need semantic normalization before compare-run reasoning
     - reliable interaction depends on page-readiness timing

5. Stack Overflow recurrence signal — interface availability after load
   - https://stackoverflow.com/questions/32830513/when-is-addjavascriptinterface-available-after-webview-load
   - Used conservatively as recurrence evidence that interface visibility timing is often misunderstood by practitioners

6. Stack Overflow recurrence signal — interface survival across reload
   - https://stackoverflow.com/questions/12655701/does-addjavascriptinterface-survive-page-reload
   - Used conservatively as recurrence evidence that bridge persistence is often true while page-consumer readiness remains the real bottleneck

7. Stack Overflow recurrence signal — `evaluateJavascript` timing/reliability issues
   - https://stackoverflow.com/questions/57528415/android-webview-evaluatejavascript-sometimes-does-not-return-a-response
   - Used as weak but relevant operator evidence that lifecycle timing and context readiness can mimic payload corruption

8. Stack Overflow recurrence signal — `WebMessagePort` listener ordering
   - https://stackoverflow.com/questions/40664350/how-to-use-new-android-webview-postwebmessage-api
   - Useful as weak but concrete support for treating listener-registration order as a first-class diagnosis axis

## Practical findings extracted
### 1. Bridge persistence and page-consumer readiness are different questions
The most useful synthesis from this pass is:

```text
bridge object still visible / still bound
  != first meaningful page consumer is ready
```

Why this matters operationally:
- analysts often stop when they prove the bridge survived reload/navigation
- the app can still fail because the actual callback/store/route consumer remounted later, was replaced, or had not yet registered

### 2. Load-boundary semantics do not solve SPA/remount timing automatically
Chromium’s Java-bridge notes support a conservative workflow rule:
- bridge exposure changes are tied to page-load boundaries
- however, app-level route/store/listener readiness may still drift within the same WebView instance

Practical consequence:
- proving WebView-level continuity is not enough in hybrid cases with SPA-like remounts or route resets

### 3. `evaluateJavascript(...)` should be treated as an emission boundary, not a success proof
The practical sources reinforced a distinction already emerging in the KB:
- visible `evaluateJavascript(...)` proves outbound native emission
- it does not prove a meaningful page-side consumer existed at that moment
- JSON-wrapped callback material can further hide the real semantic payload during compare-run work

### 4. Message-channel timing deserves equal suspicion
For `postWebMessage(...)` / `WebMessagePort` style flows:
- listener/port registration order can be the real bottleneck
- missing the first message can look like malformed payload, wrong key, or broken transport

### 5. A better compare-run template is lifecycle-centered, not just payload-centered
For this failure family, compare-run notes should explicitly record:
- bridge/interface visible at
- page callback/listener/store registered at
- route mounted or remounted at
- native emission at
- first meaningful consumer fire at
- first request-driving effect at

That structure is more useful than only diffing emitted payloads.

## Resulting KB integration direction
This pass justified tightening an existing concrete workflow note:
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`

Secondary integration candidate:
- `index.md` or subtree guidance if later navigation text needs to emphasize bridge-persistence-vs-consumer-readiness explicitly

## Evidence quality note
Strongest support here came from:
- Chromium WebView bridge design notes
- Android Developers communication-guide snippets surfaced through search

Tutorial and Q&A material was used only as recurrence evidence for practical analyst pain points, not as proof of universal platform behavior.

## Practical bottom line
The durable operator rule from this pass is:

```text
visible bridge or visible native emission
  != solved hybrid return path

also verify:
  listener / port / callback registration timing
  route mount or remount timing
  store readiness
  first meaningful consumer timing
  first request-driving effect after consumption
```
