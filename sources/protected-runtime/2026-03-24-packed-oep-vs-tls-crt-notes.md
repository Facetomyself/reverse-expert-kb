# Source notes — packed OEP vs TLS / CRT / staged-startup handoff

Generated: 2026-03-24 01:27 Asia/Shanghai

## Focus
Strengthen the KB’s protected-runtime / deobfuscation practical branch with a narrower continuation inside the packed-startup workflow:
- the analyst already has a plausible post-unpack jump or handoff
- but Windows startup reality means **TLS callbacks**, **language/CRT startup**, or a **secondary loader stage** may still execute before the first payload/business-logic region worth treating as the real handoff target
- the practical question is therefore not only “where is OEP?” but also “which boundary is late enough to count as a reusable post-unpack handoff for the actual payload I care about?”

This note is intentionally workflow-centered and source-backed.
It is meant to materially sharpen an existing KB workflow note rather than create another broad packer taxonomy.

## Source base used
### Multi-source search
- `sources/protected-runtime/2026-03-24-packed-oep-vs-tls-crt-search-layer.txt`
  - explicit `search-layer` run with `--source exa,tavily,grok`

### Pages fetched and used directly
- Raymond Chen, “WinMain is just the conventional name for the Win32 process entry point”
  - `https://devblogs.microsoft.com/oldnewthing/20110525-00?p=10573`
- Ring Zero Labs, “Analyzing TLS Callbacks”
  - `https://www.ringzerolabs.com/2019/08/analyzing-tls-callbacks.html`
- Kyle Cucci, “Unpacking StrelaStealer”
  - `https://securityliterate.com/unpacking-strela-stealer/`
- Kaimi, “Developing PE file packer step-by-step. Step 6. TLS”
  - `https://kaimi.io/en/2012/09/developing-pe-file-packer-step-by-step-step-6-tls/`
- ReverseEngineering Stack Exchange, “Real PE32(+) entry point - is it documented anywhere?”
  - `https://reverseengineering.stackexchange.com/questions/6905/real-pe32-entry-point-is-it-documented-anywhere/6912`
- Search result/snippet support for:
  - Black Hat / Yason “The Art of Unpacking”
  - Vuksan “Fast & Furious reverse engineering”

### Fetch failure recorded
- `https://blackhat.com/presentations/bh-usa-07/Yason/Whitepaper/bh-usa-07-yason-WP.pdf`
  - `web_fetch` returned a 403 / interstitial, so I only used search-layer snippet evidence for that source family in this run

## High-signal extracted patterns

### 1. “Raw PE entry point” is not the same thing as “first payload code I should care about”
Raymond Chen’s explanation and the RE Stack Exchange discussion both reinforce a basic but operationally important distinction:
- the PE entry point the loader calls is a **raw startup point**
- language runtime / CRT startup can then do substantial work before `WinMain`, `main`, or other user-facing logic
- therefore even in ordinary programs, “entry point” and “the first code I really care about” are already not the same thing

Protected or packed targets amplify this mismatch:
- the first post-unpack transfer can still land in CRT/runtime startup
- that startup may still perform module init, cookie setup, constructor runs, TLS-related work, and helper-controlled dispatch before payload logic appears
- so a dramatic transfer is often only “late enough to leave the stub,” not yet “late enough to be the most useful payload handoff”

Practical consequence:
- in packed targets, the analyst should treat **OEP**, **raw post-unpack transfer**, and **first payload/business-logic handoff** as related but separable boundaries

### 2. TLS callbacks are a recurring reason analysts stop too early
Ring Zero Labs and multiple search-layer hits reinforce the same practical warning:
- TLS callbacks run **before the traditional entry point**
- malware and packers use them for anti-debugging, polymorphic setup, decryption, unpacking, or early anti-analysis work
- a debugger that only breaks at the ordinary entry point can therefore miss meaningful earlier startup work entirely

This matters for the existing KB workflow because a simple “break at EP, follow the jump, call that OEP” recipe is too weak when TLS callbacks are in play.

Practical consequence:
- if the file or loaded image shows TLS callback presence, the analyst should explicitly ask whether the candidate boundary is:
  - before TLS-owned work
  - after TLS-owned work but before CRT/user startup settles
  - or after both, at the first ordinary payload consumer

### 3. Packers/loaders may preserve, fake, or re-stage TLS behavior, so “post-unpack transfer” can still be only a startup-management boundary
Kaimi’s packer-development write-up is especially useful because it shows the loader-facing mechanics rather than just analyst folklore:
- a packer that wants correct runtime behavior may need to preserve TLS-related state
- TLS callback arrays may be rewritten, staged, or proxied
- the unpacker may manually execute original callbacks and then rewrite callback arrays so later loader behavior remains coherent

This is a strong practical reminder that:
- the handoff after unpacking may still be a **runtime-correctness boundary** rather than the **best payload-analysis boundary**
- “I landed after decryption” is not yet enough if TLS callback replay, runtime init obligations, or callback-array repair still sit between the analyst and the first stable payload object

### 4. Real unpacking casework already shows analysts skipping TLS to reach the useful payload boundary
The StrelaStealer write-up is a very useful operator example:
- TLS callbacks are present and hit first
- the analyst intentionally runs past them for the immediate unpacking goal
- the useful breakpoint is chosen near the end of deobfuscation / transfer preparation, not merely “at EP”
- the real success criterion is a new memory region and dumped payload whose strings/import behavior are materially more ordinary

This is exactly the KB’s preferred proof style:
- not “a jump happened”
- but “a later region became stable enough, ordinary enough, and reusable enough to dump and continue statically”

Useful transfer rule:
- when TLS exists, do not argue abstractly about whether TLS is “important” in general
- ask whether your current objective is:
  - understanding the protector’s early anti-analysis/setup behavior, in which case TLS may be the real target
  - or obtaining a reusable post-unpack payload target, in which case TLS may be a stage to traverse rather than the right stopping point

### 5. The right proof object is often “first payload-bearing post-startup consumer,” not “formal OEP”
Across the Windows-startup and TLS sources, the recurring practical lesson is:
- raw entry point is a loader contract
- CRT startup is a language/runtime contract
- TLS callbacks are a loader-invoked early-init contract
- the analyst often cares about a different object: the **first payload-bearing consumer** or **first ordinary module/object/import cluster after startup machinery quiets down**

That suggests a sharper operator ladder for packed Windows targets:

```text
stub / decrypt / fixup visibility
  -> raw post-unpack transfer candidate
  -> TLS-owned startup work? (yes/no)
  -> CRT/runtime startup work? (yes/no)
  -> first stable post-startup payload consumer
  -> reusable dump / module / object / consumer target
```

### 6. Good stop rules are “startup-normalization aware”
The practical stop rule that emerges is:
- if the current boundary still looks dominated by callback replay, constructor/init tables, CRT normalization, import repair, or loader-owned startup scaffolding, do **not** overclaim that you have reached the best payload handoff yet
- stop the packed-startup workflow only when one of these becomes true:
  - a dumped image is stable and ordinary enough for real static work
  - one first real import/module/object/consumer persists beyond TLS/CRT/startup scaffolding
  - later business/payload logic clearly depends on the chosen handoff rather than only on startup machinery

## Suggested KB contribution
Sharpen `topics/packed-stub-to-oep-and-first-real-module-workflow-note.md` with a narrower subcase for:
- TLS callbacks before the visible entry point
- CRT/runtime startup after the first raw transfer
- the practical distinction between:
  - raw entry point
  - raw post-unpack transfer
  - first payload-bearing post-startup handoff

The update should preserve the KB’s practical style:
- case-driven
- consequence-oriented
- stop-rule based
- biased toward a reusable dump/module/consumer handoff rather than ceremony about formal OEP naming

## Compact operator framing
```text
packed startup looks nearly solved
  -> ask whether TLS or CRT startup still owns the next few transitions
  -> distinguish raw post-unpack transfer from first payload-bearing handoff
  -> prove one post-startup import/module/object/consumer anchor
  -> stop only when the target is reusable for ordinary static follow-up
```

## Retention note
- No binaries retained.
- This note is a compact, source-backed continuation intended to deepen an underfed practical seam in the protected-runtime / deobfuscation branch rather than add another broad canonical sync pass.
