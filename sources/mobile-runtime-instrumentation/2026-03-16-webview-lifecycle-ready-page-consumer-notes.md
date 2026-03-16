# Source Notes — 2026-03-16 — WebView lifecycle-ready page-consumer diagnosis

## Scope
Focused source pass for a narrow hybrid-app problem:
- the page→native payload appears correct
- native code appears to produce the right result
- but the case still fails because page-side consumer readiness, route mount, reload/reinit, or bridge visibility timing remains wrong

This pass was used to improve existing practical workflow notes rather than create a new abstract parent page.

## Sources checked
### Official / strong references
- Chromium Android WebView Java Bridge documentation
  - https://chromium.googlesource.com/chromium/src/+/master/android_webview/docs/java-bridge.md
- Android Developers WebView reference
  - https://developer.android.com/reference/android/webkit/WebView
- AndroidX WebViewCompat reference (`postWebMessage`, related message primitives)
  - https://developer.android.com/reference/androidx/webkit/WebViewCompat
- Android Developers native bridge risk note
  - https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridges

### Practical implementation / recurrence references
- TechYourChance WebView communication article
  - https://www.techyourchance.com/communication-webview-javascript-android
- InAppWebView communication docs
  - https://inappwebview.dev/docs/webview/javascript/communication
- StackOverflow recurrence signal on interface visibility / page update behavior
  - https://stackoverflow.com/questions/79495428/android-webview-javascript-interface-being-removed-on-webforms-partial-postback
- React Native WebView SPA navigation asymmetry issue
  - https://github.com/react-native-webview/react-native-webview/issues/2667
- 42Gears note on `evaluateJavascript` timing as practical guidance
  - https://techblogs.42gears.com/inject-javascript-to-android-webview

## Practical findings extracted
### 1. Bridge visibility and lifecycle timing are real first-class constraints
Chromium’s Java bridge documentation reinforces a concrete workflow rule already emerging in the KB:
- Java bridge exposure is tied to page/frame lifecycle
- changes to injected objects are not a free-standing proof of current-page visibility
- timing and load boundaries matter when deciding whether the page can actually consume a native return

Conservative operational takeaway:
- do not treat a correct outbound native payload as proof of success until the relevant page listener/callback/store exists in the right lifecycle window

### 2. `evaluateJavascript(...)` visibility is not the same as consumer readiness
Official docs and practical tutorials support the distinction between:
- native emission being observable
- page consumer actually being registered and ready

Useful diagnosis framing:
- visible `evaluateJavascript(...)` only proves outbound emission
- it does not prove that the first meaningful page consumer already exists, is mounted, or survives route/remount/reload behavior

### 3. Message-channel registration timing deserves equal suspicion
`postWebMessage(...)` / WebMessage-style APIs also create a registration-order problem:
- the page-side message listener or port wiring can be the real boundary
- missing or late registration can mimic payload corruption

This supports keeping message-channel return paths alongside callback-string return paths in the same concrete workflow note.

### 4. SPA / remount behavior can invalidate otherwise-correct reasoning
Practical recurrence sources are weaker than the official docs, but they repeatedly point toward the same operator problem:
- SPA route changes and remounts may not look like full classic navigations from the analyst’s vantage point
- listener registration and page state can silently drift across those transitions
- hybrid cases can therefore fail after native success simply because the page-side consumer moved, remounted, or was reset

Conservative workflow takeaway:
- include route mount / remount / reload timestamps in compare-run notes whenever native→page return is visible but behavior still diverges

## Resulting KB integration direction
This source pass justified strengthening existing pages instead of creating a new framework page:
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`

## Evidence quality note
Strongest support here came from:
- Chromium WebView Java bridge documentation
- Android / AndroidX WebView references

Implementation articles and issue threads were used only as recurrence signals for the workflow problem, not as hard proof of universal platform behavior.

## Practical bottom line
The useful operator rule from this source pass is:

```text
correct bridge payload
  != solved hybrid case

also verify:
  listener registration timing
  route mount / remount timing
  reload / reinit timing
  page-store freshness at first meaningful consumer
```
