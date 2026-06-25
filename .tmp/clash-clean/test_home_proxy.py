import yaml, subprocess, time
from urllib.parse import quote

cfg = yaml.safe_load(open('/root/.openclaw/workspace/.tmp/clash-clean/live-full.yaml', encoding='utf-8'))
proxies = {p['name']: p for p in cfg.get('proxies', [])}

for name in ['home-http-direct', 'home-http-via-hk']:
    p = proxies.get(name)
    if not p:
        print(f'{name}: missing')
        continue
    user = quote(str(p.get('username', '')), safe='')
    pw = quote(str(p.get('password', '')), safe='')
    proxy_url = f"http://{user}:{pw}@{p['server']}:{p['port']}"
    print(f'== {name} ==')
    for target in ['https://api.ipify.org', 'https://www.google.com/generate_204']:
        cp = subprocess.run([
            'curl', '-sS', '-L', '--max-time', '20',
            '-o', '/tmp/home_proxy_test.out',
            '-w', 'http_code=%{http_code} time=%{time_total} remote=%{remote_ip}\n',
            '-x', proxy_url, target,
        ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            body = open('/tmp/home_proxy_test.out', 'rb').read(200).decode('utf-8', 'replace').strip()
        except Exception:
            body = ''
        msg = f'{target} rc={cp.returncode} {cp.stdout.strip()}'
        if target.endswith('api.ipify.org'):
            msg += f' body={body}'
        print(msg)
        if cp.stderr.strip():
            print('stderr=' + cp.stderr.strip()[:200])
