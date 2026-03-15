# Run Report — 2026-03-15 10:00 Asia/Shanghai

## 1. Scope this run
This run started with a full KB state check and recent-run scan:
- root docs (`README.md`, `index.md`)
- current browser-runtime subtree
- recent concrete browser workflow notes and runs
- recent browser source notes

The goal stayed aligned with the human correction:
**do not grow more empty taxonomy; add another practical, case-driven, code-adjacent workflow page.**

Given the current browser subtree, the strongest next move was not another abstract topic page. It was a concrete browser-runtime case that broadens the subtree beyond anti-bot/captcha/request-signature families while still matching the KB’s practical direction.

This run therefore focused on a **YouTube web player signature / `n`-sig / Innertube workflow note** centered on:
- exact player-version anchoring
- served-player transform-chain localization
- separating classic signature decipher from `n`-parameter throttling recovery
- distinguishing URL-field success from actually usable media delivery

## 2. New findings
- A stable public source cluster exists for a **workflow-oriented** YouTube page even if exact current low-level internals are moving targets.
- The strongest durable analyst object is:

```text
exact player JS version
  -> one concrete protected format URL
  -> transform-chain extraction boundary
  -> classic signature decipher branch
  -> `n` / `nsig` throttling branch
  -> final delivery outcome
```

- Practical maintenance evidence from live extractor ecosystems strongly supports treating **player version drift** as a first-class diagnostic fact.
- The most important methodological distinction is not “the YouTube signature algorithm,” but:
  - classic signature decipher failure
  - `n`/`nsig` throttling failure
  - earlier player-response / client-context / Innertube acquisition failure
- This makes YouTube a good fit for the KB’s practical browser playbook model: **anchor one request/URL, localize the minimal active transform chain, classify the failure correctly, and compare browser-successful vs externalized paths at the mutation boundary.**

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- recent concrete browser workflow notes for style and structure alignment

### External / search material
Search-layer queries:
- `YouTube innertube n parameter signature decipher reverse engineering workflow`
- `YouTube nsig signatureCipher player js Innertube reverse engineering`

Readable/fetched or search-derived sources used:
- `https://tyrrrz.me/blog/reverse-engineering-youtube`
- `https://tyrrrz.me/blog/reverse-engineering-youtube-revisited`
- `https://github.com/yt-dlp/yt-dlp/issues/14400`
- `https://github.com/iv-org/invidious/issues/3230`
- search-layer Grok results highlighting extractor-maintenance and player-JS transform-chain evidence

### Source-quality judgment
- The Holub writeups remain valuable as durable workflow anchors, even though extraction quality on this host was weak.
- The `yt-dlp` issue was especially useful because it anchors the practical maintenance reality: exact `base.js` player versions matter, and `nsig` drift is a recurring breakage class.
- The Invidious issue was weaker on detail but still useful as corroborating evidence that client/player drift produces downstream breakage that is easy to misclassify.
- Overall, this source cluster justified a **workflow note**, not a brittle algorithm-fact page.

## 4. Reflections / synthesis
This run stayed on the corrected path.

The weak move would have been:
- create another generic browser media/API abstraction page
- or write a high-level “reverse engineering YouTube” survey

The stronger move was:
- identify the smallest practical analyst object
- synthesize a site-specific workflow note around it
- explicitly separate the failure classes analysts keep collapsing together

The best synthesis from this run is that YouTube web should be modeled as a **served-player transform extraction problem** with at least two distinct mutation branches:
- classic signature decipher
- `n` / `nsig` throttling recovery

That makes the new page practical:
- anchor on one player version
- anchor on one protected format URL
- localize one transform chain
- compare post-decipher vs post-`n` outcomes
- classify whether the remaining drift is earlier acquisition, mutation, or final delivery

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/youtube-player-signature-and-nsig-workflow-note.md`

### Improved this run
- `index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`

### New source note added
- `sources/browser-runtime/2026-03-15-youtube-player-signature-and-nsig-workflow-notes.md`

### Candidate future creation/improvement
- improve `topics/browser-request-finalization-backtrace-workflow-note.md` with a compact subsection on URL-mutation-stage compare-runs for media/asset targets
- consider a future cross-target browser page on **soft success vs full success classification** if the pattern keeps repeating across request-signature, media, and anti-bot families
- consider a future browser workflow note on **served-script transform extraction under version churn** if more targets beyond YouTube justify it

## 6. Next-step research directions
1. Continue filling practical browser target gaps where the subtree still lacks a site-specific or family-specific workflow note.
2. Keep favoring targets where public evidence supports durable workflow guidance even if the exact implementation churns.
3. Look for repeated browser patterns that justify later cross-target synthesis pages only after enough concrete cases exist.
4. Maintain the current KB direction: diagnosis layer first, operational workflow layer second, broad abstraction only when several concrete cases have accumulated.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated YouTube web workflow centered on:
  - exact player-version anchoring
  - one-protected-URL-first analysis
  - minimal player-JS transform-chain localization
  - explicit separation of classic signature decipher from `n`-sig throttling diagnosis
  - distinguishing invalid URL, playable-but-throttled, and fully-usable outcomes
- Added concrete breakpoint/hook placement for:
  - format-URL acquisition boundary
  - player-script transform helper boundary
  - final URL mutation boundary
  - player-version comparison edge
- Added explicit failure diagnosis for:
  - “signature solved” while delivery is still throttled
  - overreacting to player updates as conceptual breakage instead of extraction-path drift
  - whole-player cleanup ballooning beyond the active transform chain
  - blaming transform logic when the true break is earlier player-response / client-context drift

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/youtube-player-signature-and-nsig-workflow-note.md`
  - `sources/browser-runtime/2026-03-15-youtube-player-signature-and-nsig-workflow-notes.md`
  - navigation updates in `index.md`, `topics/browser-runtime-subtree-guide.md`, and `topics/browser-side-risk-control-and-captcha-workflows.md`
  - this run report
- A minor tooling mismatch occurred during an exact-match Markdown edit on `index.md`; it was repaired immediately and logged in `.learnings/ERRORS.md` as a workflow gotcha.
- Next operational steps after writing this report:
  - commit workspace changes
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, preserve local state and record the failure
