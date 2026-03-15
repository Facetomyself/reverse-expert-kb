# Run Report — 2026-03-16 04:00 Asia/Shanghai

## 1. Scope this run
This run continued the recent correction away from abstract taxonomy and toward practical browser target-family notes.

Instead of creating a new general page, it improved an existing concrete browser workflow note:
- `topics/perimeterx-human-cookie-collector-workflow-note.md`

The practical gap was clear after reviewing the recent Reese84 / `___utmvc` work and the browser subtree guide:
- the PerimeterX / HUMAN page already had a collector/cookie framing
- but it still under-emphasized a more concrete and more analyst-useful chain:
  - HTML/bootstrap script edge
  - script-driven cookie/state creation
  - later collector/solve validation boundary
  - first behavior-changing consumer request

Files reviewed at the start of this run:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/perimeterx-human-cookie-collector-workflow-note.md`
- `sources/browser-runtime/2026-03-15-perimeterx-human-cookie-collector-notes.md`
- recent browser-oriented runs, especially the 03:00 Reese84 / `___utmvc` improvement run

## 2. New findings
The main new finding this run is that the PerimeterX / HUMAN target-family page becomes materially more useful when it explicitly separates:

```text
HTML/bootstrap script visibility
  -> script-set `_px*` state
  -> collector / solve request
  -> validated or refreshed state
  -> first accepted consumer request
```

Concrete practical findings added this run:

1. **The bootstrap script edge is a first-class analyst anchor.**
   Public practitioner material repeatedly frames the HTML-loaded script and visible app/site identifier as the earliest strong localization surface.

2. **Visible `_px*` cookies should be split into bootstrap-written versus later validated/refreshed state.**
   This is more useful than merely recording that `_px3` or `_pxvid` exists.

3. **The solve/collector request is often analytically different from the script bootstrap.**
   The page now says this more clearly, so analysts do not confuse the first visible cookie write with the later request that effectively validates or refreshes acceptance state.

4. **The page needed a stronger first-consumer framing.**
   The useful outcome is still not “I saw `_px3`.”
   It is “this later application request is the first one whose server behavior changed after the collector/solve transition.”

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/perimeterx-human-cookie-collector-workflow-note.md`
- `sources/browser-runtime/2026-03-15-perimeterx-human-cookie-collector-notes.md`
- `topics/reese84-and-utmvc-workflow-note.md`
- `topics/browser-runtime-subtree-guide.md`

### External / search material
Search-layer query batch executed this run:
- `PerimeterX human cookie collector first consumer px3 pxde reverse engineering`
- `PerimeterX collector cookie refresh first request reverse engineering`
- `Human Security PerimeterX px3 cookie collector flow reverse engineering`

Most useful surfaced sources:
- HUMAN docs — `Use of cookies & web storage`
  - <https://docs.humansecurity.com/applications/use-of-cookies-web-storage>
- HUMAN technical/deployment docs surfaced through search results for first-party route shape and collector behavior
- `Pr0t0ns/PerimeterX-Reverse`
  - <https://github.com/Pr0t0ns/PerimeterX-Reverse>
- `Pr0t0ns/PerimeterX-Solver`
  - <https://github.com/Pr0t0ns/PerimeterX-Solver>

### Source-quality judgment
- HUMAN docs remain the strongest source for cookie/storage names and deployment/route shape.
- Practitioner repos are noisy and version-specific, but still useful for workflow shape because they repeatedly expose:
  - HTML script tag / app-id discovery
  - challenge script fetch
  - visible cookie creation
  - later solve request and payload family
- A fetched antibot.blog page was not usable here because it returned only a loading shell.
- A search result pointing at a puppeteer-extra GitHub URL was noisy/misresolved and not useful for integration.

## 4. Reflections / synthesis
This run reinforces a practical KB rule:

**For browser anti-bot families, the page gets better when it names the earliest bootstrap anchor, the state-write boundary, the validation/refresh request, and the first accepted consumer — not just the cookie family.**

The weaker move would have been:
- creating another generic PerimeterX / HUMAN overview
- broadening anti-bot taxonomy again
- overcommitting to specific field semantics from noisy public repos

The stronger move was:
- improve an already-concrete target-family note
- keep claims conservative
- sharpen a real operator sequence an analyst can actually test in DevTools or a controlled browser harness

This mirrors the recent Reese84 / `___utmvc` improvement:
- there, the useful chain was bootstrap resource -> unwrap -> cookie write -> first consumer
- here, the useful chain is bootstrap script -> visible `_px*` state -> collector/solve -> first accepted consumer

That symmetry makes the browser subtree more coherent as a practical playbook.

## 5. Candidate topic pages to create or improve
### Improved this run
- `topics/perimeterx-human-cookie-collector-workflow-note.md`
- `sources/browser-runtime/2026-03-15-perimeterx-human-cookie-collector-notes.md`
- `index.md`

### Created this run
- this run report

### Candidate future creation/improvement
- improve `topics/browser-side-risk-control-and-captcha-workflows.md` with a short operator-routing section that explicitly classifies families by:
  - bootstrap anchor
  - state write
  - validation/refresh request
  - first accepted consumer
- improve `topics/cloudflare-clearance-cookie-and-js-challenge-workflow-note.md` with the same four-boundary language so browser target-family notes line up better
- improve `topics/akamai-sensor-submission-and-cookie-validation-workflow-note.md` with a clearer first-consumer emphasis parallel to the PerimeterX and Reese84 notes

## 6. Next-step research directions
1. Keep strengthening existing browser target-family notes before adding new browser taxonomy pages.
2. Look for more grounded material on:
   - PerimeterX / HUMAN challenge-success callback into host-page request issuance
   - compare-run diagnosis for stale visible cookies versus freshly validated collector state
   - first-party route variations and when apparent first-party mode still hides third-party semantics upstream
3. Continue normalizing browser pages around a shared practical chain:
   - bootstrap anchor
   - state-write boundary
   - validation/refresh boundary
   - first accepted consumer request
4. Prefer improvements with breakpoint placement and failure diagnosis over generic anti-bot summaries.

## 7. Concrete scenario notes or actionable tactics added this run
This run added several practical tactics to the PerimeterX / HUMAN note:

### New practical scenario normalized
**You can see `_px3` / `_pxvid`, and maybe even a challenge success, but you still do not know which later request actually became accepted.**

### Concrete tactics added
- inspect the HTML/bootstrap script edge before treating the collector request as the beginning of the story
- separate script-set state from later validated/refreshed state
- distinguish:
  - bootstrap script URL / app-id discovery
  - cookie/state write
  - collector/solve request
  - challenge-success callback
  - first accepted consumer request
- do not assume visible cookie presence proves success; prove which later request actually changed server behavior
- compare baseline browser runs with replayed old-cookie runs to see whether the real missing ingredient is fresh collector/solve validation rather than just cookie names

## 8. Sync / preservation status
### Local preservation
Local KB progress preserved in:
- `topics/perimeterx-human-cookie-collector-workflow-note.md`
- `sources/browser-runtime/2026-03-15-perimeterx-human-cookie-collector-notes.md`
- `index.md`
- this run report

### Git / sync actions
Planned after writing this report:
1. commit changes in `/root/.openclaw/workspace`
2. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
3. if sync fails, preserve local progress and update this report with the failure
