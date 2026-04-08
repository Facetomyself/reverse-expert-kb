# CDP interception / visible postData vs body-owner truth notes

Date: 2026-04-08
Branch target: browser runtime / request-boundary practical workflows
Purpose: preserve a source-backed practical refinement for browser/CDP cases where DevTools or automation tooling can pause, continue, inspect, or even modify requests, but the analyst still has not proved who owned the last meaningful body preimage.

## Research intent
Tighten an existing browser request-boundary workflow note around a narrower practical liar:
- interception success
- visible request body/postData
- continued or modified request surface
- last meaningful body-preimage owner

The goal is not a general CDP/network page.
The goal is a reusable stop rule for browser request-finalization work.

## Search artifact
Raw multi-source search artifact:
- `sources/browser/2026-04-08-1456-cdp-body-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Exa returned usable Chrome DevTools Protocol and interception-support surfaces
- Tavily returned usable Chrome DevTools Protocol `Fetch` / `Network` documentation surfaces
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` through the configured proxy path

## Retained sources
1. Chrome DevTools Protocol `Fetch` domain documentation
   - request pausing/interception
   - continue / fulfill / fail control surfaces
   - request-stage and response-stage distinctions
2. Chrome DevTools Protocol `Network` domain documentation
   - request objects / postData retrieval surfaces
3. Puppeteer-level interception surfaces and issue/discussion material
   - request interception / override visibility
   - practical reports where postData/body override behavior was the focus

## High-signal retained findings

### 1. CDP Fetch proves interception control, not original producer ownership
The official `Fetch` domain already separates:
- request paused/intercepted
- client continues/fails/fulfills the request
- request-stage vs response-stage control

Practical consequence:
- a paused or continued request is a real boundary success
- it is still weaker than proving which earlier helper/store/producer fixed the body semantics that mattered

### 2. Network postData visibility proves body bytes, not body-preimage ownership
The official `Network` domain already exposes request/body visibility surfaces.

Practical consequence:
- seeing postData is useful request-boundary truth
- it still does not identify the last meaningful producer of the structured body or preimage that later became those bytes

### 3. Tooling-level request modification can create real-but-wrong ownership stories
Puppeteer/CDP interception surfaces can visibly modify headers or body material.

Practical consequence:
- successful interception or override is not automatically proof that the interception layer is the original owner of the request body that mattered
- the interception layer may be later than the last meaningful producer, and may only wrap, forward, or replace bytes after the real semantic object was already fixed upstream

## Practical synthesis worth preserving canonically
A compact stop-rule ladder for this seam is:

```text
request seen in DevTools/CDP
  != request paused/continued/modified via interception
  != visible body/postData bytes
  != last meaningful body-preimage owner
```

This keeps four different wins separate:
1. **request visibility**
   - the interesting request is now observable
2. **interception-surface truth**
   - the request can be paused / continued / modified at a CDP or automation layer
3. **body-byte truth**
   - body/postData content is visible at the network surface
4. **body-preimage owner truth**
   - one serializer/helper/store/producer is frozen as the owner of the last meaningful semantics before packing/encoding/wrapping

## Best KB use of this material
This material is best used to sharpen the existing browser request-finalization backtrace workflow note.
It should not become a broad CDP/network taxonomy page.

The operator-facing value is:
- do not overclaim from interception success alone
- do not overclaim from visible postData/body bytes alone
- step one layer earlier when the remaining real question is body-preimage ownership
- keep request-boundary truth and producer-ownership truth separate

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source result set.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked; its failure is recorded clearly.
