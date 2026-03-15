# Run Report — 2026-03-15 09:00 Asia/Shanghai

## 1. Scope this run
This run began with a full KB state check:
- root docs (`README.md`, `index.md`)
- current browser-runtime subtree
- recent practical browser runs
- recent browser source notes

The goal was to continue the corrected direction from the human: **less empty taxonomy growth, more concrete, practical, target-grounded workflow material**.

The browser subtree was already strong on:
- family-level request-signature practice
- captcha/session/cookie/token workflow notes
- request-boundary and parameter-path localization
- concrete notes for XHS, Kasada, Akamai, PerimeterX, DataDome, GeeTest, Turnstile, Arkose, hCaptcha, and related families

A remaining high-value gap was a dedicated **TikTok web** workflow note.
The KB had a broad ByteDance-style family page, but no site-specific TikTok page focused on:
- `X-Bogus`
- `msToken`
- final request-boundary tracing
- structured preimage capture
- empty/degraded response diagnosis versus true acceptance

This run therefore focused on creating a practical TikTok web signature workflow page, adding supporting source notes, and integrating it into navigation.

## 2. New findings
- A usable TikTok web source cluster exists even in this environment if handled conservatively:
  - one older but high-signal practical article (`nullpt.rs`) that anchors on a concrete request and call stack
  - implementation-facing GitHub repos that expose representative signer input shapes and field-family thinking
  - one more overview-style article that is weaker on rigor but still useful directionally
- The most durable practical lesson is not “how `X-Bogus` works internally” but:

```text
protected request role
  -> final request wrapper / `fetch` boundary
  -> immediate signer producer
  -> canonical query/body/UA/timestamp/session inputs
  -> `X-Bogus` + sibling fields
  -> accepted vs empty/degraded response
```

- `msToken` repeatedly appears as a first-class companion state element rather than disposable noise.
- TikTok is another good example of why the KB should distinguish:
  - visible signature generation
  - request/session-context correctness
  - true accepted data-bearing success
  - soft failure / empty-body or degraded response
- The source cluster also reinforces a workflow preference already emerging across the KB:
  - **request-boundary-first and preimage-first** analysis beats whole-bundle deobfuscation as the default first move.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/bytedance-web-request-signature-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/xiaohongshu-web-signature-workflow-note.md`
- `sources/browser-runtime/2026-03-14-bytedance-web-signature-family-notes.md`

### External / search material
Search-layer query:
- `TikTok X-Bogus msToken reverse engineering workflow`

Readable/fetched sources used:
- `https://nullpt.rs/reverse-engineering-tiktok-vm-1`
- `https://github.com/justscrapeme/tiktok-web-reverse-engineering`
- `https://github.com/tikvues/tiktok-api`
- `https://www.xugj520.cn/en/archives/tiktok-vm-reverse-engineering-webmssdk.html`

### Source-quality judgment
- `nullpt.rs` was the strongest practical workflow source because it anchors on a concrete request and call stack.
- GitHub repositories were useful as implementation-shape evidence, especially for signer input/preimage structure, but not treated as proof of current live internals.
- The xugj article was treated cautiously because it mixes useful workflow cues with claims that are too brittle to promote directly into the KB as hard facts.

## 4. Reflections / synthesis
This run stayed aligned with the human correction.

The weak move would have been:
- expanding another broad ByteDance-family abstraction
- or adding another browser taxonomy page

The stronger move was:
- identify a practical target gap still missing from the subtree
- use conservative source synthesis
- write a site-specific workflow note with breakpoints, hook surfaces, preimage model, and failure diagnosis

The best synthesis from this run is that TikTok web is not merely a “find `X-Bogus`” problem.
It is a request-contract problem where the analyst should explicitly model:
- request role
- canonicalized request inputs
- immediate signer boundary
- `msToken` and sibling state
- accepted vs empty/degraded outcome classes

That makes the new page more operational than a raw algorithm note.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/tiktok-web-signature-workflow-note.md`

### Improved this run
- `index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`

### New source note added
- `sources/browser-runtime/2026-03-15-tiktok-web-signature-workflow-notes.md`

### Candidate future creation/improvement
- improve `topics/browser-request-finalization-backtrace-workflow-note.md` with a compact subsection on empty-body / degraded-success diagnosis
- improve `topics/browser-environment-reconstruction.md` with a note on when browser trust/session state matters more than pure API patch coverage
- consider a future practical page on **response-state classification** across browser anti-bot targets if this pattern keeps repeating

## 6. Next-step research directions
1. Continue filling **site-specific browser gaps** where only family-level notes exist.
2. Prefer practical targets where public evidence still supports durable workflow notes even if exact internals churn.
3. Keep biasing the browser subtree toward:
   - first protected request role
   - attachment boundary
   - structured preimage
   - sibling state mapping
   - failure-mode diagnosis
4. Watch for repeated patterns that justify a cross-target page on:
   - empty/degraded-success classification
   - request acceptance versus signature correctness

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated TikTok web workflow centered on:
  - request-role-first analysis
  - monkey-patched `fetch` / final request wrapper as first anchor
  - immediate signer-producer tracing rather than whole-VM cleanup as the first move
  - structured preimage capture (query/body/UA/timestamp/session)
  - explicit `msToken` / sibling-state modeling
  - distinguishing hard reject, empty/degraded response, and true accepted data
- Added concrete breakpoint/hook placement for:
  - final request wrapper
  - canonicalization helper
  - immediate signer producer
  - `msToken` / session-state read boundary
  - environment-reconstruction edge
- Added explicit failure diagnosis for:
  - field-only thinking around `X-Bogus`
  - confusing visible signature generation with real request acceptance
  - overgrowing VM cleanup before stabilizing the request boundary
  - letting environment patching sprawl before measuring actual required reads

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/tiktok-web-signature-workflow-note.md`
  - `sources/browser-runtime/2026-03-15-tiktok-web-signature-workflow-notes.md`
  - navigation updates in `index.md`, `topics/browser-runtime-subtree-guide.md`, and `topics/browser-side-risk-control-and-captcha-workflows.md`
  - this run report
- Next operational steps after writing this report:
  - commit workspace changes
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, record the failure while preserving local KB state
