# Protected-runtime analysis source notes — 2026-03-14

## Focus
Strengthen the KB's anti-tamper / protected-runtime topic with better source grounding around:
- software-protection evaluation language
- MATE framing
- virtualization/devirtualization as bridge cases
- anti-cheat as protected-runtime case study

## High-value sources

### Evaluation Methodologies in Software Protection Research
- URL: https://arxiv.org/pdf/2307.07300
- Why useful:
  - gives a language for talking about protection evaluation, attacker assumptions, assets, and methodological weakness
  - useful for translating “protection strength” into analyst-centered burdens like evidence distortion, environment control, and effort displacement

### Man-at-the-End Software Protection as a Risk Analysis Process
- URL: https://arxiv.org/pdf/2011.07269
- Why useful:
  - frames software protection under white-box / MATE assumptions
  - helps distinguish asset, attacker power, and protection goal from vague anti-debug terminology

### VMAttack: Deobfuscating Virtualization-Based Packed Binaries
- URL: https://dl.acm.org/doi/10.1145/3098954.3098995
- Backup/open note source: https://github.com/anatolikalysch/VMAttack
- Why useful:
  - good bridge case between packed/virtualized code and analyst workflow under noisy traces
  - highlights ranking, clustering, static/dynamic combination, and partial deobfuscation workflow support

### If It Looks Like a Rootkit and Deceives Like a Rootkit: A Critical Examination of Kernel-Level Anti-Cheat Systems
- URL: https://arxiv.org/html/2408.00500v1
- DOI shown in fetched text: 10.1145/3664476.3670433
- Why useful:
  - concrete protected-runtime case study
  - makes tradeoffs around privilege, stealth, intrusiveness, and trust/privacy explicit
  - useful for framing anti-cheat as one subdomain of protected-runtime analysis, not the whole topic

### A Systematic Review of Technical Defenses Against Software-Based Cheating in Online Multiplayer Games
- URL: https://arxiv.org/html/2512.21377v1
- Why useful:
  - broad taxonomy of server-side, client-side anti-tamper, kernel-level, and TEE-assisted approaches
  - useful as a map of defense categories even if not all details are equally mature

## Key synthesis extracted
- Protected-runtime analysis needs vocabulary beyond “obfuscated” or “anti-debugged”.
- MATE/evaluation literature helps describe protected targets in terms of assets, attacker powers, and evaluation assumptions.
- Virtualization-based protection is a bridge case where static unreadability and runtime evidence pollution interact directly.
- Anti-cheat is useful as an explicit case of privileged monitoring and observability asymmetry.
- Better analyst-facing metrics include: evidence availability, evidence distortion risk, effort displacement, required environment control, and transferability.

## Notes
- ResearchGate mirror was blocked; did not retain.
- Some PDF endpoints returned raw bytes in web_fetch; used accessible mirrors / project page descriptions when needed.
- No large binary/source downloads retained.
