# Source Notes — Cloudflare clearance cookie and JS-challenge workflow boundaries

Date: 2026-03-15
Collector: OpenClaw autonomous KB maintenance run
Scope: gather concrete documentation signals that support a practical workflow note for Cloudflare `cf_clearance` / JS challenge / first-consumer-path analysis, especially around challenge passage, JavaScript Detections, pre-clearance, cookie scope, and the difference between browser-side challenge execution and later protected-request consumption.

## Sources consulted

### 1. Cloudflare Challenges — Clearance
URL: https://developers.cloudflare.com/cloudflare-challenges/concepts/clearance/
Type: official documentation
Observed via: `web_fetch`

Key usable signals:
- A `cf_clearance` cookie proves to Cloudflare that the visitor passed a presented challenge.
- The cookie is securely tied to the specific visitor and device it was issued to.
- Challenge Pages issue `cf_clearance` by default.
- Turnstile issues a one-time token by default; `cf_clearance` is optional through pre-clearance.
- Pre-clearance levels are explicit and ordered:
  - `interactive`
  - `managed`
  - `jschallenge`
  - `no_clearance`
- Turnstile pre-clearance only works when widget hostname matches the zone where WAF rules apply.
- JavaScript Detections data is stored in `cf_clearance`.
- `cf_clearance` cannot exceed 4096 bytes.

Why it matters:
- Strongly supports a workflow that treats `cf_clearance` as a **browser challenge outcome / clearance artifact**, not as a free-floating cookie to reason about in isolation.
- Gives a concrete basis for distinguishing:
  - challenge-page issued clearance
  - Turnstile token redemption
  - Turnstile pre-clearance cookie issuance
  - JavaScript Detections state stored inside the same outward cookie surface
- Reinforces that cookie presence alone is not the whole story: issuance path and clearance level matter.

Reliability note:
- Official and high-value for lifecycle semantics and cookie role.

---

### 2. Cloudflare Challenges — Challenge Passage
URL: https://developers.cloudflare.com/cloudflare-challenges/challenge-types/challenge-pages/challenge-passage/
Type: official documentation
Observed via: `web_fetch`

Key usable signals:
- After successful challenge completion, Cloudflare sets a `cf_clearance` cookie in the browser.
- Default cookie lifetime is 30 minutes; recommended range is 15–45 minutes.
- Cloudflare adds extra time for clock skew.
- For XmlHTTP requests, Cloudflare adds an extra hour to validation time to avoid breaking short-lifetime flows.
- Challenge Passage does not apply to rate-limiting rules.

Why it matters:
- Provides a concrete failure-diagnosis vocabulary for "worked once, later challenged again" cases.
- Supports compare-run analysis around:
  - first pass vs delayed retry
  - browser navigation vs later XHR/fetch consumption
  - challenge-passage lifetime vs other rejection causes
- Strongly suggests that analysts should separate:
  - cookie issuance timing
  - later request consumption timing
  - non-clearance controls such as rate limiting

Reliability note:
- Official and high-value for timing semantics.

---

### 3. Cloudflare Challenges — JavaScript Detections
URL: https://developers.cloudflare.com/cloudflare-challenges/challenge-types/javascript-detections/
Type: official documentation
Observed via: `web_fetch`

Key usable signals:
- JavaScript Detections is separate from Challenge Pages and Turnstile.
- It runs on HTML page responses/page views, not AJAX calls; API and mobile application traffic are unaffected.
- Cloudflare needs at least one HTML request before injecting JavaScript Detections and issuing the `cf_clearance` cookie.
- Snippets are served from `/cdn-cgi/challenge-platform/...`.
- Result of JSD execution is stored in `cf_clearance` and used to populate `cf.bot_management.js_detection.passed`.
- Enforcement does not happen automatically; customers must create WAF rules using `cf.bot_management.js_detection.passed`.
- Documentation explicitly warns not to evaluate this field on a visitor’s first request to a site.
- Manual API variant uses `/cdn-cgi/challenge-platform/scripts/jsd/api.js` and `window.cloudflare.jsd.executeOnce(...)`.
- JSD execution result `success`/`error` only indicates JS execution outcome, not whether the visitor is human.

Why it matters:
- This is the strongest practical source for a **first HTML request -> challenge-platform injection -> later protected-request consumption** workflow.
- It justifies a concrete analyst model:

```text
first HTML request
  -> challenge-platform JS injected or manually loaded
  -> browser executes JS detections
  -> `cf_clearance` updated with JSD state
  -> later browser-only endpoint evaluated by WAF rule
```

- It also gives a precise reason many analysts misread browser cases:
  - they inspect an API/XHR request directly,
  - but the decisive state was seeded on an earlier HTML page view.
- It provides good breakpoint/hook anchors:
  - `/cdn-cgi/challenge-platform/...`
  - `window.cloudflare.jsd.executeOnce`
  - first later protected browser request checked by WAF

Reliability note:
- Official and very high-value for workflow shape.

---

### 4. Cloudflare Fundamentals — Cloudflare Cookies
URL: https://developers.cloudflare.com/fundamentals/reference/policies-compliances/cloudflare-cookies/
Type: official documentation
Observed via: `web_fetch`

Key usable signals:
- `cf_clearance` stores proof of challenge passed and is used so Cloudflare does not issue a challenge again if present.
- The page also distinguishes `__cf_bm` as a separate bot-management cookie containing encrypted bot-score-related information.
- Sequence rules may use `__cfseq`.
- Cloudflare explicitly warns of issues with `cf_clearance` on non-HTTPS sites.
- The challenge platform also uses diagnostic cookies such as `cf_chl_rc_i`, `cf_chl_rc_ni`, and `cf_chl_rc_m` for internal issue identification.

Why it matters:
- Helps prevent analysts from collapsing all Cloudflare-visible cookies into one meaning.
- Supports a practical distinction between:
  - `cf_clearance` as challenge-passage / clearance artifact
  - `__cf_bm` as separate bot-product scoring/session state
  - internal challenge-platform diagnostic cookies that may appear but are not the analyst’s main object
- Adds a concrete environment assumption: HTTPS matters for reliable `cf_clearance` behavior.

Reliability note:
- Official and useful for outward artifact classification.

## Cross-source synthesis

### Core recurring pattern
A practical Cloudflare clearance case is often best modeled as:

```text
first HTML request or interstitial challenge page
  -> challenge-platform JS injected or page challenge executed
  -> browser obtains or refreshes `cf_clearance`
  -> later browser request is the first meaningful consumer
  -> request is accepted, challenged again, or rejected for a non-clearance reason
```

This is different from a simplistic:

```text
copy cookie -> request should work
```

model.

### Important boundary distinctions
The source cluster strongly supports keeping these boundaries separate:

1. **Challenge execution boundary**
   - where Cloudflare injects or serves challenge-platform JS
   - where an interstitial or JSD path actually runs in the browser

2. **Cookie issuance/update boundary**
   - where `cf_clearance` first appears or refreshes
   - whether it reflects challenge-page clearance, JSD state, or Turnstile pre-clearance

3. **First meaningful consumer boundary**
   - the later browser request whose WAF treatment changes because the state now exists
   - often not the first request overall, and often not an API-first entrypoint

4. **Non-clearance rejection boundary**
   - cases where `cf_clearance` exists but later failure is actually due to rate limiting, wrong endpoint class, missing HTML seeding step, hostname mismatch, or other bot/trust logic

### Practical implication for analysts
A strong first-pass workflow should answer:
- which HTML response or interstitial first loads `/cdn-cgi/challenge-platform/...`?
- when does `cf_clearance` first appear or change?
- is this a challenge-page case, JSD case, or Turnstile pre-clearance case?
- which later browser request is the first one whose server treatment changes?
- if the request still fails, is the problem missing HTML seeding, clearance expiry, wrong hostname/zone, rate limiting, or another cookie family like `__cf_bm` rather than `cf_clearance` itself?

### Reusable KB insight
This Cloudflare cluster is a good complement to existing browser notes:
- Turnstile note: widget lifecycle / token redemption / optional pre-clearance
- reCAPTCHA / hCaptcha notes: callback and submit boundaries
- DataDome / Akamai / PerimeterX notes: sensor/cookie/collector and later consumer request
- Cloudflare clearance note: **HTML-seeded challenge state -> `cf_clearance` -> first later protected consumer**

That makes it worth a dedicated concrete note rather than burying it inside a broader browser anti-bot overview.

## Candidate KB actions justified by this source cluster
- Create a concrete browser workflow note for Cloudflare JS challenge / `cf_clearance` / first-consumer-path analysis.
- Emphasize breakpoints and hooks on:
  - `/cdn-cgi/challenge-platform/...`
  - `window.cloudflare.jsd.executeOnce(...)` when present
  - cookie-write / cookie-change observation
  - first later protected browser request
- Add failure diagnosis for:
  - API/XHR-first analysis that missed the required HTML seeding request
  - `cf_clearance` present but failure caused by rate limiting or other control layers
  - expired or passage-window drift
  - Turnstile token vs pre-clearance confusion
  - hostname/zone mismatch in pre-clearance deployments

## Evidence limitations
- The strongest evidence here is official lifecycle and product documentation, not target-by-target public reverse-engineering writeups.
- The docs describe observable boundaries and configuration semantics more strongly than undocumented internal challenge code.
- That is acceptable for a workflow note focused on analyst entry surfaces, handoff boundaries, and failure diagnosis rather than undocumented invariants.
