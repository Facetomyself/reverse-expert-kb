# Protected-runtime topology-selection lower-surface notes

Date: 2026-04-07 16:21 Asia/Shanghai / 2026-04-07 08:21 UTC
Mode: external-research-driven
Branch: protected-runtime practical workflows -> observation-topology selection

## Why this branch
This run used the external slot on a thinner protected-runtime seam rather than returning to browser or malware work.

The practical question was not broad instrumentation taxonomy.
It was how to preserve a more operational split between:
- user-space hooks being weak/noisy/detected
- a quieter lower surface existing
- that lower surface actually answering the current question
- later mechanism/owner/consequence proof

That seam already existed partly across the topology-selection and lower-surface tracing notes, but it was worth making more explicit and operator-facing.

## Search-layer observations
Explicit multi-source search was attempted with:
- `--source exa,tavily,grok`

Queries used:
1. `eBPF tracing overhead observability anti-debug instrumentation lower surface official docs`
2. `seccomp ptrace anti debug Android syscall tracing docs eBPF official`
3. `user space hooks vs syscall tracing observation distortion anti instrumentation docs`

Observed source behavior:
- Exa returned usable hits
- Tavily returned usable hits
- Grok was invoked on all queries but failed with repeated 502 errors through the configured proxy/completions endpoint

## Primary source anchors actually used
### Linux seccomp filter docs
URL:
- https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html

Useful operator implications:
- seccomp/policy presence is its own proof object and should not be flattened into broader runtime-gate claims
- lower-surface policy/boundary visibility still needs to be tied to the current question rather than treated as automatically decisive

## Attempted but degraded source paths
- `https://docs.ebpf.io/linux/concepts/overview/` -> fetch route returned 404 in this run
- `https://source.android.com/docs/core/architecture/kernel/bpf` -> fetch route hit redirect issues in this run

These degradations were non-blocking because the run’s practical contribution was a conservative topology-selection refinement, not a detailed eBPF implementation note.

## Practical synthesis to preserve canonically
Useful ladder:

```text
quieter or lower surface exists
  != that surface answers the current question better
  != lower-surface visibility is the decisive boundary
  != broader mechanism or owner path is solved
```

Specific operator-facing reminders:
- noisy/detectable user-space hooks are weaker than a justified lower-surface move
- lower-surface availability is weaker than proving that the current behavior-bearing boundary is visible there
- lower-surface event visibility is weaker than proving decisive gate/owner/consequence truth
- the goal is usually to recover one trustworthy lower boundary and then route back upward, not to stay at the lowest surface forever

## Why this mattered to the KB
The protected-runtime branch already had both topology-selection and lower-surface tracing notes.
This run made the handoff between them more explicit so future work does not silently overread “quieter lower surface exists” as “therefore this is the right next move and the mechanism is now basically solved.”

## Candidate follow-ons
Possible later protected-runtime continuations if needed:
- a narrower compare-heavy note around proving that a lower surface changed uncertainty more than one improved user-space surface would have
- a parent-page sync only if the new topology-selection memory still feels too leaf-local
