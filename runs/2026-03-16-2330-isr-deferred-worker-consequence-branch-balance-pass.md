# Run Report — 2026-03-16 23:30 — ISR / deferred-worker consequence branch-balance pass

## 1. Scope this run
This run was a scheduled autosync / branch-balance / maintenance pass for `research/reverse-expert-kb/`.

The key direction choice this run was to keep improving the KB itself while resisting drift back into the already-dense browser anti-bot, WebView, and generic mobile protected-runtime branches.
Recent runs had already repaired a long list of thinner practical branches:
- protocol parser -> state-edge localization
- native interface -> state proof
- malware staged execution -> consequence proof
- VM trace -> semantic anchor reduction
- flattened dispatcher -> state-edge reduction
- iOS runtime-gate diagnosis
- runtime-evidence causal-write / reverse-causality localization
- Unity / IL2Cpp state ownership and persistence proof
- peripheral/MMIO effect proof

That still left a useful firmware/protocol follow-on gap:
- **the first visible MMIO/peripheral effect is sometimes not yet the most useful proof boundary because the real durable consequence only appears at an ISR, completion, bottom-half, or deferred-worker handoff**

The specific gap targeted this run was:

```text
trigger and MMIO/peripheral visibility may already exist,
possibly even one candidate effect-bearing write,
but the investigation still stalls because
no one has yet proved which ISR, completion callback,
tasklet, workqueue, or deferred handler
turns that earlier hardware-facing edge into
the first durable state, reply, scheduler, or policy consequence.
```

So this run focused on adding a practical firmware follow-on workflow note centered on ISR/deferred-worker consequence proof, plus the supporting source note and navigation updates needed to make that sub-branch visible.

## 2. Direction review
### Current direction check
The KB still improves most when a run gives the analyst a better next move instead of widening taxonomy.
That still means preferring:
- practical workflow notes
- one representative trigger or compare pair
- one causally useful handoff boundary
- one durable state/reply/scheduler effect
- one smaller next task

That practical style is already strong in:
- browser first-consumer and request-finalization notes
- WebView/native handoff and lifecycle notes
- mobile challenge / policy / delayed-consequence notes
- native interface -> state proof
- protocol parser -> state consequence routing
- deobfuscation trace / dispatcher reduction notes
- malware staged handoff -> consequence proof
- iOS runtime-gate diagnosis
- Unity / IL2Cpp ownership / persistence routing
- runtime-evidence late-effect -> causal-boundary routing
- firmware peripheral/MMIO effect proof

What remained thinner was a firmware follow-on note for the common middle state where:
- parser or trigger visibility exists
- peripheral/MMIO effect visibility may also exist
- but the first durable consequence still hides later inside interrupt/completion/deferred work handling

This run repaired that gap.

### Branch-balance review
An explicit branch-balance review was appropriate again because this was the sixth-plus repair in a row aimed at underweighted practical branches, and it was worth checking whether the KB was now only adding isolated siblings or building coherent branch depth.

Current practical branch picture before this pass looked roughly like:
- **very strong:** browser anti-bot / captcha / request-signature / hybrid WebView workflows
- **strong:** mobile protected-runtime / challenge / ownership / policy / delayed-consequence notes
- **improving:** native, protocol, malware, deobfuscation, iOS, Unity / IL2Cpp, runtime-evidence, and firmware/peripheral practical branches
- **still relatively thin inside firmware/protocol:** interrupt-driven / deferred-completion consequence routing after MMIO visibility

The specific imbalance visible here was:
- the firmware/protocol branch already had good parent synthesis
- it already had a parser-to-state note
- it had just gained a peripheral/MMIO effect-proof note
- but it still lacked a canonical practical note for the recurring case where the first visible write is not the decisive proof target because the real leverage point is later, at ISR/deferred-worker consequence handoff

That made this run a good fit for branch-balance repair.
It deepened a weaker firmware branch without defaulting back into browser or WebView micro-variants.

## 3. Files reviewed
Primary files reviewed this run:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent `runs/*.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/runtime-behavior-recovery.md`
- `topics/native-interface-to-state-proof-workflow-note.md`
- `sources/firmware-protocol/2026-03-16-peripheral-mmio-effect-proof-notes.md`

## 4. KB changes made
### A. Created a new firmware source note
Created:
- `sources/firmware-protocol/2026-03-16-isr-deferred-worker-consequence-proof-notes.md`

What it adds:
- a workflow-centered consolidation for the recurring firmware case where command families, MMIO/register paths, or peripheral-facing helpers are already visible, but the first decisive behavior change only becomes clear at an ISR, completion, bottom-half, or deferred-worker boundary
- explicit separation among:
  - trigger visibility
  - MMIO/peripheral effect candidate
  - interrupt/ack/arm boundary
  - ISR/deferred-worker consequence boundary
  - later proof-of-effect boundary
- practical framing for cases where visible writes exist but the real durable reduction happens later in completion or deferred handling

### B. Created a new practical workflow note
Created:
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`

What it adds:
- a concrete operator-facing note for firmware cases where the obvious MMIO write is not yet the best proof boundary
- explicit routing from:
  - one representative trigger or compare pair
  - one peripheral-effect boundary
  - one interrupt/deferred handoff boundary
  - one durable state/reply/scheduler reduction
  - one visible downstream proof
- scenario patterns for:
  - visible writes whose real consequence appears only when one ISR consumes completion/status material
  - deferred workers that are the true reply-selector or policy-reduction boundary
  - rehosting drift caused by under-modeled completion/interrupt/deferred logic rather than register-map ignorance

### C. Strengthened the firmware/context page
Updated:
- `topics/firmware-and-protocol-context-recovery.md`

What changed:
- expanded the practical-bridge section from one firmware/peripheral workflow note to two coordinated firmware follow-on notes
- added explicit guidance that some cases stall not at first MMIO effect proof but at the later interrupt/completion/deferred-worker handoff that turns earlier hardware-facing activity into durable behavior

### D. Updated top-level navigation
Updated:
- `index.md`

What changed:
- added the new ISR/deferred-worker note into the firmware / protocol practical branch list
- updated the branch framing from two recurring bottlenecks to three:
  - parser-to-state consequence localization
  - peripheral/MMIO effect proof
  - ISR/deferred-worker consequence proof

## 5. Why these changes matter
This run improved the KB itself rather than merely collecting another generic firmware note.

It did **not**:
- create another abstract interrupt-taxonomy page
- deepen browser or WebView notes again
- stop at saying “interrupts matter in firmware”

It **did**:
- identify a coherent follow-on gap inside the firmware branch
- normalize the recurring operator bottleneck around later ISR/deferred-worker consequence proof
- connect that branch cleanly to existing parser, peripheral, runtime-evidence, and native consequence-first styles

The durable improvement is:

```text
the KB now has a practical firmware follow-on note for the moment when
trigger visibility and even some peripheral/MMIO effect visibility already exist,
but the analyst still cannot tell which ISR, completion callback,
tasklet, workqueue, or deferred handler
turns that earlier hardware-facing edge into the first durable consequence.
```

That is much more useful than another broad “interrupt-driven firmware is hard” paragraph would have been.

## 6. New findings
### A. The firmware follow-on gap was deferred consequence proof, not more register labeling
The KB already had enough signal to say firmware analysis often depends on context, parser consequence, and MMIO/peripheral effect proof.
What it lacked was a compact operator note for the common next state where the visible write still is not the best proof boundary.

### B. Interrupt-driven firmware work fits the KB’s broader consequence-first style well
A now-clear cross-branch pattern is:
- native: interface -> state -> effect proof
- protocol: parser -> state consequence edge
- peripheral/MMIO: effect-bearing write -> proof of hardware-side consequence
- runtime evidence: late effect -> causal boundary localization
- interrupt-driven firmware: peripheral effect -> ISR/deferred handoff -> durable consequence proof

That coherence makes the KB more consistent and easier to navigate.

### C. Callback/ISR visibility is often one layer too early
One valuable normalization from this run is that firmware interrupt-driven work should not stop at enumerating vectors, acks, or deferred callbacks.
The recurring practical leverage is often at the first narrower reduction:
- completion/status -> mode bucket
- interrupt source -> one stable handler family
- deferred callback -> one state/reply selector
- wakeup/queue edge -> one later visible effect

### D. This note gives the firmware branch a healthier internal progression
The firmware/protocol practical branch can now be read as:
- parser/state consequence if the missing edge is still protocol-side
- peripheral/MMIO effect proof if the missing edge is the first hardware-facing write/arm/latch
- ISR/deferred-worker consequence proof if the visible write exists but the durable consequence only appears later

That makes the branch more navigable and more realistic.

## 7. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- recent `runs/*.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/runtime-behavior-recovery.md`
- `topics/native-interface-to-state-proof-workflow-note.md`

### Existing source notes used this run
- `sources/firmware-protocol/2026-03-16-peripheral-mmio-effect-proof-notes.md`
- `sources/datasets-benchmarks/2026-03-14-firmware-protocol-context-notes.md`

### Fresh source consolidation created this run
- `sources/firmware-protocol/2026-03-16-isr-deferred-worker-consequence-proof-notes.md`

## 8. Reflections / synthesis
A stronger KB-wide operator pattern is now visible:

```text
some useful trigger and low-level visibility already exist
  -> freeze one representative compare pair
  -> localize one causally useful handoff boundary
  -> prove one durable state/reply/scheduler effect
  -> return to one smaller next task
```

The interrupt-driven firmware branch now has its own explicit version of that pattern.
That is healthy directionally because it keeps the KB centered on:
- consequence-bearing handoffs
- proof boundaries
- next trustworthy move
- practical follow-on work

rather than on ever-wider callback, vector, or interrupt-controller taxonomy growth.

## 9. Candidate topic pages to create or improve
### Improved this run
- `topics/firmware-and-protocol-context-recovery.md`
- `index.md`

### Created this run
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`
- `sources/firmware-protocol/2026-03-16-isr-deferred-worker-consequence-proof-notes.md`
- this run report

### Good next improvements
- a follow-on note around minimal interrupt/completion modeling for rehosting once one deferred consequence edge is known
- a companion note around DMA descriptor / completion-ring proof if more cases cluster there
- a firmware branch guide page if the protocol/peripheral/interrupt practical cluster grows a few more siblings

## 10. Next-step research directions
1. Keep the firmware/protocol branch practical with small workflow notes instead of broad driver-taxonomy growth.
2. Watch for a good follow-on split around DMA descriptor / completion-ring proof if more cases cluster there.
3. Watch for a good follow-on split around minimal interrupt/completion modeling once one deferred consequence edge is proved.
4. Continue resisting browser/WebView overconcentration unless a clearly missing high-value practical gap appears.
5. Revisit top-level navigation after a few more branch-balance passes so the KB’s center of gravity remains honest.

## 11. Concrete scenario notes or actionable tactics added this run
### Practical scenario normalized this run
**A firmware case already exposes trigger visibility and even some peripheral/MMIO effect visibility, but the analyst still cannot tell which ISR, completion callback, tasklet, workqueue, or deferred handler turns that earlier hardware-facing edge into the first durable consequence.**

### Concrete tactics added
- do not confuse visible MMIO writes with the most useful proof boundary
- freeze one representative compare pair only
- mark trigger, peripheral-effect, interrupt/deferred handoff, consequence, and proof-of-effect boundaries explicitly
- prefer the first durable state/reply/scheduler reduction over broad ISR enumeration
- prove one later effect before widening rehosting or interrupt-controller modeling

## 12. Commit / archival-sync status
### KB files changed this run
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/topics/firmware-and-protocol-context-recovery.md`
- `research/reverse-expert-kb/topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`
- `research/reverse-expert-kb/sources/firmware-protocol/2026-03-16-isr-deferred-worker-consequence-proof-notes.md`
- `research/reverse-expert-kb/runs/2026-03-16-2330-isr-deferred-worker-consequence-branch-balance-pass.md`

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
This autosync run improved the reverse KB by deepening the firmware/protocol practical branch with a missing interrupt-driven follow-on note.

The KB already knew that parser visibility and peripheral/MMIO effect proof matter.
Now it also has a concrete workflow note for the common bottleneck where those earlier layers are already partly solved but the first durable consequence still hides in ISR/deferred-worker handling, which makes the firmware/protocol branch more balanced, more navigable, and more practically useful.
