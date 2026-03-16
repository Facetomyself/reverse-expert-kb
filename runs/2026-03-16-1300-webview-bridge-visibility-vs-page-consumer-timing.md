# Run Report — 2026-03-16 13:00 — WebView bridge visibility vs page-consumer timing

## 1. Scope this run
This run stayed inside the active hybrid WebView/mobile branch and deliberately avoided creating any new abstract taxonomy page.

The practical target was a recurring but easy-to-misread failure pattern:
- the Java/JS bridge appears visible
- `evaluateJavascript(...)` or message-channel traffic appears visible
- native code seems to produce the right result
- yet the case still fails because the meaningful page-side consumer was not ready, was remounted, or missed the first useful message

Primary files reviewed before editing:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`
- recent run reports under `runs/`
- `sources/mobile-runtime-instrumentation/2026-03-16-webview-lifecycle-ready-page-consumer-notes.md`
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-response-handoff-notes.md`

## 2. New findings
### A. Bridge persistence is not the same thing as consumer readiness
The most useful practical finding hardened this run is:

```text
bridge object still visible / still bound
  != first meaningful page consumer is ready
```

That is the operator distinction analysts actually need in hybrid cases.

### B. Three recurring timing traps deserve explicit treatment
This run tightened three concrete failure families inside the return-path note:
- `addJavascriptInterface(...)` persists across reload/navigation in the same WebView instance, but the route-local callback/store path remounts later
- `evaluateJavascript(...)` emission is visible, but the relevant callback/store was not yet registered or has just been reset
- `postWebMessage(...)` / `WebMessagePort` traffic exists, but listener/port registration order causes the first meaningful message to be missed

### C. Compare-run notes should be lifecycle-centered, not payload-only
The more actionable compare-run template now records:
- bridge/interface visible time
- callback/listener/port registration time
- route mount/remount time
- native result time
- native emission time
- first meaningful consumer time
- first request-driving effect time

That is more useful than diffing payload strings alone.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`
- recent run reports under `runs/`

### Existing source notes used this run
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-response-handoff-notes.md`
- `sources/mobile-runtime-instrumentation/2026-03-16-webview-lifecycle-ready-page-consumer-notes.md`

### Fresh external sources
- Chromium WebView Java bridge design notes
  - <https://chromium.googlesource.com/chromium/src/+/master/android_webview/docs/java-bridge.md>
- Android Developers communication-guide/search snippets surfaced through search-layer
  - <https://developer.android.com/develop/ui/views/layout/webapps/webview/javascript>
  - <https://developer.android.com/develop/ui/views/layout/webapps/webview-javascript>
- TechYourChance practical communication article
  - <https://www.techyourchance.com/communication-webview-javascript-android/>
- recurrence/Q&A signals consulted conservatively:
  - <https://stackoverflow.com/questions/32830513/when-is-addjavascriptinterface-available-after-webview-load>
  - <https://stackoverflow.com/questions/12655701/does-addjavascriptinterface-survive-page-reload>
  - <https://stackoverflow.com/questions/57528415/android-webview-evaluatejavascript-sometimes-does-not-return-a-response>
  - <https://stackoverflow.com/questions/40664350/how-to-use-new-android-webview-postwebmessage-api>

## 4. Reflections / synthesis
This run stayed aligned with the human correction.

The wrong move would have been:
- invent another hybrid-communication framework page
- widen the ontology again
- rephrase old structure without increasing operator value

The better move was:
- tighten one active workflow note
- add a fresh source note with concrete lifecycle findings
- make the compare-run checklist more diagnosis-oriented

A durable synthesis from this run is:

```text
visible bridge
or visible native emission
  != solved return path

also verify:
  callback / listener / port registration timing
  route mount or remount timing
  store readiness
  first meaningful consumer timing
  first request-driving effect timing
```

## 5. Candidate topic pages to create or improve
### Improved this run
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `index.md`

### Created this run
- `sources/mobile-runtime-instrumentation/2026-03-16-webview-bridge-visibility-and-page-consumer-timing-notes.md`
- this run report

### Good next improvements
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
  - add one miniature case showing bridge payload correctness but route-local consumer failure
- `topics/webview-native-mixed-request-ownership-workflow-note.md`
  - add one explicit warning that ownership may be solved while lifecycle timing is still the active bottleneck
- `topics/browser-request-finalization-backtrace-workflow-note.md`
  - add one short cross-reference for cases where the first decisive request appears only after lifecycle-correct reinjection

## 6. Next-step research directions
1. Keep strengthening the hybrid WebView/mobile loop-closure branch through compact case patterns and compare-run templates.
2. Look for stronger official or practitioner evidence on message-port/listener ordering in real Android hybrid stacks.
3. Add one tiny scenario example around route-local callback replacement after SPA-like remount.
4. Continue preferring workflow-backed diagnosis notes over new abstract parent pages.

## 7. Concrete scenario notes or actionable tactics added this run
### Practical scenario normalized this run
**The bridge appears visible and native emission appears correct, but the app still fails because the meaningful page-side consumer was not yet ready, was remounted, or missed the first useful message.**

### Concrete tactics added
- record `bridge visible` separately from `consumer ready`
- treat `evaluateJavascript(...)` as an emission boundary, not proof of successful consumption
- treat `WebMessagePort` / message-channel listener ordering as a first-class diagnosis axis
- include route mount/remount timestamps in compare-run notes
- compare first request-driving effect, not just first visible callback or DOM change

## 8. Errors / sync notes
### Error status during research/edit pass
- A shell-based bulk fetch wrapper failed due to brittle `xargs` + heredoc plumbing.
- The local workspace copy of the `search-layer` skill does not contain the implied helper path `scripts/fetch.py`.
- `web_fetch` remained fragile on some Android Developers pages due to redirect limits.

These did not block the run. The work continued with `search-layer`, direct `web_fetch` where it succeeded, and conservative use of result snippets for redirect-prone official docs.

### Local preservation status
Local KB progress preserved in:
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `sources/mobile-runtime-instrumentation/2026-03-16-webview-bridge-visibility-and-page-consumer-timing-notes.md`
- this run report

### Git / sync handling note
After this report:
1. stage only the touched reverse-expert-kb files
2. commit from `/root/.openclaw/workspace`
3. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
4. if sync fails, preserve local progress and record the failure briefly
