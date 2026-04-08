# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice
**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to CLAUDE.md, AGENTS.md, or copilot-instructions.md |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250115-001] best_practice

**Logged**: 2025-01-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/docker-m1-fixes
**Area**: infra

### Summary
Docker build fails on Apple Silicon due to platform mismatch
...
```

---

## [LRN-20260408-001] correction

**Logged**: 2026-04-08T13:50:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Do not default FRP relay mappings to SSH when the user asked for business-service ports.

### Details
In the FRPS relay follow-up for `self-server-44005`, I initially treated `30002`/`30003` as SSH exposure for `home-macmini` and `home-nas` because SSH was already easy to verify. The user corrected this: the intended public mappings were business ports, specifically ComfyUI on the Mac and the Synology DSM WebUI on the NAS, while SSH should continue over Tailscale only.

### Suggested Action
When continuing prior infra work, verify the intended service targets before freezing public port mappings in docs. If the user mentions application names (for example ComfyUI / DSM WebUI), prefer confirming local listening ports and service responses rather than assuming SSH.

### Metadata
- Source: user_feedback
- Related Files: infra/hosts/self-server/projects/frps-relay-plan.md, infra/hosts/self-server/NETWORK.md
- Tags: frp, correction, infra, service-mapping

---

## [LRN-20260314-001] correction

**Logged**: 2026-03-14T15:48:00+08:00
**Priority**: high
**Status**: promoted
**Area**: docs

### Summary
The reverse-expert KB drifted too far toward abstract taxonomy/synthesis and away from concrete, practical reverse-engineering methodology and target-specific analysis.

### Details
Human feedback was explicit: the KB feels empty and overly abstract, lacking grounded methodology, real scenario problem-solving, code-adjacent content, and specific website/app reverse-engineering analysis. Recent work overproduced structured topic pages and subtree taxonomy while underproducing pages that show how to actually solve concrete targets in practice.

### Suggested Action
Shift future KB work toward:
- practical workflow pages
- site/app/protection-family-specific case notes
- code snippets / pseudocode / hook points / harness patterns
- breakpoint plans, parameter-location tactics, environment reconstruction procedures, and failure diagnosis patterns
- concrete scenario sections inside topic pages rather than pure synthesis

### Metadata
- Source: user_feedback
- Related Files: research/reverse-expert-kb/, .learnings/LEARNINGS.md, AGENTS.md, MEMORY.md
- Tags: kb, correction, reverse-engineering, methodology, case-driven
- Pattern-Key: kb.avoid.abstract_only_synthesis
- Recurrence-Count: 1
- First-Seen: 2026-03-14
- Last-Seen: 2026-03-14
- Promoted: AGENTS.md, MEMORY.md

### Resolution
- **Resolved**: 2026-03-15T09:00:00+08:00
- **Notes**: Promoted the direction change into workspace execution rules and long-term memory so future KB work stays practical and case-driven.

---

