# Source Notes — 2026-03-17 — `sperm/md` iOS batch 2

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-iphone8p 到手，10 分钟搞定越狱 + frida 环境.md`
- `simpread-移动安全之 IOS 逆向越狱环境准备 (上).md`
- `simpread-【iOS-Flutter 逆向】__ 岛之踩坑记录篇.md`

Existing KB pages consulted for fit:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`

One additionally opened article (`【APP 逆向百例】某当劳 Frida 检测`) turned out to be Android-focused and was intentionally excluded from iOS synthesis.

## Why these articles were grouped together
This batch coheres around one practical branch:
- **before iOS runtime analysis becomes trustworthy, the analyst often has to normalize execution prerequisites: jailbreak mode, packaging/signing path, Frida deployment topology, and cross-runtime ownership boundaries such as Flutter -> Dart -> native crypto**

The subthemes are:
- jailbreak environment preparation across iOS version bands
- rootful vs rootless operational differences
- signing / sideload / TrollStore / certificate-path preparation as analysis infrastructure
- Frida deployment consistency and version matching
- Flutter on iOS as a cross-runtime owner-localization problem
- dump.dart / Dart runtime symbol recovery when reFlutter or repack fails

## Strong recurring ideas

### 1. Environment preparation is not boring setup; it changes which evidence will later be trustworthy
The jailbreak-environment articles are useful precisely because they show that iOS setup choice is not cosmetic.
Choosing among:
- unc0ver / checkra1n / Dopamine / palera1n
- rootful vs rootless
- Cydia / Sileo / Zebra
- Apple-ID signing vs sideload tool vs TrollStore
changes what can be installed, what survives reboot, how Frida behaves, and which debugging assumptions remain valid.

This strongly supports the KB’s existing iOS runtime-gate framing.

### 2. Rootful vs rootless is an operational branch, not just a community label
The longer environment article contributes a durable practical distinction:
- rootful and rootless environments have different persistence, tool layout, and operational affordances
- “Frida available” is not enough detail; how Frida arrives and how stable the environment is matter later

This is worth preserving because it directly affects reproducibility and troubleshooting.

### 3. Signing / sideload path is part of the runtime gate surface
The environment-prep material also reinforces that on iOS, packaging and installation method are not separate from reversing.
Apple ID signing, certificate-based signing, enterprise profiles, TrollStore, or direct jailbreak-side installation can each affect what runtime state you begin with.

That means packaging/installation path belongs inside the iOS gate model, not outside it.

### 4. Frida deployment topology and version coherence are first-class operational variables
The setup articles make a small but durable point:
- PC-side and device-side Frida versions need to match closely enough
- startup mode, cable/network path, and service style affect reliability
- some “analysis failures” are really deployment-path failures

This fits the broader KB theme that topology choices often matter as much as the hook logic itself.

### 5. Flutter on iOS is a cross-runtime ownership problem more than a platform-problem
The Flutter article is strong because it refuses to get trapped in one runtime too early.
It moves across:
- iOS traffic capture visibility
- app unpacking / dumped IPA inspection
- Flutter-framework detection
- reFlutter/blutter attempts
- Dart runtime dump and function-name recovery
- hook placement on Dart-side hash/update methods

That is exactly the kind of workflow the KB should keep: **cross-runtime owner localization**.

### 6. When runtime rewriting/repacking fails, dump the live runtime and localize the owner there
The Flutter article’s best lesson is not about reFlutter itself.
It is the fallback rule:
- if repacked instrumentation or static framework tooling fails to produce a stable runnable artifact,
- move to live runtime inspection (`dump.dart`, function enumeration, targeted hook on recovered methods),
- and localize the owner in the runtime that actually executes.

This is a very strong practical rule and likely deserves canonical status later.

### 7. Cross-runtime targets should still be reduced to one consequence-bearing owner
The Flutter case is useful because even across iOS + Flutter + Dart, the winning move stays consistent:
- identify one signature field
- recover the method family generating it (`updateHash` etc.)
- verify the preimage shape (sorted k+v+salt)
- reduce the case to a standard digest pipeline

That is exactly in line with the KB’s existing owner-localization and reduction-first philosophy.

## Concrete operator takeaways worth preserving

### A. iOS environment-normalization workflow
Reusable sequence:
1. record device/version/jailbreak compatibility band first
2. choose the installation/signing path intentionally (Apple ID, cert sign, TrollStore, direct jailbreak-side install, etc.)
3. classify rootful vs rootless operationally
4. install debugging substrate (Frida/package manager/OpenSSH/etc.) with version coherence in mind
5. only then treat later runtime failures as target-specific rather than setup-specific

### B. Packaging/install-path-as-gate rule
Reusable rule:
- on iOS, how the artifact is installed/signed is part of the runtime gate surface
- do not treat packaging/installation path as unrelated housekeeping when diagnosing early divergence or tool instability

### C. Frida deployment-coherence workflow for iOS
Reusable sequence:
1. align device-side and host-side Frida versions
2. record whether the transport path is USB, network, or mixed
3. note whether the service is always-on vs manually launched vs package-manager-installed
4. rule out deployment-path instability before deeper anti-instrumentation claims

### D. Cross-runtime owner-localization workflow for iOS Flutter targets
Reusable sequence:
1. confirm the target is Flutter-based (frameworks, Runner/App.framework, Dart indicators)
2. decide whether static tooling/repackaging is stable enough
3. if not, dump the live Dart runtime artifacts instead
4. recover candidate method names / offsets around the target field
5. hook the consequence-bearing Dart/native owner rather than staying trapped in framework setup details
6. reduce the recovered path into a standard-family explanation where possible

### E. Runtime-failure fallback rule for Flutter-like repack failures
Reusable sequence:
1. if reFlutter/repack instrumentation fails to produce a stable runnable app,
2. stop treating repacking success as mandatory,
3. dump the live runtime and localize the owner in the executing runtime,
4. only return to repack/static tooling if later evidence shows it is worth the effort

## Candidate KB implications
This batch strongly supports or suggests improvements to:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`
- iOS practical workflow branches in the KB
- Flutter/cross-runtime ownership notes under mobile/browser-adjacent areas

Potential future child-note opportunities:
- iOS environment-normalization and deployment-topology note
- packaging/install-path-as-runtime-gate note
- cross-runtime owner localization for Flutter on iOS
- live-runtime fallback workflow when repack instrumentation fails

## Confidence / quality note
This is a useful second iOS batch even though part of it is more operational than algorithmic.
Its strongest durable lesson is that iOS setup, deployment topology, and cross-runtime ownership are deeply entangled.

That makes the batch valuable because it prevents later analytical overconfidence built on shaky environment assumptions.
