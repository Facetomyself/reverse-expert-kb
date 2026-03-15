# Run Report — 2026-03-15 15:00 Asia/Shanghai

## 1. Scope this run
This run continued the corrected KB direction toward practical, target-adjacent mobile reversing notes instead of adding more abstract taxonomy.

The starting review covered:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent mobile subtree structure
- the prior hybrid note `topics/webview-native-mixed-request-ownership-workflow-note.md`
- recent mobile workflow notes on trust localization, mixed-stack ownership, and signature/preimage recovery
- recent source notes under `sources/mobile-runtime-instrumentation/`

The practical gap after the previous hybrid-ownership run was clear:
- the KB already had a useful note for deciding whether a hybrid app’s decisive request family belongs to WebView, native code, or a mixed path
- but it still lacked the next operational note analysts often need in the same case:
  - **how to recover what actually crosses the WebView/native bridge before native normalization destroys structure**

This run therefore focused on creating a concrete workflow page for:
- object-bridge payload capture
- message-channel payload capture
- custom-URL/navigation handoff payload capture
- alignment of bridge payload recovery with downstream native consumer selection

## 2. New findings
- The existing hybrid ownership page justified a narrower child note rather than another broad WebView/hybrid synthesis page.
- The most reusable practical split here is:
  - **bridge registration surface**
  - **bridge invocation surface**
  - **payload shape**
  - **first native consumer**
- There are at least three durable bridge families worth treating as equal-class workflow targets:
  - `addJavascriptInterface` object bridges
  - `WebMessage` / `WebMessagePort` / message-channel handoff
  - custom-URL / navigation handoff via `shouldOverrideUrlLoading(...)`
- A strong practical distinction emerged and was made explicit in the KB:
  - **bridge payload recovery is not the same as transport ownership diagnosis**
- The highest-value evidence to preserve in many hybrid cases is not the final opaque token, but the last still-structured payload crossing the bridge.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/webview-native-mixed-request-ownership-workflow-note.md`
- `topics/mobile-signature-location-and-preimage-recovery-workflow-note.md`
- `topics/cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note.md`
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-mixed-request-ownership-notes.md`

### External / search material
Search-layer queries:
- `Android WebView addJavascriptInterface reverse engineering bridge payload capture`
- `Android WebMessagePort WebView bridge reverse engineering payload`
- `Android shouldOverrideUrlLoading custom scheme bridge reverse engineering`

Primary externally consulted materials:
- Android Developers — WebView native bridges guidance
  - `https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridges`
- Android Developers — `WebView` API reference for message-channel primitives
  - `https://developer.android.com/reference/android/webkit/WebView`
- OWASP MASTG — Java objects exposed through WebViews
  - `https://mas.owasp.org/MASTG/tests/android/MASVS-PLATFORM/MASTG-TEST-0033/`
- practical implementation/problem evidence around custom URL bridge handling
  - `https://github.com/facebook/react-native/issues/10055`

### Source-quality judgment
- Android Developers and OWASP MASTG were strong enough for durable bridge-model and API-shape anchors.
- Search results and practical issue/Q&A material were useful for confirming recurring bridge families and observation boundaries.
- `web_fetch` on some official docs was fragile in this environment because redirect chains exceeded the tool’s limit.
- That failure did not block useful synthesis because the canonical OWASP path fetched successfully and the search/result cluster still gave enough grounded support for a workflow-centered note.

## 4. Reflections / synthesis
This run stayed aligned with the human correction by refusing the easy but weaker move.

The weak move would have been:
- add another general page about WebView communication
- add broad bridge-security taxonomy
- or dump a few hook snippets without showing why analysts should care about payload shape and first native consumer

The stronger move was:
- narrow the problem to a recurring analyst bottleneck
- define concrete bridge families
- explain how to capture registration and invocation separately
- preserve structured payloads before native packing/normalization
- and explicitly separate payload recovery from later transport ownership questions

The best synthesis from this run is:

**In hybrid Android cases, the bridge is often the last place where request intent is still structured. If you miss that boundary, later native traces may show only opaque tokens or generic request assembly, not the meaning of the handoff.**

That changes breakpoint choice.
Instead of “more WebView hooks” or “deeper native hooks,” the KB now recommends:
- identify the bridge family first
- capture registration for naming/topology
- capture invocation for timing/payload
- preserve the last structured payload
- then follow the first native consumer into request ownership, trust, or signature recovery as needed

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`

### Improved this run
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`

### New source note added
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-bridge-payload-recovery-notes.md`

### Candidate future creation/improvement
- a future concrete note on **bridge payload decoding and schema recovery** once more examples accumulate across real app families
- a future note on **bridge-return / native-to-page response handoff diagnosis** for cases where decisive data flows back into WebView state after native processing
- improve `topics/mobile-reversing-and-runtime-instrumentation.md` with a compact subsection linking:
  - hybrid ownership diagnosis
  - bridge payload recovery
  - transport ownership diagnosis
  - trust-path localization
  - signature/preimage recovery

## 6. Next-step research directions
1. Continue filling the hybrid/mobile branch with concrete bottleneck notes rather than broad architecture pages.
2. High-value adjacent topics now include:
   - bridge payload decoding and field-schema recovery
   - native-to-page response handoff diagnosis
   - hybrid challenge/token handoff where page logic generates request intent but native transport or signing owns the decisive step
   - mixed WebView/native request-family split where different bridge methods feed different request roles
3. Keep preferring pages that include:
   - target pattern / scenario
   - concrete workflow
   - registration/invocation hook placement
   - payload-shape preservation
   - likely failure modes
   - route-forward guidance into trust or signing notes
4. Keep the mobile subtree coherent as a practical sequence:
   - environment drift
   - observation surface selection
   - trust localization
   - transport ownership
   - hybrid ownership
   - bridge payload recovery
   - signature/path recovery

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated workflow page for **WebView/native bridge payload recovery**.
- Added explicit equal-class treatment of three bridge families:
  - `addJavascriptInterface`
  - message-channel / `WebMessagePort`
  - custom-URL / navigation handoff
- Added concrete guidance to separate:
  - registration capture
  - invocation capture
  - payload shape
  - first native consumer
- Added practical advice to preserve the last structured payload before native normalization/packing.
- Added explicit failure diagnosis for:
  - over-trusting page-side callbacks
  - assuming no bridge because `addJavascriptInterface` is absent
  - dismissing custom URLs as navigation noise
  - capturing final token output while missing the bridge preimage

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/webview-native-bridge-payload-recovery-workflow-note.md`
  - `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-bridge-payload-recovery-notes.md`
  - navigation updates in `topics/mobile-protected-runtime-subtree-guide.md` and `index.md`
  - this run report
- A tooling fragility encountered this run was also logged locally:
  - `web_fetch` redirect-limit failures on some official docs URLs
- Next operational steps after writing this report:
  - commit the KB changes in `/root/.openclaw/workspace`
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, preserve local state and record the failure locally
