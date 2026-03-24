# Reverse KB Autosync Run Report — 2026-03-24 10:16 Asia/Shanghai

Mode: external-research-driven

## Summary
This run avoided another internal-only canonical sync and instead targeted a thinner, still-practical malware branch seam: **Windows service persistence where the real durable owner is not yet known to be a normal `ServiceMain` chain**.

The resulting KB improvement was a new concrete workflow note for distinguishing four narrower service-persistence contract shapes:
- valid service contract
- `svchost` / `ServiceDll` contract
- SCM timeout-abuse launcher contract
- failure-action / restart-owned contract

This materially improves branch balance because the malware subtree already had stronger practical continuations for Scheduled Tasks, WMI, COM/CLSID, and broad service ownership, but not yet a dedicated leaf for **timeout-abuse and failure-policy-owned persistence**.

## Direction review
Recent autosync runs were already doing real external passes, so the anti-stagnation problem was not “no search at all.”
The more useful drift to avoid on this run was **easy branch polishing** or another wording/index-only sync on denser branches.

Branch-balance judgment for this run:
- firmware/protocol and protected-runtime already had multiple recent practical source-backed continuations
- malware had practical continuation growth, but the service branch still had a thinner underfed seam around **restart/failure semantics and SCM timeout abuse**
- this seam is practical and operator-facing, not taxonomy-only

Chosen seam:
- malware service persistence
- narrower question: when broad service involvement is already known, how does the analyst distinguish **real service ownership** from **brief SCM launch abuse** or **failure-action-driven relaunch/command execution**?

## Work completed
### New KB leaf
Created:
- `topics/malware-service-failure-action-and-timeout-abuse-workflow-note.md`

This page focuses on a practical analyst decision:
- whether the durable persistence chain is owned by
  - valid `ServiceMain` semantics,
  - `svchost`/`ServiceDll` hosting,
  - a short startup window before SCM timeout,
  - or service failure actions / restart policy.

### Source note archive
Created:
- `sources/malware/2026-03-24-service-failure-action-and-timeout-abuse-notes.md`
- `sources/malware/2026-03-24-service-persistence-seams-search-layer.txt`

### Routing / branch-balance updates
Updated:
- `topics/malware-persistence-consumer-localization-workflow-note.md`
  - now routes to the new leaf when the broad persistence family is already narrowed to Windows services but the unresolved issue is the narrower contract shape
- `topics/malware-service-servicemain-consumer-proof-workflow-note.md`
  - now explicitly hands off edge-case contract-shape work to the new leaf instead of trying to absorb all service cases
- `topics/malware-practical-subtree-guide.md`
  - added the new leaf to the malware practical branch and ladder
  - updated the “specialize” step so service-specific practical work now includes contract-shape reduction
- `index.md`
  - added the new leaf to the malware branch listing

## Why this was a worthwhile KB improvement
This run maintained and improved the KB itself rather than only collecting notes because it added a new operator-facing continuation page that changes analyst stopping rules.

Before this run, the service branch could still collapse into broad statements like:
- “the sample installs a service”
- “there is a `ServiceMain`”
- “`svchost` loads a DLL”

After this run, the KB now preserves a more truthful practical split:
- valid long-lived service contract
- `svchost`/`ServiceDll` contract
- non-service executable timeout abuse
- failure-action/restart-owned persistence

That is a better practical ladder for specimen-local reversing.

## Search audit
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- exa
- tavily

Failed sources:
- grok
  - actual failure observed during explicit invocation: `502 Server Error: Bad Gateway for url: http://proxy.zhangxuemin.work:8000/v1/chat/completions`

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Degraded-source-set note:
- this run **did** perform a real explicit multi-source search attempt with `--source exa,tavily,grok`
- execution was degraded in practice to **Exa + Tavily** because Grok failed with repeated 502 responses
- because Exa and Tavily returned enough practical material, the run continued conservatively and recorded the degradation here

## External research used
Primary source-backed anchors used for the new leaf:
- Microsoft Learn service entry-point semantics
- Microsoft Learn `ServiceMain` semantics
- Unit 42 write-up on abusing SCM for non-service applications
- `svchost` / `ServiceDll` practical lab material
- additional failure-action / recovery-action references surfaced through the explicit search-layer pass

Conservative synthesis retained in the KB:
- ordinary service liveness semantics are proof boundaries, not boilerplate
- SCM timeout abuse is a distinct persistence contract shape
- `svchost`/`ServiceDll` hosting should be modeled as its own contract, not folded into generic service wording
- failure actions / restart policy can be behavior-bearing persistence objects, not just detection trivia

## Files changed
- `index.md`
- `topics/malware-persistence-consumer-localization-workflow-note.md`
- `topics/malware-practical-subtree-guide.md`
- `topics/malware-service-servicemain-consumer-proof-workflow-note.md`
- `topics/malware-service-failure-action-and-timeout-abuse-workflow-note.md`
- `sources/malware/2026-03-24-service-failure-action-and-timeout-abuse-notes.md`
- `sources/malware/2026-03-24-service-persistence-seams-search-layer.txt`

## Commit / sync status
Planned after report write:
- commit KB changes if diff is non-empty
- run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

## Bottom line
This was a real external-research-driven run on an underfed practical malware seam.
It produced a new concrete continuation page and updated branch routing so the malware subtree is less likely to flatten service persistence into generic `ServiceMain` narration.
