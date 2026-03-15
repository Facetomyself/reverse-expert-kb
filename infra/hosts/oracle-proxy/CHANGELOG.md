# oracle-proxy / Change Log

## 2026-03-15
- Documented oracle-proxy host baseline, network surface, and main deployed projects.
- Finalized Tavily chain integration:
  - deployed and verified Tavily proxy on port 9874
  - imported historical keys into proxy
  - fixed password handling to use `.env`
  - fixed registration auto-upload by using `host.docker.internal:9874` inside container
  - verified fresh registrations auto-upload to proxy
  - created a working proxy token and verified `/api/search`
- Updated local search-layer to consume Tavily through `proxy.zhangxuemin.work:9874/api`.
