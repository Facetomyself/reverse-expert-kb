# Run Report — 2026-03-15 12:00 Asia/Shanghai

## 1. Scope this run
This run continued the post-correction pivot away from abstract taxonomy and toward practical, case-driven reverse-engineering workflow notes.

The run started with a KB state refresh across:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent concrete browser and mobile workflow pages
- recent run reports
- recent source notes

The previous hour had added a practical note on Android trust-path localization.
That naturally exposed the next adjacent bottleneck that still deserved its own concrete page:

- **Android request ownership diagnosis when Java-visible OkHttp/Retrofit surfaces do not match real transport behavior**
- especially mixed cases involving **Cronet-backed transport**, bridge layers, or request-family-specific ownership splits

The goal was not to produce a generic Cronet summary.
The goal was to add a reusable workflow note for how analysts decide whether a target request is:
- plain OkHttp-owned
- OkHttp-visible but Cronet-transported
- direct Cronet/native-owned
- mixed by request family

## 2. New findings
- A stable source cluster supports a dedicated **concrete workflow note** for Cronet request ownership and mixed-stack diagnosis.
- The most important practical split is **assembly owner vs transport owner**:
  - Java-visible request assembly does not guarantee Java/OkHttp transport ownership.
- The `cronet-transport-for-okhttp` bridge documentation is especially valuable because it makes the misleading case explicit:
  - apps can retain familiar OkHttp/Retrofit request surfaces
  - while bypassing substantial OkHttp core network behavior underneath.
- For KB purposes, the strongest reusable classification is:
  - plain OkHttp ownership
  - OkHttp surface + Cronet transport ownership
  - direct Cronet/native ownership
  - mixed ownership by request family
- This classification explains a very common practical symptom cluster:
  - some hooks or interception methods seem to work
  - but only for low-value or non-target traffic
  - while the decisive request family behaves differently
  - leading analysts to misdiagnose the issue as flaky tooling or generic anti-hooking.
- The most productive next hook point in these cases is often not deep native tracing, but the **owner-selection boundary**:
  - client factory selection
  - call-factory setup
  - Cronet interceptor attachment
  - engine builder / engine handoff

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/mobile-signature-location-and-preimage-recovery-workflow-note.md`
- `topics/environment-differential-diagnosis-workflow-note.md`
- `topics/android-network-trust-and-pinning-localization-workflow-note.md`

### External / search material
Search-layer queries:
- `Android Cronet request ownership reverse engineering workflow okhttp native transport`
- `Cronet reverse engineering android request path frida native workflow`
- `Android app Cronet okhttp mixed stack traffic diagnosis reverse engineering`

Primary externally consulted materials:
- Android Developers — Cronet integration / use Cronet with other libraries
  - `https://developer.android.com/develop/connectivity/cronet/integration`
- Android Developers — `CronetInterceptor` reference
  - `https://developer.android.com/develop/connectivity/cronet/okhttp/reference/com/google/net/cronet/okhttptransport/CronetInterceptor`
- Android Developers — `CronetEngine` reference
  - `https://developer.android.com/develop/connectivity/cronet/reference/org/chromium/net/CronetEngine`
- Google GitHub — `google/cronet-transport-for-okhttp`
  - `https://github.com/google/cronet-transport-for-okhttp`
- GitHub case material — `neals-sudo/okhttp3_interceptor`
  - `https://github.com/neals-sudo/okhttp3_interceptor`
- Stack Overflow discussion on likely-Cronet native TLS path localization
  - `https://stackoverflow.com/questions/79814253/frida-on-android-how-to-locate-native-tls-verify-pinning-path-likely-cronet-whe`

### Source-quality judgment
- The strongest evidence came from official Cronet integration and bridge semantics plus the transport-for-OkHttp repo documentation.
- Some fetches were imperfect in this environment:
  - Android Developers pages hit redirect limits through `web_fetch`
  - Stack Overflow fetch hit anti-bot / 403
- Because of that, the synthesis stayed conservative and workflow-centered rather than overclaiming implementation internals.
- This source cluster was still sufficient to justify a practical note focused on diagnosis boundaries and analyst decisions.

## 4. Reflections / synthesis
This run stayed aligned with the human correction.

The weak move would have been:
- add another broad page on Android networking stacks
- or collect a loose Cronet source dump
- or write an abstract taxonomy about transport layers

The stronger move was:
- isolate one recurring analyst bottleneck
- model it as a request-ownership problem
- explicitly separate Java-visible request assembly from true transport ownership
- normalize mixed-stack behavior as a common diagnosis case rather than an oddity
- connect the result directly to existing notes on trust-path localization, environment drift, and mobile signature recovery

The best synthesis from this run is:

**many Android “pinning / proxy / interception” cases are mis-scoped because the analyst has not yet classified request ownership.**

That is actionable because it changes what the next breakpoint should be.
Instead of blindly adding trust hooks or diving into native code, the KB now recommends first asking:
- which request family matters,
- which client/factory/engine owns it,
- and whether the visible Java request surface is actually the decisive layer.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note.md`

### Improved this run
- `index.md`
- `topics/mobile-protected-runtime-subtree-guide.md`

### New source note added
- `sources/mobile-runtime-instrumentation/2026-03-15-cronet-request-ownership-and-mixed-stack-diagnosis-notes.md`

### Candidate future creation/improvement
- a future concrete note on **Cronet trust / native validation boundary localization** if enough case material accumulates beyond today’s ownership-focused scope
- a future note on **WebView / app-native mixed request ownership diagnosis** if the source cluster matures
- improve `topics/mobile-reversing-and-runtime-instrumentation.md` with a compact subsection linking request ownership, trust-path localization, and signature-path localization

## 6. Next-step research directions
1. Keep strengthening the mobile subtree with early/mid-case practical diagnosis notes rather than more high-level synthesis.
2. Good next mobile bottlenecks to fill include:
   - WebView/native mixed traffic ownership
   - gRPC / HTTP2 request-family localization in mobile apps
   - Cronet-native trust-boundary and validation callback localization
   - post-transport application-trust / risk-score consequence diagnosis
3. Maintain the KB’s new pattern of pairing broad branch guides with concrete workflow entry notes.
4. Continue preferring source clusters that support:
   - breakpoint placement
   - owner-selection boundaries
   - failure splits
   - compare-run methods
   - code-adjacent harness sketches

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated workflow page for **Cronet request ownership and mixed-stack diagnosis**.
- Added explicit practical distinctions between:
  - assembly owner
  - transport owner
- Added a four-way analyst classification:
  - plain OkHttp
  - OkHttp + Cronet transport
  - direct Cronet/native
  - mixed request-family ownership
- Added concrete next-hook placement guidance for:
  - request assembly boundary
  - client / call-factory selection boundary
  - Cronet bridge setup boundary
  - engine builder / configuration boundary
- Added practical failure diagnosis for:
  - Java-visible request paths that do not own transport behavior
  - partially successful hooks in mixed-stack apps
  - wasted deep native tracing before owner-selection boundaries are checked
  - mistaken assumption that ignored OkHttp settings imply custom anti-analysis rather than Cronet-backed transport semantics

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/cronet-request-ownership-and-mixed-stack-diagnosis-workflow-note.md`
  - `sources/mobile-runtime-instrumentation/2026-03-15-cronet-request-ownership-and-mixed-stack-diagnosis-notes.md`
  - navigation updates in `index.md` and `topics/mobile-protected-runtime-subtree-guide.md`
  - this run report
- Next operational steps after writing this report:
  - commit the KB changes in `/root/.openclaw/workspace`
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, preserve local state and record the failure locally in the run report
