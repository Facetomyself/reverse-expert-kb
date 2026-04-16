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
- local TCP open check showed `30004` was listening on the host

Transit-side validation from `ali-cloud`:
- `http://211.144.221.229:30002/` -> reachable (`302 -> /home`)
- `http://211.144.221.229:30003/` -> reachable (`200 OK`)
- `30004/tcp` -> still returned connection refused during probe, so external WS access is not yet considered validated

Deeper 30004 diagnosis on 2026-04-16:
- local host state is healthy enough that this is **not** primarily a container-absent problem:
  - `easyai-wsgateway` logs showed normal Nest/PM2 startup
  - host `ss -ltnp` showed Docker proxy listening on `*:30004`
  - local `curl http://127.0.0.1:30004/` completed TCP connect and then got `connection reset by peer`, which is consistent with a non-plain-HTTP WS endpoint rather than an unopened local port
- however, the same port from `ali-cloud` still failed at TCP connect time with `connection refused`
- practical interpretation:
  - the blocker is on the **public exposure path** for `211.144.221.229:30004` rather than the inner EasyAI wsgateway container being absent
  - most likely remaining gap is upstream/shared-IP forwarding or equivalent external path configuration for `30004`, not image staging or local Docker bring-up
- operator rule:
  - treat `30004` as **locally bound but externally unvalidated/broken** until the public path is fixed and rechecked

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

## Operator cautions
- If startup fails again with `invalid pool request: Pool overlaps with other one on this address space`, inspect stale Docker networks before blaming image transfer.
- Do not assume the extra helper/runtime ports (`8080`, `8888`, `8000`, `5672`, `15672`, `27017`) are desirable public exposure just because the compose binds them.
- Do not assume `30004` is externally usable until it is revalidated from a transit/public path.
