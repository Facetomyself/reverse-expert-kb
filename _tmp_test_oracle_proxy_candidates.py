import subprocess
import time

TESTS = [
    {
        "name": "oracle-proxy-shadowsocks",
        "yaml": """mixed-port: 7900
allow-lan: false
mode: rule
log-level: info
ipv6: true

proxies:
  - name: oracle-proxy-shadowsocks
    type: ss
    server: 158.178.236.241
    port: 30005
    cipher: aes-128-gcm
    password: 822d37a6-4859-4281-ad0e-0dff90345258
    udp: true

proxy-groups:
  - name: Proxy
    type: select
    proxies:
      - oracle-proxy-shadowsocks
      - DIRECT

rules:
  - MATCH,Proxy
""",
    },
    {
        "name": "oracle-proxy-trojan",
        "yaml": """mixed-port: 7900
allow-lan: false
mode: rule
log-level: info
ipv6: true

proxies:
  - name: oracle-proxy-trojan
    type: trojan
    server: 158.178.236.241
    port: 30006
    password: 822d37a6-4859-4281-ad0e-0dff90345258
    sni: mozilla.org
    skip-cert-verify: true
    udp: true

proxy-groups:
  - name: Proxy
    type: select
    proxies:
      - oracle-proxy-trojan
      - DIRECT

rules:
  - MATCH,Proxy
""",
    },
    {
        "name": "oracle-proxy-tuic",
        "yaml": """mixed-port: 7900
allow-lan: false
mode: rule
log-level: info
ipv6: true

proxies:
  - name: oracle-proxy-tuic
    type: tuic
    server: 158.178.236.241
    port: 30003
    uuid: 822d37a6-4859-4281-ad0e-0dff90345258
    password: 822d37a6-4859-4281-ad0e-0dff90345258
    sni: mozilla.org
    skip-cert-verify: true
    alpn:
      - h3
    reduce-rtt: false
    request-timeout: 8000
    udp: true

proxy-groups:
  - name: Proxy
    type: select
    proxies:
      - oracle-proxy-tuic
      - DIRECT

rules:
  - MATCH,Proxy
""",
    },
    {
        "name": "oracle-proxy-xray-reality",
        "yaml": """mixed-port: 7900
allow-lan: false
mode: rule
log-level: info
ipv6: true

proxies:
  - name: oracle-proxy-xray-reality
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

proxy-groups:
  - name: Proxy
    type: select
    proxies:
      - oracle-proxy-xray-reality
      - DIRECT

rules:
  - MATCH,Proxy
""",
    },
]

for test in TESTS:
    path = f"/root/.openclaw/workspace/_tmp_{test['name']}.yaml"
    with open(path, "w") as f:
        f.write(test["yaml"])
    subprocess.run("docker rm -f mihomo-candidate-test >/dev/null 2>&1 || true", shell=True, check=False)
    run = subprocess.run(
        f"docker run -d --name mihomo-candidate-test --network host -v {path}:/root/.config/mihomo/config.yaml:ro metacubex/mihomo:latest >/dev/null",
        shell=True,
        capture_output=True,
        text=True,
    )
    print(f"=== {test['name']} ===")
    if run.returncode != 0:
        print("docker run failed")
        print((run.stdout + run.stderr).strip())
        print()
        continue
    time.sleep(2)
    curl = subprocess.run(
        "curl -fsS --max-time 40 --proxy http://127.0.0.1:7900 https://api.ipify.org",
        shell=True,
        capture_output=True,
        text=True,
    )
    print(f"curl_code={curl.returncode}")
    print((curl.stdout or curl.stderr).strip())
    logs = subprocess.run(
        "docker logs --tail 120 mihomo-candidate-test",
        shell=True,
        capture_output=True,
        text=True,
    )
    print(logs.stdout.strip())
    print()

subprocess.run("docker rm -f mihomo-candidate-test >/dev/null 2>&1 || true", shell=True, check=False)
