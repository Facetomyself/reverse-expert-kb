# iOS Keychain Item Retrieval → Request/Signing Owner Workflow Note

Topic class: concrete workflow note
Ontology layers: iOS practical workflow, keychain boundary, token/session material provenance, request-signing preimage routing
Maturity: practical
Related pages:
- topics/ios-practical-subtree-guide.md
- topics/ios-request-signing-finalization-and-preimage-routing-workflow-note.md
- topics/ios-objc-swift-native-owner-localization-workflow-note.md
- topics/mobile-signature-location-and-preimage-recovery-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md
Related source notes:
- sources/ios/2026-04-04-ios-keychain-item-retrieval-notes.md

## 1. Why this note exists
In iOS signing / session / auth reversing, “keychain access happened” is a recurring false stopping point.

Analysts often collapse this ladder:

```text
SecItemCopyMatching called
  == token retrieved
  == token used
  == token owned request/signature
```

But operator truth is usually a longer chain:

```text
keychain query attempted
  != query actually matched an item
  != returned object type truth (data vs ref vs attributes)
  != returned bytes decoded into the token the request uses
  != downstream request builder/signer actually consumed those bytes
  != token actually influenced the signature/preimage (vs decoy / stale / unused)
```

This page is a thin workflow note to keep those proof objects separate and to give a cheap path to prove the first consumer that turns keychain material into request/signing consequence.

## 2. When to use this note
Use when most of these are true:
- the case is iOS-shaped and already past broad setup/gate triage
- request signing / auth headers / session tokens are in scope
- you suspect the missing input is stored in the Keychain (or a framework that wraps it)
- you can observe Security.framework usage (static strings, imports, symbols, Frida hooks)
- you need to prove whether the keychain read is real, which item was returned, and whether it actually feeds the signing/request path

Do **not** use this note when:
- you already have an accepted request and the remaining work is purely downstream policy consequence
- the bottleneck is still trust-path/pinning (route to `ios-trust-path-and-pinning-localization-workflow-note`)

## 3. Core claim
Treat Keychain activity as a boundary-crossing event that produces **candidate material**.
You still need to prove:
1) it matched the right item
2) it returned the right shape
3) the shape was decoded into the actual token material
4) that material was consumed by the request builder / signer that matters

## 4. Boundary objects to keep separate
### A. Query-dictionary truth
Keychain reads are typically shaped by a query dictionary (attributes + return specifiers).
Operator goal: freeze the query dict (keys + values) and map it to one item class and one identity.

### B. Match truth
A call can succeed/fail, and a “success” can still return a shape that isn’t the token you think.
Operator goal: record status + whether an output object was returned.

### C. Return-shape truth
Keychain APIs can return:
- data bytes (`kSecReturnData`-style behavior)
- attributes dict
- a reference (persistent ref / item ref)

Operator goal: prove what kind of object was returned in your target.

### D. Decode/canonicalization truth
Even if bytes are returned, you still need to prove how they become a token:
- UTF-8 string? JSON? plist? protobuf? encrypted blob? custom packing?

### E. First consumer truth
The only strong claim is when you can point at one downstream consumer that:
- takes the returned bytes/object
- derives the field used in the request/signing preimage

## 5. Default workflow (practical)
### Step 1: localize the keychain boundary surface
Cheap anchors:
- imports: `Security.framework`
- strings: `kSecClass`, `kSecAttrService`, `kSecAttrAccount`, `kSecAttrAccessGroup`
- symbols: `SecItemCopyMatching`, `SecItemAdd`, `SecItemUpdate`, `SecItemDelete`

### Step 2: freeze one representative keychain query
Freeze one query dict (even if partial):
- item class (`kSecClass`)
- identity selectors (often `kSecAttrService`, `kSecAttrAccount`, sometimes `kSecAttrAccessGroup`)
- match limit (`kSecMatchLimit`)
- return keys (data/attributes/ref)

Stop rule:
- do not generalize across many queries yet; one query is enough.

### Step 3: prove match + return shape
For that one query, prove:
- status code path (success vs error)
- whether an output object exists
- whether it’s bytes vs dict vs ref

Practical warning preserved from Apple doc snippets:
- some return-key combinations are invalid for certain item types (so “my dict seems fine” can still be false). Treat invalid-return-shape as a *real* discriminant.

### Step 4: bridge into the request/signing path
Once you have return-shape truth:
- follow the returned object one hop: who receives it next?
- log the **first transformation** (string decode, base64, JSON parse, HMAC key setup, etc.)

The operator goal is not “full keychain taxonomy.”
It is: **one consumer**.

### Step 5: prove keychain material actually influences request/signing
Build a compare pair:
- same action with keychain item present vs deleted/changed (when safe)
- same action across fresh-login vs stale session
- same signing flow but with controlled mutation of the returned bytes at the first consumer boundary (if you can safely do it)

Success criteria:
- you can point to one request field/signature input that changes predictably with keychain material changes.

## 6. Common failure patterns this note prevents
- “I saw SecItemCopyMatching, so I found the token.” (often only query attempt)
- “Return status was success, so token must be valid.” (return-shape/decoding might be wrong)
- “Keychain access group exists, so cross-app sharing explains everything.” (access-group truth != used-by-request truth)
- “I decoded bytes, so that’s the signing key.” (decode truth != first consumer truth)

## 7. Sources
See: `sources/ios/2026-04-04-ios-keychain-item-retrieval-notes.md`

Apple documentation anchors (used conservatively as mechanism references):
- Searching for keychain items: https://developer.apple.com/documentation/security/searching-for-keychain-items
- SecItemCopyMatching: https://developer.apple.com/documentation/security/secitemcopymatching(_:_:)
- kSecReturnData: https://developer.apple.com/documentation/security/ksecreturndata
- kSecMatchLimit: https://developer.apple.com/documentation/security/ksecmatchlimit
- Keychain access groups entitlement: https://developer.apple.com/documentation/bundleresources/entitlements/keychain-access-groups
- Sharing access to keychain items among a collection of apps: https://developer.apple.com/documentation/security/sharing-access-to-keychain-items-among-a-collection-of-apps
