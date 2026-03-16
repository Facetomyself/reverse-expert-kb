# Run Report — 2026-03-16 22:30 — Peripheral / MMIO effect-proof branch-balance pass

## 1. Scope this run
This run was a scheduled autosync / branch-balance / maintenance pass for `research/reverse-expert-kb/`.

The key direction choice this run was to keep improving the KB itself while resisting drift back into the already-dense browser anti-bot, WebView, and generic mobile protected-runtime branches.
Recent runs had already repaired several underweighted practical branches with concrete notes:
- protocol parser -> state-edge localization
- native interface -> state proof
- malware staged execution -> consequence proof
- VM trace -> semantic anchor reduction
- flattened dispatcher -> state-edge reduction
- iOS runtime-gate diagnosis
- Unity / IL2Cpp state ownership and persistence proof
- runtime-evidence causal-write / reverse-causality localization

That still left a thinner but high-value firmware/protocol practical gap:
- **candidate peripheral/MMIO visibility exists, but the first behavior-changing hardware-side edge is still unproved**

The specific gap targeted this run was:

```text
candidate register ranges, MMIO families, parser paths,
or hardware-facing handlers are already visible,
but the investigation still stalls because the analyst has not yet proved
which write, mode-select, queue/DMA/interrupt arm,
or status-latch edge actually predicts later behavior.
```

So this run focused on adding a practical firmware/peripheral workflow note centered on effect proof, plus the supporting source note and navigation updates needed to make that branch visible.

## 2. Direction review
### Current direction check
The KB still improves most when a run gives the analyst a better next move instead of widening taxonomy.
That still means preferring:
- practical workflow notes
- one representative trigger or compare pair
- one consequence-bearing write / arm / state edge
- one downstream proof boundary
- one narrower next task

That practical style is already strong in:
- browser first-consumer and request-finalization notes
- WebView/native handoff and lifecycle notes
- mobile challenge / policy / delayed-consequence notes
- protocol parser -> state-edge localization
- native interface -> state proof
- malware staged handoff -> consequence proof
- deobfuscation trace / dispatcher reduction notes
- iOS runtime-gate diagnosis
- Unity / IL2Cpp state-ownership and persistence routing

What remained thinner was a concrete firmware-side note for the common middle state where:
- message/command families are already partly isolated
- candidate peripheral or MMIO families are already visible
- but the first effect-bearing write, arm, or status-latch still has not been proved

This run repaired that gap.

### Branch-balance review
An explicit branch-balance review was appropriate again because the KB had recently repaired several non-browser practical branches, and it was worth checking what still remained underrepresented.

Current practical branch picture before this pass looked roughly like:
- **very strong:** browser anti-bot / captcha / request-signature / hybrid WebView workflows
- **strong:** mobile protected-runtime / challenge / ownership / policy / delayed-consequence notes
- **improving:** native, protocol, malware, deobfuscation, iOS, Unity / IL2Cpp, and runtime-evidence practical branches
- **still relatively thin:** firmware/peripheral practical workflows past parser visibility and past nominal MMIO labeling

The specific imbalance visible here was:
- the firmware/protocol branch already had good parent synthesis
- it already had one parser-to-state consequence note
- but it still lacked a hardware-side sibling for the recurring case where parser or register visibility exists and the remaining bottleneck is proving the first effect-bearing peripheral edge

That made this run a good fit for branch-balance repair.
It improved a weaker practical branch without defaulting back into browser or WebView micro-variants.

## 3. Files reviewed
Primary files reviewed this run:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent `runs/*.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/native-binary-reversing-baseline.md`
- `topics/malware-analysis-overlaps-and-analyst-goals.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `sources/datasets-benchmarks/2026-03-14-firmware-protocol-context-notes.md`

## 4. KB changes made
### A. Created a new firmware/peripheral source note
Created:
- `sources/firmware-protocol/2026-03-16-peripheral-mmio-effect-proof-notes.md`

What it adds:
- a workflow-centered consolidation for the recurring firmware case where candidate MMIO ranges, register families, or hardware-facing handlers are already visible, but the first effect-bearing edge is still unclear
- explicit separation among:
  - MMIO/range visibility
  - register-role hypothesis
  - first effect-bearing write / arm / queue edge
  - later proof-of-effect boundary
- practical framing for cases where broad peripheral labeling exists but rehosting, replay, or modeling still stalls

### B. Created a new practical workflow note
Created:
- `topics/peripheral-mmio-effect-proof-workflow-note.md`

What it adds:
- a concrete operator-facing note for firmware/peripheral cases where analyst leverage is blocked one step after MMIO visibility
- explicit routing from:
  - one representative trigger or compare pair
  - one MMIO/peripheral-entry boundary
  - one effect-bearing write / mode-select / arm / status-latch edge
  - one visible downstream proof
- scenario patterns for:
  - mode-select writes that gate later reply/state behavior
  - queue / DMA / interrupt-arm boundaries as the real consequence edge
  - indirect proof via later status or reply differences when direct hardware action is noisy

### C. Strengthened the firmware/context page
Updated:
- `topics/firmware-and-protocol-context-recovery.md`

What changed:
- added explicit language that once candidate MMIO/register families are visible, the next practical move is often to localize the first effect-bearing write, arm, or status-latch edge
- added the new workflow note as a practical bridge page under suggested expansions

### D. Updated top-level navigation
Updated:
- `index.md`

What changed:
- added the new peripheral/MMIO note into the firmware / protocol practical branch list
- updated the branch framing from one recurring bottleneck to two coordinated firmware/protocol bottlenecks:
  - parser-to-state consequence localization
  - peripheral/MMIO effect proof

## 5. Why these changes matter
This run improved the KB itself rather than merely collecting another firmware source mention.

It did **not**:
- create another abstract firmware/peripheral taxonomy page
- return to browser or WebView timing variants
- stop at generic peripheral-label discussion

It **did**:
- identify a practical branch that had enough synthesis but no canonical hardware-side workflow note
- normalize the recurring operator bottleneck around effect-bearing MMIO/peripheral proof
- connect the branch cleanly to existing protocol, native, and runtime consequence-first styles

The durable improvement is:

```text
the KB now has a practical firmware/peripheral entry note for the moment when
candidate MMIO ranges, register families, or hardware-facing handlers are already visible,
but the analyst still cannot tell which write, mode-select, queue/DMA/interrupt arm,
or status-latch actually predicts later behavior.
```

That is much more useful than another broad “firmware context matters” paragraph would have been.

## 6. New findings
### A. The firmware/peripheral gap was effect proof, not visibility
The KB already had enough signal to say firmware context recovery depends on hidden mappings, used-context recovery, and downstream rehosting utility.
What it lacked was a compact operator note for the common middle state where visibility exists but the first hardware-side consequence is still ambiguous.

### B. Firmware/peripheral work fits the KB’s consequence-first style well
A now-clear cross-branch pattern is:
- native: interface -> state -> effect proof
- protocol: parser -> state consequence edge
- malware: staged handoff -> consequence proof
- runtime evidence: late effect -> causal boundary localization
- firmware/peripheral: command or parser path -> MMIO/peripheral edge -> effect proof

That coherence makes the KB more consistent and easier to navigate.

### C. Broad register labeling is often one layer too early
One valuable normalization from this run is that firmware/peripheral work should not stop at proving a register block or accessor helper.
The recurring practical leverage is often at the first narrower edge:
- mode/select write
- queue or DMA arm
- interrupt enable/ack path
- status/completion latch
- one hardware-conditioned reply difference

### D. This branch bridges protocol, rehosting, and hardware-model work cleanly
That makes it a high-value branch-balance repair:
- it grows a genuinely thinner firmware branch
- it also improves structural linkage between parser/state notes and later rehosting/modeling work

## 7. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- recent `runs/*.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/native-binary-reversing-baseline.md`
- `topics/malware-analysis-overlaps-and-analyst-goals.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`

### Existing source notes used this run
- `sources/datasets-benchmarks/2026-03-14-firmware-protocol-context-notes.md`

### Fresh source consolidation created this run
- `sources/firmware-protocol/2026-03-16-peripheral-mmio-effect-proof-notes.md`

## 8. Reflections / synthesis
A stronger KB-wide operator pattern is now visible:

```text
some useful structure is already visible
  -> freeze one representative trigger or compare pair
  -> localize one trustworthy consequence-bearing edge
  -> prove one downstream effect
  -> return to one smaller next task
```

The firmware/peripheral branch now has its own explicit version of that pattern.
That is healthy directionally because it keeps the KB centered on:
- consequence-bearing edges
- proof boundaries
- next trustworthy move
- practical handoff to the next experiment

rather than on ever-larger register maps or environment-taxonomy growth.

## 9. Candidate topic pages to create or improve
### Improved this run
- `topics/firmware-and-protocol-context-recovery.md`
- `index.md`

### Created this run
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `sources/firmware-protocol/2026-03-16-peripheral-mmio-effect-proof-notes.md`
- this run report

### Good next improvements
- a follow-on note around rehosting-model minimality once one effect-bearing peripheral edge is known
- a follow-on note around ISR/deferred-worker consequence proof if more firmware cases cluster there
- a companion note around protocol replay/mutation after both parser-to-state and peripheral effect edges are known

## 10. Next-step research directions
1. Keep the firmware/protocol branch practical with small workflow notes instead of broad hardware-taxonomy growth.
2. Watch for a good follow-on split around ISR/deferred-worker proof if more cases cluster there.
3. Watch for a good follow-on split around rehosting model minimality once one effect-bearing edge is proved.
4. Continue resisting browser/WebView overconcentration unless a clearly missing high-value practical gap appears.
5. Revisit top-level navigation after a few more branch-balance passes so the KB’s center of gravity remains honest.

## 11. Concrete scenario notes or actionable tactics added this run
### Practical scenario normalized this run
**A firmware case already exposes candidate MMIO ranges, register families, or hardware-facing handlers, but the analyst still cannot tell which write, mode-select, queue/DMA/interrupt arm, or status-latch actually controls later behavior.**

### Concrete tactics added
- do not confuse register visibility with proved effect
- freeze one representative trigger or compare pair only
- localize one MMIO/peripheral-entry boundary before broadening modeling work
- look for the first narrower effect-bearing write / arm / status-latch rather than trusting broad peripheral labels
- prove one visible status/reply/interrupt/hardware-side effect before deepening rehosting or taxonomy work

## 12. Commit / archival-sync status
### KB files changed this run
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/topics/firmware-and-protocol-context-recovery.md`
- `research/reverse-expert-kb/topics/peripheral-mmio-effect-proof-workflow-note.md`
- `research/reverse-expert-kb/sources/firmware-protocol/2026-03-16-peripheral-mmio-effect-proof-notes.md`
- `research/reverse-expert-kb/runs/2026-03-16-2230-peripheral-mmio-effect-proof-branch-balance-pass.md`

### Commit intent
Commit only the reverse-KB files touched by this run.
Do not mix in unrelated workspace or pre-existing reverse-KB changes.

### Pre-commit note
A pre-existing unrelated modification was already present in:
- `research/reverse-expert-kb/runs/2026-03-16-0300-reese84-utmvc-bootstrap-and-first-consumer.md`

That file should be intentionally left out of this run’s commit.

### Sync intent
After commit, run:
- `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

If sync fails:
- preserve local KB progress
- mention the failure briefly in this run report
- do not roll back the KB improvement

## 13. Bottom line
This autosync run improved the reverse KB by repairing another thinner practical branch: firmware/peripheral consequence proof after MMIO visibility.

The KB already knew from firmware/protocol synthesis that hidden mappings, used-context recovery, and downstream utility matter.
Now it also has a concrete workflow note for the common bottleneck where candidate peripheral/MMIO structure is already visible but the first effect-bearing hardware-side edge is still unproved, which makes the firmware/protocol branch more balanced, more navigable, and more practically useful.
