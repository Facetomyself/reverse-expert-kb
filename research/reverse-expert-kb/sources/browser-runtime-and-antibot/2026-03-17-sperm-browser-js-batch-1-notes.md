# Source Notes — 2026-03-17 — `sperm/md` Browser / JS anti-bot batch 1

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-Python 爬虫进阶必备 _ Js 逆向之补环境到底是在补什么？.md`
- `simpread-cloudflare 五秒盾 js 逆向分析.md`
- `simpread-curl_cffi 突破 Cloudflare 验证.md`
- `simpread-某某网站 JS 逆向及 tls 指纹绕过分析.md`
- `simpread-突破 tls_ja3 新轮子.md`
- one browser-automation / anti-detection article was intended in this batch but the local filename probe did not resolve cleanly; this batch still had enough density to extract durable patterns

## Why these articles were grouped together
This first browser/JS batch coheres around one practical branch:
- **browser-side anti-bot systems are rarely solved by “just run the JS” or “just match the UA”; the analyst usually has to align at least three layers simultaneously: runtime shape, transport fingerprint, and automation topology**

The core subthemes are:
- browser-environment emulation (“补环境”)
- Cloudflare challenge/turnstile/invisible fingerprint surfaces
- TLS / JA3 transport identity
- browser automation and anti-detection framing
- selecting between pure replay, environment reconstruction, impersonated transport, and browser-native execution

## Strong recurring ideas

### 1. “补环境” is really runtime-shape reconstruction, not variable stuffing
The environment-patching article is most useful when read beyond beginner examples.
Its durable lesson is:
- adding `window = global` or a fake `document.cookie` is only the shallowest layer
- serious detectors inspect property descriptors, prototype chains, inheritance, function identity, `toString`, and object provenance
- therefore the real task is reconstructing the **shape** of the browser runtime, not merely defining missing names

This is valuable KB language because it moves the topic from ad hoc stubbing to **runtime-shape reconstruction**.

### 2. Many browser detectors care about provenance, not just values
The discussion of `Object.getOwnPropertyDescriptor`, prototype chains, and inheritance is especially important.
It reinforces that anti-bot logic often asks questions like:
- was this property directly assigned or inherited?
- does this object look like a browser-created instance or a hand-made literal?
- do function descriptors / `toString` / constructor relations look native?

This parallels earlier Android findings nicely: the target often validates **how** an object came to exist, not just what its value is.

### 3. Cloudflare style defenses are multi-surface environment probes, not one token algorithm
The Cloudflare article is useful mostly for its surface inventory:
- challenge vs turnstile vs invisible are different operational modes
- but the hard part is not one cookie/token recipe
- the hard part is surviving a broad environment probe set around DOM, CSS, performance timing, timezone, error behavior, eval/CSP behavior, audio/image/dom features, and general browser object fidelity

This is exactly the kind of material the KB wants:
- **anti-bot as environment-surface interrogation**, not as one cryptographic obstacle.

### 4. Some browser anti-bot systems are lenient on some surfaces and strict on a few decisive ones
The Cloudflare writeup also suggests a durable operator rule:
- not all collected surfaces are equally decisive
- a few high-signal surfaces (runtime-object fidelity, descriptor/prototype integrity, timing, strict eval/CSP behavior, certain challenge-specific flows) may matter much more than many minor collected values

That supports a workflow of:
- prioritize the strict surfaces first,
- do not overfit every noisy field equally.

### 5. TLS/JA3 is a separate identity layer from JS/runtime reconstruction
The TLS fingerprint articles strongly reinforce an important separation:
- even when request params, headers, and visible app-layer data are correct,
- transport identity may still betray the client.

This matters because it keeps analysts from collapsing everything into “JS reversed successfully.”
The actual system may validate:
- JS/runtime shape
- HTTP/2 behavior / header ordering
- TLS/JA3 / client hello shape
- broader browser or library impersonation coherence

### 6. Transport impersonation can be enough for some targets, but not for all
The `curl_cffi` article is useful precisely because it is modest:
- browser-like TLS/JA3 impersonation can unlock some Cloudflare-protected targets
- but it does not solve all cases

That is a healthy KB lesson:
- **transport impersonation is one layer, not the whole solution**.

### 7. A useful operator split emerges: replay client, impersonated client, or native browser client
Across these articles, a practical decision tree appears:
- if the challenge is mostly app-layer crypto/JS, replay or reimplement may be enough
- if the challenge is transport fingerprint only, impersonated TLS/HTTP stacks may suffice
- if the challenge is runtime-shape and DOM/CSP/performance behavior, native browser execution or very deep environment reconstruction may be required

This is strong KB material because it gives a clean selection rule rather than a tool list.

## Concrete operator takeaways worth preserving

### A. Runtime-shape reconstruction workflow
Reusable sequence:
1. do not start by blindly stuffing globals
2. identify which objects/properties are interrogated
3. inspect descriptor shape, prototype inheritance, constructor identity, and function-native appearance
4. reconstruct browser-like provenance where strict surfaces demand it
5. distinguish “value correct” from “object origin and shape believable”

### B. Anti-bot surface-inventory workflow
Reusable sequence:
1. classify the challenge mode (full-page challenge, embedded turnstile, invisible/no-UI)
2. enumerate surfaces under interrogation:
   - DOM/BOM objects
   - descriptor/prototype integrity
   - CSS rules and style behavior
   - performance timing
   - timezone/locale
   - error behavior
   - CSP/eval restrictions
   - audio/canvas/image or other feature probes
   - token/cookie issuance paths
3. locate which surfaces appear strict vs noisy
4. solve strict surfaces first

### C. Transport-identity workflow
Reusable sequence:
1. separate app-layer correctness from transport identity
2. test whether header correctness alone still fails
3. compare HTTP/2 behavior and TLS/JA3/client-hello shape
4. escalate to impersonated transport libraries or custom proxying only when transport identity is the real gate

### D. Client-topology selection workflow for browser anti-bot
Reusable sequence:
1. ask which layer is failing:
   - JS/runtime
   - transport/TLS
   - automation/browser-control signals
   - full-stack coherence
2. choose among:
   - offline JS replay / reimplementation
   - deep environment reconstruction
   - transport impersonation
   - native browser automation with stealth/hardening
3. do not commit to a heavyweight browser when a transport-layer fix is enough
4. do not keep forcing replay when the detector is clearly runtime-shape- or browser-behavior-sensitive

## Candidate KB implications
This batch strongly supports or suggests improvements to:
- browser-runtime subtree notes in the KB
- `topics/runtime-behavior-recovery.md`
- anti-automation / anti-bot workflow branches

Potential future child-note opportunities:
- runtime-shape reconstruction vs simple environment patching
- strict-surface-first workflow for Cloudflare-like anti-bot systems
- transport identity (TLS/JA3/HTTP2) as a separate validation layer
- replay vs impersonation vs native-browser decision note

## Confidence / quality note
This is a strong first browser batch.
Its best contribution is not any one Cloudflare bypass.
It is the clean framing that browser anti-bot work usually spans at least three independent but interacting layers:
- runtime shape
- transport identity
- automation topology

That framing should transfer well into canonical KB notes later.
