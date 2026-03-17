# Source Notes — iOS practical branch sequencing

Date: 2026-03-17
Purpose: support a KB-maintenance pass that improves the *routing and handoff logic* of the iOS practical branch without creating another abstract mobile taxonomy page.

## Scope
This note does not add a new iOS reversing theory.
It consolidates what the KB now already knows after the recent iOS practical additions and turns that into one clearer practical sequencing claim:

- the iOS branch now has three concrete entry notes
- they cover a real analyst progression rather than three unrelated pages
- the highest-value maintenance move now is to make that progression more explicit in navigation and parent pages

The practical sequence is:

```text
iOS-shaped case
  -> first broad environment / packaging / realism gate unclear
  -> first decisive owner across ObjC / Swift / native layers unclear
  -> visible callback / result material exists, but first behavior-changing policy state still unclear
```

Mapped to current notes:

```text
ios-packaging-jailbreak-and-runtime-gate-workflow-note
  -> ios-objc-swift-native-owner-localization-workflow-note
  -> ios-result-callback-to-policy-state-workflow-note
```

## Supporting KB signals reused here

### 1. The first iOS note is genuinely a gate-triage entry note
From:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `sources/mobile-runtime-instrumentation/2026-03-16-ios-packaging-jailbreak-runtime-gate-notes.md`

High-signal points reused here:
- the main early bottleneck is often not "bypass jailbreak detection" generically
- the analyst first needs to separate packaging/resign drift, jailbreak probes, instrumentation visibility, realism drift, and later trust/session consequences
- the practical success condition is one representative flow, one compare pair, one first divergence boundary, and one proved gate family

Why it matters:
- this page is already the correct first iOS routing surface when the case still has broad environment uncertainty
- the branch should present it explicitly as the *first* note, not merely as one related note among peers

### 2. The second iOS note is a real post-gate ownership bridge
From:
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`
- `sources/mobile-runtime-instrumentation/2026-03-17-ios-objc-swift-native-owner-localization-notes.md`

High-signal points reused here:
- once the case is reachable enough to study, the bottleneck often becomes ownership rather than visibility
- selectors, Swift wrappers, and native helpers may all look plausible while none is yet proved as the first consequence-bearing owner
- the useful reduction is trigger -> reducer -> worker -> owner -> effect

Why it matters:
- this page already functions as the middle iOS bridge between broad gate triage and narrower downstream tasks
- the KB should say more directly that this is the *second* note after broad iOS gate diagnosis is complete enough

### 3. The third iOS note is a narrower result-to-policy handoff note
From:
- `topics/ios-result-callback-to-policy-state-workflow-note.md`
- `sources/mobile-runtime-instrumentation/2026-03-17-ios-result-callback-to-policy-state-notes.md`

High-signal points reused here:
- callback visibility is not yet behavioral ownership
- the useful reduction is callback -> normalization -> policy mapping -> first behavior-changing consumer -> later effect
- this note is narrower than broad owner-localization because it assumes callback/result surfaces already exist

Why it matters:
- this page is not just another iOS note; it is the practical continuation once owner-localization narrows into result consequence proof
- the branch should present it explicitly as the *third* note in the common iOS ladder

## Distilled maintenance claim
The iOS practical branch is now strong enough that the next high-value move is not another sibling page.
It is to make the existing route more explicit:

```text
1. Is the first blocker still broad iOS setup / gate uncertainty?
   -> ios-packaging-jailbreak-and-runtime-gate-workflow-note

2. Is the case now reachable, but the first consequence-bearing ObjC / Swift / native owner still unclear?
   -> ios-objc-swift-native-owner-localization-workflow-note

3. Is callback/result visibility already present, but the first behavior-changing policy state still unclear?
   -> ios-result-callback-to-policy-state-workflow-note
```

## Operator-facing handoff rules to preserve
- Do not skip from broad iOS gate uncertainty directly into callback-mapper work if the true owner is still unclear.
- Do not keep the owner-localization note open once the path has clearly narrowed into callback/result consequence reduction.
- Do not treat callback visibility as a reason to bypass gate triage; visible callbacks can still exist in a drifted or only partially trustworthy setup.
- When the iOS branch is described at parent/index level, prefer explicit *ordered routing* over a flat file list.

## Candidate canonical KB changes supported by this note
This note most directly supports improvements to:
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `index.md`

It also justifies small route-clarification edits in:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`
- `topics/ios-result-callback-to-policy-state-workflow-note.md`

## Bottom line
The iOS practical branch does not currently need another sibling topic page as much as it needs stronger route clarity.
The highest-value maintenance move is to make the existing three-note chain read like an operator ladder:
- broad gate diagnosis first
- post-gate owner localization second
- callback/result-to-policy consequence proof third
