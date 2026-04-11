# Protected-runtime lower-surface vs richer user-space uncertainty-reduction notes

Date: 2026-04-12
Branch target: protected-runtime practical workflows / observation-topology comparison
Purpose: preserve a source-backed operator refinement for the case where one lower-surface boundary is already available, one richer user-space posture is also available or tempting, and the remaining question is which one actually reduces uncertainty more honestly.

## Search artifact
Raw multi-source search artifact:
- `sources/protected-runtime/2026-04-12-0450-lower-surface-vs-user-space-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed source behavior for this run:
- Exa returned usable official Frida, DynamoRIO, and Linux-kernel documentation surfaces
- Tavily returned usable overlapping official documentation surfaces and snippets
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` errors through the configured proxy path

## Retained official source anchors
1. Frida Gadget
   - `https://frida.re/docs/gadget/`
2. Frida Stalker
   - `https://frida.re/docs/stalker/`
3. DynamoRIO Code Manipulation API
   - `https://dynamorio.org/API_BT.html`
4. DynamoRIO profiling guidance
   - `https://dynamorio.org/page_profiling.html`
5. Linux uprobe tracer
   - `https://docs.kernel.org/trace/uprobetracer.html`
6. Linux seccomp filter documentation
   - `https://docs.kernel.org/userspace-api/seccomp_filter.html`

## High-signal retained findings

### 1. Earlier user-space posture buys reach, not automatic truth
Frida Gadget is explicitly designed for cases where injected mode is not suitable and can start from a constructor-time load path. It can block on load for early instrumentation. That is real posture improvement.

But the same documentation also reminds us that the chosen posture changes the evidence model:
- Gadget is still a deliberate in-process instrumentation presence
- its configuration changes when and how the program resumes
- on jailed iOS, `code_signing=required` disables the Interceptor API, so “earlier user-space access” and “same user-space capabilities” are not the same thing

Operator consequence:
- better user-space reach is not yet proof that the current question is answered more honestly

### 2. Rich thread/code tracing improves visibility while still carrying cost and distortion risk
Frida Stalker documentation is unusually explicit that it can capture every function, every basic block, even every instruction, and that this is inherently expensive.

DynamoRIO’s Code Manipulation API and profiling documentation reinforce the same practical point from a different instrumentation family:
- DBI/code-cache tooling can expose the actual executing code stream and hot fragments
- the instrumentation system has measurable hotspots and overhead worth profiling

Operator consequence:
- richer user-space traces may be exactly right when control structure is the missing object
- but “I can see much more now” is still weaker than “the decisive uncertainty shrank”

### 3. Lower surfaces are narrower truth objects, not universal replacements
Linux uprobe tracing and seccomp-filter documentation are useful because they are explicit about what they *do* and what they *do not* mean.

Useful operator implications:
- uprobes give a narrow event surface at `PATH:OFFSET`, optional fetched arguments, and per-event hit counts
- seccomp filters operate on syscall number/arguments and can drive TRAP/TRACE/USER_NOTIF outcomes
- seccomp docs explicitly warn that seccomp is not a full sandbox and should not be overread into a complete behavior model

Operator consequence:
- lower surfaces can answer one boundary question more directly
- they often preserve less semantic carry-forward than richer user-space visibility
- that tradeoff has to be judged by the current uncertainty, not by tool ideology

### 4. The real compare question is “which uncertainty moved,” not “which tool is lower”
The retained docs together support a sharper comparison rule:
- earlier or richer user-space instrumentation changes reach and detail
- lower surfaces change boundary truth and often reduce some observer-shaped distortion
- neither choice is automatically superior without a bounded question and a same-trigger compare slice

## Practical synthesis worth preserving canonically
A compact compare ladder for this seam is:

```text
same trigger compared
  != lower surface exists
  != lower surface reduced uncertainty more than richer user-space visibility
  != lower surface preserved enough semantic meaning for the next handoff
  != richer user-space alternative is now unnecessary
  != smaller next target recovered
```

A second compact reminder worth preserving is:

```text
visibility improved
  != question answered
  != distortion reduced
  != semantic carry-forward preserved
  != next target recovered
```

These splits keep analysts from overreading:
- early Gadget posture
- heavy Stalker / DBI visibility
- one syscall-adjacent event hit
- one seccomp policy observation

as if any of those alone already proved the best topology choice.

## Best KB use of this material
This material is best used to create a narrower compare-heavy continuation under the existing protected-runtime observation-topology note.

It should *not* become:
- a broad Frida vs DBI vs eBPF tooling page
- a generic anti-instrumentation taxonomy restatement
- a claim that lower surfaces are always more truthful

The durable operator value is narrower:
- compare the same trigger under one richer user-space posture and one lower-surface posture
- ask which one removed the actual uncertainty
- ask whether the lower surface still preserved enough semantic meaning to hand back one smaller next target
- keep “pair both surfaces” available when one lower boundary proves the event but one user-space slice is still needed for owner/consumer semantics

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source result.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked; its failure is recorded clearly.
