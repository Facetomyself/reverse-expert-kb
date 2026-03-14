# Run Report — 2026-03-15 00:00 Asia/Shanghai

## 1. Scope this run
This run started by checking the current KB structure, recent concrete browser/mobile additions, and recent source notes to avoid drifting back into abstract taxonomy work.

A possible new direction around JSONP/callback-style consumer-path workflows was briefly evaluated, but the evidence quality from search this run was weak and mostly generic web-security material rather than strong reverse-engineering practitioner evidence.

So the run pivoted to a stronger, better-grounded practical gap already visible in the KB:
- several browser target-family notes existed
- several parameter-path / lifecycle notes existed
- but there was not yet a dedicated workflow page for **starting from the protected request that actually matters and backtracing from final request assembly to upstream state and producers**

The main output of this run was therefore a new concrete workflow page:
- `topics/browser-request-finalization-backtrace-workflow-note.md`

## 2. New findings
- The browser subtree had already become reasonably rich in concrete target-family notes, but it still lacked a dedicated **request-boundary-first** page.
- Existing notes repeatedly implied the same reusable analyst pattern:
  - find the one request that materially changes server behavior
  - hook the final assembly boundary
  - classify dynamic fields by role
  - backtrace only one producer layer at a time
  - capture structured preimage before opaque packing
  - compare accepted vs failed runs at the same request boundary
- This pattern is practical because it helps avoid three recurring wasteful moves:
  - over-large bundle deobfuscation before request relevance is known
  - stopping at token/cookie visibility without proving the consumer path
  - blaming “algorithm mismatch” when the real cause is stale bootstrap/session/environment state
- The attempted external search direction around JSONP/callback flows did **not** produce strong enough practitioner evidence to justify a target-specific concrete note this run.
  - Results were mostly JSONP security/XSS articles and generic callback attack material.
  - That is a useful negative finding: not every brainstormed concrete page deserves creation if its evidence base is weak.
- A better use of effort was to synthesize the stronger common workflow already supported by existing browser pages and source notes.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-parameter-path-localization-workflow-note.md`
- `topics/bytedance-web-request-signature-workflow-note.md`
- `topics/acw-sc-v2-cookie-bootstrap-and-consumer-path-note.md`
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
- `topics/mobile-signature-location-and-preimage-recovery-workflow-note.md`
- `runs/2026-03-14-2316-bytedance-web-signature-workflow.md`
- `sources/browser-runtime/2026-03-14-acw-sc-v2-cookie-bootstrap-notes.md`

### Search-layer / external search this run
Queries run:
- `jsonp callback anti bot token request path reverse engineering`
- `jsonp callback bootstrap cookie consumer path javascript protection`
- `site:github.com jsonp callback token verification browser reverse engineering`

Observed result character:
- largely generic JSONP security / XSS / CSP material
- insufficiently strong practitioner RE signal for a useful target-grounded workflow page this run

## 4. Reflections / synthesis
This run was a good example of the KB’s corrected operating mode.

The old failure mode would have been:
- produce another abstract browser methodology page
- or force a weakly grounded target-specific note just because a concrete-sounding idea appeared

This run instead did two better things:
1. rejected a weak concrete direction when the evidence quality was poor
2. created a stronger practical page that distilled a recurring method already supported by multiple existing concrete notes

That matters because the user’s correction was not “always create site-specific pages no matter what.”
It was:
- stop defaulting to abstract taxonomy
- prefer grounded, practical, code-adjacent workflows
- make pages useful for how analysts really solve targets

The new request-finalization backtrace page fits that correction well because it is:
- operational
- breakpoint-oriented
- compare-run-friendly
- cross-target reusable without becoming empty abstraction
- tightly tied to existing browser family notes

It also improves the browser subtree’s internal coherence.
Before this run, the subtree had strong pages for:
- widget lifecycle
- cookie bootstrap
- parameter-path localization
- request-signature families

What it lacked was the unifying practical move analysts often use when those pages are not enough:
- begin at the accepted/protected request itself and walk backward

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/browser-request-finalization-backtrace-workflow-note.md`

### Candidate future creation/improvement
- improve `topics/browser-runtime-subtree-guide.md` to explicitly include the new request-boundary-first entry surface
- improve `index.md` so the browser branch highlights request-boundary-first analysis as a first-class navigation path
- possible future concrete page: a stronger target-grounded note on request-finalization backtrace for one specific family only if a source cluster emerges with enough real evidence
- possible future improvement to `topics/browser-cdp-and-debugger-assisted-re.md`: add a compact “backtrace from final request” breakpoint recipe section

## 6. Next-step research directions
1. Continue looking for practical browser workflow gaps that are grounded by multiple existing target-family pages.
2. Add more cross-target-but-still-concrete cookbook pages only when they capture a real analyst move, not when they drift into generic theory.
3. Prefer new site/family-specific notes only when there is enough stable practitioner evidence to support actionable sections such as breakpoints, producer chains, failure modes, and compare-run tactics.
4. Consider a future browser page on sibling-field coupling diagnosis if enough repeated evidence accumulates across families.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a concrete browser workflow centered on:
  - choosing the one request with a behavioral boundary
  - hooking final request assembly
  - classifying dynamic fields by request/session/environment role
  - stepping backward one producer layer at a time
  - separating structured preimage from opaque final formatting
  - comparing accepted vs failed runs at the same boundary
- Added practical breakpoint families for:
  - final transport wrappers
  - serializer / request-client helpers
  - state-read boundaries
  - bootstrap / refresh edges
- Added representative recording templates for:
  - final-boundary evidence capture
  - producer mapping
  - field-family stage classification
- Added explicit failure diagnosis for:
  - `fetch` hooks that are too late
  - field-only reasoning
  - same visible token but different request outcome
  - runaway static cleanup
  - instrumentation-induced path distortion

## 8. Sync / preservation status
- Local KB progress was preserved in a new topic page and this run report.
- External search about JSONP/callback-style workflows was evaluated but not promoted into a KB topic because the evidence quality did not justify it.
- If files were modified, next operational steps are:
  - commit workspace changes
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
- If sync fails, local KB progress should still remain preserved and the failure should be noted.
