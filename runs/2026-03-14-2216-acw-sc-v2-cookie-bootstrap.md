# Run Report — 2026-03-14 22:16 Asia/Shanghai

## 1. Scope this run
This run continued the KB’s explicit pivot away from abstract/taxonomy-heavy expansion and toward concrete, target-grounded browser practice.

Instead of making another high-level browser synthesis page, the run focused on a practical browser target family note around **`acw_sc__v2` cookie bootstrap and consumer-path localization**.

The concrete problem chosen for this run was:
- how to analyze a browser challenge/bootstrap flow where a JS path computes or unlocks a cookie
- how to find the actual cookie write site
- how to identify the first request that truly depends on that cookie
- how to avoid stopping at “cookie visible” when the real issue is request-role, sibling fields, session drift, or observation drift

## 2. New findings
- `acw_sc__v2` is a good fit for the KB’s corrected direction because it naturally forces several concrete analyst tasks at once:
  - bootstrap response localization
  - cookie write tracing
  - first-consumer request identification
  - sibling-field verification
  - retry / reload / instrumentation differential diagnosis
- A recurring practical trap in this family is treating **cookie visibility** as equivalent to **request acceptance**.
- The highest-value artifact is usually a compact path of the form:

```text
challenge/bootstrap response
  -> local compute / wrapper logic
  -> document.cookie write
  -> first accepted consumer request
  -> sibling signed/derived fields if any
```

- Search-layer signals suggest some real-site `acw_sc__v2` cases coexist with another signed field (`Sign`), which means analysts should explicitly test whether:
  - cookie alone is sufficient
  - cookie + sibling field(s) form the actual accepted contract
- This family appears especially well-suited to a breakpoint strategy centered on:
  - bootstrap response entry
  - `document.cookie` setter path
  - request-finalization for the first accepted request
  - retry / redirect / reload transitions
- This target family also reinforces a broader KB lesson: **the first accepted consumer request matters more than the first visible artifact**.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/browser-parameter-path-localization-workflow-note.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/browser-fingerprint-and-state-dependent-token-generation.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/reese84-and-utmvc-workflow-note.md`
- `topics/datadome-geetest-kasada-workflow-note.md`
- `topics/environment-differential-diagnosis-workflow-note.md`

### Search-layer / external sources
- Search-layer local script queries:
  - `acw_sc__v2 reverse engineering cookie bootstrap`
  - `acw_sc__v2 逆向 cookie 参数 定位`
  - `acw_sc__v2 eval obfuscation hook xhr fetch`
- Search-layer returned useful orientation hits including:
  - `https://sechub.in/view/2850259`
  - `https://developer.aliyun.com/article/1597002`
  - `https://xz.aliyun.com/t/14872`
  - discussion-level anti-analysis signal around hooked XHR/fetch / Proxy / prototype traps

### Direct fetches attempted
- `https://developer.aliyun.com/article/1597002`
  - partial success: readable extraction was weak, but title-level evidence was still useful
- `https://xz.aliyun.com/t/14872`
  - fetch extraction failed
- `https://0x44.cc/reverse-engineering/2024/03/17/acunetix-waf-challenge-acw_sc__v2-part1.html`
  - returned 404 during this run

### Tooling/integration note
- Raw `web_search` (Brave) failed because Brave Search API credentials are not configured in this environment
- Logged this to `.learnings/ERRORS.md`
- Continued using the search-layer script path instead of blocking the run

### Source artifact created
- `sources/browser-runtime/2026-03-14-acw-sc-v2-cookie-bootstrap-notes.md`

## 4. Reflections / synthesis
This run was a good example of the corrected KB strategy.

A weaker version of this run would have produced another “browser anti-bot token families” synthesis page.
That would have added more taxonomy but not much analyst leverage.

The stronger move was to select a recurring, concrete family where the analyst has to solve a real operational bottleneck:
- not just identify a family name
- not just recognize that a cookie exists
- but trace bootstrap → cookie write → first accepted request → sibling fields / drift conditions

That makes this run more valuable because it helps the KB encode how analysts actually work:
- start from a specific response or request transition
- choose the strongest visible boundary
- identify the first authoritative consumer edge
- compare runs when the path drifts
- treat instrumentation effects as evidence-quality issues rather than only as target complexity

This also complements the existing browser subtree nicely:
- Turnstile / Arkose pages focus on widget/session/message/callback lifecycle
- Reese84 / ___utmvc focuses on browser-state-dependent token generation
- the new `acw_sc__v2` page adds a cookie-bootstrap and request-consumer workflow note

That is a healthier, more practical distribution of browser knowledge than continuing to expand browser abstraction layers.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/acw-sc-v2-cookie-bootstrap-and-consumer-path-note.md`

### Source note created this run
- `sources/browser-runtime/2026-03-14-acw-sc-v2-cookie-bootstrap-notes.md`

### Improved this run
- `index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-fingerprint-and-state-dependent-token-generation.md`

### Candidate future creation/improvement
- `topics/browser-cookie-bootstrap-and-challenge-retry-workflow-note.md`
- `topics/browser-first-accepted-request-localization.md`
- improve `browser-side-risk-control-and-captcha-workflows.md` with a stronger explicit section on cookie-bootstrap families
- improve `browser-cdp-and-debugger-assisted-re.md` with a “cookie setter to consumer request” breakpoint recipe

## 6. Next-step research directions
1. Continue adding **site/app/protection-family-specific** browser notes where practical workflow differs materially by target shape.
2. Deepen the browser subtree around the recurring problem: **first visible artifact vs first accepted consumer request**.
3. Add more notes where browser anti-bot analysis intersects with:
   - cookie bootstrap
   - redirect/retry loops
   - sibling signed fields
   - observation drift under instrumentation
4. If source quality improves, consider a second pass that strengthens this family note with better direct source excerpts while keeping the page workflow-centered.
5. Consider a matching note from the opposite direction:
   - start from the accepted request
   - trace backward to cookie bootstrap and challenge source

## 7. Concrete scenario notes or actionable tactics added this run
- Added a target-family workflow note centered on:
  - bootstrap response identification
  - `document.cookie` write tracing
  - first accepted consumer request localization
  - sibling sign-field verification
- Added a representative `document.cookie` interception sketch for capturing cookie-write timing and stack.
- Added a compact consumer-path template tailored to cookie bootstrap cases.
- Added explicit guidance to test:
  - cookie-only hypothesis
  - cookie + sibling field hypothesis
  - cookie + same session/navigation order hypothesis
- Added failure diagnosis for:
  - stopping at cookie visibility
  - overfocusing on static deobfuscation
  - one-off replay success followed by drift
  - instrumentation changing the observed workflow
  - apparently correct algorithm ports that still fail because the cookie was only one part of a coupled request contract

## 8. Sync / preservation status
- Local KB changes were integrated into canonical topic/source/index files.
- This run preserved provenance with a dedicated source note under `sources/browser-runtime/`.
- Next operational steps executed after file updates:
  - commit workspace changes
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
- If sync fails, local progress should still be preserved and the failure should be recorded.
