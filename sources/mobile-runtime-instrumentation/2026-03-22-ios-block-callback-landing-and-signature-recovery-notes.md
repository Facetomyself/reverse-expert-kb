# iOS block callback landing and signature-recovery notes

Date: 2026-03-22
Topic area: iOS runtime instrumentation, arm64e/PAC-aware callback triage, block/callback landing confirmation
Confidence: moderate

## Why these notes were collected
The current iOS practical branch was already stronger on:
- broad setup/gate diagnosis
- owner localization across ObjC / Swift / native layers
- PAC-shaped callback/dispatch failure triage
- callback/result-to-policy-state reduction

What still felt thinner was a narrower, operator-facing continuation for the case where:
- one callback family is already plausible
- arm64e / dyld-cache truthfulness still matters
- blocks/closures are involved
- the analyst needs to prove whether the landing site and parameter shape are real enough before widening into policy or replay conclusions

These notes collect source-backed reminders that support a practical continuation page rather than another broad iOS summary.

## Source set used
- Apple Developer Documentation: "Preparing your app to work with pointer authentication"
  - https://developer.apple.com/documentation/Security/preparing-your-app-to-work-with-pointer-authentication
- ipsw dyld guide
  - https://blacktop.github.io/ipsw/docs/guides/dyld/
- Everett: "Print Block Parameter Signatures in Objective-C Methods Using lldb"
  - https://everettjf.github.io/2020/02/11/print-block-in-lldb/
- Damien Deville: "Block Debugging"
  - https://ddeville.me/2013/02/block-debugging/
- supporting search-layer result overlap from Exa / Tavily / Grok on arm64e + block/callback workflows

## New or reinforced findings

### 1. PAC should be treated as a truthfulness constraint, not only a bypass problem
The Apple PAC documentation is high-level, but it still reinforces the main practical point relevant to the KB:
- arm64e pointer authentication exists specifically to protect pointers against unexpected modification
- function pointers and similar control-flow-relevant pointers are part of that world
- therefore, on modern iOS, a callback or block invoke pointer that "looks callable" in a decompiler is not automatically a trustworthy replay or ownership boundary

Useful KB translation:
- PAC pressure is often a reason to downgrade confidence in a code view or guessed callback landing, not a reason to overclaim about anti-analysis immediately
- in practice, this supports the existing branch rule that modern iOS callback/dispatch failures should first be classified conservatively as:
  - wrong family
  - wrong context / missing obligation
  - lying code view / dyld-cache truth problem
  - replay-close but still missing one runtime obligation

### 2. dyld shared cache truth matters directly for callback landing work
The `ipsw dyld` guide reinforces several points useful for operator workflow:
- modern iOS arm64e work is often based on dyld shared cache rather than simple standalone frameworks
- the cache contains mapped `__TEXT`, `__DATA`, `__AUTH`, and `__LINKEDIT` regions whose relationships matter when reasoning about callback pointers and imported/runtime-owned objects
- prebuilt loader / closure information in newer iOS generations is part of the truthful runtime picture
- extracting and inspecting cache-backed images with a toolchain that preserves arm64e context is not optional housekeeping; it is part of keeping the code view honest

Useful KB translation:
- when a callback/block landing looks strange, unmapped, or inconsistently symbolized, first ask whether the current view is cache-truthful enough
- do not jump from "odd disassembly" to "hard anti-debug" if the dyld/cache view itself may still be lying

### 3. Block debugging material gives a practical way to confirm parameter shape
The Everett LLDB article contributes a concrete operator value:
- when class-dump or header-derived signatures reduce callback parameters to `CDUnknownBlockType`, LLDB-side block inspection can recover useful parameter shape
- the practical move is not merely "hook more" but:
  - stop near the message send / call site that passes the block
  - capture the block object address
  - inspect block signature / type encodings from the runtime side
- the point is to convert a vague callback placeholder into a narrower contract you can compare against observed landing behavior

Useful KB translation:
- for iOS callback localization, a block's runtime signature can be a better next proof object than another static guess about surrounding wrappers
- this is especially helpful when deciding whether the visible block is:
  - the real policy-bearing callback
  - just an adapter / wrapper
  - mismatched to the path you are trying to replay

### 4. The older block-debugging explanation still supports the structural model
The Damien Deville article is old and x86_64-oriented, but it still reinforces two transferable ideas:
- a block is structurally a callable object with an invoke pointer plus captured context
- message-send / call-site argument reasoning is the bridge between "I see a block object" and "I know which call edge actually transfers control into it"

Useful KB translation:
- even though the exact register details differ on modern iOS arm64e, the important reasoning pattern persists:
  - distinguish the block object from the invoke target
  - distinguish the call site that passes the block from the later site that invokes it
  - do not confuse block presence with proof that the current landing path is the one changing behavior

## Synthesis for the KB
These sources support a narrower practical continuation page with this core claim:
- once a modern iOS case has already narrowed into one plausible callback/block family, the next useful move is often to prove one truthful landing boundary and one usable parameter contract before widening back into owner, policy, or replay claims

That continuation should preserve four practical reminders:
1. PAC is part of why callback views can lie
2. dyld cache truthfulness is part of callback-landings truthfulness
3. block signature recovery is a practical tactic for reducing callback ambiguity
4. the real proof object is the first truthful landing boundary plus one downstream effect, not every wrapper or block-shaped object nearby

## Likely canonical landing spot
These notes support a narrower iOS practical note that sits between:
- `topics/arm64e-pac-and-mitigation-aware-ios-reversing.md`
- `topics/ios-pac-shaped-callback-and-dispatch-failure-triage.md`
- `topics/ios-result-callback-to-policy-state-workflow-note.md`

It should not replace those pages.
It should act as a thinner continuation for the case where callback/block landing truth is the real missing proof object.

## Limits / caution
- The Apple PAC page is high-level and not a low-level reversing manual.
- The block-debugging sources are partly old and not arm64e-specific.
- The value here is workflow support and conservative operator heuristics, not a claim that these sources alone explain all modern iOS callback internals.

## Suggested canonical takeaway
Keep this as a practical rule:
- when a callback/block family looks plausible on modern iOS, first prove the code view is dyld/cache-truthful enough and the block/closure signature is narrow enough, then prove one landing boundary and one effect
- do not widen immediately into policy-state claims or replay-failure claims while the landing itself is still structurally ambiguous
