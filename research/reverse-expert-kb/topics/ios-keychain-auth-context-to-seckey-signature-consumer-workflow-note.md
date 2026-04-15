# iOS Keychain Auth-Context -> `SecKey` Signature Consumer Workflow Note

Topic class: concrete workflow note
Ontology layers: iOS practical workflow, auth-gated key use, keychain-to-signature consumer bridge
Maturity: practical
Related pages:
- topics/ios-practical-subtree-guide.md
- topics/ios-keychain-item-retrieval-to-request-signing-owner-workflow-note.md
- topics/ios-request-signing-finalization-and-preimage-routing-workflow-note.md
- topics/mobile-signature-location-and-preimage-recovery-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md
Related source notes:
- sources/ios/2026-04-16-ios-keychain-auth-context-seckey-signature-notes.md

## 1. Why this note exists
The KB already had an iOS note for **keychain item retrieval -> request/signing owner**.
What it still lacked was a narrower continuation for cases where the analyst already has one plausible keychain item, `SecKeyRef`, or Secure Enclave-backed key handle, but the real liar is now the gap between:
- query/ref truth
- access-control / authentication-context truth
- actual private-key operation truth
- returned signature bytes
- request-field consumption truth

Analysts often flatten this ladder too early:

```text
SecItemCopyMatching / Face ID prompt / SecKeyRef visible
  == key really available for this operation
  == decisive authentication just happened
  == SecKeyCreateSignature succeeded
  == request-owned signature proved
```

A tighter operator ladder is usually required:

```text
query or key ref visible
  != access-control policy on the item/key known
  != reusable auth context already satisfied
  != prompt shown for the decisive reason
  != private-key operation attempted
  != signature bytes returned
  != request field consumed
  != same-request signing consequence
```

This note exists to keep that narrower seam practical and to stop iOS signing work from collapsing back into vague “Face ID happened” or “keychain signing happened” language.

## 2. When to use this note
Use this note when most of these are true:
- the case is already clearly iOS-shaped and already past broad setup/gate triage
- one request/signing owner path is already plausible enough that broad owner search should stop
- one keychain item, `SecKeyRef`, persistent ref, or Secure Enclave-backed key handle already looks relevant
- `SecItemCopyMatching`, `kSecUseAuthenticationContext`, `kSecUseOperationPrompt`, `SecAccessControlCreateWithFlags`, `SecKeyCreateSignature`, or nearby `LAContext` surfaces are visible enough to freeze
- the real question is no longer “is keychain involved at all?” but “did this auth-gated key actually produce the current signature bytes and did the request path consume them?”

Use it for cases like:
- a biometric prompt appears near request signing, but it is unclear whether the decisive proof object is fresh authentication, reused context, or the later sign call
- `SecItemCopyMatching` returns a ref or `SecKeyRef`, but it is still unclear whether the returned handle actually becomes the current signing key
- a Secure Enclave-backed key is visible, but the analyst still needs to prove one real `SecKeyCreateSignature` call and one request attachment boundary
- prompt-free success after unlock makes the analyst unsure whether the item stopped being protected or whether one reused `LAContext` / recent unlock path satisfied the auth requirement
- a request header/body field clearly looks signature-shaped, but the first truthful consumer between key handle, sign output, and request attachment is still unclear

Do **not** use this note when:
- the first plausible owner is still unclear (route to `topics/ios-objc-swift-native-owner-localization-workflow-note.md` or the Flutter variant)
- the case is still primarily about whether the right request family is visible at all (route to traffic/trust/gate notes first)
- the remaining gap is already broader request-finalization / preimage routing rather than auth-gated key use specifically (route to `topics/ios-request-signing-finalization-and-preimage-routing-workflow-note.md`)
- truthful result material already exists and the real remaining gap is the first policy-bearing consumer (route to `topics/ios-result-callback-to-policy-state-workflow-note.md`)

## 3. Core claim
A prompt, a keychain hit, and a key reference are not the same proof object.
A practical iOS stop rule worth preserving more sharply is:

```text
query/ref truth
  != authenticated-for-this-operation truth
  != private-key operation truth
  != returned signature truth
  != request-field consumption truth
```

For Secure Enclave-backed keys, there is also a sharper reminder:

```text
Secure Enclave key ref retrieved
  != raw key material recovered
  != same key used for this sign call
  != request-owned signature proved
```

The practical question is usually narrower than “did keychain signing happen?”
It is:

```text
Which exact boundary first turns this plausible keychain/key reference into one
current request-owned signature or auth consequence I can trust?
```

## 4. Boundary objects to keep separate
### A. Query / returned-object truth
Freeze one representative object only:
- item class and identity selectors from the query
- whether the result is bytes, attributes, a ref, a persistent ref, or a `SecKeyRef`
- whether you are looking at one specific item or an over-broad enumeration surface

Practical reminder:
- Apple documents `SecItemCopyMatching` as a query-dictionary API with return-type control
- for password items, Apple explicitly warns that `kSecReturnData` and `kSecMatchLimitAll` cannot be combined, because copying each password item could require additional authentication
- for reversing, that means bulk-return behavior and authentication behavior can already distort what a “successful search” really proved

### B. Access-control policy truth
Freeze the policy attached to the item or key:
- accessibility class
- whether the item/key uses `SecAccessControl`
- whether flags like `.userPresence`, `.biometryCurrentSet`, or `.privateKeyUsage` matter

Practical reminder:
- `.userPresence` is access-via-biometry-or-passcode truth
- `.biometryCurrentSet` can invalidate the item if biometric enrollment changes
- `.privateKeyUsage` is a real usability gate for Secure Enclave private keys, not just metadata

### C. Authentication-context / prompt truth
Freeze what the current operation actually relied on:
- caller-provided `LAContext` vs system-created one
- whether the context may already have been authenticated
- whether the current operation used `kSecUseAuthenticationContext`
- whether `kSecUseOperationPrompt` only explains prompt text rather than use/ownership
- whether recent device unlock or allowable reuse duration may have satisfied the auth requirement without a fresh prompt

Practical reminder:
- Apple explicitly documents that a provided, previously authenticated `LAContext` can let later keychain operations succeed without another prompt
- therefore prompt presence/absence is weaker than same-operation auth truth

### D. Private-key operation truth
Freeze the first real use boundary:
- one `SecKeyCreateSignature(...)` call or immediate wrapper
- the specific algorithm actually requested
- any `SecKeyIsAlgorithmSupported(...)` / error path that decides whether the call is even meaningful
- whether the current object is still only a key handle or already an operation output

Practical reminder:
- the first strong post-keychain boundary is often the sign operation itself, not the earlier prompt or key ref
- for Secure Enclave cases, the key remains encoded and only the enclave can use it; this makes operation truth more valuable than key-material fantasies

### E. Signature-bytes truth
Freeze one output only:
- returned `CFData` / `Data` signature bytes or one explicit error object
- one stable shape/length/format clue if available
- one immediate caller that receives the bytes

Practical reminder:
- returned signature bytes are still weaker than request-owned consumer truth
- the output can still be dropped, wrapped, retried, or replaced before it reaches the request that matters

### F. Request-field consumer truth
Freeze the first consumer that actually matters:
- one header/body/query attachment point
- one request builder or canonicalizer that ingests the returned signature bytes
- one compare pair where the field changes predictably when the key-use/signature path changes

Practical reminder:
- this is the endpoint of the workflow
- everything before it is still setup, gating, or operation output unless proved otherwise

## 5. Default workflow
### Step 1: freeze one representative request and one candidate key surface
Write down only:
- one request family that clearly matters
- one query/ref/key handle that looks relevant
- one visible consequence (header/body field, auth blob, challenge response, or later accept/reject outcome)

Avoid mixing multiple keys, multiple prompts, or multiple request families.

### Step 2: prove the returned shape before narrating key use
For that representative query or retrieval path, prove:
- status/result path
- returned shape: bytes vs ref vs persistent ref vs `SecKeyRef`
- whether the current object is already narrow enough, or whether you are still standing on an over-broad enumeration surface

Useful stop rule:
- if a returned object is a ref or `SecKeyRef`, do **not** reopen generic byte-decoding work by default
- ask instead whether the next truthful boundary is now access-control/auth-context truth or first sign-operation truth

### Step 3: freeze access-control and auth-context together
Capture the smallest truthful pair:
- access-control policy on the item/key
- authentication context actually used for this operation

Good surfaces include:
- `SecAccessControlCreateWithFlags(...)`
- `kSecAttrAccessControl`
- `kSecUseAuthenticationContext`
- `kSecUseOperationPrompt`
- one representative `LAContext` object / wrapper

Practical reminder:
- prompt text is still UI truth
- a reused `LAContext` can be operation-enabling truth without being fresh-auth truth

### Step 4: choose the first real key-operation consumer
Good default candidates:
- `SecKeyCreateSignature(...)`
- the immediate Swift/ObjC wrapper that supplies the algorithm and data
- the first caller that turns a returned key handle into an operation request

Bad default stopping points:
- `LAContext` visibility alone
- prompt visibility alone
- `SecItemCopyMatching` alone
- a `SecKeyRef` handle alone
- Secure Enclave presence alone

### Step 5: prove sign output before request attachment
For the representative path, prove:
- one sign call or one concrete failure
- one returned signature buffer (or one error object)
- one immediate receiver of that buffer

Stop rule:
- do not treat a sign call attempt as request-owned truth until one later request field or auth object visibly consumes the returned bytes

### Step 6: tie the signature to the request that matters
Build one compare pair such as:
- same request family with a changed auth context / changed allowed prompt path
- same request family before and after biometric enrollment / passcode / key availability change when safe and realistic
- same request family with a hook/mutation at the first sign-output consumer
- same request family with a hook/mutation at the first request-attachment consumer

Success criterion:
- one request field, auth blob, or consequence changes predictably with the sign-output path you froze

## 6. Common failure patterns this note prevents
### Failure pattern A: “Face ID happened, so that must be the signing boundary.”
Often false.
The real boundary may be reused-context truth, keychain item availability, or a later `SecKeyCreateSignature` call.

### Failure pattern B: “No prompt means the item/key wasn’t protected.”
Often false.
Apple explicitly preserves reused `LAContext` and recent-unlock satisfaction paths.

### Failure pattern C: “A `SecKeyRef` means I recovered the key.”
False for Secure Enclave-backed keys and often misleading elsewhere.
A key handle is not the same thing as key-material recovery.

### Failure pattern D: “`SecKeyCreateSignature` is visible, so the request signature is explained.”
Often false.
You still need the first request-field consumer.

### Failure pattern E: “Keychain success proves request ownership.”
Often false.
Query/ref truth, auth truth, operation truth, and request consumption truth are separate.

## 7. Sources
See:
- `sources/ios/2026-04-16-ios-keychain-auth-context-seckey-signature-notes.md`

Primary Apple documentation anchors retained conservatively:
- `kSecUseAuthenticationContext`
- `kSecUseOperationPrompt`
- `LAContext`
- `Accessing Keychain Items with Face ID or Touch ID`
- `Searching for keychain items`
- `SecItemCopyMatching(_:_:)`
- `SecAccessControlCreateFlags.userPresence`
- `SecAccessControlCreateFlags.biometryCurrentSet`
- `SecAccessControlCreateFlags.privateKeyUsage`
- `SecKeyCreateSignature(_:_:_:_:)`
- `Protecting keys with the Secure Enclave`
