# 2026-04-04 iOS keychain item retrieval → request/signing owner notes

Date: 2026-04-04 07:21 Asia/Shanghai / 2026-04-03 23:21 UTC
Theme: keep keychain boundary truth separate from downstream request/signing ownership.

## Why this note exists
The KB’s iOS signing branch already mentions “keychain-backed token/session seed” as a common missing input.
What was missing was a thin workflow note that prevents the overclaim:

```text
SecItemCopyMatching observed == token recovered == token used == request/signature owned
```

This source note retains doc-backed anchors (Apple) plus a few discovery pointers (secondary sources) to support a conservative operator workflow note.

## Retained doc anchors (Apple)
The run used Apple Developer Documentation pages as conservative mechanism references:

- Searching for keychain items
  - https://developer.apple.com/documentation/security/searching-for-keychain-items
  - retained: keychain search is attribute-driven; some return options have constraints (snippet indicates certain combinations are invalid for some password-item copies)

- SecItemCopyMatching
  - https://developer.apple.com/documentation/security/secitemcopymatching(_:_:)
  - retained (from search snippets + index snippets): searches use a dictionary; search can be constrained by attributes; return shape is controlled by return keys

- kSecReturnData
  - https://developer.apple.com/documentation/security/ksecreturndata
  - retained: indicates returning secret/encrypted data for keys/password items as CFData

- kSecMatchLimit
  - https://developer.apple.com/documentation/security/ksecmatchlimit
  - retained: indicates the match limit behavior in keychain searches

- Keychain access groups entitlement
  - https://developer.apple.com/documentation/bundleresources/entitlements/keychain-access-groups
  - retained: access groups exist as an entitlement surface used for sharing (exact semantics are app-configuration-driven; do not overclaim runtime usage from entitlement presence)

- Sharing access to keychain items among a collection of apps
  - https://developer.apple.com/documentation/security/sharing-access-to-keychain-items-among-a-collection-of-apps
  - retained: cross-app keychain sharing is controlled by access groups; treat this as a configuration gate, not automatic evidence the target request consumes shared items

## Secondary / discovery-only sources (not used for strong mechanism claims)
Used to sharpen the workflow shape and common pitfalls, not to claim platform semantics:
- Stinger “Keychain Protection” / iOS testing notes: https://stinger.io/ios-app-testing/Dynamic-Analysis/iOS-Keychain-Protection/
- “Common pitfalls when using Keychain Sharing on iOS”: https://www.rambo.codes/posts/2020-01-16-common-pitfalls-when-using-keychain-sharing-on-ios
- StackOverflow discussion on query attributes (kept as a sanity check, not as canonical docs): https://stackoverflow.com/questions/48954725/secitemcopymatching-and-ksecattraccessible-in-keychain

## Operator ladder retained
This note supports the workflow ladder:

```text
query attempted
  != matched item
  != returned object type (data vs ref vs attrs)
  != decoded token material
  != first request/signing consumer
  != downstream effect ownership
```

## Search-layer trace
See:
- `sources/ios/2026-04-04-0721-ios-keychain-search-layer.txt`

Observed degraded mode:
- grok invoked but returned empty set; 502 proxy errors were printed by the tool
