from pathlib import Path
import re

p = Path('/root/tavily-key-generator/email_providers/cloudflare.py')
text = p.read_text()

marker = '    def get_messages(self, address):\n'
pos = text.find(marker)
if pos == -1:
    raise SystemExit('get_messages marker not found')

# Insert an admin-read fast path inside get_messages right after try:
needle = '    def get_messages(self, address):\n        try:\n'
if needle not in text:
    raise SystemExit('needle not found')

insert = """    def get_messages(self, address):
        try:
            # 私有 worker：优先用 /admin/mails 读取（字段最全，含 raw），避免 /api/mails 结构漂移
            if self.admin_password:
                resp = self._request_with_retry(
                    'GET',
                    f"{self.api_url}/admin/mails",
                    params={'address': address, 'limit': 10, 'offset': 0},
                    headers=self._create_headers(),
                    timeout=20,
                )
                resp.raise_for_status()
                data = resp.json()
                results = data.get('results') or []

                def extract_subject(raw_text: str) -> str:
                    if not raw_text:
                        return ''
                    lines = raw_text.splitlines()
                    subj = ''
                    i = 0
                    while i < len(lines):
                        line = lines[i]
                        if line.lower().startswith('subject:'):
                            subj = line.split(':', 1)[1].strip()
                            j = i + 1
                            # header folding: subsequent lines starting with whitespace belong to subject
                            while j < len(lines) and (lines[j].startswith(' ') or lines[j].startswith('\t')):
                                subj += ' ' + lines[j].strip()
                                j += 1
                            return subj.strip()
                        i += 1
                    return ''

                out = []
                for item in results:
                    raw = item.get('raw') or ''
                    out.append({
                        'subject': extract_subject(raw),
                        'html': item.get('html') or '',
                        'text': item.get('text') or '',
                        'raw': raw,
                    })
                return out
"""

# Replace the function header with our injected version by finding the start of body.
# We'll replace only the first lines up to the previous admin/jwt logic.
start = text.find(needle)
end = start + len(needle)
text = text[:start] + insert + text[end:]

p.write_text(text)
print(f'patched {p}')
