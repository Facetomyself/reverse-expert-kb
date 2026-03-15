# Run Report — 2026-03-15 11:00 Asia/Shanghai

## 1. Scope this run
This run started with a full KB state check and recent-run scan:
- root docs (`README.md`, `index.md`)
- browser and mobile/practice subtree guides
- recent practical workflow pages
- recent run reports and source notes

The purpose of the run was to keep following the human correction:
**do not spend the hour on more abstract taxonomy; add practical, target-grounded, code-adjacent workflow material.**

Because the last several runs heavily expanded the browser subtree, this hour intentionally shifted to a recurring **mobile mid-case bottleneck** that still lacked a dedicated practical note:
- Android network trust-path localization
- SSL pinning / certificate validation diagnosis
- Java `OkHttp` / `TrustManager` paths vs Cronet / Flutter / native TLS paths
- routing-vs-trust-vs-post-TLS failure classification

The aim was not to create another generic pinning page, but to capture how analysts actually localize the decisive trust boundary in real Android cases.

## 2. New findings
- A stable source cluster strongly supports a **workflow note** on Android trust-path localization rather than another broad mobile-security synthesis page.
- The most durable analyst object is not “SSL pinning” in the abstract, but this concrete chain:

```text
request trigger
  -> stack ownership (OkHttp / platform / Cronet / Flutter-native / mixed)
  -> routing/proxy behavior
  -> trust or pin registration boundary
  -> first decisive validation boundary
  -> request outcome (no route / TLS fail / post-TLS fail / success)
```

- The biggest practical early decision is often **stack classification**, not bypass selection.
- Public case material strongly supports using **registration/attachment boundaries** as first anchors:
  - `CertificatePinner.Builder.add(...)`
  - trust-store material loading
  - native-engine trust callback setup
- Flutter/native-engine evidence reinforces that many analysts waste time because they keep deepening Java hooks after the decisive path has already moved into native TLS validation.
- A very useful failure split emerged for the KB:
  - routing failure
  - Java trust failure
  - native trust failure
  - post-TLS / later application drift

That split makes the note more actionable than a generic “bypass certificate pinning” article.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/android-observation-surface-selection-workflow-note.md`
- `topics/mobile-signing-and-parameter-generation-workflows.md`
- `topics/environment-differential-diagnosis-workflow-note.md`
- recent browser/mobile workflow pages for style and practical-structure alignment

### External / search material
Search-layer queries:
- `Android SSL pinning OkHttp Cronet reverse engineering workflow trust manager certificate pinner`
- `Frida Android SSL pinning Cronet OkHttp trust manager workflow`
- `Android certificate pinning OkHttp Cronet native boringSSL workflow reverse engineering`

Readable/fetched or search-derived sources used:
- `https://github.com/httptoolkit/frida-interception-and-unpinning`
- `https://blog.nviso.eu/2019/04/02/circumventing-ssl-pinning-in-obfuscated-apps-with-okhttp/`
- `https://mas.owasp.org/MASTG/techniques/android/MASTG-TECH-0012/`
- `https://blog.mindedsecurity.com/2024/05/bypassing-certificate-pinning-on.html`

### Source-quality judgment
- The HTTP Toolkit repo was useful as maintained operational evidence that real Android interception/unpinning often spans multiple layers and fallback handling.
- The NVISO case study was especially valuable because it preserves a strong **boundary-first** workflow for obfuscated OkHttp targets.
- OWASP MASTG was useful as a normalization source, especially for identifying where tool coverage ends and manual localization begins.
- The Flutter/Minded Security writeup was important because it anchors the Java-vs-native split with a concrete native-engine case.

Overall, this source cluster justified a **practical workflow note**, not another abstract mobile trust/taxonomy page.

## 4. Reflections / synthesis
This run stayed aligned with the user’s correction.

The weak move would have been:
- write another broad mobile-security abstraction page
- or collect more “SSL pinning bypass resources” without integrating them

The stronger move was:
- identify a recurring analyst bottleneck in mid-case Android work
- center the page on **one target request** and **one decisive trust boundary**
- explicitly separate routing, Java trust, native trust, and post-TLS drift
- tie the note back into the existing mobile subtree as an entry point before signing/challenge workflows

The best synthesis from this run is that Android trust work should usually be modeled as a **stack-ownership and trust-boundary localization problem**, not as a monolithic pinning problem.

That makes the new page practical:
- anchor one request
- decide who owns it
- decide whether routing failed first
- locate registration before final validation
- classify the first real failure boundary
- only then deepen hooks or patching

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/android-network-trust-and-pinning-localization-workflow-note.md`

### Improved this run
- `index.md`
- `topics/mobile-protected-runtime-subtree-guide.md`

### New source note added
- `sources/mobile-runtime-instrumentation/2026-03-15-android-network-trust-and-pinning-workflow-notes.md`

### Candidate future creation/improvement
- improve `topics/mobile-reversing-and-runtime-instrumentation.md` with a compact subsection linking network trust-path localization to broader runtime access strategy
- consider a future concrete note specifically for **Cronet path localization and request ownership diagnosis** if more source evidence accumulates
- consider a future concrete note for **Flutter native transport and TLS callback localization** if more native-engine case material accumulates
- consider a later cross-target page on **routing success vs trust success vs protocol success** only after more concrete cases exist

## 6. Next-step research directions
1. Continue filling the mobile subtree with practical “first bottleneck” workflow pages rather than new abstract synthesis leaves.
2. Prefer real recurring analyst bottlenecks such as:
   - Cronet request ownership
   - WebView/native mixed traffic boundaries
   - gRPC/HTTP2 mobile path localization
   - post-TLS application trust and device-attestation coupling
3. Keep reinforcing diagnosis layers that route analysts toward deeper workflow notes only after the first divergence is classified.
4. Continue balancing browser and mobile growth so the KB remains a practical playbook across both branches.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated Android network trust-path workflow centered on:
  - one-target-request-first analysis
  - stack classification before bypass choice
  - routing-vs-trust-vs-post-TLS separation
  - registration-boundary-first localization
  - Java-vs-native validation diagnosis
- Added explicit breakpoint/hook placement for:
  - request-builder/client ownership boundary
  - pin-registration / trust-registration boundary
  - Java `TrustManager` / verifier boundary
  - native TLS / engine validation boundary
  - lower-boundary routing observation
- Added practical failure diagnosis for:
  - mistaking missing routing for pinning failure
  - staying too long in Java hooks when the decisive path is native
  - over-cleaning obfuscated smali instead of anchoring method shape / argument shape
  - mistaking post-TLS app/protocol failure for unresolved trust validation

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/android-network-trust-and-pinning-localization-workflow-note.md`
  - `sources/mobile-runtime-instrumentation/2026-03-15-android-network-trust-and-pinning-workflow-notes.md`
  - navigation updates in `index.md` and `topics/mobile-protected-runtime-subtree-guide.md`
  - this run report
- A small exact-match edit mismatch occurred while cleaning a duplicated trailing line in `index.md`; it was corrected immediately with a direct file rewrite and did not affect KB content.
- Next operational steps after writing this report:
  - commit workspace changes
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, preserve local state and record the failure
