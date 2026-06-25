import subprocess, textwrap, time

variants = [
    ("hk-hy2", textwrap.dedent("""
  - name: hk-hy2
    type: hysteria2
    server: 154.86.30.10
    port: 8444
    password: "db8cb0279a30e252754be058a7efe09f"
    sni: www.apple.com
    skip-cert-verify: true
    udp: true
""")),
    ("hk-reality", textwrap.dedent("""
  - name: hk-reality
    type: vless
    server: 154.86.30.10
    port: 8443
    uuid: 7d426249-1723-437e-8e17-70e9cca11a03
    network: tcp
    udp: true
    tls: true
    servername: www.cloudflare.com
    flow: xtls-rprx-vision
    reality-opts:
      public-key: KFJNJ2wp9cnCSiDel7ur72xAFWUZ7wdHa356ORxAplQ
      short-id: 3fbc4bb7d47e8fda
    client-fingerprint: chrome
""")),
]

for name, transit in variants:
    cfg = f"""mixed-port: 7899
allow-lan: false
mode: rule
log-level: info
ipv6: true

proxies:
{transit}
  - name: home-http-via-{name}
    type: http
    server: 204.237.153.49
    port: 60088
    username: VbyYbQEAVhrp
    password: lPgcIWCHPKQ9
    tls: false
    udp: false
    dialer-proxy: {name}

proxy-groups:
  - name: Proxy
    type: select
    proxies:
      - home-http-via-{name}
      - DIRECT

rules:
  - MATCH,Proxy
"""
    path = f"/root/.openclaw/workspace/_tmp_mihomo_{name}.yaml"
    with open(path, "w") as f:
        f.write(cfg)
    subprocess.run("docker rm -f mihomo-chain-test >/dev/null 2>&1 || true", shell=True, check=False)
    subprocess.run(
        f"docker run -d --name mihomo-chain-test --network host -v {path}:/root/.config/mihomo/config.yaml:ro metacubex/mihomo:latest >/dev/null",
        shell=True,
        check=True,
    )
    time.sleep(2)
    res = subprocess.run(
        "curl -fsS --max-time 40 --proxy http://127.0.0.1:7899 https://api.ipify.org",
        shell=True,
        capture_output=True,
        text=True,
    )
    logs = subprocess.run(
        "docker logs --tail 80 mihomo-chain-test",
        shell=True,
        capture_output=True,
        text=True,
    )
    print(f"=== {name} ===")
    print(f"code={res.returncode}")
    print((res.stdout or res.stderr).strip())
    print(logs.stdout.strip())
    print()

subprocess.run("docker rm -f mihomo-chain-test >/dev/null 2>&1 || true", shell=True, check=False)
