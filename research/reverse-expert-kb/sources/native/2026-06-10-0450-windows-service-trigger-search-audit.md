# Search-layer audit — Windows service trigger to worker consumer

Date: 2026-06-10 04:50 Asia/Shanghai

Command used:

```bash
python3 skills/search-layer/scripts/search.py --source exa,tavily,grok --mode deep --num 5 --intent exploratory --queries \
  "Windows service trigger start service trigger event reverse engineering SERVICE_TRIGGER_INFO HandlerEx controls" \
  "Windows service control handler HandlerEx preshutdown stop control accepted dwControlsAccepted SERVICE_STATUS reverse engineering" \
  "Windows SCM service trigger SERVICE_TRIGGER_TYPE_DEVICE_INTERFACE_EVENT ETW service start"
```

Requested sources: exa,tavily,grok

Succeeded sources: exa,tavily

Failed sources: grok

Failure observed: `502 Server Error: Bad Gateway for url: http://proxy.zhangxuemin.work:8000/v1/chat/completions` for all three queried prompts.

Endpoints used / configured:

- Exa endpoint: `http://158.178.236.241:7860/search`
- Tavily endpoint: `http://proxy.zhangxuemin.work:9874/api/search`
- Grok endpoint: `http://proxy.zhangxuemin.work:8000/v1/chat/completions`

Representative merged results used:

- Microsoft Learn — Service Trigger Events: https://learn.microsoft.com/en-us/windows/win32/services/service-trigger-events
- Microsoft Learn — `SERVICE_TRIGGER`: https://learn.microsoft.com/en-us/windows/win32/api/winsvc/ns-winsvc-service_trigger
- Microsoft Learn — Service Control Handler Function: https://learn.microsoft.com/en-us/windows/win32/services/service-control-handler-function
- Microsoft Learn — `LPHANDLER_FUNCTION_EX`: https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nc-winsvc-lphandler_function_ex
- Microsoft Learn — `SERVICE_STATUS`: https://learn.microsoft.com/en-us/windows/win32/api/winsvc/ns-winsvc-service_status
- Inbits — Reversing `npsvctrig.sys` - Named Pipe Service Triggers: https://inbits-sec.com/posts/npsvctrig-notes/

Degraded-mode note: all requested sources were invoked explicitly through `search-layer --source exa,tavily,grok`; Grok returned no usable results, so synthesis used Exa/Tavily and fetched sources conservatively.
