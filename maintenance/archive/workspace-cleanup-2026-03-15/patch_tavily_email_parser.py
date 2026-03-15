from pathlib import Path

p = Path('/root/tavily-key-generator/email_providers/base.py')
text = p.read_text()

old = """    def _decode_blob(self, value):
        if not value:
            return ""
        if not isinstance(value, str):
            value = str(value)
        try:
            value = quopri.decodestring(value.encode('utf-8', errors='ignore')).decode('utf-8', errors='ignore')
        except Exception:
            pass
        value = value.replace('=\\r\\n', '').replace('=\\n', '')
        value = value.replace('&amp;', '&')
        return value
"""
new = """    def _decode_blob(self, value):
        if not value:
            return ""
        if not isinstance(value, str):
            value = str(value)
        # 先清理 quoted-printable 软换行，再做解码，避免 URL 被折断
        value = value.replace('=\\r\\n', '').replace('=\\n', '')
        try:
            value = quopri.decodestring(value.encode('utf-8', errors='ignore')).decode('utf-8', errors='ignore')
        except Exception:
            pass
        value = value.replace('&amp;', '&')
        return value
"""
if old not in text:
    raise SystemExit('old decode block not found')
text = text.replace(old, new)

old2 = """            html = self._decode_blob(msg.get(\"html\") or \"\")
            text = self._decode_blob(msg.get(\"text\") or \"\")
            raw = self._decode_blob(msg.get(\"raw\") or \"\")
            combined = \"\\n\".join([html, text, raw])

            # 优先从 href 抓
            links = re.findall(r'href=[\"\\'](https?://[^\"\\']+)[\"\\']', combined, flags=re.I)
            # 再抓裸 URL
            links += re.findall(r'https?://[^\\s<>\"\\']+', combined, flags=re.I)
"""
new2 = """            html = self._decode_blob(msg.get(\"html\") or \"\")
            text = self._decode_blob(msg.get(\"text\") or \"\")
            raw = self._decode_blob(msg.get(\"raw\") or \"\")
            combined = \"\\n\".join([html, text, raw])
            normalized = combined.replace('=3D', '=')
            normalized = normalized.replace('\\r', '')
            # 去掉 URL 中被折断的换行/空白，例如 email-\\nverification 或 ticket=\\nabc
            normalized = re.sub(r'(?<=[A-Za-z0-9:/?&._%#=-])\\n+(?=[A-Za-z0-9/_?&.%#=-])', '', normalized)
            normalized = re.sub(r'(?<=[A-Za-z0-9:/?&._%#=-])[ \\t]+(?=[A-Za-z0-9/_?&.%#=-])', '', normalized)

            # 优先从 href 抓
            links = re.findall(r'href=[\"\\'](https?://[^\"\\']+)[\"\\']', normalized, flags=re.I)
            # 再抓裸 URL
            links += re.findall(r'https?://[^\\s<>\"\\']+', normalized, flags=re.I)
"""
if old2 not in text:
    raise SystemExit('old link block not found')
text = text.replace(old2, new2)

old3 = """            for link in dedup:
                link_lower = link.lower()
"""
new3 = """            for link in dedup:
                link = link.strip().strip(\"()[]{}<>.,;\\\"'\")
                link_lower = link.lower()
"""
if old3 not in text:
    raise SystemExit('old cleanup block not found')
text = text.replace(old3, new3)

p.write_text(text)
print(f'patched {p}')
