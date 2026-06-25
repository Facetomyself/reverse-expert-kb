import io, json, os, shutil, time

files = [
    '/opt/1panel/apps/astrbot/astrbot/data/cmd_config.json',
    '/opt/1panel/apps/astrbot/astrbot/data/config/abconf_dd547db0-c864-43a8-a0a7-46675d251c52.json',
]
proxy = None
with open('/etc/profile.d/ali-proxy.sh', 'r') as f:
    for line in f:
        s = line.strip()
        if s.startswith('export HTTP_PROXY='):
            proxy = s.split('=', 1)[1].strip().strip('"').strip("'")
            break
if not proxy:
    raise SystemExit('proxy not found')

print('proxy=', proxy)
for p in files:
    bak = p + '.bak-' + time.strftime('%Y%m%d-%H%M%S')
    shutil.copy2(p, bak)
    with io.open(p, 'r', encoding='utf-8-sig') as f:
        conf = json.load(f)
    changed = 0
    for src in conf.get('provider_sources', []):
        if src.get('type') == 'openai_chat_completion' or src.get('provider') == 'openai' or src.get('id') == 'openai':
            if src.get('proxy') != proxy:
                src['proxy'] = proxy
                changed = 1
    with io.open(p, 'w', encoding='utf-8') as f:
        json.dump(conf, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(p, 'changed=', changed, 'backup=', bak)

for p in files:
    with io.open(p, 'r', encoding='utf-8-sig') as f:
        conf = json.load(f)
    print('FILE', p)
    for src in conf.get('provider_sources', []):
        print(src.get('id'), src.get('proxy'))
