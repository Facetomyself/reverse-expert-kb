# Source notes — packed startup payload handoff after TLS / CRT / startup normalization

Generated: 2026-03-24 20:20 Asia/Shanghai

## Focus
This run revisited the packed-startup seam as a real external-research-driven pass rather than a pure internal sync.

The practical question was narrow:
- the analyst already has a plausible unpacking transfer or OEP-like jump
- but Windows startup reality can still place TLS callbacks, CRT/language startup, security-cookie/runtime setup, constructor/init-table work, or callback-array repair between that transfer and the first payload/business-logic region worth treating as the real handoff target
- the KB therefore benefits from preserving a sharper three-boundary rule:
  - raw PE entry point
  - raw post-unpack transfer
  - payload-bearing post-startup handoff

## Search artifact
- `sources/protected-runtime/2026-03-24-packed-startup-payload-handoff-search-layer.txt`
  - explicit `search-layer` run with `--source exa,tavily,grok`

## Directly fetched pages retained
- Raymond Chen, `WinMain is just the conventional name for the Win32 process entry point`
  - useful for the operational distinction between raw entry and language/runtime startup
- Ring Zero Labs, `Analyzing TLS Callbacks`
  - useful for preserving that TLS callbacks execute before the traditional entry point and are routinely used for anti-analysis/unpacking work
- Kyle Cucci, `Unpacking StrelaStealer`
  - useful as a practical case where TLS callbacks are present but the actual unpacking goal is a later breakpoint and a later dumped payload region
- Kaimi, `Developing PE file packer step-by-step. Step 6. TLS`
  - useful because it preserves loader/packer-side mechanics: callback arrays can be staged, replayed, or rewritten, so a post-unpack transfer may still be startup-management truth rather than payload truth

## High-signal retained points

### 1. Raw entry is already not the same as user-facing logic
Raymond Chen is enough to preserve a conservative operator reminder:
- the OS calls a raw process entry
- language/CRT startup may still do meaningful setup before `WinMain`, `main`, or other user-facing logic
- therefore a reverse analyst should not collapse `entry point` and `first code I actually care about` into the same object by default

### 2. TLS callbacks are an execution-before-EP family, not trivia
Ring Zero Labs reinforces the practical consequence:
- TLS callbacks can execute before the traditional entry point
- malware/protected targets use them for anti-analysis, unpacking, decryption, and obfuscation
- so “break at EP and follow the jump” is not a strong enough stop rule when TLS is in play

### 3. Pack/unpack correctness may preserve or replay TLS machinery
Kaimi is useful not because every real target behaves exactly the same, but because it preserves a real implementation family:
- packers may need to preserve TLS state, stage dummy callbacks, manually run original callbacks, then rewrite callback arrays
- this means a post-unpack transfer can still be dominated by runtime-correctness work rather than payload/business logic
- operationally, that supports treating callback replay / array repair as startup proof, not automatically payload proof

### 4. Real unpacking practice often wants a later, reusable payload boundary
The StrelaStealer write-up is a good operator anchor:
- TLS callbacks are visible first
- but for the immediate unpacking goal, the analyst intentionally runs past them
- the useful target is a later call / new memory region / dump boundary whose strings and imports become materially more ordinary
- this matches the KB’s preferred proof style: one reusable post-startup payload target, not just one dramatic jump

## Practical operator rule preserved this run
Use a startup-normalization-aware ladder:

```text
raw PE entry point
  -> raw post-unpack transfer
  -> TLS-owned work? / CRT-owned work? / constructor or callback-array repair still dominating?
  -> first payload-bearing post-startup handoff
  -> reusable dump / module / object / consumer target
```

Stop rule:
- if the next region is still mostly TLS callback replay, CRT/language startup, security-cookie/runtime normalization, constructor/init-table dispatch, or callback-array repair, record the current boundary only as a raw post-unpack transfer candidate
- only upgrade it to the payload-bearing handoff when one downstream import/module/object/consumer anchor remains useful after startup obligations quiet down

## KB contribution this note supports
This run should sharpen canonical routing, not create another detached taxonomy page.

The best contribution is therefore:
- refine `topics/packed-stub-to-oep-and-first-real-module-workflow-note.md` with an explicit three-boundary startup-normalization check
- reinforce the same distinction in `topics/protected-runtime-practical-subtree-guide.md`

## Retention note
- This note is workflow-centered and conservative.
- It exists to preserve a thinner practical seam in the deobfuscation / protected-runtime branch.
