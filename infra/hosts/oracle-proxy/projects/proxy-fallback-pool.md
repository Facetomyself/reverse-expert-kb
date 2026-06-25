# Verified Proxy Fallback Pool (`Oracle-Proxy-Extra`)

## 1. Summary
- Project / logical pack: Verified Proxy Fallback Pool
- Host: `oracle-proxy`
- Purpose: 为私有订阅和手工调度提供一组已经外测通过的 **非 HK 额外落地节点**
- Runtime status: available / host-level listeners active
- Priority: Tier 2
- Current subscription role: can be published as group `Oracle-Proxy-Extra` inside private Mihomo / Clash.Meta subscriptions

## 2. Why this exists
This pack is the "extra bag of tools" behind the cleaner HK-facing subscription surface.

Practical role:
- provide **non-HK datacenter fallback** choices when `hk-relay` is not the right exit
- give a small set of **already verified** protocol variants instead of forcing future work to rediscover which old listeners still function
- let private subscriptions expose a compact `Oracle-Proxy-Extra` group without having to publish every historically configured protocol on `oracle-proxy`

## 3. Validation status
Validated externally on **2026-04-21** with fresh Mihomo smoke tests.

Validation result for every promoted node below:
- client type: fresh Mihomo container on the OpenClaw host
- test target: `https://api.ipify.org`
- observed exit IP: **`158.178.236.241`**
- interpretation: protocol path is still alive and usable as an external client entry

## 4. Recommended selection order
Default practical order when you just need a working extra fallback:
1. `oracle-proxy-hy2-extra`
2. `oracle-proxy-xray-reality-extra`
3. `oracle-proxy-tuic-extra`
4. `oracle-proxy-trojan-extra`
5. `oracle-proxy-shadowsocks-extra`

Rule of thumb:
- prefer **HY2** first for general speed / simplicity when UDP is fine
- prefer **Xray Reality Vision** when you want a stronger modern TCP/TLS-shaped path
- prefer **TUIC** as another UDP-first modern option
- prefer **Trojan** on more restrictive networks where plain TLS-shaped TCP often behaves better
- keep **Shadowsocks** as the simple compatibility fallback

## 5. Current promoted nodes

### 5.1 `oracle-proxy-hy2-extra`
- Protocol: `hysteria2`
- Server: `158.178.236.241`
- Port: `30002/udp`
- Password: `822d37a6-4859-4281-ad0e-0dff90345258`
- SNI: `mozilla.org`
- TLS note: server cert on-host was observed as a long-lived self-signed cert with subject/issuer `mozilla.org`, so Mihomo-side `skip-cert-verify: true` is currently the practical setting
- Best use: first extra fallback when UDP works and you just want a straightforward non-HK exit

Mihomo snippet:
```yaml
- name: oracle-proxy-hy2-extra
  type: hysteria2
  server: 158.178.236.241
  port: 30002
  password: "822d37a6-4859-4281-ad0e-0dff90345258"
  sni: mozilla.org
  skip-cert-verify: true
  udp: true
```

### 5.2 `oracle-proxy-xray-reality-extra`
- Protocol: `vless` + `reality` + `xtls-rprx-vision`
- Server: `158.178.236.241`
- Port: `14391/tcp`
- UUID: `62a6644b-0e24-4ec1-8a2d-5c95c84a248c`
- Flow: `xtls-rprx-vision`
- Reality server name: `player.live-video.net`
- Reality public key: `byedoCbgTqEE_6onxgxE5Q2xZnzMqApdswmpmnnEAWg`
- Reality short-id: `6ba85179e30d4fc2`
- Client fingerprint used in validation: `chrome`
- Best use: modern TCP/TLS-shaped fallback when you want something cleaner than old WS-style paths

Mihomo snippet:
```yaml
- name: oracle-proxy-xray-reality-extra
  type: vless
  server: 158.178.236.241
  port: 14391
  uuid: 62a6644b-0e24-4ec1-8a2d-5c95c84a248c
  network: tcp
  udp: true
  tls: true
  servername: player.live-video.net
  flow: xtls-rprx-vision
  reality-opts:
    public-key: byedoCbgTqEE_6onxgxE5Q2xZnzMqApdswmpmnnEAWg
    short-id: 6ba85179e30d4fc2
  client-fingerprint: chrome
```

### 5.3 `oracle-proxy-tuic-extra`
- Protocol: `tuic`
- Server: `158.178.236.241`
- Port: `30003/udp`
- UUID: `822d37a6-4859-4281-ad0e-0dff90345258`
- Password: `822d37a6-4859-4281-ad0e-0dff90345258`
- SNI: `mozilla.org`
- Validation setting: `skip-cert-verify: true`
- Best use: second-line UDP modern transport when HY2 is not the best fit

Mihomo snippet:
```yaml
- name: oracle-proxy-tuic-extra
  type: tuic
  server: 158.178.236.241
  port: 30003
  uuid: 822d37a6-4859-4281-ad0e-0dff90345258
  password: "822d37a6-4859-4281-ad0e-0dff90345258"
  sni: mozilla.org
  skip-cert-verify: true
  alpn:
    - h3
  reduce-rtt: false
  request-timeout: 8000
  udp: true
```

### 5.4 `oracle-proxy-trojan-extra`
- Protocol: `trojan`
- Server: `158.178.236.241`
- Port: `30006/tcp`
- Password: `822d37a6-4859-4281-ad0e-0dff90345258`
- SNI: `mozilla.org`
- Validation setting: `skip-cert-verify: true`
- Best use: TLS-looking TCP fallback on stricter or UDP-unfriendly networks

Mihomo snippet:
```yaml
- name: oracle-proxy-trojan-extra
  type: trojan
  server: 158.178.236.241
  port: 30006
  password: "822d37a6-4859-4281-ad0e-0dff90345258"
  sni: mozilla.org
  skip-cert-verify: true
  udp: true
```

### 5.5 `oracle-proxy-shadowsocks-extra`
- Protocol: `shadowsocks`
- Server: `158.178.236.241`
- Port: `30005/tcp+udp`
- Cipher: `aes-128-gcm`
- Password: `822d37a6-4859-4281-ad0e-0dff90345258`
- Best use: simple compatibility fallback; low ceremony, easy to port into clients that do not like newer stacks

Mihomo snippet:
```yaml
- name: oracle-proxy-shadowsocks-extra
  type: ss
  server: 158.178.236.241
  port: 30005
  cipher: aes-128-gcm
  password: "822d37a6-4859-4281-ad0e-0dff90345258"
  udp: true
```

## 6. Suggested group template
If publishing this pack into a private Mihomo / Clash.Meta subscription, the practical group shape is:

```yaml
proxy-groups:
  - name: Oracle-Proxy-Extra
    type: select
    proxies:
      - oracle-proxy-hy2-extra
      - oracle-proxy-xray-reality-extra
      - oracle-proxy-tuic-extra
      - oracle-proxy-trojan-extra
      - oracle-proxy-shadowsocks-extra
      - DIRECT
```

Recommended use in a broader subscription:
- expose `Oracle-Proxy-Extra` as a **manual fallback pool**, not necessarily the primary everyday default
- keep more specialized routing groups (`Home-Egress`, `HK-Transit`, `Big-Transfer`) separate so this pool stays understandable

## 7. What is intentionally not promoted here
Observed but not promoted into this pack as of 2026-04-21:
- sing-box `xtls-reality` on `30001`
- `ShadowTLS` on `30004`
- `vmess-ws` on `30007`
- `vless-ws-tls` on `30008`
- `h2-reality` on `30009`
- `grpc-reality` on `30010`

Reason:
- either not yet re-validated in the same clean Mihomo pass
- or not worth polluting the default extra pool until there is a concrete need

## 8. Operations
### Re-run smoke test for one node
Example Mihomo-side validation pattern:
```bash
# 1. write a temporary Mihomo config with only the candidate node
# 2. run a disposable mihomo container bound to a local mixed-port
# 3. curl https://api.ipify.org through that local proxy
# 4. confirm expected egress IP is 158.178.236.241
```

### Re-check on host before promoting more nodes
```bash
ssh oracle-proxy
systemctl is-active sing-box xray
ss -lntup | grep -E '14391|3000[1-9]|30010'
```

## 9. Cross-links
- Host docs: `../HOST.md`, `../NETWORK.md`, `../PROJECTS.md`
- Related infra note: `./network-stack.md`
- Downstream usage example: private `hk-relay` Clash.Meta track can publish this pack as group `Oracle-Proxy-Extra`

## 10. Change History
- 2026-04-21:
  - created a dedicated operator-oriented manual for the externally verified extra fallback nodes on `oracle-proxy`
  - recorded full Mihomo snippets for `hysteria2`, `xray reality vision`, `tuic`, `trojan`, and `shadowsocks`
  - documented recommended selection order and reasons for not promoting the rest of the historical protocol surface yet
