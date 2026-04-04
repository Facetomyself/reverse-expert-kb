# TLS Callback to First Payload Consumer Workflow Note

Topic class: concrete workflow note
Ontology layers: protected-runtime practical workflow, packed/bootstrap startup truth, TLS callback ownership, first payload-bearing consumer proof
Maturity: practical
Related pages:
- topics/protected-runtime-practical-subtree-guide.md
- topics/packed-stub-to-oep-and-first-real-module-workflow-note.md
- topics/decrypted-artifact-to-first-consumer-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md
Related source notes:
- sources/protected-runtime/2026-04-04-tls-callback-first-payload-consumer-notes.md

## 1. Why this note exists
The packed/bootstrap branch already preserves an important stop rule:

```text
raw_entry != pre_entry_startup != unpack_transfer != payload_handoff != consumed
```

But in Windows-native packed/protected cases there is a thinner recurring seam after that reminder:
- the analyst already suspects the ambiguity is specifically **TLS-callback-owned startup work**
- broad OEP naming is no longer the real question
- the next useful output is one **TLS callback -> first payload-bearing consumer** proof object

The overclaim this note prevents is:

```text
TLS callbacks exist
  == this callback owns the interesting behavior
  == this is already payload proof
```

The smaller truthful ladder is:

```text
TLS directory / callback array exists
  != callback replay truth for this run
  != this callback owns the startup work that matters
  != startup-owned callback body has handed off to payload-bearing code
  != first payload-bearing consumer truth
```

## 2. When to use this note
Use this note when most of these are true:
- the case is Windows/native enough that PE/TLS startup surfaces are relevant
- the broad packed-stub / OEP handoff has already been reduced enough to say “the remaining ambiguity is now TLS-callback-shaped”
- a callback array or TLS structure is already visible statically or dynamically
- the analyst needs one smaller proof object showing where TLS-owned startup stops and payload-bearing work actually begins

Do **not** use this note when:
- the main uncertainty is still the broad post-unpack handoff or dump boundary (use the packed-stub note)
- runtime tables / constructors / CRT startup remain equally plausible and TLS is not yet the best discriminant
- the first readable artifact already exists and the real missing edge is its ordinary consumer

## 3. Conservative doc-backed anchors
From PE / TLS references retained this run:
- the PE format includes a `.tls` section and TLS-related initialization data
- TLS structures include callback routines for per-thread initialization / termination
- the TLS directory exposes an `AddressOfCallbacks`-style callback array concept
- callbacks are part of startup-time behavior and can run before the analyst’s nominal main-entry expectation

Operator consequence:
- static TLS callback presence is weaker than proving one callback actually replayed in the run you care about
- proving one callback replayed is still weaker than proving that callback is the first payload-bearing consumer

## 4. Boundary objects to keep separate
### A. TLS structure truth
Freeze:
- whether the image really has TLS structures / callback entries
- one callback pointer or array slot identity

### B. Callback replay truth
Ask:
- did this callback actually execute in the run that matters?
- was the observed work owned by this callback or by adjacent startup scaffolding?

### C. Startup-owned truth
Even if the callback replayed, the body can still be mostly:
- CRT/runtime normalization
- constructor/init-table dispatch
- import/loader cleanup
- environment/cookie setup
- other startup-managed work

### D. Payload-bearing handoff truth
The stronger question is:
- what first consumer exists downstream of TLS-owned startup that actually carries payload-bearing state, parsing, config use, request shaping, or other ordinary target behavior?

## 5. Default workflow
### Step 1: freeze one callback object, not “all TLS callbacks”
Pick one representative callback pointer/slot.
Do not widen to every callback in the array unless the case forces it.

### Step 2: separate presence from replay
Write the smaller ladder explicitly:

```text
callback listed
  -> callback replayed
  -> callback-owned startup work
  -> payload-bearing handoff
  -> first payload consumer
```

This prevents stopping at `.tls` inventory.

### Step 3: test whether the callback is still only startup proof
If the region downstream is still dominated by:
- runtime normalization
- constructor replay
- import/repair cleanup
- other scaffolding

then record **startup proof**, not **payload proof**.

### Step 4: look for one handoff out of TLS-owned startup
The useful unit is one handoff such as:
- one call into ordinary parser/config/request logic
- one write that makes a real artifact consumable
- one transfer into a first real module/object family
- one consumer routine that survives compare-runs better than the callback body itself

### Step 5: stop at one first payload-bearing consumer
Do not force the full unpacking story.
One callback -> one handoff -> one first payload-bearing consumer is enough.

## 6. Practical failure patterns this note prevents
- “TLS callback array present, therefore that explains the protected behavior”
- “I landed in a TLS callback, so I found the real entry”
- “callback replay proved payload ownership”
- “the first post-callback code block is automatically payload, not startup normalization”

## 7. Sources
See: `sources/protected-runtime/2026-04-04-tls-callback-first-payload-consumer-notes.md`

Primary references:
- https://learn.microsoft.com/en-us/windows/win32/debug/pe-format
- https://learn.microsoft.com/en-us/cpp/build/reference/tls?view=msvc-170
- https://learn.microsoft.com/en-us/archive/msdn-magazine/2002/march/inside-windows-an-in-depth-look-into-the-win32-portable-executable-file-format-part-2
