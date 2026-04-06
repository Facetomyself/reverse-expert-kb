# iOS PAC-shaped callback / dispatch failure triage notes

Date: 2026-04-07 06:21 Asia/Shanghai / 2026-04-06 22:21 UTC
Mode: external-research-driven
Branch: iOS practical workflows -> PAC-shaped callback / dispatch failure triage

## Why this branch
Recent external runs already spent time on malware persistence/trigger seams.
This run used the external slot on a thinner iOS practical branch to avoid clustering too tightly in malware and to keep branch balance healthier.

The chosen seam was:
- PAC-shaped callback / dispatch failure triage on arm64e iOS

Why it fit:
- practical operator value
- still thinner than the stronger browser/mobile protected-runtime clusters
- easy for analysts to overread as generic hook instability or generic EXC_BAD_ACCESS noise

## Search-layer observations
Explicit multi-source search was attempted with:
- `--source exa,tavily,grok`

Queries used:
1. `arm64e pointer authentication objc block invoke callback dispatch crash triage official docs`
2. `Apple pointer authentication arm64e dispatch blocks Objective-C official documentation`
3. `iOS arm64e PAC callback block dispatch debugging crash EXC_BAD_ACCESS docs`

Observed source behavior:
- Exa returned useful hits
- Tavily returned useful hits
- Grok was invoked but failed through the configured proxy/completions endpoint with repeated 502 errors

## Primary source anchors
### Apple: Preparing your app to work with pointer authentication
URL:
- https://developer.apple.com/documentation/security/preparing_your_app_to_work_with_pointer_authentication

Useful operator implications:
- pointer authentication is not just generic memory corruption folklore; arm64e pointer-use failures can be shaped by authenticated code/data pointer expectations
- stale, copied, reinterpreted, or incorrectly reconstructed callable pointers can fail differently from ordinary selector/signature mistakes
- arm64e-specific realism matters when debugging callback/function-pointer crashes

### Apple: Investigating memory access crashes
URL:
- https://developer.apple.com/documentation/xcode/investigating-memory-access-crashes

Useful operator implications:
- not every callback crash on arm64e is actually a PAC problem
- ordinary memory-lifetime, ownership, corruption, and invalid-access causes still need to be separated from PAC-shaped hypotheses
- practical triage should reduce the crash into one narrower category before opening broader mitigation narratives

## Practical synthesis to preserve canonically
Useful triage split:

```text
callback/dispatch crash
  != PAC-shaped callable-pointer failure
  != generic selector/signature mismatch
  != block-lifetime / capture / object-ownership failure
  != later consumer/state consequence problem
```

More useful operator-facing split for this branch:
- selector/ABI/signature mismatch
- block layout / invoke-pointer / capture-lifetime mistake
- stale or wrongly reconstructed function pointer under arm64e/PAC expectations
- later queue/actor/UI consumer problem after callback delivery is already fine

## Practical value to keep in the KB
The branch should push analysts toward:
- proving whether the failure is really at callback identity / invoke boundary
- distinguishing ordinary lifetime/layout bugs from arm64e authenticated-pointer failures
- avoiding the common overclaim that any callback crash on modern iOS is automatically “PAC”
- keeping callback landing truth, callable-pointer truth, actual resume/delivery truth, and later consumer truth separate

## Candidate follow-ons
Possible later iOS follow-up if the branch still needs it:
- a narrower case-driven continuation around block layout / invoke-pointer truth vs continuation-resume truth when callback landing is visible but execution still fails under arm64e

This run should stop after materially improving the existing PAC triage note and syncing parent/index memory only if needed.
