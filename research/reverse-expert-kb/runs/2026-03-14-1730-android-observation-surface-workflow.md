# Run Report — 2026-03-14 17:30 Asia/Shanghai

## Focus
Continue converting the mobile / protected-runtime subtree into a practical analyst playbook by adding an operational note for alternative Android observation-surface selection.

This run focused on the gap between:
- having a synthesis page that says linker / Binder / eBPF observation matters
- actually knowing how to choose the next surface in a live protected-runtime case

## What was added
### New concrete workflow note
- `topics/android-observation-surface-selection-workflow-note.md`

This page adds a practical workflow centered on:
- naming the missing evidence before switching surfaces
- choosing among linker / loader, Binder, eBPF / seccomp / SVC, and targeted trace / DBI based on evidence type
- defining one narrow observation slice tied to one app action
- reconnecting lower-layer events to app action, protocol role, state transition, or later consequence
- compare-run evaluation of whether a lower surface is actually better, not merely lower
- failure diagnosis for “lower but not more useful” workflows

## Navigation updates
Updated:
- `index.md`
- `topics/mobile-protected-runtime-subtree-guide.md`

These updates make the mobile subtree’s new concrete-note layer more explicit, especially for the “observability under resistance” branch.

## Why this matters
The KB had already become much stronger on:
- signature / preimage recovery
- challenge / verification-loop analysis

But the practical question of **how to choose the next observation surface when hooks fail** was still under-specified.

This run helps close that gap by adding a decision-oriented workflow note rather than another generic page about Android internals.

The mobile subtree now has a clearer three-part practical shape:
- request-shaping and signature recovery
- challenge / verification-loop analysis
- observation-surface selection under protection pressure

## Follow-up directions
Natural next steps from here:
1. add a practical environment-differential diagnosis workflow note for protected mobile targets
2. add a more concrete eBPF / seccomp / SVC tracing note if that branch keeps growing
3. continue this paired pattern elsewhere: synthesis page + concrete workflow note

## Files changed
- `research/reverse-expert-kb/topics/android-observation-surface-selection-workflow-note.md`
- `research/reverse-expert-kb/index.md`
- `research/reverse-expert-kb/topics/mobile-protected-runtime-subtree-guide.md`
