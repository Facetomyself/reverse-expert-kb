# iOS Signing Finalization and Preimage-Routing Notes

Date: 2026-03-21
Area: iOS runtime / request-signing continuation
Purpose: source-backed practical support for an iOS-specific continuation note between owner plausibility and generic mobile preimage recovery

## Search intent
This source pass asked a narrower question than “how do iOS signatures work?”

The real target was:
- after one iOS owner path is already plausible,
- what practical evidence helps decide whether the next move should be request-finalization localization,
- earlier preimage capture,
- or preserving one truthful in-app black-box replay path?

Queries used:
- `iOS app request signing Frida Chomper workflow`
- `iOS reverse engineering signature generation Frida replay request signing`
- `iOS SDK signing owner localization token generation reverse engineering`

Search mode/intent:
- deep exploratory multi-source pass

## Retained external signals
### 1. Request-dump / interception tooling supports late-boundary proof
- `https://github.com/alza54/frida-ios-dump-requests`
- `https://github.com/httptoolkit/frida-interception-and-unpinning`
- `https://frida.re/docs/ios/`

Why retained:
- these sources reinforce that on iOS a useful practical boundary often remains at Foundation / request-construction layers
- they support the rule that analysts should anchor one final emitted request shape before assuming standalone signer extraction is the only worthwhile next step
- they justify late request-builder / request-finalization hooks as operator-relevant surfaces

### 2. Chomper-style black-box invocation remains useful, but not sufficient by itself
- `https://bbs.kanxue.com/thread-285666.htm`
- prior KB source notes from 2026-03-17 under `sources/ios-runtime-and-sign-recovery/`

Why retained:
- these sources reinforce the branch rule that execution-assisted owner replay is often the cheapest next move once one owner path is plausible
- but they also leave open the recurring gap this run addresses: after plausible black-box invocation exists, analysts still need to decide whether one finalization boundary, one earlier preimage capture point, or one minimal preserved black-box path is the right stopping point

### 3. Practitioner signals keep pointing to preimage/state rather than pure crypto-family cleanup
- `https://github.com/luoyanbei/reserveSignatureOfOneApp`
- `https://www.mustafadur.com/blog/reverse-ios/`
- `https://www.reddit.com/r/AskReverseEngineering/comments/1gdbrx1/use_frida_to_retrieve_apps_secret_to_sign_jwts/`

Why retained cautiously:
- these are uneven in rigor, but together they reinforce one repeated practical signal: many hard cases are dominated by upstream state, canonicalization, or secret/input recovery rather than by identifying a final hash primitive alone
- this supports routing from an iOS-specific finalization boundary into the generic mobile preimage page only when that is truly the next narrow bottleneck

## Conservative synthesis used for the KB update
The following claims were retained conservatively:
- no claim that one universal iOS signing workflow exists
- no claim that Chomper or Frida-based interception alone solves request acceptance
- no claim that generic request-dump visibility automatically reveals the true signer owner
- no claim that near-correct outputs imply the wrong algorithm rather than missing init/state/finalization context

The smaller practical synthesis carried into the KB was:
- once one iOS owner path is already plausible, many cases need one explicit routing decision between:
  - last request-finalization boundary
  - earlier preimage/state capture
  - preserving one truthful in-app black-box path and moving on

## Why this source pass justified a new page
The iOS branch already had:
- traffic topology relocation
- environment normalization / deployment coherence
- packaging/jailbreak/runtime gate diagnosis
- trust-path localization
- broad ObjC / Swift / native owner localization
- Flutter/cross-runtime owner localization
- Chomper/black-box owner replay
- runtime-table/init-obligation repair
- callback/result-to-policy consequence proof

What still felt under-described was the narrow decision point between:
- “owner plausible and callable enough”, and
- “generic mobile signature/preimage reduction”.

This source pass supported preserving that decision as a distinct iOS-shaped continuation instead of flattening it into either the Chomper note or the generic mobile preimage note.
