# Cloudflare Clearance Cookie and JS-Challenge Workflow Note

Topic class: concrete target-family workflow note
Ontology layers: browser-runtime subdomain, challenge-state workflow, cookie/bootstrap consumer-path analysis
Maturity: structured-practical
Related pages:
- topics/browser-side-risk-control-and-captcha-workflows.md
- topics/browser-fingerprint-and-state-dependent-token-generation.md
- topics/browser-request-finalization-backtrace-workflow-note.md
- topics/browser-environment-reconstruction.md
- topics/environment-differential-diagnosis-workflow-note.md
- topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md
- topics/recaptcha-v3-and-invisible-workflow-note.md
- topics/datadome-cookie-challenge-workflow-note.md

## 1. Why this page exists
This page exists because the KB already had a concrete Turnstile page, but it still lacked a dedicated note for a different and very common Cloudflare practical scenario:
- first HTML request or interstitial challenge page
- challenge-platform JavaScript runs
- `cf_clearance` is issued or refreshed
- a later browser request is the first meaningful consumer

That case is easy to misread in practice.
Analysts often do one of two unhelpful things:
- treat the case as only “copy the `cf_clearance` cookie”
- start from an API/XHR endpoint and miss that the decisive state was seeded on an earlier HTML page view

The more useful analyst object is broader:

```text
HTML or challenge-page entry
  -> challenge-platform JS runs
  -> `cf_clearance` appears or changes
  -> later protected browser request is evaluated
  -> request is accepted, challenged again, or rejected for some other reason
```

This page is therefore a concrete workflow note about **clearance-state seeding and first-consumer-path localization**, not a generic Cloudflare taxonomy page.

## 2. Target pattern / scenario
A representative Cloudflare clearance case looks like:

```text
first HTML page view or interstitial challenge
  -> `/cdn-cgi/challenge-platform/...` JS is injected or loaded
  -> browser executes challenge / JavaScript Detections
  -> `cf_clearance` cookie is created or refreshed
  -> later browser request reaches a WAF-protected path
  -> request is accepted, challenged, or still rejected
```

Common variants:
- classic challenge page / interstitial
- JavaScript Detections (JSD) seeded from a normal HTML page
- Turnstile with optional pre-clearance enabled
- higher-clearance challenge replacing an earlier lower-clearance cookie

Common analyst situations:
- an API request keeps failing even though `cf_clearance` is visible
- replaying a request with copied cookies works once, then fails later
- the analyst never sees meaningful challenge traffic because they started from XHR/fetch rather than the HTML page that seeded state
- a Turnstile deployment is mistaken for a pure `cf_clearance` case even though token redemption and pre-clearance are separate boundaries
- multiple Cloudflare-visible cookies exist and the analyst over-attributes everything to `cf_clearance`

## 3. Analyst goal
The goal is not just “obtain a cookie string.”
The goal is to recover the full state-seeding and consumer path:

```text
HTML/challenge entry
  -> challenge-platform execution
  -> `cf_clearance` issuance/update
  -> first behavior-changing protected request
  -> whether later failures are due to expiry, missing HTML seeding, rate limiting, or another trust layer
```

A useful output from this workflow looks like:

```text
first HTML GET /account injects `/cdn-cgi/challenge-platform/...`
  -> JS executes successfully
  -> `cf_clearance` appears
  -> later POST /api/profile is first WAF-checked consumer
  -> delayed replay fails after passage window, while same-session browser navigation works
```

That artifact is much more useful than “the cookie exists.”

## 4. The first five questions to answer
Before deep source browsing or static cleanup, answer these:

1. **Which HTML response or interstitial first loads `/cdn-cgi/challenge-platform/...` or otherwise seeds Cloudflare challenge state?**
2. **When does `cf_clearance` first appear or refresh?**
3. **Is this mainly a challenge-page case, a JavaScript Detections case, or a Turnstile pre-clearance case?**
4. **Which later browser request is the first meaningful consumer whose treatment changes?**
5. **If failure remains, is it really a clearance problem, or is it rate limiting, endpoint class mismatch, wrong hostname/zone, expiry, or another cookie/trust family?**

Those questions usually create more leverage than trying to reason from the final rejected request alone.

## 5. Concrete workflow

### Step 1: anchor the first HTML or interstitial state-seeding edge
Do not start from the failing API call unless you already know the browser state path.
Start from the first browser page view that could seed challenge state.

High-yield clues:
- HTML response that injects `/cdn-cgi/challenge-platform/...`
- visible interstitial challenge page
- manual JSD injection via `/cdn-cgi/challenge-platform/scripts/jsd/api.js`
- Cloudflare Turnstile page where pre-clearance may also be enabled

Why this matters:
- official docs explicitly state JavaScript Detections requires at least one HTML request before the browser receives and executes the injected challenge code
- API/mobile traffic is unaffected by JSD injection itself
- this means an analyst who starts at XHR/fetch can completely miss the decisive earlier boundary

Useful run sketch:

```text
run A:
  GET /dashboard (HTML)
  -> challenge-platform script injected
  -> `cf_clearance` appears
  -> later GET /api/me succeeds

run B:
  direct request to /api/me without visiting HTML page first
  -> no new state seeding
  -> request challenged or denied
```

### Step 2: classify which Cloudflare path you are actually in
Do not collapse all Cloudflare cases together.
At least distinguish:
- **Challenge page / interstitial**: challenge directly issues `cf_clearance`
- **JavaScript Detections**: HTML page injects JS, result stored in `cf_clearance`, later WAF rule checks `cf.bot_management.js_detection.passed`
- **Turnstile pre-clearance**: widget still issues a token by default; `cf_clearance` is optional extra state when pre-clearance is enabled

Why this matters:
- the breakpoint locations and failure diagnoses differ
- Turnstile token redemption is not the same thing as JSD/browser challenge state
- `cf_clearance` may reflect different issuance paths and clearance levels

### Step 3: anchor the cookie issuance or refresh boundary
Once the seeding edge is known, localize when outward cookie state changes.

What to record:
- request/response that immediately precedes cookie appearance
- whether `cf_clearance` is newly created or replaced
- whether challenge level appears to have changed (for example, lower-clearance state replaced by higher-clearance state)
- whether the browser also carries other Cloudflare cookies such as `__cf_bm`

Why this matters:
- cookie presence is an outward truth surface
- but the exact **issuance/update edge** tells you which branch of the workflow you are actually observing
- replacement events matter because higher-security challenge outcomes can overwrite earlier lower-level clearance

### Step 4: identify the first meaningful consumer request
The first request after cookie appearance is not always the one that matters.
Find the first request whose server treatment materially changes because state now exists.

Record:
- endpoint and method
- browser navigation, fetch/XHR, or form submit class
- accepted vs challenged vs blocked outcome
- whether success depends on same-page/session timing rather than merely visible cookie presence

Representative artifact:

```text
seed edge: GET /login HTML -> challenge platform injects
state edge: `cf_clearance` refreshed
first consumer: POST /api/session/bootstrap
effect: accepted only after HTML seed + fresh cookie, not by copied old cookie alone
```

### Step 5: compare first-pass vs replay / delay / endpoint-shape variants
At minimum compare:
- seeded HTML path vs direct API path
- immediate protected request vs delayed protected request
- same-session navigation vs copied-cookie replay
- browser endpoint vs mobile/API-like endpoint

Why this matters:
- Challenge Passage has timing semantics
- JSD specifically depends on browser HTML seeding
- some failures that look like “bad cookie” are actually caused by endpoint class mismatch or other controls such as rate limiting

### Step 6: separate clearance problems from non-clearance problems
If `cf_clearance` exists but the target still fails, explicitly test these competing hypotheses:
- **expiry / passage-window drift**
- **missing or wrong HTML seeding step**
- **wrong hostname / zone in pre-clearance scenarios**
- **rate limiting**, which Challenge Passage does not bypass
- **other Cloudflare state**, such as `__cf_bm`, being the more relevant outward artifact
- **request-family mismatch**, where a browser-cleared path is being confused with a non-browser/mobile/API surface

This prevents overfitting everything to one cookie.

## 6. Where to place breakpoints / hooks

### A. `/cdn-cgi/challenge-platform/...` injection/load boundary
Use when:
- you need the earliest reliable Cloudflare-specific code edge
- you suspect the decisive state is seeded on an HTML page rather than at the later API request

Inspect:
- which HTML page loaded it
- whether it is injected automatically or included explicitly
- whether execution happens on the first page load or only on selected pages

### B. `window.cloudflare.jsd.executeOnce(...)` when present
Use when:
- documentation or page inspection suggests manual/selective JSD deployment
- you want to confirm that the page is intentionally running JSD on a chosen HTML page

Inspect:
- callback timing
- execution success/error
- whether cookie state changes after execution

Representative sketch:
```javascript
// sketch only
if (window.cloudflare?.jsd?.executeOnce) {
  const orig = window.cloudflare.jsd.executeOnce;
  window.cloudflare.jsd.executeOnce = function(opts) {
    console.log('jsd.executeOnce', opts);
    debugger;
    return orig.apply(this, arguments);
  };
}
```

### C. Cookie-change observation around `cf_clearance`
Use when:
- you know challenge-platform JS ran, but need the exact outward state edge
- you need to compare issuance vs refresh vs replacement

Inspect:
- exact timing of `cf_clearance` appearance/change
- whether `__cf_bm` or diagnostic challenge cookies are also changing
- whether the page must remain on the same session/navigation path for the update to matter

### D. First consumer request boundary
Use when:
- `cf_clearance` is already visible
- the main unknown is which later request actually proves the state mattered

Inspect:
- whether the request is browser HTML/navigation, XHR/fetch, or form-submit driven
- whether acceptance differs between fresh seeded runs and copied-cookie replay
- whether rate limiting or another control layer still blocks the request

## 7. Representative code / pseudocode / harness fragments

### Challenge-state run log template
```text
seed page:
  GET /account
  challenge-platform loaded: yes

state update:
  cf_clearance: absent -> present
  other cookies: __cf_bm present

first consumer:
  POST /api/bootstrap
  outcome: accepted in seeded run, challenged in direct-API run

compare note:
  delayed replay after 40 min fails
  immediate same-session browser path works
```

### Cookie observation sketch
```javascript
// sketch only
const poll = setInterval(() => {
  const cookies = document.cookie;
  if (cookies.includes('cf_clearance=')) {
    console.log('cf_clearance visible', cookies);
  }
}, 500);
```

### Minimal thought model
```text
browser HTML entry
  -> challenge-platform execution
  -> clearance state visible
  -> first browser consumer request
  -> accepted / challenged / blocked-for-other-reason
```

The point is not to port Cloudflare internals.
The point is to localize the state-seeding edge and the first request that proves the state mattered.

## 8. Likely failure modes

### Failure mode 1: analyst starts from the API request and misses the decisive earlier page view
Likely cause:
- JSD or challenge state was seeded on a prior HTML response
- no meaningful browser seeding happened on the API path itself

Next move:
- move outward to the first HTML or interstitial page and identify where challenge-platform code runs

### Failure mode 2: `cf_clearance` is visible, but the request still fails
Likely causes:
- the request is outside the path/class that the cleared browser session actually unlocks
- cookie expired or passage window drifted
- rate limiting still applies
- another Cloudflare state family matters too

Next move:
- compare first consumer requests across fresh-seeded, delayed, and copied-cookie runs
- explicitly test non-clearance hypotheses

### Failure mode 3: copied cookie replay works once, then later fails
Likely causes:
- Challenge Passage timing / expiry
- state tied to the original browser/device/session context
- later rejection is not a pure clearance issue

Next move:
- compare immediate same-session consumption against delayed replay
- record first divergence point rather than only final failure

### Failure mode 4: Turnstile case is misread as only a `cf_clearance` case
Likely causes:
- analyst collapsed token redemption and optional pre-clearance into one boundary

Next move:
- separate:
  - widget token issuance and Siteverify redemption
  - optional pre-clearance cookie issuance
  - later WAF bypass semantics

### Failure mode 5: analyst over-attributes all Cloudflare cookies to one meaning
Likely causes:
- `cf_clearance`, `__cf_bm`, and diagnostic challenge cookies were not separated

Next move:
- classify outward artifacts first and keep `cf_clearance` reasoning narrow and explicit

## 9. Environment assumptions
This family strongly depends on preserving:
- a browser HTML page view when the site expects one
- realistic challenge-platform JS execution
- correct hostname/zone relationships in pre-clearance setups
- HTTPS for reliable `cf_clearance` behavior
- enough session continuity for the later browser request to consume the newly seeded state

Unlike some heavier token families, the first major win often comes from **correctly mapping HTML seeding and consumer timing**, not from deep deobfuscation.

## 10. What to verify next
Once the first-pass map exists, verify:
- whether the site uses challenge page, JSD, or Turnstile pre-clearance
- whether cookie issuance happens on initial HTML view, explicit challenge, or widget success
- whether the first meaningful consumer is navigation, form submission, or fetch/XHR
- whether delayed or replayed requests fail first because of expiry, endpoint mismatch, or non-clearance controls
- whether a browser-only path is being confused with a mobile/API path the docs explicitly exclude from JSD seeding

## 11. What this page adds to the KB
This page adds a concrete Cloudflare workflow the browser subtree was missing:
- first HTML/interstitial seeding edge
- challenge-platform execution boundary
- `cf_clearance` issuance/update edge
- first later consumer request localization
- explicit failure diagnosis for expiry, direct-API blind spots, rate limiting, Turnstile/pre-clearance confusion, and multi-cookie misclassification

That is exactly the kind of practical, target-grounded note the KB needs more of.

## 12. Source footprint / evidence note
Grounding for this page comes mainly from:
- `sources/browser-runtime/2026-03-15-cloudflare-clearance-cookie-and-js-challenge-workflow-notes.md`
- official Cloudflare docs on:
  - Clearance / `cf_clearance`
  - Challenge Passage
  - JavaScript Detections
  - Cloudflare cookie semantics
- the existing Turnstile workflow note, used only as a neighboring contrast page for token-vs-clearance boundary separation

This page intentionally stays workflow-centered and conservative.
It focuses on observable boundaries, outward artifacts, and failure diagnosis rather than undocumented challenge internals.

## 13. Topic summary
Cloudflare clearance-cookie analysis is often best approached as a **browser state-seeding and first-consumer-path problem**:

```text
HTML or interstitial entry
  -> challenge-platform JS runs
  -> `cf_clearance` appears or refreshes
  -> later protected browser request is evaluated
```

It matters because many analysts stop at “the cookie exists,” when the more useful answer is: this was the first HTML seed page, this was the challenge-platform boundary, this is when clearance state became visible, this later request was the first real consumer, and this is where expiry or another non-clearance control started to matter.
