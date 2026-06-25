from pathlib import Path
import copy
import subprocess
import textwrap
import time
import yaml

SECRET_PATH = "sub-a49d371396d93e9572ddecff6f51fc4707316b99c0edc0b6"
SRC = Path('/root/.openclaw/workspace/_tmp_live_private_clash_meta_v3.yaml')
OUT = Path('/root/.openclaw/workspace/_tmp_live_private_clash_meta_v4.yaml')

data = yaml.safe_load(SRC.read_text())

# Safer client defaults for Mihomo/Clash.Meta clients.
data['mode'] = 'rule'
data['unified-delay'] = True
data['tcp-concurrent'] = True
data['profile'] = {
    'store-selected': True,
    'store-fake-ip': True,
}

dns = data.setdefault('dns', {})
dns['enhanced-mode'] = 'fake-ip'
dns.setdefault('fake-ip-filter', [])
for item in [
    '*.lan', '*.local', 'localhost.ptlogin2.qq.com',
    'time.*.com', 'time.*.gov', 'time.*.edu.cn', 'time.*.apple.com',
    'ntp.*.com', 'ntp.*.com.cn', '*.ntp.org.cn', '+.pool.ntp.org',
    'connect.rom.miui.com', 'connectivitycheck.gstatic.com',
    'detectportal.firefox.com', 'msftconnecttest.com', 'msftncsi.com',
    '*.home.arpa', 'router.asus.com', 'routerlogin.net',
]:
    if item not in dns['fake-ip-filter']:
        dns['fake-ip-filter'].append(item)

BASE = 'https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta'
# MRS provider names are intentionally narrow/category-based; manual overrides stay above broad providers.
data['rule-providers'] = {
    'geosite-private': {
        'type': 'http', 'behavior': 'domain', 'format': 'mrs', 'interval': 86400,
        'path': './rulesets/geosite-private.mrs',
        'url': f'{BASE}/geo/geosite/private.mrs',
        'proxy': 'Proxy',
    },
    'geoip-private': {
        'type': 'http', 'behavior': 'ipcidr', 'format': 'mrs', 'interval': 86400,
        'path': './rulesets/geoip-private.mrs',
        'url': f'{BASE}/geo/geoip/private.mrs',
        'proxy': 'Proxy',
    },
    'geosite-cn': {
        'type': 'http', 'behavior': 'domain', 'format': 'mrs', 'interval': 86400,
        'path': './rulesets/geosite-cn.mrs',
        'url': f'{BASE}/geo/geosite/cn.mrs',
        'proxy': 'Proxy',
    },
    'geoip-cn': {
        'type': 'http', 'behavior': 'ipcidr', 'format': 'mrs', 'interval': 86400,
        'path': './rulesets/geoip-cn.mrs',
        'url': f'{BASE}/geo/geoip/cn.mrs',
        'proxy': 'Proxy',
    },
    'ai-non-cn': {
        'type': 'http', 'behavior': 'domain', 'format': 'mrs', 'interval': 86400,
        'path': './rulesets/ai-non-cn.mrs',
        'url': f'{BASE}/geo/geosite/category-ai-!cn.mrs',
        'proxy': 'Proxy',
    },
    'dev': {
        'type': 'http', 'behavior': 'domain', 'format': 'mrs', 'interval': 86400,
        'path': './rulesets/dev.mrs',
        'url': f'{BASE}/geo/geosite/category-dev.mrs',
        'proxy': 'Proxy',
    },
    'github': {
        'type': 'http', 'behavior': 'domain', 'format': 'mrs', 'interval': 86400,
        'path': './rulesets/github.mrs',
        'url': f'{BASE}/geo/geosite/github.mrs',
        'proxy': 'Proxy',
    },
    'google': {
        'type': 'http', 'behavior': 'domain', 'format': 'mrs', 'interval': 86400,
        'path': './rulesets/google.mrs',
        'url': f'{BASE}/geo/geosite/google.mrs',
        'proxy': 'Proxy',
    },
    'cloudflare': {
        'type': 'http', 'behavior': 'domain', 'format': 'mrs', 'interval': 86400,
        'path': './rulesets/cloudflare.mrs',
        'url': f'{BASE}/geo/geosite/cloudflare.mrs',
        'proxy': 'Proxy',
    },
    'docker': {
        'type': 'http', 'behavior': 'domain', 'format': 'mrs', 'interval': 86400,
        'path': './rulesets/docker.mrs',
        'url': f'{BASE}/geo/geosite/docker.mrs',
        'proxy': 'Proxy',
    },
    'npmjs': {
        'type': 'http', 'behavior': 'domain', 'format': 'mrs', 'interval': 86400,
        'path': './rulesets/npmjs.mrs',
        'url': f'{BASE}/geo/geosite/npmjs.mrs',
        'proxy': 'Proxy',
    },
    'python': {
        'type': 'http', 'behavior': 'domain', 'format': 'mrs', 'interval': 86400,
        'path': './rulesets/python.mrs',
        'url': f'{BASE}/geo/geosite/python.mrs',
        'proxy': 'Proxy',
    },
    'telegram': {
        'type': 'http', 'behavior': 'domain', 'format': 'mrs', 'interval': 86400,
        'path': './rulesets/telegram.mrs',
        'url': f'{BASE}/geo/geosite/telegram.mrs',
        'proxy': 'Proxy',
    },
    'discord': {
        'type': 'http', 'behavior': 'domain', 'format': 'mrs', 'interval': 86400,
        'path': './rulesets/discord.mrs',
        'url': f'{BASE}/geo/geosite/discord.mrs',
        'proxy': 'Proxy',
    },
    'youtube': {
        'type': 'http', 'behavior': 'domain', 'format': 'mrs', 'interval': 86400,
        'path': './rulesets/youtube.mrs',
        'url': f'{BASE}/geo/geosite/youtube.mrs',
        'proxy': 'Proxy',
    },
}

# Make default auto pools semantically cleaner: fast/general auto excludes home-account and low-level extra fallbacks.
groups = {g['name']: g for g in data.get('proxy-groups', [])}
if 'Proxy-Auto' in groups:
    groups['Proxy-Auto']['proxies'] = [
        'hk-hy2', 'hk-reality', 'oracle-proxy-hy2-extra',
        'oracle-proxy-xray-reality-extra', 'oracle-gateway-hy2-backup',
        'ali-socks-oracle-egress', 'ali-http-oracle-egress', 'hk-socks', 'hk-http',
    ]
if 'Big-Transfer-Auto' in groups:
    groups['Big-Transfer-Auto']['proxies'] = [
        'hk-socks', 'hk-http', 'ali-socks-oracle-egress', 'ali-http-oracle-egress',
        'oracle-proxy-shadowsocks-extra', 'oracle-proxy-hy2-extra',
    ]

rules = [
    # Local/private safety first.
    'DOMAIN-SUFFIX,local,DIRECT',
    'DOMAIN-SUFFIX,lan,DIRECT',
    'RULE-SET,geosite-private,DIRECT',
    'RULE-SET,geoip-private,DIRECT,no-resolve',
    'IP-CIDR,127.0.0.0/8,DIRECT,no-resolve',
    'IP-CIDR,10.0.0.0/8,DIRECT,no-resolve',
    'IP-CIDR,172.16.0.0/12,DIRECT,no-resolve',
    'IP-CIDR,192.168.0.0/16,DIRECT,no-resolve',
    'IP-CIDR,100.64.0.0/10,DIRECT,no-resolve',

    # Account-sensitive AI/login surfaces: deliberately narrow to Home-Egress.
    'DOMAIN-SUFFIX,openai.com,Home-Egress',
    'DOMAIN-SUFFIX,chatgpt.com,Home-Egress',
    'DOMAIN-SUFFIX,oaistatic.com,Home-Egress',
    'DOMAIN-SUFFIX,oaiusercontent.com,Home-Egress',
    'DOMAIN-SUFFIX,anthropic.com,Home-Egress',
    'DOMAIN-SUFFIX,claude.ai,Home-Egress',
    'DOMAIN-SUFFIX,x.ai,Home-Egress',
    'DOMAIN-SUFFIX,grok.com,Home-Egress',
    'RULE-SET,ai-non-cn,Home-Egress',

    # Large transfer / package / model registries.
    'DOMAIN-SUFFIX,huggingface.co,Big-Transfer',
    'DOMAIN-SUFFIX,hf.co,Big-Transfer',
    'DOMAIN-SUFFIX,huggingfaceusercontent.com,Big-Transfer',
    'DOMAIN-SUFFIX,cdn-lfs.huggingface.co,Big-Transfer',
    'DOMAIN-SUFFIX,github-releases.githubusercontent.com,Big-Transfer',
    'DOMAIN-SUFFIX,objects.githubusercontent.com,Big-Transfer',
    'DOMAIN-SUFFIX,ghcr.io,Big-Transfer',
    'DOMAIN-SUFFIX,docker.com,Big-Transfer',
    'DOMAIN-SUFFIX,docker.io,Big-Transfer',
    'DOMAIN-SUFFIX,dockerusercontent.com,Big-Transfer',
    'DOMAIN-SUFFIX,quay.io,Big-Transfer',
    'DOMAIN-SUFFIX,npmjs.org,Big-Transfer',
    'DOMAIN-SUFFIX,registry.npmjs.org,Big-Transfer',
    'DOMAIN-SUFFIX,pypi.org,Big-Transfer',
    'DOMAIN-SUFFIX,pythonhosted.org,Big-Transfer',
    'DOMAIN-SUFFIX,files.pythonhosted.org,Big-Transfer',
    'RULE-SET,docker,Big-Transfer',
    'RULE-SET,npmjs,Big-Transfer',
    'RULE-SET,python,Big-Transfer',

    # Dev / infra / communication.
    'RULE-SET,github,Proxy',
    'RULE-SET,google,Proxy',
    'RULE-SET,cloudflare,Proxy',
    'RULE-SET,dev,Proxy',
    'RULE-SET,telegram,Proxy',
    'RULE-SET,discord,Proxy',
    'RULE-SET,youtube,Proxy',
    'DOMAIN-SUFFIX,gitlab.com,Proxy',
    'DOMAIN-SUFFIX,bitbucket.org,Proxy',
    'DOMAIN-SUFFIX,jsdelivr.net,Proxy',
    'DOMAIN-SUFFIX,unpkg.com,Proxy',
    'DOMAIN-SUFFIX,workers.dev,Proxy',

    # Mainland direct after explicit foreign/account/download overrides.
    'RULE-SET,geosite-cn,DIRECT',
    'RULE-SET,geoip-cn,DIRECT,no-resolve',
    'GEOSITE,CN,DIRECT',
    'GEOIP,CN,DIRECT',
    'MATCH,Proxy',
]
data['rules'] = rules

OUT.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding='utf-8')
print(f'wrote {OUT} proxies={len(data.get("proxies", []))} groups={len(data.get("proxy-groups", []))} providers={len(data.get("rule-providers", {}))} rules={len(rules)}')

# Deploy to private path only; keep old public root path untouched/404 if disabled by Caddy.
content = OUT.read_text(encoding='utf-8')
remote_py = textwrap.dedent(f'''
from pathlib import Path
import shutil, time
content = {content!r}
secret = {SECRET_PATH!r}
path = Path('/srv/drop/public') / secret / 'clash-meta.yaml'
ts = time.strftime('%Y%m%d-%H%M%S')
if not path.exists():
    raise SystemExit(f'missing expected private subscription path: {{path.parent}}/clash-meta.yaml')
backup = Path(str(path) + f'.bak-{{ts}}')
shutil.copy2(path, backup)
path.write_text(content, encoding='utf-8')
print('updated private subscription')
print('backup created')
''')
proc = subprocess.run(
    ['ssh','-o','BatchMode=yes','-o','ConnectTimeout=10','hk-relay','python3','-'],
    input=remote_py, text=True, capture_output=True,
)
print(proc.stdout, end='')
print(proc.stderr, end='')
raise SystemExit(proc.returncode)
