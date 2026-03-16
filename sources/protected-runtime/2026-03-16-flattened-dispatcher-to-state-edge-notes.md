# Source notes — flattened dispatcher to state-edge / consequence-localization workflow

Generated: 2026-03-16 18:32 Asia/Shanghai

## Focus
Strengthen the KB’s deobfuscation / protected-runtime practical branch with a workflow for the recurring case where:
- flattening, dispatcher churn, or partial virtualization is already visible
- the analyst already has some static foothold or narrow trace slice
- but the first consequence-bearing state edge is still hidden behind dispatcher updates, helper churn, or mixed handler families

This note is intentionally workflow-centered.
It is meant to support a practical KB page rather than a benchmark summary.

## Source base used
### Existing KB synthesis pages
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/jsvmp-and-ast-based-devirtualization.md`
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- `topics/trace-slice-to-handler-reconstruction-workflow-note.md`

### Existing source notes
- `sources/datasets-benchmarks/2026-03-14-obfuscation-benchmarks-source-notes.md`
- `sources/protected-runtime/2026-03-16-vm-trace-to-semantic-anchor-notes.md`
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`

## High-signal extracted patterns

### 1. A common stall point appears after dispatcher recognition, not before it
In many practical deobfuscation cases, the analyst already knows they are looking at:
- a flattened switch loop
- a VM-like dispatcher
- a handler table or opcode family
- or a repetitive helper chain feeding one dispatch region

But progress still stalls because "dispatcher found" does not yet tell the analyst:
- which state slot actually matters
- which helper reduces noisy handler outputs into a durable local state
- which handler family first predicts later behavior
- where to reconnect the protected region back to ordinary static reasoning

Useful reformulation:
- finding the dispatcher is only orientation
- finding the first consequence-bearing state edge is the milestone

### 2. The right unit of progress is often one state-edge class, not one handler catalog
Practical signals across VM / OLLVM / flattened / JSVMP-style casework suggest that the highest-payoff next object is often:
- one state slot that later gates behavior
- one normalization helper that converts many handler effects into one enum/flag/object
- one dispatcher exit edge that consistently feeds a meaningful branch
- one handler bucket that always precedes the first durable state write

That is usually more useful than trying to fully map every opcode or every handler family first.

### 3. Flattened targets often need a dispatcher -> reduction-helper -> state-edge view
A compact operator model that seems to recur is:

```text
flattened / virtualized dispatcher churn
  -> repeated helper or small handler bucket
  -> first durable state reduction or write
  -> later operational effect
```

The helper layer matters because many targets do not expose the decisive semantics directly inside a single handler.
Instead they:
- accumulate transient values
- repack state
- normalize local registers/slots/objects
- collapse many VM states into a smaller policy or mode object

### 4. Compare-run discipline helps separate state edges from decorative churn
A useful workflow pattern is to compare at the same semantic boundary:
- same dispatcher entry window
- same late effect window
- same candidate state object or helper output

This often reveals that most handler churn is shared while one smaller difference appears at:
- a state-slot update
- a helper output shape
- a branch-family selector
- a scheduler enqueue/suppress decision

That difference is frequently the real leverage point.

### 5. Good outputs are reconnectable static targets
The workflow pays off when it returns one reconnectable object such as:
- one state slot worth renaming and watchpointing
- one helper worth pseudocode cleanup
- one dispatcher exit family worth decompiling carefully
- one narrowed handler bucket for further reconstruction

If the result is just a nicer dispatcher diagram, analyst payoff is still weak.

## Suggested KB contribution
Create a concrete workflow note centered on:
- flattened/dispatcher-heavy regions
- reduction from dispatcher recognition to the first durable state edge
- compare-run alignment around one state object or helper output
- reconnecting the result back to one smaller static target

## Compact operator framing
```text
dispatcher / flattened churn is already visible
  -> pick one late effect
  -> mark one dispatcher window
  -> identify one reduction helper or state object
  -> localize first consequence-bearing state edge
  -> prove one downstream effect
  -> return to static work with one smaller target
```

## Retention note
- No large datasets or binaries retained.
- This note is a compact practical consolidation intended to support immediate KB improvement in an underdeveloped deobfuscation branch.
