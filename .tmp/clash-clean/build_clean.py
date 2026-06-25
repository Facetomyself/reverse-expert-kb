import copy, pathlib, yaml
src = yaml.safe_load(pathlib.Path(".tmp/clash-clean/live-full.yaml").read_text())
by_name = {p["name"]: p for p in src["proxies"]}
rename = {
    "hk-hy2": "香港 01",
    "hk-reality": "香港 02",
    "hk-socks": "香港 03",
    "hk-http": "香港 04",
    "home-http-direct": "家庭出口 01",
    "oracle-gateway-hy2-backup": "备用 01",
    "oracle-proxy-hy2-extra": "备用 02",
    "ali-socks-oracle-egress": "备用 03",
}
proxies = []
for old, new in rename.items():
    p = copy.deepcopy(by_name[old])
    p["name"] = new
    # clean subscription intentionally does not expose/chase dialer-proxy internals
    p.pop("dialer-proxy", None)
    proxies.append(p)
providers = copy.deepcopy(src.get("rule-providers", {}))
for v in providers.values():
    if isinstance(v, dict) and "proxy" in v:
        v["proxy"] = "自动选择"

groups = [
    {"name":"自动选择","type":"url-test","proxies":["香港 01","香港 02","备用 01","备用 02","备用 03"],"url":"https://cp.cloudflare.com/generate_204","interval":300,"tolerance":80},
    {"name":"香港优先","type":"select","proxies":["香港 01","香港 02","香港 03","香港 04","自动选择","DIRECT"]},
    {"name":"AI账号","type":"select","proxies":["家庭出口 01","备用 01","自动选择","DIRECT"]},
    {"name":"大文件","type":"select","proxies":["香港 03","香港 04","备用 03","自动选择","DIRECT"]},
    {"name":"故障切换","type":"fallback","proxies":["备用 01","备用 02","备用 03","香港 01","DIRECT"],"url":"https://cp.cloudflare.com/generate_204","interval":300},
    {"name":"手动选择","type":"select","proxies":["自动选择","香港优先","AI账号","大文件","故障切换","香港 01","香港 02","香港 03","香港 04","家庭出口 01","备用 01","备用 02","备用 03","DIRECT"]},
]
map_group = {"Proxy":"自动选择", "Home-Egress":"AI账号", "Big-Transfer":"大文件", "Fallback":"故障切换", "HK":"香港优先"}
rules=[]
for r in src.get("rules", []):
    nr=r
    for old,new in map_group.items():
        nr=nr.replace(","+old, ","+new)
    rules.append(nr)
clean = {}
for k in ["mixed-port","allow-lan","mode","log-level","ipv6","unified-delay","tcp-concurrent","profile","dns"]:
    if k in src:
        clean[k]=copy.deepcopy(src[k])
clean.setdefault("profile", {})
clean["profile"]["store-selected"] = True
clean["profile"]["store-fake-ip"] = True
clean.setdefault("dns", {})
clean["proxies"] = proxies
clean["proxy-groups"] = groups
clean["rule-providers"] = providers
clean["rules"] = rules
pathlib.Path(".tmp/clash-clean/clash-clean.yaml").write_text(yaml.safe_dump(clean, allow_unicode=True, sort_keys=False), encoding="utf-8")
print("clean", len(proxies), len(groups), len(providers), len(rules))
