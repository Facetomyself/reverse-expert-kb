# 2026-04-16 iOS keychain auth-context -> `SecKey` signature consumer notes

Date: 2026-04-16 04:50 Asia/Shanghai / 2026-04-15 20:50 UTC
Theme: keep keychain query/ref truth, authentication-context truth, private-key operation truth, and request-owned signature consequence separate.

## Why this note exists
The KB already had a practical iOS note for **keychain item retrieval -> request/signing owner**.
What it still lacked was a narrower continuation for cases where the analyst has already localized one plausible keychain item, `SecKeyRef`, or Secure Enclave-backed key handle, but still keeps flattening this ladder:

```text
SecItemCopyMatching / Face ID prompt / SecKeyRef visible
  == same key actually available for the current operation
  == decisive authentication just happened
  == SecKeyCreateSignature actually ran
  == returned bytes became the request-owned signature
```

That flattening is especially risky on iOS because Apple’s own docs preserve several distinct proof objects:
- keychain query/result shape
- access-control policy on the item or key
- reusable `LAContext` truth
- prompt text / prompt presence truth
- actual private-key operation truth
- signature-bytes return truth
- later request-field consumption truth

This source note retains only the smaller, reusable operator facts needed to support a practical workflow note.

## Retained doc anchors (Apple)
### `kSecUseAuthenticationContext`
- Doc JSON endpoint: `https://developer.apple.com/tutorials/data/documentation/security/ksecuseauthenticationcontext.json`
- Retained:
  - value is an `LAContext`
  - if omitted and the item requires authentication, the system creates a new context, uses it once, and discards it
  - if supplied with a previously authenticated context, the operation may succeed without prompting again
  - if supplied with an unauthenticated context, the system attempts authentication and the context may then be reused in later keychain operations
- Practical meaning:
  - **prompt absence != no-auth requirement**
  - a later keychain or key-use success can be reused-context truth before it is fresh-authentication truth

### `kSecUseOperationPrompt`
- Doc JSON endpoint: `https://developer.apple.com/tutorials/data/documentation/security/ksecuseoperationprompt.json`
- Retained:
  - value is a localized prompt string for the authentication operation
- Practical meaning:
  - prompt wording/presence is UI truth, not automatic proof that the same key or same sign call mattered

### `LAContext`
- Doc JSON endpoint: `https://developer.apple.com/tutorials/data/documentation/localauthentication/lacontext.json`
- Retained:
  - `LAContext` evaluates authentication policies and access controls
  - it handles user interaction and interfaces to the Secure Enclave
- Practical meaning:
  - a visible `LAContext` is an authentication surface, not yet key-use truth or signature-consumer truth

### `Accessing Keychain Items with Face ID or Touch ID`
- Doc JSON endpoint: `https://developer.apple.com/tutorials/data/documentation/localauthentication/accessing-keychain-items-with-face-id-or-touch-id.json`
- Retained:
  - Apple’s sample explicitly creates access control with:
    - `SecAccessControlCreateWithFlags(nil, kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly, .userPresence, nil)`
  - the sample query includes:
    - `kSecAttrAccessControl`
    - `kSecUseAuthenticationContext`
  - keychain services may use a caller-provided `LAContext`
  - `touchIDAuthenticationAllowableReuseDuration` can let recent device unlock satisfy the next keychain authentication window and avoid a second immediate authentication prompt
  - Apple explicitly says that this prevents authenticating twice in quick succession, while also noting the grace period is about recent device unlock behavior rather than collapsing all retrieval auth into one generic fact
- Practical meaning:
  - **Face ID / Touch ID UI behavior can lie about the decisive boundary**
  - one recent unlock, one reused context, and one later keychain read are not automatically the same proof object as one request-owned signing operation

### `Searching for keychain items`
- Doc JSON endpoint: `https://developer.apple.com/tutorials/data/documentation/security/searching-for-keychain-items.json`
- Retained:
  - keychain search is query-dictionary driven
  - the query controls both match criteria and return shape
- Practical meaning:
  - query truth and return-shape truth should be frozen before making token/key-use claims

### `SecItemCopyMatching`
- Doc JSON endpoint: `https://developer.apple.com/tutorials/data/documentation/security/secitemcopymatching(_:_:).json`
- Retained:
  - search dictionaries combine item class, attributes, search parameters, and return-type keys
  - when multiple return types are requested, the result can be a dictionary containing the requested shapes
  - Apple explicitly notes you can’t combine `kSecReturnData` and `kSecMatchLimitAll` for password items, because copying each password item could require additional authentication; instead, request a ref/persistent ref first and then request data only for the specific items you actually need
- Practical meaning:
  - bulk-return behavior and authentication behavior are coupled enough that **returned ref != raw secret already recovered**
  - for reversing, a returned item ref or `SecKeyRef` may already be the right narrow object, but it is still weaker than actual consumer/use truth

### `SecAccessControlCreateFlags`
Primary doc JSON endpoints:
- `https://developer.apple.com/tutorials/data/documentation/security/secaccesscontrolcreateflags/privatekeyusage.json`
- `https://developer.apple.com/tutorials/data/documentation/security/secaccesscontrolcreateflags/userpresence.json`
- `https://developer.apple.com/tutorials/data/documentation/security/secaccesscontrolcreateflags/biometrycurrentset.json`

Retained:
- `userPresence` allows access through biometry or passcode
- `biometryCurrentSet` invalidates the item when biometric enrollment changes
- `privateKeyUsage` enables a private key to be used in signing/verification operations; Apple specifically says it is the typical constraint for Secure Enclave key pairs, that attempts to use it outside Secure Enclave generation fail, and that signing with a Secure Enclave private key generated without this constraint fails
- Practical meaning:
  - access-control flags are not background metadata; they materially decide whether the key can be used now, later, or after enrollment change
  - **retrieved handle != currently usable key**

### `SecKeyCreateSignature`
- Doc JSON endpoint: `https://developer.apple.com/tutorials/data/documentation/security/seckeycreatesignature(_:_:_:_:).json`
- Retained:
  - creates a signature using a private key and specified algorithm
  - the caller supplies the private key, algorithm, and data
  - Apple points to `SecKeyIsAlgorithmSupported` as the suitability check
  - function returns signature data or failure
- Practical meaning:
  - the first strong post-keychain boundary is usually not prompt visibility and not key ref visibility, but **one actual signing call plus one returned signature/error object**

### `Protecting keys with the Secure Enclave`
- Doc JSON endpoint: `https://developer.apple.com/tutorials/data/documentation/security/protecting-keys-with-the-secure-enclave.json`
- Retained:
  - Secure Enclave-protected private keys are created/encoded so the app never handles the plain-text key
  - the analyst/app receives only the output of later operations
  - the private key remains logically part of the keychain and can later be retrieved by reference in the usual way
  - only the Secure Enclave that created the key can actually use it
- Practical meaning:
  - a retrieved Secure Enclave-backed `SecKeyRef` is **capability-handle truth**, not key-material truth
  - if the analyst’s goal is a request-owned signature, the first decisive boundary is usually the private-key operation output and later request-field attachment

## Operator ladder retained
This source pass supports the narrower ladder:

```text
query or key ref visible
  != access-control policy on the item/key known
  != reusable auth context already satisfied
  != prompt shown for the decisive reason
  != private-key signing operation attempted
  != signature bytes returned
  != request field consumed
  != same-request signing consequence
```

A second compact reminder worth preserving:

```text
Face ID / Touch ID prompt happened
  != same key was used
  != same sign call succeeded
  != same request attached the returned bytes
```

And a Secure Enclave-specific compact reminder:

```text
Secure Enclave key ref retrieved
  != raw private key recovered
  != current sign operation succeeded
  != request-owned signature proved
```

## Practical workflow cues retained
- freeze one representative query/result shape before narrating “keychain gave me the signing key”
- if a returned object is a ref/handle instead of bytes, ask whether the real next proof object is now **access-control/auth-context truth** or **first `SecKeyCreateSignature` truth**, not generic decoding
- treat reusable `LAContext` success and recent-unlock reuse as separate from fresh-auth proof
- when reversing auth-gated iOS signing, prefer one narrow chain:
  - candidate item/ref -> access-control/auth-context -> sign call -> returned signature/error -> request attachment
- for Secure Enclave cases, stop talking about “key extraction” once the only truthful object left is a key reference and the real analyst goal is operation output or request consequence

## Search-layer trace
See:
- `sources/ios/2026-04-16-0450-keychain-auth-seckey-search-layer.txt`

Observed degraded mode:
- Grok was explicitly invoked via `--source exa,tavily,grok` but returned repeated 502 proxy errors
- Exa and Tavily still returned enough Apple documentation surfaces to support a conservative, bounded iOS continuation
