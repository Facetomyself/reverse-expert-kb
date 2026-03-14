# Run Report — 2026-03-15 04:00 Asia/Shanghai

## 1. Scope this run
This run started by loading the KB root structure, recent browser practical notes, and the newest run reports to stay aligned with the human correction: **less abstract taxonomy growth, more concrete target-family and workflow material**.

The recent browser branch already had practical notes for:
- Turnstile
- Arkose FunCaptcha
- hCaptcha
- `acw_sc__v2`
- Reese84 / `___utmvc`
- ByteDance-style request-signature families
- Akamai sensor / cookie-validation workflows
- PerimeterX / HUMAN collector/cookie-refresh workflows
- request-finalization backtrace and parameter-path localization

A remaining gap was that the KB still lacked a **dedicated Kasada target-family workflow page**.
The existing `datadome-geetest-kasada-workflow-note.md` was useful as a comparison note, but not enough as a site-family-first cookbook.

This run therefore focused on a concrete page for:
- **Kasada request-role identification**
- **SDK / challenge bootstrap edges such as `p.js` / `ips.js`-style paths**
- **`X-KPSDK-*` request attachment tracing**
- **one-layer-earlier structured preimage capture**
- **challenge freshness / invisible challenge / PoW failure diagnosis**

Primary outputs:
- `topics/kasada-x-kpsdk-request-attachment-workflow-note.md`
- `sources/browser-runtime/2026-03-15-kasada-request-role-and-pow-workflow-notes.md`
- browser navigation updates in `index.md`, `topics/browser-runtime-subtree-guide.md`, and `topics/browser-side-risk-control-and-captcha-workflows.md`

This run explicitly chose a **concrete target-family workflow note** over any new broad anti-bot synthesis page.

## 2. New findings
- Kasada vendor material supports a practical analyst framing around:
  - client-side JS tag / SDK installation
  - invisible challenges rather than classic visible CAPTCHA as the dominant path
  - application/browser fingerprinting plus proof-of-work / challenge pressure
  - code virtualization / anti-reverse-engineering pressure on the client side
- Public practitioner/bypass material repeatedly surfaces browser-visible anchors strong enough for a workflow note:
  - `X-KPSDK-*` headers, especially `X-KPSDK-Ct`
  - script names such as `p.js` and `ips.js`
  - cookie names like `kas.js`, `kas_challenge`, and related `_kas*` state
- A stable practical analyst framing emerged:

```text
SDK/challenge bootstrap
  -> browser/runtime + challenge state
  -> request-role-specific `X-KPSDK-*` attachment
  -> protected request outcome
```

- The key workflow trap is clear:
  - analysts often stop at seeing one `X-KPSDK-*` header or copied cookie state
  - but the useful question is whether the **request-role-specific producer path** and **fresh challenge/bootstrap dependency** are actually understood
- This family strongly rewards:
  - request-finalization-first tracing
  - one-frame-earlier structured object capture
  - compare-runs across fresh vs stale challenge state and browser-native vs copied-header replay
- This family does **not** appear best approached as:
  - generic CAPTCHA analysis
  - whole-bundle devirtualization first
  - header copying first

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/datadome-geetest-kasada-workflow-note.md`
- `topics/reese84-and-utmvc-workflow-note.md`
- `topics/browser-parameter-path-localization-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- recent browser practical run reports

### External / search material
Search-layer queries:
- `Kasada x-kpsdk-cd x-kpsdk-ct browser workflow reverse`
- `Kasada p.js ips.js x-kpsdk browser challenge workflow`
- `Imperva Incapsula reese84___utmvc cookie bootstrap workflow`

High-signal sources used:
- `https://scrapfly.io/blog/posts/how-to-bypass-kasada-anti-scraping-waf`
- `https://scrapfly.io/bypass/kasada`
- `https://www.kasada.io/mastery-of-the-puppets-advanced-bot-detection/`
- `https://www.kasada.io/integration/`

### Source-quality judgment
- Kasada vendor material was the strongest source for:
  - integration shape
  - invisible challenge framing
  - browser inspection / proof-of-work coupling
  - client-side virtualization / anti-reverse-engineering pressure
- Public scraping/bypass material was useful for:
  - recurring browser-visible anchors like `X-KPSDK-*`, `p.js`, `ips.js`, and cookie names
  - practical workflow-shape hints
- Public field-level semantics remain noisy and version-dependent.
  So the resulting page stayed conservative on exact meaning of individual header names and focused on **workflow boundaries** instead.

## 4. Reflections / synthesis
This run stayed on the corrected direction.

The weak move would have been:
- write another broad vendor-comparison page
- or spin up a generic “invisible challenge taxonomy” note

The stronger move was:
- identify a specific missing target-family page
- anchor it around request-role tracing and one-layer-earlier state capture
- write it in a way that tells an analyst where to place breakpoints and how to diagnose stale copied-state failures

The resulting practical shape is different from nearby browser pages:
- Turnstile / hCaptcha / Arkose notes are callback / widget / iframe handoff heavy
- Akamai is sensor POST -> cookie validation -> first consumer request
- PerimeterX / HUMAN is collector -> `_px*` refresh -> challenge-success handoff -> first consumer request
- **Kasada is SDK/challenge bootstrap -> `X-KPSDK-*` request attachment -> protected request role outcome**

That distinction improves the browser subtree because it increases the ratio of **real workflow archetypes** to generic anti-bot abstraction.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/kasada-x-kpsdk-request-attachment-workflow-note.md`

### Improved this run
- `index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`

### New source note added
- `sources/browser-runtime/2026-03-15-kasada-request-role-and-pow-workflow-notes.md`

### Candidate future creation/improvement
- improve `topics/browser-environment-reconstruction.md` with a compact section on when to delay full environment rebuilding until the request-role-specific attachment helper is localized
- improve `topics/browser-debugger-detection-and-countermeasures.md` with a small section on observation pressure and timing sensitivity in invisible-challenge / pre-dispatch token-attachment families
- improve `topics/cdp-guided-token-generation-analysis.md` with a short concrete subsection on choosing the one-layer-earlier helper above `X-KPSDK-*` attachment rather than evaluating only on the final paused frame

## 6. Next-step research directions
1. Continue filling **missing concrete browser target-family notes** only where source quality is strong enough to justify breakpoint placement and compare-run advice.
2. Prefer workflow notes centered on real analyst boundaries such as:
   - request-role identification
   - one-layer-earlier structured preimage capture
   - stale-visible-state vs accepted-state diagnosis
   - challenge/bootstrap dependency mapping
3. Look for further cases where the KB still has a broad comparison page but lacks a corresponding target-family cookbook page.
4. Keep resisting the temptation to create thin anti-bot taxonomies when a better move is another grounded scenario page.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a concrete Kasada workflow centered on:
  - protected request role identification
  - SDK/challenge bootstrap boundaries
  - final `X-KPSDK-*` request-attachment tracing
  - one-layer-earlier structured preimage capture
  - accepted-vs-blocked compare-runs across fresh vs stale challenge state
- Added breakpoint/hook families for:
  - SDK/challenge script load edge
  - final request boundary
  - one-layer-earlier helper
  - challenge/state update boundary
  - first protected consumer request
- Added explicit failure diagnosis for:
  - copied `X-KPSDK-*` headers that still fail
  - challenge/bootstrap edges skipped in replay
  - devirtualization started before request role was anchored
  - same request shape with different server outcome because challenge freshness or trust state changed
  - minimal harness producing similar fields but not accepted behavior

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/kasada-x-kpsdk-request-attachment-workflow-note.md`
  - `sources/browser-runtime/2026-03-15-kasada-request-role-and-pow-workflow-notes.md`
  - browser navigation updates
  - this run report
- Next operational steps after writing this report:
  - commit workspace changes
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, record the failure while preserving local KB state
