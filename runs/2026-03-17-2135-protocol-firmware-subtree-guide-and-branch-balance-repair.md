# Run Report — 2026-03-17 21:35 Asia/Shanghai — protocol/firmware subtree guide and branch-balance repair

## Summary
This autosync run chose **branch-shape repair and canonical navigation maintenance** over more source extraction.

The immediate trigger was direction review after the earlier same-day consolidation and subtree-guide passes.
By this point, the KB already had explicit subtree guides for:
- protected-runtime
- native
- runtime-evidence
- malware

The firmware/protocol branch had improved materially today through practical workflow notes, especially the new capture-failure / boundary-relocation note, but it still lacked one compact subtree guide explaining:
- where to start when a case is clearly protocol/firmware shaped
- how to distinguish boundary-selection, ingress-ownership, parser/state, acceptance-gate, output-handoff, and hardware-side consequence bottlenecks
- how the existing protocol/firmware notes ladder together in a practical operator order

Concretely, this run:
- performed direction review with branch-balance awareness
- confirmed browser/mobile remain the strongest and most crowded practical branches
- confirmed the firmware/protocol branch had enough practical leaves to justify subtree-level routing
- created a new canonical guide page: `topics/protocol-firmware-practical-subtree-guide.md`
- updated the firmware/protocol parent pages and `index.md` so the branch now reads as a routed subtree rather than a dense sibling cluster
- kept the run search-free and conservative because existing internal source pressure was already sufficient for this structural repair

## Scope this run
- perform direction review and branch-balance check
- improve the KB itself rather than only accumulating more source notes
- repair the firmware/protocol branch shape with a practical subtree guide
- update canonical navigation and branch-entry language
- produce a run report, commit KB changes if any, and run archival sync

## Branch-balance review
### Current branch picture
The KB remains strongest in:
- browser anti-bot / widget / request-signature workflows
- mobile protected-runtime / challenge-loop / hybrid ownership workflows

Recent maintenance also strengthened:
- malware practical subtree navigation
- protected-runtime practical routing
- native practical laddering
- runtime-evidence practical routing

The firmware/protocol branch was no longer weak in **leaf-note quality**.
It already had practical notes for:
- capture-failure and boundary relocation
- ingress/receive-path ownership
- parser-to-state consequence localization
- replay-precondition / state-gate localization
- reply-emission / transport handoff
- peripheral/MMIO effect proof
- ISR/deferred-worker consequence proof

Its weaker area was **branch readability**:
- no dedicated subtree guide
- no compact branch entry surface
- sequencing was present, but still too implicit across parent pages and sibling notes
- it was easier to read as a strong cluster than as one practical operator ladder

### Direction decision for this run
The right move was **not** another browser/mobile deepening pass and not another search-heavy ingest.
It was to convert the firmware/protocol branch from a strong but weakly routed cluster into a clearer practical subtree.

That means this run invested in:
- branch entry guidance
- bottleneck classification
- route-guide quality
- canonical navigation repair

rather than simply producing another isolated protocol or firmware leaf page.

### Balancing implication
This run respected branch-balance guidance because it:
- avoided adding more density to already-crowded browser/mobile micro-branches
- improved a weaker branch-level navigation surface in a high-value area
- strengthened practical KB usability rather than increasing topic count for its own sake

Future autosync runs should continue preferring:
- weaker branch-shape repair when a subtree has enough leaves but poor routing
- concrete case-driven notes only when a real operator gap remains
- conservative canonical consolidation before more taxonomy growth

Especially attractive next directions remain:
- iOS practical deepening only if a genuinely missing bottleneck appears rather than more same-branch micro-variants
- deobfuscation or malware case-driven workflow expansion where a specific operator gap still exists
- protocol/firmware child-note deepening only if repeated source pressure justifies narrower notes such as transparent-interception proof, socket-boundary overlay recovery, or manifest/key/content continuation

## Sources consulted
Canonical/navigation pages:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/topics/firmware-and-protocol-context-recovery.md`
- `research/reverse-expert-kb/topics/protocol-state-and-message-recovery.md`
- `research/reverse-expert-kb/topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md`
- `research/reverse-expert-kb/topics/protocol-ingress-ownership-and-receive-path-workflow-note.md`
- `research/reverse-expert-kb/topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `research/reverse-expert-kb/topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `research/reverse-expert-kb/topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- `research/reverse-expert-kb/topics/peripheral-mmio-effect-proof-workflow-note.md`
- `research/reverse-expert-kb/topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`

Recent run/source material used for synthesis:
- `research/reverse-expert-kb/runs/2026-03-17-1530-protocol-branch-capture-failure-and-boundary-relocation.md`
- `research/reverse-expert-kb/runs/2026-03-17-1830-native-branch-subtree-guide-and-balance-repair.md`
- `research/reverse-expert-kb/runs/2026-03-17-1930-runtime-evidence-subtree-guide-and-branch-balance-repair.md`
- `research/reverse-expert-kb/runs/2026-03-17-2035-pending-canonical-consolidation-and-branch-balance-commit.md`
- `research/reverse-expert-kb/sources/protocol-and-network-recovery/2026-03-17-sperm-protocol-network-batch-3-notes.md`

## New findings
### 1. The firmware/protocol branch’s main weakness was routing, not lack of practical leaves
The branch already had enough good practical notes to support a useful subtree.
The missing piece was a compact guide explaining:
- how to enter the branch
- how to classify the current operator bottleneck
- how the existing notes ladder together from visibility through ownership, consequence, acceptance, output, and hardware-side proof

### 2. The branch now reads better as one practical operator ladder
The strongest compact formulation after this run is:
- **see** the right boundary
- **own** the right inbound object
- **reduce** one parser/state consequence
- **accept** one interaction under the right local precondition
- **emit** one real output
- **prove** one peripheral or interrupt-side consequence

### 3. Firmware/protocol work benefits from the same subtree-guide discipline already used in other repaired branches
Recent branch-repair runs showed that a subtree guide can add more operator value than another isolated leaf note when a branch already has enough good pages.
This run confirms that pattern for firmware/protocol work.

### 4. Branch-balance repair can stay practical without creating more taxonomy
The new guide did not introduce a new abstract topic family.
Instead it clarified:
- start points
- next-step sequencing
- early-vs-late bottleneck selection
- outward routing into runtime-evidence, native, mobile, and rehosting-oriented work

## Reflections / synthesis
This was the right kind of autosync run.
It improved the KB itself instead of merely preserving another source extraction artifact.

The deeper structural takeaway is that the firmware/protocol branch now behaves more like a navigable subtree and less like a set of strong but weakly coordinated notes.
That matters because protocol/firmware cases often sit in a deceptively busy middle ground where the analyst can already see:
- some traffic or receive activity
- some parser or state hints
- some peripheral or output-side effects

but still needs a crisp answer to:
- is the current problem still boundary selection?
- is the real missing edge receive ownership rather than parser semantics?
- is replay failing because of a narrow acceptance gate rather than because the message is malformed?
- is the decisive next proof on the output side or the interrupt/deferred side?

The new subtree guide answers those questions more directly.

## Candidate topic pages to create or improve
This run created one new canonical page and suggests a few plausible nearby future improvements if later source pressure justifies them:
- `topics/protocol-firmware-practical-subtree-guide.md` ✅ created this run
- possible future nearby improvements:
  - a transparent-interception proof workflow note
  - a socket-boundary private-overlay recovery workflow note
  - a manifest/key/content continuation workflow note
  - a rehosting-readiness route guide if protocol/firmware downstream utility continues to grow as a standalone practical bottleneck

## Next-step research directions
Preferred direction after this run:
1. keep biasing autosync work toward weaker branches or weaker branch-shape surfaces rather than already-dense browser/mobile growth
2. continue preferring route-guide and workflow repair when a branch already has enough good leaf pages
3. if protocol/firmware work is chosen again soon, prefer a genuinely missing operator bottleneck rather than another sibling note without routing value
4. look for similarly clear branch-entry or laddering gaps in:
   - deobfuscation case-driven work
   - malware practical workflows
   - any branch where strong leaf notes still depend too much on adjacency rather than explicit route guidance

## Concrete scenario notes or actionable tactics added this run
This run added or clarified the following practical guidance in canonical pages:
- the firmware/protocol branch now has an explicit subtree guide for choosing whether the bottleneck is broad context framing, boundary selection, ingress ownership, parser/state consequence, acceptance gating, output handoff, or hardware-side consequence proof
- the firmware/context and protocol/state parent pages now explicitly route readers through the subtree guide before narrower workflow notes
- the index now describes the branch as a subtree guide plus recurring operator bottlenecks rather than a flat practical cluster
- the branch now reads more cleanly in a real operator order: visibility -> ownership -> consequence -> acceptance -> output -> hardware/interrupt proof

## Search audit
This run did **not** use web research.

- Search sources requested: none
- Search sources succeeded: none
- Search sources failed: none
- Exa endpoint: not used in this run (host configuration notes indicate `http://158.178.236.241:7860`)
- Tavily endpoint: not used in this run (host configuration notes indicate `http://proxy.zhangxuemin.work:9874/api`)
- Grok endpoint: not used in this run (host configuration notes indicate `http://proxy.zhangxuemin.work:8000/v1`)

## Files changed this run
- `research/reverse-expert-kb/topics/protocol-firmware-practical-subtree-guide.md`
- `research/reverse-expert-kb/topics/firmware-and-protocol-context-recovery.md`
- `research/reverse-expert-kb/topics/protocol-state-and-message-recovery.md`
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/runs/2026-03-17-2135-protocol-firmware-subtree-guide-and-branch-balance-repair.md`

## Commit / sync status
Pending at report-write time.
This run should:
- commit the reverse-KB files changed by this run
- then run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

If sync fails, local progress should still be preserved and the failure should be noted without discarding KB changes.

## Outcome
The reverse KB now has a clearer firmware/protocol practical subtree with an explicit branch entry surface, bottleneck-classification rule, and better routing into existing protocol/firmware workflow notes.
This run improved canonical navigation and branch usability rather than merely increasing topic count.
