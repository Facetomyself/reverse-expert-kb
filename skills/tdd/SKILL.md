---
name: tdd
description: "Use red-green-refactor development for features or fixes, especially when tests, seams, or integration behavior matter."
homepage: "https://github.com/mattpocock/skills"
license: "MIT"
---

# TDD

Use when building features or fixes test-first, adding regression coverage, or the user mentions TDD/red-green-refactor.
Adapted from `mattpocock/skills`; upstream reference is in `references/upstream-tdd.md`.

## Core loop

Red → green → review/refactor.

- Red: write one failing test for one behavior at one public seam.
- Green: implement only enough production code to pass that test.
- Review/refactor: after behavior is green, improve shape without changing behavior.

## Good tests

Good tests verify observable behavior through public interfaces, not private implementation details.
They read like a specification and survive refactors.

Avoid:

- implementation-coupled tests: private methods, internal collaborators, side-channel assertions
- tautological tests: expected value computed the same way as the implementation
- snapshot sprawl without meaningful assertions
- horizontal slicing: writing many speculative tests before learning from the first green slice

Use independent expected values: known-good literals, worked examples, fixtures from the spec, captured real payloads, or documented protocol behavior.

## Seams and user-confirmation policy

A seam is the boundary where behavior is observed: public function, CLI, HTTP route, UI flow, queue consumer, database-visible transaction, or integration contract.

Default for this OpenClaw environment:

- If the seam is obvious and low-risk, choose it, state the assumption briefly, and proceed.
- Ask the user only when multiple seams imply materially different architecture, cost, or risk.
- For external/destructive systems, use fixtures, mocks at service boundaries, or a safe staging loop unless explicitly authorized.

## Working rules

- One slice at a time: one seam, one behavior, one minimal implementation.
- Run the targeted test frequently.
- Run typecheck/lint or nearby suites as the change grows.
- Do not add speculative features for tests not yet written.
- Prefer integration-level coverage for behavior that depends on wiring.
- Mock only at true external boundaries: network services, clocks, randomness, payment/email/SMS, expensive third-party systems.
- If a bug has no good test seam, say so; that is an architecture finding.

## Completion standard

Before claiming done, provide evidence:

- failing test was created or existing red loop identified
- targeted test now passes
- meaningful broader gate ran when feasible
- any skipped gate has a reason

See `references/tests.md` and `references/mocking.md` when test quality or mocking policy is the hard part.
