# Run Report — 2026-03-15 21:00 Asia/Shanghai

## 1. Scope this run
This run continued the KB’s concrete-practical pivot and deliberately avoided creating another abstract synthesis page.

The focus was a missing but recurring browser-side target pattern inside the existing practical subtree:
- Cloudflare challenge-platform / JavaScript Detections / `cf_clearance` workflows
- specifically, the analyst problem of locating the **HTML-seeding edge**, the **cookie issuance/update edge**, and the **first later protected request that actually consumes the newly seeded state**

Work performed this run:
- re-read KB structure, browser subtree guide, recent run report, and neighboring concrete browser notes
- confirmed that Turnstile was already covered, but the KB still lacked a dedicated page for non-widget Cloudflare clearance-cookie and JS-challenge workflows
- gathered a narrow official-doc source cluster around `cf_clearance`, Challenge Passage, JavaScript Detections, and Cloudflare cookie semantics
- synthesized that cluster into a new concrete workflow note and wired it into KB navigation

## 2. New findings
- The KB had a practical **Cloudflare Turnstile** note, but not a dedicated practical note for the very different and common case of:

```text
first HTML page or interstitial
  -> challenge-platform JS runs
  -> `cf_clearance` appears or refreshes
  -> later protected browser request is evaluated
```

- Official Cloudflare docs strongly support a concrete workflow-centered distinction among:
  - challenge-page/interstitial clearance issuance
  - JavaScript Detections (JSD) state seeding on HTML pages
  - Turnstile token issuance vs optional pre-clearance cookie issuance
- The strongest practical insight from the source cluster is that **many Cloudflare cases are misread because analysts start from an API/XHR request and miss the earlier HTML page that seeded the state**.
- Official JSD docs explicitly support this model:
  - JSD runs on HTML pages / page views, not AJAX calls
  - Cloudflare needs at least one HTML request before injecting JSD and issuing `cf_clearance`
  - enforcement occurs later via WAF rules using `cf.bot_management.js_detection.passed`
- Challenge Passage docs add a useful failure-diagnosis layer:
  - default lifetime ~30 minutes
  - extra allowance exists for clock skew and XmlHTTP requests
  - passage does **not** bypass rate limiting rules
- Cloudflare cookie docs help prevent over-attribution by distinguishing:
  - `cf_clearance`
  - `__cf_bm`
  - challenge-platform diagnostic cookies

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
- `topics/acw-sc-v2-cookie-bootstrap-and-consumer-path-note.md`
- `topics/datadome-cookie-challenge-workflow-note.md`
- recent run reports under `runs/`

### New source notes written this run
- `sources/browser-runtime/2026-03-15-cloudflare-clearance-cookie-and-js-challenge-workflow-notes.md`

### External sources consulted
Official Cloudflare docs:
- `https://developers.cloudflare.com/cloudflare-challenges/concepts/clearance/`
- `https://developers.cloudflare.com/cloudflare-challenges/challenge-types/challenge-pages/challenge-passage/`
- `https://developers.cloudflare.com/cloudflare-challenges/challenge-types/javascript-detections/`
- `https://developers.cloudflare.com/fundamentals/reference/policies-compliances/cloudflare-cookies/`

Search-layer was used for a narrow official-doc verification pass before extraction.

## 4. Reflections / synthesis
This run is exactly the kind of concrete improvement the user asked for.

Instead of adding more top-level ontology, it filled a recurring analyst gap with a bounded practical note:
- where challenge-platform state is first seeded
- where `cf_clearance` becomes visible
- which later request is the first meaningful consumer
- why failures are often not just “bad cookie” problems

The most important synthesis added this run is:

**Cloudflare `cf_clearance` cases are often best modeled as HTML-seeding and first-consumer-path problems, not merely cookie-capture problems.**

That shift changes the analyst’s next move:
- if they started from an API request, move outward to the HTML seed page or interstitial
- if `cf_clearance` exists but requests still fail, test expiry / direct-API blind spots / rate limiting / other cookie families instead of assuming the cookie is wrong
- if the site is using Turnstile, keep token redemption and optional pre-clearance separate rather than collapsing them into one boundary

This is a strong example of the KB moving toward **real target-solving entry surfaces** instead of taxonomy-only structure.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/cloudflare-clearance-cookie-and-js-challenge-workflow-note.md`

### Improved this run
- `topics/browser-runtime-subtree-guide.md`
- `index.md`

### Candidate future improvements
- a future browser-family contrast note comparing:
  - callback/token-redemption families
  - clearance-cookie / HTML-seeding families
  - collector/sensor/cookie-refresh families
- a compact note on how to differentiate `cf_clearance`-centered failures from `__cf_bm` / rate-limit / endpoint-class failures in the field

## 6. Next-step research directions
1. Continue filling practical browser-family gaps with pages that localize:
   - first bootstrap edge
   - outward artifact edge
   - first real consumer request
2. Good next candidates include other concrete Cloudflare-adjacent or CDN/WAF families where the outward artifact is visible but the first meaningful consumer path is under-modeled.
3. Tighten cross-links among existing browser notes so analysts can more quickly choose between:
   - token-contract problems
   - cookie-bootstrap problems
   - clearance-cookie / HTML-seeding problems
   - request-signature-family problems
4. Prefer adding compact code/hook sketches only where they improve breakpoint choice or compare-run discipline.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a new practical workflow note for **Cloudflare clearance-cookie / JS-challenge analysis**.
- Added explicit practical guidance to start from the **first HTML/interstitial seeding edge**, not blindly from the failing API request.
- Added a concrete analyst split among:
  - challenge-page/interstitial clearance
  - JavaScript Detections seeding
  - Turnstile token + optional pre-clearance
- Added breakpoint/hook anchors on:
  - `/cdn-cgi/challenge-platform/...`
  - `window.cloudflare.jsd.executeOnce(...)` when present
  - cookie-change observation
  - first later protected consumer request
- Added explicit failure diagnosis for:
  - direct-API blind spots
  - expiry / passage-window drift
  - rate limiting not covered by Challenge Passage
  - multi-cookie misclassification
  - Turnstile token-vs-pre-clearance confusion

## 8. Sync / preservation status
- Local KB changes were preserved in:
  - `topics/cloudflare-clearance-cookie-and-js-challenge-workflow-note.md`
  - `topics/browser-runtime-subtree-guide.md`
  - `index.md`
  - `sources/browser-runtime/2026-03-15-cloudflare-clearance-cookie-and-js-challenge-workflow-notes.md`
  - this run report
- Next operational steps after writing this report:
  - commit the KB changes in `/root/.openclaw/workspace`
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, preserve local state and record the failure in this report
