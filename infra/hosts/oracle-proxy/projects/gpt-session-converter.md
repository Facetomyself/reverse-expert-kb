# GPT Session Converter

## Runtime
- Source repository: `https://github.com/Facetomyself/GPTSession2CPAandSub2API`
- Upstream: `https://github.com/gtxx3600/GPTSession2CPAandSub2API`
- Deployed commit: `a097eb155bb7bdf6cbbc26f1e4e75e120ab3163c`
- Runtime path: `/root/containers/gpt-session-converter`
- Served directory: `/root/containers/gpt-session-converter/docs`
- Service type: static browser-only HTML tool; no backend, database, or token persistence on the server.

## Entrypoints
- Global/source: `https://gpt-session.zhangxuemin.work/`
- Domestic/HK edge: `https://gpt-session-cn.zhangxuemin.work/`

## Front Door
- Source front door is `caddy-cpam` on `oracle-proxy`.
- `caddy-cpam` mounts the static directory read-only as `/srv/gpt-session-converter` and serves it with Caddy `file_server`.
- HK edge terminates TLS for `gpt-session-cn.zhangxuemin.work` and reverse-proxies to `https://gpt-session.zhangxuemin.work` with origin Host/SNI preserved.

## Deployment Notes
- On 2026-07-06, the existing fork had diverged from upstream. The old fork main was preserved as branch `archive/fork-main-before-upstream-sync-20260706`, then `Facetomyself/GPTSession2CPAandSub2API:main` was force-with-lease aligned to upstream commit `a097eb1`.
- Cloudflare DNS-only A records:
  - `gpt-session.zhangxuemin.work -> 158.178.236.241`
  - `gpt-session-cn.zhangxuemin.work -> 154.86.30.10`

## Verification
- `https://gpt-session.zhangxuemin.work/` returned HTTP 200 with `content-type: text/html; charset=utf-8`.
- `https://gpt-session-cn.zhangxuemin.work/` returned HTTP 200 through HK edge with the same HTML title.
