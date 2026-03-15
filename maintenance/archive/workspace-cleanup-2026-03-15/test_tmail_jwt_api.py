import requests, json
BASE='https://tmail.zhangxuemin.work'
HEADERS={'x-admin-auth':'Zxm971004','x-custom-auth':'Zxm971004','x-site-password':'Zxm971004','Content-Type':'application/json'}
# create a fresh address to inspect schema
resp=requests.post(BASE+'/admin/new_address', json={'enablePrefix': True, 'name': 'apitestmailbox', 'domain': 'zhangxuemin.work'}, headers=HEADERS, timeout=30)
print('CREATE', resp.status_code)
print(resp.text[:1000])
data=resp.json()
jwt=data.get('jwt')
addr=data.get('address')
print('ADDR', addr)
if jwt:
    r=requests.get(BASE+'/api/mails', params={'limit': 10, 'offset': 0}, headers={'Authorization': f'Bearer {jwt}','x-custom-auth':'Zxm971004','x-site-password':'Zxm971004','Content-Type':'application/json'}, timeout=30)
    print('API_MAILS', r.status_code)
    print(r.text[:2000])
