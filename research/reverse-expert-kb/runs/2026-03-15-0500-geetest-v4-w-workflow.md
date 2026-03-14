# Run Report — 2026-03-15 05:00 Asia/Shanghai

## 1. Scope this run
This run started by reading the KB root files, current browser-runtime structure, recent practical workflow notes, and the latest run reports to stay aligned with the human correction: **less empty taxonomy growth, more concrete target-grounded workflow knowledge**.

The browser subtree already had concrete notes for:
- Turnstile
- hCaptcha
- Arkose FunCaptcha
- Akamai sensor/cookie workflows
- Kasada request attachment
- PerimeterX / HUMAN collector and cookie-refresh paths
- request-finalization backtrace and parameter-path localization

A remaining practical gap was that GeeTest still existed mainly inside a broad comparison page:
- `topics/datadome-geetest-kasada-workflow-note.md`

That page was useful, but it did not give a dedicated, target-family-first cookbook for:
- GeeTest v4 widget mode and challenge timing
- `initGeetest4` / `showCaptcha()` lifecycle
- browser-side `w` packing / encryption localization
- `getValidate()` result-object boundaries
- host-page submit and backend `/validate` diagnosis

This run therefore focused on creating a **dedicated GeeTest v4 practical workflow page** and related source notes, then integrating it into the browser subtree.

Primary outputs:
- `topics/geetest-v4-w-parameter-and-validate-workflow-note.md`
- `sources/browser-runtime/2026-03-15-geetest-v4-w-parameter-and-validate-workflow-notes.md`
- navigation updates in `index.md`, `topics/browser-runtime-subtree-guide.md`, and `topics/browser-side-risk-control-and-captcha-workflows.md`

This run explicitly chose a **concrete target-family workflow note** over any new abstract anti-bot synthesis page.

## 2. New findings
- Official GeeTest v4 client docs provide a strong, concrete lifecycle map around:
  - `initGeetest4(...)`
  - widget `product` modes (`float`, `popup`, `bind`)
  - delayed challenge start through `showCaptcha()` in `bind` flows
  - `onSuccess(...)`
  - `getValidate()`
  - `reset()`
- Official GeeTest docs explicitly document the outward success/result object containing:
  - `lot_number`
  - `captcha_output`
  - `pass_token`
  - `gen_time`
- Official server docs provide a clean backend truth surface:
  - validation endpoint `gcaptcha4.geetest.com/validate`
  - server-side inputs `lot_number`, `captcha_output`, `pass_token`, `gen_time`, `captcha_id`, `sign_token`
  - failure language like `pass_token expire` and `illegal gen_time`
- GeeTest’s own client docs also emphasize that initialization timing matters because late initialization can miss behavioral data and produce invalid verification.
- Practitioner/search material consistently frames GeeTest v4 `w` as a packed/encrypted browser-side answer object.
- The practical analyst framing that emerged is:

```text
widget mode + challenge timing
  -> answer object
  -> pack/encrypt boundary (`w`)
  -> success state / `getValidate()`
  -> app submit
  -> backend `/validate`
```

- The key workflow trap is clear:
  - analysts can waste time either staring at the visible slider/challenge UI
  - or staring only at final opaque encrypted payloads
  - when the highest-leverage boundary is often **the last readable answer object before packing/encryption**, plus the later `getValidate()` / `/validate` truth surface

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/datadome-geetest-kasada-workflow-note.md`
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
- `topics/hcaptcha-callback-submit-and-siteverify-workflow-note.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- recent browser practical run reports

### External / search material
Official docs fetched:
- `https://docs.geetest.com/BehaviorVerification/apirefer/api/web`
- `https://docs.geetest.com/BehaviorVerification/deploy/client/web`
- `https://docs.geetest.com/BehaviorVerification/deploy/server`
- `https://docs.geetest.com/BehaviorVerification/apirefer/api/server`

Search-layer queries:
- `GeeTest v4 w parameter reverse engineering workflow`
- `GeeTest slide w parameter javascript analysis`
- `GeeTest v4 initGeetest4 captcha_id lot_number pass_token gen_time w workflow`
- `GeeTest v4 w parameter lot_number pass_token gen_time`

Practitioner / solver signal surfaced by search-layer:
- 2Captcha GeeTest docs
- practitioner blog posts describing `w` as a packed/encrypted answer object and focusing on the last readable object before encryption

### Source-quality judgment
- Official GeeTest docs were the strongest sources for:
  - lifecycle shape
  - documented success/result fields
  - backend validation semantics
  - reset/retry behavior
  - challenge timing assumptions
- Practitioner material was useful for:
  - consistent framing of `w` as the browser-side packed/encrypted answer object
  - reinforcing the importance of locating the pre-encryption answer object
- Public detailed internal algorithm claims remain noisy and version-sensitive.
  So the resulting page stayed conservative on invariant internals and focused on **workflow boundaries**.

## 4. Reflections / synthesis
This run stayed on the corrected direction.

The weak move would have been:
- write another broad anti-bot comparison page
- or expand GeeTest only as one bullet inside a family taxonomy

The stronger move was:
- identify a target-family gap in the browser subtree
- build a dedicated practical workflow page
- center it on the concrete handoff chain analysts actually need

The resulting GeeTest page improves the subtree because it has a distinct practical identity from nearby pages:
- Turnstile emphasizes widget lifecycle and token redemption timing
- hCaptcha emphasizes callback / hidden-field / execute-on-submit behavior
- Arkose emphasizes iframe/session/token boundaries
- Kasada emphasizes protected request-role attachment
- **GeeTest v4 now explicitly emphasizes answer-object → pack/encrypt (`w`) → `getValidate()` → `/validate` workflow**

That is a better use of effort than more abstract browser anti-bot ontology.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/geetest-v4-w-parameter-and-validate-workflow-note.md`

### Improved this run
- `index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`

### New source note added
- `sources/browser-runtime/2026-03-15-geetest-v4-w-parameter-and-validate-workflow-notes.md`

### Candidate future creation/improvement
- improve `topics/browser-cdp-and-debugger-assisted-re.md` with a compact section on locating the last readable answer object before crypto/packing boundaries in browser anti-bot families
- improve `topics/browser-parameter-path-localization-workflow-note.md` with a small subsection distinguishing “final parameter string” from “last structured preimage”
- improve `topics/browser-environment-reconstruction.md` with a short section on when initialization timing / behavioral-data capture should be treated as part of the environment contract instead of just a transport detail

## 6. Next-step research directions
1. Keep filling **missing target-family workflow pages** where the KB still has only broad family comparison notes.
2. Prefer pages that anchor on analyst leverage such as:
   - last readable structured object before packing/encryption
   - callback-to-submit handoff
   - widget mode and delayed execution edges
   - accepted-vs-rejected compare-runs at a concrete boundary
3. Continue strengthening the browser subtree as a set of real workflow archetypes rather than abstract anti-bot classes.
4. Look for similar gaps in mobile protected-runtime and mixed JS/Wasm branches where a family is mentioned broadly but lacks a concrete cookbook page.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated GeeTest v4 workflow centered on:
  - `initGeetest4` mode classification
  - `showCaptcha()` / delayed challenge-start analysis
  - localizing the last readable answer object before `w` packing/encryption
  - using `onSuccess` and `getValidate()` as outward truth surfaces
  - following the result object into app submit and backend `/validate`
- Added breakpoint/hook families for:
  - `initGeetest4(...)`
  - `captchaObj.showCaptcha()`
  - `captchaObj.onSuccess(...)`
  - `captchaObj.getValidate()`
  - pre-encryption answer-object / pack helper
  - host-page submit and backend handoff boundary
- Added explicit failure diagnosis for:
  - challenge never starting because `bind` mode delayed execution
  - analysis focusing too late on final encrypted payloads
  - challenge success not being redeemed correctly by the host page
  - delayed submit causing backend failures like expired `pass_token`
  - first run working but later runs failing due to reset/retry/state rotation

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/geetest-v4-w-parameter-and-validate-workflow-note.md`
  - `sources/browser-runtime/2026-03-15-geetest-v4-w-parameter-and-validate-workflow-notes.md`
  - navigation updates
  - this run report
- Next operational steps after writing this report:
  - commit workspace changes
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, record the failure while preserving local KB state
