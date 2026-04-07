# Targeted Evidence Trust Calibration

Topic class: concrete workflow note
Ontology layers: browser practical workflow, evidence discipline, anti-bot/debugger analysis support
Maturity: practical
Related pages:
- topics/browser-runtime-subtree-guide.md
- topics/cdp-side-effect-and-automation-signal-analysis.md
- topics/browser-environment-reconstruction.md
- topics/browser-debugger-detection-and-countermeasures.md
- topics/trust-calibration-and-verification-burden.md
- topics/runtime-evidence-package-and-handoff-workflow-note.md
- topics/analytic-provenance-and-evidence-management.md

## 1. When to use this note
Use this note when a browser reverse-engineering case already has **some** evidence about a token path, challenge trigger, automation signal, request builder, or state transition, but the analyst still cannot tell which part is trustworthy enough to act on next.

Typical entry conditions:
- one hook, trace, CDP snapshot, compare pair, or intercepted request already looks useful
- several candidate explanations exist, but not all evidence slices deserve equal trust
- the current risk is no longer “I have no evidence,” but “I may overread the evidence I do have”
- the next useful move depends on deciding which small claim is strong enough to drive the next hook, replay, or environment repair

Use it for cases like:
- one token-generation trace exists, but it is unclear whether it proves preimage ownership, finalization ownership, or only one late wrapper step
- one CDP/debugger compare pair exists, but it is unclear whether it proves target-consumed automation signal or only analyst-induced side effect
- one request snapshot or cookie mutation exists, but it is unclear whether it proves first consumer, delayed consequence, or only transient intermediate state
- one challenge difference is visible across runs, but several competing causes still fit the evidence

Do **not** use this note when:
- the current problem is still broad evidence collection and no representative slice exists yet
- the real bottleneck is still choosing an observation surface, not deciding how much to trust a current result
- one claim is already strong enough and the next problem is now purely branch-specific execution, replay, or packaging work

## 2. Core claim
A common browser-analysis failure is not lack of evidence.
It is using evidence that is **real but too weak for the claim being made**.

The practical ladder is:

```text
evidence slice exists
  != evidence slice supports this exact claim
  != claim is strong enough to drive the next action
  != neighboring hypotheses are actually ruled out
  != broader mechanism is solved
```

This note exists to keep those steps separate.

## 3. What counts as a good target claim
A useful target claim is:
- small
- testable
- action-driving
- narrower than the full subsystem story

Good claims:
- this compare pair is strong enough to justify moving from CDP side-effect triage into environment reconstruction
- this trace slice is strong enough to say the final request body was already fixed before wrapper `X`
- this cookie/state mutation is strong enough to justify looking at delayed consequence rather than initial challenge trigger

Weak claims:
- this trace proves the anti-bot system
- this request snapshot solves signing
- this one debugger delta proves the whole automation model

## 4. Default workflow

### Step 1: Write the exact claim you want to support
Do not calibrate trust against a vague goal.
Write one exact next-use claim first.

Examples:
- “This evidence is strong enough to move the next hook earlier.”
- “This evidence is strong enough to stop blaming CDP and reopen environment mismatch.”
- “This evidence is strong enough to freeze one first consumer.”

### Step 2: Mark the evidence boundary
Freeze exactly what the evidence is:
- one compare pair
- one request snapshot
- one hook hit
- one storage mutation
- one callback delivery slice
- one DOM/runtime/worker event slice

Do not silently widen one small slice into a larger body of proof.

### Step 3: Separate four trust questions
1. **Observation trust**
   - did this event/value/state change really occur as observed?
2. **Boundary trust**
   - does it happen at the boundary you think it does, or only nearby?
3. **Causal trust**
   - is it strong enough to drive the next action, or only correlated?
4. **Exclusion trust**
   - what neighboring hypotheses are still alive?

A compact shorthand:

```text
observed
  != boundary-correct
  != action-driving
  != excluding neighbors
```

### Step 4: Prefer the smallest claim that changes the next move
The question is not “what is the biggest story I can tell?”
It is:
- what is the smallest trustworthy claim that changes what I do next?

That usually means choosing one of these:
- move earlier
- move later
- switch branch
- keep current branch
- package and hand off

### Step 5: Record what the evidence does **not** prove
Useful examples:
- “shows later state consequence, not first trigger”
- “shows wrapper entry, not preimage ownership”
- “shows side effect after CDP attach, not target-consumed automation signal”
- “shows candidate consumer, not exclusion of neighboring consumers”

This is often the difference between useful trust calibration and overclaim.

### Step 6: Choose the next action only after calibration
Good next actions after calibration:
- one earlier hook
- one compare repair
- one environment-normalization check
- one delayed-consequence follow-up
- one evidence package/handoff

Do not choose the next action just because the evidence exists.
Choose it because the evidence is strong enough for that specific move.

## 5. Practical scenario patterns

### Scenario A: Real trace, oversized claim
Pattern:

```text
one trace slice exists
  -> analyst is tempted to narrate the whole subsystem
  -> slice only supports one smaller boundary claim
  -> smaller claim is still enough to drive the next move
```

Best move:
- shrink the claim until the evidence is honestly action-driving

### Scenario B: Compare pair exists, but neighbors remain alive
Pattern:

```text
run A differs from run B
  -> one hypothesis looks attractive
  -> neighboring explanations still fit
  -> next action should reduce neighbors, not celebrate closure
```

Best move:
- record what the compare pair does not exclude yet

### Scenario C: Browser/CDP side effect is real, but target consumption is not proved
Pattern:

```text
CDP or DevTools changes behavior
  -> evidence of side effect is real
  -> target-consumed automation signal is still not proved
  -> next move depends on calibrating that distinction honestly
```

Best move:
- keep side-effect truth separate from target-consumption truth

## 6. What to record
Keep the evidence package bounded:
- exact claim being calibrated
- exact evidence slice
- what is directly observed
- what boundary it probably supports
- what it does not yet prove
- what next action it is strong enough to justify

## 7. Exit conditions and handoffs
Stay on this note while the main problem is still **how much to trust one current browser evidence slice for one specific next move**.

Leave once one of these is already good enough:
- one claim is strong enough to drive the next branch/hook/replay move
- one smaller evidence package is ready for handoff
- the main uncertainty has shifted back into branch-specific technical proof rather than trust calibration

Common next moves:
- `topics/cdp-side-effect-and-automation-signal-analysis.md`
- `topics/browser-environment-reconstruction.md`
- `topics/browser-parameter-path-localization-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/runtime-evidence-package-and-handoff-workflow-note.md`

## 8. Why this page exists
The browser subtree guide already advertised a targeted evidence-calibration seam, but the canonical leaf was missing.

This page repairs that gap by preserving one smaller practical ladder:

```text
evidence exists
  != supports this claim
  != strong enough for next action
  != excludes neighbors
```

That is the durable operator value here.
