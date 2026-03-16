# Run Report — 2026-03-16 18:32 — flattened dispatcher / state-edge branch-balance pass

## 1. Scope this run
This run was a scheduled autosync / branch-balance / maintenance pass for `research/reverse-expert-kb/`.

The direction choice this run was to keep strengthening the KB itself while resisting overconcentration in the already-dense browser anti-bot and mobile protected-runtime subtrees.
Recent runs had already added practical notes for:
- trace-slice to handler reconstruction
- protocol parser to state-edge localization
- native interface to state proof
- VM trace to semantic-anchor reduction
- malware staged execution to first proved consequence

That left the deobfuscation / protected-runtime practical branch still somewhat thinner than it should be relative to the maturity of its synthesis parent.
The specific gap targeted this run was:

```text
flattened / dispatcher-heavy logic is already visible,
but the first durable state object or consequence-bearing state edge
is still hidden behind handler churn or helper noise.
```

So this run focused on adding a practical workflow note for flattened-dispatcher -> state-edge reduction, plus the supporting source note and navigation updates needed to make that branch more legible.

## 2. Direction review
### Current direction check
The KB remains healthiest when each run improves an analyst’s next move rather than merely widening taxonomy.
That still means preferring:
- practical workflow notes
- consequence-first routing
- case-driven boundary selection
- small reconnectable static targets
- compare-run / state-edge / first-proof framing

That direction is now strong in:
- browser request-finalization and first-consumer notes
- WebView/native lifecycle and response-consumer notes
- mobile challenge / policy / delayed-consequence notes
- protocol parser -> state consequence routing
- native interface -> state proof
- malware staged execution -> first consequence proof
- protected-runtime trace -> semantic-anchor reduction

This run extended that same philosophy one level deeper inside the deobfuscation branch:
- **not just semantic-anchor reduction, but the more specific moment where the dispatcher is already visible and the analyst needs the first durable state edge**

### Branch-balance review
Branch balance remains better than before, but still visibly uneven.
A rough practical picture at the start of this run looked like:
- **very strong:** browser anti-bot / captcha / request-signature / hybrid WebView workflows
- **strong:** mobile protected-runtime / challenge / policy / ownership / consequence notes
- **improving:** protocol, native, malware, and deobfuscation practical branches
- **still thin:** iOS practical workflows

Within the deobfuscation branch itself, there was still a shape imbalance:
- mature synthesis parent existed
- one practical VM trace -> semantic anchor note existed
- but there was no separate workflow note for the narrower and very common case where the dispatcher is already recognized and the bottleneck is now the first durable state object / state edge

That made this run a good fit for branch-balance repair without drifting back into the easier browser/mobile gravity well.

## 3. Files reviewed
Primary files reviewed this run:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent `runs/*.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- `topics/trace-slice-to-handler-reconstruction-workflow-note.md`
- `topics/jsvmp-and-ast-based-devirtualization.md`
- `sources/datasets-benchmarks/2026-03-14-obfuscation-benchmarks-source-notes.md`
- `sources/protected-runtime/2026-03-16-vm-trace-to-semantic-anchor-notes.md`
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`

## 4. KB changes made
### A. Created a new protected-runtime / deobfuscation source note
Created:
- `sources/protected-runtime/2026-03-16-flattened-dispatcher-to-state-edge-notes.md`

What it adds:
- a workflow-centered consolidation for the recurring case where dispatcher recognition exists but the decisive state edge is still unclear
- an explicit operator model:
  - dispatcher churn
  - reduction helper / handler bucket
  - first durable state object or state edge
  - later operational effect
- a stronger distinction between “found the dispatcher” and “proved the first behavior-predicting state edge”

### B. Created a new practical workflow note
Created:
- `topics/flattened-dispatcher-to-state-edge-workflow-note.md`

What it adds:
- a concrete operator-facing workflow note for flattened or dispatcher-heavy regions once broad VM/flattening structure is already visible
- explicit routing from:
  - one late effect
  - one narrow dispatcher window
  - one role-labeled reduction helper / state object
  - one first consequence-bearing state edge
  - one downstream proof
  - one smaller static target only
- concrete scenario families for:
  - reduction-helper -> mode/enum edges
  - state-slot -> scheduler edges
  - dispatcher-exit -> consumer edges
  - compare-run state-edge divergence

### C. Strengthened the deobfuscation synthesis parent with a second practical child route
Updated:
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`

What changed:
- expanded the practical-bridge section from one practical child page to two
- clarified the difference between:
  - semantic-anchor-first reduction (`vm-trace-to-semantic-anchor-workflow-note`)
  - dispatcher-to-state-edge reduction (`flattened-dispatcher-to-state-edge-workflow-note`)

This makes the protected/deobfuscation branch less dependent on a single practical note.

### D. Updated top-level navigation
Updated:
- `index.md`

What changed:
- added a dedicated **Deobfuscation / protected-runtime practical branch** section
- made this branch more visible alongside malware, protocol, native, browser, and mobile practical branches
- positioned the new workflow note as the practical entry page for cases where the dispatcher is already recognizable and the next bottleneck is the first durable state object / state edge

## 5. Why these changes matter
This run improved the KB itself rather than merely collecting another note about deobfuscation.

It did **not**:
- deepen browser anti-bot or WebView timing again
- create another umbrella deobfuscation taxonomy page
- pretend that full handler/opcode reconstruction is the right milestone for every flattened target

It **did**:
- identify a recurring middle-state bottleneck inside the deobfuscation branch
- add a practical note for that bottleneck
- make navigation reflect the branch more honestly
- strengthen KB-wide coherence around a repeated theme:

```text
some structure is already visible
  -> pick one narrow window
  -> localize one durable object or edge
  -> prove one downstream effect
  -> return to one smaller static target
```

The durable improvement is:

```text
the KB now has a practical note for the moment when
flattened / dispatcher-heavy logic is already recognized,
but the analyst still needs the first durable state edge
that predicts later behavior before deeper static work becomes trustworthy.
```

## 6. New findings
### A. Deobfuscation had a practical gap between “semantic anchor” and “full handler reconstruction”
The VM trace -> semantic-anchor note already solved one real problem.
But a smaller and more concrete recurring problem still lacked its own page:
- dispatcher recognized
- helper churn partly reduced
- first durable state edge still unclear

That gap is common enough to deserve a dedicated workflow note.

### B. “First durable state edge” is a useful deobfuscation-side milestone
A stronger cross-branch parallel is now visible:
- browser: first accepted consumer / request-finalization edge
- mobile: first policy bucket / delayed consequence edge
- native: first interface -> state -> effect proof
- protocol: first parser -> state consequence edge
- malware: first staging handoff that predicts later behavior
- deobfuscation / flattened dispatcher: first durable state edge that predicts later behavior

That parallelism improves KB coherence and makes the practical notes easier to navigate conceptually.

### C. Dispatcher recognition is only orientation, not payoff
A recurring failure mode in protected/deobfuscation work is to overvalue the moment when the dispatcher has been found.
In practice, the higher-payoff milestone is usually:
- one durable state object
- one reduction helper
- one dispatcher-exit family
- one consequence-bearing write/branch

That smaller milestone is easier to prove and easier to hand back to static analysis.

### D. The deobfuscation branch now has a clearer practical shape
Before this run, the branch had:
- one mature synthesis page
- one practical VM note

After this run, it has:
- one mature synthesis page
- one trace -> semantic-anchor note
- one dispatcher -> state-edge note

That is a better shape for future growth because follow-up notes can now stay small and role-specific rather than bloating one practical page.

## 7. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- recent `runs/*.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- `topics/trace-slice-to-handler-reconstruction-workflow-note.md`
- `topics/jsvmp-and-ast-based-devirtualization.md`

### Existing source notes used this run
- `sources/datasets-benchmarks/2026-03-14-obfuscation-benchmarks-source-notes.md`
- `sources/protected-runtime/2026-03-16-vm-trace-to-semantic-anchor-notes.md`
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`

### Fresh source consolidation created this run
- `sources/protected-runtime/2026-03-16-flattened-dispatcher-to-state-edge-notes.md`

## 8. Reflections / synthesis
The KB is increasingly converging on a reliable operator pattern:

```text
visible but noisy structure
  -> choose one small boundary/window
  -> name one durable object or edge
  -> prove one downstream effect
  -> convert that into one smaller next target
```

This run matters because it applies that pattern to a common deobfuscation failure mode where analysts can already point to the flattened region but still cannot say which state transition actually matters.

That is exactly the kind of gap a practical KB should close.

## 9. Candidate topic pages to create or improve
### Improved this run
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `index.md`

### Created this run
- `topics/flattened-dispatcher-to-state-edge-workflow-note.md`
- `sources/protected-runtime/2026-03-16-flattened-dispatcher-to-state-edge-notes.md`
- this run report

### Good next improvements
- an iOS practical workflow note to repair the thinnest major branch
- a deobfuscation note around unpacked-region relabeling after the first stable state edge is proved
- a deobfuscation note around handler-bucket -> outer-consumer proof in mixed JS/wasm or native protected loops
- a protected-runtime note around integrity-result -> feature-gate -> later consequence mapping

## 10. Next-step research directions
1. Keep the deobfuscation branch growing through small practical notes rather than broad new taxonomy pages.
2. Use upcoming runs to strengthen iOS practical reversing, which remains the clearest thin branch at the top level.
3. Consider a follow-on protected/deobfuscation note around reduction-helper -> outer-consumer proof once this new page has had time to settle structurally.
4. Continue resisting browser/WebView overconcentration unless a clearly missing high-value practical gap appears.
5. Periodically revisit the index so top-level navigation keeps matching the KB’s real center of gravity.

## 11. Concrete scenario notes or actionable tactics added this run
### Practical scenario normalized this run
**The dispatcher is already visible, but the investigation still stalls until one durable state object or state edge is proved to predict the later behavior.**

### Concrete tactics added
- do not treat “dispatcher found” as the milestone; treat “first durable state edge proved” as the milestone
- freeze one narrow dispatcher window rather than trying to map the whole protected region
- role-label regions as dispatcher churn / reduction helper / durable state write / outer consumer before exact semantics
- prefer one reconnectable state object or helper over a giant handler catalog
- push one step past helper identification to the first durable write / branch / scheduler edge
- hand the result back as one smaller static target only

## 12. Commit / archival-sync status
### KB files changed this run
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `research/reverse-expert-kb/topics/flattened-dispatcher-to-state-edge-workflow-note.md`
- `research/reverse-expert-kb/sources/protected-runtime/2026-03-16-flattened-dispatcher-to-state-edge-notes.md`
- `research/reverse-expert-kb/runs/2026-03-16-1832-flattened-dispatcher-state-edge-branch-balance-pass.md`

### Commit intent
Commit only the reverse-KB files touched by this run.
Do not mix in unrelated workspace or `infra/` changes.

### Pre-commit note
A pre-existing unrelated modification was already present in:
- `research/reverse-expert-kb/runs/2026-03-16-0300-reese84-utmvc-bootstrap-and-first-consumer.md`

That file was intentionally left out of this run’s commit.

### Sync intent
After commit, run:
- `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

If sync fails:
- preserve local KB progress
- mention the failure briefly in this run report
- do not roll back the KB improvement

## 13. Bottom line
This autosync run improved the reverse KB by strengthening a still-thin deobfuscation / protected-runtime practical branch.

The KB already had the synthesis needed to talk about obfuscation, protected execution, JSVMP, and trace-guided reduction.
Now it also has a practical workflow note for the common middle-state bottleneck where the dispatcher is already recognizable but the first durable state edge that actually predicts later behavior is still unproven, which makes the branch more practical, more navigable, and better balanced against the already-dense browser/mobile areas.
