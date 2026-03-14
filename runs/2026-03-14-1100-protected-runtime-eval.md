# Reverse Expert KB Run Report — 2026-03-14 11:00 Asia/Shanghai

## 1. Scope this run
This run focused on deepening an already-created topic rather than creating another new page:

- **anti-tamper and protected-runtime analysis**
- stronger **software-protection / MATE evaluation framing**
- **virtualization-based obfuscation** as a bridge case between unreadable code and hostile runtime
- **kernel-level anti-cheat** as a concrete protected-runtime case study
- improved language for describing analyst burden in terms of **observability, distortion, and environment control**

The goal was to get genuinely new material into the KB by improving the source density and conceptual precision of an existing topic page, not by rehashing generic anti-debug ideas.

## 2. New findings

### Protected-runtime analysis benefits from software-protection evaluation vocabulary
A useful new seam this run was the software-protection literature around **MATE (man-at-the-end)** assumptions and evaluation methodology.

That literature is valuable for the KB because it gives better language for describing protected targets:
- what assets are being protected
- what powers the analyst/attacker has over the execution environment
- which actions are merely delayed versus made unreliable
- how protection claims are or are not evaluated rigorously

This is stronger than calling a target merely “obfuscated” or “anti-debugged.”

### “Hard to read” and “hard to observe safely” are separate burdens
The anti-tamper topic already pointed in this direction, but this run sharpened it.

A protected target can be difficult because:
- static recovery is poor
- hooks/traces are difficult to sustain
- runtime observations are distorted by protection logic
- the required environment control is expensive or brittle

That suggests a better analyst-facing vocabulary includes:
- **unreadability**
- **unhookability / trace resistance**
- **evidence distortion risk**
- **required environment control**
- **effort displacement**

This feels like a meaningful KB-wide improvement, not just a local note.

### Evaluation-methodology work helps avoid vague claims about “strong protection”
Work on software-protection evaluation methodology was useful because it emphasizes that protection research often compares systems poorly unless attacker goals, assets, and success criteria are explicit.

For this KB, the implication is:
protected-runtime pages should avoid vague language like “hard to reverse” when they can instead say:
- what evidence becomes less available
- what analyst actions become less reliable
- which assumptions about environment control now matter
- whether burden is increased by readability loss, observability loss, or both

### Virtualization-based obfuscation is a strong bridge case
The VMAttack paper/project materials were especially useful as a bridge between the existing packed/obfuscation page and the anti-tamper/protected-runtime page.

Why:
- virtualization-heavy targets are not just “packed once” and restored to normal code
- the analyst often faces an interpreter, bytecode layer, and noisy traces
- progress depends on combining static and dynamic evidence
- ranking and clustering trace regions becomes part of the workflow
- partial deobfuscation can be more valuable than full semantic recovery

This is important because it shows a middle zone where code transformation and runtime evidence-management interact directly.

### Anti-cheat is a useful protected-runtime subdomain because the tradeoffs are explicit
The kernel-level anti-cheat sources were valuable less as “game hacking” material and more as a very explicit case study in protected-runtime tradeoffs.

They foreground:
- privilege level
- stealth/intrusiveness
- monitoring scope
- integrity enforcement
- privacy/system-integrity cost
- rootkit-like behavior as an evaluative frame

That makes anti-cheat a good subdomain for the KB because it reveals how protected-runtime analysis often depends on reasoning about **who controls observation**, **at what privilege level**, and **with what trust cost**.

### The anti-tamper page now has a better path toward later splitting
This run clarified likely future child pages:
- anti-instrumentation and anti-debugging
- integrity checks and tamper response
- protected observation workflows
- anti-cheat / trusted-runtime environments

That is useful because the topic no longer feels like a catch-all page; it now has a clearer internal decomposition.

## 3. Sources consulted
- https://arxiv.org/pdf/2307.07300
- https://arxiv.org/pdf/2011.07269
- https://github.com/anatolikalysch/VMAttack
- https://dl.acm.org/doi/10.1145/3098954.3098995
- https://arxiv.org/html/2408.00500v1
- https://arxiv.org/html/2512.21377v1
- search-layer deep exploratory passes around:
  - anti-tamper protected runtime analysis reverse engineering virtualization obfuscation anti debug survey
  - software protection anti tamper reverse engineering dynamic analysis virtualization obfuscation
  - anti cheat protected binaries reverse engineering anti debug virtualization packers survey
  - VMAttack Deobfuscating Virtualization-Based Packed Binaries pdf
  - evaluation methodologies in software protection research anti tamper man at the end pdf

Additional local source note saved:
- `sources/protected-runtime/2026-03-14-evaluation-and-cases.md`

## 4. Reflections / synthesis
This run mostly improved **conceptual precision**.

Earlier KB structure already distinguished:
- obfuscation/deobfuscation
- runtime behavior recovery
- mobile instrumentation constraints
- native baseline workflows

What this run adds is a better way to connect them:
protected-runtime analysis is where those concerns become unified under the question,
**“what evidence can still be trusted under active resistance?”**

A second useful synthesis is that software-protection literature, even when written from a defender or evaluation perspective, can still enrich an analyst-centered KB if translated carefully. The best reuse is not defensive design advice; it is the vocabulary for talking about:
- assets
- attacker powers
- evaluation assumptions
- which burdens are actually being imposed on analysis

That makes the anti-tamper page more disciplined and less folklore-driven.

## 5. Candidate topic pages to create or improve
- Improved: `topics/anti-tamper-and-protected-runtime-analysis.md`
- Improve later: `topics/obfuscation-deobfuscation-and-packed-binaries.md` with a clearer cross-link to virtualization-as-bridge-case
- Improve later: `topics/runtime-behavior-recovery.md` with explicit “evidence distortion” language
- Create later: `topics/anti-instrumentation-and-anti-debugging.md`
- Create later: `topics/integrity-checks-and-tamper-response.md`
- Create later: `topics/protected-observation-workflows.md`
- Create later: `topics/anti-cheat-and-trusted-runtime-analysis.md`
- Possibly improve: `index.md` later if the protected-runtime branch grows enough to deserve explicit mention in the high-level reading order

## 6. Next-step research directions
1. Find stronger sources specifically on **anti-instrumentation / anti-debugging** that are workflow-relevant rather than purely bypass-oriented.
2. Do a dedicated pass on **integrity-check and tamper-response** literature with an analyst-centered framing.
3. Compare **virtualization-based obfuscation** workflows with other protection families to identify shared evidence-management patterns.
4. Look for sources that make **trace pollution / trace ranking / partial evidence filtering** explicit across more than one protection family.
5. Build a reusable KB vocabulary for protected targets along dimensions like:
   - readability loss
   - hookability
   - evidence distortion risk
   - environment-control burden
   - trust/privacy cost of observation
6. Revisit the high-level KB map once two or three more protected-runtime child pages exist.

## Operational notes
- Improved an existing topic page instead of creating a duplicate one.
- Saved one compact source-note file under `sources/protected-runtime/`.
- Did not retain bulky external artifacts.
- This run stayed fully within research/collection/synthesis.
