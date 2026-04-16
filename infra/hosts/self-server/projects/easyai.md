# EasyAI on `self-server-44005`

## Purpose
EasyAI deployment on `host185` (`self-server-44005`) using a Docker Compose stack under the constrained `30001-30010` public TCP budget of the `:44005` VM.

## Placement
- Host: `self-server-44005` / hostname `host185`
- Public IP: `211.144.221.229`
- Deployment root: `/opt/easyai`
- Runtime manager: Docker Compose

## Main intended published ports
- `30002/tcp` -> `EasyAI WebUI`
- `30003/tcp` -> `EasyAI API`
- `30004/tcp` -> `EasyAI WS gateway`
- `30009/tcp` -> `EasyAI ASG / governance API`

## Additional host-bound helper/runtime ports currently present from the shipped compose
These are host listeners created by the compose stack and should be reviewed before treating them as intended public surface:
- `8080/tcp` -> `dozzle`
- `8888/tcp` -> `sandbox`
- `8000/tcp` -> `video-edit`
- `5672/tcp` / `15672/tcp` -> `rabbitmq`
- `27017/tcp` -> `mongo`

## Runtime state confirmed on 2026-04-16
Containers up after recovery:
- `easyai-web`
- `easyai-server`
- `easyai-wsgateway`
- `easyai-asg`
- `agent-memory`
- `easyai-pgvector`
- `mongo`
- `redis`
- `rabbitmq`
- `sandbox`
- `video-edit`
- `dozzle`
- `watchtower`

Host-local validation:
- `curl -I http://127.0.0.1:30002/` -> `302 Found` with redirect to `/home`
- `curl -I http://127.0.0.1:30003/` -> `200 OK`
- `curl http://127.0.0.1:30009/health` -> `200 OK`
- `curl http://127.0.0.1:30004/` -> `426 Upgrade Required`

Transit-side validation from `ali-cloud`:
- `http://211.144.221.229:30002/` -> reachable (`302 -> /home`)
- `http://211.144.221.229:30003/` -> reachable (`200 OK`)
- `http://211.144.221.229:30009/health` -> reachable (`200 OK`)
- `http://211.144.221.229:30004/` -> reachable and returns `426 Upgrade Required`

Practical meaning of the `30004` probe:
- `30004` is now externally reachable, so the earlier connection-refused state was not a permanent upstream/shared-IP limitation
- `426 Upgrade Required` is the expected shape for a plain HTTP probe against the current ws-gateway implementation, which requires a real WebSocket upgrade rather than normal HTTP

## Runtime config gotchas confirmed on 2026-04-16
- `ws-gateway` is **not** a Socket.IO service in the current image; the container code uses the Node `ws` library and starts a raw WebSocket server.
- The current gateway code requires WebSocket query parameters `channel` and `client_id`, then expects a session protocol (`session.initialize`, optional `session.authenticate`) after connection.
- This means `30004` is not a general HTTP health endpoint and not a raw "anything goes" WebSocket target.
- A concrete local misconfiguration was identified and fixed in the compose/runtime wiring for `ws-gateway`:
  - compose published `host ${CONFIG_WS_PORT}:container 3002`
  - but the `easyai-wsgateway` container inherited `CONFIG_WS_PORT=30004` from `.env`
  - so the process listened on `30004` **inside** the container while Docker forwarded the host port to container `3002`
  - fix applied: keep host publish on `30004`, but override the container-internal `CONFIG_WS_PORT=3002` in the `ws-gateway` service so Docker forwards to the actual listening port again
- A second config split-brain was identified and fixed for ASG:
  - front-end config used `NUXT_PUBLIC_SG_APIURL=http://211.144.221.229:30009`
  - `.env.ASG` set `ASG_PORT=30009`
  - but compose host-port substitution still defaulted to `3003` because `ASG_PORT` was not present in the main `.env`
  - fix applied: add `ASG_PORT=30009` to the main `.env` for compose substitution, while overriding the `easyai-asg` container runtime back to `ASG_PORT=3003` internally so host `30009` maps correctly to container `3003`
- Result after those two fixes:
  - `30004` became externally reachable and now returns `426 Upgrade Required` on a plain HTTP probe
  - `30009/health` became externally reachable and returns `200 OK`

## Recovery note: first startup blocker
The blocked startup was initially misattributed to image verification after a long offline image-sync run, but the real final blocker was Docker network overlap during `docker-compose up -d`.

Confirmed recovery details on 2026-04-16:
- all required images were already present on `host185`
- temporary `.tar.gz` bundles had already been cleaned from:
  - `host185:/data`
  - `ali-cloud:/tmp/easyai-image-cache/http-root`
- the EasyAI compose wanted custom subnet `172.21.0.0/16`
- stale abandoned Docker network `one-mcp_default` still occupied `172.21.0.0/16`
- verification before cleanup showed:
  - `one-mcp_default` had no attached containers
  - `/opt/1panel/mcp` was empty
- removing `one-mcp_default` allowed `docker-compose up -d` to complete successfully

## Offline image-staging note
Direct registry pulls to `host185` had been unreliable, so the successful import path used staged artifacts from `ali-cloud`.

By the time of the final manual recovery:
- all required images were already loaded on `host185`
- last confirmed large image loaded successfully:
  - `registry.cn-shanghai.aliyuncs.com/comfy-ai/comfy-server:latest`
- other large images present included:
  - `registry.cn-shanghai.aliyuncs.com/easyaigc/videoedit:latest`
  - `registry.cn-shanghai.aliyuncs.com/easyaigc/agent-memory:latest`
  - `registry.cn-shanghai.aliyuncs.com/easyaigc/wsgateway:latest`

## Public exposure recommendations
### Core public ports for the current IP-based deployment
These are the only EasyAI ports that clearly belong in the main public surface if you keep the current direct-IP style deployment:
- `30002/tcp` -> EasyAI WebUI
- `30003/tcp` -> EasyAI API
- `30004/tcp` -> EasyAI WebSocket gateway

### Optional feature ports
Expose these only if you explicitly need the corresponding feature from outside the host:
- `30009/tcp` -> EasyAI ASG / governance API
  - upstream README explicitly says Agent governance is optional and not required for the main service
- `3004/tcp` -> `agent-memory` HTTP port
  - the main service uses internal container networking (`MEMORY_TCP_HOST=agent-memory`, `MEMORY_TCP_PORT=4004`)
  - no evidence in the current deployment suggests this needs direct public exposure for normal app use

### Should generally stay internal / not public unless you have a specific ops need
- `8000/tcp` -> `video-edit`
  - main app already calls it over container networking via `CONFIG_VIDEO_EDIT_API_URL=http://video-edit:8000`
- `8080/tcp` -> `dozzle`
  - log UI / ops helper, not core app traffic
- `8888/tcp` -> `sandbox` JupyterLab
  - upstream README explicitly says the sandbox service is not recommended to expose publicly
  - default app-side sandbox access already uses internal `http://sandbox:8000`
- `5672/tcp` / `15672/tcp` -> `rabbitmq`
  - internal MQ / admin surface, not required for normal public app use
- `27017/tcp` -> `mongo`
  - compose itself comments that production should avoid exposing it

### Practical minimal recommendation on a tight public-port budget
If you do not currently need governance or remote ops helpers, the EasyAI public set can likely be reduced to just:
- `30002`
- `30003`
- `30004`

If governance is needed, keep `30009` too.

## Operator cautions
- If startup fails again with `invalid pool request: Pool overlaps with other one on this address space`, inspect stale Docker networks before blaming image transfer.
- Do not assume the extra helper/runtime ports (`8080`, `8888`, `8000`, `5672`, `15672`, `27017`) are desirable public exposure just because the compose binds them.
- Do not test `30004` with plain HTTP and conclude the gateway is broken just because it does not return a normal page; for this service, `426 Upgrade Required` on `/` is the healthy indicator that a real WebSocket upgrade is required.
