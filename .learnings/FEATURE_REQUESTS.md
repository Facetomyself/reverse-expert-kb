# Feature Requests

Capabilities requested by user that don't currently exist.

## How to Use

Log a feature request here when the human wants something that is not currently supported, not automated yet, or would require new plumbing/integration instead of a simple one-off action.

Good triggers:
- "Can you also do X automatically?"
- "I wish you could..."
- "Why can't you..."
- "Can this be turned into a workflow / button / scheduled task / skill?"

Do **not** log here when:
- the capability already exists and just needs to be used correctly
- the problem is really a bug, failure, or missing config (log to `ERRORS.md`)
- the main outcome is a correction or best practice (log to `LEARNINGS.md`)

## Triage Rules

### Use `simple` when
- one file / one script / one prompt tweak could add it
- no new external service or auth model is needed

### Use `medium` when
- it needs a small workflow, helper script, or reusable skill
- it spans multiple files or tools

### Use `complex` when
- it needs a new integration, background workflow, persistent service, browser automation path, or nontrivial product design

## Promotion Rules

Promote recurring or clearly valuable requests into one of these:
- `AGENTS.md` — if it should become a standing workflow rule
- `TOOLS.md` — if it depends on local environment/tooling notes
- a new skill under `skills/` — if it becomes a reusable capability
- project/task backlog docs — if it needs implementation tracking

## Template

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
What the human wanted to do

### User Context
Why they wanted it / what problem this would solve

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this might be built or what it could extend

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name
- Promotion Target: AGENTS.md | TOOLS.md | skill | backlog (optional)

---
```

## Starter Strategy for This Workspace

When future requests come up, especially consider logging these kinds of asks:
- "Turn this recurring workflow into a skill"
- "Make this periodic/research task more automatic"
- "Add a safer/faster content extraction path for a stubborn site class"
- "Create a reusable GitHub / research / reverse-engineering helper workflow"
- "Expose a common operation as a documented shortcut instead of re-explaining it each time"

---
