# Run Report — 2026-03-14 23:16 Asia/Shanghai

## 1. Scope this run
This run continued the KB’s corrected direction by choosing a **concrete browser request-signature family workflow** instead of creating another abstract browser synthesis page.

The practical gap selected this run was:
- browser requests carrying families like `X-Bogus`, `_signature`, `msToken`, `a_bogus`, and adjacent site-specific families such as Xiaohongshu `x-s` / `x-t` / `x-s-common`
- the recurring analyst need to recover **request attachment path + structured preimage + sibling field family**, not just the name of one signature field

The run therefore focused on a practical workflow note for **Bytedance-style web request-signature analysis**.

## 2. New findings
- This family is a strong fit for the KB’s concrete-first correction because it repeatedly forces analysts to solve practical bottlenecks:
  - find the exact request role
  - find the field insertion site
  - capture the immediate producer
  - recover structured preimage inputs
  - compare named field vs sibling field-family requirements
  - explain replay drift across cookie/session/environment changes
- A recurring practical trap is **field-only thinking**:
  - analysts stop at `X-Bogus` or `x-s`
  - but acceptance often depends on a **coupled field family** and browser/cookie state, not one isolated output
- Search-layer results showed a stable practitioner cluster around:
  - `X-Bogus`
  - `_signature`
  - `msToken`
  - `verifyFp` / `fp`
  - `ttwid` / `webid`
  - `x-s` / `x-t` / `x-s-common`
- The most actionable workflow pattern emerging from the source cluster was:

```text
protected request
  -> field insertion site
  -> immediate producer
  -> structured preimage / sibling state family
  -> compare-run drift across retries and environments
```

- This family also reinforces a broader browser-side KB lesson:
  - request-boundary-first analysis often beats starting with broad JSVMP cleanup
  - the field insertion site is frequently a better first foothold than the deepest transform function

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/browser-fingerprint-and-state-dependent-token-generation.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-parameter-path-localization-workflow-note.md`
- `topics/acw-sc-v2-cookie-bootstrap-and-consumer-path-note.md`
- `topics/environment-differential-diagnosis-workflow-note.md`
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`

### Search-layer / external source cluster
Queries run:
- `x-bogus msToken _signature reverse engineering parameter path`
- `小红书 x-s x-t 参数 逆向 附着 路径`
- `x-gorgon browser parameter localization anti bot web`

Representative results used:
- `https://github.com/justbeluga/tiktok-web-reverse-engineering`
- `https://github.com/tikvues/tiktok-api`
- `https://github.com/iamatef/xbogus`
- `https://github.com/wei168hua/xhs-xs-xt`
- `https://github.com/jobsonlook/xhs-mcp`
- `https://github.com/Cloxl/xhshow`
- `https://blog.csdn.net/u013444182/article/details/134933150`
- `https://blog.csdn.net/qiulin_wu/article/details/138661790`
- `http://www.tpcf.cn/web/10583.shtml`
- `https://blog.csdn.net/weixin_44697518/article/details/138369646`
- `https://blog.csdn.net/asknh/article/details/146225305`

### Source artifact created
- `sources/browser-runtime/2026-03-14-bytedance-web-signature-family-notes.md`

## 4. Reflections / synthesis
This run was valuable mainly because it resisted the temptation to write a generic “browser signature systems” page.

That weaker page would likely have repeated known abstractions:
- browser tokens exist
- browser state matters
- obfuscation exists
- environment reconstruction matters

Instead, the new workflow note focuses on how analysts actually approach these targets in practice:
- choose one request that truly matters
- localize the final insertion boundary first
- distinguish insertion, formatting, transform, and preimage stages
- capture field-family inputs rather than only the final output string
- compare baseline browser behavior against altered replay conditions

That makes the new page a better fit for the user’s correction because it is:
- request-adjacent
- code-adjacent
- breakpointable
- failure-diagnosable
- reusable across a recurring real target family

This run also improved the browser subtree’s internal balance.
The browser branch already had:
- widget/session/callback/iframe workflow pages
- cookie bootstrap practice
- token-generation and environment pages

What it still lacked was a practical note for **browser request-signature families** where the core challenge is not the widget lifecycle or cookie bootstrap path, but the **final signed-field insertion + sibling-state contract**.

The new page fills that gap.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/bytedance-web-request-signature-workflow-note.md`

### Source note created this run
- `sources/browser-runtime/2026-03-14-bytedance-web-signature-family-notes.md`

### Improved this run
- `index.md`
- `topics/browser-runtime-subtree-guide.md`

### Candidate future creation/improvement
- `topics/browser-request-family-coupling-and-sibling-field-diagnosis.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/xhs-xs-xt-request-family-workflow-note.md`
- improve `browser-fingerprint-and-state-dependent-token-generation.md` with a stronger explicit section on field-family coupling and insertion-boundary-first analysis
- improve `browser-cdp-and-debugger-assisted-re.md` with a “signed request family” breakpoint recipe

## 6. Next-step research directions
1. Continue adding browser notes where the central task is **request-family recovery**, not just artifact naming.
2. Add more site/family-specific notes when they materially differ in workflow shape, especially around:
   - coupled query/header families
   - cookie + query hybrid contracts
   - environment-sensitive request wrappers
3. Consider a companion note that starts from the opposite direction:
   - first accepted request
   - backward trace to field family and state reads
4. Deepen the browser subtree around a recurring practical question:
   - when a replay reproduces the named field but still fails, which sibling state families should be checked first?

## 7. Concrete scenario notes or actionable tactics added this run
- Added a workflow note centered on:
  - request-role-first analysis
  - final insertion-boundary localization
  - structured preimage capture
  - field-family rather than field-only reasoning
- Added breakpoint suggestions for:
  - request-finalization wrappers
  - serializer / canonicalization helpers
  - cookie/state read boundaries
  - immediate producers of named fields
  - environment reconstruction edges
- Added a practical preimage thought model covering:
  - request context
  - state context
  - runtime context
- Added failure diagnosis for:
  - field-only thinking
  - over-focusing on JSVMP wrappers too early
  - reproducing the field but missing sibling state
  - unconstrained environment patching
  - retry-driven drift mistaken for algorithm drift

## 8. Sync / preservation status
- Local KB changes were integrated into canonical topic/source/index files.
- This run preserved provenance with a dedicated source note under `sources/browser-runtime/`.
- Next operational steps after file updates:
  - commit workspace changes
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
- If sync fails, local progress should still be preserved and the failure recorded locally.
