# Reverse KB Autosync Run Report

Date: 2026-03-22 11:21 Asia/Shanghai / 2026-03-22 03:21 UTC
Mode: external-research-driven
Focus: protocol/firmware practical subtree — pending-request ownership, correlation matching, and async-reply consumption as a narrow child of replay gating

## Why this branch
Recent same-day autosync runs were already doing useful practical work, but they were still concentrated on internal branch balancing and closely adjacent ladder refinements:
- first-bad-write runtime evidence
- iOS PAC callback dispatch triage
- method-contract -> minimal replay fixture
- native GUI message-pump first consumer

That was enough internal-maintenance density that another wording/index-only pass would risk stagnation. This run therefore prioritized a thinner still-practical protocol seam where operator value was present but no dedicated workflow note existed yet.

## Direction review
Protocol replay already had:
- broad replay-precondition / state-gate guidance
- minimal replay-fixture guidance
- reply-emission / transport-handoff guidance

But it did **not** yet have one narrow practical note for the recurring case where:
- a response or completion is already structurally plausible
- the parser may even accept it
- yet behavior still does not advance because the real gate is one outstanding-request owner, async handle, callback queue, pending slot, or correlation match

This is a practical operator seam, not a taxonomy flourish, and it is especially relevant in RPC, mailbox, and queue-backed protocols.

## Work completed

### New source note
Added:
- `sources/firmware-protocol/2026-03-22-pending-request-correlation-and-async-reply-notes.md`

What it retains:
- Windows async RPC completion-handle behavior
- `RPC_ASYNC_STATE` as a durable async-call state carrier
- RPC Investigator / ETW-aware active-call visibility
- ALPC communication-object context
- RabbitMQ correlation-ID reply matching as a clean generic ownership model
- BitBlaze / Replayer framing for dialogue replay as a downstream protocol-RE goal

### New practical workflow note
Added:
- `topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md`

What it contributes:
- a concrete narrow workflow for cases where reply-like traffic is visible but still not consumed
- explicit separation of response shape correctness vs response ownership correctness
- a five-boundary model:
  1. request issuance
  2. pending-owner creation
  3. response arrival
  4. ownership match
  5. consume / wake / complete
- concrete operator anchors: pending tables, async handles, callback queues, correlation IDs, descriptor slots, promise/future resolution, stale-drop branches
- handoff discipline so the branch does not widen back into generic replay theory once the ownership gate is the real bottleneck

### Branch-balance / canonical sync updates
Updated parent pages so the new note is discoverable from the protocol/firmware operator ladder:
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/firmware-and-protocol-context-recovery.md`

These were intentionally minimal link-and-routing updates, not another broad wording cleanup pass.

## Practical value added
This run improved the KB itself, not just note collection, by adding a reusable continuation page for a concrete stalled-replay pattern:
- “reply exists but nothing wakes/completes/advances”

That should help future operators choose a smaller next experiment instead of repeatedly cycling between:
- more packet labeling
- broader replay-gate theorizing
- more service/schema cleanup

## Search audit
Requested sources: exa, tavily, grok
Succeeded sources: exa, tavily, grok
Failed sources: none

Endpoints used:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Search invocation:
- explicit `search-layer` script run with `--source exa,tavily,grok`
- query set targeted pending-request correlation, async reply completion, and request/response ownership patterns

Outcome quality:
- all three requested sources were actually invoked
- result quality was mixed but usable
- strongest retained evidence came from:
  - Microsoft Learn async RPC docs
  - Trail of Bits RPC Investigator context
  - ALPC internals article
  - RabbitMQ RPC correlation tutorial
  - BitBlaze / Replayer framing
- this was sufficient for a conservative, source-backed practical note

Artifacts:
- raw search-layer output captured at `sources/2026-03-22-protocol-pending-request-correlation-search-layer.txt`

## Files changed
- `sources/firmware-protocol/2026-03-22-pending-request-correlation-and-async-reply-notes.md`
- `topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `runs/2026-03-22-1121-pending-request-correlation-async-reply-autosync.md`

## Commit / sync plan
If git diff shows only the above KB paths as relevant changes, commit them as one scoped KB update and then run:
- `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

## Confidence and limits
Confidence:
- good for the workflow shape and branch fit
- good that this is a thinner, practical, operator-valuable continuation page rather than index churn

Limits:
- source set is heterogeneous and not all hits were equally high-signal
- the new note is intentionally conservative and does **not** claim pending-request ownership is the universal cause of ignored replies
- this run did not attempt to widen into a larger protocol-state or queueing taxonomy

## Result
Successful external-research-driven practical branch extension.
The protocol/firmware subtree now has a dedicated narrow continuation page for outstanding-request ownership and reply-consumption failures, with parent-page routing updated accordingly.
