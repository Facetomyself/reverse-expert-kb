# Reverse KB Autosync Run Report

Date: 2026-03-26 10:19 Asia/Shanghai / 2026-03-26 02:19 UTC
Mode: external-research-driven
Scope: `research/reverse-expert-kb/`
Primary branch worked: malware practical subtree
Chosen seam: request-builder -> committed send-boundary work where async wrapper APIs and durable transfer APIs make initiation weaker than real commitment, so the first honest analyst proof lives in callback/state progression or durable completion semantics instead of the initiating helper alone

## Summary
This run intentionally avoided another internal wording/index/family-count sync pass.

Recent malware practical work had already improved:
- Run-key / StartupApproved startup-live truth
- Scheduled Task live-scheduler / conditions / Scheduled Job truth
- service failure-action / queued-action / launch-context truth
- BITS-job persistence consumer truth
- broad async-wrapper committed-boundary guidance

The thinner, still-practical gap was narrower and comms-shaped:
- the malware send-boundary branch already said not to flatten initiation into commitment
- but it still under-preserved the specific Windows wrapper semantics that make that warning operationally honest
- especially for WinHTTP, WinINet, and BITS-shaped durable transfer cases where analysts can still overclaim from helper visibility alone

This run therefore did a real explicit multi-source external search attempt and then made canonical KB updates rather than only dropping notes:
- refined the malware request-builder -> send-boundary workflow note with sharper WinHTTP / WinINet / BITS stop rules
- synchronized the malware subtree guide and top-level index so the refinement survives as branch memory instead of living only in one leaf
- preserved the raw search artifact as the research trace for follow-on runs

## Direction review
This run stayed aligned with the KB’s intended direction:
- maintain and improve the KB itself, not just collect notes
- keep work practical and case-driven
- preserve operator stop rules rather than broad API-taxonomy text
- avoid another easy dense-branch polish loop by targeting a thinner comms seam with direct analyst value

Why this seam was worth working:
- it changes how analysts choose the first truthful proof object in wrapper-heavy malware comms cases
- it helps stop a common failure mode: treating `WinHttpSendRequest(...)`, callback installation, or visible BITS setup as equivalent to a real committed outbound effect
- it sharpens the malware branch’s handoff into protocol work by freezing a smaller honest local claim first
- it complements the existing BITS persistence work without repeating it

## Branch-balance awareness
Current balance judgment after this run:
- **still easy to overfeed:** browser/mobile anti-bot branches, broad protected-runtime wording polish, and internal synchronization passes that do not add a new operator stop rule
- **recently improved and worth preserving canonically:** malware persistence specializations, runtime-evidence compare-run truth selection, iOS callback/continuation stop rules, and protocol replay-fixture call-context truth
- **good target for this run:** malware practical workflows, specifically the thinner communications seam where async wrapper or durable transfer semantics decide what should count as committed send proof

Why this was the right maintenance move instead of another persistence leaf:
- the branch already had the right page structure
- the real gap was a still-too-weak stop rule inside an existing practical note
- parent/subtree/index synchronization around this narrower rule adds more long-term operator value than another near-duplicate communications micro-leaf

## External research performed
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries used:
1. `WinHTTP SendRequest ReceiveResponse status callback async request handle reverse engineering malware`
2. `WinINet InternetSetStatusCallback async request complete handle context reverse engineering malware`
3. `BITS SetNotifyInterface SetNotifyFlags callback delivery Complete notification ordering malware analysis`

Saved raw search artifact:
- `sources/malware/2026-03-26-async-send-boundary-search-layer.txt`

## Search audit
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- exa
- tavily
- grok

Failed sources:
- none

Source-result caveat:
- Grok was explicitly invoked and returned zero retained results in the saved artifact, but the source itself was attempted successfully
- this still counts as a real multi-source external-research run, not degraded Grok-only or KB-internal maintenance

Endpoints used on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Degraded-mode note:
- none for this run
- all three requested sources were actually attempted

## Sources used conservatively
Readable retained anchors:
- Microsoft Learn — `WinHttpSendRequest`
- Microsoft Learn — `WinHttpReceiveResponse`
- Microsoft Learn — `InternetSetStatusCallback`
- Microsoft Learn — `Registering a COM Callback`
- retained search results also surfaced `WINHTTP_STATUS_CALLBACK`, `InternetStatusCallback`, `IBackgroundCopyJob::SetNotifyInterface`, and `IBackgroundCopyJob::SetNotifyFlags` as corroborating API surfaces

Conservative source-backed cues retained:
- WinHTTP async use still distinguishes send initiation from later send-complete / request-sent and later headers-available / response truth
- WinHTTP docs explicitly tie async success/failure to later callback outcomes rather than the initiating call alone
- WinINet callback delivery depends on callback installation and callback-eligible nonzero context rather than merely using an async-capable API family
- `INTERNET_STATUS_REQUEST_COMPLETE` is the meaningful completion edge for asynchronous WinINet work; callback setup alone is weaker
- BITS callback registration and durable completion semantics make job ownership / notify-progression / final availability more truthful than immediate packet intuition
- for malware comms analysis, these API semantics justify freezing a smaller callback/state or durable completion proof object before widening into protocol narration

## KB changes made
### Canonical malware send-boundary page materially refined
Updated:
- `topics/malware-request-builder-to-send-boundary-workflow-note.md`

Material improvements:
- strengthened the async-wrapper scenario with explicit WinHTTP and WinINet truth splits
- clarified that WinHTTP `WinHttpSendRequest(...)` visibility alone is weaker than callback-confirmed send-complete / request-sent / headers-available progression
- clarified that WinINet callback installation and callback-eligible request context are weaker than actual `INTERNET_STATUS_REQUEST_COMPLETE` truth
- extended hook / breakpoint guidance so analysts can freeze one callback/status edge or one durable BITS progression edge instead of narrating broad wrapper presence
- updated the source-footprint section so the newer Windows API references survive as practical branch memory

### Malware subtree guide updated
Updated:
- `topics/malware-practical-subtree-guide.md`

Change:
- preserved the sharper Windows-wrapper stop rule at subtree level so WinHTTP, WinINet, and durable-transfer truth splits survive beyond the leaf page

### Top-level index updated
Updated:
- `index.md`

Change:
- the branch-balance summary for malware practical workflows now preserves the thinner async-wrapper send-boundary refinement as a top-level maintenance memory

## Practical operator value added
This run improved a real comms-analysis stop rule.

Before this refinement, the branch already helped analysts separate:
- request-family proof
- builder / serializer / send-boundary proof
- durable transfer ownership
- later protocol continuation

But one avoidable ambiguity remained:
- if a wrapper-heavy API family is already visible, what exactly counts as the first honest local proof that the request really committed?

After this refinement, the branch more honestly supports a smaller split:
- initiation truth
- callback-eligible context truth
- callback/state progression truth
- durable completion / final-availability truth

That changes live case handling:
- analysts are less likely to overread `WinHttpSendRequest(...)` alone as committed request proof
- WinINet-heavy cases are less likely to stop at callback installation or async-capable handles without proving request-complete delivery on the right context
- BITS-shaped cases are less likely to blur durable job ownership and final file/effect availability into one vague network story
- malware-side comms work can hand off into protocol recovery with a smaller, more truthful local ownership claim

This is practical operator value because it is:
- small enough to apply immediately in live reversing work
- source-backed enough to preserve conservatively
- thin-branch work rather than another dense-branch convenience edit

## Files changed
Added:
- `runs/2026-03-26-1019-reverse-kb-autosync.md`
- `sources/malware/2026-03-26-async-send-boundary-search-layer.txt`

Updated:
- `topics/malware-request-builder-to-send-boundary-workflow-note.md`
- `topics/malware-practical-subtree-guide.md`
- `index.md`

## Best-effort errors logging note
No `.learnings/ERRORS.md` update was necessary for the main workflow.
A small local parsing slip happened while summarizing the saved search artifact, but the search itself completed and the artifact remained usable, so this did not require durable error logging.

## Commit / sync status
Plan for this run:
1. commit the reverse-KB files changed by this workflow
2. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
3. leave this run report as the archival record

## Bottom line
This was a real external-research-driven maintenance run on a thinner malware communications seam.

The KB now preserves a sharper send-boundary stop rule:
- WinHTTP initiation is not the same as send-complete or response availability
- WinINet callback setup is not the same as callback-eligible request completion truth
- BITS durable transfer ownership is not the same as `Complete()` / final-availability truth
- and malware comms analysis should freeze one of those smaller honest proof objects before widening into broader protocol storytelling
