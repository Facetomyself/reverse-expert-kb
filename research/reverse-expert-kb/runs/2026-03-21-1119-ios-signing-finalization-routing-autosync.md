# Reverse Expert KB Autosync Run Report

Date: 2026-03-21 11:19 Asia/Shanghai
Mode: external-research-driven
Area: iOS practical branch
Focus: request-signing finalization / preimage-routing continuation after owner plausibility

## Summary
This run intentionally avoided another KB-internal canonical-sync-only pass.
Recent autosync history still leaned heavily toward internal synchronization, family-count cleanup, and parent-page wording maintenance, with only limited fresh external work.
Per the anti-stagnation rule, this run performed a real multi-source external search pass and used it to strengthen a thinner practical gap inside the iOS branch.

The chosen gap was the underdescribed step between:
- broad iOS owner localization / Chomper-style black-box invocation, and
- the more generic mobile signature/preimage-recovery workflow.

The work product was a new iOS-specific continuation note for deciding whether the cheapest next move is:
- one last iOS request-finalization boundary,
- one hop earlier into preimage/state capture,
- or stopping at one truthful in-app black-box path and routing onward.

## Direction review
Recent maintenance risk:
- too many recent runs leaned toward internal sync/index/family-shape maintenance
- browser/mobile protected-runtime branches are easier to overfeed, but this run still found a genuinely under-described iOS practical seam rather than polishing the dense parts again
- the existing iOS branch was already mature on topology, environment normalization, setup/gates, trust, owner proof, black-box replay, runtime-table repair, and callback consequence, but still thin on one request-signing continuation between owner plausibility and generic preimage reduction

Direction decision for this run:
- keep the run external-research-driven
- strengthen a real operator gap instead of another wording-only pass
- make the addition practical and case-driven rather than broad mobile-signing taxonomy

## Branch-balance review
Branch-balance judgment at start of run:
- browser/mobile/protected-runtime remain strong and easy to over-service
- protocol/firmware and malware each already received recent source-backed growth today
- the iOS subtree was not empty, but still had one practical continuity gap between owner plausibility and generic preimage work

Branch-balance action taken:
- added a narrow iOS-specific continuation note instead of another broad mobile page
- updated the iOS subtree guide, the mobile-signing parent page, the mobile runtime parent page, and the top-level index so the branch remembers the new rung canonically
- kept the work focused on operator routing rather than dense-branch polish

## External research performed
Queries used:
- `iOS app request signing Frida Chomper workflow`
- `iOS reverse engineering signature generation Frida replay request signing`
- `iOS SDK signing owner localization token generation reverse engineering`

Search intent/mode:
- deep exploratory multi-source pass

Retained external signals:
- `frida-ios-dump-requests` reinforced the practical value of anchoring one final emitted request shape and late request-construction boundary before assuming standalone signer extraction is necessary
- Frida iOS interception/documentation surfaces reinforced that useful request-signing evidence often remains at ObjC / Swift / Foundation request-construction layers, not only inside low-level crypto helpers
- the Kanxue Chomper case and prior internal iOS Chomper notes reinforced that black-box invocation is a useful continuation once an owner path is plausible, but does not by itself answer whether the next reduction should be finalization proof, earlier preimage capture, or stopping at one truthful in-app request path
- practitioner material around app-side signing / JWT secret recovery reinforced a conservative rule: many hard cases are dominated by upstream state, canonicalization, or secret/input recovery rather than by identifying the final hash primitive alone

Conservative synthesis applied:
- did not claim one universal iOS signing workflow
- did not treat request-dump visibility as proof of true owner localization
- did not assume near-correct outputs imply the wrong algorithm rather than missing init/state/finalization context
- kept the new note scoped to one iOS-specific decision boundary between owner plausibility and generic preimage work

## KB changes made
Added:
- `topics/ios-request-signing-finalization-and-preimage-routing-workflow-note.md`
- `sources/ios-runtime-and-sign-recovery/2026-03-21-ios-signing-finalization-and-preimage-routing-notes.md`
- `runs/2026-03-21-1119-ios-signing-finalization-routing-autosync.md`

Updated:
- `topics/ios-practical-subtree-guide.md`
- `topics/mobile-signing-and-parameter-generation-workflows.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `index.md`

## Practical value added
New iOS ladder step added:
- after one owner path is already plausible, decide whether the cheapest next move is:
  - prove one last iOS request-finalization boundary,
  - move one hop earlier into preimage/state capture,
  - or preserve one truthful black-box request path and route onward

This materially improves the branch because it prevents two common waste patterns:
- overextending broad replay/harness work after one truthful in-app path already exists
- flattening an iOS-shaped request-signing case into generic mobile preimage recovery before the last request-builder / canonicalization boundary has been proved

## Concrete scenario notes or actionable tactics added this run
- preserve one decisive request family only; do not widen to many request roles before the routing choice is settled
- find the last iOS-shaped boundary where request semantics are still human-readable: request builder, body canonicalizer, header merge, `NSMutableURLRequest` mutation, or native-helper entry with structured arguments
- use one near-identical compare pair to distinguish wrapper/finalization drift from upstream preimage/state drift
- treat a truthful in-app request path as a legitimate stopping point when the real next bottleneck is runtime-table/init repair or callback consequence, not signer extraction itself

## Sources consulted
Primary retained sources:
- `https://github.com/alza54/frida-ios-dump-requests`
- `https://github.com/httptoolkit/frida-interception-and-unpinning`
- `https://frida.re/docs/ios/`
- `https://bbs.kanxue.com/thread-285666.htm`
- `https://github.com/luoyanbei/reserveSignatureOfOneApp`
- `https://www.mustafadur.com/blog/reverse-ios/`
- `https://www.reddit.com/r/AskReverseEngineering/comments/1gdbrx1/use_frida_to_retrieve_apps_secret_to_sign_jwts/`
- prior internal notes under `sources/ios-runtime-and-sign-recovery/`

## Reflections / synthesis
This was a good anti-stagnation run because it used external search to justify a narrow practical addition instead of growing another dense generic subtree.
The new note is intentionally small and routing-oriented.
It should help future runs resist two bad habits:
- using “signing” as a flattening label for several different iOS continuation problems
- assuming every owner-plausible case needs either more replay scaffolding or immediate full preimage reduction

## Candidate topic pages to create or improve
If future iOS request-signing runs accumulate enough concrete source weight, useful continuations would be:
- a narrower iOS request-builder canonicalization note
- a Foundation / `NSMutableURLRequest` late-attachment diagnostic note
- an iOS session-seed / keychain-backed input provenance note

These should only be added if source-backed case pressure appears; the branch does not need speculative micro-pages yet.

## Next-step research directions
- look for a future source-backed run on one thinner practical branch outside mobile/browser unless a fresh iOS/operator gap becomes obvious again
- if more iOS signing material accumulates, prefer one concrete case-driven continuation page over broad mobile-signing wording changes
- keep watching for whether the new iOS signing-routing note reduces repeated wording drift across iOS and mobile-signing parent pages

## Search audit
Search sources requested:
- exa
- tavily
- grok

Search sources succeeded:
- exa
- tavily
- grok

Search sources failed:
- none observed in the search pass
- note: the local helper `scripts/reverse-kb-search-audit.py` initially errored when called with an unsupported `--print-endpoints` flag, but the real multi-source search pass itself succeeded and a machine-readable audit was then saved successfully

Exa endpoint:
- `http://158.178.236.241:7860`

Tavily endpoint:
- `http://proxy.zhangxuemin.work:9874/api`

Grok endpoint:
- `http://proxy.zhangxuemin.work:8000/v1`
