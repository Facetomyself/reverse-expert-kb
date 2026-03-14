# Akamai sensor submission / `_abck` / `bm_sz` workflow notes

Date: 2026-03-15
Topic: browser anti-bot workflow, sensor submission boundary, cookie lifecycle, practical breakpoint strategy

## Scope
These notes were gathered to decide whether the KB should add a concrete Akamai workflow page.
The goal was not to collect bypass material, but to extract a practical analyst workflow around:
- browser-side sensor script loading
- signal collection and sensor payload assembly
- sensor submission boundary
- `_abck` / `bm_sz` cookie lifecycle observations
- first accepted consumer-request tracing

## Sources consulted

### 1. `Edioff/akamai-analysis` GitHub repository
- Page: `https://github.com/Edioff/akamai-analysis`
- Raw README: `https://raw.githubusercontent.com/Edioff/akamai-analysis/main/README.md`
- Access result: success via repository page and raw README

Key extractable claims from the README:
- describes Akamai Bot Manager v2 as a large obfuscated browser-side JS sensor system
- emphasizes a pipeline of:
  - script load
  - runtime string decoding / obfuscation handling
  - browser/device/behavior signal collection
  - sensor payload generation
  - POST submission to a verification/challenge endpoint
  - server validation that sets `_abck`
  - subsequent requests carrying `_abck`
- explicitly treats `_abck` and `bm_sz` as part of a cookie-based challenge/validation workflow
- highlights timing traps, prototype checks, canvas/WebGL collection, and environment-sensitive signals

Why it is useful:
- strong practical shape for a workflow note
- enough boundary information to justify breakpoint placement and compare-run methodology
- useful because it frames the case around workflow stages, not just obfuscation internals

Limitations:
- repository README is a secondary practitioner source, not formal vendor documentation
- exact endpoint names and signal coverage may vary by target/version
- claims should be treated as target-family guidance, not universal invariants

### 2. `botswin/Akamai-Privacy-Research` GitHub repository (redirect from older repo result)
- Repository page fetched from redirect target after search result pointed to `MiddleSchoolStudent/Akamai-Reverse`
- Page: `https://github.com/botswin/Akamai-Privacy-Research`
- Raw README attempt: `https://raw.githubusercontent.com/botswin/Akamai-Privacy-Research/main/README.md`
- Access result: repository page fetch succeeded; raw README returned 404

Key extractable claims from repository page text:
- positions the repo as privacy/security research on Akamai Bot Manager behavior
- mentions deobfuscated bot-manager JS, browser automation research, fingerprinting analysis, and TLS/fingerprinting studies

Why it is useful:
- supports the idea that the Akamai family is repeatedly studied as a browser-runtime + fingerprint + automation-observation problem

Limitations:
- raw content was not fully retrievable in this run
- repository page is less specific than the Edioff case study
- should be treated as supporting signal rather than primary grounding

### 3. Stack Overflow: `_abck` / `bm_sz` purpose discussion
- URL: `https://stackoverflow.com/questions/57121107/what-is-the-purpose-of-abck-and-bm-sz`
- Access result: blocked by 403 / interstitial through `web_fetch`
- Search-layer snippet still indicated:
  - `_abck` is associated with anti-bot validation and sensor submission
  - `bm_sz` is associated with bot-detection support state

Why it is useful:
- weak but directionally consistent public corroboration that these cookie names are analyst-visible workflow anchors

Limitations:
- blocked during direct fetch this run
- snippet-level only; not trustworthy enough for detailed claims

### 4. Search-layer multi-query results
Query cluster used:
- `Akamai bot manager sensor_data _abck bm_sz reverse engineering workflow`
- `akamai _abck bm_sz sensor_data request flow breakpoint hook`
- `Akamai Bot Manager cookie lifecycle sensor_data community reverse engineering`

Useful returned results included:
- `Edioff/akamai-analysis`
- `Myronfr/akamai-v3-sensor-analysis`
- `botswin/Akamai-Privacy-Research`
- `_abck` / `bm_sz` public discussion snippet

Why it is useful:
- enough to confirm that the Akamai family is a recurring practical workflow class worth representing in the KB

Limitations:
- Brave-backed `web_search` was unavailable due to missing API key
- source quality was mixed and included noisy scraping/bypass-adjacent results, so only the strongest workflow-relevant observations were retained

## Extracted practical workflow shape
A useful family-level model from the consulted sources is:

```text
page load / protected navigation
  -> obfuscated Akamai script loads
  -> runtime decode / wrapper setup
  -> browser/device/behavior/environment signal collection
  -> sensor payload assembly
  -> POST submission to verification/challenge endpoint
  -> server returns/updates `_abck` and related cookie state
  -> later protected requests consume cookie state and may still depend on broader browser/TLS/session context
```

This is valuable because it suggests the analyst should often anchor on:
1. the sensor submission request
2. the `_abck` write/update path
3. the first consumer request whose server behavior changes materially

## Concrete analyst implications extracted this run

### 1. Treat sensor submission as the decisive browser boundary
The practical anchor is not just the existence of a large obfuscated script.
The stronger anchor is the submission edge where collected signals become one request payload.

### 2. `_abck` visibility is not equivalent to solved workflow
Seeing `_abck` in storage is only one milestone.
The KB should emphasize that analysts need to verify:
- when it was written
- what request caused the write/update
- what later request actually benefits from it
- whether sibling state and broader environment still matter

### 3. Compare-run discipline matters
The consulted material strongly suggests drift sources such as:
- instrumentation/timing changes
- browser-environment differences
- server-side validation differences despite similar visible cookies
- broader transport or TLS context not explained by client JS alone

### 4. Best breakpoint surfaces are boundary-oriented
Strong candidate breakpoint/hook families:
- script entry / wrapper init only if needed to orient
- sensor payload assembly helper
- request-finalization boundary for sensor POST
- cookie setter / cookie update path for `_abck`
- first accepted or behavior-changing consumer request after cookie update

### 5. Environment reconstruction should be bounded
These notes support a practical stance already present in the KB:
- do not rebuild the whole environment first
- first localize the exact request and state boundary that matter
- only then decide what minimum browser/runtime assumptions must be preserved

## KB decision from this source cluster
This source cluster justifies a concrete page rather than another abstract anti-bot synthesis page.
The practical missing page is best framed as:
- Akamai sensor submission and cookie-validation workflow
- centered on `_abck`, `bm_sz`, sensor POST boundary, compare-runs, and first consumer request tracing

## Evidence quality note
Evidence quality this run is:
- moderate for workflow shape
- weak-to-moderate for exact family internals across all deployments
- strong enough for a practical family workflow note if it stays conservative and boundary-oriented

The page should avoid overclaiming exact invariants and instead emphasize:
- where to look
- what to compare
- what false conclusions to avoid
