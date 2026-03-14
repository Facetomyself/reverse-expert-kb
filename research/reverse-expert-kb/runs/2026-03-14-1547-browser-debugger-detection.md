# Reverse Expert KB Run Report — 2026-03-14 15:47 Asia/Shanghai

## 1. Scope this run
This run focused on strengthening the **browser-runtime subtree** by filling a structural gap between:
- `topics/browser-cdp-and-debugger-assisted-re.md`
- `topics/observation-distortion-and-misleading-evidence.md`
- browser anti-bot / risk-control pages

The main task was to normalize **browser debugger detection and countermeasure reasoning** into a dedicated topic page rather than leaving it scattered across CDP/debugger, anti-tamper, and practitioner source notes.

## 2. New findings
- Browser anti-debugging is well established enough to justify a dedicated KB page, not just incidental mentions:
  - USENIX Security 2021 abstract reports **9 anti-debugging techniques** and substantial in-the-wild prevalence.
- The problem space clearly spans multiple mechanism families rather than one generic “anti-debugging” bucket:
  - debugger traps
  - resize/timing/console/source-map/feature side channels
  - CDP-side-effect and automation-surface detection
- A useful synthesis distinction emerged:
  - **what is being detected** (visible DevTools, debugger semantics, CDP side effects, automation surface)
  - versus **what the consequence is** (blocking, redirecting, decoying, risk scoring, evidence distortion)
- Countermeasure practice suggests a meaningful split between:
  - JS-level detector patching
  - browser/runtime-surface changes such as quieter instrumentation or patched browsers
- Anti-bot / anti-automation literature and vendor material make it clear that browser debugger detection overlaps with risk scoring and challenge workflows, not only local nuisance or anti-analysis behavior.

## 3. Sources consulted
### Existing KB material
- `README.md`
- `index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-cdp-and-debugger-assisted-re.md`
- `topics/js-browser-runtime-reversing.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/environment-state-checks-in-protected-runtimes.md`
- `topics/observation-distortion-and-misleading-evidence.md`
- recent run note: `runs/2026-03-14-1516-collaborative-malware-analysis.md`

### New external/browser-runtime sources used this run
- USENIX Security 2021 landing page for **U Can't Debug This: Detecting JavaScript Anti-Debugging Techniques in the Wild**
  - https://www.usenix.org/conference/usenixsecurity21/presentation/musch
- Curated practitioner list:
  - https://github.com/weizman/awesome-javascript-anti-debugging
- DataDome threat-research article:
  - https://datadome.co/threat-research/how-new-headless-chrome-the-cdp-signal-are-impacting-bot-detection
- ByteHide devtools-blocking docs:
  - https://docs.bytehide.com/platforms/javascript/products/shield/devtools-blocking
- Pixelmelt practitioner write-up:
  - https://blog.pixelmelt.dev/defeating-devtools-detection

### Source artifact created
- `sources/browser-runtime/2026-03-14-browser-debugger-detection-notes.md`

## 4. Reflections / synthesis
The main synthesis improvement this run is that the browser-runtime subtree now treats **instrumentation** and **counter-instrumentation** as paired pages rather than leaving the latter implicit.

That matters because browser RE often depends on DevTools/CDP-style observation, but many real targets make that observation visible. Once that happens, the analyst is no longer simply tracing logic; they are negotiating with a protected runtime that may:
- block
- classify
- distort
- decoy

This framing also improves subtree coherence:
- `browser-cdp-and-debugger-assisted-re` now reads as the positive instrumentation page
- `browser-debugger-detection-and-countermeasures` now reads as the mirrored contested-observability page
- `observation-distortion-and-misleading-evidence` remains the more general cross-domain evidence-quality bridge

A second useful synthesis point is that “browser anti-debugging” should not be treated as a malware-only or nuisance-only concept. The source cluster shows it spans:
- evasive/malicious sites
- commercial code-protection features
- anti-bot / risk-control instrumentation detection

That broadens the KB’s protected-runtime interpretation in a justified way.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/browser-debugger-detection-and-countermeasures.md`

### Improved this run
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-cdp-and-debugger-assisted-re.md`
- `topics/js-browser-runtime-reversing.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `index.md`

### Strong candidates for future creation/improvement
- `topics/cdp-side-effect-and-automation-signal-analysis.md`
- `topics/devtools-open-side-channels.md`
- `topics/browser-anti-debugging-evidence-trust.md`
- `topics/targeted-evidence-trust-calibration.md`

## 6. Next-step research directions
- Do a dedicated pass on **CDP-side-effect detection** as a child page, especially the overlap with anti-bot automation detection.
- Normalize **DevTools-open side channels** separately from CDP/automation-side signals.
- Deepen the evidence-quality side by connecting browser anti-debugging more explicitly to trust calibration methods.
- Gather stronger academic/full-text sources on browser anti-debugging and debugger-detection countermeasures when source access is better.
- Continue growing the browser subtree in a way that preserves the distinction between:
  - instrumentation
  - anti-instrumentation
  - environment reconstruction
  - stateful browser risk-control workflows

## Sync / preservation notes
- Local KB progress was preserved in canonical topic/source/run files.
- External source access had minor friction this run:
  - SSRN fetch returned 403/holding-page content
  - direct PDF extraction quality was poor for at least one academic PDF
- These failures did not block KB integration because HTML landing pages and other source pages were sufficient for this synthesis pass.
