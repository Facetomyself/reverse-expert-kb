import io, json, subprocess

with io.open('/opt/1panel/apps/astrbot/astrbot/data/cmd_config.json', 'r', encoding='utf-8-sig') as f:
    conf = json.load(f)

key = conf['provider_sources'][0]['key'][0]
url = conf['provider_sources'][0]['api_base'].rstrip('/') + '/models'
proxy = None
with open('/etc/profile.d/ali-proxy.sh', 'r') as f:
    for line in f:
        s = line.strip()
        if s.startswith('export HTTP_PROXY='):
            proxy = s.split('=', 1)[1].strip().strip('"').strip("'")
            break

fmt = 'lookup=%{time_namelookup} connect=%{time_connect} start=%{time_starttransfer} total=%{time_total} code=%{http_code}\n'

def run(cmd):
    return subprocess.check_output(cmd).decode('utf-8', 'ignore').strip()

base = ['curl', '-sS', '-o', '/dev/null', '-w', fmt, '--max-time', '20', '-H', 'Authorization: Bearer ' + key, url]
print('DIRECT')
for _ in range(3):
    print(run(base))

print('PROXY', proxy if proxy else 'missing')
if proxy:
    via = ['curl', '-x', proxy, '-sS', '-o', '/dev/null', '-w', fmt, '--max-time', '20', '-H', 'Authorization: Bearer ' + key, url]
    for _ in range(3):
        print(run(via))
