# Browser Runtime Subtree Guide

Topic class: framework / guide page
Ontology layers: navigation, subtree map, domain-practice guide
Maturity: structured
Related pages:
- topics/js-browser-runtime-reversing.md
- topics/jsvmp-and-ast-based-devirtualization.md
- topics/browser-side-risk-control-and-captcha-workflows.md
- topics/browser-cdp-and-debugger-assisted-re.md
- topics/browser-debugger-detection-and-countermeasures.md
- topics/browser-environment-reconstruction.md
- topics/js-wasm-mixed-runtime-re.md
- topics/community-practice-signal-map.md

## Purpose
This page explains how to navigate the browser-runtime branch of the reverse-expert KB.

The browser subtree grew quickly because the manually curated community-practice source cluster contained unusually dense real-world material around:
- browser-side runtime observation
- CDP/debugger workflows
- JSVMP and AST-based devirtualization
- captcha and anti-bot analysis
- environment reconstruction
- JS/wasm mixed execution

This page exists to keep that growth coherent.

## Core claim
The browser-runtime branch should be read as a coordinated subtree, not as a loose pile of web-reversing notes.

Its organizing logic is:
- a browser-executed target exists as the parent problem
- different child pages describe different analyst entry surfaces into that problem
- those entry surfaces should be understood as complementary rather than competitive

## Parent page
### Browser runtime parent
- `topics/js-browser-runtime-reversing.md`

Use this page when the question is broad, such as:
- is this a browser-runtime reversing problem at all?
- is the key difficulty runtime behavior, browser environment, deobfuscation, anti-analysis, or protocol/state coupling?
- which child branch should I read next?

## Main child branches

### 1. JSVMP and AST-based devirtualization
- `topics/jsvmp-and-ast-based-devirtualization.md`

Read this when the main problem is:
- JSVMP
- AST-hostile transforms
- flattening / dispatcher recovery
- browser-side virtualized logic
- custom decompiler or transform workflows

### 2. Browser-side risk-control and captcha workflows
- `topics/browser-side-risk-control-and-captcha-workflows.md`

Read this when the main problem is:
- slider / click / gesture / silent captcha
- anti-bot client-side workflows
- fingerprint / token / challenge-response logic
- stateful request and retry behavior

### 3. Browser CDP and debugger-assisted RE
- `topics/browser-cdp-and-debugger-assisted-re.md`

Read this when the main problem is:
- locating live value-generation paths
- using breakpoints / stepping / CDP / DevTools for evidence
- runtime/network correlation inside browser execution
- deciding where debugger-assisted inspection gives the highest leverage

### 4. Browser debugger detection and countermeasures
- `topics/browser-debugger-detection-and-countermeasures.md`

Read this when the main problem is:
- the target appears to notice DevTools, breakpoints, or instrumentation
- debugger-visible behavior may be distorted, suppressed, or classified as risky
- you need to distinguish visible DevTools checks from CDP-side-effect or automation-surface detection
- the right next move may be quieter instrumentation or a different browser surface rather than more breakpoints

### 5. Browser environment reconstruction
- `topics/browser-environment-reconstruction.md`

Read this when the main problem is:
- 补环境
- reproducing browser APIs or state
- node-side reuse of browser bundles
- building a minimal harness for controlled execution
- separating functional environment needs from anti-analysis checks

### 6. JS / WASM mixed runtime RE
- `topics/js-wasm-mixed-runtime-re.md`

Read this when the main problem is:
- JS ↔ wasm boundary recovery
- wasm-backed browser-side logic
- mixed execution paths for tokens, crypto, or challenge logic
- lifting / wrapping / externalizing wasm-backed functionality

## How the branches relate
These child pages are not isolated.
They often form a pipeline.

### Common path A: risk-control target
Typical path:
1. Start at `js-browser-runtime-reversing.md`
2. Move to `browser-side-risk-control-and-captcha-workflows.md`
3. Use `browser-cdp-and-debugger-assisted-re.md` to observe live value paths
4. If the target reacts to observation, move to `browser-debugger-detection-and-countermeasures.md`
5. Use `browser-environment-reconstruction.md` if the logic must be replayed or externalized
6. Use `jsvmp-and-ast-based-devirtualization.md` if JSVMP or flattening blocks further progress

### Common path B: JSVMP-heavy browser target
Typical path:
1. Start at `js-browser-runtime-reversing.md`
2. Move to `jsvmp-and-ast-based-devirtualization.md`
3. Use `browser-cdp-and-debugger-assisted-re.md` to align transformed structure with live behavior
4. If debugger-visible execution looks unstable or defensive, move to `browser-debugger-detection-and-countermeasures.md`
5. Use `browser-environment-reconstruction.md` if replay or external harnessing becomes necessary

### Common path C: wasm-backed target
Typical path:
1. Start at `js-browser-runtime-reversing.md`
2. Move to `js-wasm-mixed-runtime-re.md`
3. Use `browser-cdp-and-debugger-assisted-re.md` to inspect JS↔wasm boundary behavior
4. If instrumentation appears visible or untrustworthy, move to `browser-debugger-detection-and-countermeasures.md`
5. Use `browser-environment-reconstruction.md` if wasm must be externalized under controlled conditions

## What this subtree is best at
The browser-runtime subtree is especially strong for:
- runtime-first web reverse engineering
- anti-bot / risk-control / challenge workflows
- browser-side protected code analysis
- environment reconstruction and externalization
- JSVMP and AST-based deobfuscation
- browser-domain instrumentation via CDP / debugger surfaces
- debugger-detection and observation-pressure reasoning

## What this subtree is weaker at
This subtree is currently weaker on:
- formal benchmark coverage specific to browser RE
- deeper normalization of debugger-detection countermeasures
- deeper normalization of JS/wasm protection patterns
- systematic separation between browser-only and hybrid mobile-webview cases

### 7. Browser fingerprint and state-dependent token generation
- `topics/browser-fingerprint-and-state-dependent-token-generation.md`

Read this when the main problem is:
- browser-side request values depend on fingerprint inputs, timing, retry state, or other browser-local context
- you need to recover the local input → transform → output chain for a token or field
- environment reconstruction and live observation both seem necessary to explain the value

### 8. Concrete target-family workflow notes
Current concrete notes:
- `topics/reese84-and-utmvc-workflow-note.md`
- `topics/datadome-geetest-kasada-workflow-note.md`
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
- `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md`
- `topics/browser-parameter-path-localization-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/acw-sc-v2-cookie-bootstrap-and-consumer-path-note.md`
- `topics/bytedance-web-request-signature-workflow-note.md`

Read this branch when the main problem is:
- you are working on a browser anti-bot or captcha family and need a concrete first-pass workflow
- you need breakpoint placement, compare-run strategy, and harness externalization guidance
- you need to distinguish whether the target is mainly state/sensor-driven, artifact/packing-driven, token-contract-driven, request-signature-family driven, parameter-path-localization driven, or request-boundary-backtrace driven
- the issue is not abstract taxonomy but how to approach a real target family

## Suggested next expansions from this subtree
The most natural next child pages include:
- `topics/js-wasm-boundary-tracing.md`
- `topics/targeted-evidence-trust-calibration.md`
- `topics/cdp-side-effect-and-automation-signal-analysis.md`

## Source anchor
The subtree is strongly justified by the practitioner cluster documented in:
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`
- `topics/community-practice-signal-map.md`

## Bottom line
The browser-runtime subtree is now one of the most developed applied branches in the KB.

Its pages should be read as a coordinated set of analyst entry surfaces into browser-side reverse engineering:
- structural recovery
- interaction workflow recovery
- instrumentation / observability
- environment reconstruction
- mixed-runtime semanticson
- mixed-runtime semantics