import requests
import quopri
import re
from email_providers.base import EmailProvider

ADDR = 'tmailtavilybfiopzoz@zhangxuemin.work'
BASE = 'https://tmail.zhangxuemin.work'
HEADERS = {
    'x-admin-auth': 'Zxm971004',
    'x-custom-auth': 'Zxm971004',
    'x-site-password': 'Zxm971004',
}

class T(EmailProvider):
    def create_email(self, prefix=None):
        raise NotImplementedError
    def get_messages(self, address):
        raise NotImplementedError

r = requests.get(BASE + '/admin/mails', params={'address': ADDR, 'limit': 1, 'offset': 0}, headers=HEADERS, timeout=30)
r.raise_for_status()
msg = r.json()['results'][0]
raw = msg.get('raw') or ''
print('RAW_LEN', len(raw))
print('RAW_HAS_email_verification', 'email-verification' in raw)
print('RAW_HAS_ticket', 'ticket=' in raw)

normalized_before_decode = raw.replace('=\r\n', '').replace('=\n', '')
decoded = quopri.decodestring(normalized_before_decode.encode('utf-8', 'ignore')).decode('utf-8', 'ignore')
print('DEC_HAS_email_verification', 'email-verification' in decoded)
print('DEC_HAS_ticket', 'ticket=' in decoded)

urls = re.findall(r'https?://[^\s<>"\']+', decoded, flags=re.I)
print('URL_COUNT', len(urls))
for u in urls[:20]:
    print('URL', u)

idx = decoded.find('email-verification')
print('IDX', idx)
if idx != -1:
    print(decoded[max(0, idx-200):idx+500])

parser = T()
messages = [{
    'subject': 'Verify your email',
    'html': msg.get('html') or '',
    'text': msg.get('text') or '',
    'raw': raw,
}]
print('PARSER_LINK', parser.find_verification_link(messages))
