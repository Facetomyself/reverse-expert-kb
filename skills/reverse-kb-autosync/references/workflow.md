# Reverse KB Autosync Workflow

## Goal

Continuously grow, analyze, integrate, normalize, review, and preserve the reverse-engineering expert knowledge base under:

- `research/reverse-expert-kb/`

The human wants strategic steering only. Ordinary topic creation, consolidation, navigation cleanup, commits, and sync should proceed autonomously.

---

## Primary operating rules

### 1. Stay practical

Do **not** spend most runs creating new abstract taxonomy pages.

Prefer:
- concrete methodology
- target-specific workflow notes
- case-driven analysis
- code-adjacent notes
- breakpoint / hook placement tactics
- compare-run diagnosis
- environment reconstruction procedures
- failure-mode diagnosis
- small representative pseudocode / code fragments when useful

### 2. Improve the KB, not just notes about the KB

Prefer improving canonical topic pages and navigation over producing isolated scratch output.

Use source notes and run reports to support the KB, not replace it.

### 3. Preserve provenance

Keep external source traces organized under:
- `research/reverse-expert-kb/sources/`

Write one Markdown run report per execution under:
- `research/reverse-expert-kb/runs/`

### 4. Commit and sync

If KB files changed:
- commit in `/root/.openclaw/workspace`
- then run:
  - `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

If sync fails:
- record the failure briefly in the run report
- keep local KB progress intact

### 5. Learnings logging is best-effort only

If tooling failures or workflow gotchas should be recorded in:
- `/root/.openclaw/workspace/.learnings/ERRORS.md`

that logging is **best-effort only**.

If it fails:
- mention it briefly in the run report
- do **not** fail the whole run solely because that append/edit missed

---

## Mandatory direction review

This workflow must not act like a blind topic generator.

Before deciding scope for each run, perform a direction check:
- Which major branches are currently strongest?
- Which branches are weak, missing, or underdeveloped?
- Is recent work over-concentrated in one subtree or micro-theme?
- Is this run better spent on:
  - new concrete workflow content
  - consolidation
  - navigation cleanup
  - branch-balance repair
  - case-note deepening

### Periodic branch-balance review

At least every 6 runs, or sooner if drift is obvious, include a more explicit review in the run report covering:
- branch strength vs weakness
- overrepresented vs underrepresented domains
- whether browser-runtime and mobile/protected-runtime are crowding out other RE areas
- whether the KB is missing high-value practical branches such as:
  - iOS practical reversing
  - desktop native practical workflows
  - protocol / firmware practical workflows
  - malware practical workflows
  - deobfuscation case-driven workflows
- whether top-level navigation still reflects the KB’s real center of gravity

When imbalance is visible, let it influence the next topic choice.

Do **not** keep deepening the same micro-branch forever just because recent source notes make that easy.

---

## Current balancing guidance

Treat these as currently strong branches unless fresh evidence suggests otherwise:
- browser anti-bot / captcha / request-signature workflows
- mobile protected-runtime / WebView / hybrid challenge-loop workflows

Treat these as relatively weaker branches unless fresh evidence shows they are now sufficiently mature:
- iOS practical reversing
- desktop native practical workflows
- protocol / firmware practical workflows
- malware practical workflows
- deeper deobfuscation case-driven workflows

If recent runs have concentrated heavily on WebView/mobile timing, native→page handoff, or browser anti-bot micro-variants, bias upcoming runs toward weaker but high-value branches unless there is a compelling continuity reason to finish a nearly-complete local sequence.

---

## Preferred run shape

Each run should usually do some mix of:
1. Read current structure and recent work
2. Choose a practical, high-value scope
3. Add or improve KB pages
4. Update navigation when structure changes, but do it with small robust edits and best-effort tolerance
5. Write one run report
6. Commit changes if any
7. Sync subtree to GitHub

---

## Run report sections

Every run report should include:
1. Scope this run
2. New findings
3. Sources consulted
4. Reflections / synthesis
5. Candidate topic pages to create or improve
6. Next-step research directions
7. Concrete scenario notes or actionable tactics added this run
8. Search audit (for any run that used search)

For search-bearing runs, the `Search audit` section should at minimum include:
- `Search sources requested:` `exa,tavily,grok`
- `Search sources succeeded:` ...
- `Search sources failed:` ...
- `Exa endpoint:` ...
- `Tavily endpoint:` ...
- `Grok endpoint:` ...

When a branch-balance review is performed, include a clearly labeled section for it.

---

## Suggested reading focus before choosing work

Always consult:
- `research/reverse-expert-kb/index.md`
- recent `runs/*.md`
- recent `sources/**/*.md`
- relevant subtree guide pages

Useful subtree guides include:
- `research/reverse-expert-kb/topics/browser-runtime-subtree-guide.md`
- `research/reverse-expert-kb/topics/mobile-protected-runtime-subtree-guide.md`

---

## Anti-drift rule

Before creating a new abstract page, ask whether the same effort would be better spent on one of these instead:
- a concrete scenario page
- a case-study page
- a methodology page with operator steps
- a workflow cookbook page
- a code-backed note
- a branch consolidation / route guide page

Bias toward the concrete option unless there is a strong structural reason not to.
seful subtree guides include:
- `research/reverse-expert-kb/topics/browser-runtime-subtree-guide.md`
- `research/reverse-expert-kb/topics/mobile-protected-runtime-subtree-guide.md`

---

## Anti-drift rule

Before creating a new abstract page, ask whether the same effort would be better spent on one of these instead:
- a concrete scenario page
- a case-study page
- a methodology page with operator steps
- a workflow cookbook page
- a code-backed note
- a branch consolidation / route guide page

Bias toward the concrete option unless there is a strong structural reason not to.
age, ask whether the same effort would be better spent on one of these instead:
- a concrete scenario page
- a case-study page
- a methodology page with operator steps
- a workflow cookbook page
- a code-backed note
- a branch consolidation / route guide page

Bias toward the concrete option unless there is a strong structural reason not to.
ether the same effort would be better spent on one of these instead:
- a concrete scenario page
- a case-study page
- a methodology page with operator steps
- a workflow cookbook page
- a code-backed note
- a branch consolidation / route guide page

Bias toward the concrete option unless there is a strong structural reason not to.
age, ask whether the same effort would be better spent on one of these instead:
- a concrete scenario page
- a case-study page
- a methodology page with operator steps
- a workflow cookbook page
- a code-backed note
- a branch consolidation / route guide page

Bias toward the concrete option unless there is a strong structural reason not to.
