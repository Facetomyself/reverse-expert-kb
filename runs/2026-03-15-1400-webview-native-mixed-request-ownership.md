# Run Report — 2026-03-15 14:00 Asia/Shanghai

## 1. Scope this run
This run continued the KB’s corrected direction: fewer abstract topic expansions, more concrete mid-case workflow notes that mirror how analysts actually get unstuck.

The run started with a structure refresh across:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- browser and mobile subtree guides
- recent concrete workflow notes, especially:
  - `topics/akamai-sensor-submission-and-cookie-validation-workflow-note.md`
  - `topics/cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note.md`
- recent run reports and source notes

The next practical gap was in the mobile subtree:
- the KB already had concrete notes for Android trust-path localization and Cronet/mixed-stack ownership
- but it still lacked a dedicated note for **hybrid WebView/native ownership ambiguity**, which is a very common real-world failure mode in Android app reversing

So this run focused on:
- validating whether there was enough source support for a concrete hybrid-app workflow note
- capturing durable ownership/boundary patterns instead of generic WebView theory
- adding a practical page centered on **intent owner**, **bridge boundary**, **transport owner**, and **response consumer**

## 2. New findings
- There was enough evidence to justify a dedicated practical note on **WebView / native mixed request ownership** rather than another broad WebView/mobile synthesis page.
- The strongest reusable analyst distinction is:
  - **intent owner** vs **transport owner**
- In hybrid Android apps, the decisive request path often falls into one of four practical classes:
  - pure WebView ownership
  - JS intent, native transport ownership
  - native bootstrap, WebView consumer
  - mixed / duplicated ownership by request family
- A high-value recurring boundary is the **JS/native bridge** itself:
  - `addJavascriptInterface(...)`
  - message-style bridge APIs
  - custom URL handoff / navigation callbacks
- `shouldInterceptRequest(...)` and related WebView hooks are useful orientation/observation boundaries, but they are not complete truth for decisive transport ownership.
- A key practical mistake worth normalizing in the KB is:
  - seeing the same host family in page JS and native code does **not** mean both sides own the same request role.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note.md`
- `topics/android-network-trust-and-pinning-localization-workflow-note.md`
- `sources/mobile-runtime-instrumentation/2026-03-15-android-network-trust-and-pinning-workflow-notes.md`

### External / search material
Search-layer queries:
- `Android WebView native mixed request ownership reverse engineering workflow`
- `Android WebView bridge network request ownership Frida reverse engineering`
- `Android app WebView native API mixed traffic diagnosis reverse engineering`

Primary externally consulted materials:
- Android Developers — WebView native bridges risk guidance
  - `https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridges`
- WebView Community Group issue on Native/WebView request/response sharing overlap
  - `https://github.com/WebView-CG/usage-and-challenges/issues/12`
- practical surfaced reference around Frida/WebView observation boundaries
  - `https://stackoverflow.com/questions/70904547/frida-intercept-all-webview-traffic`

### Source-quality judgment
- The source cluster was not strong enough for deep implementation claims about all hybrid-app architectures.
- It **was** strong enough for a practical, conservative workflow note because it consistently justified:
  - Native/WebView request overlap as a recurring problem
  - bridge surfaces as key ownership checkpoints
  - WebView request hooks as useful but incomplete observation boundaries
- `web_fetch` reliability was mixed in this environment:
  - Android Developers redirect chain failed through fetch
  - Stack Overflow fetch hit anti-bot / 403
  - the GitHub/WebView-CG discussion fetched successfully and provided useful direct wording for native/WebView request overlap
- Because of that, the resulting note stayed workflow-centered and conservative instead of overclaiming internals.

## 4. Reflections / synthesis
This run stayed aligned with the human correction and with the KB’s best recent pattern.

The weak move would have been:
- write a general page on WebView security or hybrid apps
- dump a set of WebView hook snippets without an ownership model
- or expand the taxonomy of Android networking without resolving a concrete analyst bottleneck

The stronger move was:
- isolate one recurring failure mode
- model it explicitly as an **ownership diagnosis** problem
- extend the mobile subtree’s earlier work on transport ownership into the hybrid WebView/native case
- and link the result directly to bridge boundaries, hook placement, and next-step routing into trust/signing notes

The best synthesis from this run is:

**In hybrid Android reversing, “WebView is involved” is not an explanation. The real leverage comes from separating intent owner, bridge boundary, transport owner, and response consumer for one request family at a time.**

That matters because it changes the next breakpoint.
Instead of logging everything everywhere, the KB now recommends:
- pick one decisive request family
- compare it against one non-target family
- inspect bridge registration/invocation
- then classify whether the case is page-owned, bridge-handoff, native-bootstrap, or mixed by request family

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/webview-native-mixed-request-ownership-workflow-note.md`

### Improved this run
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`

### New source note added
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-mixed-request-ownership-notes.md`

### Candidate future creation/improvement
- a future practical note on **bridge payload recovery and parameter handoff** once enough examples accumulate across hybrid apps
- a future note on **WebView challenge/token generation vs native submission ownership** if browser-like anti-bot workflows become common in mobile hybrids
- improve `topics/mobile-reversing-and-runtime-instrumentation.md` with a compact subsection linking:
  - WebView/native ownership diagnosis
  - Cronet/mixed transport ownership
  - network trust localization
  - signing/parameter recovery

## 6. Next-step research directions
1. Keep filling concrete mobile mid-case bottlenecks instead of returning to abstract network/app architecture pages.
2. High-value adjacent topics now include:
   - bridge payload recovery and structured argument capture
   - WebView/native mixed challenge or captcha handoff diagnosis
   - hybrid-app token/bootstrap generation where page JS and native transport split responsibility
   - gRPC / WebSocket / HTTP2 role ownership in mixed mobile stacks
3. Continue favoring notes that include:
   - request-family-first reasoning
   - boundary placement
   - explicit failure classes
   - compare-run methods
   - small code/pseudocode fragments
4. Keep the mobile subtree coherent as a sequence of practical entry notes:
   - environment drift
   - observation surface selection
   - trust localization
   - transport ownership
   - hybrid ownership
   - signature/path recovery

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated workflow page for **WebView / native mixed request ownership diagnosis**.
- Added explicit practical separation between:
  - intent owner
  - bridge boundary
  - transport owner
  - response consumer
- Added a four-way analyst classification:
  - pure WebView ownership
  - JS intent + native transport
  - native bootstrap + WebView consumer
  - mixed / duplicated ownership by request family
- Added concrete next-hook placement guidance for:
  - WebView navigation / bootstrap boundary
  - `shouldInterceptRequest(...)`
  - bridge registration / invocation boundary
  - native client / request-wrapper selection boundary
  - response-consumer boundary
- Added practical failure diagnosis for:
  - WebView-heavy UI being mistaken for WebView transport ownership
  - native client visibility being mistaken for ownership of the target family
  - over-trusting `shouldInterceptRequest(...)`
  - contradictory evidence caused by duplicated host families across both surfaces

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/webview-native-mixed-request-ownership-workflow-note.md`
  - `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-mixed-request-ownership-notes.md`
  - navigation updates in `topics/mobile-protected-runtime-subtree-guide.md` and `index.md`
  - this run report
- Next operational steps after writing this report:
  - commit the KB changes in `/root/.openclaw/workspace`
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, preserve local state and record the failure locally
