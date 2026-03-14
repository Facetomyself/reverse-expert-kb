# Run Report — 2026-03-14 18:00 Asia/Shanghai

## 1. Scope this run
Pivot the browser-runtime branch further toward concrete, family-differentiated practice.

Instead of adding another abstract browser anti-bot synthesis page, this run focused on a practical gap:
- the KB already had strong notes on Reese84 / ___utmvc and CDP-guided token analysis
- but it still lacked a grounded page explaining that not all browser "slider/captcha/anti-bot" families deserve the same first-pass workflow

This run therefore targeted three recurring families with materially different analyst shapes:
- DataDome-like workflows
- GeeTest-like workflows
- Kasada-like workflows

## 2. New findings

### A. "Slider" is too coarse a category to drive analyst workflow
The source cluster made it clear that a single umbrella label like "slider" or even "browser anti-bot" hides important practical differences.

A useful operational split is:
- **DataDome-like**: challenge/bootstrap + browser sensor / consistency / behavior collection + cookie/token state transitions
- **GeeTest-like**: challenge artifact / image answer path + validation-request packing / encryption
- **Kasada-like**: pre-dispatch token-family generation + fingerprint/state coupling + obfuscated live request-shaping path

This is exactly the kind of differentiation the KB needs more of.

### B. DataDome-family work is best framed as state/sensor/challenge tracing, not only captcha solving
The practitioner repo summary plus official slider documentation both point to a challenge family shaped by:
- browser/environment feature collection
- behavior and timing signals
- challenge/cookie state transitions
- consistency checks across browser/runtime observations

The practical implication is that DataDome-like analysis often rewards:
- bootstrap/challenge-response anchoring
- cookie write/update tracing
- environment-collection observation
- compare-run testing across browser-state changes

### C. GeeTest-family work can be much more answer-object / packing centric than environment centric
The GeeTest V4 practitioner note strongly suggests a very different practical emphasis in the studied version:
- limited browser information collection
- image challenge and solution path as a central object
- encrypted validation request packaging as the important transform boundary

The practical implication is that analysts should not automatically jump into full browser-environment reconstruction just because a target is a slider/captcha family.

### D. Kasada-family work is better approached as live token-contract recovery
The Kasada cluster reinforced a token-family view:
- identify the exact request role carrying CT/CD-like fields
- locate the final attachment path
- capture the paused live frame where the token function plus helper scope coexist
- recover the callable contract before trying to port or externalize

This fits well with the existing KB page on CDP-guided token generation analysis.

## 3. Sources consulted
- `sources/browser-runtime/2026-03-14-datadome-geetest-kasada-notes.md`
- GitHub repo summary: `https://github.com/gravilk/datadome-documented`
- GitHub repo summary: `https://github.com/gravilk/geetest-v4-slide-documented`
- GitHub repo summary: `https://github.com/tramodule/kasada-solver`
- Official DataDome slider documentation: `https://docs.datadome.co/docs/datadome-captcha`
- Search-layer exploratory query cluster over DataDome / GeeTest / Kasada target families

## 4. Reflections / synthesis
This run produced a useful structural correction for the browser subtree.

Previously, the KB already knew that browser anti-bot analysis is stateful, runtime-heavy, and often coupled to token generation.
That part was true but still too blended.

What the KB needed was a more opinionated practical claim:
- **different protection families deserve different first-pass workflows**
- if the analyst fails to classify the family shape early, they may spend hours on the wrong surface

The new page deliberately encodes a family-differentiated workflow:
- DataDome-like -> trace challenge/bootstrap, sensor collection, cookie refresh, state transitions
- GeeTest-like -> trace answer object, image/challenge parameters, validation packing/encryption boundary
- Kasada-like -> trace request-finalization path, live token contract, paused frame, pre-dispatch helper scope

That is much closer to how analysts actually work.

## 5. Candidate topic pages to create or improve
Improved this run:
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/browser-fingerprint-and-state-dependent-token-generation.md`
- `topics/browser-runtime-subtree-guide.md`
- `index.md`

Created this run:
- `topics/datadome-geetest-kasada-workflow-note.md`

Candidate future practical pages:
- a concrete Cloudflare Turnstile / challenge-transition workflow note
- a concrete DataDome challenge-bootstrap / cookie refresh workflow note if enough stable evidence accumulates
- a browser image-artifact vs stateful token-family decision note spanning GeeTest / other visual families

## 6. Next-step research directions
1. Continue the browser subtree in this same concrete mode: prefer target-family and workflow-note pages over more taxonomy-first expansion.
2. Add at least one more browser-family workflow note where the main practical issue is challenge transition or response-driven refresh.
3. Deepen one DataDome-like note only if enough evidence supports something more specific than generic family-shape guidance.
4. Continue looking for target families where the main analyst mistake is choosing the wrong observation surface too early.

## 7. Concrete scenario notes or actionable tactics added this run
Added actionable tactics through the new workflow note, including:
- classify the target before doing heavy code cleanup:
  - state/sensor/challenge-driven
  - artifact/packing-driven
  - token-contract-driven
- choose breakpoints by family:
  - DataDome-like: bootstrap/cookie/sensor hooks
  - GeeTest-like: answer-object / pack / encrypt hooks
  - Kasada-like: request-finalization / paused call-frame hooks
- capture the highest-value structured artifact before irreversible transform:
  - DataDome-like: signal/state object
  - GeeTest-like: answer object before encryption
  - Kasada-like: live callable contract and input object
- use family-specific failure diagnosis:
  - environment-heavy workflow may be wrong for a GeeTest-like case
  - pure image mindset may be wrong for a DataDome-like case
  - static prettification may be wrong for a Kasada-like case without request-role anchoring
