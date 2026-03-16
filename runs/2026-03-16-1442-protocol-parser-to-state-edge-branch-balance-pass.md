# Run Report — 2026-03-16 14:42 — Protocol parser-to-state edge branch-balance pass

## 1. Scope this run
This run was an explicit autosync / branch-balance maintenance pass for `research/reverse-expert-kb/`.

The main decision was to **avoid extending the already-dense browser/WebView/mobile timing branch again**.
Recent runs had concentrated heavily on:
- browser-runtime anti-bot and captcha workflows
- hybrid WebView/native handoff timing
- page-consumer readiness and request-boundary continuation
- mobile challenge / verdict / delayed-consequence chains

So this pass deliberately rebalanced toward a weaker but high-value practical branch:
- firmware / protocol workflow guidance

The target was not another synthesis page.
It was one recurring operator bottleneck the KB still handled mostly implicitly:

```text
message family is already visible,
parser candidates are already visible,
but the first behavior-changing parser/state edge is still unclear.
```

## 2. Direction review
### Current direction check
The KB remains strongest when it behaves like an investigator playbook rather than a taxonomy garden.
That means biasing toward:
- concrete scenario notes
- compare-run discipline
- first consequence-bearing edge localization
- pages that help choose the next hook, breakpoint, or proof target

That direction is healthy in the browser/mobile subtree.
But branch balance had drifted.

### Branch-balance review
Current practical-strength picture before this pass:
- **very strong:** browser anti-bot / captcha / request-signature / WebView hybrid workflow notes
- **strong and improving:** mobile protected-runtime challenge, response-consumer, policy-mapping, and delayed-consequence notes
- **moderate synthesis but weaker practical guidance:** firmware / protocol practical workflows
- **still comparatively thinner overall branches:** deeper iOS practical reversing, desktop native practical workflows, malware practical workflows, and some deobfuscation case-driven branches

This run chose firmware/protocol because it had:
- clear existing synthesis pages
- a real missing operator note
- immediate value for branch-balance repair without needing a large new research sweep

## 3. Files reviewed
Primary files reviewed this run:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent run reports under `runs/`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/native-binary-reversing-baseline.md`
- `topics/malware-analysis-overlaps-and-analyst-goals.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/trace-guided-and-dbi-assisted-re.md`
- `sources/datasets-benchmarks/2026-03-14-firmware-protocol-context-notes.md`
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`

## 4. KB changes made
### A. Created a new firmware/protocol practical source note
Created:
- `sources/firmware-protocol/2026-03-16-protocol-parser-to-state-edge-localization-notes.md`

What it adds:
- a normalized workflow framing for the recurring case where packet families and parser candidates are already visible, but the first behavior-changing edge is still missing
- explicit separation between parser visibility and consequence visibility
- concrete localization anchors around state writes, reply-family selection, queue/timer insertion, and peripheral action

### B. Created a new practical workflow note
Created:
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`

What it adds:
- a concrete operator-facing note for firmware/protocol analysis
- compare-run discipline for narrowing to one representative pair
- four explicit boundaries:
  - message-family discriminator
  - parse boundary
  - consequence-boundary candidate
  - proof-of-effect boundary
- a strong bias toward the first consequence-bearing edge rather than broader packet labeling
- concrete scenario patterns for reply selection, deferred queue/timer work, and peripheral-action proof

### C. Strengthened the protocol topic page with a practical next move
Updated:
- `topics/protocol-state-and-message-recovery.md`

What changed:
- added explicit language that protocol work often needs parser-to-state consequence localization after message families are already known
- added the new workflow note as a plausible child-page expansion

### D. Strengthened the firmware/context page with a practical firmware-side move
Updated:
- `topics/firmware-and-protocol-context-recovery.md`

What changed:
- added the practical move of localizing the first parser-to-state or parser-to-peripheral consequence edge once one message family is isolated
- made the page more obviously routable toward concrete next actions instead of stopping at context framing alone

### E. Updated top-level navigation
Updated:
- `index.md`

What changed:
- added a dedicated firmware/protocol practical branch section
- clarified a three-step routing path:
  - environment/context recovery
  - message/state recovery
  - parser-to-state consequence localization

## 5. Why these changes matter
This run improved the KB itself instead of adding another detached note dump.

It did **not**:
- keep extending the hottest WebView micro-branch
- create another abstract firmware/protocol umbrella page
- rephrase existing synthesis without changing operator value

It **did**:
- identify a branch whose synthesis was ahead of its practical playbooks
- add one workflow note that solves a recurring “what do I do next?” gap
- tighten navigation so firmware/protocol work has a clearer practical route

The durable improvement is:

```text
firmware/protocol work in the KB now has a concrete note
for turning parser visibility into one proved state/reply/peripheral consequence edge.
```

That is more useful than another generic protocol taxonomy expansion would have been.

## 6. New findings
### A. Parser visibility is often one layer too early
A recurring analyst mistake is to treat parser identification as the end of the hard part.
This pass made explicit that the higher-value target is often the first edge that turns parsed material into:
- state transition
- reply-family selection
- deferred queue/timer work
- peripheral effect

### B. Firmware/protocol practical work benefits from the same consequence-first style already helping the mobile branch
The KB already had strong mobile notes organized around first consumer, first policy bucket, and first delayed consequence.
A similar style is also useful in firmware/protocol analysis.
The reusable pattern is:
- stop broadening observation once one good compare pair exists
- localize the first consequence-bearing edge
- prove it with one downstream effect

### C. Branch-balance repair can come from adding routing value, not only adding source volume
This run did not require a huge new source sweep.
It mainly required turning existing supported synthesis into a practical workflow note that the branch had been missing.
That is a useful autosync lesson in itself.

## 7. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- recent `runs/*.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/native-binary-reversing-baseline.md`
- `topics/malware-analysis-overlaps-and-analyst-goals.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/trace-guided-and-dbi-assisted-re.md`

### Existing source notes used this run
- `sources/datasets-benchmarks/2026-03-14-firmware-protocol-context-notes.md`
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`

### Fresh source consolidation created this run
- `sources/firmware-protocol/2026-03-16-protocol-parser-to-state-edge-localization-notes.md`

## 8. Reflections / synthesis
A strong pattern across the KB is becoming clearer:

```text
visible artifact
  -> visible parser / consumer / callback
  -> one smaller local edge actually changes later behavior
  -> prove that edge with one downstream consequence
```

The browser/mobile subtree had already started expressing this well.
This run extended that same practical philosophy into firmware/protocol work.

That is good directionally because it keeps the KB centered on:
- next trustworthy object
- next trustworthy decision
- next useful hook or breakpoint target

rather than on maximum taxonomy spread.

## 9. Candidate topic pages to create or improve
### Improved this run
- `topics/protocol-state-and-message-recovery.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `index.md`

### Created this run
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `sources/firmware-protocol/2026-03-16-protocol-parser-to-state-edge-localization-notes.md`
- this run report

### Good next improvements
- a companion note for protocol replay/mutation proof design after parser-to-state localization
- a firmware-side note for peripheral/MMIO effect proof and rehosting handoff
- a desktop-native practical note to keep branch-balance repair going beyond mobile/browser dominance
- an iOS practical workflow note if the next few runs also avoid the browser/WebView hotspot

## 10. Next-step research directions
1. Keep firmware/protocol growth practical: more small operator notes, fewer umbrella pages.
2. Add one follow-on note around protocol replay/mutation after the decisive edge is known.
3. Consider a firmware-specific note around peripheral-action proof and used-vs-unused modeling handoff.
4. Keep avoiding automatic drift back into the already-saturated WebView timing branch unless a genuinely new gap appears.
5. Continue branch-balance reviews explicitly every few runs so the KB does not keep rewarding only the easiest hot branch.

## 11. Concrete scenario notes or actionable tactics added this run
### Practical scenario normalized this run
**A message family and parser are already known, but the analysis still stalls until the first local state write, reply selector, queue/timer insertion, or peripheral action that actually predicts later behavior is proved.**

### Concrete tactics added
- freeze one representative compare-run pair before widening traffic collection
- mark four boundaries explicitly:
  - message-family discriminator
  - parse boundary
  - consequence-boundary candidate
  - proof-of-effect boundary
- prefer the first stable fan-out after parse over the deepest field semantics
- treat the first state write / reply selector / deferred queue insertion as the likely leverage point
- prove the candidate edge with one downstream emitted reply, transition, retry, or peripheral effect

## 12. Commit / archival-sync status
### KB files changed this run
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/topics/firmware-and-protocol-context-recovery.md`
- `research/reverse-expert-kb/topics/protocol-state-and-message-recovery.md`
- `research/reverse-expert-kb/topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `research/reverse-expert-kb/sources/firmware-protocol/2026-03-16-protocol-parser-to-state-edge-localization-notes.md`
- `research/reverse-expert-kb/runs/2026-03-16-1442-protocol-parser-to-state-edge-branch-balance-pass.md`

### Commit intent
Commit only the reverse-KB files touched by this run.
Do not mix in unrelated workspace or `infra/` changes.

### Sync intent
After commit, run:
- `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

If sync fails:
- preserve local KB progress
- mention the failure briefly in this run report or commit-adjacent notes
- do not roll back the KB improvement

## 13. Bottom line
This autosync run improved the reverse KB by repairing branch balance in a practical way.

The browser/WebView/mobile branch was already rich in operator notes.
The firmware/protocol branch had the synthesis but needed a stronger playbook.
This pass added a concrete workflow note that helps analysts move from parser visibility to a proved state/reply/peripheral consequence edge.
