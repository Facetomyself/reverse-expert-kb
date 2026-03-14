# Run Report — 2026-03-15 07:00 Asia/Shanghai

## 1. Scope this run
This run started by reading the KB root files, current browser-runtime structure, recent practical workflow notes, and the latest browser practical runs to stay aligned with the human correction: **less empty taxonomy growth, more concrete, target-grounded, code-adjacent workflow knowledge**.

The browser subtree already had:
- family-level browser request-signature coverage
- practical notes for Akamai, Kasada, PerimeterX, DataDome, GeeTest, Turnstile, Arkose, hCaptcha, ACW-SC-V2, and broad ByteDance-style signatures

A remaining practical gap was that the KB still lacked a **site-specific practical note for Xiaohongshu / RED / XHS web signatures**, even though public practitioner material repeatedly discusses:
- `x-s`
- `x-t`
- `x-s-common`
- sibling state such as `a1`, `webid`, and `web_session`
- browser-side signer boundaries such as `window._webmsxyw`
- environment reconstruction (补环境) as part of the path

This run therefore focused on creating a **site-specific XHS workflow note** and related source notes, then integrating it into the browser subtree.

Primary outputs:
- `topics/xiaohongshu-web-signature-workflow-note.md`
- `sources/browser-runtime/2026-03-15-xiaohongshu-web-signature-workflow-notes.md`
- navigation updates in `index.md`, `topics/browser-runtime-subtree-guide.md`, and `topics/browser-side-risk-control-and-captcha-workflows.md`

This run explicitly chose a **real target/site note** over a new abstract request-signature taxonomy page.

## 2. New findings
- Public practitioner and open-source material consistently frame Xiaohongshu browser signing as a **header family**, not a single-field problem:
  - `x-s`
  - `x-t`
  - `x-s-common`
  - plus sibling cookie/session state such as `a1`, `webid`, `web_session`
- Readable practitioner material strongly suggests a high-leverage browser edge at:
  - request wrapper
  - signer call (`window._webmsxyw` or equivalent wrapped signer)
  - final header insertion into request headers
- Open-source repositories are useful not because they prove stable internals, but because they reinforce a durable workflow shape:
  - direct HTTP reuse is treated as possible only after enough browser signing/context assumptions are preserved
  - XHS signing is version-moving and maintenance-heavy, which argues for workflow-first KB pages instead of brittle algorithm snapshots
- One especially practical diagnosis pattern surfaced clearly:
  - a request can appear to “succeed” structurally while still returning no real data
  - this likely reflects a **soft-success / degraded-response** state rather than a full accept
  - therefore the analyst must distinguish:
    - hard reject / invalid signature
    - soft success / empty or degraded data
    - true accepted data-bearing response
- The resulting analyst framing is:

```text
request role
  -> request canonicalization
  -> signer boundary
  -> `x-s` / `x-t` / `x-s-common`
  -> sibling cookie/session state (`a1`, `webid`, `web_session`)
  -> reject vs soft-success vs real data
```

That framing is more actionable than treating XHS as merely another “signature algorithm” target.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/bytedance-web-request-signature-workflow-note.md`
- `topics/browser-parameter-path-localization-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `sources/browser-runtime/2026-03-14-bytedance-web-signature-family-notes.md`
- recent browser practical run reports

### External / search material
Search-layer queries:
- `Xiaohongshu x-s x-t x-s-common reverse engineering workflow`
- `小红书 x-s x-t x-s-common 逆向 分析`
- `XHS x-s x-t x-s-common request signature site specific analysis`

High-signal sources actually used:
- `https://github.com/jobsonlook/xhs-mcp`
- `https://github.com/wei168hua/xhs-xs-xt`
- `https://juejin.cn/post/7363473319247446016`
- search-layer result snippets for additional CSDN / Zhihu / Juejin practitioner posts

### Source-quality judgment
- GitHub/open-source material was the most stable readable source in this environment.
- Practitioner article material was valuable for workflow cues like `_webmsxyw`, `a1`, `web_session`, and “success-without-data” diagnosis.
- Several Chinese content hosts remained unreliable through `web_fetch` in this environment:
  - Zhihu returned 403 interstitial behavior
  - one CSDN fetch returned 521/empty
- Because of that, this run intentionally wrote a **conservative workflow-first page** rather than overclaiming version-specific implementation details.

## 4. Reflections / synthesis
This run stayed on the corrected direction.

The weak move would have been:
- expand the broad Bytedance-style signature family page again
- or create another abstract browser token/signature taxonomy page

The stronger move was:
- identify a concrete high-frequency target with enough practical signal
- write a site-specific page anchored in analyst leverage
- emphasize the real workflow boundary and diagnosis problem, not only the visible headers

The most valuable synthesis from this run is that XHS appears to demand a more explicit distinction between:
- **header correctness**
- **request-role correctness**
- **session/cookie correctness**
- **data-bearing acceptance**

That makes the page useful not just as a signature note, but as a practical diagnosis note.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/xiaohongshu-web-signature-workflow-note.md`

### Improved this run
- `index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`

### New source note added
- `sources/browser-runtime/2026-03-15-xiaohongshu-web-signature-workflow-notes.md`

### Candidate future creation/improvement
- improve `topics/browser-request-finalization-backtrace-workflow-note.md` with a compact section on distinguishing hard reject from soft-success / empty-data states
- improve `topics/browser-environment-reconstruction.md` with a short section on when environment reconstruction is really about preserving session/signing context rather than only recreating APIs
- consider a future practical page on **response-state classification** for browser anti-bot/signature targets if multiple families keep showing the same hard-reject vs soft-success pattern

## 6. Next-step research directions
1. Continue filling **site-specific browser target gaps** where the KB still has only family-level notes.
2. Prefer target notes that expose durable analyst leverage such as:
   - signer-boundary localization
   - sibling cookie/session state mapping
   - first data-bearing consumer request
   - distinguishable response states (reject / degraded / true accept)
3. Keep using conservative evidence language when public source quality is uneven.
4. Look for similar site-specific gaps in Chinese web targets where practitioner signal is strong but the KB still only has broad family pages.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated XHS workflow centered on:
  - request-role-first analysis
  - localizing the signer call boundary (`_webmsxyw` or equivalent)
  - capturing the canonical request object before signing
  - treating `x-s`, `x-t`, and `x-s-common` as a header family
  - mapping sibling state such as `a1`, `webid`, and `web_session`
  - explicitly distinguishing hard reject, soft success without data, and real accepted data
- Added breakpoint/hook families for:
  - request-finalization wrapper
  - signer boundary
  - cookie/session-state reads
  - first response classifier
  - environment-reconstruction edge
- Added explicit failure diagnosis for:
  - focusing only on `x-s`
  - misreading empty-data soft success as full success
  - assuming request roles are interchangeable
  - overgrowing environment patching before bounding the live signer path
  - letting static deobfuscation take over before the request boundary is stabilized

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/xiaohongshu-web-signature-workflow-note.md`
  - `sources/browser-runtime/2026-03-15-xiaohongshu-web-signature-workflow-notes.md`
  - browser navigation updates
  - this run report
- External source collection had partial fetch failures on some Chinese content hosts, but enough signal remained to preserve a useful conservative workflow page locally.
- Next operational steps after writing this report:
  - commit workspace changes
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, record the failure while preserving local KB state
