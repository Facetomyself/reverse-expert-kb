# Source Notes — DataDome / GeeTest / Kasada target-family cluster

Date: 2026-03-14
Collector: OpenClaw autonomous KB maintenance run
Scope: gather concrete, practitioner-facing signals for browser anti-bot / captcha target families that can support a practical workflow note rather than another abstract taxonomy page.

## Sources consulted

### 1. gravilk/datadome-documented
URL: https://github.com/gravilk/datadome-documented
Type: practitioner repository / notes
Observed via: `web_fetch`

Key usable signals:
- Claims a July 2023 working solver and notes likely target drift afterward.
- Describes the high-value entry point as a request to `https://api-js.datadome.co/js/` returning a `datadome` cookie.
- States that the browser data being sent was not encrypted/encoded in the examined version, but field semantics were still nontrivial.
- Lists representative client-side checks / features observed in that version:
  - screen size
  - execution timing
  - renderer information
  - webdriver / JSDom-like checks
  - timezone
  - plugins
  - `eval`-related check
  - audio/video capability support
  - browser-specific element existence
  - USB support
- Strong practical hint: find site URL and site key from the API request, then map variable names back into the script.

Usefulness for KB:
- Good grounding for a DataDome workflow centered on network-anchor-first, cookie/write-site tracing, and environment-drift comparison.
- Confirms a target shape where browser feature collection and challenge workflow are tightly coupled.

Reliability note:
- Old and explicitly version-sensitive; useful as family-shape evidence, not as a stable algorithm reference.

---

### 2. DataDome official slider documentation
URL: https://docs.datadome.co/docs/datadome-captcha
Type: official vendor documentation
Observed via: `web_fetch`

Key usable signals:
- Explicitly states the slider inspects technical and behavioral details.
- Lists concrete observed categories of signals:
  - max/current resolution, screen size, video quality, touch support
  - audio/video codecs, media extensions, plugins, browser checks
  - CPU / GPU information
  - JS consistency challenges, canvas rendering, execution times
  - mouse / touch / scrolling / keystroke / device movement dynamics
- Indicates the slider is intended to work across mobile/desktop and ties behavior to analytics / challenge outcomes.

Usefulness for KB:
- Good official confirmation that DataDome-family analysis must treat the challenge as a broader state-and-sensor workflow rather than image solving alone.
- Supports breakpoint/hook advice around environment collection, behavior capture, and challenge-transition timing.

Reliability note:
- Official high-level claims, not reverse-engineering detail. Useful for family-shape confirmation and scope, not implementation specifics.

---

### 3. gravilk/geetest-v4-slide-documented
URL: https://github.com/gravilk/geetest-v4-slide-documented
Type: practitioner repository / notes
Observed via: `web_fetch`

Key usable signals:
- Claims a July 2023 working Geetest V4 slide solver and notes likely drift risk.
- Characterizes GeeTest as collecting near to no browser information beyond a few IDs and the image solution in the studied version.
- Notes AES + RSA encryption around validation requests.
- Describes a concrete solving strategy built around a finite image corpus (~1200 possible images in the examined set), hashing, and manual labeling of offsets rather than full browser-state emulation.
- Mentions partial deobfuscation and deobfuscator scripts as fallback if the image-set assumption breaks.

Usefulness for KB:
- Strongly suggests GeeTest-family workflow should begin by deciding whether the real bottleneck is image artifact solving / request encryption rather than browser-environment reconstruction.
- Supports the idea that not all slider families deserve the same environment-heavy workflow.

Reliability note:
- Old and version-sensitive, but still highly useful as a family-distinction signal.

---

### 4. tramodule/Kasada-Solver
URL: https://github.com/tramodule/kasada-solver
Type: practitioner repository / reverse-engineering claim
Observed via: `web_fetch`

Key usable signals:
- Frames Kasada work around Client Token (CT) and CD / token-key value generation.
- Explicitly centers token generation, fingerprinting, obfuscation, and reverse engineering of anti-bot defenses.
- Implies a workflow where token-family generation and browser fingerprint/state coupling are central rather than image challenge solving.

Usefulness for KB:
- Supports treating Kasada-like targets as token-family / browser-state / polymorphic-wrapper cases rather than classic captcha-centric cases.
- Good justification for emphasizing request-role anchoring, pre-dispatch frame capture, compare-run drift analysis, and in-browser harnessing.

Reliability note:
- Extracted page content is high-level and partly self-promotional; use as family-shape evidence, not as proof of exact current internals.

---

## Cross-source synthesis

### Concrete family differences that matter analytically

#### DataDome family
- Practical object often looks like a challenge + browser sensor + cookie/token refresh workflow.
- High-value first anchor is often the challenge/bootstrap API request and resulting cookie / challenge state transitions.
- Environment and interaction signals appear materially important.

#### GeeTest family
- Practical object may be much more artifact/protocol-centric than environment-centric.
- High-value first question is often whether the main blocker is image position solving, request encryption, or challenge parameter packing.
- A browser-state-heavy workflow may be overkill on some GeeTest variants.

#### Kasada family
- Practical object looks more like polymorphic browser-side token generation with fingerprint/state coupling.
- High-value first anchor is often pre-dispatch request shaping and token-family attachment rather than visible captcha UI.
- Compare-run methodology and in-browser callable-contract recovery appear especially important.

### Reusable KB insight
A generic label like "slider" or "captcha" hides materially different analyst workflows:
- some families are environment-and-behavior heavy (DataDome)
- some are image/protocol/packing heavy (GeeTest, in the examined practitioner note)
- some are token-family / fingerprint / polymorphic-runtime heavy (Kasada)

This is exactly the kind of practical differentiation the KB should preserve.

## Candidate KB actions justified by this source cluster
- Create a concrete browser target-family note comparing DataDome / GeeTest / Kasada first-pass workflows.
- Add decision rules for when to prioritize:
  - cookie / request-attachment tracing
  - image/artifact solving path
  - browser-environment reconstruction
  - pre-dispatch frame capture / CDP evaluation
- Cross-link the note from browser risk-control, fingerprint/token, and browser subtree guide pages.

## Evidence limitations
- Most practitioner sources found here are version-sensitive and sometimes old.
- Extracted GitHub repository front pages are often summary-level only.
- This cluster is still good enough for family-shape workflow synthesis, but not for asserting stable current implementation details.
